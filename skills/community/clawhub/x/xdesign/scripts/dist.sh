#!/usr/bin/env bash
# dist.sh
# =========
# Build a clean distributable .skill package for XDesign.
#
# Why this exists (and why we don't just run package_skill.py directly):
# - package_skill.py does not exclude .git, so a build from a live
#   repository ships 200+ KB of git internals (refs, index, objects)
#   and exposes .git/config, .git/logs/HEAD, etc.
# - This script rsyncs a clean tree (no .git) into a staging dir
#   and then invokes the upstream packager.
#
# Usage:
#   ./scripts/dist.sh [output-dir]
#
# Output:
#   <output-dir>/XDesign.skill  (default: ./dist/)

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_ROOT")"
OUT_DIR="${1:-$SKILL_ROOT/dist}"
STAGING="$(mktemp -d -t xdesign-dist)"
trap 'rm -rf "$STAGING"' EXIT

mkdir -p "$OUT_DIR"

echo "[INFO] Staging clean copy at $STAGING"
rsync -a \
  --exclude='.git' \
  --exclude='dist' \
  --exclude='__pycache__' \
  --exclude='.DS_Store' \
  --exclude='*.pyc' \
  "$SKILL_ROOT/" "$STAGING/$SKILL_NAME/"

echo "[INFO] Invoking package_skill.py"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGER="$SCRIPT_DIR/../../skill-creator/scripts/package_skill.py"

if [[ ! -f "$PACKAGER" ]]; then
  echo "[ERR] Cannot locate skill-creator/scripts/package_skill.py at $PACKAGER" >&2
  exit 1
fi

PYPATH="$(cd "$(dirname "$PACKAGER")/.." && pwd)"
PYTHONPATH="$PYPATH" python3 "$PACKAGER" "$STAGING/$SKILL_NAME" "$OUT_DIR"

echo "[OK] Clean package written to $OUT_DIR/$SKILL_NAME.skill"
