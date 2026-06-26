#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/tts.pid"
LOG_FILE="$SCRIPT_DIR/tts.log"
PORT=5002
START_BIN="$SCRIPT_DIR/venv/bin/xdp-tts-service"

[[ -x "$START_BIN" ]] || { log_error "未找到 $START_BIN，请先运行 bash setup_env.sh"; exit 1; }
[[ -f "$SCRIPT_DIR/tts_config.json" ]] || { log_error "未找到 tts_config.json"; exit 1; }

if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
  log_error "端口 $PORT 已被占用"
  exit 1
fi

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  log_error "TTS 服务已在运行 (PID: $(cat "$PID_FILE"))"
  exit 1
fi

log_step "启动 TTS Flask 服务"
XDP_TTS_CONFIG="$SCRIPT_DIR/tts_config.json" nohup "$START_BIN" --host 127.0.0.1 --port $PORT --config "$SCRIPT_DIR/tts_config.json" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
sleep 3

if curl -fsS http://127.0.0.1:$PORT/api/health >/dev/null 2>&1; then
  log_info "TTS 服务启动成功: http://127.0.0.1:$PORT/api/health"
else
  log_warn "TTS 服务已启动，但健康检查暂未通过，请查看 $LOG_FILE"
fi
