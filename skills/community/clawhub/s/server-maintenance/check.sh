#!/bin/bash
# Server Maintenance - Check Script
# 检查单个服务器的磁盘和资源使用情况

set -e

SERVER_HOST="${1:-localhost}"
SERVER_NAME="${2:-本地}"

echo "=== $SERVER_NAME 服务器状态 ==="

if [ "$SERVER_HOST" = "localhost" ]; then
    # 本地检查
    CMD_PREFIX=""
else
    # 远程检查
    CMD_PREFIX="ssh root@$SERVER_HOST"
fi

# 磁盘使用
echo "磁盘使用："
$CMD_PREFIX df -h / | tail -1

# 大目录
echo -e "\n大目录 Top 8："
if [ "$SERVER_HOST" = "localhost" ]; then
    du -h --max-depth=2 /root 2>/dev/null | sort -rh | head -8
else
    ssh root@$SERVER_HOST "du -h --max-depth=2 /root 2>/dev/null | sort -rh | head -8"
fi

# 大文件
echo -e "\n大文件 (>100MB)："
if [ "$SERVER_HOST" = "localhost" ]; then
    find /root -type f -size +100M 2>/dev/null -exec du -h {} + | sort -rh | head -5
else
    ssh root@$SERVER_HOST "find /root -type f -size +100M 2>/dev/null -exec du -h {} + | sort -rh | head -5"
fi

# 内存和 Swap
echo -e "\n内存使用："
$CMD_PREFIX free -h

echo -e "\n✓ 检查完成"
