#!/usr/bin/env bash
set -euo pipefail

TEXT="${1:-}"
OUTPUT="${2:-/tmp/edge-tts-output.mp3}"
VOICE="${3:-zh-CN-XiaoxiaoNeural}"

if [[ -z "$TEXT" ]]; then
  echo "Usage: edge-tts.sh \"文本\" [输出文件] [声音]" >&2
  exit 1
fi

edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$OUTPUT"
echo "$OUTPUT"
