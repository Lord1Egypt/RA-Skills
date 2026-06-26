#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-9222}"
PROFILE_SYNC_MODE="${WEREAD_PROFILE_SYNC_MODE:-isolated}"
DEFAULT_PROFILE_DIR="$HOME/.weread-import-profile"
if [ "$PROFILE_SYNC_MODE" = "isolated" ]; then
  DEFAULT_PROFILE_DIR="$HOME/.weread-import-profile-isolated"
fi
PROFILE_DIR="${WEREAD_PROFILE_DIR:-$DEFAULT_PROFILE_DIR}"
CHROME_BIN="${WEREAD_CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
CHROME_DEFAULT="${WEREAD_CHROME_DEFAULT:-$HOME/Library/Application Support/Google/Chrome}"
START_URL="${WEREAD_BROWSER_START_URL:-https://weread.qq.com/}"

SYNC_ITEMS=(
  "Default/Cookies"
  "Default/Cookies-journal"
  "Default/Login Data"
  "Default/Login Data-journal"
  "Default/Login Data For Account"
  "Default/Login Data For Account-journal"
  "Default/Preferences"
  "Default/Secure Preferences"
  "Local State"
)

if [ ! -x "$CHROME_BIN" ]; then
  echo "未找到 Google Chrome: $CHROME_BIN" >&2
  exit 1
fi

needs_profile_sync() {
  if [ "$PROFILE_SYNC_MODE" != "legacy" ]; then
    return 1
  fi

  if [ ! -d "$PROFILE_DIR/Default" ] || [ "${SYNC_PROFILE:-}" = "1" ]; then
    return 0
  fi

  local item src dest
  for item in "${SYNC_ITEMS[@]}"; do
    src="$CHROME_DEFAULT/$item"
    dest="$PROFILE_DIR/$item"
    if [ -e "$src" ] && { [ ! -e "$dest" ] || [ "$src" -nt "$dest" ]; }; then
      return 0
    fi
  done

  return 1
}

sync_profile() {
  echo "正在从默认 Chrome Profile 同步登录态..." >&2
  mkdir -p "$PROFILE_DIR"
  # 仅复制保留登录态所需的文件
  local item src dest
  for item in "${SYNC_ITEMS[@]}"; do
    src="$CHROME_DEFAULT/$item"
    dest="$PROFILE_DIR/$item"
    if [ -e "$src" ]; then
      mkdir -p "$(dirname "$dest")"
      cp -f "$src" "$dest"
    fi
  done
  echo "同步完成。" >&2
}

ensure_profile_dir() {
  mkdir -p "$PROFILE_DIR/Default"
}

cdp_running() {
  curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1
}

managed_listener_pids() {
  local pid cmd
  while read -r pid; do
    [ -z "$pid" ] && continue
    cmd="$(ps -p "$pid" -o command= 2>/dev/null || true)"
    if [[ "$cmd" == *"--user-data-dir=$PROFILE_DIR"* ]]; then
      echo "$pid"
    fi
  done < <(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true)
}

restart_managed_listener() {
  local pids
  pids="$(managed_listener_pids)"
  if [ -z "$pids" ]; then
    echo "检测到外部 Chrome CDP 已在端口 $PORT 运行，保留现状。" >&2
    return 1
  fi

  echo "Chrome CDP 快照已过期，正在重启受管实例..." >&2
  kill $pids 2>/dev/null || true
  for _ in $(seq 1 20); do
    if ! cdp_running; then
      return 0
    fi
    sleep 0.5
  done

  return 0
}

if cdp_running; then
  if ! needs_profile_sync; then
    echo "Chrome CDP 已在端口 $PORT 运行。" >&2
    exit 0
  fi

  if ! restart_managed_listener; then
    exit 0
  fi
fi

if needs_profile_sync; then
  sync_profile
else
  ensure_profile_dir
fi

exec "$CHROME_BIN" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE_DIR" \
  "$START_URL"
