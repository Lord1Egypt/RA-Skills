#!/usr/bin/env bash
# Upload a local file to ZOOOP storage and print the resulting public URL.
# Used to convert "user has a file on disk" into "AI task input URL".
#
# Image / audio resolve in a single POST (sync, < 1s typical).
# Video resolves async — this script polls the moderation workflow until
# terminal, then prints the URL (or exits non-zero on block / error).
#
# Usage: upload.sh <path-to-file>
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <path-to-file>" >&2
  exit 64
fi

FILE="$1"
if [[ ! -f "$FILE" ]]; then
  echo "no such file: $FILE" >&2
  exit 66
fi

# Derive content-type from extension. macOS's bash 3.2 doesn't support `${var,,}`
# so we lowercase via `tr`. Override with ZOOOP_CONTENT_TYPE for off-ext files.
EXT="${FILE##*.}"
EXT=$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')
case "$EXT" in
  jpg|jpeg) CT="image/jpeg" ;;
  png)      CT="image/png" ;;
  webp)     CT="image/webp" ;;
  gif)      CT="image/gif" ;;
  mp3)      CT="audio/mpeg" ;;
  wav)      CT="audio/wav" ;;
  ogg)      CT="audio/ogg" ;;
  webm)     CT="video/webm" ;;
  mp4)      CT="video/mp4" ;;
  mov)      CT="video/quicktime" ;;
  *)        CT="${ZOOOP_CONTENT_TYPE:-application/octet-stream}" ;;
esac

# jq-free string field extraction — naive but works for the flat shapes we get.
extract_field() {
  local field="$1"; local json="$2"
  printf '%s' "$json" | grep -oE "\"$field\":\"[^\"]+\"" | head -1 | sed "s/^\"$field\":\"//; s/\"\$//"
}

# Single-shot raw-body upload. The server streams the bytes straight into R2
# `_pending/` then dispatches the moderation path appropriate to the mime.
RESP=$(curl -fsS -X POST "$HOST/v1/uploads" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: $CT" \
  --data-binary "@$FILE")

STATUS=$(extract_field "status" "$RESP")

case "$STATUS" in
  ready)
    URL=$(extract_field "url" "$RESP")
    if [[ -z "$URL" ]]; then
      echo "upload returned 'ready' but no url:" >&2
      printf '%s\n' "$RESP" >&2
      exit 1
    fi
    printf '%s\n' "$URL"
    ;;
  processing)
    # Video — poll the moderation workflow until terminal. The 30-min ceiling
    # matches the server-side workflow's POLL_DEADLINE_MS.
    UPLOAD_ID=$(extract_field "uploadId" "$RESP")
    if [[ -z "$UPLOAD_ID" ]]; then
      echo "upload returned 'processing' but no uploadId:" >&2
      printf '%s\n' "$RESP" >&2
      exit 1
    fi
    START=$(date +%s)
    DEADLINE=$((START + 1800))
    SLEEPS="5 10 20"
    while true; do
      for s in $SLEEPS 20; do
        sleep "$s"
        POLL=$(curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
          "$HOST/v1/uploads/$UPLOAD_ID")
        PSTATUS=$(extract_field "status" "$POLL")
        case "$PSTATUS" in
          processing) ;;
          ready)
            URL=$(extract_field "url" "$POLL")
            printf '%s\n' "$URL"
            exit 0
            ;;
          blocked)
            echo "upload blocked by content moderation" >&2
            printf '%s\n' "$POLL" >&2
            exit 1
            ;;
          errored|*)
            echo "upload errored:" >&2
            printf '%s\n' "$POLL" >&2
            exit 1
            ;;
        esac
        NOW=$(date +%s)
        if [[ "$NOW" -ge "$DEADLINE" ]]; then
          echo "upload polling timed out after 30 min" >&2
          exit 1
        fi
      done
    done
    ;;
  *)
    echo "unexpected upload response:" >&2
    printf '%s\n' "$RESP" >&2
    exit 1
    ;;
esac
