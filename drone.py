import RPi.GPIO as GPIO
from time import sleep

#GPIO Pin Assignments
w1Pin1 = 24
w1Pin2 = 23
w2Pin1 = 22
w2Pin2 = 27
w3Pin1 = 20
w3Pin2 = 21
w4Pin1 = 19
w4Pin2 = 26
frontWheelsPWMPin = 25
frontOtherWheelPWMPin = 17
backWheelsPWMPin = 16
backWheelOtherPWMPin = 13

#setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(w1Pin1, GPIO.OUT)
GPIO.setup(w1Pin2, GPIO.OUT)
GPIO.setup(w2Pin1, GPIO.OUT)
GPIO.setup(w2Pin2, GPIO.OUT)
GPIO.setup(w3Pin1, GPIO.OUT)
GPIO.setup(w3Pin2, GPIO.OUT)
GPIO.setup(w4Pin1, GPIO.OUT)
GPIO.setup(w4Pin2, GPIO.OUT)
GPIO.setup(frontWheelsPWMPin, GPIO.OUT)
GPIO.setup(frontOtherWheelPWMPin, GPIO.OUT)
GPIO.setup(backWheelsPWMPin, GPIO.OUT)
GPIO.setup(backWheelOtherPWMPin, GPIO.OUT)

#Set all pins to LOW
GPIO.output(w1Pin1, GPIO.LOW)
GPIO.output(w1Pin2, GPIO.LOW)
GPIO.output(w2Pin1, GPIO.LOW)
GPIO.output(w2Pin2, GPIO.LOW)
GPIO.output(w3Pin1, GPIO.LOW)
GPIO.output(w3Pin2, GPIO.LOW)
GPIO.output(w4Pin1, GPIO.LOW)
GPIO.output(w4Pin2, GPIO.LOW)

#Set PWM Pins
pFront = GPIO.PWM(frontWheelsPWMPin, 1000)
pFrontOther = GPIO.PWM(frontOtherWheelPWMPin, 1000)
pBack = GPIO.PWM(backWheelsPWMPin, 1000)
pBackOther = GPIO.PWM(backWheelOtherPWMPin, 1000)
pFront.start(100)
pBack.start(100)
pFrontOther.start(100)
pBackOther.start(100)

class Wheel:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2

    def MoveForward(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)

    def MoveReverse(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)

    def StopMovement(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)

class AllWheels:
    def __init__(self, 
        FrontLeftWheel, 
        FrontRightWheel,
        BackLeftWheel,
        BackRightWheel):
        self.FrontLeftWheel = FrontLeftWheel
        self.FrontRightWheel = FrontRightWheel
        self.BackLeftWheel = BackLeftWheel
        self.BackRightWheel = BackRightWheel

    def Forward(self):
        self.FrontRightWheel.MoveForward()
        self.FrontLeftWheel.MoveForward()
        #setReverse for backwheels since they are backwards
        self.BackRightWheel.MoveReverse()
        self.BackLeftWheel.MoveReverse()

    def Reverse(self):
        self.FrontRightWheel.MoveReverse()
        self.FrontLeftWheel.MoveReverse()
        self.BackLeftWheel.MoveForward()
        self.BackRightWheel.MoveForward()

    def Stop(self):
        self.FrontRightWheel.StopMovement()
        self.FrontLeftWheel.StopMovement()
        self.BackRightWheel.StopMovement()
        self.BackLeftWheel.StopMovement()

    def LeftTurn(self):
        self.FrontRightWheel.MoveForward()
        self.FrontLeftWheel.MoveReverse()
        self.BackRightWheel.MoveReverse()
        self.BackLeftWheel.MoveForward()

    def RightTurn(self):
        self.FrontLeftWheel.MoveForward()
        self.FrontRightWheel.MoveReverse()
        self.BackLeftWheel.MoveReverse()
        self.BackRightWheel.MoveForward()

    def SetSpeed(self, speedRating):
        self.FrontRightWheel.ChangeDutyCycle(speedRating)
        self.BackRightWheel.ChangeDutyCycle(speedRating)
        self.FrontLeftWheel.ChangeDutyCycle(speedRating)
        self.BackLeftWheel.ChangeDutyCycle(speedRating)

#Instantiate Wheels
FLW = Wheel(w1Pin1, w1Pin2)
FRW = Wheel(w2Pin1, w2Pin2)
RLW = Wheel(w3Pin1, w3Pin2)
RRW = Wheel(w4Pin1, w4Pin2)

#Instantiate AllWheels class
Mower = AllWheels(FLW, FRW, RLW, RRW)

while(True):
    print("test\n>>>")
    input = raw_input()

    if input == 'q':
        GPIO.cleanup()
        break
    elif input == 'test':
        Mower.Forward()
        sleep(20)
        Mower.Stop()
    elif input == 'f':
        Mower.Forward()
    elif input == 's':
        Mower.Stop()
    elif input == 'r':
        Mower.Reverse()
    elif input == 'left':
        Mower.LeftTurn()
    elif input == 'right':
        Mower.RightTurn()