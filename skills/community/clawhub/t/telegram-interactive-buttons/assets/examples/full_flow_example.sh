#!/bin/bash
# Example: Complete callback handling flow
# Demonstrates the full lifecycle: send → callback → confirm → edit
#
# ⚠️ SECURITY WARNING:
# - Replace YOUR_CHAT_ID with your actual Telegram chat ID
# - Review this script before running
# - Only run in trusted environments
# - Requires openclaw CLI configured with Telegram bot token
# - This script is INTERACTIVE - it will prompt for input

TARGET="telegram:YOUR_CHAT_ID"  # ⚠️ REPLACE WITH YOUR CHAT ID

# Step 1: Send message with buttons
echo "=== Step 1: Sending interactive message ==="
RESPONSE=$(openclaw message send \
    --target "$TARGET" \
    --message "Select a file operation:" \
    --buttons '[[{"text": "📁 Backup", "callback_data": "file_backup"}, {"text": "🗑️ Delete", "callback_data": "file_delete", "style": "danger"}], [{"text": "❌ Cancel", "callback_data": "file_cancel"}]]' 2>&1)

# Extract message ID from response
MESSAGE_ID=$(echo "$RESPONSE" | grep "Message ID:" | sed 's/.*Message ID: //')
echo "Sent message with ID: $MESSAGE_ID"
echo ""

# Simulate waiting for user callback
echo "=== Waiting for user to click a button... ==="
echo "(In real usage, this happens asynchronously via Telegram callback)"
echo ""

# Simulate different callback scenarios:
echo "Choose which button was clicked:"
echo "  1) Backup"
echo "  2) Delete"
echo "  3) Cancel"
read -p "Enter choice (1-3): " choice

# Step 2: Handle callback based on user selection
echo ""
echo "=== Step 2: Handling callback ==="

case $choice in
    1)
        CALLBACK="file_backup"
        SELECTED="Backup"
        CONFIRM_MSG="✅ Backup initiated. Files are being copied..."
        ;;
    2)
        CALLBACK="file_delete"
        SELECTED="Delete"
        CONFIRM_MSG="🗑️ Files deleted successfully."
        ;;
    3)
        CALLBACK="file_cancel"
        SELECTED="Cancel"
        CONFIRM_MSG="❌ Operation cancelled."
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo "User clicked: $SELECTED (callback_data: $CALLBACK)"
echo ""

# Step 3: Send confirmation message
echo "=== Step 3: Sending confirmation ==="
openclaw message send \
    --target "$TARGET" \
    --message "$CONFIRM_MSG"
echo ""

# Step 4: Edit original message to remove buttons
echo "=== Step 4: Editing original message (removing buttons) ==="
openclaw message edit \
    --target "$TARGET" \
    --message-id "$MESSAGE_ID" \
    --message "Select a file operation: [$SELECTED selected]"

echo ""
echo "✅ Complete flow executed successfully!"
echo ""
echo "Summary:"
echo "  1. Sent interactive message with 3 buttons"
echo "  2. User clicked: $SELECTED"
echo "  3. Sent confirmation message"
echo "  4. Edited original message to show selection and remove buttons"
echo ""
echo "This prevents:"
echo "  - Accidental re-clicks on old buttons"
echo "  - Confusion about which option was selected"
echo "  - Cluttered chat history"
