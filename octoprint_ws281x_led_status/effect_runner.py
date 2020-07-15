# run the effect, handle switching from queue.
# Should be run as a thread
from __future__ import absolute_import, unicode_literals

import time

import rpi_ws281x
from rpi_ws281x import PixelStrip

from octoprint_ws281x_led_status.effects import basic, progress
from octoprint_ws281x_led_status.util import hex_to_rgb

KILL_MSG = 'KILL'
STRIP_SETTINGS = [  # ALL LED SETTINGS, for rpi_ws281x.PixelStrip
    'led_count',
    'led_pin',
    'led_freq_hz',
    'led_dma',
    'led_invert',
    'led_brightness',
    'led_channel',
    'strip_type'
]
STRIP_TYPES = {  # Add more here once we get going....
    'WS2811_STRIP_GRB': rpi_ws281x.WS2811_STRIP_GRB,
    'WS2812_STRIP': rpi_ws281x.WS2812_STRIP,
    'WS2811_STRIP_RGB': rpi_ws281x.WS2811_STRIP_RGB,
    'WS2811_STRIP_RBG': rpi_ws281x.WS2811_STRIP_RBG,
    'WS2811_STRIP_GBR': rpi_ws281x.WS2811_STRIP_GBR,
    'WS2811_STRIP_BGR': rpi_ws281x.WS2811_STRIP_BGR,
    'WS2811_STRIP_BRG': rpi_ws281x.WS2811_STRIP_BRG,
}
EFFECTS = {  # Add more here once we get going....
    'solid': basic.solid_color,
    'wipe': basic.color_wipe,
    'wipe2': basic.color_wipe_2,
    'pulse': basic.simple_pulse,
    'rainbow': basic.rainbow,
    'cycle': basic.rainbow_cycle,
    'bounce': basic.bounce,
    'progress_print': progress.progress,
    'progress_heatup': progress.progress
}
MODES = [  # Add more here once we get going....
    'startup',
    'idle',
    'disconnected',
    'progress_print',
    'progress_heatup',
    'failed',
    'success',
    'paused'
]


def effect_runner(logger, queue, all_settings, previous_state):
    def on_exit(led_strip):
        EFFECTS['solid'](strip, queue, [0, 0, 0])

    print("[RUNNER] Hello!")
    # start strip, run startup effect until we get something else
    strip = start_strip(logger, all_settings['strip'])
    if not strip:
        print("[RUNNER] Exiting effect runner")
        return

    start_time = all_settings['active_start'].split(":") if all_settings['active_start'] else None
    end_time = all_settings['active_stop'].split(":") if all_settings['active_stop'] else None

    msg = previous_state
    try:
        while True:
            if not queue.empty():
                msg = queue.get()  # The ONLY place the queue should be 'got'
            if msg:
                msg_split = msg.split()
                # Run messaged effect
                if msg == KILL_MSG:
                    print("[RUNNER] Received KILL message")
                    on_exit(strip)
                    return
                else:
                    if check_times(start_time, end_time) and msg_split[0] in MODES:
                        effect_settings = all_settings[msg_split[0]]  # dict containing 'enabled', 'effect', 'color', 'delay'/'base'
                        if 'progress' in msg:
                            value = msg_split[1]
                            EFFECTS[msg_split[0]](strip, queue, int(value), hex_to_rgb(effect_settings['color']),
                                                  hex_to_rgb(effect_settings['base']), all_settings['strip']['led_brightness'])
                        else:
                            EFFECTS[effect_settings['effect']](strip, queue, hex_to_rgb(effect_settings['color']),
                                                               effect_settings['delay'], all_settings['strip']['led_brightness'])

                    elif not check_times(start_time, end_time):
                        EFFECTS['solid'](strip, queue, [0, 0, 0])
                        time.sleep(0.1)
                    else:
                        time.sleep(0.1)
            elif check_times(start_time, end_time):
                effect_settings = all_settings['startup']
                if effect_settings['enabled']:
                    # Run startup effect (We haven't got a message yet)
                    EFFECTS[effect_settings['effect']](strip, queue, hex_to_rgb(effect_settings['color']),
                                                       effect_settings['delay'], all_settings['strip']['led_brightness'])
                if not queue.empty():
                    time.sleep(0.1)
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        on_exit(strip)
        return


def start_strip(logger, strip_settings):
    try:
        strip = PixelStrip(
            num=strip_settings['led_count'],
            pin=strip_settings['led_pin'],
            freq_hz=strip_settings['led_freq_hz'],
            dma=strip_settings['led_dma'],
            invert=strip_settings['led_invert'],
            brightness=strip_settings['led_brightness'],
            channel=strip_settings['led_channel'],
            strip_type=STRIP_TYPES[strip_settings['strip_type']]
        )
        strip.begin()
        print("Strip object initialised")
        return strip
    except Exception as e:  # Probably wrong settings...
        print("[RUNNER] Strip failed to initialize, no effects will be run.")
        print("[RUNNER] Exception: {}".format(e))
        return None


def check_times(start_time, end_time):
    """
    Return true if time is after start, before end, false if outside
    Times should be list, format [hh,mm]
    """
    if not start_time or not end_time:
        return True
    current_time = time.ctime(time.time()).split()[3].split(":")
    ct_mins = (int(current_time[0]) * 60) + int(current_time[1])
    st_mins = (int(start_time[0]) * 60) + int(start_time[1])
    et_mins = (int(end_time[0]) * 60) + int(end_time[1])

    return st_mins <= ct_mins < et_mins


class FakeStrip:
    def __init__(self, num, pin, freq_hz, dma, invert, brightness, channel, strip_type):
        self.pixels = num
        self.pin = pin
        self.freq_hz = freq_hz
        self.dma = dma
        self.invert = invert
        self.brightness = brightness
        self.channel = channel
        self.strip_type = strip_type

    def numPixels(self):
        return self.pixels

    def begin(self):
        pass

    def show(self):
        pass

    def setPixelColorRGB(self, num, red, green, blue, white=0):
        pass

    def _cleanup(self):
        print("Cleaning up FakeStrip")
        pass
