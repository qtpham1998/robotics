from math import pi
import time
import MCL

class Movement:

    def __init__(self, bp, mcl, sensor):
        self.BP = bp
        self.leftMotor = bp.PORT_B
        self.rightMotor = bp.PORT_C
        self.MCL = mcl
        self.sensor = sensor
        self.initialise()

    def initialise(self):
        self.BP.set_motor_limits(self.leftMotor, 70, 350)
        self.BP.set_motor_limits(self.rightMotor, 70, 350)

    def calculateTargetDistance(self, dist):
        '''
        Calculates the motor position needed to travel given distance
        @param dist The distance to travel
        @return The needed motor position
        '''
        return (dist / (7 * pi)) * 360

    def resetEncoder(self):
        '''
        Reset the motor encoder offset
        @throws IOError
        '''
        try:
            self.BP.offset_motor_encoder(self.leftMotor, self.BP.get_motor_encoder(self.leftMotor))
            self.BP.offset_motor_encoder(self.rightMotor, self.BP.get_motor_encoder(self.rightMotor))
        except IOError as error:
            print (error)

    def getMotorDps(self):
        '''
        Gets the motor velocity (dps)
        @return Left motor velocity, Right motor velocity
        '''
        return self.BP.get_motor_status(self.leftMotor)[3], self.BP.get_motor_status(self.rightMotor)[3]
    
    def setMotorPosition(self, left, right):
        self.BP.set_motor_position(self.rightMotor, left)
        self.BP.set_motor_position(self.leftMotor, right)
        self.wait()
        
    def getMotorPosition(self):
        return self.BP.get_motor_encoder(self.leftMotor), self.BP.get_motor_encoder(self.rightMotor)

    def touchObstacle(self, dps):
        start, _ = self.getMotorPosition()
        
        self.BP.set_motor_dps(self.leftMotor, dps)
        self.BP.set_motor_dps(self.rightMotor, dps)
        
        leftReading, rightReading = self.sensor.getTouchSensorReading()
        while(leftReading != 1 and rightReading != 1):
            leftReading, rightReading = self.sensor.getTouchSensorReading()
        
        end, _ = self.getMotorPosition()
            
        self.BP.set_motor_dps(self.leftMotor, 0)
        self.BP.set_motor_dps(self.rightMotor, 0)
        
        self.resetEncoder()
        dist = start - end
        self.setMotorPosition(dist, dist)

    def wait(self):
        '''
        Waits for the robot to stop moving
        '''
        #print("Waiting for robot to stop.")
        time.sleep(0.5)
        vLeft, vRight = self.getMotorDps()
        while(vLeft != 0 or vRight != 0):
            vLeft, vRight = self.getMotorDps()
        #print("Wait finished")

    def moveForward(self, dist, update): #distance in cm
        '''
        Moves forward for a given distance
        @param dist The distance to move
        '''
        self.resetEncoder()
        targetDist = self.calculateTargetDistance(dist) 
        self.setMotorPosition(-targetDist, -targetDist)
        if update:
            self.MCL.updateParticles(dist, 0)

    def rotateDegree(self, degrees):
        '''
        Rotates left a certain number of degrees
        @param degrees The angle to rotate
        '''
        self.resetEncoder()
        pos = self.calculateTargetDistance(degrees * 13 * pi / 360)         
        self.setMotorPosition(-pos, pos)
        self.MCL.updateParticles(0, degrees)

    def moveLine(self, dist, interval):
        '''
        Moves 'dist' metres in intervals of 'interval'
        @param interval Distance to move at a time
        @param dist Total distance to move
        '''
        print("Moving forward %d cm" %dist)
        while (dist >= interval):
            self.moveForward(interval)
            dist -= interval
        if (dist > 0):
            self.moveForward(dist)
            
