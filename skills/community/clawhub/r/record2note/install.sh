#!/bin/bash
set -euo pipefail

# Install to the shared path ~/.config/record2note/
# If your agent uses a custom skill directory (for example Codex CLI or Claude),
# copy the files there after installation:
#   cp -r ~/.config/record2note/* ~/.codex/skills/record2note/

SKILL_NAME="record2note"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.config/$SKILL_NAME"

echo "=== Installing $SKILL_NAME skill ==="

# Create install directory
mkdir -p "$INSTALL_DIR"

# Copy files (excluding config.json, which is user-specific)
cp "$SRC_DIR/SKILL.md" "$INSTALL_DIR/"
cp "$SRC_DIR/config.example.json" "$INSTALL_DIR/"
cp -r "$SRC_DIR/scripts" "$INSTALL_DIR/"
cp -r "$SRC_DIR/templates" "$INSTALL_DIR/"

# Copy .gitignore if it exists
cp "$SRC_DIR/.gitignore" "$INSTALL_DIR/" 2>/dev/null || true

# Set execute permissions
chmod +x "$INSTALL_DIR/scripts/macos/"*.sh 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts/common/"*.py 2>/dev/null || true

echo ""
echo "=== Install complete ==="
echo "Skill installed to: $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "1. Tell your AI Agent: 'Use record2note'"
echo "2. Agent will guide you through setup"
