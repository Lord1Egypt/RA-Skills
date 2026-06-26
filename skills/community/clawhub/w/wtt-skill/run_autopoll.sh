#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="${WTT_SKILL_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
cd "$SKILL_DIR"

is_py_ready() {
  local py="$1"
  [[ -x "$py" ]] || return 1
  "$py" - <<'PY' >/dev/null 2>&1
import importlib.util, sys
req = ("httpx", "websockets", "dotenv", "socksio")
missing = [m for m in req if importlib.util.find_spec(m) is None]
sys.exit(0 if not missing else 1)
PY
}

choose_py() {
  local c

  # Even when WTT_PY_BIN is set by systemd, verify deps before using it.
  if [[ -n "${WTT_PY_BIN:-}" ]] && is_py_ready "${WTT_PY_BIN}"; then
    echo "${WTT_PY_BIN}"
    return 0
  fi

  local candidates=(
    "$SKILL_DIR/.venv/bin/python"
    "$SKILL_DIR/.venv311/bin/python"
    "$HOME/.openclaw/workspace/skills/.venv311/bin/python"
    "$(command -v python3 || true)"
  )

  for c in "${candidates[@]}"; do
    if [[ -n "$c" ]] && is_py_ready "$c"; then
      echo "$c"
      return 0
    fi
  done

  # Last resort: keep previous behavior (will fail fast with clear error)
  if [[ -n "${WTT_PY_BIN:-}" ]] && [[ -x "${WTT_PY_BIN}" ]]; then
    echo "${WTT_PY_BIN}"
    return 0
  fi
  command -v python3
}

PY="$(choose_py)"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  echo "❌ No runnable python found for wtt autopoll"
  exit 1
fi

if ! is_py_ready "$PY"; then
  echo "❌ Python missing required deps (httpx/websockets/python-dotenv/socksio): $PY"
  exit 1
fi

exec "$PY" "$SKILL_DIR/start_wtt_autopoll.py"
