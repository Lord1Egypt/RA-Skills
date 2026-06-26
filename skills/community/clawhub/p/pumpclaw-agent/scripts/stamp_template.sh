#!/usr/bin/env bash
set -euo pipefail

# Stamp the template into a new project folder.
# Usage:
#   ./scripts/stamp_template.sh <project-slug> [dest-dir]
# Example:
#   ./scripts/stamp_template.sh acme-bot /tmp

SLUG=${1:-}
DEST_DIR=${2:-.}

if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <project-slug> [dest-dir]" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$SKILL_DIR/assets/template"
OUT_DIR="$DEST_DIR/$SLUG"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template not found: $TEMPLATE_DIR" >&2
  exit 1
fi

if [[ -e "$OUT_DIR" ]]; then
  echo "Destination already exists: $OUT_DIR" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# tar copy keeps permissions and avoids needing rsync
( cd "$TEMPLATE_DIR" && tar -cf - . ) | ( cd "$OUT_DIR" && tar -xf - )

# Remove common local state if it slipped in
rm -f "$OUT_DIR"/*.log "$OUT_DIR"/*.pid "$OUT_DIR"/demo.db "$OUT_DIR"/.env "$OUT_DIR"/.env.local 2>/dev/null || true

echo "Stamped template to: $OUT_DIR"
echo "Next: cd '$OUT_DIR' && npm install"
