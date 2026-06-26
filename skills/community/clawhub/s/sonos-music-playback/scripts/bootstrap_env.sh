#!/bin/zsh
set -euo pipefail

SKILL_DIR="$(cd -- "$(dirname -- "$0")/.." && pwd)"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$(cd -- "$SKILL_DIR/../.." && pwd)}"
VENV_DIR="${OPENCLAW_SONOS_VENV:-$HOME/.openclaw/venvs/soco-sonos}"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"
NETEASE_WRAPPER="${OPENCLAW_SONOS_NETEASE_WRAPPER:-$WORKSPACE_DIR/scripts/sonos_netease_play.sh}"
QQ_WRAPPER="${OPENCLAW_SONOS_QQ_WRAPPER:-$WORKSPACE_DIR/scripts/sonos_qq_play.sh}"
NETEASE_SCRIPT="${OPENCLAW_SONOS_NETEASE_SCRIPT:-$WORKSPACE_DIR/scripts/sonos_netease_play.py}"
QQ_SCRIPT="${OPENCLAW_SONOS_QQ_SCRIPT:-$WORKSPACE_DIR/scripts/sonos_qq_play.py}"

status() {
  echo "[sonos-bootstrap] $*"
}

status "skill_dir=$SKILL_DIR"
status "workspace_dir=$WORKSPACE_DIR"
status "venv_dir=$VENV_DIR"

status "checking sonos CLI"
if ! command -v sonos >/dev/null 2>&1; then
  echo "ERROR: sonos CLI not found in PATH" >&2
  echo "Install or restore the sonos CLI first, then rerun bootstrap." >&2
  exit 1
fi

status "ensuring venv exists"
if [ ! -x "$PYTHON_BIN" ]; then
  python3 -m venv "$VENV_DIR"
fi

status "ensuring pip exists"
"$PYTHON_BIN" -m ensurepip --upgrade >/dev/null 2>&1 || true

status "ensuring soco is installed"
if ! "$PYTHON_BIN" -c 'import soco' >/dev/null 2>&1; then
  "$PIP_BIN" install --upgrade pip soco
fi

status "checking playback entrypoints"
if [ ! -f "$NETEASE_SCRIPT" ]; then
  echo "ERROR: missing playback script: $NETEASE_SCRIPT" >&2
  exit 1
fi
if [ ! -f "$QQ_SCRIPT" ]; then
  echo "ERROR: missing playback script: $QQ_SCRIPT" >&2
  exit 1
fi
if [ ! -f "$NETEASE_WRAPPER" ]; then
  echo "ERROR: missing playback wrapper: $NETEASE_WRAPPER" >&2
  exit 1
fi
if [ ! -f "$QQ_WRAPPER" ]; then
  echo "ERROR: missing playback wrapper: $QQ_WRAPPER" >&2
  exit 1
fi
if [ ! -x "$NETEASE_WRAPPER" ]; then
  chmod +x "$NETEASE_WRAPPER"
fi
if [ ! -x "$QQ_WRAPPER" ]; then
  chmod +x "$QQ_WRAPPER"
fi

status "environment ready"
"$PYTHON_BIN" -c 'import soco; print("soco", soco.__version__)'
command -v sonos
