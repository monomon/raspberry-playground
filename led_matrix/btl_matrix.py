#!/usr/bin/env python

import RPi.GPIO as GPIO
import traceback
import time
import random
import math

SDI = 17
RCLK = 18
SRCLK = 27

heart = [
    "00000000",
    "00110110",
    "01111111",
    "01111111",
    "00111110",
    "00011100",
    "00001000",
    "00000000"
]

burst = [[
    "10000001",
    "00100100",
    "10000001",
    "00011000",
    "00011000",
    "10000001",
    "00100100",
    "10000001",
], [
    "00000000",
    "01000010",
    "00000000",
    "00011000",
    "00011000",
    "00000000",
    "01000010",
    "00000000",
], [
    "01000010",
    "00000000",
    "00100000",
    "00011000",
    "00011000",
    "00100100",
    "00000000",
    "01000010",
]]

alphabet = {
    " ": [
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
        "00000000",
    ],
    "a": [
        "00000000",
        "00111100",
        "01000010",
        "01111110",
        "01000010",
        "01000010",
        "01000010",
        "00000000"],
    "b": [
        "00000000",
        "01111100",
        "01000010",
        "01111100",
        "01000010",
        "01000010",
        "01111100",
        "00000000"
    ],
    "c": [
        "00000000",
        "00111110",
        "01000000",
        "01000000",
        "01000000",
        "01000000",
        "00111110",
        "00000000",
    ],
    "e": [
        "00000000",
        "01111110",
        "01000000",
        "01111110",
        "01000000",
        "01000000",
        "01111110",
        "00000000"
    ],
    "h": [
        "00000000",
        "01000010",
        "01000010",
        "01111110",
        "01000010",
        "01000010",
        "01000010",
        "00000000",
    ],
    "i": [
        "00000000",
        "00111000",
        "00010000",
        "00010000",
        "00010000",
        "00010000",
        "00111000",
        "00000000"
    ],
    "l": [
        "00000000",
        "01000000",
        "01000000",
        "01000000",
        "01000000",
        "01000000",
        "01111110",
        "00000000"
    ],
    "n": [
        "00000000",
        "01000010",
        "01100010",
        "01010010",
        "01001010",
        "01000110",
        "01000010",
        "00000000",
    ],
    "o": [
        "00000000",
        "00111100",
        "01000010",
        "01000010",
        "01000010",
        "01000010",
        "00111100",
        "00000000",
    ],
    "p": [
        "00000000",
        "01111100",
        "01000010",
        "01111100",
        "01000000",
        "01000000",
        "01000000",
        "00000000",
    ],
    "r": [
        "00000000",
        "01111100",
        "01000010",
        "01111100",
        "01000010",
        "01000010",
        "01000010",
        "00000000"
    ],
    "s": [
        "00000000",
        "01111110",
        "01000000",
        "01111110",
        "00000010",
        "00000010",
        "01111110",
        "00000000",
    ],
    "t": [
        "00000000",
        "11111110",
        "00010000",
        "00010000",
        "00010000",
        "00010000",
        "00010000",
        "00000000"
    ],
}

pictures = [[
    "00111100",
    "01111110",
    "11111111",
    "11111111",
    "01111110",
    "01011010",
    "00111100",
    "01011010"
], [
    "01000010",
    "01100110",
    "00100100",
    "00011000",
    "00111100",
    "01011010",
    "11111111",
    "01100110"
], [
    "01000010",
    "01100110",
    "00111100",
    "01111110",
    "11000011",
    "10111101",
    "01100110",
    "01000010"
], [
    "11000011",
    "01111110",
    "01000010",
    "01011010",
    "01000010",
    "01111110",
    "01011010",
    "00100100"
], [
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "00111100",
    "01111110",
    "10100101"
], [
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "11111111",
    "10111101",
    "01000010",
    "00111100"
]]

skull = [
    "00111100",
    "01111110",
    "11111111",
    "11111111",
    "01111110",
    "01011010",
    "00111100",
    "01011010"
]

sand_clock = [[
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00011000",
    "00000000",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00011000",
    "00111100",
    "00000000",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00011000",
    "00111100",
    "01111110",
    "00000000",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00011000",
    "00111100",
    "01111110",
    "11111111",
], [
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00011000",
    "00111100",
    "01111110",
    "11111111",
]]

saucer = [[
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000000",
    "10000000",
    "10000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000000",
    "11000000",
    "11000000",
    "00000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "10000000",
    "11100000",
    "11100000",
    "10000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "11000000",
    "11110000",
    "11110000",
    "11000000",
    "10000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "11100000",
    "11111000",
    "11111000",
    "11100000",
    "11000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "11110000",
    "11111100",
    "11111100",
    "11110000",
    "01100000",
    "00000000",
], [
    "00000000",
    "00000000",
    "01111000",
    "11111110",
    "11111110",
    "01111000",
    "00110000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00111100",
    "11111111",
    "11111111",
    "00111100",
    "00011000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00011111",
    "01111111",
    "01111111",
    "00011110",
    "00001100",
    "00000000",
], [
    "00000000",
    "00000000",
    "00001111",
    "00111111",
    "00111111",
    "00001111",
    "00000110",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000111",
    "00011111",
    "00011111",
    "00000111",
    "00000011",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000011",
    "00001111",
    "00001111",
    "00000011",
    "00000001",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000001",
    "00000111",
    "00000111",
    "00000001",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000000",
    "00000011",
    "00000011",
    "00000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000000",
    "00000001",
    "00000001",
    "00000000",
    "00000000",
    "00000000",
], [
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
    "00000000",
]]


clock_interval = 4e-7
shift_interval = 0.0001
frame_interval = 0.07


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
    """
    The result is a sparse animation that contains the positive areas
    of the frame
    """
    frames = []
    midy = int(round(height/2.0))
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
                int(round(angle_sin*radius) + midy),
                int(round(angle_cos*radius) + midy)
            ))

        frames.append(frame)
        angle += angle_increment

    return frames


def convert_coords_to_bitmask(coords, height, width):
    return (
        (1 << coords[1]) ^ 0xff,  # take one"s complement for column
        (1 << coords[0])
    )

# frame is like [[(lo, hi)]]


def convert_frame_to_bitmask(frame, height, width):
    return [convert_coords_to_bitmask(coords, height, width) for coords in frame]


def convert_animation_to_bitmask_array(animation, height, width):
    return [convert_frame_to_bitmask(frame, height, width) for frame in animation]


def convert_text_to_788bs_animated_mask(txt):
    return [convert_image_to_788bs_mask(alphabet[im]) for im in txt]

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
    repetitions = int(
        round(frame_interval/float(8*(2*clock_interval + shift_interval))))

    for frame in frames:
        for i in range(repetitions):
            for line in frame:
                send_byte(line[0])
                send_byte(line[1])
                flush()


def play_blink_frames(frames):
    repetitions = int(
        round(frame_interval/float(8*(2*clock_interval + shift_interval))))

    for frame in frames:
        for i in range(repetitions):
            for line in frame:
                send_byte(line[0])
                send_byte(line[1])
                flush()
        # clear and wait a bit
        send_byte(0)
        send_byte(0)
        flush()
        time.sleep(frame_interval*2)


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

    sand_clock_frames = [convert_image_to_788bs_mask(f) for f in sand_clock]

    bottleship_letters = convert_text_to_788bs_animated_mask("no procrastination station ")

    bitmask_skull = [convert_image_to_788bs_mask(skull)]
    saucer_frames = [convert_image_to_788bs_mask(f) for f in saucer]

    try:
        while True:
            frame_interval = 0.02
            for i in range(3):
                play_frames(saucer_frames)

            frame_interval = 0.015
            for i in range(2):
                play_frames(sand_clock_frames)

            frame_interval = 0.1
            for i in range(3):
                play_frames(bitmask_skull)

            frame_interval = 0.03
            for i in range(2):
                play_blink_frames(bottleship_letters)

            frame_interval = 0.1
            for i in range(3):
                play_frames(bitmask_skull)

            frame_interval = 0.01
            for i in range(10):
                play_frames(bitmask_radar_frames)

    except Exception:
        traceback.print_exc()
        GPIO.cleanup()
