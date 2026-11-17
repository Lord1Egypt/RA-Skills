#!/usr/bin/env bash
# bitmap2vector.sh — reading-notes-master v2.3 图形资产管线 A5
# 位图 → SVG 矢量描摹。默认 vtracer（彩色保留）；--bw 切 potrace（黑白/单色，稿线更干净）。
# 用法: bitmap2vector.sh <input.png|jpg|bmp> <output.svg> [--bw]
set -euo pipefail

usage() { echo "Usage: $0 <input-image> <output.svg> [--bw]"; exit 1; }
[ $# -lt 2 ] && usage

IN="$1"; OUT="$2"; MODE="color"
[ "${3:-}" = "--bw" ] && MODE="bw"
[ -f "$IN" ] || { echo "ERROR: input not found: $IN"; exit 2; }

# ---- tool discovery: PATH -> managed venv -> homebrew ----
find_tool() {
  if command -v "$1" >/dev/null 2>&1; then command -v "$1"
  elif [ -x "$HOME/.workbuddy/binaries/python/envs/default/bin/$1" ]; then echo "$HOME/.workbuddy/binaries/python/envs/default/bin/$1"
  elif [ -x "/opt/homebrew/bin/$1" ]; then echo "/opt/homebrew/bin/$1"
  else echo ""; fi
}

if [ "$MODE" = "bw" ]; then
  POTRACE="$(find_tool potrace)"
  [ -z "$POTRACE" ] && { echo "ERROR: potrace not found. Fix: brew install potrace"; exit 3; }
  # potrace 只吃 PBM/PPM：先用 Python 标准链路转灰度 PBM 再描摹
  PY="${PYTHON:-$(find_tool python3)}"
  BMP="${IN%.*}.pbm"
  "$PY" - "$IN" "$BMP" <<'EOF'
import sys
from PIL import Image
img = Image.open(sys.argv[1]).convert("L")
img = img.point(lambda p: 0 if p < 128 else 255, mode="1")
img.save(sys.argv[2])
EOF
  "$POTRACE" "$BMP" -s -o "$OUT" --flat
  rm -f "$BMP"
else
  VTRACER="$(find_tool vtracer)"
  [ -z "$VTRACER" ] && { echo "ERROR: vtracer not found. Fix: pip install vtracer (managed venv) + CLI wrapper"; exit 3; }
  "$VTRACER" --input "$IN" --output "$OUT" \
    --colormode color --hierarchical stacked --mode spline \
    --filter_speckle 8 --color_precision 6 --layer_difference 16 \
    --corner_threshold 60 --length_threshold 4.0 --splice_threshold 45 --path_precision 3
fi

[ -f "$OUT" ] && echo "OK: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes, mode=$MODE)" || { echo "ERROR: no output"; exit 4; }
