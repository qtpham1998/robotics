from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
from math import pi, cos, sin
import random

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

NUMBER_OF_PARTICLES = 100
particleSet = []
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C

class Particle:
    def __init__(self, x, y, theta, w=1/NUMBER_OF_PARTICLES):
        self.x = x
        self.y = y
        self.theta = theta
        self.w = w

    def calcX(dist):
        return self.x + (dist + random.gauss(0, 5)) * cos(self.theta / 180 * pi)

    def calcY(dist):
        return self.y + (dist + random.gauss(0, 5)) * sin(self.theta / 180 * pi)

    def calcTheta():
        return self.theta + random.gauss(0, 5)

    def generateParticleLine(dist):
        return Particle(self.calcX(dist), self.calcY(dist), self.theta)

    def generateParticleRotate(degrees):
        return Particle(self.x, self.y, self.calcTheta(degrees))

    def getCoords():
        return (self.x, self.y, self.theta)

def initialise():
    particleSet = [Particle(0,0,0) for i in range(NUMBER_OF_PARTICLES)]
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)

def calculateTargetDistance(dist):
    return 1.5 * (dist / (7.3 * math.pi)) * 360

def resetEncoder():
    try:
        BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
        BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    except IOError as error:
        print (error)

def getMotorDps():
    return BP.get_motor_status(leftMotor)[3], BP.get_motor_status(rightMotor)[3]

def wait():
    print("Waiting for robot to stop.")
    time.sleep(1)
    vLeft, vRight = getMotorDps()
    while(vLeft != 0 or vRight != 0):
        vLeft, vRight = getMotorDps()
    print("Wait finished")

def moveForward(dist): # distance in cm
    print("Moving forward %d cm" %dist)
    resetEncoder()
    targetDist = calculateTargetDistance(dist) 
    BP.set_motor_position(leftMotor, -targetDist)
    BP.set_motor_position(rightMotor, -targetDist)

def rotateDegree(degrees):
    print("Rotating %d degrees" %degrees)
    resetEncoder()
    pos = calculateTargetDistance(degrees / 360 * 14 * math.pi)
    BP.set_motor_position(rightMotor, pos)
    BP.set_motor_position(leftMotor, -pos)

def moveLine(dist):
    for i in range(4):
        moveForward(dist)
        wait()
        #calculate new particles

def moveSquare(num):
    for n in range(num):
        for i in range(4):
            moveLine(10)
            wait()
            rotateDegree(90)
            wait()

def coordAxis:
    print("drawLine:" + str())

def drawParticleSet:
    particles = [p.getCoords() for p in range particleSet]
    print("drawParticles:" + str(particles))

try:
    initialise()
    moveSquare(1)


except KeyboardInterrupt:
    BP.reset_all()