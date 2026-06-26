#!/usr/bin/env bash
set -euo pipefail

RAW_SESSION_KEY="${1:-default}"
WAIT_SECONDS="${2:-20}"

SESSION_KEY="$(printf '%s' "$RAW_SESSION_KEY" | tr -cd '[:alnum:]._-' )"
SESSION_KEY="${SESSION_KEY:-default}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

STATE_ROOT="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/weixin-plugin-installer"
SESSION_DIR="$STATE_ROOT/$SESSION_KEY"
LOGS_DIR="$SESSION_DIR/refresh-logs"
LOCK_DIR="$SESSION_DIR/refresh.lock"

DELIVERY_DIR="$SKILL_DIR/.out/$SESSION_KEY"
CURRENT_QR_PNG="$DELIVERY_DIR/current_qr.png"
CURRENT_QR_TXT="$DELIVERY_DIR/current_qr.txt"
CURRENT_QR_JSON="$DELIVERY_DIR/current_qr.json"

ACTIVE_PID_FILE="$SESSION_DIR/active_login.pid"
ACTIVE_LOG_FILE="$SESSION_DIR/active_login.log"
ACTIVE_REQUEST_FILE="$SESSION_DIR/active_request_id"
RESTART_DELAY_SECONDS=8

mkdir -p "$SESSION_DIR" "$LOGS_DIR" "$DELIVERY_DIR"

emit_json() {
  local ok="$1"
  local state="$2"
  local message="${3:-}"
  cat <<JSON
{"ok":$ok,"session_key":"$SESSION_KEY","state":"$state","message":"${message//\"/\\\"}","qr_png_path":"$CURRENT_QR_PNG","qr_txt_path":"$CURRENT_QR_TXT","qr_json_path":"$CURRENT_QR_JSON"}
JSON
}

cleanup_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup_lock EXIT

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  emit_json true "starting" "已有二维码刷新任务在运行，请稍后发送“查看微信连接状态”"
  exit 0
fi

is_pid_running() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

stop_old_active_login() {
  if [[ -f "$ACTIVE_PID_FILE" ]]; then
    old_pid="$(cat "$ACTIVE_PID_FILE" 2>/dev/null || true)"
    if is_pid_running "${old_pid:-}"; then
      kill "$old_pid" 2>/dev/null || true
      sleep 1
      if is_pid_running "${old_pid:-}"; then
        kill -9 "$old_pid" 2>/dev/null || true
      fi
    fi
  fi
}

write_current_meta() {
  local request_id="$1"
  local source_log="$2"
  python3 - "$CURRENT_QR_JSON" "$request_id" "$source_log" <<'PY'
import json, os, sys, datetime
path, request_id, source_log = sys.argv[1:4]
data = {}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
data["request_id"] = request_id
data["source_log"] = source_log
data["generated_at"] = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
data["status"] = "waiting_scan"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
PY
}

RENDER_TMP_DIR="$DELIVERY_DIR/.pending"
mkdir -p "$RENDER_TMP_DIR"

render_from_log_to_pending() {
  local log_file="$1"
  local req="$2"
  python3 "$SCRIPT_DIR/render_terminal_qr.py" \
    --input "$log_file" \
    --png "$RENDER_TMP_DIR/${req}.png" \
    --txt "$RENDER_TMP_DIR/${req}.txt" \
    --json "$RENDER_TMP_DIR/${req}.json" >/dev/null 2>&1
}

publish_pending_as_current() {
  local req="$1"
  mv "$RENDER_TMP_DIR/${req}.png" "$CURRENT_QR_PNG"
  mv "$RENDER_TMP_DIR/${req}.txt" "$CURRENT_QR_TXT"
  mv "$RENDER_TMP_DIR/${req}.json" "$CURRENT_QR_JSON"
}

SUCCESS_PAT='(连接成功|登录成功|绑定成功|已完成连接|扫码成功|微信连接成功|connected successfully|login success|connection established)'
SCANNED_PAT='(已扫码|在微信继续操作|scaned)'
FAILED_PAT='(error|failed|失败|异常|traceback|fatal|安装失败|连接失败)'

cleanup_active_login_files() {
  rm -f "$ACTIVE_PID_FILE" "$ACTIVE_LOG_FILE" "$ACTIVE_REQUEST_FILE"
}

schedule_gateway_restart() {
  bash "$SCRIPT_DIR/schedule_gateway_restart.sh" "$SESSION_KEY" "$RESTART_DELAY_SECONDS" >/dev/null 2>&1 || true
}

stop_old_active_login

REQUEST_ID="$(date +%Y%m%dT%H%M%S)"
LOG_FILE="$LOGS_DIR/refresh-$REQUEST_ID.log"

: > "$LOG_FILE"

(
  cd "$HOME"
  exec bash -lc 'openclaw channels login --channel openclaw-weixin'
) >>"$LOG_FILE" 2>&1 &

PID=$!
echo "$PID" > "$ACTIVE_PID_FILE"
printf '%s' "$LOG_FILE" > "$ACTIVE_LOG_FILE"
printf '%s' "$REQUEST_ID" > "$ACTIVE_REQUEST_FILE"

DEADLINE=$(( $(date +%s) + WAIT_SECONDS ))

while [[ "$(date +%s)" -lt "$DEADLINE" ]]; do
  qr_updated=false

  if render_from_log_to_pending "$LOG_FILE" "$REQUEST_ID"; then
    publish_pending_as_current "$REQUEST_ID"
    write_current_meta "$REQUEST_ID" "$LOG_FILE"
    qr_updated=true
  fi

  if [[ -f "$LOG_FILE" ]] && grep -Eiq "$SUCCESS_PAT" "$LOG_FILE"; then
    cleanup_active_login_files
    schedule_gateway_restart
    emit_json true "success" "微信连接已完成，网关将在几秒后自动重启，期间可能短暂失联。"
    exit 0
  fi

  if [[ -f "$LOG_FILE" ]] && grep -Eiq "$SCANNED_PAT" "$LOG_FILE"; then
    emit_json true "scanned" "已检测到扫码，请在微信里确认授权。"
    exit 0
  fi

  if [[ "$qr_updated" == "true" ]]; then
    emit_json true "waiting_scan" "二维码已刷新，请扫描最新二维码"
    exit 0
  fi

  if ! is_pid_running "$PID"; then
    break
  fi

  sleep 2
done

if [[ -f "$LOG_FILE" ]] && grep -Eiq "$FAILED_PAT" "$LOG_FILE"; then
  tail_msg="$(tail -n 20 "$LOG_FILE" 2>/dev/null | tr '\n' ' ' | sed 's/"/\\"/g')"
  cleanup_active_login_files
  emit_json false "failed" "${tail_msg:-刷新二维码失败}"
  exit 0
fi

emit_json true "starting" "正在生成新的二维码，请 3 到 5 秒后发送“查看微信连接状态”"
