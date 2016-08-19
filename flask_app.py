
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask.ext.cors import CORS
from enhanceapi import imgweb
from enhanceapi import imgandroid

app = Flask(__name__)
CORS(app)

@app.route('/web', methods=['GET', 'POST'])
def image_web():
    return imgweb()

@app.route('/android', methods=['GET', 'POST'])
def image_android():
    return imgandroid()

