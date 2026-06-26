#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -f tts.pid ]]; then
  PID="$(cat tts.pid)"
  kill "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null || true
  rm -f tts.pid
fi

PID_9002=$(lsof -Pi :9002 -sTCP:LISTEN -t 2>/dev/null | head -1 || true)
if [[ -n "$PID_9002" ]]; then
  kill "$PID_9002" 2>/dev/null || kill -9 "$PID_9002" 2>/dev/null || true
fi

pkill -f "node.*server.js" 2>/dev/null || true
echo "Xeon TTS 服务已停止"
