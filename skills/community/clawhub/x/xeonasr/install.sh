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

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

SKIP_START=0
SETUP_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-start) SKIP_START=1; shift ;;
    --force|--skip-deps) SETUP_ARGS+=("$1"); shift ;;
    *) log_error "未知参数: $1"; exit 1 ;;
  esac
done

command -v node >/dev/null 2>&1 || { log_error "需要 Node.js 18+"; exit 1; }
command -v npm >/dev/null 2>&1 || { log_error "需要 npm"; exit 1; }

log_step "安装 Python 环境与模型配置"
bash "$SKILL_DIR/setup_env.sh" "${SETUP_ARGS[@]}"

log_step "安装 Node 依赖"
npm install

log_step "配置 OpenClaw QQBOT TTS 集成"
bash "$SKILL_DIR/configure_openclaw_integration.sh"

log_step "安装开机自启服务"
bash "$SKILL_DIR/install_systemd_services.sh"

if [[ "$SKIP_START" -ne 1 ]]; then
  log_step "启动本地服务"
  bash "$SKILL_DIR/start_all.sh"
else
  log_warn "已跳过自动启动，可手工执行 ./start_all.sh"
fi

log_step "执行自检"
bash "$SKILL_DIR/self_check.sh"

log_info "Xeon TTS 安装完成"
