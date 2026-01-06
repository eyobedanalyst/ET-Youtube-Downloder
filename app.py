import streamlit as st
import yt_dlp
import os
from pathlib import Path

st.set_page_config(page_title="Mr Eyobed Sebrala YouTube Downloader", page_icon="📹", layout="centered")

st.title("📹 This is Mr Eyobed  sebrala YouTube Downloader")
st.markdown("Download YouTube videos for personal and educational use")

# Create downloads directory if it doesn't exist
downloads_dir = Path("downloads")
downloads_dir.mkdir(exist_ok=True)

# URL input
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Quality selection
quality = st.selectbox(
    "Select quality:",
    ["Best Quality (Video + Audio)", "Audio Only (MP3)", "720p", "480p", "360p"]
)

if st.button("Download", type="primary"):
    if not url:
        st.error("Please enter a YouTube URL")
    else:
        try:
            with st.spinner("Downloading..."):
                # Configure download options based on selection
                ydl_opts = {
                    'outtmpl': str(downloads_dir / '%(title)s.%(ext)s'),
                    'progress_hooks': [],
                }
                
                if quality == "Audio Only (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                elif quality == "Best Quality (Video + Audio)":
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                elif quality == "720p":
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif quality == "480p":
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                elif quality == "360p":
                    ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
                
                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # For audio downloads, adjust filename
                    if quality == "Audio Only (MP3)":
                        filename = filename.rsplit('.', 1)[0] + '.mp3'
                    
                    title = info.get('title', 'Unknown')
                
                st.success(f"✅ Downloaded: {title}")
                st.info(f"📁 Saved to: {filename}")
                
                # Offer download button
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download File",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="video/mp4" if quality != "Audio Only (MP3)" else "audio/mpeg"
                        )
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Make sure the URL is valid and the video is accessible")

# Footer
st.markdown("---")
st.markdown("⚠️ **Note:** Only download videos you have permission to download. Respect copyright laws.")
st.markdown("This tool is for personal and educational use only.")