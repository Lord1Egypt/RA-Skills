#!/usr/bin/env bash
# God Mode Setup Script
# Initializes the autonomous agent loop in any OpenClaw workspace

set -euo pipefail

WORKSPACE="${1:-.}"

echo "🦅 God Mode — Autonomous Agent Loop Setup"
echo "=========================================="
echo ""

# Check if in an OpenClaw workspace
if [ ! -f "$WORKSPACE/AGENTS.md" ] && [ ! -f "$WORKSPACE/SOUL.md" ]; then
  echo "⚠️  Warning: No AGENTS.md or SOUL.md found. Are you in an OpenClaw workspace?"
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Create TASKS.md if missing
if [ ! -f "$WORKSPACE/TASKS.md" ]; then
  cp "$(dirname "$0")/../references/TASKS-template.md" "$WORKSPACE/TASKS.md"
  echo "✅ Created TASKS.md"
else
  echo "ℹ️  TASKS.md already exists — skipping"
fi

# Create god-mode-state.json in memory/
mkdir -p "$WORKSPACE/memory"
if [ ! -f "$WORKSPACE/memory/god-mode-state.json" ]; then
  cp "$(dirname "$0")/../references/god-mode-state-template.json" "$WORKSPACE/memory/god-mode-state.json"
  echo "✅ Created memory/god-mode-state.json"
else
  echo "ℹ️  memory/god-mode-state.json already exists — skipping"
fi

# Create memory/archive/ directory
mkdir -p "$WORKSPACE/memory/archive"
echo "✅ Ensured memory/archive/ exists"

# Add God Mode reference to HEARTBEAT.md if it exists
if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
  if ! grep -q "God Mode" "$WORKSPACE/HEARTBEAT.md"; then
    echo "" >> "$WORKSPACE/HEARTBEAT.md"
    echo "## God Mode Protocol" >> "$WORKSPACE/HEARTBEAT.md"
    echo "- Read TASKS.md → pick highest-priority unblocked task" >> "$WORKSPACE/HEARTBEAT.md"
    echo "- Execute → log to memory/YYYY-MM-DD.md" >> "$WORKSPACE/HEARTBEAT.md"
    echo "- Update memory/god-mode-state.json" >> "$WORKSPACE/HEARTBEAT.md"
    echo "- Self-audit every cycle" >> "$WORKSPACE/HEARTBEAT.md"
    echo "✅ Updated HEARTBEAT.md with God Mode protocol"
  else
    echo "ℹ️  HEARTBEAT.md already has God Mode reference"
  fi
else
  cp "$(dirname "$0")/../references/HEARTBEAT-template.md" "$WORKSPACE/HEARTBEAT.md"
  echo "✅ Created HEARTBEAT.md from template"
fi

echo ""
echo "🚀 God Mode is installed!"
echo ""
echo "Next steps:"
echo "  1. Edit TASKS.md with your priority queue"
echo "  2. Set heartbeat interval in OpenClaw config (30 min recommended)"
echo "  3. Your agent will now autonomously execute tasks on every heartbeat"
