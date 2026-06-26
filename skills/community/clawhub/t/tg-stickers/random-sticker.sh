#!/bin/bash
# random-sticker.sh - Pick a random sticker by emotion tags
# Usage: ./random-sticker.sh "happy" "excited"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STICKERS_JSON="$SCRIPT_DIR/stickers.json"

if [ ! -f "$STICKERS_JSON" ]; then
    echo "Error: stickers.json not found" >&2
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 <tag1> [tag2] [tag3]..." >&2
    exit 1
fi

# Build jq filter for multiple tags (OR logic)
TAGS=("$@")
JQ_FILTER='.collected[] | select('

for i in "${!TAGS[@]}"; do
    if [ $i -gt 0 ]; then
        JQ_FILTER+=" or "
    fi
    JQ_FILTER+=".tags[]? | contains(\"${TAGS[$i]}\")"
done

JQ_FILTER+=') | .file_id'

# Get all matching stickers and pick random one
cat "$STICKERS_JSON" | jq -r "$JQ_FILTER" | sort -R | head -1
