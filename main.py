#!/usr/bin/env python3

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors, Motor, reset_brick
from time import sleep

MOTOR = Motor("D")

#Set up touch sensors and ultrasonic sensors to respective ports
TOUCH_SENSOR = TouchSensor(2)
FLUTE_SENSOR = TouchSensor(3)
US_SENSOR = EV3UltrasonicSensor(4)
KILL_SWITCH = TouchSensor(1)

#Dictionary of notes and corresponding distances from the ultrasonic sensor
PITCHES = {5 : "C4", 7.3 : "D4", 9.1 : "E4", 10.4 : "F4", 12.1 : "G4", 13.9 : "A4", 15.6 : "B4",
           17.5 : "C5", 18.8 : "D5", 20.3 : "E5", 21.9 : "F5", 23.7 : "G5", 25.9 : "A5", 28.1 : "B5", 30.6 : "C6"}
DISTANCES = [5, 7.3, 9.1, 10.4, 12.1, 13.9, 15.6, 17.5, 18.8, 20.3, 21.9, 23.7, 25.9, 28.1, 30.6]

wait_ready_sensors(True)
print("System Ready")

def flute():
    dist = US_SENSOR.get_value()
    #Convert measured distance to the closest distance that corresponds to a note
    distance = min(DISTANCES, key=lambda x: abs(dist - x))
    #When corresponding touch sensor pressed, play note. Different volume to compensate for higher notes due to inheritent speaker traits
    if FLUTE_SENSOR.is_pressed():
        if distance < 17.5:
            sound.Sound(duration=.1, pitch=PITCHES[distance], volume=90).play()
            print(PITCHES[distance])
        else:
            sound.Sound(duration=.1, pitch=PITCHES[distance], volume=85).play()
            print(PITCHES[distance])
        sleep(1)


def drum():
    #When touch sensor pressed, start or stop motor based on current status
    if TOUCH_SENSOR.is_pressed() and not MOTOR.is_moving():
        MOTOR.set_dps(60)
        MOTOR.set_power(50)
        sleep(.25)
    elif TOUCH_SENSOR.is_pressed() and MOTOR.is_moving():
        MOTOR.set_power(0)
        sleep(.25)

def program():
    try:
        #Kill switch logic, drum and flute subsystem continuously loops before kill switch is pressed
        while not KILL_SWITCH.is_pressed(): 
            drum()
            flute()
        #In case motor is currently active, stop the motor
        MOTOR.set_power(0)
    finally:
        reset_brick()
        exit()

if __name__ == "__main__":
    program()