#!/bin/bash
# download_audio.sh - Download audio from a YouTube URL using yt-dlp
# Usage: bash download_audio.sh <URL> [output_dir] [cookies_file]
# Output: Prints the downloaded file path to stdout on success
# Exit codes: 0=success, 1=bad args, 2=yt-dlp not found, 3=download failed

set -euo pipefail

URL="${1:-}"
OUT_DIR="${2:-/tmp/yt-audio}"
COOKIES="${3:-}"

if [[ -z "$URL" ]]; then
  echo "ERROR: No URL provided." >&2
  echo "Usage: $0 <youtube_url> [output_dir] [cookies_file]" >&2
  exit 1
fi

# Find yt-dlp: prefer /tmp/yt-dlp (latest) > PATH > venv
if [[ -x "/tmp/yt-dlp" ]]; then
  YT_DLP="/tmp/yt-dlp"
elif command -v yt-dlp &>/dev/null; then
  YT_DLP="$(command -v yt-dlp)"
elif [[ -x "/app/.venv/bin/yt-dlp" ]]; then
  YT_DLP="/app/.venv/bin/yt-dlp"
else
  echo "ERROR: yt-dlp not found. Install with:" >&2
  echo "  curl -sL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /tmp/yt-dlp && chmod +x /tmp/yt-dlp" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"

# Build cookie args
COOKIE_ARGS=()
if [[ -n "$COOKIES" && -f "$COOKIES" ]]; then
  COOKIE_ARGS=(--cookies "$COOKIES")
elif [[ -n "$COOKIES" && "$COOKIES" == browser:* ]]; then
  # e.g. COOKIES="browser:chrome"
  BROWSER="${COOKIES#browser:}"
  COOKIE_ARGS=(--cookies-from-browser "$BROWSER")
fi

# Download best audio, convert to mp3, print file path
"$YT_DLP" \
  -x \
  --audio-format mp3 \
  --audio-quality 0 \
  -o "$OUT_DIR/%(title)s.%(ext)s" \
  --print after_move:filepath \
  --no-playlist \
  "${COOKIE_ARGS[@]+"${COOKIE_ARGS[@]}"}" \
  "$URL" || {
    echo "ERROR: Download failed. If YouTube blocks the request, try:" >&2
    echo "  1. Export cookies: yt-dlp --cookies-from-browser chrome ..." >&2
    echo "  2. Use a cookies.txt file as the 3rd argument" >&2
    exit 3
  }
