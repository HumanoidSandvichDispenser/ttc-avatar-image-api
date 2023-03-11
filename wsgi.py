#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2023 sandvich <sandvich@artix>
#
# Distributed under terms of the MIT license.

from io import BytesIO
from PIL import Image
from flask import Flask, request
import imageprocessor
import requests


app = Flask(__name__)

@app.route("/")
def root_path():
    return "Among us"

@app.route("/convert", methods=["POST"])
def convert():
    json_request = request.get_json()
    print(json_request)
    img_response = requests.get(json_request["url"], timeout = 3)
    img = Image.open(BytesIO(img_response.content))
    img = imageprocessor.process_image(img, json_request)
    hex_str = imageprocessor.image_to_hex(img)

    # this json response can then be directly used to request avatar upload
    return {
        "data": hex_str,
    }
