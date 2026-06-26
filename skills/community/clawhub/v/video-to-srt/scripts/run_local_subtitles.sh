#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

VENV_DIR="${VENV_DIR:-$SKILL_DIR/.venv}"
CACHE_ROOT="${CACHE_ROOT:-$SKILL_DIR/.cache}"
HF_HOME_DIR="${HF_HOME:-$CACHE_ROOT/hf}"
XDG_CACHE_HOME_DIR="${XDG_CACHE_HOME:-$CACHE_ROOT/xdg}"
PY_CACHE_DIR="${PYTHONPYCACHEPREFIX:-${PY_CACHE:-$SKILL_DIR/.pycache}}"

mkdir -p "$CACHE_ROOT" "$HF_HOME_DIR" "$XDG_CACHE_HOME_DIR" "$PY_CACHE_DIR"

if [ ! -x "$VENV_DIR/bin/python3" ]; then
  python3 -m venv "$VENV_DIR"
fi

if ! "$VENV_DIR/bin/python3" -c "import faster_whisper" >/dev/null 2>&1; then
  "$VENV_DIR/bin/python3" -m pip install -U pip >/dev/null
  "$VENV_DIR/bin/python3" -m pip install -r "$SCRIPT_DIR/requirements.txt" >/dev/null
fi

env \
  PYTHONPYCACHEPREFIX="$PY_CACHE_DIR" \
  HF_HOME="$HF_HOME_DIR" \
  XDG_CACHE_HOME="$XDG_CACHE_HOME_DIR" \
  HF_HUB_DISABLE_XET=1 \
  "$VENV_DIR/bin/python3" "$SCRIPT_DIR/transcribe_to_srt.py" "$@"
