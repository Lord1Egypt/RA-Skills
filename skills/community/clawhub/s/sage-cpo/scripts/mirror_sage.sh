#!/usr/bin/env bash
set -euo pipefail

SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
TARGET="${1:-sage-mirror}"

if [ ! -d "$SAGE_HOME" ]; then
  echo "[MISSING] $SAGE_HOME does not exist. Run init_sage.sh first." >&2
  exit 1
fi

if [ -e "$TARGET" ]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  BACKUP="${TARGET}.backup-${TS}"
  mv "$TARGET" "$BACKUP"
  echo "[INFO] Existing $TARGET moved to $BACKUP"
fi

mkdir -p "$TARGET"
cp -R "$SAGE_HOME"/. "$TARGET"/

cat > "$TARGET/README.md" <<'EOF'
# Sage DNA Mirror

This folder is a read-only workspace mirror of `~/.sage`, created for convenient browsing.

Rules:

- `~/.sage` remains the source of truth.
- Do not edit this mirror expecting changes to sync back automatically.
- If you want to update company DNA, update `~/.sage` through Sage COO.
EOF

echo "[OK] Mirrored $SAGE_HOME to $TARGET"
echo "[NOTE] This is a read-only browsing mirror. Source of truth remains $SAGE_HOME"
