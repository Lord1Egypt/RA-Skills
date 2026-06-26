#!/usr/bin/env bash
set -euo pipefail

SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$SKILL_DIR/assets/sage-template"

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "[ERROR] Template directory not found: $TEMPLATE_DIR" >&2
  exit 1
fi

if [ -d "$SAGE_HOME" ]; then
  echo "[OK] $SAGE_HOME already exists. No files overwritten."
  exit 0
fi

mkdir -p "$SAGE_HOME"
cp -R "$TEMPLATE_DIR"/. "$SAGE_HOME"/

TODAY="$(date +%Y-%m-%d)"
if [ -f "$SAGE_HOME/MANIFEST.yaml" ]; then
  sed -i.bak "s/last_updated: \"YYYY-MM-DD\"/last_updated: \"$TODAY\"/" "$SAGE_HOME/MANIFEST.yaml" && rm -f "$SAGE_HOME/MANIFEST.yaml.bak"
fi
if [ -f "$SAGE_HOME/INDEX.md" ]; then
  perl -0pi -e 's/`YYYY-MM-DD`：初始化/`'"$TODAY"'`：初始化/' "$SAGE_HOME/INDEX.md"
fi

echo "[OK] Initialized Sage company DNA at $SAGE_HOME"
echo "[NEXT] Open ~/.sage/INDEX.md, run ensure_growth_extension.sh, then use Sage CGO onboarding."
