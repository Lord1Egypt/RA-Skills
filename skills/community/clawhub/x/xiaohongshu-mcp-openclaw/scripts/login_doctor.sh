#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_NAME="${1:-xiaohongshu-mcp}"
PORT="${XHS_MCP_PORT:-18060}"
LOG_FILE="${XHS_MCP_LOG_DIR:-$HOME/.openclaw/logs}/xiaohongshu-mcp-server.log"
STATE_DIR="${XHS_MCP_STATE_DIR:-$HOME/.openclaw/state/xiaohongshu-mcp}"
PID_FILE="$STATE_DIR/server.pid"

section() {
  echo
  echo "========== $1 =========="
}

section "Skill"
echo "base_dir: $BASE_DIR"
echo "server: $SERVER_NAME"
echo "port: $PORT"
echo "state_dir: $STATE_DIR"
echo "pid_file: $PID_FILE"

section "Dependencies"
for bin in python3 jq mcporter lsof; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "[OK] $bin: $(command -v "$bin")"
  else
    echo "[MISS] $bin"
  fi
done

section "Port & Process"
if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  lsof -iTCP:"$PORT" -sTCP:LISTEN | sed -n '1,8p'
  PID="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN | head -n 1 || true)"
  if [ -n "$PID" ] && command -v ps >/dev/null 2>&1; then
    echo "process_command:"
    ps -p "$PID" -o command=
  fi
elif [ -f "$PID_FILE" ]; then
  PID="$(sed -n '1p' "$PID_FILE" 2>/dev/null | tr -d '[:space:]')"
  echo "[WARN] lsof unavailable or no listener detected; fallback PID file: $PID"
  if [ -n "${PID:-}" ] && command -v ps >/dev/null 2>&1; then
    echo "process_command:"
    ps -p "$PID" -o command= || true
  fi
else
  echo "[WARN] no listener on :$PORT"
fi

section "Mcporter Config"
if mcporter config get "$SERVER_NAME" --json >/tmp/xhs_doctor_cfg.json 2>/tmp/xhs_doctor_cfg.err; then
  cat /tmp/xhs_doctor_cfg.json
else
  echo "[WARN] failed to read mcporter config"
  cat /tmp/xhs_doctor_cfg.err || true
fi

section "Tool Discovery"
if python3 "$BASE_DIR/scripts/xhs_mcp_client.py" --server "$SERVER_NAME" --timeout 20000 tools >/tmp/xhs_doctor_tools.json 2>/tmp/xhs_doctor_tools.err; then
  jq '.tools | length as $n | {tool_count:$n, first_tools:(.[0:8]|map(.name))}' /tmp/xhs_doctor_tools.json
else
  echo "[WARN] tool discovery failed"
  cat /tmp/xhs_doctor_tools.err || true
fi

section "Login Status"
if python3 "$BASE_DIR/scripts/xhs_mcp_client.py" --server "$SERVER_NAME" --timeout 20000 ensure-login --no-qrcode >/tmp/xhs_doctor_login.json 2>/tmp/xhs_doctor_login.err; then
  cat /tmp/xhs_doctor_login.json
else
  echo "[WARN] ensure-login failed"
  cat /tmp/xhs_doctor_login.err || true
fi

section "Recent Log"
if [ -f "$LOG_FILE" ]; then
  tail -n 80 "$LOG_FILE"
else
  echo "[WARN] log file not found: $LOG_FILE"
fi

section "Suggested Fix"
echo "1) Preflight: bash $BASE_DIR/scripts/preflight.sh"
echo "2) Start server: bash $BASE_DIR/scripts/start_server.sh"
echo "3) Register server: bash $BASE_DIR/scripts/register.sh $SERVER_NAME"
echo "4) Login flow: bash $BASE_DIR/scripts/login_flow.sh $SERVER_NAME 120"
echo "5) Verify: STRICT=1 bash $BASE_DIR/scripts/smoke_test.sh $SERVER_NAME"
echo "6) Optional keepalive service: bash $BASE_DIR/scripts/service_install.sh $SERVER_NAME"
