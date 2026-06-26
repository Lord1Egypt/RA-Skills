#!/bin/bash
# cross-agent-sessions - 查看目标机器的OpenClaw会话

set -e

TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
TARGET_USER="${2:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${3:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent sessions <IP> [用户名] [密码]"
    exit 1
fi

echo "📋 获取 ${TARGET_IP} 上的OpenClaw会话..."
echo ""

sshpass -p "$TARGET_PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}" \
    "export PATH=\$HOME/.npm-global/bin:\$PATH && openclaw sessions 2>&1" 2>&1 || {
    echo "❌ 获取失败"
    exit 1
}