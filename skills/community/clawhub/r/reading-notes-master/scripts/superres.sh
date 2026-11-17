#!/usr/bin/env bash
# superres.sh — reading-notes-master v2.3 图形资产管线 A6
# Real-ESRGAN 图片超分（upscayl-bin ncnn-vulkan 预编译版，realesrgan-x4plus 模型内嵌，
# arm64 原生、零 Python 依赖——刻意不走 pip realesrgan，basicsr 与 Python 3.13 不兼容）。
# 用法: superres.sh <input.png|jpg|webp> <output.png> [--scale 2|3|4] [--model NAME]
set -euo pipefail

usage() { echo "Usage: $0 <input> <output> [--scale 2|3|4] [--model realesrgan-x4plus]"; exit 1; }
[ $# -lt 2 ] && usage
IN="$1"; OUT="$2"; SCALE=4; MODEL="realesrgan-x4plus"
shift 2
while [ $# -gt 0 ]; do
  case "$1" in
    --scale) SCALE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    *) shift;;
  esac
done
[ -f "$IN" ] || { echo "ERROR: input not found: $IN"; exit 2; }

# ---- upscayl-bin discovery: PATH -> ~/.workbuddy/bin ----
UPS="$(command -v upscayl-bin || true)"
[ -z "$UPS" ] && [ -x "$HOME/.workbuddy/bin/upscayl-bin" ] && UPS="$HOME/.workbuddy/bin/upscayl-bin"
[ -z "$UPS" ] && { echo "ERROR: upscayl-bin not found. Fix: download from github.com/upscayl/upscayl-ncnn/releases -> cp to ~/.workbuddy/bin/"; exit 3; }

"$UPS" -i "$IN" -o "$OUT" -s "$SCALE" -n "$MODEL" 2>&1 | grep -E "Upscayled|ERROR|Error" || true
[ -f "$OUT" ] && echo "OK: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes, scale=${SCALE}x, model=$MODEL)" || { echo "ERROR: no output"; exit 4; }
