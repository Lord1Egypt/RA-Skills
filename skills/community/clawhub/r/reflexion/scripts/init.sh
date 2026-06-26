#!/usr/bin/env bash
# reflexion/scripts/init.sh
# Initialize the .reflexion/ directory structure.
# Safe to run multiple times -- never overwrites existing data.
set -euo pipefail

# Resolve project root: prefer CLAUDE_PROJECT_ROOT, fall back to git root, then cwd
PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"

mkdir -p "$REFLEX_DIR/entries"

# Create keyword index if missing
[ -f "$REFLEX_DIR/index.txt" ] || touch "$REFLEX_DIR/index.txt"

# Create stats file if missing
if [ ! -f "$REFLEX_DIR/stats.json" ]; then
  cat > "$REFLEX_DIR/stats.json" << 'EOF'
{
  "total_captured": 0,
  "total_recalled": 0,
  "total_promoted": 0,
  "last_capture": null,
  "last_recall": null,
  "last_promotion": null
}
EOF
fi

# Suggest .gitignore entry (don't auto-modify)
if [ -f "$PROJECT_ROOT/.gitignore" ]; then
  if ! grep -qF '.reflexion/' "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
    echo "[reflexion] Consider adding '.reflexion/' to .gitignore for private projects."
  fi
fi
