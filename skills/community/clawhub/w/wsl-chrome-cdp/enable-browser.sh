#!/bin/bash
# =====================================================
# WSL Chrome CDP - 全自动启用浏览器
# 用途：自动检测并启动 Chrome，无需手动操作
# 作者：杏子
# 创建日期：2026-03-11
# =====================================================

set -e

POWERShell="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
CDP_PORT=9222

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${CYAN}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[✗]${NC} $1"; }

echo "========================================="
echo "WSL Chrome CDP - 全自动启用"
echo "作者：杏子 🍑"
echo "========================================="
echo ""

# 取消代理
export no_proxy="127.0.0.1,localhost,0.0.0.0,*"
unset http_proxy https_proxy 2>/dev/null || true

# 获取 Windows IP
get_windows_ip() {
    local ip=$($POWERShell -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike '*Loopback*' -and $_.IPAddress -notlike '169.254.*' -and $_.IPAddress -ne '127.0.0.1'}).IPAddress" 2>/dev/null | head -n1)
    if [ -z "$ip" ]; then
        ip=$(cat /etc/resolv.conf 2>/dev/null | grep nameserver | awk '{print $2}' | head -n1)
    fi
    echo "${ip:-127.0.0.1}"
}

WINDOWS_IP=$(get_windows_ip)
CDP_URL="http://127.0.0.1:$CDP_PORT/json/version"
CDP_URL_ALT="http://$WINDOWS_IP:$CDP_PORT/json/version"

# 检查 CDP 连接
check_cdp() {
    local url="${1:-$CDP_URL}"
    local response=$(curl -s --connect-timeout 3 -w "\n%{http_code}" "$url" 2>/dev/null || echo "")
    local code=$(echo "$response" | tail -n1)
    [ "$code" = "200" ] && echo "$response" || echo ""
}

# 步骤 1：检查 CDP
log "检查 Chrome CDP 连接..."
response=$(check_cdp "$CDP_URL")
if [ -z "$response" ]; then
    log "尝试 Windows IP: $WINDOWS_IP"
    response=$(check_cdp "$CDP_URL_ALT")
fi

if [ -n "$response" ]; then
    ok "Chrome CDP 已就绪"
    version=$(echo "$response" | head -n-1 | grep -o '"Browser": "[^"]*"' | cut -d'"' -f4)
    log "Chrome 版本：$version"
    echo ""
    echo "========================================="
    ok "浏览器已就绪，可以使用！"
    echo "========================================="
    exit 0
fi

# 步骤 2：启动 Chrome
warn "Chrome CDP 未就绪，正在自动启动..."
log "通过 PowerShell 启动 Chrome 调试模式..."

ps_command='Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222","--user-data-dir=C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\Debug","--no-first-run"'
$POWERShell -Command "$ps_command"

log "等待 Chrome 启动（8 秒）..."
sleep 8

# 步骤 3：验证
log "验证 CDP 连接..."
response=$(check_cdp "$CDP_URL" || check_cdp "$CDP_URL_ALT")

if [ -n "$response" ]; then
    ok "Chrome CDP 启动成功"
    version=$(echo "$response" | head -n-1 | grep -o '"Browser": "[^"]*"' | cut -d'"' -f4)
    log "Chrome 版本：$version"
    echo ""
    echo "========================================="
    ok "浏览器已就绪，可以使用！"
    echo "========================================="
    exit 0
else
    fail "Chrome CDP 启动失败"
    echo ""
    echo "请检查："
    echo "  1. Chrome 是否安装（C:\Program Files\Google\Chrome）"
    echo "  2. 防火墙是否阻止端口 9222"
    echo "  3. 端口 9222 是否被占用"
    echo ""
    echo "故障排查：查看 docs/troubleshooting.md"
    exit 1
fi
