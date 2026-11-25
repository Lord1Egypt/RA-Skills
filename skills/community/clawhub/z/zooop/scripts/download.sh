#!/usr/bin/env bash
# Download a Zooop task's first output to ~/Desktop, picking the extension
# from the response Content-Type. Pass either a taskId or a direct URL.
#
# Usage:  download.sh <taskId>
#         download.sh <url>
#         download.sh <taskId|url> /custom/output/path
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <taskId|url> [outputPath]" >&2
  exit 64
fi

ARG="$1"
OUT_OVERRIDE="${2:-}"

if [[ "$ARG" =~ ^https?:// ]]; then
  URL="$ARG"
else
  RESPONSE=$(curl -fsS "$HOST/v1/tasks/$ARG" \
    -H "Authorization: Bearer $ZOOOP_API_KEY")
  URL=$(printf '%s' "$RESPONSE" | grep -oE '"url":"[^"]+"' | head -1 | cut -d'"' -f4)
  if [[ -z "$URL" ]]; then
    echo "no output url on task $ARG" >&2
    printf '%s\n' "$RESPONSE" >&2
    exit 2
  fi
fi

CT=$(curl -sIL "$URL" | awk 'tolower($1)=="content-type:" {print $2}' | tail -1 | tr -d '\r')
case "$CT" in
  image/png)   EXT=png ;;
  image/jpeg)  EXT=jpg ;;
  image/*)     EXT="${CT#image/}" ;;
  video/mp4)   EXT=mp4 ;;
  video/*)     EXT="${CT#video/}" ;;
  audio/mpeg)  EXT=mp3 ;;
  audio/*)     EXT="${CT#audio/}" ;;
  *)           EXT=bin ;;
esac

OUT="${OUT_OVERRIDE:-$HOME/Desktop/zooop-$(date +%Y%m%d-%H%M%S).$EXT}"
curl -fL -o "$OUT" "$URL"
echo "$OUT"
