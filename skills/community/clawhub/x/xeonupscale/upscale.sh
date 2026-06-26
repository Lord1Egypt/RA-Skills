#!/usr/bin/env bash
# xeonupscale: ffmpeg lanczos upscale (e.g. 480p->540p->1080p).
# Usage:
#   upscale.sh <input> <WxH|preset> [output]
# Presets: 540p (960x540), 720p (1280x720), 1080p (1920x1080), 1440p, 2160p
# Examples:
#   upscale.sh in.mp4 540p
#   upscale.sh in.mp4 1920x1080 out_1080p.mp4
set -euo pipefail

IN="${1:?usage: $0 <input> <WxH|preset> [output]}"
TGT="${2:?usage: $0 <input> <WxH|preset> [output]}"
case "$TGT" in
  540p)  RES="960x540" ;;
  720p)  RES="1280x720" ;;
  1080p) RES="1920x1080" ;;
  1440p) RES="2560x1440" ;;
  2160p|4k) RES="3840x2160" ;;
  *x*)   RES="$TGT" ;;
  *) echo "unknown preset/resolution: $TGT"; exit 1 ;;
esac
W="${RES%x*}"; H="${RES#*x}"

OUT="${3:-${IN%.*}_${RES}.mp4}"

FFMPEG="${FFMPEG:-ffmpeg}"
"$FFMPEG" -y -i "$IN" \
  -vf "scale=${W}:${H}:flags=lanczos" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a copy "$OUT"

echo "✓ $OUT"
