from __future__ import print_function
from enum import Enum

pins = {
    'button_1': 14,
    'led_1_red': 18,
    'led_1_green': 17,
    'led_1_blue': 27,
}
colors = {
    'red_light': 0x220000,
    'red': 0xFF0000,
    'green': 0x00FF00,
    'blue': 0x0000FF,
}

class SystemStatus(Enum):
    READY = colors['green']
    RECORDING = colors['red']
    CAPTURED = colors['red_light']

def log(*args):
    print(args)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

