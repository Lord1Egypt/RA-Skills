#!/bin/bash
# Helper script for sending Telegram messages with inline buttons
# Usage: ./send_buttons.sh TARGET MESSAGE BUTTONS_JSON

set -e

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <target> <message> <buttons_json>"
    echo ""
    echo "Example:"
    echo "  $0 'telegram:1216079319' 'Choose:' '[[{\"text\": \"Yes\", \"callback_data\": \"yes\"}]]'"
    exit 1
fi

TARGET="$1"
MESSAGE="$2"
BUTTONS="$3"

# Validate JSON structure (optional, requires validate_buttons.py)
if command -v python3 &> /dev/null; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/validate_buttons.py" ]; then
        python3 "$SCRIPT_DIR/validate_buttons.py" "$BUTTONS" || exit 1
    fi
fi

# Send message with buttons
openclaw message send \
    --target "$TARGET" \
    --message "$MESSAGE" \
    --buttons "$BUTTONS"
