#!/usr/bin/env bash
# YouTube Transcriber — one-command video transcription
# Downloads audio + transcribes via OpenAI Whisper API
# Works even when YouTube subtitles are disabled
set -euo pipefail

# --- Defaults ---
LANG_CODE=""
OUT_FILE=""
FORCE_WHISPER=false
KEEP_AUDIO=false
AUDIO_BITRATE=64
URL=""

usage() {
  cat >&2 <<'EOF'
Usage:
  transcribe.sh <youtube-url> [options]

Options:
  --lang <code>           Language hint (en, zh, ja, ko, etc.)
  --out <path>            Output transcript file path
  --force-whisper         Skip subtitle check, always use Whisper
  --keep-audio            Keep downloaded audio file
  --audio-bitrate <kbps>  Audio compression bitrate (default: 64)
  -h, --help              Show this help
EOF
  exit 2
}

# --- Parse args ---
[[ $# -eq 0 ]] && usage

URL="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)        LANG_CODE="${2:-}"; shift 2 ;;
    --out)         OUT_FILE="${2:-}"; shift 2 ;;
    --force-whisper) FORCE_WHISPER=true; shift ;;
    --keep-audio)  KEEP_AUDIO=true; shift ;;
    --audio-bitrate) AUDIO_BITRATE="${2:-64}"; shift 2 ;;
    -h|--help)     usage ;;
    *)             echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Extract video ID ---
VIDEO_ID=""
if [[ "$URL" =~ v=([a-zA-Z0-9_-]{11}) ]]; then
  VIDEO_ID="${BASH_REMATCH[1]}"
elif [[ "$URL" =~ youtu\.be/([a-zA-Z0-9_-]{11}) ]]; then
  VIDEO_ID="${BASH_REMATCH[1]}"
elif [[ "$URL" =~ ^[a-zA-Z0-9_-]{11}$ ]]; then
  VIDEO_ID="$URL"
  URL="https://www.youtube.com/watch?v=$VIDEO_ID"
fi

if [[ -z "$VIDEO_ID" ]]; then
  echo "Error: Could not extract video ID from URL" >&2
  exit 1
fi

# --- Default output path ---
if [[ -z "$OUT_FILE" ]]; then
  OUT_FILE="/tmp/yt_transcript_${VIDEO_ID}.txt"
fi

# --- Find yt-dlp ---
YTDLP=""
for p in "$HOME/.venvs/agent-reach/bin/yt-dlp" /opt/homebrew/bin/yt-dlp "$HOME/Library/Python/3.9/bin/yt-dlp" yt-dlp; do
  if command -v "$p" &>/dev/null || [[ -x "$p" ]]; then
    YTDLP="$p"
    break
  fi
done

if [[ -z "$YTDLP" ]]; then
  echo "Error: yt-dlp not found. Install with: brew install yt-dlp" >&2
  exit 1
fi

# --- Find ffmpeg ---
FFMPEG=""
for p in ffmpeg /opt/homebrew/bin/ffmpeg /usr/local/bin/ffmpeg; do
  if command -v "$p" &>/dev/null || [[ -x "$p" ]]; then
    FFMPEG="$p"
    break
  fi
done

if [[ -z "$FFMPEG" ]]; then
  echo "Error: ffmpeg not found. Install with: brew install ffmpeg" >&2
  exit 1
fi

# --- Step 1: Try subtitles first (unless --force-whisper) ---
if [[ "$FORCE_WHISPER" == false ]]; then
  echo ">>> Checking for existing subtitles..." >&2

  SUB_LANG="${LANG_CODE:-en}"
  SUB_DIR=$(mktemp -d)
  SUB_FILE=""

  if $YTDLP --write-sub --write-auto-sub --sub-lang "${SUB_LANG},zh-Hans,zh,en" \
       --skip-download --sub-format vtt \
       -o "${SUB_DIR}/%(id)s" "$URL" 2>/dev/null; then
    # Find the downloaded subtitle file
    SUB_FILE=$(find "$SUB_DIR" -name "*.vtt" -type f 2>/dev/null | head -1)
  fi

  if [[ -n "$SUB_FILE" && -s "$SUB_FILE" ]]; then
    echo ">>> Subtitles found! Extracting clean transcript..." >&2

    # Parse VTT to clean text
    python3 -c "
import re, sys

with open('$SUB_FILE', 'r') as f:
    content = f.read()

# Remove VTT header
content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)

# Remove timestamps and cue metadata
lines = []
seen = set()
for line in content.split('\n'):
    line = line.strip()
    # Skip timestamp lines
    if re.match(r'^\d{2}:\d{2}', line):
        continue
    # Skip empty lines and position metadata
    if not line or line.startswith('align:') or line.startswith('position:'):
        continue
    # Remove inline timestamps
    line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', line)
    # Remove HTML tags
    line = re.sub(r'<[^>]+>', '', line)
    # Deduplicate
    if line not in seen:
        seen.add(line)
        lines.append(line)

text = ' '.join(lines)
# Clean up whitespace
text = re.sub(r'\s+', ' ', text).strip()

with open('$OUT_FILE', 'w') as f:
    f.write(text + '\n')
print(f'Transcript saved ({len(text)} chars)', file=sys.stderr)
" 2>&1

    rm -rf "$SUB_DIR"
    echo "$OUT_FILE"
    exit 0
  fi

  rm -rf "$SUB_DIR"
  echo ">>> No subtitles available. Falling back to Whisper API..." >&2
fi

# --- Step 2: Download audio ---
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY not set. Required for Whisper transcription." >&2
  exit 1
fi

AUDIO_RAW="/tmp/yt_audio_raw_${VIDEO_ID}"
AUDIO_COMPRESSED="/tmp/yt_audio_${VIDEO_ID}.m4a"

echo ">>> Downloading audio..." >&2
$YTDLP -x --audio-format m4a -o "$AUDIO_RAW" "$URL" 2>&1 | grep -E '^\[download\]|^\[ExtractAudio\]|ERROR' >&2 || true

# Find the actual downloaded file (extension may vary)
AUDIO_ACTUAL=$(ls ${AUDIO_RAW}.* 2>/dev/null | head -1 || true)
if [[ -z "$AUDIO_ACTUAL" || ! -s "$AUDIO_ACTUAL" ]]; then
  echo "Error: Failed to download audio" >&2
  exit 1
fi

# --- Step 3: Compress audio to fit 25MB API limit ---
AUDIO_SIZE=$(stat -f%z "$AUDIO_ACTUAL" 2>/dev/null || stat -c%s "$AUDIO_ACTUAL" 2>/dev/null)
MAX_SIZE=$((24 * 1024 * 1024))  # 24MB to be safe

if [[ "$AUDIO_SIZE" -gt "$MAX_SIZE" ]]; then
  echo ">>> Audio ${AUDIO_SIZE} bytes, compressing to mono ${AUDIO_BITRATE}kbps..." >&2
  $FFMPEG -i "$AUDIO_ACTUAL" -b:a "${AUDIO_BITRATE}k" -ac 1 "$AUDIO_COMPRESSED" -y 2>/dev/null
  WHISPER_INPUT="$AUDIO_COMPRESSED"
else
  WHISPER_INPUT="$AUDIO_ACTUAL"
fi

# Check compressed size, reduce bitrate if still too large
FINAL_SIZE=$(stat -f%z "$WHISPER_INPUT" 2>/dev/null || stat -c%s "$WHISPER_INPUT" 2>/dev/null)
if [[ "$FINAL_SIZE" -gt "$MAX_SIZE" ]]; then
  echo ">>> Still too large, compressing to 32kbps..." >&2
  $FFMPEG -i "$AUDIO_ACTUAL" -b:a 32k -ac 1 "${AUDIO_COMPRESSED}.low.m4a" -y 2>/dev/null
  WHISPER_INPUT="${AUDIO_COMPRESSED}.low.m4a"
fi

# --- Step 4: Transcribe via Whisper API ---
echo ">>> Transcribing via OpenAI Whisper API..." >&2

CURL_ARGS=(
  -s
  -X POST
  "https://api.openai.com/v1/audio/transcriptions"
  -H "Authorization: Bearer ${OPENAI_API_KEY}"
  -F "file=@${WHISPER_INPUT}"
  -F "model=whisper-1"
  -F "response_format=text"
)

if [[ -n "$LANG_CODE" ]]; then
  CURL_ARGS+=(-F "language=${LANG_CODE}")
fi

RESULT=$(curl "${CURL_ARGS[@]}")

# Check for API errors
if echo "$RESULT" | grep -q '"error"'; then
  echo "Error: Whisper API failed:" >&2
  echo "$RESULT" >&2
  exit 1
fi

# Save transcript
echo "$RESULT" > "$OUT_FILE"
CHAR_COUNT=${#RESULT}
echo ">>> Transcript saved (${CHAR_COUNT} chars)" >&2

# --- Cleanup ---
if [[ "$KEEP_AUDIO" == false ]]; then
  rm -f "$AUDIO_RAW" "$AUDIO_ACTUAL" "$AUDIO_COMPRESSED" "${AUDIO_COMPRESSED}.low.m4a" 2>/dev/null
else
  echo ">>> Audio kept at: ${WHISPER_INPUT}" >&2
fi

echo "$OUT_FILE"
