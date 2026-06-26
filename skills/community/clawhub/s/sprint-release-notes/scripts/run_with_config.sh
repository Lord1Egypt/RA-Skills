#!/bin/bash
# Sprint Release Notes Runner
# Reads config and executes the generation script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../references/config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

# Parse YAML config (simple extraction)
PAT_TOKEN=$(grep "pat_token:" "$CONFIG_FILE" | sed 's/.*pat_token: *//' | tr -d '"')
BOARD_URL=$(grep "project_board_url:" "$CONFIG_FILE" | sed 's/.*project_board_url: *//' | tr -d '"')

if [ -z "$PAT_TOKEN" ] || [ -z "$BOARD_URL" ]; then
    echo "Error: Missing pat_token or project_board_url in config"
    exit 1
fi

# Run the script with config values
# Note: For per-repo publish, we'll need a modified script version
# For now, run with --dry-run to test, then manually publish
python3 "$SCRIPT_DIR/generate_release_notes.py" \
    --board-url "$BOARD_URL" \
    --pat "$PAT_TOKEN" \
    --release-repo "OpenPecha/release-notes" \
    --dry-run
