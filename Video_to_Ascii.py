import cv2
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import time
import os


# Currently only the Black-and-White mode is supported
# Built a colour-to-ascii converter but the JSON data was way too large for Web Play

# How to use: type { python Video_to_Ascii.py <Video Path> <Columns> <Rows> } in the command line

def ascii_art(image, columns, rows):
    # Define the list of ASCII characters to be used
    ascii_chars = list(" @B%8WM#*oahkbdpwmZO0QCJYXzcvnxrjft/\|()1{}[]-_+~<>i!lI;:,\"^`'. ")
    char_length = len(ascii_chars)

    # Resize the input image
    image_width, image_height = image.size
    aspect_ratio = float(image_height) / float(image_width)
    new_width = columns
    new_height = int(aspect_ratio * new_width * 0.5)
    image = image.resize((new_width, new_height))

    # Convert the image to grayscale
    image = image.convert("L")

    # Create ASCII art
    ascii_image = ""
    for y in range(new_height):
        for x in range(new_width):
            brightness = image.getpixel((x, y))
            char_index = int((brightness * (char_length - 1)) / 255)
            ascii_image += ascii_chars[char_index]
        ascii_image += "\n"

    return ascii_image

def video_to_ascii_animation(video_path, output_path, columns, rows):
    video_capture = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        ascii_frame = ascii_art(pil_image, columns, rows)
        frames.append(ascii_frame)

    video_capture.release()

    with open(output_path, "w") as output_file:
        json.dump(frames, output_file)

def play_ascii_animation(json_file):
    with open(json_file, "r") as input_file:
        frames = json.load(input_file)

    os.system("cls" if os.name == "nt" else "clear")
    for frame in frames:
        print(frame)
        time.sleep(1/30)  # Assuming 30 FPS
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    video_path = sys.argv[1]
    output_path = "outputAnimation.json"
    columns = int(sys.argv[2])
    rows = int(sys.argv[3])

    video_to_ascii_animation(video_path, output_path, columns, rows)
    play_ascii_animation(output_path)
