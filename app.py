import os
from io import BytesIO

from PIL import Image

import streamlit as st

THUMBNAIL_WIDTH = 750


def bytes_to_kb(n_bytes):
    return int(n_bytes / float(1<<10))


def get_file_size_kb(file_path):
    return bytes_to_kb(os.path.getsize(file_path))


st.set_page_config(
    page_title="PNG to JPG Converter", page_icon="📷"
)

st.title('PNG to JPG Converter')

size_threshold_kb = st.slider('Size threshold (kB)', 0, 200, 90)

uploaded_img = st.file_uploader('Upload a PNG')
if uploaded_img:
    png_name = uploaded_img.name
    jpg_name = png_name.split('.')[0] + '.jpg'
    
    try:
        img = Image.open(uploaded_img)
        png_size_kb = bytes_to_kb(uploaded_img.size)
        st.write(f'Original image ({png_name}, {png_size_kb} kB):')
    except Exception as e:
        st.error(f'Unable to open file: {png_name}')
    
    show_original_image = st.checkbox('Show original image')
    if show_original_image:
        st.image(img, width=THUMBNAIL_WIDTH)
    
    if png_size_kb < size_threshold_kb:
        st.success('The original image is small enought. No need to resize')
    else:
        img_rgb = img.convert('RGB')
        jpg_size_kb = png_size_kb
        quality = 95
        
        while jpg_size_kb >= size_threshold_kb:
            img_rgb.save(jpg_name, 'JPEG', quality=quality, optimize=True)
            jpg_size_kb = get_file_size_kb(jpg_name)
            quality -= 5
            
        st.write(f'Converted to JPG (quality {quality}). Size: {jpg_size_kb} kB')
        
        with open(jpg_name, 'rb') as jpg_fp:
            st.download_button('Download JPG', jpg_fp, jpg_name)
        
        st.image(jpg_name, width=THUMBNAIL_WIDTH)

    
    # jpg_path = png_path.replace('.png', '.jpg')
    