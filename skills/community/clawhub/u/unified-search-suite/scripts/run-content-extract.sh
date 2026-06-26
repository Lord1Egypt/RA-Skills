#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PY="$SKILL_DIR/.venv/bin/python"
TARGET="$SCRIPT_DIR/local-content-extract.py"
ENV_LOADER="$SCRIPT_DIR/load-search-env.sh"

if [[ ! -x "$VENV_PY" ]]; then
  echo "[ERROR] Python virtualenv not found at $VENV_PY" >&2
  exit 1
fi

if [[ ! -f "$TARGET" ]]; then
  echo "[ERROR] local content extractor not found: $TARGET" >&2
  exit 1
fi

[[ -f "$ENV_LOADER" ]] && source "$ENV_LOADER"
exec "$VENV_PY" "$TARGET" "$@"
