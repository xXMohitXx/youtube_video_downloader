import cv2
import os
import streamlit as st
from moviepy.editor import VideoFileClip

# Streamlit UI
st.title("Video Quality Enhancer")
st.write("Upload a video, select desired enhancements (resolution and bitrate), and improve its quality.")

# File uploader
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

# Resolution options
resolution_options = ['Original', '720p', '1080p', '4K']
selected_resolution = st.selectbox("Select desired resolution", resolution_options)

# Bitrate options
bitrate_options = ['1000k', '3000k', '5000k', '8000k', '12000k']  # in kbps
selected_bitrate = st.selectbox("Select desired bitrate", bitrate_options)

# Ensure the downloads directory exists
if not os.path.exists('enhanced_videos'):
    os.makedirs('enhanced_videos')

# Helper function to change resolution
def change_resolution(cap, width, height, output_file):
    # Get the original video properties
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to the desired resolution
        resized_frame = cv2.resize(frame, (width, height))
        out.write(resized_frame)

    cap.release()
    out.release()

# Helper function to adjust resolution based on selection
def get_resolution_dims(video_path, selected_resolution):
    # Get the original dimensions of the video
    cap = cv2.VideoCapture(video_path)
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Determine the new resolution based on the user's selection
    if selected_resolution == '720p':
        return 1280, 720
    elif selected_resolution == '1080p':
        return 1920, 1080
    elif selected_resolution == '4K':
        return 3840, 2160
    else:
        return original_width, original_height  # Keep original resolution

# Download button logic
if uploaded_file:
    st.video(uploaded_file)

    if st.button("Enhance Video"):
        # Save uploaded file temporarily
        video_path = os.path.join('enhanced_videos', uploaded_file.name)
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Load the video using OpenCV
        cap = cv2.VideoCapture(video_path)

        # Get new resolution dimensions
        width, height = get_resolution_dims(video_path, selected_resolution)

        # Output file path for enhanced video
        output_file = os.path.join('enhanced_videos', f"enhanced_{uploaded_file.name}")

        # Enhance video resolution
        change_resolution(cap, width, height, output_file)

        # Modify bitrate (using moviepy for simplicity)
        clip = VideoFileClip(output_file)
        bitrate = selected_bitrate
        enhanced_output_file = os.path.join('enhanced_videos', f"enhanced_bitrate_{uploaded_file.name}")
        clip.write_videofile(enhanced_output_file, bitrate=bitrate)

        # Display success message and download link
        st.success("Video enhancement completed successfully!")
        st.video(enhanced_output_file)
        st.markdown(f"[Download Enhanced Video](enhanced_videos/enhanced_bitrate_{uploaded_file.name})")

