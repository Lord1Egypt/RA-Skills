#!/bin/bash
# Example: Basic Yes/No confirmation dialog
# This is the simplest form of interactive buttons
#
# ⚠️ SECURITY WARNING:
# - Replace YOUR_CHAT_ID with your actual Telegram chat ID
# - Review this script before running
# - Only run in trusted environments
# - Requires openclaw CLI configured with Telegram bot token

TARGET="telegram:YOUR_CHAT_ID"  # ⚠️ REPLACE WITH YOUR CHAT ID

echo "Sending yes/no confirmation..."

openclaw message send \
    --target "$TARGET" \
    --message "Do you want to proceed?" \
    --buttons '[[{"text": "✅ Yes", "callback_data": "confirm_yes"}, {"text": "❌ No", "callback_data": "confirm_no"}]]'

echo ""
echo "Button callbacks to handle:"
echo "  - confirm_yes: User clicked Yes"
echo "  - confirm_no: User clicked No"
echo ""
echo "After handling callback, edit the message to remove buttons:"
echo "  openclaw message edit --target '$TARGET' --message-id 'MESSAGE_ID' --message 'Selection recorded'"
