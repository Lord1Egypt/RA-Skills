#!/bin/bash
# Step 2: Download audio from YouTube video as fallback
# Usage: ./download_audio.sh <video_url> [output_path]
set -e

VIDEO_URL="$1"
OUTPUT_FILE="${2:-/tmp/audio.mp3}"

if [ -z "$VIDEO_URL" ]; then
  echo "ERROR: video_url is required"
  exit 1
fi

echo "Downloading audio from: $VIDEO_URL"

# 使用 yt-dlp 下载最佳音频
if command -v yt-dlp &> /dev/null; then
  yt-dlp \
    -x \
    --audio-format mp3 \
    --audio-quality 0 \
    -o "$OUTPUT_FILE" \
    "$VIDEO_URL"
else
  echo "ERROR: yt-dlp is not installed"
  echo "Installing yt-dlp..."
  pip install yt-dlp -q
  yt-dlp \
    -x \
    --audio-format mp3 \
    --audio-quality 0 \
    -o "$OUTPUT_FILE" \
    "$VIDEO_URL"
fi

echo "AUDIO_FILE=$OUTPUT_FILE"
