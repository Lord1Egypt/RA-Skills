#!/bin/bash
# Transcribe audio/video files using Whisper API via curl
# Usage: ./transcribe.sh inputfile.ogg or inputfile.mp4

FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: $0 <audio_file.ogg | video_file.mp4>"
    exit 1
fi

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found"
    exit 1
fi

# Transcribe using curl (no Python dependencies)
curl -s -X POST "http://192.168.0.11:8080/v1/audio/transcriptions" \
  -F "file=@$FILE" \
  -F "model=whisper-small"