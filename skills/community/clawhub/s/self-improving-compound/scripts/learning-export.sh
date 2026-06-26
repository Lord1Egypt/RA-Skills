#!/usr/bin/env bash
set -euo pipefail
ROOT="${OPENCLAW_WORKSPACE:-$PWD}"
LEARNING_ROOT="${SELF_IMPROVING_LEARNING_ROOT:-${SELF_IMPROVING_LEARNING_DIR:-$ROOT/learning}}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="${SELF_IMPROVING_SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
LEARNINGS_CLI="${SELF_IMPROVING_LEARNINGS_CLI:-$SKILL_DIR/scripts/learnings.py}"
OUT="$LEARNING_ROOT/memory-export.md"
mkdir -p "$LEARNING_ROOT"
python3 "$LEARNINGS_CLI" --root "$ROOT" export --output "$OUT"
python3 "$LEARNINGS_CLI" --root "$ROOT" status --format json > "$LEARNING_ROOT/status.json"
echo "[learning-export] wrote $OUT"
