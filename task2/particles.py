from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import random
from math import pi, cos, sin, atan2, sqrt
from os import system

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
NUMBER_OF_PARTICLES = 100
OFFSETX = 400
OFFSETY = 200
MULT = 10
particleSet = []

class Particle:
    def __init__(self, x, y, theta, size,w=1/NUMBER_OF_PARTICLES):
        self.x = x
        self.y = y
        self.theta = theta
        self.size = size
        self.w = w

    def calcX(self, dist):
        return self.x + (dist + random.gauss(0, 0.5)) * cos(self.theta / 180 * pi)

    def calcY(self, dist):
        return self.y + (dist + random.gauss(0, 0.5)) * sin(self.theta / 180 * pi)

    def calcTheta(self, degrees):
        return self.theta - (degrees + random.gauss(0, 1.5)) 
    
    def updateParticleCoords(self, dist):
        #return Particle(self.calcX(dist), self.calcY(dist), self.theta)
        return updateParticle(self, dist, None)
    
    def updateParticleAngle(self, degrees):
        #return Particle(self.x, self.y, self.calcTheta(degrees))
        return updateParticle(self, None, degrees)

    def updateParticle(self, dist, degrees):
        x = self.x
        y = self.y
        theta = self.theta
        if(dist != None):
            x = self.calcX(dist)
            y = self.calcY(dist)
            theta = self.calcTheta(0)
        if(degrees != None):
            theta = self.calcTheta(degrees)
        return Particle(x, y, theta, self.size)
        
    def getCoords(self):
        return (self.x * MULT + OFFSETX, self.y * MULT + OFFSETY + self.size * MULT * 4 , self.theta)

def initialise(size):
    system('clear')
    for i in range(NUMBER_OF_PARTICLES):
        particleSet.append(Particle(0,0,0,size))
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)

def calculateTargetDistance(dist):
    return (dist / (7 * pi)) * 360

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
    pos = calculateTargetDistance(degrees / 360 * 13.0 * pi)
    BP.set_motor_position(rightMotor, pos)
    BP.set_motor_position(leftMotor, -pos)
    updateParticles(None, degrees)
    
def moveLine(interval, dist):
    while (dist >= interval):
        moveForward(interval)
        wait()
        updateParticles(interval, None)
        dist -= interval
    if(dist > 0):
        moveForward(dist)
        wait()
        updateParticles(dist, None)
        
def getAverageCoordinate():
    xCoord = 0
    yCoord = 0
    theta = 0
    for i in range(len(particleSet)):
        xCoord += particleSet[i].x
        yCoord += particleSet[i].y
        theta += particleSet[i].theta
    return (xCoord/ NUMBER_OF_PARTICLES, yCoord/ NUMBER_OF_PARTICLES, theta/ NUMBER_OF_PARTICLES)        
        

def updateParticles(dist, degrees):
    for i in range(len(particleSet)):
        particleSet[i] = particleSet[i].updateParticle(dist, degrees)
    drawParticleSet()
    #newSet = []
    #for p in particleSet:
    #    newSet.append(p.updateParticle(dist, degrees))
    #particleSet =  newSet

def moveSquare(num, size):
    for n in range(num):
        for i in range(4):
            moveLine(size, 40)
            wait()
            rotateDegree(90)
            wait()

def coordAxis():
    print("drawLine:" + str((0, 0, 0, 5000)))
    print("drawLine:" + str((0, 0, 5000, 0)))
          
def drawSquare(size):
    diff = size * MULT * 4
    print("drawLine:" + str((OFFSETX, OFFSETY, OFFSETX, OFFSETY + diff)))
    print("drawLine:" + str((OFFSETX, OFFSETY, OFFSETX + diff, OFFSETY)))
    print("drawLine:" + str((OFFSETX + diff, OFFSETY, OFFSETX + diff, OFFSETY + diff)))
    print("drawLine:" + str((OFFSETX, OFFSETY + diff, OFFSETX + diff, OFFSETY + diff)))
    
def drawParticleSet():
    particles = [p.getCoords() for p in particleSet]
    print("drawParticles:" + str(particles))
    
    
def navigateToWaypoint(X,Y):
    coordinates = getAverageCoordinate()
    xCoordinate = coordinates[0]
    print("the current X coordinate is " + str(xCoordinate))
    yCoordinate = coordinates[1]
    print("the current Y coordinate is " + str(yCoordinate))
    theta = coordinates[2]
    print("the current angle is " + str(theta))
    xDiff = abs(X*100 - xCoordinate)
    yDiff = abs(Y*100 - yCoordinate)
    newTheta = atan2(yDiff, xDiff) * 180 / pi
    degree = 0
    if(X * 100 > xCoordinate and Y * 100 < yCoordinate):
        newTheta = -1 * newTheta
    elif(X * 100 < xCoordinate and Y * 100 < yCoordinate):
        newTheta = -180 + newTheta
    elif(X * 100 < xCoordinate and Y * 100 > yCoordinate):
        newTheta = 180 - newTheta
    
    if(theta < newTheta):
            degree = newTheta - theta
    else:
            degree = 360 - (theta - newTheta)
    if degree % 360 != 0:                          
        rotateDegree(degree % 360)
    wait()
    moveLine(10, sqrt(xDiff * xDiff + yDiff * yDiff))
            
        
        
    
def navigate():
    while(True):
        print("Do you want to start now? Press N to stop, any other key to start")
        start = raw_input()
        if(start == "N"):
            break
        print("Please enter an X coordinate in meters")
        x = input()
        print("Please input an Y coordinate in meters")
        y = input()
        navigateToWaypoint(x,y)
        
    

try:
    initialise(10)
    navigate() 
    #drawSquare(10)
    #moveSquare(1, 10)


except KeyboardInterrupt:
    BP.reset_all()
