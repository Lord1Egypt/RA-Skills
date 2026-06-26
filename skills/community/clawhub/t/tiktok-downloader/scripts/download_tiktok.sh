#!/bin/bash

# TikTok Downloader Script for Manus
# Usage: ./download_tiktok.sh <url> [output_dir]

URL=$1
OUTPUT_DIR=${2:-"."}
COOKIES_DIR="/home/ubuntu/.browser_data_dir"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

if [ -z "$URL" ]; then
    echo "Error: No URL provided."
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Attempting to download: $URL"

# Try with cookies and custom user-agent
yt-dlp --no-warnings \
  --cookies-from-browser "chromium:$COOKIES_DIR" \
  --user-agent "$USER_AGENT" \
  --add-header "Referer:https://www.tiktok.com/" \
  -o "$OUTPUT_DIR/%(uploader)s - %(title).80s.%(ext)s" \
  "$URL"

if [ $? -eq 0 ]; then
    echo "Download successful."
else
    echo "Download failed. Attempting fallback without cookies..."
    yt-dlp --no-warnings \
      --user-agent "$USER_AGENT" \
      -o "$OUTPUT_DIR/%(uploader)s - %(title).80s.%(ext)s" \
      "$URL"
fi
