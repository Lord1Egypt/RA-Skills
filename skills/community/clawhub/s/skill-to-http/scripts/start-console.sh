#!/usr/bin/env bash
# start-console.sh — 稳定启动 skill-to-http 控制台
#
# 用途：用 setsid 在独立 session 中启动控制台，彻底脱离
#       OpenClaw exec 工具的进程组，避免因 exec 超时 SIGTERM 被杀。
#
# 用法：
#   bash start-console.sh              # 默认 0.0.0.0:9000
#   bash start-console.sh --port 9001  # 自定义端口
#   bash start-console.sh --port 9000 --host 127.0.0.1
#
# 启动后：
#   控制台日志：/tmp/console.log
#   PID 文件：与 _paths.py 同源（OpenClaw 环境为 <workspace>/.skill-to-http/console.pid）

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/console.log"
# PID 文件路径与 _paths.py 保持同源（OPENCLAW_S2H_DATA_DIR > workspace/.skill-to-http > ~/.skill-to-http）
PID_FILE="$(python3 -c "import sys; sys.path.insert(0, '${SCRIPTS_DIR}'); from _paths import CONSOLE_PID_FILE; print(CONSOLE_PID_FILE)")"

# ── 解析参数 ───────────────────────────────────────────────────────────
PORT=9000
HOST="0.0.0.0"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)  PORT="$2"; shift 2 ;;
    --host)  HOST="$2"; shift 2 ;;
    *)       echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# ── 检查旧进程 ─────────────────────────────────────────────────────────
if [[ -f "$PID_FILE" ]]; then
  OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
  if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "⚠️  控制台已在运行（PID $OLD_PID），先停止旧进程..."
    kill -TERM "$OLD_PID" 2>/dev/null || true
    sleep 2
  fi
fi

# ── 启动控制台 ─────────────────────────────────────────────────────────
mkdir -p "$(dirname "$PID_FILE")"
echo "🚀 启动控制台 http://${HOST}:${PORT} ..."
echo "   日志: $LOG_FILE"

setsid python3 "${SCRIPTS_DIR}/console.py" start --port "$PORT" --host "$HOST" \
  >> "$LOG_FILE" 2>&1 &

CONSOLE_PID=$!
echo "$CONSOLE_PID" > "$PID_FILE"
disown "$CONSOLE_PID"

# ── Readiness probe ────────────────────────────────────────────────────
echo -n "   等待就绪..."
READY=0
for i in $(seq 1 30); do
  sleep 1
  # 用 / 静态页探活（/api/status 开鉴权后返回 403 会误报超时）
  if curl -sf "http://127.0.0.1:${PORT}/" > /dev/null 2>&1; then
    READY=1
    break
  fi
  echo -n "."
done
echo ""

if [[ $READY -eq 1 ]]; then
  echo "✅ 控制台已就绪！"
  echo ""
  echo "   本地：http://127.0.0.1:${PORT}"
  # 获取 LAN IP
  LAN_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[^ ]+' || echo "")
  if [[ -n "$LAN_IP" ]]; then
    echo "   内网：http://${LAN_IP}:${PORT}"
  fi
  echo "   PID：$CONSOLE_PID"
else
  echo "⚠️  超时，控制台可能还在启动中，查看日志: tail -f $LOG_FILE"
fi
