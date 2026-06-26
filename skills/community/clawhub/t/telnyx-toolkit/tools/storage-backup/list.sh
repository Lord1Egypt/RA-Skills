#!/bin/bash
#
# list.sh - List available backups in Telnyx Storage
#
# Usage: ./list.sh [bucket_name]
#

BUCKET="${1:-openclaw-backup}"

echo "📋 Available Backups"
echo "========================================"
echo "Bucket: $BUCKET"
echo ""

# Check CLI is available
if ! command -v telnyx &> /dev/null; then
    echo "❌ Telnyx CLI not found. Install: npm install -g telnyx-cli"
    echo "   Then run: telnyx auth setup"
    exit 1
fi

telnyx storage object list "$BUCKET" | grep "openclaw-backup-" | while read -r backup; do
    echo "  • $backup"
done

echo ""
echo "To restore: ./restore.sh <backup_name>"
echo "To restore latest: ./restore.sh latest"
