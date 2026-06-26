#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   stitch_scenes.sh <module_dir> [order_file]
# Expects:
#   <module_dir>/dist/scenes/*.mp4
#   order file lines: NN.mp4
# Produces:
#   <module_dir>/dist/module-first-cut.mp4

MODULE_DIR="${1:?module_dir required}"
DIST_DIR="$MODULE_DIR/dist"
SCENES_DIR="$DIST_DIR/scenes"
ORDER_FILE="${2:-$DIST_DIR/scene-order.txt}"
CONCAT_FILE="$DIST_DIR/concat-scenes.txt"
OUT_FILE="$DIST_DIR/module-first-cut.mp4"

[ -d "$SCENES_DIR" ] || { echo "Missing scenes dir: $SCENES_DIR"; exit 1; }
[ -f "$ORDER_FILE" ] || { echo "Missing scene order file: $ORDER_FILE"; exit 1; }

: > "$CONCAT_FILE"
while IFS= read -r line; do
  line="${line%%#*}"
  line="$(echo "$line" | xargs)"
  [ -z "$line" ] && continue

  scene="$SCENES_DIR/$line"
  [ -f "$scene" ] || { echo "Scene listed but missing: $scene"; exit 1; }
  echo "file '$scene'" >> "$CONCAT_FILE"
done < "$ORDER_FILE"

ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$OUT_FILE" >/dev/null 2>&1

echo "Built final: $OUT_FILE"
