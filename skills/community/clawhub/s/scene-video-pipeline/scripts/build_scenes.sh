#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   build_scenes.sh <module_dir>
# Expects:
#   <module_dir>/slides/NN.png
#   <module_dir>/tts/audio/NN.mp3
# Produces:
#   <module_dir>/dist/scenes/NN.mp4
#   <module_dir>/dist/scene-order.txt (if missing)

MODULE_DIR="${1:?module_dir required}"
SLIDES_DIR="$MODULE_DIR/slides"
AUDIO_DIR="$MODULE_DIR/tts/audio"
DIST_DIR="$MODULE_DIR/dist"
SCENES_DIR="$DIST_DIR/scenes"
ORDER_FILE="$DIST_DIR/scene-order.txt"

mkdir -p "$SCENES_DIR"

for audio in "$AUDIO_DIR"/*.mp3; do
  [ -e "$audio" ] || { echo "No audio files found in $AUDIO_DIR"; exit 1; }
  base="$(basename "$audio" .mp3)"
  slide="$SLIDES_DIR/${base}.png"
  out="$SCENES_DIR/${base}.mp4"

  [ -f "$slide" ] || { echo "Missing slide image: $slide"; exit 1; }

  duration="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$audio")"

  ffmpeg -y \
    -loop 1 -framerate 30 -t "$duration" -i "$slide" \
    -i "$audio" \
    -c:v libx264 -pix_fmt yuv420p -r 30 \
    -c:a aac -b:a 192k -shortest \
    "$out" >/dev/null 2>&1

  echo "Built scene: $out"
done

if [ ! -f "$ORDER_FILE" ]; then
  ls "$SCENES_DIR"/*.mp4 | sort | xargs -n1 basename > "$ORDER_FILE"
  echo "Created default scene order: $ORDER_FILE"
fi

echo "Scene build complete: $SCENES_DIR"
