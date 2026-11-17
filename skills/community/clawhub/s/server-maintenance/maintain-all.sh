#!/bin/bash
# Server Maintenance - Maintain All Servers
# 批量维护所有服务器

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== 服务器批量维护 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 定义服务器列表
declare -a SERVERS=(
    "中央:43.163.225.27"
    "东京:43.167.192.145"
)

echo "| 服务器 | 清理前 | 清理后 | 状态 |"
echo "|--------|--------|--------|------|"

for server in "${SERVERS[@]}"; do
    IFS=':' read -r name host <<< "$server"
    
    # 获取清理前状态
    BEFORE=$(ssh -o StrictHostKeyChecking=no root@$host "df -h / | tail -1 | awk '{print \$5}'")
    
    # 执行清理
    ssh -o StrictHostKeyChecking=no root@$host "npm cache clean --force > /dev/null 2>&1" || true
    
    # 获取清理后状态
    AFTER=$(ssh -o StrictHostKeyChecking=no root@$host "df -h / | tail -1 | awk '{print \$5}'")
    
    echo "| $name | $BEFORE | $AFTER | ✓ |"
done

echo ""
echo "✓ 批量维护完成"
