#!/bin/bash
# cross-agent-scan - 扫描局域网内在线设备

set -e

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取网段参数
NETWORK="${1:-192.168.3}"

echo "🔍 扫描 ${NETWORK}.0/24 网段..."
echo ""

# 提取基础网段
BASE_IP=$(echo "$NETWORK" | cut -d. -f1-3)

# 扫描
FOUND=0
for i in $(seq 1 254); do
    IP="${BASE_IP}.${i}"
    if ping -c 1 -W 0.5 "$IP" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} ${IP} is up"
        ((FOUND++))
    fi
done

echo ""
echo "📊 扫描完成: 发现 ${FOUND} 台在线设备"

# 检查常见OpenClaw端口
echo ""
echo "🔎 检查OpenClaw Gateway端口..."
for i in $(seq 1 254); do
    IP="${BASE_IP}.${i}"
    if nc -z -w 1 "$IP" 18789 2>/dev/null; then
        echo -e "${YELLOW}★${NC} ${IP}:18789 - 发现OpenClaw Gateway!"
    fi
done