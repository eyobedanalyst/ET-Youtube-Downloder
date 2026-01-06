# Mr Eyobed Sebrala YouTube Downloader

A simple Streamlit app for downloading YouTube videos for personal and educational use.

## Features

- Download videos in multiple quality options (Best, 720p, 480p, 360p)
- Extract audio only as MP3
- Clean and simple interface
- Direct download to your computer

## Prerequisites

- Python 3.13.3 (or compatible version)
- pip package manager

## Installation

1. Clone or download this repository

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. (Optional) Install FFmpeg for audio extraction:
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (usually http://localhost:8501)

3. Paste a YouTube URL into the input field

4. Select your desired quality

5. Click "Download"

6. The file will be saved to the `downloads` folder and you can download it to your computer

## File Structure

```
youtube-downloader/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── downloads/         # Downloaded files (created automatically)
```

## Legal Notice

⚠️ **Important**: This tool is for personal and educational use only. Only download videos you have permission to download. Respect copyright laws and YouTube's Terms of Service.

## Troubleshooting

### "ERROR: Unable to extract..."
- Check if the URL is correct and the video is publicly accessible
- Some videos may be geo-restricted or age-restricted

### Audio extraction not working
- Install FFmpeg (see Prerequisites section)

### Port already in use
- Use a different port: `streamlit run app.py --server.port 8502`

## Dependencies

- **streamlit**: Web interface framework
- **yt-dlp**: YouTube download library (actively maintained fork of youtube-dl)

## License

This project is for educational purposes. Use responsibly and ethically.