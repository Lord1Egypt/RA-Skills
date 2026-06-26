#!/usr/bin/env bash
# shellbot-creative-studio — sound effects generation
# Usage: sfx --prompt "..." --duration <0.5-22> [--loop] [--provider freepik|elevenlabs] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

PROMPT=""
DURATION=""
LOOP=false
INFLUENCE=0.3
PROVIDER=""
OUTPUT=""
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: sfx --prompt "..." --duration <seconds> [options]

Options:
  --prompt     Sound description (required)
  --duration   Length in seconds: 0.5-22 (required)
  --loop       Make the sound loop-friendly
  --influence  Prompt influence: 0-1 (default: 0.3)
  --provider   Force provider: freepik, elevenlabs
  --output     Output file path (.mp3)
  --dry-run    Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)    PROMPT="$2"; shift 2 ;;
    --duration)  DURATION="$2"; shift 2 ;;
    --loop)      LOOP=true; shift ;;
    --influence) INFLUENCE="$2"; shift 2 ;;
    --provider)  PROVIDER="$2"; shift 2 ;;
    --output)    OUTPUT="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=true; shift ;;
    -h|--help)   usage; exit 0 ;;
    *)           log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$PROMPT" ]]; then log_error "--prompt is required"; usage; exit 1; fi
if [[ -z "$DURATION" ]]; then log_error "--duration is required"; usage; exit 1; fi

SELECTED=$(select_provider sfx ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}"

# ─── Freepik ─────────────────────────────────────────────────────────────────
generate_freepik_sfx() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  local payload
  payload=$(jq -n \
    --arg text "$PROMPT" \
    --argjson duration "$DURATION" \
    --argjson loop "$LOOP" \
    --argjson influence "$INFLUENCE" \
    '{text: $text, duration_seconds: $duration, loop: $loop, prompt_influence: $influence}')

  local endpoint="https://api.freepik.com/v1/ai/sound-effects"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model=sound-effects dry_run=true)"
    return
  fi

  log_info "Generating sound effect via Freepik..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local task_id
  task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty')

  if [[ -n "$task_id" ]]; then
    log_task "$task_id" "freepik" "sfx" "pending" "${OUTPUT:-}"
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

  json_output "$(json_build status=completed provider="$SELECTED" model=sound-effects audio="$audio_json")"
}

# ─── ElevenLabs Direct ───────────────────────────────────────────────────────
generate_elevenlabs_sfx() {
  require_provider_key elevenlabs
  local api_key
  api_key=$(get_provider_key elevenlabs)

  local endpoint="https://api.elevenlabs.io/v1/sound-generation"

  local payload
  payload=$(jq -n \
    --arg text "$PROMPT" \
    --argjson duration "$DURATION" \
    --argjson influence "$INFLUENCE" \
    '{text: $text, duration_seconds: $duration, prompt_influence: $influence}')

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model=elevenlabs-sfx dry_run=true)"
    return
  fi

  log_info "Generating sound effect via ElevenLabs..."

  local output_file="${OUTPUT:-$(mktemp /tmp/creative-sfx-XXXX.mp3)}"
  mkdir -p "$(dirname "$output_file")"

  curl -sf -X POST "$endpoint" \
    -H "xi-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    -o "$output_file"

  log_ok "SFX saved to ${output_file}"
  json_output "$(json_build status=completed provider="$SELECTED" model=elevenlabs-sfx audio="{\"local_path\":\"${output_file}\"}")"
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  freepik)    generate_freepik_sfx ;;
  elevenlabs) generate_elevenlabs_sfx ;;
  *)          json_error "Unsupported provider for sfx: ${SELECTED}" ;;
esac
