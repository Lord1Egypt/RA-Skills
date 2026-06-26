#!/bin/bash
set -e

# Generate TTS audio segments from a JSON sections file using edge-tts.
# Usage: generate-tts.sh <sections_json> <output_dir> [voice] [rate]
#
# sections_json: JSON array of strings, each string is one narration segment.
#   Example: ["First segment text.", "Second segment text."]
#
# Output: seg01.mp3, seg02.mp3, ..., narration.mp3 (concatenated with gaps)

SECTIONS_JSON="${1:?Usage: generate-tts.sh <sections_json> <output_dir> [voice] [rate]}"
OUTPUT_DIR="${2:?Usage: generate-tts.sh <sections_json> <output_dir> [voice] [rate]}"
VOICE="${3:-en-US-GuyNeural}"
RATE="${4:-+0%}"

mkdir -p "$OUTPUT_DIR"

python3 << PYEOF
import asyncio
import json
import edge_tts

with open("$SECTIONS_JSON") as f:
    segments = json.load(f)

voice = "$VOICE"
rate = "$RATE"
output_dir = "$OUTPUT_DIR"

async def generate():
    for i, text in enumerate(segments, 1):
        comm = edge_tts.Communicate(text, voice, rate=rate)
        fname = f"{output_dir}/seg{i:02d}.mp3"
        await comm.save(fname)
        print(f"Generated {fname}")

asyncio.run(generate())
PYEOF

# Create silence gap
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.4 -q:a 9 -c:a libmp3lame \
  "${OUTPUT_DIR}/silence.mp3" 2>/dev/null

# Build concat list
CONCAT_FILE="${OUTPUT_DIR}/concat.txt"
> "$CONCAT_FILE"
for f in "${OUTPUT_DIR}"/seg*.mp3; do
  [ "$(basename "$f")" = "silence.mp3" ] && continue
  echo "file '$(basename "$f")'" >> "$CONCAT_FILE"
  echo "file 'silence.mp3'" >> "$CONCAT_FILE"
done
# Remove trailing silence entry
sed -i.bak '$ d' "$CONCAT_FILE" && rm -f "${CONCAT_FILE}.bak"

# Concatenate
ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c:a libmp3lame -q:a 2 \
  "${OUTPUT_DIR}/narration.mp3" 2>/dev/null

DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "${OUTPUT_DIR}/narration.mp3")
echo "Narration generated: ${OUTPUT_DIR}/narration.mp3 (${DURATION}s)"
