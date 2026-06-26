#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

echo "========================================"
echo "  启动 Xeon TTS 服务"
echo "========================================"

[ ! -d node_modules ] && npm install

log_step "启动 Python TTS 服务 (5002)"
if ! lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null 2>&1; then
  ./start_tts_service.sh
  sleep 2
fi

log_step "启动 Node TTS 工作流网关 (9002)"
pkill -f "node.*server.js" 2>/dev/null || true
sleep 1
(setsid node server.js >> skill.log 2>&1 </dev/null &)
sleep 3

PID_9002=$(lsof -Pi :9002 -sTCP:LISTEN -t 2>/dev/null | head -1 || true)
if [[ -z "$PID_9002" ]]; then
  log_warn "未检测到 9002 监听进程，请查看 skill.log"
  exit 1
fi

echo "$PID_9002" > skill.pid
log_info "Node 网关已启动 (PID: $PID_9002)"

if command -v openclaw >/dev/null 2>&1; then
  log_step "重启 OpenClaw gateway"
  openclaw gateway restart || log_warn "gateway restart 失败，请手工执行"
fi

log_info "完成。健康检查: curl http://127.0.0.1:5002/api/health && curl http://127.0.0.1:9002/health"
