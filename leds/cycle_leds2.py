import RPi.GPIO as GPIO
import traceback
import time

led_timeout = 0.05

led_pins = [22, 21, 20, 19, 18, 25]
button_pins = [16, 23]
pot_pin = 17
pwm_pot = None

direction = 1
current_pin_index = 0

def setup():
    global pwm_pot

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for p in led_pins:
        GPIO.setup(p, GPIO.OUT)
        
    for p in button_pins:
        GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    GPIO.setup(pot_pin, GPIO.IN)
    pwm_pot = GPIO.PWM(pot_pin, 100)
    pwm_pot.start(0)
    
def play():
    global direction
    global current_pin_index
    
    num_leds = len(led_pins)
    
    while True:
        if GPIO.input(button_pins[0]) == GPIO.HIGH:
            direction = -1
        if GPIO.input(button_pins[1]) == GPIO.HIGH:
            direction = 1
        
        current_pin_index = (current_pin_index + direction) % num_leds
        GPIO.output(led_pins[current_pin_index], GPIO.HIGH)
        time.sleep(led_timeout)
        GPIO.output(led_pins[current_pin_index], GPIO.LOW)

if __name__ == "__main__":
    setup()
    try:
        play()
    except Exception:
        traceback.print_exc()
        pwm_pot.stop()
        GPIO.cleanup()