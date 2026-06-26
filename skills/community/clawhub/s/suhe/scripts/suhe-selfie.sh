#!/bin/bash

# Suhe Selfie Generator
# Generates selfies using Tongyi Wanxiang API

set -e  # Exit on any error

echo "📸 Starting Suhe Selfie Generation..."

# Check if required environment variables are set
if [ -z "$DASHSCOPE_API_KEY" ]; then
  echo "❌ Error: DASHSCOPE_API_KEY environment variable is not set"
  echo "💡 Solution: export DASHSCOPE_API_KEY='your_api_key_here'"
  exit 1
fi

if [ -z "$OPENCLAW_GATEWAY_TOKEN" ]; then
  echo "❌ Error: OPENCLAW_GATEWAY_TOKEN environment variable is not set"
  echo "💡 Solution: Run 'openclaw doctor --generate-gateway-token' to generate one"
  exit 1
fi

# Default values
INPUT_PROMPT=""
TARGET_CHANNEL="#general"
MODE="mirror"  # Default mode

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--prompt)
      INPUT_PROMPT="$2"
      shift 2
      ;;
    -c|--channel)
      TARGET_CHANNEL="$2"
      shift 2
      ;;
    -m|--mode)
      MODE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate inputs
if [ -z "$INPUT_PROMPT" ]; then
  echo "❌ Error: No prompt provided"
  echo "Usage: $0 -p \"your prompt here\" [-c target_channel] [-m mode]"
  exit 1
fi

echo "🔧 Using mode: $MODE"
echo "📥 Input prompt: $INPUT_PROMPT"
echo "📡 Target channel: $TARGET_CHANNEL"

# Generate the final prompt based on mode
FINAL_PROMPT=""
REFERENCE_IMAGE="https://pic.lilozkzy.top/reference/suhe-new.png"

if [ "$MODE" == "mirror" ]; then
  # Mirror selfie: best for outfits, full body shots
  FINAL_PROMPT="make a pic of this person, but ${INPUT_PROMPT}. the person is taking a mirror selfie"
else
  # Direct selfie: best for close-ups, locations, expressions
  FINAL_PROMPT="a close-up selfie taken by herself at ${INPUT_PROMPT}, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible"
fi

echo "🎨 Generated prompt: $FINAL_PROMPT"

# Call the Tongyi Wanxiang API
echo "☁️ Calling Tongyi Wanxiang API..."
API_RESPONSE=$(curl -s -X POST \
  "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"wanx-imagegen\"",
    \"input\": {
      \"prompt\": \"$FINAL_PROMPT\",
      \"reference_image\": \"$REFERENCE_IMAGE\"
    },
    \"parameters\": {
      \"size\": \"1024*1024\",
      \"n\": 1
    }
  }")

# Extract image URL from response (this assumes a standard response format)
IMAGE_URL=$(echo $API_RESPONSE | jq -r '.output.images[0].url')

if [ "$IMAGE_URL" == "null" ] || [ -z "$IMAGE_URL" ]; then
  echo "❌ Failed to generate image"
  echo "API Response: $API_RESPONSE"
  exit 1
fi

echo "🖼️ Generated image: $IMAGE_URL"

# Send image to OpenClaw gateway
echo "📤 Sending image to OpenClaw gateway..."
GATEWAY_RESPONSE=$(curl -s -X POST \
  "http://localhost:3000/api/v1/messages" \
  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"target\": \"$TARGET_CHANNEL\",
    \"message\": {
      \"type\": \"image_url\",
      \"data\": {
        \"url\": \"$IMAGE_URL\",
        \"caption\": \"$INPUT_PROMPT\"
      }
    }
  }")

echo "✅ Selfie sent successfully!"
echo "Gateway Response: $GATEWAY_RESPONSE"