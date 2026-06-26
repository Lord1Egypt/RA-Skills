#!/bin/bash
# suhe-selfie.sh
# Generate Suhe's selfie with Tongyi Wanxiang qwen-image-2.0 model
# Supports reference image for consistent character appearance
#
# Usage: ./suhe-selfie.sh "<prompt>" "<channel>" ["<caption>"]
#
# Environment variables required:
#   DASHSCOPE_API_KEY - Your DashScope API key from Aliyun

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check required environment variables
if [ -z "${DASHSCOPE_API_KEY:-}" ]; then
    log_error "DASHSCOPE_API_KEY environment variable not set"
    echo "Get your API key from: https://dashscope.console.aliyun.com/"
    exit 1
fi

# Check for jq
if ! command -v jq &> /dev/null; then
    log_error "jq is required but not installed"
    echo "Install with: apt install jq (Linux)"
    exit 1
fi

# Suhe's reference image (AI generated, safe to use)
REFERENCE_IMAGE="http://pic.lilozkzy.top/reference/suhe-new.png"

# Parse arguments
USER_CONTEXT="${1:-}"
CHANNEL="${2:-}"
CAPTION="${3:-苏禾的自拍 💕}"
MODE="${4:-auto}"

if [ -z "$USER_CONTEXT" ] || [ -z "$CHANNEL" ]; then
    echo "Usage: $0 <user_context> <channel> [caption] [mode]"
    echo ""
    echo "Arguments:"
    echo "  user_context - Situation description (required)"
    echo "  channel      - Target channel (required)"
    echo "  caption      - Message caption (default: '苏禾的自拍 💕')"
    echo "  mode         - mirror, direct, or auto (default: auto)"
    echo ""
    echo "Example:"
    echo "  $0 '穿着白色连衣裙' '#general' '今天的穿搭~' mirror"
    echo "  $0 '在咖啡厅里' '@user' '下午茶时间' direct"
    exit 1
fi

# Auto-detect mode based on keywords
if [ "$MODE" == "auto" ]; then
    if echo "$USER_CONTEXT" | grep -qiE "穿着|衣服|服装|dress|skirt|fashion|全身|镜子"; then
        MODE="mirror"
    elif echo "$USER_CONTEXT" | grep -qiE "咖啡厅|餐厅|公园|家里|办公室|特写|肖像|脸|微笑"; then
        MODE="direct"
    else
        MODE="mirror"  # default
    fi
    log_info "Auto-detected mode: $MODE"
fi

# Build prompt based on mode
# Suhe: 28-year-old freelance illustrator from Hangzhou, independent personality
if [ "$MODE" == "direct" ]; then
    EDIT_PROMPT="Generate a close-up portrait photo of this person at $USER_CONTEXT, direct eye contact with camera, warm smile, high quality photography"
else
    EDIT_PROMPT="Generate a photo of this person taking a mirror selfie, $USER_CONTEXT, showing full body, confident posture, high quality photography"
fi

log_info "Generating Suhe's selfie with qwen-image-2.0..."
log_info "Mode: $MODE"
log_info "Prompt: $EDIT_PROMPT"
log_info "Reference image: $REFERENCE_IMAGE"

# Build JSON payload for qwen-image-2.0 (multimodal-generation endpoint)
# Reference: https://help.aliyun.com/zh/model-studio/developer-reference/tongyi-wanxiang
PAYLOAD=$(jq -n \
    --arg ref_url "$REFERENCE_IMAGE" \
    --arg prompt "$EDIT_PROMPT" \
    '{
        model: "qwen-image-2.0",
        input: {
            messages: [
                {
                    role: "user",
                    content: [
                        {image: $ref_url},
                        {text: $prompt}
                    ]
                }
            ]
        },
        parameters: {
            n: 1,
            size: "1024*1024",
            watermark: true,
            negative_prompt: "low quality, blurry, distorted, ugly"
        }
    }')

# Submit via DashScope API
log_info "Submitting task to Tongyi Wanxiang API..."
RESPONSE=$(curl -s -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

# Check for errors
if echo "$RESPONSE" | jq -e '.code' > /dev/null 2>&1; then
    ERROR_CODE=$(echo "$RESPONSE" | jq -r '.code // empty')
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "Unknown error"')
    log_error "Image generation failed: [$ERROR_CODE] $ERROR_MSG"
    echo "Response: $RESPONSE"
    exit 1
fi

# Extract image URL from response
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.output.choices[0].message.content[0].image // empty')

if [ -z "$IMAGE_URL" ]; then
    log_error "Failed to extract image URL from response"
    echo "Response: $RESPONSE"
    exit 1
fi

log_info "Image generated successfully!"
log_info "URL: $IMAGE_URL"

# Send via OpenClaw
log_info "Sending to channel: $CHANNEL"

if command -v openclaw &> /dev/null; then
    openclaw message send \
        --channel "$CHANNEL" \
        --target "$CHANNEL" \
        -m "$CAPTION" \
        --media "$IMAGE_URL"
else
    # Direct API call to gateway
    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18889}"
    
    curl -s -X POST "$GATEWAY_URL/message" \
        -H "Content-Type: application/json" \
        -d "{
            \"action\": \"send\",
            \"channel\": \"$CHANNEL\",
            \"message\": \"$CAPTION\",
            \"media\": \"$IMAGE_URL\"
        }"
fi

log_info "Done! Image sent to $CHANNEL"

# Output JSON for programmatic use
echo ""
echo "--- Result ---"
jq -n \
    --arg url "$IMAGE_URL" \
    --arg channel "$CHANNEL" \
    --arg prompt "$EDIT_PROMPT" \
    --arg caption "$CAPTION" \
    --arg mode "$MODE" \
    '{
        success: true,
        image_url: $url,
        channel: $channel,
        prompt: $prompt,
        caption: $caption,
        mode: $mode
    }'
