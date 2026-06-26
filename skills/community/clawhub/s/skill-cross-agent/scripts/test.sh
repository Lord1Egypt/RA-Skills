#!/bin/bash
# cross-agent-test - 测试SSH连接

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 读取参数或使用默认值
TARGET_IP="${1:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_ip | cut -d= -f2)}"
TARGET_USER="${2:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_user | cut -d= -f2)}"
TARGET_PASS="${3:-$(cat ~/.config/openclaw/cross-agent.conf 2>/dev/null | grep default_pass | cut -d= -f2)}"

if [ -z "$TARGET_IP" ] || [ -z "$TARGET_USER" ] || [ -z "$TARGET_PASS" ]; then
    echo "❌ 错误: 缺少参数"
    echo "用法: openclaw cross-agent test <IP> [用户名] [密码]"
    echo "或者先配置默认值: openclaw cross-agent config"
    exit 1
fi

echo "🧪 测试连接到 ${TARGET_USER}@${TARGET_IP}..."

# 测试ping
echo -n "  📡 Ping测试... "
if ping -c 1 -W 2 "$TARGET_IP" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}失败${NC}"
    exit 1
fi

# 测试SSH
echo -n "  🔑 SSH测试... "
if sshpass -p "$TARGET_PASS" ssh \
    -o ConnectTimeout=5 \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}" "echo 'SSH_OK'" 2>/dev/null | grep -q "SSH_OK"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}失败${NC}"
    echo "提示: 检查用户名/密码，或目标机器SSH是否开启"
    exit 1
fi

# 测试OpenClaw
echo -n "  🤖 OpenClaw检查... "
if sshpass -p "$TARGET_PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${TARGET_USER}@${TARGET_IP}" "ps aux | grep openclaw-gateway | grep -v grep" > /dev/null 2>&1; then
    echo -e "${GREEN}运行中${NC}"
else
    echo -e "${RED}未运行${NC}"
    echo "提示: 目标机器需要运行 'openclaw gateway start'"
fi

echo ""
echo "✅ 连接测试完成!"