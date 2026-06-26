#!/bin/zsh
set -euo pipefail

SKILL_DIR="$(cd -- "$(dirname -- "$0")/.." && pwd)"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-$(cd -- "$SKILL_DIR/../.." && pwd)}"
VENV_DIR="${OPENCLAW_SONOS_VENV:-$HOME/.openclaw/venvs/soco-sonos}"
PYTHON_BIN="$VENV_DIR/bin/python"
NETEASE_WRAPPER="${OPENCLAW_SONOS_NETEASE_WRAPPER:-$WORKSPACE_DIR/scripts/sonos_netease_play.sh}"
QQ_WRAPPER="${OPENCLAW_SONOS_QQ_WRAPPER:-$WORKSPACE_DIR/scripts/sonos_qq_play.sh}"

ok=true

echo "skill_dir=$SKILL_DIR"
echo "workspace_dir=$WORKSPACE_DIR"

echo -n "sonos_cli="
if command -v sonos >/dev/null 2>&1; then
  echo "ok:$(command -v sonos)"
else
  echo "missing"
  ok=false
fi

if [ -x "$PYTHON_BIN" ]; then
  echo "venv=ok:$PYTHON_BIN"
  if "$PYTHON_BIN" -c 'import soco' >/dev/null 2>&1; then
    echo "soco=ok"
  else
    echo "soco=missing"
    ok=false
  fi
else
  echo "venv=missing:$VENV_DIR"
  ok=false
fi

if [ -x "$NETEASE_WRAPPER" ]; then
  echo "netease_wrapper=ok:$NETEASE_WRAPPER"
else
  echo "netease_wrapper=missing:$NETEASE_WRAPPER"
  ok=false
fi

if [ -x "$QQ_WRAPPER" ]; then
  echo "qq_wrapper=ok:$QQ_WRAPPER"
else
  echo "qq_wrapper=missing:$QQ_WRAPPER"
  ok=false
fi

if [ "$ok" = true ]; then
  echo "ready=yes"
else
  echo "ready=no"
  exit 1
fi
