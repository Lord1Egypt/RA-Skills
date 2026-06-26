#!/bin/bash
#
# Check Sticker Collection Status
# Quick check if you have stickers ready to use
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STICKERS_JSON="$SCRIPT_DIR/stickers.json"

# Check if stickers.json exists
if [ ! -f "$STICKERS_JSON" ]; then
    echo "⚠️  No stickers.json found!"
    echo ""
    echo "📝 Quick setup:"
    echo "   1. cp stickers.json.example stickers.json"
    echo "   2. Send some stickers in Telegram"
    echo "   3. Run: ./add-sticker.sh <file_id> <emoji>"
    exit 1
fi

# Count collected stickers
TOTAL=$(jq '.collected | length' "$STICKERS_JSON")

if [ "$TOTAL" -eq 0 ]; then
    echo "📭 Sticker collection is empty!"
    echo ""
    echo "💡 To get started:"
    echo "   1. Send me some stickers in Telegram"
    echo "   2. I'll show you the file_id in the message"
    echo "   3. Run: ./add-sticker.sh <file_id> <emoji> [set_name] [tags]"
    echo ""
    echo "Example:"
    echo "   ./add-sticker.sh 'CAACAgEA...' '😀' 'MySet' 'happy,excited'"
else
    echo "✅ You have $TOTAL sticker(s) in your collection!"
    echo ""
    echo "📊 Collection preview:"
    jq -r '.collected[] | "   \(.emoji) - \(.set_name) (used \(.used_count) times)"' "$STICKERS_JSON"
    echo ""
    echo "📈 Stats:"
    jq -r '"   Total sent: \(.stats.total_sent)"' "$STICKERS_JSON"
    jq -r '"   Last sent: \(.stats.last_sent_at // "Never")"' "$STICKERS_JSON"
fi
