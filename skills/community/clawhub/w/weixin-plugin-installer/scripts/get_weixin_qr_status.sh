#!/usr/bin/env bash
set -euo pipefail

RAW_SESSION_KEY="${1:-default}"

SESSION_KEY="$(printf '%s' "$RAW_SESSION_KEY" | tr -cd '[:alnum:]._-' )"
SESSION_KEY="${SESSION_KEY:-default}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

STATE_ROOT="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/weixin-plugin-installer"
SESSION_DIR="$STATE_ROOT/$SESSION_KEY"

DELIVERY_DIR="$SKILL_DIR/.out/$SESSION_KEY"
CURRENT_QR_PNG="$DELIVERY_DIR/current_qr.png"
CURRENT_QR_TXT="$DELIVERY_DIR/current_qr.txt"
CURRENT_QR_JSON="$DELIVERY_DIR/current_qr.json"

ACTIVE_PID_FILE="$SESSION_DIR/active_login.pid"
ACTIVE_LOG_FILE="$SESSION_DIR/active_login.log"
ACTIVE_REQUEST_FILE="$SESSION_DIR/active_request_id"
RESTART_DELAY_SECONDS=8

mkdir -p "$SESSION_DIR" "$DELIVERY_DIR"

emit_json() {
  local ok="$1"
  local state="$2"
  local message="${3:-}"
  cat <<JSON
{"ok":$ok,"session_key":"$SESSION_KEY","state":"$state","message":"${message//\"/\\\"}","qr_png_path":"$CURRENT_QR_PNG","qr_txt_path":"$CURRENT_QR_TXT","qr_json_path":"$CURRENT_QR_JSON"}
JSON
}

is_pid_running() {
  local pid="$1"
  [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null
}

read_active_request_id() {
  if [[ -f "$ACTIVE_REQUEST_FILE" ]]; then
    cat "$ACTIVE_REQUEST_FILE" 2>/dev/null || true
  fi
}

read_active_log_file() {
  if [[ -f "$ACTIVE_LOG_FILE" ]]; then
    cat "$ACTIVE_LOG_FILE" 2>/dev/null || true
  fi
}

current_hash() {
  if [[ -f "$CURRENT_QR_JSON" ]]; then
    python3 - "$CURRENT_QR_JSON" <<'PY'
import json, sys
path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(str(data.get("selected_hash", "") or ""))
except Exception:
    print("")
PY
  else
    echo ""
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

pending_hash() {
  local req="$1"
  local path="$RENDER_TMP_DIR/${req}.json"
  if [[ -f "$path" ]]; then
    python3 - "$path" <<'PY'
import json, sys
path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(str(data.get("selected_hash", "") or ""))
except Exception:
    print("")
PY
  else
    echo ""
  fi
}

publish_pending_as_current() {
  local req="$1"
  mv "$RENDER_TMP_DIR/${req}.png" "$CURRENT_QR_PNG"
  mv "$RENDER_TMP_DIR/${req}.txt" "$CURRENT_QR_TXT"
  mv "$RENDER_TMP_DIR/${req}.json" "$CURRENT_QR_JSON"
}

has_current_qr() {
  [[ -f "$CURRENT_QR_PNG" && -f "$CURRENT_QR_JSON" ]]
}

SUCCESS_PAT='(连接成功|登录成功|绑定成功|已完成连接|扫码成功|微信连接成功|connected successfully|login success|connection established)'
SCANNED_PAT='(已扫码|在微信继续操作|scaned)'

cleanup_active_login_files() {
  rm -f "$ACTIVE_PID_FILE" "$ACTIVE_LOG_FILE" "$ACTIVE_REQUEST_FILE"
}

schedule_gateway_restart() {
  bash "$SCRIPT_DIR/schedule_gateway_restart.sh" "$SESSION_KEY" "$RESTART_DELAY_SECONDS" >/dev/null 2>&1 || true
}

ACTIVE_REQ="$(read_active_request_id)"
ACTIVE_LOG="$(read_active_log_file)"
CUR_HASH="$(current_hash)"

if [[ -f "$ACTIVE_PID_FILE" ]]; then
  ACTIVE_PID="$(cat "$ACTIVE_PID_FILE" 2>/dev/null || true)"
else
  ACTIVE_PID=""
fi

# 如果当前刷新任务还在跑，优先尝试从这次刷新日志里提取最新二维码
if [[ -n "${ACTIVE_LOG:-}" && -f "$ACTIVE_LOG" ]]; then
  if [[ -f "$ACTIVE_LOG" ]] && grep -Eiq "$SUCCESS_PAT" "$ACTIVE_LOG"; then
    cleanup_active_login_files
    schedule_gateway_restart
    emit_json true "success" "微信连接已完成，网关将在几秒后自动重启，期间可能短暂失联。"
    exit 0
  fi

  qr_updated=false

  if [[ -n "${ACTIVE_REQ:-}" ]] && render_from_log_to_pending "$ACTIVE_LOG" "$ACTIVE_REQ"; then
    NEW_HASH="$(pending_hash "$ACTIVE_REQ")"
    if [[ -n "$NEW_HASH" && "$NEW_HASH" != "$CUR_HASH" ]]; then
      publish_pending_as_current "$ACTIVE_REQ"
      write_current_meta "$ACTIVE_REQ" "$ACTIVE_LOG"
      qr_updated=true
    fi
  fi

  if [[ -f "$ACTIVE_LOG" ]] && grep -Eiq "$SCANNED_PAT" "$ACTIVE_LOG"; then
    emit_json true "scanned" "已检测到扫码，请在微信里确认授权。"
    exit 0
  fi

  if [[ "$qr_updated" == "true" ]]; then
    emit_json true "waiting_scan" "二维码已刷新，请扫描最新二维码"
    exit 0
  fi

  if is_pid_running "${ACTIVE_PID:-}"; then
    if has_current_qr; then
      emit_json true "waiting_scan" "这是当前缓存的二维码；如果扫码提示过期，请稍后再次发送“刷新微信二维码”"
      exit 0
    fi
    emit_json true "starting" "正在生成新的二维码，请稍后再试"
    exit 0
  fi
fi

# 没有活动刷新任务时，只读缓存，不再调用 openclaw CLI
if has_current_qr; then
  emit_json true "waiting_scan" "这是最近一次生成的二维码；如果扫码提示过期，请发送“刷新微信二维码”"
  exit 0
fi

emit_json false "not_found" "当前没有可用的二维码缓存"
