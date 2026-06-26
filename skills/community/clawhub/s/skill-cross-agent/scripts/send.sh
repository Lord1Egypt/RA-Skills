#!/bin/bash
# cross-agent-send - 发送任务给目标Agent

set -e

TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
MESSAGE="$2"
TARGET_USER="${3:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${4:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$MESSAGE" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent send <IP> <消息> [用户名] [密码]"
    echo "示例: openclaw cross-agent send 192.168.3.54 '请搜索教程' admin 123456"
    exit 1
fi

echo "📤 发送任务到 ${TARGET_USER}@${TARGET_IP}..."
echo "💬 消息: ${MESSAGE}"
echo ""

# 转义消息中的特殊字符
ESCAPED_MSG=$(echo "$MESSAGE" | sed "s/'/'\\''/g")

sshpass -p "$TARGET_PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}" \
    "export PATH=\$HOME/.npm-global/bin:\$PATH && openclaw agent -m '${ESCAPED_MSG}' 2>&1" 2>&1 || {
    echo ""
    echo "⚠️ 注意: 虽然可能有错误提示，但消息可能已送达"
    echo "   目标Agent通常通过webchat接收消息"
}