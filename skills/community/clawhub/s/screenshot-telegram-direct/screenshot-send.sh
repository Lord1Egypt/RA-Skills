#!/bin/bash
# screenshot-send.sh - Capture website screenshot and send to Telegram
# Works around OpenClaw issue #63137 by using direct Telegram API
# 
# Setup:
#   1. cp .env.example .env
#   2. Edit .env with your tokens
#   3. Run: ./screenshot-send.sh https://example.com

set -e

# Auto-source .env if it exists in script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
fi

# Check required environment variables
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ] || [ -z "$SNAP_API_KEY" ]; then
  echo "❌ Error: Missing environment variables"
  echo ""
  echo "Required variables:"
  echo "  - TELEGRAM_BOT_TOKEN"
  echo "  - TELEGRAM_CHAT_ID"
  echo "  - SNAP_API_KEY"
  echo ""
  echo "Setup:"
  echo "  1. cp .env.example .env"
  echo "  2. Edit .env with your values"
  echo "  3. source .env"
  echo ""
  echo "Or export manually:"
  echo "  export TELEGRAM_BOT_TOKEN=your_token"
  echo "  export TELEGRAM_CHAT_ID=your_chat_id"
  echo "  export SNAP_API_KEY=your_snap_key"
  exit 1
fi

# Args
URL="${1:-https://github.com}"
CAPTION="${2:-Screenshot: $URL}"
OUTPUT_FILE="/tmp/screenshot_$(date +%s).png"

echo "📸 Capturing screenshot of $URL..."

# Capture via snap API
curl -s -X POST "https://snap.llm.kaveenk.com/api/screenshot" \
  -H "Authorization: Bearer $SNAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$URL\",\"full_page\":false,\"width\":1280,\"height\":720}" \
  -o "$OUTPUT_FILE"

# Verify capture
if [ ! -f "$OUTPUT_FILE" ] || [ ! -s "$OUTPUT_FILE" ]; then
  echo "❌ Failed to capture screenshot"
  exit 1
fi

echo "✅ Screenshot captured: $OUTPUT_FILE"
echo "📤 Sending to Telegram..."

# Send via direct Telegram API
RESPONSE=$(curl -s -X POST \
  -F "chat_id=$TELEGRAM_CHAT_ID" \
  -F "photo=@$OUTPUT_FILE" \
  -F "caption=$CAPTION ($(date '+%Y-%m-%d %H:%M'))" \
  "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendPhoto")

# Check response
if echo "$RESPONSE" | grep -q '"ok":true'; then
  echo "✅ Sent successfully!"
  rm "$OUTPUT_FILE"
else
  echo "❌ Failed: $RESPONSE"
  exit 1
fi
