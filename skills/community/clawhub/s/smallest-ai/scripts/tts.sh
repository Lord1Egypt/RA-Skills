#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Smallest AI TTS — Text-to-Speech via Lightning model
# Ultra-fast speech generation with sub-100ms latency
#
# Usage:
#   tts.sh "Hello world"
#   tts.sh "Hello world" --voice robert --rate 24000 --speed 1.2
#   tts.sh "नमस्ते दुनिया" --voice advika --lang hi
#
# Output: MEDIA: <path_to_wav_file>
# ============================================================

# --- Argument parsing ---
if [[ $# -lt 1 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  cat << 'USAGE'
Smallest AI TTS — Lightning Model

Usage: tts.sh "text" [options]

Options:
  --voice <id>     Voice: sophia|robert|advika|vivaan|camilla (default: sophia)
  --rate  <hz>     Sample rate: 8000|16000|24000|48000 (default: 24000)
  --speed <n>      Speed: 0.5-2.0 (default: 1.0)
  --lang  <code>   Language: en|hi|es|fr|de|ja|ko|zh|... (default: en)
  --out   <path>   Output file (default: media/tts_<timestamp>.wav)
  -h, --help       Show this help

Examples:
  tts.sh "Good morning! Here is your daily briefing."
  tts.sh "Meeting starts in 5 minutes" --voice robert --speed 1.3
  tts.sh "आज का मौसम बहुत अच्छा है" --voice advika --lang hi

Environment:
  SMALLEST_API_KEY   Required. Get from https://waves.smallest.ai
USAGE
  exit 0
fi

TEXT="$1"
shift

VOICE="sophia"
RATE=24000
SPEED=1.0
LANG="en"
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice) VOICE="$2"; shift 2 ;;
    --rate)  RATE="$2"; shift 2 ;;
    --speed) SPEED="$2"; shift 2 ;;
    --lang)  LANG="$2"; shift 2 ;;
    --out)   OUT="$2"; shift 2 ;;
    *) echo "Warning: Unknown option $1" >&2; shift ;;
  esac
done

# --- Validate ---
API_KEY="${SMALLEST_API_KEY:?Error: Set SMALLEST_API_KEY environment variable. Get yours at https://waves.smallest.ai}"

if [[ -z "$TEXT" ]]; then
  echo "Error: Text cannot be empty" >&2
  exit 1
fi

# Check text length (~5000 char limit)
TEXT_LEN=${#TEXT}
if [[ $TEXT_LEN -gt 5000 ]]; then
  echo "Warning: Text is $TEXT_LEN chars (limit ~5000). Consider splitting into chunks." >&2
fi

# --- Output path ---
if [[ -z "$OUT" ]]; then
  TIMESTAMP=$(date +%s%3N 2>/dev/null || date +%s)
  OUT="media/tts_${VOICE}_${TIMESTAMP}.wav"
fi

mkdir -p "$(dirname "$OUT")"

# --- Escape text for JSON ---
# Handle quotes, backslashes, newlines in the text
JSON_TEXT=$(printf '%s' "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || printf '%s' "$TEXT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
# Remove outer quotes if python3 was used (json.dumps adds them)
JSON_TEXT="${JSON_TEXT#\"}"
JSON_TEXT="${JSON_TEXT%\"}"

# --- API call ---
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

HTTP_CODE=$(curl -s -w "%{http_code}" -o "$OUT" \
  --connect-timeout 10 \
  --max-time 30 \
  -X POST "https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"$JSON_TEXT\",
    \"voice_id\": \"$VOICE\",
    \"sample_rate\": $RATE,
    \"speed\": $SPEED,
    \"language\": \"$LANG\",
    \"output_format\": \"wav\"
  }" 2>"$TMPFILE")

# --- Handle response ---
case "$HTTP_CODE" in
  200)
    # Verify file is not empty and looks like audio
    FILE_SIZE=$(wc -c < "$OUT" | tr -d ' ')
    if [[ "$FILE_SIZE" -lt 100 ]]; then
      echo "Error: Generated audio file is suspiciously small (${FILE_SIZE} bytes)" >&2
      cat "$OUT" >&2
      rm -f "$OUT"
      exit 1
    fi
    echo "MEDIA: $OUT"
    ;;
  401)
    echo "Error: Invalid or expired API key. Check SMALLEST_API_KEY." >&2
    rm -f "$OUT"
    exit 1
    ;;
  429)
    echo "Error: Rate limited. Wait a moment and try again." >&2
    rm -f "$OUT"
    exit 1
    ;;
  400)
    echo "Error: Bad request. Check voice_id and text length." >&2
    cat "$OUT" >&2 2>/dev/null || true
    rm -f "$OUT"
    exit 1
    ;;
  *)
    echo "Error: HTTP $HTTP_CODE" >&2
    cat "$OUT" >&2 2>/dev/null || true
    cat "$TMPFILE" >&2 2>/dev/null || true
    rm -f "$OUT"
    exit 1
    ;;
esac
