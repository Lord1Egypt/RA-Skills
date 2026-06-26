#!/bin/zsh
set -euo pipefail

SKILL_DIR="$(cd -- "$(dirname -- "$0")/.." && pwd)"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$(cd -- "$SKILL_DIR/../.." && pwd)}"
VENV_DIR="${OPENCLAW_SONOS_VENV:-$HOME/.openclaw/venvs/soco-sonos}"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"
WRAPPER="${OPENCLAW_SONOS_WRAPPER:-$WORKSPACE_DIR/scripts/sonos_netease_play.sh}"
SCRIPT_PY="${OPENCLAW_SONOS_SCRIPT:-$WORKSPACE_DIR/scripts/sonos_netease_play.py}"

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
if [ ! -f "$SCRIPT_PY" ]; then
  echo "ERROR: missing playback script: $SCRIPT_PY" >&2
  echo "Restore or provide a playback implementation at workspace/scripts/sonos_netease_play.py, or override it with OPENCLAW_SONOS_SCRIPT." >&2
  exit 1
fi
if [ ! -f "$WRAPPER" ]; then
  status "wrapper missing, creating a default wrapper"
  mkdir -p "$(dirname -- "$WRAPPER")"
  cat > "$WRAPPER" <<EOF
#!/bin/zsh
set -euo pipefail
exec "$PYTHON_BIN" "$SCRIPT_PY" "\$@"
EOF
fi
if [ ! -x "$WRAPPER" ]; then
  chmod +x "$WRAPPER"
fi

status "environment ready"
"$PYTHON_BIN" -c 'import soco; print("soco", soco.__version__)'
command -v sonos
