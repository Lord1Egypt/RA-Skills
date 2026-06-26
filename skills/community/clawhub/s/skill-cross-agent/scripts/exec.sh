#!/bin/bash
# cross-agent-exec - 在目标机器执行命令

set -e

TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
COMMAND="$2"
TARGET_USER="${3:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${4:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$COMMAND" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent exec <IP> <命令> [用户名] [密码]"
    exit 1
fi

echo "🔧 在 ${TARGET_USER}@${TARGET_IP} 执行: ${COMMAND}"
echo ""

sshpass -p "$TARGET_PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}" "$COMMAND" 2>&1