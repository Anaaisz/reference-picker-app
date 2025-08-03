import os
import random
import time
from PIL import Image
import streamlit as st

# Set up page
st.set_page_config(page_title="🎨 1, 2, Sketch!", layout="centered")
st.title("🎨 1, 2, Sketch!")

# Image structure
BASE_FOLDER = "images"
CATEGORIES = ["Buildings", "Landscapes", "People", "Faces", "Nature", "Mix"]
CATEGORY_TO_FOLDER = {
    "Buildings": "buildings",
    "Landscapes": "landscapes",
    "People": "people",
    "Faces": "faces",
    "Nature": "nature"
}

# Sidebar controls
category = st.sidebar.selectbox("Choose a Category", CATEGORIES)
timer_label = st.sidebar.radio("Set Timer", ["No timer", "30 seconds", "60 seconds", "2 minutes"])
start_btn = st.sidebar.button("Start")
stop_btn = st.sidebar.button("Stop")

# Session state to control timer
if "running" not in st.session_state:
    st.session_state.running = False

# Stop button logic
if stop_btn:
    st.session_state.running = False
    st.success("⏹️ Stopped!")

# Helper: get image list
def get_images(category):
    if category == "Mix":
        images = []
        for folder in CATEGORY_TO_FOLDER.values():
            path = os.path.join(BASE_FOLDER, folder)
            if os.path.isdir(path):
                images.extend([
                    os.path.join(path, f) for f in os.listdir(path)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ])
        return images
    else:
        path = os.path.join(BASE_FOLDER, CATEGORY_TO_FOLDER[category])
        return [
            os.path.join(path, f) for f in os.listdir(path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

# Timer values
TIMER_MAP = {
    "No timer": None,
    "30 seconds": 30,
    "60 seconds": 60,
    "2 minutes": 120
}

# Image display
def show_image(image_path):
    img = Image.open(image_path)
    max_height = 800
    aspect_ratio = img.width / img.height
    new_width = int(max_height * aspect_ratio)
    resized = img.resize((new_width, max_height))
    st.image(resized, caption=os.path.basename(image_path))

# Main logic
if start_btn:
    st.session_state.running = True
    images = get_images(category)

    if not images:
        st.warning("No images found.")
    else:
        timer = TIMER_MAP[timer_label]
        placeholder = st.empty()

        if timer is None:
            # Manual mode
            if st.button("🎲 Next Image"):
                selected = random.choice(images)
                with placeholder.container():
                    show_image(selected)
        else:
            # Timed mode
            while st.session_state.running:
                selected = random.choice(images)
                with placeholder.container():
                    show_image(selected)
                time.sleep(timer)
