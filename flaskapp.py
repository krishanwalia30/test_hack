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

def calculate_score(results):
        labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
        scores = {0: 70,  # Bathtub
                       1: 50,  # 'c' idk wtf is this
                       2: 60,  # Geyser is imp
                       3: 80,  # Mirrors are op
                       4: 60,  # Showerhead is ok, but not imp when shitting
                       5: 90,  # Sink is a S+
                       6: 100,  # Not imp
                       7: 40,  # Towels
                       8: 80,  # Washbasin
                       9: 100,  # 'wc'
                       10: 0}  # 'none'
        score = 0
        for key, value in labels.items():
            if value in results:
                score = score + scores[key]

        score = (score*100.0)/730.0
        return score

app = Flask(__name__)
CORS(app)
        

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
    html_content = "<h1>SERVER UP!</h1>"
    return html_content, 200, {'Content-Type': 'text/html'}
    

@app.route('/api/process-images', methods=['POST'])
def process_images():
    try:
        if 'images' not in request.files:
            return jsonify({"error": "No images uploaded"}), 400
        
        images = request.files.getlist('images')

        model = YOLO('model/best.pt')
        
        for image in images:
            image_file = image
            image_file.save('input.png')  # Example: Save image as 'uploaded_image.png'


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
        Img = Image.open(image_file)

        results = model(Img)

        class_id = results[0].boxes.cls.numpy()
        labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
        
        classes = set()
        for i in class_id:
            classes.add(labels[i])
        
        return jsonify({"Facilities_Detected": list(classes), "Toilet_Score":calculate_score(classes)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/c', methods=['POST'])
def processor_image():
# try:
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files.getlist('image')
    print(image_file)

    total_list = set()
    
    for image in image_file:
    
        model = YOLO("model/best.pt")
        image.save('input.png')  # Example: Save image as 'uploaded_image.png'
    # image_file.save('input.png')  # Example: Save image as 'uploaded_image.png'

        Img = Image.open(image)
        results = model(Img)

        class_id = results[0].boxes.cls.numpy()
        labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
        
        # classes = set()
        for i in class_id:
            total_list.add(labels[i])

        # total_list.append(classes)
    print(total_list)
    return jsonify({"Facilities_Detected": list(total_list), "Toilet_Score":calculate_score(set(total_list))}), 200
# except Exception as e:
#     return jsonify({"error": str(e)}), 500



app.run(host='0.0.0.0', port=1000)