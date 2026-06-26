#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 input.gif output-dir [fps]" >&2
  exit 1
fi

INPUT="$1"
OUTDIR="$2"
FPS="${3:-1}"
mkdir -p "$OUTDIR"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 2
fi

ffmpeg -hide_banner -loglevel error -i "$INPUT" -vf "fps=${FPS}" "$OUTDIR/frame-%04d.png"
ls -1 "$OUTDIR"/frame-*.png
