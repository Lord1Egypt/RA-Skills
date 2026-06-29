#!/usr/bin/env bash
# seddo install — universal installer for all agents
# Usage: bash install.sh [agent-type] [bin-dir]
# agent-type: auto (default), claude-code, openclaw, opencode, generic

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT="${1:-auto}"
BIN_DIR="${2:-/usr/local/bin}"

detect_agent() {
  if command -v openclaw &>/dev/null; then
    echo "openclaw"
  elif [[ -d "$HOME/.claude" ]]; then
    echo "claude-code"
  elif [[ -d "$HOME/.opencode" ]]; then
    echo "opencode"
  else
    echo "generic"
  fi
}

[[ "$AGENT" == "auto" ]] && AGENT=$(detect_agent)

case "$AGENT" in
  openclaw)   DEST="$HOME/.openclaw/workspace/skills/seddo" ;;
  claude-code) DEST="$HOME/.claude/skills/seddo" ;;
  opencode)   DEST="$HOME/.opencode/skills/seddo" ;;
  *)          DEST="$HOME/.local/share/seddo" ;;
esac

echo "🤝 Seddo Installer"
echo "   Agent detected: ${AGENT}"
echo "   Install path:   ${DEST}"
echo ""

mkdir -p "$DEST/scripts" "$DEST/templates"

cp "$REPO_DIR/SKILL.md" "$DEST/"
cp "$REPO_DIR/scripts/seddo.sh" "$DEST/scripts/"
chmod +x "$DEST/scripts/seddo.sh"
cp "$REPO_DIR/templates/"*.md "$DEST/templates/"

echo "✅ Files installed to ${DEST}"

# Symlink to PATH
if [[ -w "$BIN_DIR" ]]; then
  ln -sf "$DEST/scripts/seddo.sh" "$BIN_DIR/seddo"
  echo "✅ Symlink: ${BIN_DIR}/seddo → ${DEST}/scripts/seddo.sh"
else
  echo ""
  echo "⚠️  Cannot write to ${BIN_DIR} (no sudo). Choose one:"
  echo ""
  echo "   Option A — sudo symlink:"
  echo "   sudo ln -sf ${DEST}/scripts/seddo.sh ${BIN_DIR}/seddo"
  echo ""
  echo "   Option B — user bin (no sudo):"
  mkdir -p "$HOME/.local/bin"
  ln -sf "$DEST/scripts/seddo.sh" "$HOME/.local/bin/seddo"
  echo "   ✅ Symlink created: ~/.local/bin/seddo"
  echo "   Add to your shell if not already:"
  echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Agent-specific post-install instructions
echo ""
case "$AGENT" in
  claude-code)
    echo "📋 Claude Code — add to your project CLAUDE.md:"
    echo ""
    echo "   ## Seddo"
    echo "   SWARM_GIST_ID=<your-gist-id>   # set after 'seddo init'"
    echo "   SEDDO_AGENT=claude-code"
    echo ""
    echo "   At conversation start involving shared work:"
    echo "   1. Run: seddo sync"
    echo "   2. Run: seddo inbox"
    echo "   3. Run: seddo tasks"
    echo "   Then act on relevant messages/tasks and update the gist."
    ;;
  openclaw)
    echo "✅ OpenClaw: skill auto-loaded from ${DEST}"
    ;;
  opencode)
    echo "📋 OpenCode — add SWARM_GIST_ID to your agent config or .env"
    ;;
  *)
    echo "📋 Generic — add to your agent's system prompt or config:"
    echo "   SWARM_GIST_ID=<your-gist-id>"
    echo "   SEDDO_AGENT=<your-agent-name>"
    ;;
esac

echo ""
echo "🔍 Running doctor check..."
echo ""
bash "$DEST/scripts/seddo.sh" doctor || true

echo ""
echo "🤝 Done! Run 'seddo init' to create your first seddo."
