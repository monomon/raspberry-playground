import RPi.GPIO as GPIO
import traceback
import time

SDI = 17
RCLK = 18
SRCLK = 27

image = [0x01,0xff,0x80,0xff,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
code_L = [0x00,0x7f,0x00,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f]

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)
    
def send_byte(dat):
    for b in range(0, 8):
        GPIO.output(SDI, 0x80 & (dat << b))
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
        
def flush():
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    
def play():
    print("printing {}".format(image))
    for i in range(0, len(image)):
        send_byte(code_L[i])
        send_byte(image[i])
        
        flush()
        time.sleep(0.1)
        
    for i in range(len(image) - 1, -1, -1):
        send_byte(code_L[i])
        send_byte(image[i])
        flush()
        time.sleep(0.1)
    
if __name__ == "__main__":
    setup()
    try:
        play()
    except Exception:
        traceback.print_exc()
        GPIO.cleanup()
