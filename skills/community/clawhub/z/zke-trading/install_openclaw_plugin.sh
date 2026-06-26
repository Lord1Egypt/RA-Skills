#!/bin/bash
# ==============================================================================
# ZKE OpenClaw 官方标准闭环管理脚本 (纯净编译版 - ClawHub 专用)
# ==============================================================================

set -euo pipefail

PLUGIN_ID="zke-trading"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SRC="$CURRENT_DIR/openclaw-plugin"

log_info() { echo -e "\033[32m[INFO]\033[0m $1"; }
log_err()  { echo -e "\033[31m[ERROR]\033[0m $1"; exit 1; }

safe_exec() { "$@" < /dev/null; }

check_env() {
    command -v npm >/dev/null 2>&1 || log_err "找不到 npm"
    command -v openclaw >/dev/null 2>&1 || log_err "找不到 openclaw CLI"
    PYTHON_BIN=""
    for cmd in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$cmd" >/dev/null 2>&1 && "$cmd" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' >/dev/null 2>&1; then
            PYTHON_BIN="$cmd"; break
        fi
    done
    [ -z "$PYTHON_BIN" ] && log_err "未找到 Python 3.10+"
}

do_install() {
    log_info "清理历史残留..."
    safe_exec openclaw plugins disable "$PLUGIN_ID" 2>/dev/null || true
    safe_exec openclaw plugins uninstall "$PLUGIN_ID" 2>/dev/null || true

    log_info "编译本地 TypeScript 插件..."
    cd "$PLUGIN_SRC"
    npm install >/dev/null 2>&1 && npm run build || log_err "编译失败"

    log_info "构建 Python 虚拟环境..."
    cd "$CURRENT_DIR"
    "$PYTHON_BIN" -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt >/dev/null 2>&1 || log_err "依赖安装失败"

    log_info "注册 MCP 插件..."
    cd "$PLUGIN_SRC"
    safe_exec openclaw plugins install . 
    safe_exec openclaw plugins enable "$PLUGIN_ID"

    echo -e "\n\033[32m[✓] 插件编译与注册成功！\033[0m"
    echo -e "\033[33m请在 OpenClaw 环境变量中配置 ZKE_API_KEY 和 ZKE_SECRET_KEY 以启用交易功能。\033[0m"
}

check_env
do_install