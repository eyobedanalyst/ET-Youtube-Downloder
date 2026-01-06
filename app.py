import streamlit as st
import yt_dlp
import os
from pathlib import Path
import shutil

st.set_page_config(page_title="Mr Eyobed Sebrala YouTube Downloader", page_icon="📹", layout="centered")

st.title("📹Mr Eyobed Sebrala YouTube Downloader")
st.markdown("Download YouTube videos for personal and educational use")

# Create downloads directory if it doesn't exist
downloads_dir = Path("downloads")
downloads_dir.mkdir(exist_ok=True)

# Check if FFmpeg is available
def check_ffmpeg():
    return shutil.which('ffmpeg') is not None

has_ffmpeg = check_ffmpeg()

# Display FFmpeg status
if not has_ffmpeg:
    st.info("ℹ️ FFmpeg not detected. Using compatibility mode (works without FFmpeg).")
    with st.expander("Want better quality? Install FFmpeg"):
        st.markdown("""
        **Windows:** Download from https://ffmpeg.org/download.html
        
        **Mac:** `brew install ffmpeg`
        
        **Linux:** `sudo apt-get install ffmpeg`
        
        After installation, restart the app.
        """)

# URL input
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Quality selection based on FFmpeg availability
if has_ffmpeg:
    quality_options = [
        "Best Quality", 
        "1080p", 
        "720p", 
        "480p", 
        "Audio Only (MP3)"
    ]
else:
    quality_options = [
        "Best Available",
        "High Quality (720p)",
        "Medium Quality (480p)",
        "Low Quality (360p)"
    ]

quality = st.selectbox("Select quality:", quality_options)

if st.button("Download", type="primary"):
    if not url:
        st.error("Please enter a YouTube URL")
    else:
        try:
            with st.spinner("Fetching video information..."):
                # Configure download options based on selection
                ydl_opts = {
                    'outtmpl': str(downloads_dir / '%(title)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': False,
                }
                
                if has_ffmpeg:
                    # Full quality options with FFmpeg
                    if quality == "Audio Only (MP3)":
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })
                    elif quality == "Best Quality":
                        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                    elif quality == "1080p":
                        ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]'
                    elif quality == "720p":
                        ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]'
                    elif quality == "480p":
                        ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]'
                else:
                    # Without FFmpeg - use pre-merged formats only
                    if quality == "Best Available":
                        # Try best mp4, fallback to any best format
                        ydl_opts['format'] = 'best[ext=mp4]/best'
                    elif quality == "High Quality (720p)":
                        ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[height<=720]/best'
                    elif quality == "Medium Quality (480p)":
                        ydl_opts['format'] = 'best[height<=480][ext=mp4]/best[height<=480]/best'
                    elif quality == "Low Quality (360p)":
                        ydl_opts['format'] = 'best[height<=360][ext=mp4]/best[height<=360]/best'
                
                # Download the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.info("⏳ Downloading... This may take a few moments depending on file size.")
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # For audio downloads, adjust filename
                    if has_ffmpeg and quality == "Audio Only (MP3)":
                        filename = filename.rsplit('.', 1)[0] + '.mp3'
                    
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    filesize = info.get('filesize') or info.get('filesize_approx', 0)
                
                # Verify file exists and is not empty
                if not os.path.exists(filename):
                    st.error("❌ Download failed: File was not created")
                elif os.path.getsize(filename) == 0:
                    st.error("❌ Download failed: File is empty")
                    os.remove(filename)  # Clean up empty file
                else:
                    st.success(f"✅ Successfully downloaded: {title}")
                    
                    # Show file info
                    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
                    st.info(f"📁 File size: {file_size_mb:.2f} MB | Duration: {duration//60}:{duration%60:02d}")
                    
                    # Offer download button
                    with open(filename, 'rb') as f:
                        file_ext = filename.rsplit('.', 1)[-1].lower()
                        
                        if file_ext == 'mp3':
                            mime_type = "audio/mpeg"
                        elif file_ext in ['mp4', 'webm', 'mkv']:
                            mime_type = "video/mp4"
                        else:
                            mime_type = "application/octet-stream"
                        
                        st.download_button(
                            label="⬇️ Download to Computer",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime=mime_type,
                            use_container_width=True
                        )
                
        except yt_dlp.utils.DownloadError as e:
            st.error(f"❌ Download Error: {str(e)}")
            st.info("💡 Try selecting a different quality option or check if the video is available in your region")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Troubleshooting tips:")
            st.markdown("""
            - Make sure the URL is complete and valid
            - Check if the video is publicly accessible (not private/deleted)
            - Try a different quality setting
            - Some age-restricted videos may not work
            """)

# Footer
st.markdown("---")
st.markdown("⚠️ **Note:** Only download videos you have permission to download. Respect copyright laws.")
st.markdown("This tool is for personal and educational use only. and Thank Eyobed to ")