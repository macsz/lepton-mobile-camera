#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
from timeit import default_timer as timer

from enum import Enum
from tools import log, map, pins, SystemStatus, colors

def setColor(color):
    if issubclass(SystemStatus, Enum):
        color = color.value
    R_val = (color & 0xFF0000) >> 16
    G_val = (color & 0x00FF00) >> 8
    B_val = (color & 0x0000FF) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)

    log("color_msg: R_val = %s,   G_val = %s,     B_val = %s"%(R_val, G_val, B_val))

system_status = SystemStatus.READY

def setup():
    global p_R, p_G, p_B
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins['button_1'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pins['button_1'], GPIO.FALLING, callback=swLed, bouncetime=1000)

    for pin_led in [pins[pin_led] for pin_led in pins if pin_led.startswith('led')]:
        log('Setting', pin_led)
        GPIO.setup(pin_led, GPIO.OUT, initial=GPIO.HIGH)
    p_R = GPIO.PWM(pins['led_1_red'], 2000)
    p_G = GPIO.PWM(pins['led_1_green'], 2000)
    p_B = GPIO.PWM(pins['led_1_blue'], 2000)

    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

    setColor(SystemStatus.READY)

def swLed(ev=None):
    global system_status
    if system_status is SystemStatus.READY:
        system_status = SystemStatus.RECORDING
    else:
        system_status = SystemStatus.READY
    setColor(system_status)
    log(system_status)

def main():
    while True:
        if system_status is SystemStatus.RECORDING:
            time_start = timer()
            cmd = ["camera/capture/capture.exe"]
            setColor(SystemStatus.CAPTURED)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            setColor(SystemStatus.RECORDING)
            time_stop = timer()
            print('Captured in', time_stop - time_start)
            time.sleep(0.2)
        else:
            time.sleep(1)

def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    try:
        GPIO.output(pins, GPIO.HIGH)
    except TypeError, ValueError:
        #TODO fix
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
