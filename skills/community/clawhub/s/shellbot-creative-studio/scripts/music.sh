#!/usr/bin/env bash
# shellbot-creative-studio — music generation
# Usage: music --prompt "..." --duration <10-240> [--provider freepik|elevenlabs] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

PROMPT=""
DURATION=""
PROVIDER=""
OUTPUT=""
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: music --prompt "..." --duration <seconds> [options]

Options:
  --prompt    Music description (required)
  --duration  Length in seconds: 10-240 (required)
  --provider  Force provider: freepik, elevenlabs
  --output    Output file path (.mp3)
  --dry-run   Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)   PROMPT="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --output)   OUTPUT="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=true; shift ;;
    -h|--help)  usage; exit 0 ;;
    *)          log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$PROMPT" ]]; then log_error "--prompt is required"; usage; exit 1; fi
if [[ -z "$DURATION" ]]; then log_error "--duration is required"; usage; exit 1; fi

SELECTED=$(select_provider music ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}"

# ─── Freepik ─────────────────────────────────────────────────────────────────
generate_freepik_music() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  local payload
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --argjson duration "$DURATION" \
    '{prompt: $prompt, music_length_seconds: $duration}')

  local endpoint="https://api.freepik.com/v1/ai/music-generation"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model=music-generation dry_run=true)"
    return
  fi

  log_info "Generating music via Freepik..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local task_id
  task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty')

  if [[ -n "$task_id" ]]; then
    log_task "$task_id" "freepik" "music" "pending" "${OUTPUT:-}"
    local result
    result=$(poll_task freepik "$task_id")
    local audio_url
    audio_url=$(echo "$result" | jq -r '.data.audio.url // .data.audio_url // .data[0].url // empty')
  else
    local audio_url
    audio_url=$(echo "$response" | jq -r '.data.audio.url // .data.audio_url // .data[0].url // empty')
  fi

  local audio_json="{\"url\":\"${audio_url}\"}"
  if [[ -n "$OUTPUT" && -n "$audio_url" ]]; then
    download_to "$audio_url" "$OUTPUT" >/dev/null
    audio_json="{\"url\":\"${audio_url}\",\"local_path\":\"${OUTPUT}\"}"
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model=music-generation audio="$audio_json")"
}

# ─── ElevenLabs Direct ───────────────────────────────────────────────────────
generate_elevenlabs_music() {
  require_provider_key elevenlabs
  local api_key
  api_key=$(get_provider_key elevenlabs)

  local endpoint="https://api.elevenlabs.io/v1/music"

  local payload
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --argjson duration "$DURATION" \
    '{prompt: $prompt, duration_seconds: $duration}')

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model=elevenlabs-music dry_run=true)"
    return
  fi

  log_info "Generating music via ElevenLabs..."

  local output_file="${OUTPUT:-$(mktemp /tmp/creative-music-XXXX.mp3)}"
  mkdir -p "$(dirname "$output_file")"

  curl -sf -X POST "$endpoint" \
    -H "xi-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    -o "$output_file"

  log_ok "Music saved to ${output_file}"
  json_output "$(json_build status=completed provider="$SELECTED" model=elevenlabs-music audio="{\"local_path\":\"${output_file}\"}")"
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  freepik)    generate_freepik_music ;;
  elevenlabs) generate_elevenlabs_music ;;
  *)          json_error "Unsupported provider for music: ${SELECTED}" ;;
esac
