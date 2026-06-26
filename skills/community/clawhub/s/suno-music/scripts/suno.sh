#!/usr/bin/env bash
# Suno API wrapper — calls local gcui-art/suno-api on localhost:3100
set -euo pipefail

BASE="${SUNO_API_URL:-http://localhost:3100}"
DOWNLOAD_DIR="${SUNO_DOWNLOAD_DIR:-/tmp/suno-downloads}"
mkdir -p "$DOWNLOAD_DIR"

usage() {
  cat <<EOF
Usage: suno.sh <command> [options]

Commands:
  generate    Simple generation (Suno writes lyrics from description)
  custom      Full control (your lyrics, style tags, title)
  lyrics      Generate lyrics from a theme (review before generating)
  status      Check generation status by IDs
  credits     Check remaining credits
  download    Download audio file from URL

Options:
  --prompt TEXT       Song description or lyrics
  --style TEXT        Genre/style tags (custom mode)
  --title TEXT        Song title (custom mode)
  --instrumental      Generate instrumental only (no vocals)
  --wait              Wait for audio to be ready (blocks ~60-120s)
  --ids ID1,ID2       Comma-separated song IDs (status command)
  --url URL           Audio URL to download
  --out PATH          Output path for download
EOF
  exit 1
}

check_server() {
  if ! curl -sf "$BASE" >/dev/null 2>&1; then
    echo '{"error": "Suno API server not running on localhost:3100. Start the suno-api server first (see setup instructions)."}' >&2
    exit 1
  fi
}

cmd_generate() {
  local prompt="" instrumental=false wait_audio=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --prompt) prompt="$2"; shift 2 ;;
      --instrumental) instrumental=true; shift ;;
      --wait) wait_audio=true; shift ;;
      *) shift ;;
    esac
  done
  [[ -z "$prompt" ]] && { echo '{"error": "Missing --prompt"}'; exit 1; }
  check_server

  curl -sf -X POST "$BASE/api/generate" \
    -H 'Content-Type: application/json' \
    -d "$(jq -n \
      --arg prompt "$prompt" \
      --argjson instrumental "$instrumental" \
      --argjson wait "$wait_audio" \
      '{prompt: $prompt, make_instrumental: $instrumental, wait_audio: $wait}')" \
    2>&1
}

cmd_custom() {
  local prompt="" style="" title="" instrumental=false wait_audio=false negative_tags=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --prompt) prompt="$2"; shift 2 ;;
      --style) style="$2"; shift 2 ;;
      --title) title="$2"; shift 2 ;;
      --negative-tags) negative_tags="$2"; shift 2 ;;
      --instrumental) instrumental=true; shift ;;
      --wait) wait_audio=true; shift ;;
      *) shift ;;
    esac
  done
  [[ -z "$prompt" ]] && { echo '{"error": "Missing --prompt (lyrics)"}'; exit 1; }
  [[ -z "$style" ]] && { echo '{"error": "Missing --style (genre tags)"}'; exit 1; }
  [[ -z "$title" ]] && { echo '{"error": "Missing --title"}'; exit 1; }
  check_server

  local json
  json=$(jq -n \
    --arg prompt "$prompt" \
    --arg tags "$style" \
    --arg title "$title" \
    --arg neg "$negative_tags" \
    --argjson instrumental "$instrumental" \
    --argjson wait "$wait_audio" \
    '{prompt: $prompt, tags: $tags, title: $title, make_instrumental: $instrumental, wait_audio: $wait, negative_tags: $neg}')

  curl -sf -X POST "$BASE/api/custom_generate" \
    -H 'Content-Type: application/json' \
    -d "$json" 2>&1
}

cmd_lyrics() {
  local prompt=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --prompt) prompt="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  [[ -z "$prompt" ]] && { echo '{"error": "Missing --prompt (theme)"}'; exit 1; }
  check_server

  curl -sf -X POST "$BASE/api/generate_lyrics" \
    -H 'Content-Type: application/json' \
    -d "$(jq -n --arg prompt "$prompt" '{prompt: $prompt}')" 2>&1
}

cmd_status() {
  local ids=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --ids) ids="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  [[ -z "$ids" ]] && { echo '{"error": "Missing --ids"}'; exit 1; }
  check_server

  curl -sf "$BASE/api/get?ids=$ids" 2>&1
}

cmd_credits() {
  check_server
  curl -sf "$BASE/api/get_limit" 2>&1
}

cmd_download() {
  local url="" out=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --url) url="$2"; shift 2 ;;
      --out) out="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  [[ -z "$url" ]] && { echo '{"error": "Missing --url"}'; exit 1; }

  if [[ -z "$out" ]]; then
    local filename
    filename="suno-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4).mp3"
    out="$DOWNLOAD_DIR/$filename"
  fi

  curl -sfL "$url" -o "$out" 2>&1
  echo "{\"downloaded\": \"$out\"}"
}

# Main dispatch
[[ $# -lt 1 ]] && usage
cmd="$1"; shift
case "$cmd" in
  generate) cmd_generate "$@" ;;
  custom) cmd_custom "$@" ;;
  lyrics) cmd_lyrics "$@" ;;
  status) cmd_status "$@" ;;
  credits) cmd_credits "$@" ;;
  download) cmd_download "$@" ;;
  *) usage ;;
esac
