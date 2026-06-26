#!/bin/bash
set -e

# Merge narration audio onto a video file.
# Usage: merge-audio.sh <video_path> <audio_path> [output_path]

VIDEO_PATH="${1:?Usage: merge-audio.sh <video_path> <audio_path> [output_path]}"
AUDIO_PATH="${2:?Usage: merge-audio.sh <video_path> <audio_path> [output_path]}"

# Default output: "<name> (with narration).<ext>"
if [ -n "$3" ]; then
  OUTPUT_PATH="$3"
else
  DIR=$(dirname "$VIDEO_PATH")
  BASE=$(basename "$VIDEO_PATH")
  EXT="${BASE##*.}"
  NAME="${BASE%.*}"
  OUTPUT_PATH="${DIR}/${NAME} (with narration).${EXT}"
fi

echo "Merging audio onto video..."
ffmpeg -y \
  -i "$VIDEO_PATH" \
  -i "$AUDIO_PATH" \
  -c:v copy \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  "$OUTPUT_PATH" 2>&1 | tail -3

# Verify
V_STREAMS=$(ffprobe -v quiet -show_entries stream=codec_type -of csv=p=0 "$OUTPUT_PATH" | sort -u | tr '\n' '+')
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_PATH")
SIZE=$(ls -lh "$OUTPUT_PATH" | awk '{print $5}')

echo "Output: $OUTPUT_PATH"
echo "Duration: ${DURATION}s | Size: ${SIZE} | Streams: ${V_STREAMS%+}"
