#!/usr/bin/env bash
# shellbot-creative-studio — image generation
# Usage: image --prompt "..." [--style photo|digital_art|illustration] [--size 16:9|9:16|1:1|4:3]
#              [--resolution 1k|2k|4k] [--provider freepik|fal|nano-banana-2] [--model ...]
#              [--reference <url>] [--count 1-4] [--output <path>] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"
source "${SCRIPT_DIR}/lib/async_poll.sh"
source "${SCRIPT_DIR}/lib/task_log.sh"

# Defaults
PROMPT=""
STYLE="photo"
SIZE="16:9"
RESOLUTION="2k"
PROVIDER=""
MODEL=""
REFERENCE=""
COUNT=1
OUTPUT=""
DRY_RUN=false

usage() {
  cat >&2 <<'EOF'
Usage: image --prompt "..." [options]

Options:
  --prompt      Text prompt (required)
  --style       Style: photo, digital_art, illustration (default: photo)
  --size        Aspect ratio: 16:9, 9:16, 1:1, 4:3 (default: 16:9)
  --resolution  Resolution: 1k, 2k, 4k (default: 2k)
  --provider    Force provider: freepik, fal, nano-banana-2
  --model       Force model (e.g., mystic, flux-2, seedream-v4-5)
  --reference   Reference image URL for style/structure guidance
  --count       Number of images: 1-4 (default: 1)
  --output      Output file path (auto-generated if omitted)
  --dry-run     Show the command without executing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)     PROMPT="$2"; shift 2 ;;
    --style)      STYLE="$2"; shift 2 ;;
    --size)       SIZE="$2"; shift 2 ;;
    --resolution) RESOLUTION="$2"; shift 2 ;;
    --provider)   PROVIDER="$2"; shift 2 ;;
    --model)      MODEL="$2"; shift 2 ;;
    --reference)  REFERENCE="$2"; shift 2 ;;
    --count)      COUNT="$2"; shift 2 ;;
    --output)     OUTPUT="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=true; shift ;;
    -h|--help)    usage; exit 0 ;;
    *)            log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  log_error "--prompt is required"
  usage
  exit 1
fi

# Select provider
SELECTED=$(select_provider image ${PROVIDER:+--provider "$PROVIDER"})
log_info "Provider: ${SELECTED}"

# Resolve model
if [[ -z "$MODEL" ]]; then
  MODEL=$(get_default_model "$SELECTED" image)
fi
log_info "Model: ${MODEL}"

# ─── Nano Banana 2 ───────────────────────────────────────────────────────────
generate_nano_banana() {
  require_provider_key nano-banana-2
  local backend
  backend=$(get_nano_banana_backend)
  log_info "Nano Banana 2 backend: ${backend}"

  local input_json
  input_json=$(jq -n \
    --arg prompt "$PROMPT" \
    --arg aspect "$SIZE" \
    --arg res "$RESOLUTION" \
    --argjson count "$COUNT" \
    '{prompt: $prompt, aspect_ratio: $aspect, resolution: ($res | ascii_upcase), num_images: $count}')

  # Add reference images if provided
  if [[ -n "$REFERENCE" ]]; then
    input_json=$(echo "$input_json" | jq --arg ref "$REFERENCE" '. + {images: [$ref]}')
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    case "$backend" in
      infsh)      json_output "$(json_build command="infsh app run google/gemini-3-1-flash-image-preview --input '...'" provider="$SELECTED" model="$MODEL" backend="$backend" dry_run=true)" ;;
      google)     json_output "$(json_build command="curl -s -X POST 'https://generativelanguage.googleapis.com/...' ..." provider="$SELECTED" model="$MODEL" backend="$backend" dry_run=true)" ;;
      fal)        json_output "$(json_build command="curl -s -X POST 'https://queue.fal.run/fal-ai/nano-banana-2' ..." provider="$SELECTED" model="$MODEL" backend="$backend" dry_run=true)" ;;
      openrouter) json_output "$(json_build command="curl -s -X POST 'https://openrouter.ai/api/v1/...' ..." provider="$SELECTED" model="$MODEL" backend="$backend" dry_run=true)" ;;
    esac
    return
  fi

  log_info "Generating with Nano Banana 2 (${backend})..."
  local result

  if [[ "$backend" == "infsh" ]]; then
    # Use infsh CLI
    result=$(infsh app run google/gemini-3-1-flash-image-preview --input "$input_json" 2>/dev/null)
  elif [[ "$backend" == "google" ]]; then
    # Use Google Gemini API directly
    local api_key="${GOOGLE_API_KEY}"
    # Resolve model: default is gemini-3.1-flash-image-preview (Nano Banana 2)
    # Also supports gemini-3-pro-image-preview (Nano Banana Pro)
    local gemini_model="$MODEL"
    case "$MODEL" in
      pro|nb-pro)   gemini_model="gemini-3-pro-image-preview" ;;
      flash|nb2)    gemini_model="gemini-3.1-flash-image-preview" ;;
    esac
    # Map size to Gemini imageSize format
    local gemini_size="1K"
    case "$RESOLUTION" in
      1k) gemini_size="1K" ;;
      2k) gemini_size="2K" ;;
      4k) gemini_size="4K" ;;
    esac
    # Map aspect ratio
    local gemini_aspect=""
    case "$SIZE" in
      16:9) gemini_aspect="16:9" ;;
      9:16) gemini_aspect="9:16" ;;
      1:1)  gemini_aspect="1:1" ;;
      4:3)  gemini_aspect="4:3" ;;
      3:4)  gemini_aspect="3:4" ;;
    esac
    local payload
    payload=$(jq -n --arg prompt "$PROMPT" --arg size "$gemini_size" --arg aspect "$gemini_aspect" \
      '{
        contents: [{role: "user", parts: [{text: $prompt}]}],
        generationConfig: {
          responseModalities: ["IMAGE", "TEXT"],
          thinkingConfig: {thinkingLevel: "MINIMAL"},
          imageConfig: {imageSize: $size, aspectRatio: $aspect}
        }
      }')
    result=$(curl -sf -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/${gemini_model}:generateContent?key=${api_key}" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>/dev/null)
  elif [[ "$backend" == "fal" ]]; then
    # Use fal.ai nano-banana-2 endpoint
    local api_key="${FAL_API_KEY}"
    local payload
    payload=$(jq -n --arg prompt "$PROMPT" '{prompt: $prompt}')
    result=$(curl -sf -X POST "https://queue.fal.run/fal-ai/nano-banana-2" \
      -H "Authorization: Key ${api_key}" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>/dev/null)
    # fal returns request_id, need to poll
    local request_id
    request_id=$(echo "$result" | jq -r '.request_id // empty')
    if [[ -n "$request_id" ]]; then
      result=$(poll_task fal "$request_id" "https://queue.fal.run/fal-ai/nano-banana-2")
    fi
  elif [[ "$backend" == "openrouter" ]]; then
    # Use OpenRouter API
    local api_key="${OPENROUTER_API_KEY}"
    local or_model="google/gemini-3.1-flash-image-preview"
    case "$MODEL" in
      pro|nb-pro) or_model="google/gemini-3-pro-image-preview" ;;
    esac
    local payload
    payload=$(jq -n --arg prompt "$PROMPT" --arg model "$or_model" \
      '{model: $model, messages: [{role: "user", content: $prompt}]}')
    result=$(curl -sf -X POST "https://openrouter.ai/api/v1/chat/completions" \
      -H "Authorization: Bearer ${api_key}" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>/dev/null)
  fi

  # Extract image URLs from result (handles multiple response formats)
  local images
  images=$(echo "$result" | jq '[.images[]? // .output.images[]? | {url: .}]' 2>/dev/null || echo "[]")

  # If no images found, try Google API response format
  if [[ "$images" == "[]" || "$images" == "null" ]]; then
    images=$(echo "$result" | jq '[.candidates[0].content.parts[]? | select(.inlineData) | {url: ("data:" + .inlineData.mimeType + ";base64," + .inlineData.data)}]' 2>/dev/null || echo "[]")
  fi

  # Download if output specified
  if [[ -n "$OUTPUT" ]]; then
    local first_url
    first_url=$(echo "$images" | jq -r '.[0].url // empty')
    if [[ -n "$first_url" ]]; then
      if [[ "$first_url" == data:* ]]; then
        # Base64 data URI — decode to file
        echo "$first_url" | sed 's/^data:[^;]*;base64,//' | base64 -d > "$OUTPUT"
        log_ok "Downloaded → ${OUTPUT}"
        images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
      else
        download_to "$first_url" "$OUTPUT" >/dev/null
        images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
      fi
    fi
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model="$MODEL" backend="$backend" images="$images")"
}

# ─── Freepik ─────────────────────────────────────────────────────────────────
generate_freepik() {
  require_provider_key freepik
  local api_key
  api_key=$(get_provider_key freepik)

  # Determine endpoint based on model
  # Default: seedream-v5-lite (best balance of quality, speed, and cost)
  local endpoint="https://api.freepik.com/v1/ai/text-to-image/seedream-v5-lite"
  case "$MODEL" in
    seedream-v5-lite) endpoint="https://api.freepik.com/v1/ai/text-to-image/seedream-v5-lite" ;;
    seedream-v4-5)    endpoint="https://api.freepik.com/v1/ai/text-to-image/seedream-v4-5" ;;
    mystic)           endpoint="https://api.freepik.com/v1/ai/mystic" ;;
    flux-2-klein)     endpoint="https://api.freepik.com/v1/ai/text-to-image/flux-2-klein" ;;
    flux-kontext-pro) endpoint="https://api.freepik.com/v1/ai/text-to-image/flux-kontext-pro" ;;
    *)                endpoint="https://api.freepik.com/v1/ai/text-to-image/seedream-v5-lite" ;;
  esac

  # Map size to freepik aspect_ratio format
  # Seedream v5 lite uses different names than Mystic/Flux
  local fp_aspect
  if [[ "$MODEL" == "seedream-v5-lite" || "$MODEL" == "seedream-v5" ]]; then
    case "$SIZE" in
      16:9) fp_aspect="widescreen_16_9" ;;
      9:16) fp_aspect="social_story_9_16" ;;
      1:1)  fp_aspect="square_1_1" ;;
      4:3)  fp_aspect="classic_4_3" ;;
      3:4)  fp_aspect="traditional_3_4" ;;
      3:2)  fp_aspect="standard_3_2" ;;
      2:3)  fp_aspect="portrait_2_3" ;;
      21:9) fp_aspect="cinematic_21_9" ;;
      *)    fp_aspect="widescreen_16_9" ;;
    esac
  else
    case "$SIZE" in
      16:9) fp_aspect="landscape_16_9" ;;
      9:16) fp_aspect="portrait_9_16" ;;
      1:1)  fp_aspect="square_1_1" ;;
      4:3)  fp_aspect="landscape_4_3" ;;
      *)    fp_aspect="landscape_16_9" ;;
    esac
  fi

  # Build payload — unified for all Freepik models
  local payload
  if [[ "$MODEL" == "mystic" ]]; then
    # Mystic has a slightly different payload shape
    payload=$(jq -n \
      --arg prompt "$PROMPT" \
      --arg res "$RESOLUTION" \
      --arg style "$STYLE" \
      --argjson count "$COUNT" \
      '{prompt: $prompt, resolution: $res, num_images: $count, styling: {style: $style}}')
    if [[ -n "$REFERENCE" ]]; then
      payload=$(echo "$payload" | jq --arg ref "$REFERENCE" '. + {style_reference: {image_url: $ref, strength: 70}}')
    fi
  else
    # Seedream / Flux / all other models
    payload=$(jq -n \
      --arg prompt "$PROMPT" \
      --arg aspect "$fp_aspect" \
      --argjson count "$COUNT" \
      '{prompt: $prompt, aspect_ratio: $aspect, num_images: $count}')
    if [[ -n "$REFERENCE" ]]; then
      payload=$(echo "$payload" | jq --arg ref "$REFERENCE" '. + {input_image: $ref}')
    fi
  fi

  local cmd="curl -s -X POST '${endpoint}' -H 'x-freepik-api-key: \$FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '${payload}'"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="$cmd" provider="$SELECTED" model="$MODEL" dry_run=true)"
    return
  fi

  log_info "Generating with Freepik ${MODEL}..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "x-freepik-api-key: ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  # Check if async (has task_id) or sync (has data.images)
  local task_id
  task_id=$(echo "$response" | jq -r '.data.task_id // .task_id // empty' 2>/dev/null)

  if [[ -n "$task_id" ]]; then
    log_task "$task_id" "freepik" "image" "pending" "${OUTPUT:-}"
    local result
    result=$(poll_task freepik "$task_id" "$endpoint")
    local images
    images=$(echo "$result" | jq '[.data.generated[]? | {url: .}] // [.data.images[]? | {url: .url}]' 2>/dev/null || echo "[]")
  else
    # Sync response
    local images
    images=$(echo "$response" | jq '[.data[]? | {url: .url}] // [.data.images[]? | {url: .url}]' 2>/dev/null || echo "[]")
  fi

  # Download first image if output specified
  if [[ -n "$OUTPUT" ]]; then
    local first_url
    first_url=$(echo "$images" | jq -r '.[0].url // empty')
    if [[ -n "$first_url" ]]; then
      download_to "$first_url" "$OUTPUT" >/dev/null
      images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
    fi
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model="$MODEL" images="$images")"
}

# ─── fal.ai ──────────────────────────────────────────────────────────────────
generate_fal() {
  require_provider_key fal
  local api_key
  api_key=$(get_provider_key fal)

  # Resolve model ID
  local model_id="fal-ai/flux-2"
  case "$MODEL" in
    flux-2)     model_id="fal-ai/flux-2" ;;
    flux-2-pro) model_id="fal-ai/flux-2-pro" ;;
    *)          model_id="$MODEL" ;;
  esac

  # Map size to fal format
  local fal_size="landscape_16_9"
  case "$SIZE" in
    16:9) fal_size="landscape_16_9" ;;
    9:16) fal_size="portrait_9_16" ;;
    1:1)  fal_size="square" ;;
    4:3)  fal_size="portrait_4_3" ;;
  esac

  local payload
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --arg size "$fal_size" \
    --argjson count "$COUNT" \
    '{prompt: $prompt, image_size: $size, num_images: $count}')

  if [[ -n "$REFERENCE" ]]; then
    payload=$(echo "$payload" | jq --arg ref "$REFERENCE" '. + {image_url: $ref}')
  fi

  local endpoint="https://queue.fal.run/${model_id}"
  local cmd="curl -s -X POST '${endpoint}' -H 'Authorization: Key \$FAL_API_KEY' -H 'Content-Type: application/json' -d '${payload}'"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="$cmd" provider="$SELECTED" model="$model_id" dry_run=true)"
    return
  fi

  log_info "Generating with fal ${model_id}..."
  local response
  response=$(curl -sf -X POST "$endpoint" \
    -H "Authorization: Key ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local request_id
  request_id=$(echo "$response" | jq -r '.request_id // empty')

  if [[ -n "$request_id" ]]; then
    log_task "$request_id" "fal" "image" "pending" "${OUTPUT:-}"
    local result
    result=$(poll_task fal "$request_id" "$endpoint")
    local images
    images=$(echo "$result" | jq '[.images[]? | {url: .url}]' 2>/dev/null || echo "[]")
  else
    # Direct response
    local images
    images=$(echo "$response" | jq '[.images[]? | {url: .url}]' 2>/dev/null || echo "[]")
  fi

  # Download first image if output specified
  if [[ -n "$OUTPUT" ]]; then
    local first_url
    first_url=$(echo "$images" | jq -r '.[0].url // empty')
    if [[ -n "$first_url" ]]; then
      download_to "$first_url" "$OUTPUT" >/dev/null
      images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
    fi
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model="$model_id" images="$images")"
}

# ─── OpenRouter ───────────────────────────────────────────────────────────────
generate_openrouter() {
  require_provider_key openrouter
  local api_key
  api_key=$(get_provider_key openrouter)

  # Default to nano-banana-2 model on OpenRouter, but support any image model
  local or_model="google/gemini-3.1-flash-image-preview"
  case "$MODEL" in
    pro|nb-pro|gemini-3-pro-image-preview)
      or_model="google/gemini-3-pro-image-preview" ;;
    gemini-3.1-flash-image-preview|flash|nb2)
      or_model="google/gemini-3.1-flash-image-preview" ;;
    openrouter/*)
      or_model="${MODEL#openrouter/}" ;;
    */*)
      or_model="$MODEL" ;;  # Pass through any provider/model format
  esac

  local payload
  payload=$(jq -n --arg prompt "$PROMPT" --arg model "$or_model" \
    '{model: $model, messages: [{role: "user", content: $prompt}]}')

  local endpoint="https://openrouter.ai/api/v1/chat/completions"

  if [[ "$DRY_RUN" == "true" ]]; then
    json_output "$(json_build command="curl -s -X POST '${endpoint}' ..." provider="$SELECTED" model="$or_model" dry_run=true)"
    return
  fi

  log_info "Generating with OpenRouter (${or_model})..."
  local result
  result=$(curl -sf -X POST "$endpoint" \
    -H "Authorization: Bearer ${api_key}" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null)

  # Extract images from OpenRouter response (varies by model)
  local images="[]"

  # Try: choices[0].message.content with base64 inline data
  local b64_data
  b64_data=$(echo "$result" | jq -r '.choices[0].message.content // empty' 2>/dev/null)
  if [[ -n "$b64_data" && "$b64_data" == data:image* ]]; then
    images="[{\"url\":\"${b64_data}\"}]"
  fi

  # Try: image_urls array in response
  if [[ "$images" == "[]" ]]; then
    images=$(echo "$result" | jq '[(.image_urls // .images // [])[] | {url: .}]' 2>/dev/null || echo "[]")
  fi

  # Download if output specified
  if [[ -n "$OUTPUT" ]]; then
    local first_url
    first_url=$(echo "$images" | jq -r '.[0].url // empty')
    if [[ -n "$first_url" ]]; then
      if [[ "$first_url" == data:* ]]; then
        echo "$first_url" | sed 's/^data:[^;]*;base64,//' | base64 -d > "$OUTPUT"
        log_ok "Downloaded → ${OUTPUT}"
        images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
      else
        download_to "$first_url" "$OUTPUT" >/dev/null
        images=$(echo "$images" | jq --arg lp "$OUTPUT" '.[0].local_path = $lp')
      fi
    fi
  fi

  json_output "$(json_build status=completed provider="$SELECTED" model="$or_model" images="$images")"
}

# ─── Dispatch ────────────────────────────────────────────────────────────────
case "$SELECTED" in
  nano-banana-2) generate_nano_banana ;;
  freepik)       generate_freepik ;;
  fal)           generate_fal ;;
  openrouter)    generate_openrouter ;;
  *)             json_error "Unsupported provider: ${SELECTED}" ;;
esac
