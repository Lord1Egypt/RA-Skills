#!/usr/bin/env bash
# shellbot-creative-studio — image editing
# Usage: edit --input <url_or_path> --action <action> [--prompt "..."]
#             [--mask <url>] [--reference <url>] [--scale 2|4]
#             [--provider freepik|fal|nano-banana-2] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

INPUT=""
ACTION=""
PROMPT=""
MASK=""
REFERENCE=""
SCALE=4
PROVIDER=""
OUTPUT=""
DRY_RUN=false
# Outpaint margins
LEFT=0; RIGHT=0; TOP=0; BOTTOM=0

usage() {
  cat >&2 <<'EOF'
Usage: edit --input <url_or_path> --action <action> [options]

Actions:
  upscale         Enlarge image with AI enhancement
  remove-bg       Remove background (sync, instant)
  inpaint         Edit masked region with prompt
  outpaint        Expand canvas with AI fill
  style-transfer  Apply reference image style
  relight         Change lighting with prompt

Options:
  --input      Input image URL or path (required)
  --action     Edit action (required)
  --prompt     Text guidance for the edit
  --mask       Mask image URL (for inpaint)
  --reference  Reference image URL (for style-transfer)
  --scale      Upscale factor: 2-16 (default: 4, for upscale)
  --left       Outpaint left margin in px (default: 0)
  --right      Outpaint right margin in px (default: 0)
  --top        Outpaint top margin in px (default: 0)
  --bottom     Outpaint bottom margin in px (default: 0)
  --provider   Force provider: freepik, fal, nano-banana-2
  --output     Output file path
  --dry-run    Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)     INPUT="$2"; shift 2 ;;
    --action)    ACTION="$2"; shift 2 ;;
    --prompt)    PROMPT="$2"; shift 2 ;;
    --mask)      MASK="$2"; shift 2 ;;
    --reference) REFERENCE="$2"; shift 2 ;;
    --scale)     SCALE="$2"; shift 2 ;;
    --left)      LEFT="$2"; shift 2 ;;
    --right)     RIGHT="$2"; shift 2 ;;
    --top)       TOP="$2"; shift 2 ;;
    --bottom)    BOTTOM="$2"; shift 2 ;;
    --provider)  PROVIDER="$2"; shift 2 ;;
    --output)    OUTPUT="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=true; shift ;;
    -h|--help)   usage; exit 0 ;;
    *)           log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$INPUT" ]]; then log_error "--input is required"; usage; exit 1; fi
if [[ -z "$ACTION" ]]; then log_error "--action is required"; usage; exit 1; fi

SELECTED=$(select_provider edit ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}, Action: ${ACTION}"

# ─── Freepik Actions ────────────────────────────────────────────────────────
freepik_edit() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  local endpoint=""
  local payload=""
  local is_sync=false

  case "$ACTION" in
    upscale)
      endpoint="https://api.freepik.com/v1/ai/image-upscaler-precision-v2"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --argjson scale "$SCALE" \
        '{image: $image, scale_factor: $scale, sharpen: 7, smart_grain: 7, ultra_detail: 30, flavor: "photo"}')
      ;;

    remove-bg)
      endpoint="https://api.freepik.com/v1/ai/beta/remove-background"
      payload=$(jq -n --arg url "$INPUT" '{image_url: $url}')
      is_sync=true
      ;;

    inpaint)
      if [[ -z "$MASK" ]]; then
        log_error "--mask is required for inpaint action"
        exit 1
      fi
      endpoint="https://api.freepik.com/v1/ai/ideogram-image-edit"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --arg mask "$MASK" \
        --arg prompt "${PROMPT:-edit this area}" \
        '{image: $image, mask: $mask, prompt: $prompt, rendering_speed: "DEFAULT", magic_prompt: "AUTO", style_type: "REALISTIC"}')
      ;;

    outpaint)
      endpoint="https://api.freepik.com/v1/ai/image-expand/seedream-v4-5"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --arg prompt "${PROMPT:-extend naturally}" \
        --argjson left "$LEFT" \
        --argjson right "$RIGHT" \
        --argjson top "$TOP" \
        --argjson bottom "$BOTTOM" \
        '{image: $image, prompt: $prompt, left: $left, right: $right, top: $top, bottom: $bottom}')
      ;;

    style-transfer)
      if [[ -z "$REFERENCE" ]]; then
        log_error "--reference is required for style-transfer action"
        exit 1
      fi
      endpoint="https://api.freepik.com/v1/ai/image-style-transfer"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --arg ref "$REFERENCE" \
        --arg prompt "${PROMPT:-}" \
        '{image: $image, reference_image: $ref, prompt: $prompt}')
      ;;

    relight)
      endpoint="https://api.freepik.com/v1/ai/image-relight"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --arg prompt "${PROMPT:-natural lighting}" \
        '{image: $image, prompt: $prompt}')
      ;;

    *)
      json_error "Unknown action: ${ACTION}. Use: upscale, remove-bg, inpaint, outpaint, style-transfer, relight"
      ;;
  esac

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" action="$ACTION" dry_run=true)"
    return
  fi

  log_info "Editing with Freepik (${ACTION})..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  if [[ "$is_sync" == "true" ]]; then
    # Sync response (remove-bg)
    local result_url
    result_url=$(echo "$response" | jq -r '.data.high_resolution // .data[0].url // empty')

    local result_json="{\"url\":\"${result_url}\"}"
    if [[ -n "$OUTPUT" && -n "$result_url" ]]; then
      download_to "$result_url" "$OUTPUT" >/dev/null
      result_json="{\"url\":\"${result_url}\",\"local_path\":\"${OUTPUT}\"}"
    fi

    json_output "$(json_build status=completed provider="$SELECTED" action="$ACTION" result="$result_json")"
  else
    # Async response
    local task_id
    task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty')

    if [[ -n "$task_id" ]]; then
      log_task "$task_id" "freepik" "edit-${ACTION}" "pending" "${OUTPUT:-}"
      local result
      result=$(poll_task freepik "$task_id")
      local result_url
      result_url=$(echo "$result" | jq -r '.data.images[0].url // .data[0].url // .data.image.url // empty')
    else
      local result_url
      result_url=$(echo "$response" | jq -r '.data.images[0].url // .data[0].url // .data.image.url // empty')
    fi

    local result_json="{\"url\":\"${result_url}\"}"
    if [[ -n "$OUTPUT" && -n "$result_url" ]]; then
      download_to "$result_url" "$OUTPUT" >/dev/null
      result_json="{\"url\":\"${result_url}\",\"local_path\":\"${OUTPUT}\"}"
    fi

    json_output "$(json_build status=completed provider="$SELECTED" action="$ACTION" result="$result_json")"
  fi
}

# ─── fal.ai Actions ─────────────────────────────────────────────────────────
fal_edit() {
  require_provider_key fal
  local api_key
  api_key=$(get_provider_key fal)

  local model_id=""
  local payload=""

  case "$ACTION" in
    upscale)
      model_id="fal-ai/creative-upscaler"
      payload=$(jq -n \
        --arg image "$INPUT" \
        --argjson scale "$SCALE" \
        --arg prompt "${PROMPT:-high quality, sharp details}" \
        '{image_url: $image, scale: $scale, prompt: $prompt}')
      ;;
    *)
      json_error "Action '${ACTION}' not supported on fal. Use freepik instead."
      ;;
  esac

  local endpoint="https://queue.fal.run/${model_id}"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" action="$ACTION" dry_run=true)"
    return
  fi

  log_info "Editing with fal (${ACTION})..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "Authorization: Key ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local request_id
  request_id=$(echo "$response" | jq -r '.request_id // empty')

  if [[ -n "$request_id" ]]; then
    log_task "$request_id" "fal" "edit-${ACTION}" "pending" "${OUTPUT:-}"
    local result
    result=$(poll_task fal "$request_id" "$endpoint")
    local result_url
    result_url=$(echo "$result" | jq -r '.image.url // .images[0].url // empty')
  else
    local result_url
    result_url=$(echo "$response" | jq -r '.image.url // .images[0].url // empty')
  fi

  local result_json="{\"url\":\"${result_url}\"}"
  if [[ -n "$OUTPUT" && -n "$result_url" ]]; then
    download_to "$result_url" "$OUTPUT" >/dev/null
    result_json="{\"url\":\"${result_url}\",\"local_path\":\"${OUTPUT}\"}"
  fi

  json_output "$(json_build status=completed provider="$SELECTED" action="$ACTION" result="$result_json")"
}

# ─── Nano Banana 2 Actions ──────────────────────────────────────────────────
nano_banana_edit() {
  case "$ACTION" in
    upscale|inpaint|outpaint|style-transfer)
      # Nano Banana supports instruction-based editing via images + prompt
      local input_json
      input_json=$(jq -n \
        --arg prompt "${PROMPT:-enhance and improve this image}" \
        --arg image "$INPUT" \
        '{prompt: $prompt, images: [$image]}')

      if [[ -n "$REFERENCE" ]]; then
        input_json=$(echo "$input_json" | jq --arg ref "$REFERENCE" '.images += [$ref]')
      fi

      if [[ "$DRY_RUN" == "true" ]]; then
        json_output "$(json_build command="infsh app run google/gemini-3-1-flash-image-preview --input '...'" provider="$SELECTED" action="$ACTION" dry_run=true)"
        return
      fi

      log_info "Editing with Nano Banana 2 (${ACTION})..."
      local result
      result=$(infsh app run google/gemini-3-1-flash-image-preview --input "$input_json" 2>/dev/null)

      local images
      images=$(echo "$result" | jq '[.images[]? // .output.images[]? | {url: .}]' 2>/dev/null || echo "[]")

      if [[ -n "$OUTPUT" ]]; then
        local first_url
        first_url=$(echo "$images" | jq -r '.[0].url // empty')
        if [[ -n "$first_url" ]]; then
          download_to "$first_url" "$OUTPUT" >/dev/null
          images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
        fi
      fi

      json_output "$(json_build status=completed provider="$SELECTED" action="$ACTION" result="$(echo "$images" | jq '.[0]')")"
      ;;
    *)
      json_error "Action '${ACTION}' not supported on nano-banana-2. Use freepik instead."
      ;;
  esac
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  freepik)       freepik_edit ;;
  fal)           fal_edit ;;
  nano-banana-2) nano_banana_edit ;;
  *)             json_error "Unsupported provider for edit: ${SELECTED}" ;;
esac
