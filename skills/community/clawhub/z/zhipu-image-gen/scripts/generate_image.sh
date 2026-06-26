#!/bin/bash
# GLM Image Generation Script
# Calls Zhipu AI's image generation API

set -e

# Default values
DEFAULT_SIZE="1280x1280"
DEFAULT_MODEL="glm-image"
DEFAULT_WATERMARK="false"
API_URL="https://open.bigmodel.cn/api/paas/v4/images/generations"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load ZHIPU_API_KEY from .env file if exists (secure: only read the specific variable)
ENV_FILE="$SKILL_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    # Secure read: only extract ZHIPU_API_KEY, ignore other content
    API_KEY_FROM_ENV=$(grep -E '^ZHIPU_API_KEY=' "$ENV_FILE" 2>/dev/null | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    if [ -n "$API_KEY_FROM_ENV" ]; then
        export ZHIPU_API_KEY="$API_KEY_FROM_ENV"
    fi
fi

# Check for API key
API_KEY="${ZHIPU_API_KEY:-}"
if [ -z "$API_KEY" ]; then
    echo "Error: ZHIPU_API_KEY not found"
    echo ""
    echo "Please configure using one of these methods:"
    echo ""
    echo "Method 1: Environment variable"
    echo "  export ZHIPU_API_KEY=your_api_key"
    echo ""
    echo "Method 2: .env file (recommended)"
    echo "  Create file: $ENV_FILE"
    echo "  Add line: ZHIPU_API_KEY=your_api_key"
    echo ""
    echo "Get your API key from: https://open.bigmodel.cn/"
    exit 1
fi

# Parse arguments
PROMPT=""
SIZE="$DEFAULT_SIZE"
OUTPUT_DIR="."
WATERMARK="$DEFAULT_WATERMARK"

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--prompt)
            PROMPT="$2"
            shift 2
            ;;
        -s|--size)
            SIZE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -w|--watermark)
            WATERMARK="true"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 -p <prompt> [-s <size>] [-o <output_dir>] [-w]"
            echo ""
            echo "Options:"
            echo "  -p, --prompt     The image generation prompt (required)"
            echo "  -s, --size       Image size (default: $DEFAULT_SIZE)"
            echo "  -o, --output     Output directory (default: current directory)"
            echo "  -w, --watermark  Enable watermark (default: false)"
            echo "  -h, --help       Show this help message"
            echo ""
            echo "Configuration:"
            echo "  Set ZHIPU_API_KEY via environment variable or .env file"
            echo "  .env file location: $ENV_FILE"
            echo ""
            echo "Example:"
            echo "  $0 -p '一只可爱的小猫咪，坐在阳光明媚的窗台上' -s 1280x1280"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate prompt
if [ -z "$PROMPT" ]; then
    echo "Error: Prompt is required. Use -p or --prompt to specify."
    exit 1
fi

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Generate timestamp for filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Call API
echo "Generating image..."
echo "Prompt: $PROMPT"
echo "Size: $SIZE"
echo "Watermark: $WATERMARK"

RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$DEFAULT_MODEL\",
        \"prompt\": \"$PROMPT\",
        \"size\": \"$SIZE\",
        \"watermark_enabled\": $WATERMARK
    }")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "API Error:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# Extract image URL
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.data[0].url // empty')

if [ -z "$IMAGE_URL" ] || [ "$IMAGE_URL" = "null" ]; then
    echo "Error: No image URL in response"
    echo "Response: $RESPONSE"
    exit 1
fi

# Download image
OUTPUT_FILE="${OUTPUT_DIR}/glm_image_${TIMESTAMP}.png"
echo "Downloading image to: $OUTPUT_FILE"
curl -s -o "$OUTPUT_FILE" "$IMAGE_URL"

if [ $? -eq 0 ]; then
    echo "✓ Image saved successfully: $OUTPUT_FILE"
    echo "Image URL: $IMAGE_URL"
else
    echo "Error downloading image"
    exit 1
fi
