#!/bin/bash

# Twitter Video Downloader Script
# Usage: ./download.sh <twitter-url> [options]

set -e

# Default settings
QUALITY="best"
AUDIO_ONLY=false
OUTPUT_DIR="$HOME/Downloads/twitter-videos"
AUDIO_DIR="$HOME/Downloads/twitter-audio"
PROXY=""
URL=""

# Show network warning
show_network_warning() {
  echo ""
  echo "⚠️  Network Notice:"
  echo "   If you are in a network-restricted country/region (e.g., China mainland),"
  echo "   Twitter/X may be blocked. Please use the --proxy option:"
  echo ""
  echo "   $0 \"$URL\" --proxy http://127.0.0.1:7890"
  echo ""
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --quality|-q)
      QUALITY="$2"
      shift 2
      ;;
    --audio-only|-a)
      AUDIO_ONLY=true
      shift
      ;;
    --output|-o)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --proxy|-p)
      PROXY="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 <twitter-url> [options]"
      echo ""
      echo "Options:"
      echo "  -q, --quality <quality>   Video quality: best, 1080, 720, 480, 360"
      echo "  -a, --audio-only          Download audio only (MP3)"
      echo "  -o, --output <dir>        Output directory"
      echo "  -p, --proxy <url>         Proxy URL (e.g., http://127.0.0.1:7890)"
      echo "  -h, --help                Show this help"
      echo ""
      echo "Examples:"
      echo "  $0 \"https://x.com/user/status/123\""
      echo "  $0 \"https://x.com/user/status/123\" -p http://127.0.0.1:7890"
      echo "  $0 \"https://x.com/user/status/123\" -a -p socks5://127.0.0.1:1080"
      exit 0
      ;;
    *)
      if [[ -z "$URL" ]]; then
        URL="$1"
      fi
      shift
      ;;
  esac
done

# Validate URL
if [[ -z "$URL" ]]; then
  echo "❌ Error: Please provide a Twitter/X URL"
  echo "Usage: $0 <twitter-url>"
  exit 1
fi

# Check if URL is valid Twitter/X URL
if [[ ! "$URL" =~ ^https?://(www\.)?(twitter|x)\.com/[^/]+/status/[0-9]+ ]]; then
  echo "❌ Error: Invalid Twitter/X URL"
  echo "Supported formats:"
  echo "  - https://twitter.com/username/status/1234567890"
  echo "  - https://x.com/username/status/1234567890"
  exit 1
fi

# Create output directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$AUDIO_DIR"

echo "🐦 Twitter Video Downloader"
echo "🔗 URL: $URL"

# Build proxy args
PROXY_ARGS=""
if [[ -n "$PROXY" ]]; then
  echo "🌐 Proxy: $PROXY"
  PROXY_ARGS="--proxy $PROXY"
fi

# Download based on mode
if [[ "$AUDIO_ONLY" == true ]]; then
  echo "🎵 Mode: Audio Only (MP3)"
  echo "📁 Output: $AUDIO_DIR"
  
  if ! yt-dlp \
    --extract-audio \
    --audio-format mp3 \
    --audio-quality 0 \
    --output "$AUDIO_DIR/%(title)s_%(id)s.%(ext)s" \
    --no-warnings \
    --progress \
    $PROXY_ARGS \
    "$URL" 2>&1; then
    
    echo ""
    echo "❌ Download failed!"
    show_network_warning
    exit 1
  fi
  
  echo ""
  echo "✅ Audio downloaded successfully!"
  echo "📁 Location: $AUDIO_DIR"
else
  echo "🎬 Mode: Video"
  echo "📊 Quality: $QUALITY"
  echo "📁 Output: $OUTPUT_DIR"
  
  # Build format string based on quality
  case "$QUALITY" in
    1080)
      FORMAT="bestvideo[height<=1080]+bestaudio/best[height<=1080]"
      ;;
    720)
      FORMAT="bestvideo[height<=720]+bestaudio/best[height<=720]"
      ;;
    480)
      FORMAT="bestvideo[height<=480]+bestaudio/best[height<=480]"
      ;;
    360)
      FORMAT="bestvideo[height<=360]+bestaudio/best[height<=360]"
      ;;
    *)
      FORMAT="bestvideo+bestaudio/best"
      ;;
  esac
  
  if ! yt-dlp \
    --format "$FORMAT" \
    --merge-output-format mp4 \
    --output "$OUTPUT_DIR/%(title)s_%(id)s.%(ext)s" \
    --no-warnings \
    --progress \
    $PROXY_ARGS \
    "$URL" 2>&1; then
    
    echo ""
    echo "❌ Download failed!"
    show_network_warning
    exit 1
  fi
  
  echo ""
  echo "✅ Video downloaded successfully!"
  echo "📁 Location: $OUTPUT_DIR"
fi

echo ""
echo "🎉 Download complete!"
