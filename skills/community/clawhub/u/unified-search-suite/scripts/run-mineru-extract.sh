#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PY="$SKILL_DIR/.venv/bin/python"
TARGET="$SKILL_DIR/vendor/openclaw-search-skills/mineru-extract/scripts/mineru_extract.py"
ENV_LOADER="$SCRIPT_DIR/load-search-env.sh"

if [[ ! -x "$VENV_PY" ]]; then
  echo "[ERROR] unified-search venv python not found: $VENV_PY" >&2
  exit 1
fi
if [[ ! -f "$TARGET" ]]; then
  echo "[ERROR] vendored mineru-extract script not found: $TARGET" >&2
  exit 1
fi

[[ -f "$ENV_LOADER" ]] && source "$ENV_LOADER"
exec "$VENV_PY" "$TARGET" "$@"
