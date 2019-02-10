import RPi.GPIO as GPIO
import traceback
import time
import random
import math

SDI = 17
RCLK = 18
SRCLK = 27

letters = [[
    '00000000',
    '01111100',
    '01000010',
    '01111100',
    '01000010',
    '01000010',
    '01111100',
    '00000000'
], [
    '00000000',
    '01111110',
    '01000000',
    '01111110',
    '01000000',
    '01000000',
    '01111110',
    '00000000'
], [
    '00000000',
    '01000000',
    '01000000',
    '01000000',
    '01000000',
    '01000000',
    '01111110',
    '00000000'
], [
    '00000000',
    '00111100',
    '01000010',
    '01000010',
    '01111110',
    '01000010',
    '01000010',
    '00000000'
], [
    '00000000',
    '00110110',
    '01111111',
    '01111111',
    '00111110',
    '00011100',
    '00001000',
    '00000000'
]]

burst = [[
    '10000001',
    '00100100',
    '10000001',
    '00011000',
    '00011000',
    '10000001',
    '00100100',
    '10000001',
    ], [
    '00000000',
    '01000010',
    '00000000',
    '00011000',
    '00011000',
    '00000000',
    '01000010',
    '00000000',
    ], [
    '01000010',
    '00000000',
    '00100000',
    '00011000',
    '00011000',
    '00100100',
    '00000000',
    '01000010',
        ]]

pictures = [[
    '00111100',
    '01111110',
    '11111111',
    '11111111',
    '01111110',
    '01011010',
    '00111100',
    '01011010'
], [
    '01000010',
    '01100110',
    '00100100',
    '00011000',
    '00111100',
    '01011010',
    '11111111',
    '01100110'
], [
    '01000010',
    '01100110',
    '00111100',
    '01111110',
    '11000011',
    '10111101',
    '01100110',
    '01000010'
], [
    '11000011',
    '01111110',
    '01000010',
    '01011010',
    '01000010',
    '01111110',
    '01011010',
    '00100100'
], [
    '00011000',
    '00111100',
    '01111110',
    '11011011',
    '11111111',
    '00111100',
    '01111110',
    '10100101'
], [
    '00111100',
    '01111110',
    '11011011',
    '11111111',
    '11111111',
    '10111101',
    '01000010',
    '00111100'
]]

clock_interval = 1e-6
shift_interval = 0.0001
frame_interval = 0.03

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
        time.sleep(clock_interval)
        GPIO.output(SRCLK, GPIO.LOW)
        
def flush():
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(shift_interval)
    GPIO.output(RCLK, GPIO.LOW)

def generate_radar_animation(num_frames, height, width):
    frames = []
    midy = round(height/2.0)
    angle_increment = (2*math.pi)/float(num_frames)
    angle = 0

    for f in range(num_frames):
        frame = []
        angle_sin = math.sin(angle)
        angle_cos = math.cos(angle)
        # sweep radius from center outwards
        for radius in range(midy):
            # translate to the center
            frame.append((
                round(angle_sin*radius) + midy,
                round(angle_cos*radius) + midy
            ))
                
        frames.append(frame)
        angle += angle_increment
        
    return frames


def convert_coords_to_bitmask(coords, height, width):
    return (
        (1 << coords[1]) ^ 0xff, # take one's complement for column
        (1 << coords[0])
    )

# frame is like [[(lo, hi)]]

def convert_frame_to_bitmask(frame, height, width):
    return [convert_coords_to_bitmask(coords, height, width) for coords in frame]

def convert_animation_to_bitmask_array(animation, height, width):
    return [convert_frame_to_bitmask(frame, height, width) for frame in animation]

def convert_image_to_788bs_mask(image):
    """
    Convert a bitmap to a sequence of
    bitmaps for each line.
    This is what is actually sent to the multiplexer
    """
    mask = []
    for i, row in enumerate(image):
        row_bin = int(row, 2)
        mask.append((
            (1 << i) ^ 0xff if row_bin > 0 else 0xff,
            row_bin
        ))
        
    return mask

def play_frames(frames):
    """
    Play frames, consisting of [[low,high]] bitmaps,
    each frame is a continuous repetition of "scan lines"
    """
    repetitions = round(frame_interval/float(8*(2*clock_interval + shift_interval)))
    for frame in frames:
        for i in range(repetitions):
            for line in frame:
                send_byte(line[0])
                send_byte(line[1])
                flush()

if __name__ == "__main__":
    setup()
    animation_frames = 16
    width = 8
    height = 8
    radar_frames = generate_radar_animation(
        animation_frames,
        width,
        height
    )
    
    bitmask_radar_frames = convert_animation_to_bitmask_array(
        radar_frames,
        height,
        width
    )

    bitmask_letters = [convert_image_to_788bs_mask(im) for im in letters]
    bitmask_burst = [convert_image_to_788bs_mask(im) for im in burst]
    bitmask_pictures = [convert_image_to_788bs_mask(im) for im in pictures]

    try:
        while True:
            frame_interval = 0.05
            for i in range(4):
                play_frames(bitmask_pictures)
                
            frame_interval = 0.03
            for i in range(2):
                play_frames(bitmask_letters)

            frame_interval = 0.005
            for i in range(6):
                play_frames(bitmask_radar_frames)
            for i in range(10):
                play_frames(bitmask_burst)

    except Exception:
        traceback.print_exc()
        GPIO.cleanup()
