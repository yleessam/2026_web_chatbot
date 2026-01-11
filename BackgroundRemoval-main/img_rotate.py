import streamlit as st
from PIL import Image
from io import BytesIO
import os
import traceback
import time

st.set_page_config(layout="wide", page_title="Image Rotator (180°)")

st.write("## Rotate your image 180°")
st.write(
    "📸 Upload an image and watch it rotate 180°. "
    "You can download the rotated image from the sidebar."
)
st.sidebar.write("## Upload and download ⚙️")

# File size limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Max dimensions for processing
MAX_IMAGE_SIZE = 2000  # pixels


# Convert image for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Resize image while maintaining aspect ratio
def resize_image(image, max_size):
    width, height = image.size
    if width <= max_size and height <= max_size:
        return image

    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    return image.resize((new_width, new_height), Image.LANCZOS)


@st.cache_data
def process_image(image_bytes):
    """Rotate image 180 degrees with caching"""
    try:
        image = Image.open(BytesIO(image_bytes))
        resized = resize_image(image, MAX_IMAGE_SIZE)
        rotated = resized.rotate(180, expand=True)
        return image, rotated
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None, None


def fix_image(upload):
    try:
        start_time = time.time()
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        status_text.text("Loading image...")
        progress_bar.progress(10)

        # Read image bytes
        if isinstance(upload, str):
            if not os.path.exists(upload):
                st.error(f"Default image not found at path: {upload}")
                return
            with open(upload, "rb") as f:
                image_bytes = f.read()
        else:
            image_bytes = upload.getvalue()

        status_text.text("Rotating image...")
        progress_bar.progress(40)

        image, rotated = process_image(image_bytes)
        if image is None or rotated is None:
            return

        progress_bar.progress(80)
        status_text.text("Displaying results...")

        col1.write("Original Image 📷")
        col1.image(image)

        col2.write("Rotated Image 🔄 (180°)")
        col2.image(rotated)

        st.sidebar.markdown("\n")
        st.sidebar.download_button(
            "Download rotated image",
            convert_image(rotated),
            "rotated.png",
            "image/png"
        )

        progress_bar.progress(100)
        elapsed = time.time() - start_time
        status_text.text(f"Completed in {elapsed:.2f} seconds")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.sidebar.error("Failed to process image")
        print(traceback.format_exc())


# UI Layout
col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

with st.sidebar.expander("ℹ️ Image Guidelines"):
    st.write("""
    - Maximum file size: 10MB
    - Large images are resized automatically
    - Supported formats: PNG, JPG, JPEG
    """)

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error(
            f"The uploaded file is too large. "
            f"Please upload an image smaller than {MAX_FILE_SIZE/1024/1024:.1f}MB."
        )
    else:
        fix_image(upload=my_upload)
else:
    default_images = ["./zebra.jpg", "./wallaby.png"]
    for img_path in default_images:
        if os.path.exists(img_path):
            fix_image(img_path)
            break
    else:
        st.info("Please upload an image to get started!")
