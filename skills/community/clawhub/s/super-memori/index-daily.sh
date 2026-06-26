#!/bin/bash
# index-daily.sh — Incremental memory indexing into Qdrant
# Run via cron: 0 2 * * * ~/.openclaw/skills/memory-enhancement/index-daily.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
COLLECTION="memories"
QDRANT_URL="http://127.0.0.1:6333"

# Lock to prevent overlapping runs
exec 200>/tmp/memory-index.lock
flock -n 200 || { echo "[$(date)] Another indexing run in progress, skipping."; exit 0; }

STATE_FILE="$SCRIPT_DIR/.index_state"

# Ensure collection exists
create_collection() {
    curl -s -X PUT "${QDRANT_URL}/collections/${COLLECTION}" \
        -H 'Content-Type: application/json' \
        -d '{
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            },
            "optimizers_config": {
                "memmap_threshold": 50000
            }
        }' 2>/dev/null || true
}

echo "[$(date)] Starting memory index..."

# Create state file if it doesn't exist
touch "$STATE_FILE"

# Find only changed or new files since last index
changed_files=$(find "$MEMORY_DIR" -name "*.md" -type f -newer "$STATE_FILE" 2>/dev/null)

if [ -z "$changed_files" ]; then
    echo "[$(date)] No changes detected since last index."
    touch "$STATE_FILE"
    exit 0
fi

echo "$changed_files" | while read -r filepath; do
    # Check if file needs embedding (modified since last index)
    python3 "$SCRIPT_DIR/embed-file.py" "$filepath" "$COLLECTION" "$QDRANT_URL"
done

echo "[$(date)] Index complete."
