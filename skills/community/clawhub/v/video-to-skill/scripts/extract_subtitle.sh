#!/bin/bash
# Step 1: Extract subtitle from YouTube video using MiniMax API
# Usage: ./extract_subtitle.sh <video_url>
set -e

VIDEO_URL="$1"
OUTPUT_FILE="${2:-/tmp/subtitle.srt}"
MINIMAX_API_KEY="${MINIMAX_API_KEY:-}"

if [ -z "$VIDEO_URL" ]; then
  echo "ERROR: video_url is required"
  exit 1
fi

if [ -z "$MINIMAX_API_KEY" ]; then
  echo "ERROR: MINIMAX_API_KEY is not set"
  exit 1
fi

echo "Extracting subtitle from: $VIDEO_URL"

RESPONSE=$(curl -s -X POST "https://api.minimax.chat/v1/video/subtitle" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg url "$VIDEO_URL" '{"video_url": $url, "format": "srt"}')")

if echo "$RESPONSE" | jq -e '.code' | grep -q '"0"'; then
  echo "$RESPONSE" | jq -r '.data.subtitle // .data // .subtitle // .content' > "$OUTPUT_FILE"
  echo "SUBTITLE_FILE=$OUTPUT_FILE"
  echo "SUBTITLE_AVAILABLE=true"
else
  echo "SUBTITLE_AVAILABLE=false"
  echo "SUBTITLE_ERROR=$(echo "$RESPONSE" | jq -r '.message // .error // "unknown_error"')"
  exit 1
fi
