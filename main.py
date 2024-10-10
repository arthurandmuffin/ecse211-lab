#!/usr/bin/env python3

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep

MOTOR = Motor("A")

TOUCH_SENSOR = TouchSensor(1)
FLUTE_SENSOR = TouchSensor(2)
US_SENSOR = EV3UltrasonicSensor(3)
KILL_SWITCH = TouchSensor(4)

PITCHES = {10 : "A5", 20 : "B5", 30 : "C5", 40 : "D5"}
DISTANCES = [10, 20, 30, 40]

wait_ready_sensors(True)

def flute():
    while True:
        dist = US_SENSOR.get_value()
        distance = min(DISTANCES, key=lambda x: abs(dist - x))
        if FLUTE_SENSOR.is_pressed():
            sound.Sound(duration=0.1, pitch=PITCHES[distance], volume=150).play()
            sleep(1)
        if KILL_SWITCH.is_pressed():
            MOTOR.set_power(0)
            return

def drum():
    MOTOR.set_dps(60)
    MOTOR.set_power(50)

def program():
    try:
        while not TOUCH_SENSOR.is_pressed():
            pass
        drum()
        flute()
    finally:
        reset_brick()
        exit()

if __name__ == "__main__":
    program()