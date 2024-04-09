import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
import io

st.title("HACKATHON")

uploaded_image = st.file_uploader("Select the Image (JPG Format): ", type='png',accept_multiple_files=False)

if uploaded_image:
    # Converting the image to bytes
    bytes_data_image = uploaded_image.getvalue()

    # Converting the bytes back to image
    image_conv = Image.open(io.BytesIO(bytes_data_image))

    # Saving the image to the filepath specified in clApp.filename
    image_conv.save('input.png')

    # Creating a button for prediction
    if st.button("Find Facilities"):
        model = YOLO("model/best.pt")
        Img = Image.open('input.png')
        img= np.asarray(Img)

        results = model(Img)

        class_id = results[0].boxes.cls.numpy()
        labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
        
        classes = []
        for i in class_id:
            classes.append(labels[i])
        st.write(classes)


    if st.button("Train"):
        # os.system("dvc repro")
        st.success("Training Successful!")