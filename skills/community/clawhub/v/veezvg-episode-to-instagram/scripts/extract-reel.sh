#!/bin/bash
# extract-reel.sh — Extract a reel clip from the source video
# Usage: ./extract-reel.sh <video_file> <output_path> <start_seconds> <duration_seconds>
# Outputs: vertical 9:16 clip with optional crop, re-encoded for Instagram Reels

set -euo pipefail

VIDEO_FILE="${1:?Usage: extract-reel.sh <video_file> <output_path> <start> <duration>}"
OUTPUT_PATH="${2:?Usage: extract-reel.sh <video_file> <output_path> <start> <duration>}"
START="${3:?Provide start time in seconds}"
DURATION="${4:-90}"

echo "==> Extracting reel: ${START}s to $((START + DURATION))s..."

# Get source video dimensions
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO_FILE")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO_FILE")

echo "  Source: ${WIDTH}x${HEIGHT}"

# If source is landscape (16:9), center-crop to 9:16 portrait
if [ "$WIDTH" -gt "$HEIGHT" ]; then
    # Landscape → portrait: crop center
    CROP_W=$((HEIGHT * 9 / 16))
    CROP_X=$(( (WIDTH - CROP_W) / 2 ))
    FILTER="crop=${CROP_W}:${HEIGHT}:${CROP_X}:0,scale=1080:1920"
    echo "  Cropping landscape to portrait: ${CROP_W}x${HEIGHT} → 1080x1920"
else
    # Already portrait or square, just scale
    FILTER="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
    echo "  Scaling to 1080x1920"
fi

ffmpeg -y -ss "$START" -i "$VIDEO_FILE" -t "$DURATION" \
    -vf "$FILTER" \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    "$OUTPUT_PATH" 2>/dev/null

FILESIZE=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat --printf="%s" "$OUTPUT_PATH" 2>/dev/null)
echo "==> Reel saved: $OUTPUT_PATH ($(( FILESIZE / 1024 / 1024 ))MB)"
