#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 sandvich <sandvich@manjaro>
#
# Distributed under terms of the MIT license.

from PIL import Image, ImageOps, ImageFilter
#from palettes import palettes
#from pyxelate import Pyx
#import skimage
#import numpy


def process_image(img, options):
    #if "--palette" in options:
    #    # number of colors in palette
    #    palette = 3
    #    palette_value = options["--palette"]

    #    # resize to both dimensions at most 128 pixels to process the image faster
    #    if img.width > img.height:
    #        if img.width > 128:
    #            new_height = 128 * 128 // img.width
    #            img = img.resize((128, img.height))
    #    elif img.height > 128:
    #        new_width = 128 * 128 // img.height
    #        img = img.resize((new_width, 128))
    #    
    #    if palette_value.isdigit():
    #        palette = min(max(int(palette_value), 2), 8)
    #    elif palette_value in palettes:
    #        palette = palettes[palette_value]

    #    skimage_img = numpy.array(img)

    #    pyx = Pyx(height = 32, width = 32, palette = palette, sobel = 4)
    #    new_image = pyx.fit_transform(skimage_img)
    #    img = Image.fromarray(new_image)

    # add white background if needed
    if "background" in options:
        background: str | list[int] | bool = options["background"]
        color: tuple[int, int, int] | None = None
        if background is None or background == True:
            color = (255, 255, 255)
        elif isinstance(background, list):
            color = tuple(background)
        elif isinstance(background, str) and background[0] == "#":
            color = tuple(int(background[i : i + 2], 16) for i in (0, 2, 4))
        if color is not None:
            img = add_background(img, color)

    # Resampling: NEAREST, BILINEAR, BICUBIC, LANCZOS
    resample_opt = Image.LANCZOS
    if "resample" in options:
        if options["resample"] == "NEAREST":
            resample_opt = Image.NEAREST
        elif options["resample"] == "BILINEAR":
            resample_opt = Image.BILINEAR
        elif options["resample"] == "BICUBIC":
            resample_opt = Image.BICUBIC
        elif options["resample"] == "LANCZOS":
            resample_opt = Image.LANCZOS
        else:
            return "Unknown image sampling method", 400


    if "invert" in options and options["invert"]:
        img = ImageOps.invert(img)

    if "flip" in options and options["flip"]:
        img = ImageOps.flip(img)

    if "mirror" in options and options["mirror"]:
        img = ImageOps.mirror(img)

    img = img.resize((32, 32), resample_opt)

    if "sharpen" in options:
        iterations = 1
        sharpen_value = options["sharpen"]

        # convert the value of --sharpen to an int.
        # if it is not an int, default value is 1
        # the option is capped at 5.

        if sharpen_value.isdigit():
            iterations = min(int(sharpen_value), 5)

        for _ in range(iterations):
            img = img.filter(ImageFilter.SHARPEN)

    return img

def add_background(img, color = (255, 255, 255)):
    if img.mode != "RGBA":
        return img
    background = Image.new("RGBA", img.size, color)
    background.paste(img, (0, 0), img)
    print("Adding background!")
    print(img.size)
    return background

def image_to_hex(image):
    rgb_img = image.convert("RGB")
    hex_str = ""
    for y in range(rgb_img.height):
        for x in range(rgb_img.width):
            hex_str += "%02x%02x%02x" % rgb_img.getpixel((x, y))
    return hex_str
