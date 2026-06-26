#!/usr/bin/env bash
set -euo pipefail
URL="${1:?URL required}"
OUT_DIR="${2:-video-download}"
mkdir -p "$OUT_DIR"
yt-dlp -f 'bv*+ba/best' --merge-output-format mp4 -o "$OUT_DIR/%(title).120s-%(id)s.%(ext)s" "$URL"
find "$OUT_DIR" -type f -name '*.mp4' -o -type f -name '*.mov' -o -type f -name '*.mkv' | sort | tail -1
