#!/usr/bin/env bash
# shellbot-creative-studio — text-to-speech
# Usage: voice --text "..." [--voice <voice_id>] [--speed 0.7-1.2]
#              [--language en|es|...] [--provider freepik|elevenlabs] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

TEXT=""
VOICE_ID="21m00Tcm4TlvDq8ikWAM"  # Rachel (default)
SPEED=1.0
STABILITY=0.5
SIMILARITY=0.2
PROVIDER=""
OUTPUT=""
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: voice --text "..." [options]

Options:
  --text        Text to speak (required)
  --voice       ElevenLabs voice ID (default: 21m00Tcm4TlvDq8ikWAM / Rachel)
  --speed       Speaking speed: 0.7-1.2 (default: 1.0)
  --stability   Voice stability: 0-1 (default: 0.5)
  --similarity  Similarity boost: 0-1 (default: 0.2)
  --provider    Force provider: freepik, elevenlabs
  --output      Output file path (.mp3)
  --dry-run     Show the command without executing

Common voice IDs:
  21m00Tcm4TlvDq8ikWAM  Rachel (female, narration)
  EXAVITQu4vr4xnSDxMaL  Bella (female, soft)
  ErXwobaYiN019PkySvjV   Antoni (male, deep)
  VR6AewLTigWG4xSOukaG   Arnold (male, confident)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)       TEXT="$2"; shift 2 ;;
    --voice)      VOICE_ID="$2"; shift 2 ;;
    --speed)      SPEED="$2"; shift 2 ;;
    --stability)  STABILITY="$2"; shift 2 ;;
    --similarity) SIMILARITY="$2"; shift 2 ;;
    --provider)   PROVIDER="$2"; shift 2 ;;
    --output)     OUTPUT="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=true; shift ;;
    -h|--help)    usage; exit 0 ;;
    *)            log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$TEXT" ]]; then
  log_error "--text is required"
  usage
  exit 1
fi

SELECTED=$(select_provider voice ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}"

# ─── Freepik (ElevenLabs) ───────────────────────────────────────────────────
generate_freepik_voice() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  local payload
  payload=$(jq -n \
    --arg text "$TEXT" \
    --arg voice "$VOICE_ID" \
    --argjson speed "$SPEED" \
    --argjson stability "$STABILITY" \
    --argjson similarity "$SIMILARITY" \
    '{text: $text, voice_id: $voice, speed: $speed, stability: $stability, similarity_boost: $similarity}')

  local endpoint="https://api.freepik.com/v1/ai/voiceover/elevenlabs-turbo-v2-5"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model="elevenlabs-turbo-v2-5" dry_run=true)"
    return
  fi

  log_info "Generating voiceover via Freepik ElevenLabs..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  # Check for task_id (async) or direct audio URL
  local task_id
  task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty')

  local audio_url=""
  if [[ -n "$task_id" ]]; then
    log_task "$task_id" "freepik" "voice" "pending" "${OUTPUT:-}"
    local result
    result=$(poll_task freepik "$task_id")
    audio_url=$(echo "$result" | jq -r '.data.audio.url // .data.audio_url // empty')
  else
    audio_url=$(echo "$response" | jq -r '.data.audio.url // .data.audio_url // .data[0].url // empty')
  fi

  local audio_json="{\"url\":\"${audio_url}\"}"
  if [[ -n "$OUTPUT" && -n "$audio_url" ]]; then
    download_to "$audio_url" "$OUTPUT" >/dev/null
    audio_json="{\"url\":\"${audio_url}\",\"local_path\":\"${OUTPUT}\"}"
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model=elevenlabs-turbo-v2-5 audio="$audio_json")"
}

# ─── ElevenLabs Direct ───────────────────────────────────────────────────────
generate_elevenlabs_voice() {
  require_provider_key elevenlabs
  local api_key
  api_key=$(get_provider_key elevenlabs)

  local endpoint="https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}"

  local payload
  payload=$(jq -n \
    --arg text "$TEXT" \
    --arg model "eleven_turbo_v2_5" \
    --argjson stability "$STABILITY" \
    --argjson similarity "$SIMILARITY" \
    '{text: $text, model_id: $model, voice_settings: {stability: $stability, similarity_boost: $similarity}}')

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model="eleven_turbo_v2_5" dry_run=true)"
    return
  fi

  log_info "Generating voiceover via ElevenLabs direct..."

  local output_file="${OUTPUT:-$(mktemp /tmp/creative-voice-XXXX.mp3)}"
  mkdir -p "$(dirname "$output_file")"

  curl -sf -X POST "$endpoint" \
    -H "xi-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    -o "$output_file"

  log_ok "Audio saved to ${output_file}"
  json_output "$(json_build status=completed provider="$SELECTED" model=eleven_turbo_v2_5 audio="{\"local_path\":\"${output_file}\"}")"
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  freepik)    generate_freepik_voice ;;
  elevenlabs) generate_elevenlabs_voice ;;
  *)          json_error "Unsupported provider for voice: ${SELECTED}" ;;
esac
