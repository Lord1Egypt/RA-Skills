#!/bin/bash
set -e

# Extract key frames from a video at regular intervals.
# Usage: extract-frames.sh <video_path> [output_dir] [interval_seconds]

VIDEO_PATH="${1:?Usage: extract-frames.sh <video_path> [output_dir] [interval_seconds]}"
OUTPUT_DIR="${2:-${VIDEO_PATH%.*}_frames}"
INTERVAL="${3:-5}"

mkdir -p "$OUTPUT_DIR"

echo "Extracting frames every ${INTERVAL}s from: $VIDEO_PATH"
ffmpeg -i "$VIDEO_PATH" -vf "fps=1/${INTERVAL}" -q:v 2 "${OUTPUT_DIR}/frame_%03d.jpg" 2>&1 | tail -3

DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO_PATH")
COUNT=$(ls -1 "${OUTPUT_DIR}"/frame_*.jpg 2>/dev/null | wc -l | tr -d ' ')
echo "Extracted ${COUNT} frames (video duration: ${DURATION}s)"
echo "Output directory: ${OUTPUT_DIR}"
