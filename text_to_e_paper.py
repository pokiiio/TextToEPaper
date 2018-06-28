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
    if (len(sys.argv) < 3 or len(sys.argv) % 2 == 0):
        quit()

    info_count = (len(sys.argv) - 1) / 2
    text_size = 16 - 2 * (info_count - 1)

    image_black = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))

    image_red = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))

    for num in range(info_count):
        image_black.paste(text_to_image.text_to_image(
            E_PAPER_WIDTH, E_PAPER_HEIGHT / info_count - HEADER_SIZE, unicode(sys.argv[2 + 2 * num], 'utf-8'), text_size), (0, HEADER_SIZE + E_PAPER_HEIGHT / info_count * num))

        image_red.paste(ImageOps.invert(text_to_image.text_to_image(
            E_PAPER_WIDTH, HEADER_SIZE, unicode(sys.argv[1 + 2 * num], 'utf-8'), text_size)), (0, E_PAPER_HEIGHT / info_count * num))

    show_image(image_black.rotate(90, expand=True),
               image_red.rotate(90, expand=True))
