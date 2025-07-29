import os
import random
from PIL import Image
import streamlit as st

# Title
st.title("🎨 1, 2, Sketch!")

# Folder where your images are stored
IMAGE_FOLDER = "images"

# Get list of image files
image_files = [file for file in os.listdir(IMAGE_FOLDER) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not image_files:
    st.warning("No images found. Please add .jpg, .png, or .jpeg files to the 'images' folder.")
else:
    if st.button("🎲"):
        selected = random.choice(image_files)
        image_path = os.path.join(IMAGE_FOLDER, selected)
        st.image(Image.open(image_path), caption=selected, use_column_width=True)
