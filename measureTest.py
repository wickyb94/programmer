from util import path
import time
import RPi.GPIO as GPIO


BOARD_TO_GPIO = {
    "INPUT_1": 22,
    "INPUT_2": 23,
}

# map of gpio to pins
GPIO_TO_PIN = {
    22: 15,
    23: 16,
}


class PowerStateMeasurement:
    input1 = GPIO_TO_PIN[BOARD_TO_GPIO["INPUT_1"]]
    input2 = GPIO_TO_PIN[BOARD_TO_GPIO["INPUT_2"]]

    def __init__(self):
        self.last_zero_input1 = 0
        self.last_zero_input2 = 0

        self.i1On = False
        self.i2On = False

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.input1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.input2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def cleanup(self):
        GPIO.cleanup([self.input1, self.input2])

    def checkPowerStates(self):
        startT = time.time()
        t = startT
        self.i1On = False
        self.i2On = False
        while t < startT + 0.4 and not (self.i1On and self.i2On):
            i1 = GPIO.input(self.input1)
            i2 = GPIO.input(self.input2)
            if i1 == 0:
                self.i1On = True
                self.last_zero_input1 = time.time()

            if i2 == 0:
                self.i2On = True
                self.last_zero_input2 = time.time()

            t = time.time()

    def powerThroughI1(self):
        res = time.time() - self.last_zero_input1 < 0.1
        print("Power throughI1:", res, time.time(), self.last_zero_input1)
        return res

    def powerThroughI2(self):
        res = time.time() - self.last_zero_input2 < 0.1
        print("Power throughI2:", res, time.time(), self.last_zero_input2)
        return res

    def powerThroughLoad(self):
        return self.powerThroughI1() or self.powerThroughI2()


a = PowerStateMeasurement()
a.setup()

while True:
    a.checkPowerStates()
    a.powerThroughI1()
    a.powerThroughI2()
    time.sleep(0.2)