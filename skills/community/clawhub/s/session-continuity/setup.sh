#!/bin/bash
# Setup script for session-continuity skill
# Usage: bash setup.sh

set -e

echo "📦 Setting up session-continuity for OpenClaw..."

OPENCLAW_WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$OPENCLAW_WORKSPACE/skills/session-continuity"
CHECKPOINT_DIR="$OPENCLAW_WORKSPACE/memory/checkpoints"

# Determine script's own directory (supports symlinks)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Copy skill files if not already installed
if [ ! -d "$SKILL_DIR" ]; then
    echo "  → Installing skill to $SKILL_DIR"
    cp -r "$SCRIPT_DIR" "$SKILL_DIR"
else
    echo "  → Skill already installed at $SKILL_DIR"
fi

# 2. Create checkpoints directory
if [ ! -d "$CHECKPOINT_DIR" ]; then
    echo "  → Creating checkpoints directory at $CHECKPOINT_DIR"
    mkdir -p "$CHECKPOINT_DIR"
    touch "$CHECKPOINT_DIR/.gitkeep"
else
    echo "  → Checkpoints directory already exists"
fi

# 3. Verify
echo ""
echo "✅ Setup complete!"
echo ""
echo "Verify:"
echo "  openclaw skills check | grep session-continuity"
echo ""
echo "Quick test:"
echo "  python3 $SKILL_DIR/scripts/checkpoint.py list"
echo ""
echo "Get started:"
echo '  /checkpoint save my-task   # in any OpenClaw conversation'