#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
if [ ! -d "$ROOT_DIR/node_modules" ]; then
  echo "首次运行，正在安装依赖..." >&2
  (cd "$ROOT_DIR" && npm install --production)
fi

COOKIE_FROM="manual"
for ((i=1; i<=$#; i++)); do
  if [ "${!i}" = "--cookie-from" ]; then
    next_index=$((i + 1))
    COOKIE_FROM="${!next_index:-manual}"
    break
  fi
done
if [ "$COOKIE_FROM" = "browser" ]; then
  COOKIE_FROM="browser-managed"
fi

# 自动确保 Chrome CDP 可用，并在受管模式下触发同步/重启
CDP_PORT="${WEREAD_CDP_PORT:-9222}"
if [ "$COOKIE_FROM" = "browser-managed" ]; then
  echo "正在校验 Chrome CDP..." >&2
  MANAGED_COLD_START=1
  if curl -s "http://127.0.0.1:$CDP_PORT/json/version" > /dev/null 2>&1; then
    MANAGED_COLD_START=0
  fi
  nohup bash "$SCRIPT_DIR/open-chrome-debug.sh" "$CDP_PORT" > /dev/null 2>&1 </dev/null &
  for i in $(seq 1 10); do
    sleep 1
    if curl -s "http://127.0.0.1:$CDP_PORT/json/version" > /dev/null 2>&1; then
      echo "Chrome CDP 已就绪。" >&2
      break
    fi
    if [ "$i" -eq 10 ]; then
      echo "Chrome CDP 启动超时，将仅使用 API 模式。" >&2
    fi
  done
  if [ "$MANAGED_COLD_START" -eq 1 ]; then
    node "$SCRIPT_DIR/wait-browser-managed-ready.mjs" \
      --cdp "http://127.0.0.1:$CDP_PORT" \
      --timeout-ms "${WEREAD_BROWSER_READY_TIMEOUT_MS:-8000}"
  fi
elif [ "$COOKIE_FROM" = "browser-live" ]; then
  echo "正在校验外部 Chrome CDP..." >&2
  for i in $(seq 1 10); do
    sleep 1
    if curl -s "http://127.0.0.1:$CDP_PORT/json/version" > /dev/null 2>&1; then
      echo "外部 Chrome CDP 已就绪。" >&2
      break
    fi
    if [ "$i" -eq 10 ]; then
      echo "未检测到外部 Chrome CDP，请先手动启动带远程调试端口的 Chrome，或改用 --cookie-from browser-managed。" >&2
      exit 1
    fi
  done
fi

node "$ROOT_DIR/src/cli.mjs" "$@"
