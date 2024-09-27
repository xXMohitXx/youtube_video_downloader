import os
import streamlit as st
import yt_dlp as youtube_dl  # yt-dlp to handle video downloads without FFmpeg

# Ensure the downloads directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Function to download video or audio without FFmpeg
def download_video(url, format, quality):
    try:
        # Options for downloading video and audio without FFmpeg
        ydl_opts = {}
        if format == 'mp4':
            # Select video formats that are pre-merged (video + audio combined)
            if quality == 'Highest':
                ydl_opts = {
                    'format': 'best[ext=mp4]',  # Download the best video/audio in mp4 (pre-merged)
                    'outtmpl': f'downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                }
            elif quality == '720p':
                ydl_opts = {
                    'format': 'best[height<=720][ext=mp4]',  # Download 720p in mp4
                    'outtmpl': f'downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                }
            elif quality == '480p':
                ydl_opts = {
                    'format': 'best[height<=480][ext=mp4]',  # Download 480p in mp4
                    'outtmpl': f'downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                }
            elif quality == '360p':
                ydl_opts = {
                    'format': 'best[height<=360][ext=mp4]',  # Download 360p in mp4
                    'outtmpl': f'downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                }
        elif format == 'mp3':
            # For MP3, download audio only without conversion
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': f'downloads/%(title)s.%(ext)s',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'prefer_ffmpeg': False,  # Disable ffmpeg
            }

        # Download the video or audio
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        st.success("Download completed successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI
st.title("YouTube Video Downloader (No FFmpeg)")
st.write("Enter the YouTube video URL, choose the format, and quality to download.")

# Input fields
url = st.text_input("YouTube Video URL")
format = st.selectbox("Choose format", options=['mp4', 'mp3'])

# Quality checkboxes for video format (only for mp4)
quality = None
if format == 'mp4':
    quality = st.selectbox("Select video quality", options=['Highest', '720p', '480p', '360p'])

# Download button
if st.button("Download"):
    if url and format:
        download_video(url, format, quality)
    else:
        st.warning("Please enter a valid URL and select a format.")
