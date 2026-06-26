#!/usr/bin/env bash
# shellbot-creative-studio — video generation
# Usage: video --prompt "..." [--image <url>] [--duration 5|10] [--aspect 16:9|9:16|1:1]
#              [--provider freepik|fal] [--model kling-v3-omni-pro|...] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

PROMPT=""
IMAGE=""
DURATION=5
ASPECT="16:9"
PROVIDER=""
MODEL=""
OUTPUT=""
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: video --prompt "..." [options]

Options:
  --prompt    Text prompt (required)
  --image     Input image URL for image-to-video
  --duration  Duration in seconds: 3-15 (default: 5)
  --aspect    Aspect ratio: 16:9, 9:16, 1:1 (default: 16:9)
  --provider  Force provider: freepik, fal
  --model     Force model (e.g., kling-v3-omni-pro, kling-v3-pro, runway-4-5)
  --output    Output file path
  --dry-run   Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)   PROMPT="$2"; shift 2 ;;
    --image)    IMAGE="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --aspect)   ASPECT="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --model)    MODEL="$2"; shift 2 ;;
    --output)   OUTPUT="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=true; shift ;;
    -h|--help)  usage; exit 0 ;;
    *)          log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  log_error "--prompt is required"
  usage
  exit 1
fi

SELECTED=$(select_provider video ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}"

if [[ -z "$MODEL" ]]; then
  MODEL=$(get_default_model "$SELECTED" video)
fi
log_info "Model: ${MODEL}"

# ─── Freepik ─────────────────────────────────────────────────────────────────
generate_freepik_video() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  # Determine endpoint
  local endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni-pro"
  local poll_endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni"
  case "$MODEL" in
    kling-v3-omni-pro)
      endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni-pro"
      poll_endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni"
      ;;
    kling-v3-pro)
      endpoint="https://api.freepik.com/v1/ai/video/kling-v3-pro"
      poll_endpoint="https://api.freepik.com/v1/ai/video/kling-v3-pro"
      ;;
    runway-4-5)
      if [[ -n "$IMAGE" ]]; then
        endpoint="https://api.freepik.com/v1/ai/image-to-video/runway-4-5"
      else
        endpoint="https://api.freepik.com/v1/ai/text-to-video/runway-4-5"
      fi
      poll_endpoint="$endpoint"
      ;;
    wan-v2-6)
      endpoint="https://api.freepik.com/v1/ai/text-to-video/wan-v2-6-1080p"
      poll_endpoint="$endpoint"
      ;;
    *)
      endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni-pro"
      poll_endpoint="https://api.freepik.com/v1/ai/video/kling-v3-omni"
      ;;
  esac

  local payload
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --arg aspect "$ASPECT" \
    --argjson duration "$DURATION" \
    '{prompt: $prompt, aspect_ratio: $aspect, duration: $duration}')

  if [[ -n "$IMAGE" ]]; then
    payload=$(echo "$payload" | jq --arg img "$IMAGE" '. + {image_url: $img}')
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model="$MODEL" dry_run=true)"
    return
  fi

  log_info "Generating video with Freepik ${MODEL}..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local task_id
  task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty')

  if [[ -z "$task_id" ]]; then
    log_error "No task_id in response"
    json_error "Failed to submit video generation"
  fi

  log_task "$task_id" "freepik" "video" "pending" "${OUTPUT:-}"
  log_info "Task submitted: ${task_id}"

  # Poll for completion
  local elapsed=0
  local max_wait=600
  local interval=5

  while [[ $elapsed -lt $max_wait ]]; do
    local status_response
    status_response=$(curl -sf "${poll_endpoint}/${task_id}" \
      -H "x-freepik-api-key: ${api_key}" 2>/dev/null) || true

    if [[ -z "$status_response" ]]; then
      sleep "$interval"
      elapsed=$((elapsed + interval))
      continue
    fi

    local status
    status=$(echo "$status_response" | jq -r '.data.status // .status // "unknown"')

    case "$status" in
      COMPLETED|completed)
        log_ok "Video completed"
        local video_url
        video_url=$(echo "$status_response" | jq -r '.data.video.url // .data.videos[0].url // empty')

        local video_json="{\"url\":\"${video_url}\"}"

        if [[ -n "$OUTPUT" && -n "$video_url" ]]; then
          download_to "$video_url" "$OUTPUT" >/dev/null
          video_json="{\"url\":\"${video_url}\",\"local_path\":\"${OUTPUT}\"}"
        fi

        log_task "$task_id" "freepik" "video" "completed" "${OUTPUT:-}"
        json_output "$(json_build status=completed provider="$SELECTED" model="$MODEL" task_id="$task_id" video="$video_json")"
        return
        ;;
      FAILED|failed)
        log_error "Video generation failed"
        log_task "$task_id" "freepik" "video" "failed" ""
        json_error "Video generation failed: $(echo "$status_response" | jq -r '.data.error // .error // "unknown"')"
        ;;
      *)
        log_info "Status: ${status} — ${elapsed}s elapsed"
        ;;
    esac

    sleep "$interval"
    elapsed=$((elapsed + interval))
  done

  json_error "Video generation timed out after ${max_wait}s. Task ID: ${task_id}"
}

# ─── fal.ai ──────────────────────────────────────────────────────────────────
generate_fal_video() {
  require_provider_key fal
  local api_key
  api_key=$(get_provider_key fal)

  local model_id="fal-ai/kling-video/v2/image-to-video"
  case "$MODEL" in
    fal-ai/*) model_id="$MODEL" ;;
    *)        model_id="fal-ai/kling-video/v2/image-to-video" ;;
  esac

  local payload
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --argjson duration "$DURATION" \
    '{prompt: $prompt, duration: $duration}')

  if [[ -n "$IMAGE" ]]; then
    payload=$(echo "$payload" | jq --arg img "$IMAGE" '. + {image_url: $img}')
  fi

  local endpoint="https://queue.fal.run/${model_id}"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model="$model_id" dry_run=true)"
    return
  fi

  log_info "Generating video with fal ${model_id}..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "Authorization: Key ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local request_id
  request_id=$(echo "$response" | jq -r '.request_id // empty')

  if [[ -z "$request_id" ]]; then
    json_error "Failed to submit video generation to fal"
  fi

  log_task "$request_id" "fal" "video" "pending" "${OUTPUT:-}"
  log_info "Request submitted: ${request_id}"

  local result
  result=$(poll_task fal "$request_id" "$endpoint" --max-wait 600 --interval 5)

  local video_url
  video_url=$(echo "$result" | jq -r '.video.url // .videos[0].url // empty')

  local video_json="{\"url\":\"${video_url}\"}"

  if [[ -n "$OUTPUT" && -n "$video_url" ]]; then
    download_to "$video_url" "$OUTPUT" >/dev/null
    video_json="{\"url\":\"${video_url}\",\"local_path\":\"${OUTPUT}\"}"
  fi

  log_task "$request_id" "fal" "video" "completed" "${OUTPUT:-}"
  json_output "$(json_build status=completed provider="$SELECTED" model="$model_id" task_id="$request_id" video="$video_json")"
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  freepik) generate_freepik_video ;;
  fal)     generate_fal_video ;;
  *)       json_error "Unsupported provider for video: ${SELECTED}" ;;
esac
