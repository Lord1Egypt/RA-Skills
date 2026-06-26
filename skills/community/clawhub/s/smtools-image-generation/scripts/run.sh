#!/usr/bin/env bash
# Wrapper: activates the skill's virtualenv and runs generate.py
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$SKILL_DIR/.venv/bin/python3"

if [ ! -f "$VENV_PYTHON" ]; then
    echo '{"status":"error","error":"Virtual environment not found. Run: bash setup.sh"}' >&2
    exit 1
fi

exec "$VENV_PYTHON" "$SKILL_DIR/scripts/generate.py" "$@"
