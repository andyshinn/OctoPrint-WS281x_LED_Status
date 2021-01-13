# -*- coding: utf-8 -*-

defaults = {
    "debug_logging": False,
    "led_count": 24,
    "led_pin": 10,
    "led_freq_hz": 800000,
    "led_dma": 10,
    "led_invert": False,
    "led_brightness": 50,
    "led_channel": 0,
    "strip_type": "WS2811_STRIP_GRB",
    "reverse": False,
    "startup_enabled": True,
    "startup_effect": "Color Wipe",
    "startup_color": "#00ff00",
    "startup_delay": "75",
    "idle_enabled": True,
    "idle_effect": "Color Wipe 2",
    "idle_color": "#00ccf0",
    "idle_delay": "75",
    "disconnected_enabled": True,
    "disconnected_effect": "Rainbow Cycle",
    "disconnected_color": "#000000",
    "disconnected_delay": "25",
    "failed_enabled": True,
    "failed_effect": "Pulse",
    "failed_color": "#ff0000",
    "failed_delay": "10",
    "success_enabled": True,
    "success_effect": "Rainbow",
    "success_color": "#000000",
    "success_delay": "25",
    "success_return_idle": "0",
    "paused_enabled": True,
    "paused_effect": "Bounce",
    "paused_color": "#0000ff",
    "paused_delay": "40",
    "progress_print_enabled": True,
    "progress_print_color_base": "#000000",
    "progress_print_color": "#00ff00",
    "printing_enabled": False,
    "printing_effect": "Solid Color",
    "printing_color": "#ffffff",
    "printing_delay": 1,
    "progress_heatup_enabled": True,
    "progress_heatup_color_base": "#0000ff",
    "progress_heatup_color": "#ff0000",
    "progress_heatup_tool_enabled": True,
    "progress_heatup_bed_enabled": True,
    "progress_heatup_tool_key": 0,
    "progress_cooling_enabled": True,
    "progress_cooling_color_base": "#0000ff",
    "progress_cooling_color": "#ff0000",
    "progress_cooling_bed_or_tool": "tool",
    "progress_cooling_threshold": "40",
    "progress_temp_start": 0,
    "torch_enabled": True,
    "torch_effect": "Solid Color",
    "torch_color": "#ffffff",
    "torch_delay": 1,
    "torch_timer": 15,
    "torch_toggle": False,
    "active_hours_enabled": False,
    "active_hours_start": "09:00",
    "active_hours_stop": "21:00",
    "at_command_reaction": True,
    "intercept_m150": True,
}