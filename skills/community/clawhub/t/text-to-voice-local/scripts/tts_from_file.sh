#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 INPUT_TXT OUTPUT_MP3 [VOICE]" >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_TXT="$1"
OUTPUT_MP3="$2"
VOICE="${3:-ru-RU-DmitryNeural}"
TEXT="$(cat "$INPUT_TXT")"
TMP_OUT="${OUTPUT_MP3}.tmp.$$"
cleanup(){ rm -f "$TMP_OUT"; }
trap cleanup EXIT
ATTEMPTS="${TTS_RETRIES:-3}"
for i in $(seq 1 "$ATTEMPTS"); do
  if node "$SCRIPT_DIR/edge_tts.js" --voice "$VOICE" --out "$TMP_OUT" "$TEXT" >/dev/null 2>&1; then
    if [ -s "$TMP_OUT" ]; then
      mv -f "$TMP_OUT" "$OUTPUT_MP3"
      trap - EXIT
      printf '%s\n' "$OUTPUT_MP3"
      exit 0
    fi
  fi
  sleep 1
done
exit 1
