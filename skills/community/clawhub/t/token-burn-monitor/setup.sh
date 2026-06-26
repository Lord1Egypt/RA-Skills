#!/bin/bash
# Token Burn Monitor - Post-install setup
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR"

echo "⚡ Token Burn Monitor installed at $SKILL_DIR"
echo ""
echo "Quick start:"
echo "  bash start.sh          # Start the dashboard"
echo "  bash start.sh status   # Check if running"
echo "  bash start.sh stop     # Stop the dashboard"
echo ""
echo "Custom config: copy config.default.json → config.json and edit."
echo "Dashboard URL: http://localhost:3847"
