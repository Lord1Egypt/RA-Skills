#!/usr/bin/env bash
# wip-ldm-os/bin/scaffold.sh
# Scaffolds ~/.ldm/agents/cc/ for Claude Code.
# Idempotent: skips existing files, never overwrites.

set -euo pipefail

LDM_HOME="${HOME}/.ldm"
CC_HOME="${LDM_HOME}/agents/cc"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATES="${SCRIPT_DIR}/templates/cc"

# Resolve workspace from LDM config or default
WORKSPACE=$(python3 -c "import json; print(json.load(open('$HOME/.ldm/config.json')).get('workspace','$HOME/wipcomputerinc'))" 2>/dev/null || echo "$HOME/wipcomputerinc")

# Existing soul files (now under workspace/team/cc-mini/)
CC_DOCS="${WORKSPACE}/team/cc-mini/documents"
CC_SOUL="${CC_DOCS}/cc-soul"

echo "=== LDM OS Scaffold ==="
echo "Target: ${LDM_HOME}"
echo ""

# Create directory tree
dirs=(
  "${CC_HOME}/memory/daily"
  "${CC_HOME}/memory/journals"
  "${LDM_HOME}/shared/dream-weaver"
  "${LDM_HOME}/shared/boot"
  "${LDM_HOME}/bin"
)

for dir in "${dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    echo "  created: ${dir#$HOME/}"
  fi
done

# Copy file only if target doesn't exist
safe_copy() {
  local src="$1"
  local dst="$2"
  local label="$3"
  if [ ! -f "$dst" ]; then
    if [ -f "$src" ]; then
      cp "$src" "$dst"
      echo "  copied:  ${label}"
    else
      echo "  MISSING: ${src} (skipping ${label})"
    fi
  else
    echo "  exists:  ${label} (skipped)"
  fi
}

# Write file only if target doesn't exist
safe_write() {
  local dst="$1"
  local src="$2"
  local label="$3"
  if [ ! -f "$dst" ]; then
    cp "$src" "$dst"
    echo "  seeded:  ${label}"
  else
    echo "  exists:  ${label} (skipped)"
  fi
}

echo ""
echo "--- Agent: cc ---"

# Soul files from existing cc-soul directory
safe_copy "${CC_SOUL}/IDENTITY.md" "${CC_HOME}/IDENTITY.md" "IDENTITY.md"
safe_copy "${CC_SOUL}/SOUL.md" "${CC_HOME}/SOUL.md" "SOUL.md"

# Template files
safe_write "${CC_HOME}/CONTEXT.md" "${TEMPLATES}/CONTEXT.md" "CONTEXT.md"
safe_write "${CC_HOME}/REFERENCE.md" "${TEMPLATES}/REFERENCE.md" "REFERENCE.md"
safe_write "${CC_HOME}/config.json" "${TEMPLATES}/config.json" "config.json"

# Global config
safe_write "${LDM_HOME}/config.json" "${SCRIPT_DIR}/templates/config.json" "global config.json"

# Copy existing journals
if [ -d "${CC_DOCS}/journals" ]; then
  echo ""
  echo "--- Copying existing journals ---"
  for journal in "${CC_DOCS}/journals/"*.md; do
    [ -f "$journal" ] || continue
    name="$(basename "$journal")"
    safe_copy "$journal" "${CC_HOME}/memory/journals/${name}" "journals/${name}"
  done
fi

echo ""
echo "=== Scaffold complete ==="
echo "Home: ${CC_HOME}"
echo ""
echo "Next: populate CONTEXT.md with current state"
