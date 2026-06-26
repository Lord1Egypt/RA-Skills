#!/bin/bash
# Archive current relay snapshot with timestamp
# Usage: archive-snapshot.sh [workspace_dir]

WORKSPACE="${1:-$(pwd)}"
SNAPSHOT="$WORKSPACE/memory/relay-snapshot.md"
ARCHIVE_DIR="$WORKSPACE/memory/relay-archive"

if [ ! -f "$SNAPSHOT" ]; then
    echo "No snapshot to archive"
    exit 0
fi

mkdir -p "$ARCHIVE_DIR"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
cp "$SNAPSHOT" "$ARCHIVE_DIR/$TIMESTAMP.md"
rm "$SNAPSHOT"
echo "Archived to $ARCHIVE_DIR/$TIMESTAMP.md"
