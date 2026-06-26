#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Smallest AI STT — Speech-to-Text via Pulse model
# 64ms time-to-first-token. Speaker diarization. Emotion detection.
#
# Usage:
#   stt.sh recording.wav
#   stt.sh meeting.mp3 --diarize --timestamps --emotions
#   stt.sh podcast.ogg --lang hi
#
# Output: JSON with transcription and optional metadata
# ============================================================

if [[ $# -lt 1 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  cat << 'USAGE'
Smallest AI STT — Pulse Model

Usage: stt.sh <audio_file> [options]

Options:
  --lang       <code>   Language: en|hi|es|fr|de|... (default: en)
  --diarize             Identify different speakers
  --timestamps          Include word-level timestamps
  --emotions            Detect emotional tone
  --format     <fmt>    Output: json|text (default: json)
  -h, --help            Show this help

Supported audio formats: WAV, MP3, OGG, FLAC, M4A

Examples:
  stt.sh meeting.wav --diarize --timestamps
  stt.sh voicenote.mp3 --lang hi
  stt.sh interview.wav --diarize --emotions --format text

Environment:
  SMALLEST_API_KEY   Required. Get from https://waves.smallest.ai
USAGE
  exit 0
fi

AUDIO="$1"
shift

# Validate audio file
if [[ ! -f "$AUDIO" ]]; then
  echo "Error: File not found: $AUDIO" >&2
  exit 1
fi

LANG="en"
DIARIZE="false"
TIMESTAMPS="false"
EMOTIONS="false"
FORMAT="json"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)       LANG="$2"; shift 2 ;;
    --diarize)    DIARIZE="true"; shift ;;
    --timestamps) TIMESTAMPS="true"; shift ;;
    --emotions)   EMOTIONS="true"; shift ;;
    --format)     FORMAT="$2"; shift 2 ;;
    *) echo "Warning: Unknown option $1" >&2; shift ;;
  esac
done

API_KEY="${SMALLEST_API_KEY:?Error: Set SMALLEST_API_KEY environment variable. Get yours at https://waves.smallest.ai}"

# Detect content type from extension
CONTENT_TYPE="audio/wav"
AUDIO_LOWER=$(printf '%s' "$AUDIO" | tr '[:upper:]' '[:lower:]')
case "$AUDIO_LOWER" in
  *.mp3)  CONTENT_TYPE="audio/mpeg" ;;
  *.ogg)  CONTENT_TYPE="audio/ogg" ;;
  *.flac) CONTENT_TYPE="audio/flac" ;;
  *.m4a)  CONTENT_TYPE="audio/mp4" ;;
  *.wav)  CONTENT_TYPE="audio/wav" ;;
  *)
    echo "Warning: Unknown audio format. Defaulting to audio/wav" >&2
    ;;
esac

# Check file size (warn if very large)
FILE_SIZE=$(wc -c < "$AUDIO" | tr -d ' ')
if [[ "$FILE_SIZE" -gt 26214400 ]]; then  # 25MB
  echo "Warning: Large file ($(( FILE_SIZE / 1048576 ))MB). This may take longer." >&2
fi

# Build query params
PARAMS="model=pulse&language=$LANG&diarize=$DIARIZE&word_timestamps=$TIMESTAMPS&emotion_detection=$EMOTIONS"

# API call
RESPONSE=$(curl -s \
  --connect-timeout 15 \
  --max-time 120 \
  -X POST \
  "https://api.smallest.ai/waves/v1/pulse/get_text?$PARAMS" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: $CONTENT_TYPE" \
  --data-binary "@$AUDIO" \
  -w "\n%{http_code}")

# Extract HTTP code (last line) and body (everything else)
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  200)
    if [[ "$FORMAT" == "text" ]]; then
      # Extract just the transcription text
      echo "$BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, dict):
        print(data.get('transcription', data.get('text', json.dumps(data))))
    else:
        print(data)
except:
    print(sys.stdin.read())
" 2>/dev/null || echo "$BODY"
    else
      echo "$BODY"
    fi
    ;;
  401)
    echo "Error: Invalid or expired API key." >&2
    exit 1
    ;;
  429)
    echo "Error: Rate limited. Wait and retry." >&2
    exit 1
    ;;
  413)
    echo "Error: Audio file too large. Try splitting into smaller segments." >&2
    exit 1
    ;;
  *)
    echo "Error: HTTP $HTTP_CODE" >&2
    echo "$BODY" >&2
    exit 1
    ;;
esac
