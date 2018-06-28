# coding=utf-8

import sys
import text_to_image
import numpy
import epd2in7b
from os import path
from PIL import Image, ImageOps, ImageFont, ImageDraw

E_PAPER_WIDTH = 264
E_PAPER_HEIGHT = 176
HEADER_SIZE = 20


def show_image(black_image, red_image):
    epd = epd2in7b.EPD()
    epd.init()

    frame_black = epd.get_frame_buffer(black_image)
    frame_red = epd.get_frame_buffer(red_image)
    epd.display_frame(frame_black, frame_red)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        quit()

    image_black = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))

    image_black.paste(text_to_image.text_to_image(
        E_PAPER_WIDTH, E_PAPER_HEIGHT - HEADER_SIZE, sys.argv[2], 16), (0, HEADER_SIZE))

    image_red = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))

    image_red.paste(ImageOps.invert(text_to_image.text_to_image(
        E_PAPER_WIDTH, HEADER_SIZE, sys.argv[1], 16)))

    show_image(image_black.rotate(90, expand=True),
               image_red.rotate(90, expand=True))
