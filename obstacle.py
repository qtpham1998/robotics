#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running a motor to a target position set by the encoder of another motor.
#
# Hardware: Connect EV3 or NXT motors to the BrickPi3 motor ports B and C. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, motor C power will be controlled by the position of motor B. Manually rotate motor B, and motor C's power will change.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import math

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
# Motor ports
rightMotor = BP.PORT_
leftMotor = BP.PORT_
# Sensor ports 
rightSensor = BP.PORT_
leftSensor = BP.PORT_

def moveForward(dist): # distance in cm
    try:
        print("forward")
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    except IOError as error:
        print (error)
    targetDist = calculateTargetDistance(dist) 
    BP.set_motor_limits(BP.PORT_B, 70, 200)
    BP.set_motor_limits(BP.PORT_C, 70, 200)
    BP.set_motor_position(BP.PORT_B, targetDist)
    BP.set_motor_position(BP.PORT_C, targetDist)

def wait():
    print("waiting")
    time.sleep(1)
    vB = BP.get_motor_status(BP.PORT_B)[3]
    vC = BP.get_motor_status(BP.PORT_C)[3]
    while(vB != 0 or vC != 0):
        vB = BP.get_motor_status(BP.PORT_B)[3]
        vC = BP.get_motor_status(BP.PORT_C)[3]
    print("wait finished")


def rotateDegree(degrees):
    print("rotate")
    try:
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    except IOError as error:
        print (error)
    pos = calculateTargetDistance(degrees / 360 * 12.699999 * math.pi)
    print(pos)
    BP.set_motor_position(BP.PORT_C, -pos)
    BP.set_motor_position(BP.PORT_B, pos)

def initialise():
    BP.set_sensor_type(leftSensor, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(rightSensor, BP.SENSOR_TYPE.TOUCH)
    

try:
    initialise()
    moveForward()
    while True:
        try:
            leftSense = BP.get_sensor(leftSensor)
            rightSense = BP.get_sensor(rightSensor)
            if (leftSense == 1 and rightSense == 1):
                moveBack()
            elif (leftSense == 1):
                turnRight()
            elif (rightSense == 1):
                turnLeft()
        except brickpi3.SensorError as error:
            print(error)
        wait()


except KeyboardInterrupt:
    BP.reset_all()
