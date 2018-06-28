# coding=utf-8

import numpy
from os import path
from PIL import Image, ImageFont, ImageDraw

FONT_PATH = path.dirname(path.abspath(__file__)) + '/mplus-2p-heavy.ttf'


def text_to_image(width, height, text, text_size):
    font = ImageFont.truetype(FONT_PATH, text_size, encoding='unic')
    image = Image.new("RGB", (width, height), (255, 255, 255))
    text_array = text_to_array(text, width, height, font)
    image = draw_text_array(image, text_array, width, height, font)
    return image


def text_to_array(text, width, height, font):
    array = []

    partial_text = u""

    for char in text:
        if font.getsize(partial_text + char)[0] < width:
            partial_text = partial_text + char
        else:
            array.append(partial_text)
            partial_text = char

    if len(partial_text) > 0:
        array.append(partial_text)

    return array


def draw_text_array(image, text_array, width, height, font):
    draw = ImageDraw.Draw(image)
    draw.font = font
    num_line = min(height / font.getsize(text_array[0])[1], len(text_array))

    if num_line < len(text_array):
        truncated_text = text_array[num_line - 1][:-1] + u"…"
        text_array[num_line - 1] = truncated_text

    del text_array[num_line:]
    img_size = numpy.array((width, height))
    txt_size = (max(list(map(lambda s: font.getsize(s)[0], text_array))), sum(
        list(map(lambda s: font.getsize(s)[1], text_array))))

    for index in range(num_line):
        pos = (img_size - txt_size) / 2
        pos = pos + \
            (0, sum(
                list(map(lambda s: font.getsize(s)[1], text_array[0:index]))))
        draw.text(pos, text_array[index], (0, 0, 0))

    return image
