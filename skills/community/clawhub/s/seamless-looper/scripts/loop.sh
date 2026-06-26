#!/bin/bash
# Seamless Looper — create seamless looping videos with crossfade at junction
# Usage: bash loop.sh <source_dir> <output_dir> [crossfade_seconds]
# Requires: ffmpeg, ffprobe

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: bash loop.sh <source_dir> <output_dir> [crossfade_seconds]"
  echo "Example: bash loop.sh ~/Videos/ambient ~/Videos/looped 1"
  exit 1
fi

SRC_DIR="$1"
DST_DIR="$2"
XFADE="${3:-1}"

mkdir -p "$DST_DIR"

if ! command -v ffmpeg &>/dev/null || ! command -v ffprobe &>/dev/null; then
  echo "ERROR: ffmpeg and ffprobe required. Install with: brew install ffmpeg"
  exit 1
fi

for f in "$SRC_DIR"/*.mp4; do
  if [ ! -f "$f" ]; then
    echo "No .mp4 files found in $SRC_DIR"
    exit 1
  fi

  filename=$(basename "$f")
  name="${filename%.mp4}"

  echo "Processing: $filename"

  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
  dur=${dur%.*}

  if [ -z "$dur" ] || [ "$dur" -lt 2 ]; then
    echo "  Skipping $filename — duration <2s or unknown"
    continue
  fi

  half_dur=$((dur - XFADE))

  echo "  Duration: ${dur}s | Crossfade: ${XFADE}s | Output: ${name}_looped.mp4"

  ffmpeg -y -stream_loop 1 -i "$f" -i "$f" \
    -filter_complex "[0:v]format=pix_fmts=yuva420p,fade=t=in:st=0:d=0.5:alpha=0[v0];[1:v]format=pix_fmts=yuva420p,fade=t=out:st=${half_dur}:d=${XFADE}:alpha=0[v1];[v0][v1]overlay=0:0:enable='between(t,${half_dur},'$(($half_dur + $XFADE))')'[out]" \
    -map "[out]" \
    -c:v libx264 -preset fast -crf 18 \
    -t "$((dur * 2))" \
    "$DST_DIR/${name}_looped.mp4" 2>/dev/null

  if [ $? -eq 0 ]; then
    echo "  ✓ Saved: ${name}_looped.mp4"
  else
    echo "  ✗ Failed: $filename"
  fi
done

echo ""
echo "Done! Looped videos → $DST_DIR"
