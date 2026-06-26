#!/usr/bin/env bash
# groove-utilities-task-prime — run task backend prime if configured

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX=".groove/index.md"

if [ ! -f "$INDEX" ]; then
  exit 0
fi

# Extract tasks.backend from frontmatter
backend=$(sed -n '/^---$/,/^---$/p' "$INDEX" | grep 'backend:' | head -1 | sed 's/.*backend:[[:space:]]*//' | tr -d '[:space:]')

if [ -z "$backend" ] || [ "$backend" = "none" ]; then
  exit 0
fi

if [ "$backend" = "beans" ]; then
  if command -v beans &>/dev/null; then
    echo ""
    echo "## Tasks"
    beans prime 2>/dev/null || true
  fi
fi
