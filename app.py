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

# --- Session State Initialization ---
if "running" not in st.session_state:
    st.session_state.running = False
if "images" not in st.session_state:
    st.session_state.images = []
if "last_image" not in st.session_state:
    st.session_state.last_image = None
if "category" not in st.session_state:
    st.session_state.category = None

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
        if not os.path.isdir(path):
            return []
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

# Main display area
placeholder = st.empty()
timer = TIMER_MAP[timer_label]

# --- Start Logic ---
if start_btn:
    st.session_state.running = True
    st.session_state.category = category
    st.session_state.images = get_images(category)
    st.session_state.last_image = None

# --- MANUAL MODE ("No timer") ---
if st.session_state.running and timer is None:
    if not st.session_state.images:
        st.warning("No images found for this category.")
    else:
        if st.button("🎲 Next Image"):
            new_image = random.choice(st.session_state.images)
            while new_image == st.session_state.last_image and len(st.session_state.images) > 1:
                new_image = random.choice(st.session_state.images)
            st.session_state.last_image = new_image
            with placeholder.container():
                show_image(new_image)

        # Show the last image even before clicking "Next"
        elif st.session_state.last_image:
            with placeholder.container():
                show_image(st.session_state.last_image)

# --- TIMED MODE with Countdown ---
elif st.session_state.running and timer is not None:
    if not st.session_state.images:
        st.warning("No images found for this category.")
    else:
        while st.session_state.running:
            new_image = random.choice(st.session_state.images)
            with placeholder.container():
                show_image(new_image)

            # Countdown display
            for remaining in range(timer, 0, -1):
                if not st.session_state.running:
                    break  # Exit early if stop button pressed
                st.info(f"⏳ {remaining} second{'s' if remaining > 1 else ''} left...")
                time.sleep(1)

