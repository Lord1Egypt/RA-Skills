#!/bin/bash
# install.sh
# WitPulse-redditnews Installation Script

SKILL_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Initializing WitPulse-redditnews..."

# Ensure data directory exists
mkdir -p "$SKILL_ROOT/data"

# Ensure config exists
if [ ! -f "$SKILL_ROOT/config.json" ]; then
    echo "Creating default config..."
    echo '{"subreddits": ["r/technology"], "language": "zh-CN"}' > "$SKILL_ROOT/config.json"
fi

echo "Initialization complete."
echo "You can run this skill using:"
echo "bash $SKILL_ROOT/scripts/run_witpulse.sh"
