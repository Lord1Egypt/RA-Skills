#!/bin/bash
#
# Import entire Telegram sticker pack
# Usage: ./import-sticker-pack.sh <pack_name>
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STICKERS_JSON="$SCRIPT_DIR/stickers.json"

# Telegram Bot Token (read from OpenClaw config)
BOT_TOKEN=$(jq -r '.channels.telegram.botToken' ~/.openclaw/openclaw.json)

if [ -z "$1" ]; then
    echo "Usage: $0 <pack_name>"
    echo ""
    echo "Example:"
    echo "  $0 p_8RnHygLOjgFhGENFwoc1_by_SigStick11Bot"
    echo ""
    echo "To find pack name: right-click a sticker in Telegram → Copy Link"
    echo "The URL will be: https://t.me/addstickers/<pack_name>"
    exit 1
fi

PACK_NAME="$1"

echo "🔍 Fetching sticker pack: $PACK_NAME"

# Get sticker set from Telegram API
RESPONSE=$(curl -s "https://api.telegram.org/bot$BOT_TOKEN/getStickerSet?name=$PACK_NAME")

# Check if successful
if ! echo "$RESPONSE" | jq -e '.ok' > /dev/null; then
    ERROR=$(echo "$RESPONSE" | jq -r '.description // "Unknown error"')
    echo "❌ Failed to fetch sticker pack: $ERROR"
    exit 1
fi

# Extract sticker count
STICKER_COUNT=$(echo "$RESPONSE" | jq '.result.stickers | length')
PACK_TITLE=$(echo "$RESPONSE" | jq -r '.result.title')

echo "📦 Pack: $PACK_TITLE ($STICKER_COUNT stickers)"
echo ""

# Process each sticker
ADDED=0
SKIPPED=0
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "$RESPONSE" | jq -c '.result.stickers[]' | while read -r sticker; do
    FILE_ID=$(echo "$sticker" | jq -r '.file_id')
    EMOJI=$(echo "$sticker" | jq -r '.emoji')
    
    # Check if already exists
    if jq -e --arg fid "$FILE_ID" '.collected[] | select(.file_id == $fid)' "$STICKERS_JSON" > /dev/null 2>&1; then
        echo "  ⏭️  Skipped: $EMOJI (already in collection)"
        ((SKIPPED++)) || true
        continue
    fi
    
    # Add to collection
    jq --arg fid "$FILE_ID" \
       --arg emoji "$EMOJI" \
       --arg set "$PACK_NAME" \
       --arg ts "$TIMESTAMP" \
       '.collected += [{
           "file_id": $fid,
           "emoji": $emoji,
           "set_name": $set,
           "added_at": $ts,
           "used_count": 0,
           "last_used": null,
           "tags": []
       }]' "$STICKERS_JSON" > "$STICKERS_JSON.tmp"
    
    mv "$STICKERS_JSON.tmp" "$STICKERS_JSON"
    
    echo "  ✅ Added: $EMOJI"
    ((ADDED++)) || true
done

# Update total count
jq --arg count "$ADDED" '.stats.total_collected += ($count | tonumber)' "$STICKERS_JSON" > "$STICKERS_JSON.tmp"
mv "$STICKERS_JSON.tmp" "$STICKERS_JSON"

echo ""
echo "✅ Import complete!"
echo "   Added: $ADDED stickers"
echo "   Skipped: $SKIPPED (duplicates)"
echo ""
echo "📊 Run './check-collection.sh' to see your collection"
