#!/usr/bin/env bash
# Workspace Archiver - Archive old files
# Part of workspace-manager skill

set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
ARCHIVE="$WORKSPACE/archive"
ARTIFACTS="$WORKSPACE/Workspace_Agent/artifacts"
DAYS="${DAYS:-7}"

echo "=========================================="
echo "      📦 Workspace Archiver"
echo "=========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo "Archive files older than: $DAYS days"
echo ""

# Create archive directory by month
MONTH=$(date '+%Y-%m')
mkdir -p "$ARCHIVE/$MONTH"

echo "📂 Scanning for files older than $DAYS days in artifacts..."
echo ""

# Find old files (excluding protected)
OLD_FILES=$(find "$ARTIFACTS" -maxdepth 1 -type f -mtime +$DAYS 2>/dev/null || true)

if [ -z "$OLD_FILES" ]; then
    echo "✅ No files to archive."
    exit 0
fi

COUNT=$(echo "$OLD_FILES" | wc -l)
echo "Found $COUNT files to archive:"
echo ""

# Show what will be archived
TOTAL_SIZE=0
while IFS= read -r file; do
    SIZE=$(du -h "$file" 2>/dev/null | cut -f1)
    echo "   📄 $SIZE - $(basename "$file")"
    TOTAL_SIZE=$((TOTAL_SIZE + $(stat -c%s "$file" 2>/dev/null || echo 0)))
done <<< "$OLD_FILES"

echo ""
echo "Destination: $ARCHIVE/$MONTH/"
echo ""

# Confirm before archiving
read -p "⚠️  Proceed with archiving? (y/N): " confirm
if [ "${confirm:-N}" != "y" ]; then
    echo "❌ Cancelled."
    exit 0
fi

# Archive files
ARCHIVED=0
while IFS= read -r file; do
    mv "$file" "$ARCHIVE/$MONTH/"
    echo "   ✅ $(basename "$file")"
    ARCHIVED=$((ARCHIVED + 1))
done <<< "$OLD_FILES"

echo ""
echo "✅ Archived $ARCHIVED files to $ARCHIVE/$MONTH/"
