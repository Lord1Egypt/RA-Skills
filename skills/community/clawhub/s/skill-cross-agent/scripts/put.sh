#!/bin/bash
# cross-agent-put - 向目标机器发送文件

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
LOCAL_PATH="$2"
REMOTE_PATH="${3:-~/Desktop/}"
TARGET_USER="${4:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${5:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$LOCAL_PATH" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent put <IP> <本地路径> [远程路径] [用户名] [密码]"
    exit 1
fi

if [ ! -f "$LOCAL_PATH" ]; then
    echo "❌ 错误: 本地文件不存在: ${LOCAL_PATH}"
    exit 1
fi

echo "📤 发送 ${LOCAL_PATH} 到 ${TARGET_IP}:${REMOTE_PATH}..."
echo ""

if sshpass -p "$TARGET_PASS" scp \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "$LOCAL_PATH" "${TARGET_USER}@${TARGET_IP}:${REMOTE_PATH}" 2>&1; then
    echo -e "${GREEN}✅ 文件发送成功!${NC}"
else
    echo -e "${RED}❌ 文件发送失败${NC}"
    exit 1
fi