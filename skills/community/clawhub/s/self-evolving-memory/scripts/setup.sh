#!/usr/bin/env bash
# memory-orchestrator setup script
# Usage: bash scripts/setup.sh [workspace-path]
# Example: bash scripts/setup.sh ~/.openclaw/workspace-myagent

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── Resolve workspace path ────────────────────────────────────────────────────
if [ -n "$1" ]; then
  WORKSPACE="$1"
else
  # Try to auto-detect OpenClaw workspace
  if [ -d ~/.openclaw ]; then
    # List available workspaces
    WORKSPACES=($(ls -d ~/.openclaw/workspace-* 2>/dev/null))
    if [ ${#WORKSPACES[@]} -eq 1 ]; then
      WORKSPACE="${WORKSPACES[0]}"
      echo "Auto-detected workspace: $WORKSPACE"
    elif [ ${#WORKSPACES[@]} -gt 1 ]; then
      echo "Multiple workspaces found:"
      for i in "${!WORKSPACES[@]}"; do
        echo "  [$i] ${WORKSPACES[$i]}"
      done
      read -r -p "Enter workspace number: " idx
      WORKSPACE="${WORKSPACES[$idx]}"
    else
      read -r -p "Enter workspace path: " WORKSPACE
    fi
  else
    read -r -p "Enter workspace path: " WORKSPACE
  fi
fi

WORKSPACE="${WORKSPACE/#\~/$HOME}"

if [ ! -d "$WORKSPACE" ]; then
  echo "Error: Workspace not found: $WORKSPACE"
  echo "Please create it first or provide a valid path."
  exit 1
fi

echo ""
echo "Setting up memory system in: $WORKSPACE"
echo ""

# ── Helper ────────────────────────────────────────────────────────────────────
copy_template() {
  local src="$SKILL_DIR/templates/$1"
  local dst="$WORKSPACE/$1"
  if [ -f "$dst" ]; then
    echo "  ⚠️  Skipping (already exists): $1"
  else
    cp "$src" "$dst"
    echo "  ✅  Created: $1"
  fi
}

# ── Create memory directory ───────────────────────────────────────────────────
mkdir -p "$WORKSPACE/memory"

# ── Copy templates ────────────────────────────────────────────────────────────
echo "📁 Copying memory file templates..."
copy_template "SESSION-STATE.md"
copy_template "MEMORY.md"
copy_template "HEARTBEAT.md"
copy_template "memory/preferences.md"
copy_template "memory/system.md"
copy_template "memory/projects.md"
copy_template "memory/MEMORY.md"

# ── Check agent files ─────────────────────────────────────────────────────────
echo ""
echo "🔍 Checking agent configuration files..."

for f in SOUL.md AGENTS.md TOOLS.md; do
  if [ -f "$WORKSPACE/$f" ]; then
    echo "  ✅  Found: $f"
  else
    echo "  ⚠️  Missing: $f — recommended for full memory discipline"
  fi
done

# ── Check openclaw.json for memorySearch ─────────────────────────────────────
echo ""
echo "🔍 Checking embedding configuration..."

OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"
if [ -f "$OPENCLAW_JSON" ]; then
  if grep -q '"memorySearch"' "$OPENCLAW_JSON"; then
    ENABLED=$(python3 -c "
import json, sys
d = json.load(open('$OPENCLAW_JSON'))
agents = d.get('agents', {})
defaults = agents.get('defaults', {})
ms = defaults.get('memorySearch', {})
print(ms.get('enabled', 'not set'))
" 2>/dev/null || echo "unknown")
    echo "  ✅  memorySearch config found (enabled: $ENABLED)"
  else
    echo "  ⚠️  No memorySearch config found in openclaw.json"
    echo "     → Add embedding config to enable semantic memory search"
    echo "     → See references/embedding-setup.md for options"
  fi
else
  echo "  ⚠️  openclaw.json not found at $OPENCLAW_JSON"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════"
echo "  Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. Review and fill in your memory files:"
echo "     $WORKSPACE/memory/"
echo ""
echo "  2. If embedding is not configured yet:"
echo "     → See references/embedding-setup.md"
echo ""
echo "  3. Add memory discipline to SOUL.md and AGENTS.md:"
echo "     → See references/setup-checklist.md (Step 3)"
echo ""
echo "  4. Verify by asking your agent:"
echo "     'Check my memory system setup'"
echo "══════════════════════════════════════════"
