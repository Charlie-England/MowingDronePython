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

class WheelAxle:
    def __init__(self, Wheel1, Wheel2):
        self.Wheel1 = Wheel1
        self.Wheel2 = Wheel2

    def SetWheelsForwardMovement(self):
        self.Wheel1.MoveForward()
        self.Wheel2.MoveForward()

    def SetWheelsReverseMovement(self):
        self.Wheel1.MoveReverse()
        self.Wheel2.MoveReverse()

    def StopWheels(self):
        self.Wheel1.StopMovement()
        self.Wheel2.StopMovement()

    def SetWheelsLeftTurn(self):
        self.Wheel1.MoveReverse()
        self.Wheel2.MoveForward()

    def SetWheelsRightTurn(self):
        self.Wheel1.MoveForward()
        self.Wheel2.MoveReverse()

class AllWheels:
    def __init__(self, FrontAxle, BackAxle):
        self.FrontAxle = FrontAxle
        self.BackAxle = BackAxle

    def Forward(self):
        self.FrontAxle.SetWheelsForwardMovement()
        #setReverse for backwheels since they are backwards
        self.BackAxle.SetWheelsReverseMovement()

    def Reverse(self):
        self.FrontAxle.SetWheelsReverseMovement()
        self.BackAxle.SetWheelsForwardMovement()

    def Stop(self):
        self.FrontAxle.StopWheels()
        self.BackAxle.StopWheels()

    def LeftTurn(self):
        self.FrontAxle.SetWheelsLeftTurn()
        self.BackAxle.SetWheelsRightTurn()

    def RightTurn(self):
        self.FrontAxle.SetWheelsRightTurn()
        self.BackAxle.SetWheelsLeftTurn()

    def SetSpeed(self, speedRating):
        pFront.ChangeDutyCycle(speedRating)
        pBack.ChangeDutyCycle(speedRating)

#Instantiate Wheels
FLW = Wheel(w1Pin1, w1Pin2)
FRW = Wheel(w2Pin1, w2Pin2)
RLW = Wheel(w3Pin1, w3Pin2)
RRW = Wheel(w4Pin1, w4Pin2)

#Instantiate Axel Classes
frontAxle = WheelAxle(FLW, FRW)
rearAxle = WheelAxle(RLW, RRW)

#Instantiate AllWheels class
Mower = AllWheels(frontAxle, rearAxle)

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