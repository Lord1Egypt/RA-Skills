#!/usr/bin/env bash
# ============================================================================
# Weibo QR Login Skill — 一键安装脚本
# 适用于：Ubuntu 22.04+ / Debian 12+（需要已安装 OpenClaw + Node.js 18+）
# 用途：安装 Playwright + Chromium，配置 OpenClaw 浏览器环境
# 使用：bash scripts/setup.sh
# ============================================================================

set -euo pipefail

PLAYWRIGHT_MIRROR="https://npmmirror.com/mirrors/playwright"
CHROMIUM_PATH=""

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

info()  { echo "[INFO] $*"; }
ok()    { echo "[ OK ] $*"; }
warn()  { echo "[WARN] $*"; }
fail()  { echo "[FAIL] $*"; exit 1; }

has_cmd() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------------------
# Step 1: 前置检查
# ---------------------------------------------------------------------------

preflight() {
    info "前置检查..."

    [[ "$(uname -s)" == "Linux" ]] || fail "仅支持 Linux（当前: $(uname -s)）"
    has_cmd openclaw               || fail "未找到 openclaw — https://docs.openclaw.ai/"
    has_cmd node                   || fail "未找到 node — 请先安装 Node.js 18+"
    has_cmd npm                    || fail "未找到 npm — 请先安装 Node.js 18+"

    ok "前置检查通过"
}

# ---------------------------------------------------------------------------
# Step 2: 安装 Playwright + Chromium（使用国内镜像）
# ---------------------------------------------------------------------------

install_browser() {
    if has_cmd playwright; then
        ok "Playwright 已安装（$(playwright --version 2>/dev/null)），跳过"
    else
        info "安装 Playwright（Node.js）..."
        npm install -g playwright 2>&1 | tail -1
    fi

    info "安装 Chromium 系统依赖（已安装的会自动跳过）..."
    playwright install-deps chromium 2>&1 || warn "install-deps 有警告（通常不影响使用）"

    info "安装 Chromium（镜像: npmmirror）..."
    PLAYWRIGHT_DOWNLOAD_HOST="$PLAYWRIGHT_MIRROR" playwright install chromium

    CHROMIUM_PATH=$(find ~/.cache/ms-playwright -name "chrome" -type f -path "*/chromium-*/chrome-linux64/chrome" 2>/dev/null | head -1)
    if [[ -z "$CHROMIUM_PATH" || ! -x "$CHROMIUM_PATH" ]]; then
        fail "未找到 Chromium 可执行文件"
    fi

    ok "浏览器就绪"
}

# ---------------------------------------------------------------------------
# Step 3: 配置 OpenClaw
# ---------------------------------------------------------------------------

config_matches() {
    python3 << PYEOF
import json, subprocess, sys

def get(path):
    r = subprocess.run(["openclaw", "config", "get", path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None

def subset(current, expected):
    if not isinstance(current, dict) or not isinstance(expected, dict):
        return current == expected
    return all(k in current and subset(current[k], v) for k, v in expected.items())

browser_expected = {
    "enabled": True, "headless": True, "noSandbox": True,
    "executablePath": "$CHROMIUM_PATH",
    "defaultProfile": "openclaw",
    "profiles": {"openclaw": {"cdpPort": 18800, "color": "#FF4500"}}
}
tools_expected = {"profile": "full", "deny": []}

browser_ok = subset(get("browser"), browser_expected)
tools_ok = subset(get("tools"), tools_expected)
sys.exit(0 if browser_ok and tools_ok else 1)
PYEOF
}

configure_openclaw() {
    if config_matches; then
        ok "OpenClaw 配置已是目标状态，跳过"
        return
    fi

    info "配置 OpenClaw..."

    openclaw config set browser.enabled true
    openclaw config set browser.headless true
    openclaw config set browser.noSandbox true
    openclaw config set browser.executablePath "$CHROMIUM_PATH"
    openclaw config set browser.defaultProfile openclaw
    openclaw config set browser.profiles.openclaw '{"cdpPort":18800,"color":"#FF4500"}' --strict-json
    openclaw config set tools.profile full
    openclaw config set tools.deny '[]' --strict-json

    nohup bash -c 'sleep 15 && openclaw gateway restart' > /dev/null 2>&1 &

    warn "配置已变更，gateway 将在 15 秒后自动重启"
    echo "GATEWAY_RESTART_REQUIRED"
}

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

main() {
    echo ""
    echo "=== Weibo QR Login Skill — 一键安装 ==="
    echo ""

    preflight
    echo ""
    install_browser
    echo ""
    configure_openclaw

    echo ""
    ok "安装完成！对 Agent 说「获取微博登录二维码」即可使用"
    echo ""
}

main "$@"
