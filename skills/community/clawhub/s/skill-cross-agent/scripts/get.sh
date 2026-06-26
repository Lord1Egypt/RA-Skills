#!/bin/bash
# cross-agent-get - 从目标机器获取文件

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
REMOTE_PATH="$2"
LOCAL_PATH="${3:-./}"
TARGET_USER="${4:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${5:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$REMOTE_PATH" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent get <IP> <远程路径> [本地路径] [用户名] [密码]"
    exit 1
fi

echo "📥 从 ${TARGET_IP}:${REMOTE_PATH} 获取文件..."
echo "📂 保存到: ${LOCAL_PATH}"
echo ""

# 确保本地目录存在
mkdir -p "$(dirname "$LOCAL_PATH")" 2>/dev/null || true

if sshpass -p "$TARGET_PASS" scp \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}:${REMOTE_PATH}" "$LOCAL_PATH" 2>&1; then
    echo -e "${GREEN}✅ 文件获取成功!${NC}"
    ls -lh "$LOCAL_PATH"
else
    echo -e "${RED}❌ 文件获取失败${NC}"
    exit 1
fi