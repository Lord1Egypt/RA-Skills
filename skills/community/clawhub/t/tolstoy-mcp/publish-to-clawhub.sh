#!/bin/bash
# Publish Tolstoy MCP skill to ClawHub
# Run this AFTER: clawhub login (or clawhub login --token YOUR_TOKEN)

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
BUNDLE_DIR="/tmp/tolstoy-mcp-skill"

echo "Preparing bundle from $SKILL_DIR..."
rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"
cp -r "$SKILL_DIR"/* "$BUNDLE_DIR"/
rm -rf "$BUNDLE_DIR/node_modules" 2>/dev/null || true

echo "Publishing to ClawHub..."
clawhub publish "$BUNDLE_DIR" \
  --slug tolstoy-mcp \
  --name "Tolstoy MCP" \
  --version 1.0.0 \
  --changelog "Initial release - connect OpenClaw to Tolstoy's video commerce platform"

echo "Done. Check https://clawhub.ai for the skill."
