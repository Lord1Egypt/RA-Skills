#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 TEXT_FILE OUTPUT_MP3 [VOICE] [MAX_DIRECT_CHARS]" >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
TEXT_FILE="$1"
OUTPUT_MP3="$2"
VOICE="${3:-ru-RU-DmitryNeural}"
MAX_DIRECT_CHARS="${4:-280}"
STATE_DIR="$WORKSPACE/skills/text-to-voice-local/state"
LAST_FILE="$STATE_DIR/last-output.txt"
LATEST_MP3="$WORKSPACE/tmp/voice-mode-latest.mp3"
mkdir -p "$STATE_DIR" "$WORKSPACE/tmp"
TMP_OUT="${OUTPUT_MP3}.tmp.$$"
cleanup(){ rm -f "$TMP_OUT"; }
trap cleanup EXIT
CHARS=$(wc -m < "$TEXT_FILE" | tr -d ' ')
if [ "$CHARS" -le "$MAX_DIRECT_CHARS" ]; then
  node "$SCRIPT_DIR/edge_tts.js" --voice "$VOICE" --out "$TMP_OUT" "$(cat "$TEXT_FILE")" >/dev/null
else
  "$SCRIPT_DIR/tts_from_file_chunked.sh" "$TEXT_FILE" "$TMP_OUT" "$VOICE" >/dev/null
fi
[ -s "$TMP_OUT" ] || exit 1
mv -f "$TMP_OUT" "$OUTPUT_MP3"
if [ "$OUTPUT_MP3" != "$LATEST_MP3" ]; then cp -f "$OUTPUT_MP3" "$LATEST_MP3"; fi
printf '%s\n' "$OUTPUT_MP3" > "$LAST_FILE"
trap - EXIT
printf '%s\n' "$OUTPUT_MP3"
