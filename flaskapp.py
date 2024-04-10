import base64
from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
# -
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
import io

app = Flask(__name__)
CORS(app)

class Classifier:
    def __init__(self):
        self.model = YOLO('model/best.pt')
        

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


@app.route("/", methods = ['GET'])
@cross_origin()
def home():
    html_content = "<h1>Hello, this is an HTML response!</h1>"
    return html_content, 200, {'Content-Type': 'text/html'}
    # return render_template('index.html')
    

@app.route('/api/process-images', methods=['POST'])
def process_images():
    try:
        if 'images' not in request.files:
            return jsonify({"error": "No images uploaded"}), 400
        
        images = request.files.getlist('images')

        processed_images = []
        for image in images:
            # Read image file
            img = Image.open(image)
            # Perform processing (example: resizing)
            img_resized = img.resize((100, 100))  # Resize the image to 100x100 (example)
            # Convert processed image to bytes
            buffered = BytesIO()
            img_resized.save(buffered, format="JPEG")
            processed_images.append(buffered.getvalue())
        
        return jsonify({"processed_images": processed_images}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        image_file = request.files['image']
        image_file.save('input.png')  # Example: Save image as 'uploaded_image.png'

        model = YOLO("model/best.pt")
        Img = Image.open('input.png')

        results = model(Img)

        class_id = results[0].boxes.cls.numpy()
        labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
        
        classes = set()
        for i in class_id:
            classes.add(labels[i])
        
        return jsonify({"processed_image": list(classes)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
    # clApp = ClientApp()
app.run(host='0.0.0.0', port=1000)