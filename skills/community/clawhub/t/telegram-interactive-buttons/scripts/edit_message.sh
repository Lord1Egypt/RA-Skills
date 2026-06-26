#!/bin/bash
# Helper script for editing Telegram messages (typically to remove buttons)
# Usage: ./edit_message.sh TARGET MESSAGE_ID NEW_MESSAGE

set -e

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <target> <message_id> <new_message>"
    echo ""
    echo "Example:"
    echo "  $0 'telegram:1216079319' '939' 'Selection complete'"
    exit 1
fi

TARGET="$1"
MESSAGE_ID="$2"
NEW_MESSAGE="$3"

# Edit message (removes buttons by default)
openclaw message edit \
    --target "$TARGET" \
    --message-id "$MESSAGE_ID" \
    --message "$NEW_MESSAGE"
