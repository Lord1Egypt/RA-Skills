#!/usr/bin/env bash
set -euo pipefail

MCP_BIN="${XHS_MCP_BIN:-xiaohongshu-mcp}"
PORT="${XHS_MCP_PORT:-18060}"
HEADLESS="${XHS_MCP_HEADLESS:-true}"
FORCE_RESTART="${XHS_MCP_FORCE_RESTART:-0}"
LOG_DIR="${XHS_MCP_LOG_DIR:-$HOME/.openclaw/logs}"
LOG_FILE="$LOG_DIR/xiaohongshu-mcp-server.log"
STATE_DIR="${XHS_MCP_STATE_DIR:-$HOME/.openclaw/state/xiaohongshu-mcp}"
PID_FILE="$STATE_DIR/server.pid"
START_TIMEOUT="${XHS_MCP_START_TIMEOUT:-20}"
ALLOW_KILL_OTHER="${XHS_MCP_ALLOW_KILL_OTHER:-0}"
HOST="${XHS_MCP_HOST:-127.0.0.1}"

case "$HEADLESS" in
  true|false) ;;
  *)
    echo "[ERROR] XHS_MCP_HEADLESS must be true or false (got: $HEADLESS)"
    exit 1
    ;;
esac

case "$START_TIMEOUT" in
  ''|*[!0-9]*)
    START_TIMEOUT=20
    ;;
esac

is_windows_shell() {
  case "$(uname -s 2>/dev/null | tr '[:upper:]' '[:lower:]')" in
    *mingw*|*msys*|*cygwin*) return 0 ;;
    *) return 1 ;;
  esac
}

port_open() {
  python3 - "$HOST" "$PORT" <<'PY'
import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.6)
try:
    sock.connect((host, port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
raise SystemExit(0)
PY
}

pid_from_port() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -tiTCP:"$PORT" -sTCP:LISTEN | head -n 1 || true
    return 0
  fi
  if [ -f "$PID_FILE" ]; then
    sed -n '1p' "$PID_FILE" 2>/dev/null | tr -d '[:space:]'
  fi
}

cmdline_by_pid() {
  local pid="$1"
  if [ -z "$pid" ]; then
    return 0
  fi
  if command -v ps >/dev/null 2>&1; then
    ps -p "$pid" -o command= 2>/dev/null || true
  fi
}

is_expected_process() {
  local cmd="$1"
  local bin_name
  bin_name="$(basename "$MCP_BIN")"
  if echo "$cmd" | grep -q "$bin_name"; then
    return 0
  fi
  if echo "$cmd" | grep -q "xiaohongshu-mcp"; then
    return 0
  fi
  return 1
}

if ! command -v "$MCP_BIN" >/dev/null 2>&1; then
  if [ -x "$HOME/go/bin/$MCP_BIN" ]; then
    MCP_BIN="$HOME/go/bin/$MCP_BIN"
  else
    echo "[ERROR] $MCP_BIN is not found in PATH or \$HOME/go/bin"
    echo "Run setup first: bash $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/setup.sh"
    exit 1
  fi
fi

if is_windows_shell; then
  echo "[ERROR] This script targets Linux/macOS shells. On Windows, run in WSL or Git Bash."
  exit 1
fi

mkdir -p "$LOG_DIR"
mkdir -p "$STATE_DIR"

if port_open; then
  RUNNING_PID="$(pid_from_port)"
  RUNNING_CMD=""
  if [ -n "$RUNNING_PID" ]; then
    RUNNING_CMD="$(cmdline_by_pid "$RUNNING_PID")"
  fi

  if [ "$FORCE_RESTART" = "1" ]; then
    if [ -n "$RUNNING_PID" ]; then
      if [ -n "$RUNNING_CMD" ] && ! is_expected_process "$RUNNING_CMD" && [ "$ALLOW_KILL_OTHER" != "1" ]; then
        echo "[ERROR] Port :$PORT is occupied by a different process (pid=$RUNNING_PID)."
        echo "[ERROR] Refusing to kill it automatically."
        echo "[INFO] Process: $RUNNING_CMD"
        echo "[INFO] If you are sure, rerun with XHS_MCP_ALLOW_KILL_OTHER=1"
        exit 1
      fi
      echo "[INFO] Port :$PORT is occupied (pid=$RUNNING_PID), force restarting..."
      kill "$RUNNING_PID" >/dev/null 2>&1 || true
      sleep 1
    elif [ "$ALLOW_KILL_OTHER" != "1" ]; then
      echo "[ERROR] Port :$PORT is occupied but PID is unknown (lsof unavailable)."
      echo "[INFO] Install lsof or stop the process manually, then rerun."
      exit 1
    fi

    if port_open; then
      echo "[ERROR] Port :$PORT is still occupied after restart attempt."
      echo "[INFO] Stop the conflicting process manually and retry."
      exit 1
    fi
  else
    if [ -n "$RUNNING_CMD" ]; then
      if [ "$HEADLESS" = "true" ] && echo "$RUNNING_CMD" | grep -q -- "-headless=false"; then
        echo "[WARN] Existing process runs with headless=false (will pop browser windows)."
        echo "[INFO] To switch to headless mode:"
        echo "       XHS_MCP_FORCE_RESTART=1 XHS_MCP_HEADLESS=true bash $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/start_server.sh"
      fi
      if [ "$HEADLESS" = "false" ] && echo "$RUNNING_CMD" | grep -q -- "-headless=true"; then
        echo "[WARN] Existing process runs with headless=true."
      fi
    fi
    echo "[OK] xiaohongshu-mcp already listening on :$PORT"
    echo "[INFO] MCP endpoint: http://$HOST:$PORT/mcp"
    echo "[INFO] State dir: $STATE_DIR"
    exit 0
  fi
fi

echo "[INFO] Starting xiaohongshu-mcp on :$PORT (headless=$HEADLESS)"
echo "[INFO] State dir: $STATE_DIR"
(
  cd "$STATE_DIR"
  nohup "$MCP_BIN" -headless="$HEADLESS" -port ":$PORT" >"$LOG_FILE" 2>&1 &
  echo "$!" > "$PID_FILE"
)

for _ in $(seq 1 "$START_TIMEOUT"); do
  if port_open; then
    break
  fi
  sleep 1
done

if port_open; then
  echo "[OK] xiaohongshu-mcp started"
  echo "[INFO] MCP endpoint: http://$HOST:$PORT/mcp"
  echo "[INFO] Log file: $LOG_FILE"
  if [ -f "$PID_FILE" ]; then
    echo "[INFO] PID file: $PID_FILE ($(cat "$PID_FILE" 2>/dev/null || true))"
  fi
else
  echo "[ERROR] start failed, see log: $LOG_FILE"
  tail -n 60 "$LOG_FILE" || true
  exit 1
fi
