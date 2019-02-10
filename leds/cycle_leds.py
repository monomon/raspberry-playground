import RPi.GPIO as GPIO
import time

leds = [19,20,21, 12]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for l in leds:
    GPIO.setup(l, GPIO.OUT)

timeout = 0.1

while True:
    for l in leds:
        GPIO.output(l, GPIO.HIGH)
        time.sleep(timeout)
        GPIO.output(l, GPIO.LOW)
