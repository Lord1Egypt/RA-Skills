#!/bin/bash
set -e

SKILL_DIR="$HOME/.claude/skills/unsplash"

echo "Installing Unsplash skill to $SKILL_DIR"

# Create directory
mkdir -p "$SKILL_DIR"

# Copy files
cp SKILL.md "$SKILL_DIR/"
cp -r scripts "$SKILL_DIR/"
cp -r examples "$SKILL_DIR/"
cp .env.example "$SKILL_DIR/"

# Make scripts executable
chmod +x "$SKILL_DIR/scripts"/*.sh

echo "✓ Installed successfully"
echo ""
echo "Next steps:"
echo "1. Get your free API key from https://unsplash.com/developers"
echo "2. Create .env in your project root with: UNSPLASH_ACCESS_KEY=your_key"
echo "3. Test with: /unsplash sunset"
echo ""
echo "Note: Add the export to ~/.zshrc or ~/.bash_profile to persist across sessions"
