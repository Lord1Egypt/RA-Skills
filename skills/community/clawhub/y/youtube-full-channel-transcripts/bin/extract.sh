#!/usr/bin/env bash
set -euo pipefail

# Ensure user-installed binaries are available
export PATH="$HOME/bin:$PATH"

# YouTube Full Channel Transcripts Extractor
# Free, local alternative to Apify actor

# Defaults
OUTPUT_FORMAT="${output_format:-json}"
MAX_VIDEOS="${max_videos:-}"
LANGUAGES="${languages:-en}"
INCLUDE_AUTO_GENERATED="${include_auto_generated:-true}"
OUTPUT_DIR="${output_dir:-$(pwd)/exports/youtube-transcripts}"

CHANNEL_URL="${channel_url:?Channel URL is required}"

# Create output dir
mkdir -p "$OUTPUT_DIR"

# Step 1: Get all videos from channel/playlist (with Node.js runtime for yt-dlp)
echo "Fetching video list from: $CHANNEL_URL"
if [[ -n "$MAX_VIDEOS" ]]; then
  PLAYLIST_OPTS="--playlist-end $MAX_VIDEOS"
else
  PLAYLIST_OPTS=""
fi

yt-dlp --flat-playlist -J --js-runtimes node "$CHANNEL_URL" $PLAYLIST_OPTS > /tmp/playlist.json || {
  echo "Error: Failed to fetch playlist/channel info"
  exit 1
}

# Normalize to entries array (handle single-video case)
if jq -e '.entries' /tmp/playlist.json >/dev/null 2>&1; then
  ENTRIES_JSON=$(jq '.entries' /tmp/playlist.json)
else
  # Single video: root is the video object, wrap in array
  ENTRIES_JSON="[$(cat /tmp/playlist.json)]"
fi

TOTAL_VIDEOS=$(echo "$ENTRIES_JSON" | jq 'length')
echo "Found $TOTAL_VIDEOS videos"

# Prepare output file
OUTPUT_FILE="$OUTPUT_DIR/transcripts.$OUTPUT_FORMAT"
> "$OUTPUT_FILE"  # clear

SUCCESS_COUNT=0
FAIL_COUNT=0

# Step 2: Loop through videos (use process substitution to avoid subshell)
while IFS= read -r video; do
  VIDEO_ID=$(echo "$video" | jq -r '.id')
  VIDEO_URL="https://www.youtube.com/watch?v=$VIDEO_ID"
  TITLE=$(echo "$video" | jq -r '.title')
  UPLOAD_DATE=$(echo "$video" | jq -r '.upload_date // ""')
  DURATION=$(echo "$video" | jq -r '.duration // 0')

  echo "Processing: [$VIDEO_ID] $TITLE"

  # Fetch transcript subtitles
  # Fetch transcript subtitles
  # Use a temp base name; yt-dlp may add language code or .auto
  SUBTITLE_BASE="/tmp/$VIDEO_ID"
  if [[ "$INCLUDE_AUTO_GENERATED" == "true" ]]; then
    # Include auto-generated subtitles
    if ! yt-dlp --write-subs --sub-format srt --skip-download --sub-lang "$LANGUAGES" --js-runtimes node -o "$SUBTITLE_BASE" "$VIDEO_URL" 2>/dev/null; then
      echo "  [SKIP] No transcript available"
      FAIL_COUNT=$((FAIL_COUNT+1))
      continue
    fi
  else
    # Only manual subtitles
    if ! yt-dlp --write-subs --sub-format srt --skip-download --sub-lang "$LANGUAGES" --no-auto-subs --js-runtimes node -o "$SUBTITLE_BASE" "$VIDEO_URL" 2>/dev/null; then
      echo "  [SKIP] No manual transcript available"
      FAIL_COUNT=$((FAIL_COUNT+1))
      continue
    fi
  fi

  # Find the subtitle file that was created (may have language code or .auto)
  SUBTITLE_FILE=$(ls /tmp/$VIDEO_ID*.srt 2>/dev/null | head -n1)
  if [[ -z "$SUBTITLE_FILE" || ! -s "$SUBTITLE_FILE" ]]; then
    echo "  [SKIP] Subtitle file empty or not created"
    ((FAIL_COUNT++))
    continue
  fi

  # Convert SRT to plain text
  TRANSCRIPT=$(sed '/^\s*$/d' "$SUBTITLE_FILE" | sed -E 's/^[0-9]+$//; s/^[0-9]+:[0-9]+:[0-9]+,[0-9]+ --> [0-9]+:[0-9]+:[0-9]+,[0-9]+$//' | sed '/^\s*$/d' | tr '\n' ' ' | sed 's/  */ /g')

  # Detect auto-generated from filename (contains .auto) or language wildcard
  IS_AUTO=false
  if [[ "$LANGUAGES" == "*" ]] || [[ "$SUBTITLE_FILE" == *.auto.* ]]; then
    IS_AUTO=true
  fi

  # Build record
  case "$OUTPUT_FORMAT" in
    json)
      RECORD=$(jq -n -c \
        --arg vid "$VIDEO_ID" \
        --arg title "$TITLE" \
        --arg url "$VIDEO_URL" \
        --arg date "$UPLOAD_DATE" \
        --arg duration "$DURATION" \
        --arg transcript "$TRANSCRIPT" \
        --argjson auto "$IS_AUTO" \
        '{video_id: $vid, title: $title, url: $url, upload_date: $date, duration: ($duration|tonumber), transcript: $transcript, is_auto_generated: $auto}')
      echo "$RECORD" >> "$OUTPUT_FILE"
      ;;
    csv)
      if [[ ! -s "$OUTPUT_FILE" ]]; then
        echo "video_id,title,url,upload_date,duration,transcript,is_auto_generated" > "$OUTPUT_FILE"
      fi
      ESCAPED_TRANSCRIPT=$(echo "$TRANSCRIPT" | sed 's/"/""/g')
      echo "\"$VIDEO_ID\",\"$TITLE\",\"$VIDEO_URL\",\"$UPLOAD_DATE\",$DURATION,\"$ESCAPED_TRANSCRIPT\",$IS_AUTO" >> "$OUTPUT_FILE"
      ;;
  esac

  SUCCESS_COUNT=$((SUCCESS_COUNT+1))
  rm -f "$SUBTITLE_FILE" "${SUBTITLE_FILE}.auto" 2>/dev/null || true
done < <(echo "$ENTRIES_JSON" | jq -c '.[]')

# Summary
echo "========================================"
echo "Completed: $SUCCESS_COUNT videos extracted, $FAIL_COUNT failed/skipped"
echo "Output saved to: $OUTPUT_FILE"
