#!/bin/bash
# ============================================================
# socratic-reading-coach · 停止服务脚本
# 用法：bash stop.sh
# 凭本应用写入的 PID 文件精确停止服务，不影响端口上的其他程序。
# ============================================================
PORT=3456
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$SKILL_DIR/assets/.server.pid"

echo "🛑 正在停止 AI 伴读服务（端口 ${PORT}）…"

PID="$(cat "$PID_FILE" 2>/dev/null || true)"

if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
  kill "$PID" 2>/dev/null || true
  for i in 1 2 3 4 5; do kill -0 "$PID" 2>/dev/null || break; sleep 0.5; done
  rm -f "$PID_FILE"
  echo "✅ 已停止本应用进程：$PID"
  exit 0
fi
rm -f "$PID_FILE"

# PID 文件不存在或进程已退出，确认端口状态
if command -v lsof &>/dev/null; then
  PIDS="$(lsof -ti :"$PORT" 2>/dev/null || true)"
  if [ -z "$PIDS" ]; then
    echo "ℹ️  端口 ${PORT} 未被占用，服务未在运行"
  else
    echo "⚠️  端口 ${PORT} 上的进程不属于本应用（无本应用 PID 记录），未做任何操作："
    lsof -i :"$PORT" 2>/dev/null | head -5 || true
    exit 1
  fi
else
  echo "ℹ️  服务未在运行"
fi
