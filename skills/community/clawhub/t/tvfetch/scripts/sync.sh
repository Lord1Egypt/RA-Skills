#!/usr/bin/env bash
# Deploy tvfetch skill to all supported AI agent skill directories.
# Usage: bash scripts/sync.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="tvfetch"

echo "Deploying $SKILL_NAME from: $SCRIPT_DIR"
echo ""

# Claude Code
CLAUDE_DIR="$HOME/.claude/skills/$SKILL_NAME"
if [ -d "$HOME/.claude" ]; then
    mkdir -p "$CLAUDE_DIR"
    rsync -a --delete --exclude='__pycache__' --exclude='.git' --exclude='*.egg-info' --exclude='.pytest_cache' "$SCRIPT_DIR/" "$CLAUDE_DIR/" 2>/dev/null || cp -r "$SCRIPT_DIR/." "$CLAUDE_DIR/"
    echo "  Claude Code:  $CLAUDE_DIR"
else
    echo "  Claude Code:  ~/.claude not found (skipped)"
fi

# OpenAI Codex / Agents
for AGENT_DIR in "$HOME/.agents/skills/$SKILL_NAME" "$HOME/.codex/skills/$SKILL_NAME"; do
    PARENT="$(dirname "$(dirname "$AGENT_DIR")")"
    if [ -d "$PARENT" ]; then
        mkdir -p "$AGENT_DIR"
        rsync -a --delete --exclude='__pycache__' --exclude='.git' --exclude='*.egg-info' --exclude='.pytest_cache' "$SCRIPT_DIR/" "$AGENT_DIR/" 2>/dev/null || cp -r "$SCRIPT_DIR/." "$AGENT_DIR/"
        echo "  Codex/Agents: $AGENT_DIR"
    fi
done

# Gemini CLI
GEMINI_DIR="$HOME/.gemini/extensions/$SKILL_NAME"
if [ -d "$HOME/.gemini" ]; then
    mkdir -p "$GEMINI_DIR"
    rsync -a --delete --exclude='__pycache__' --exclude='.git' --exclude='*.egg-info' --exclude='.pytest_cache' "$SCRIPT_DIR/" "$GEMINI_DIR/" 2>/dev/null || cp -r "$SCRIPT_DIR/." "$GEMINI_DIR/"
    echo "  Gemini CLI:   $GEMINI_DIR"
else
    echo "  Gemini CLI:   ~/.gemini not found (skipped)"
fi

echo ""
echo "Done. Restart your AI assistant to pick up changes."
