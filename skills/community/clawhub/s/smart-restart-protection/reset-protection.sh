#!/bin/bash
# reset-protection.sh - 重置重启保护状态（紧急使用）
# 龍哥的专属保护重置脚本 by 小包子

set -e

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}⚠️  OpenClaw 重启保护状态重置工具 ⚠️${NC}"
echo "========================================"
echo "此工具用于紧急情况下重置重启保护状态。"
echo "仅在以下情况使用："
echo "1. 保护机制误触发导致无法重启"
echo "2. 测试或调试需要"
echo "3. 系统时钟异常"
echo ""
echo -e "${RED}警告：滥用此工具可能导致无限循环！${NC}"
echo ""

# 确认操作
read -p "是否继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 0
fi

STATE_DIR="$HOME/.openclaw/restart-state"
LOCK_FILE="/tmp/openclaw-restart.lock"

echo ""
echo "正在检查状态..."

# 1. 检查锁文件
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if ps -p "$LOCK_PID" > /dev/null 2>&1; then
        echo -e "${RED}错误：重启进程正在运行 (PID: $LOCK_PID)${NC}"
        echo "请先等待该进程完成或手动终止"
        exit 1
    else
        echo "发现陈旧的锁文件，正在删除..."
        rm -f "$LOCK_FILE"
        echo "✅ 锁文件已删除"
    fi
fi

# 2. 检查状态目录
if [ ! -d "$STATE_DIR" ]; then
    echo "状态目录不存在，无需重置"
    exit 0
fi

# 显示当前状态
echo ""
echo "当前状态："
if [ -f "$STATE_DIR/restarts.log" ]; then
    RESTART_COUNT=$(wc -l < "$STATE_DIR/restarts.log")
    echo "  重启记录数: $RESTART_COUNT"
    
    if [ $RESTART_COUNT -gt 0 ]; then
        echo "  最近5次重启记录:"
        tail -5 "$STATE_DIR/restarts.log" | while read line; do
            timestamp=$(echo $line | awk '{print $1}')
            reason=$(echo $line | cut -d' ' -f2-)
            date_str=$(date -d "@$timestamp" '+%Y-%m-%d %H:%M:%S')
            echo "    $date_str - $reason"
        done
    fi
fi

if [ -f "$STATE_DIR/last_restart" ]; then
    last_ts=$(cat "$STATE_DIR/last_restart")
    if [ "$last_ts" != "0" ]; then
        date_str=$(date -d "@$last_ts" '+%Y-%m-%d %H:%M:%S')
        echo "  最后重启时间: $date_str"
    fi
fi

# 二次确认
echo ""
read -p "确定要重置所有保护状态吗？(输入'RESET'确认): " -r
if [[ ! $REPLY == "RESET" ]]; then
    echo "操作已取消"
    exit 0
fi

# 执行重置
echo ""
echo "正在重置保护状态..."

# 备份当前状态
BACKUP_DIR="$HOME/.openclaw/backups/protection-state"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/protection-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$BACKUP_FILE" -C "$STATE_DIR" . 2>/dev/null || true
echo "✅ 状态已备份到: $BACKUP_FILE"

# 重置状态
echo "0" > "$STATE_DIR/last_restart"
if [ -f "$STATE_DIR/restarts.log" ]; then
    mv "$STATE_DIR/restarts.log" "$STATE_DIR/restarts.log.backup"
fi
touch "$STATE_DIR/restarts.log"

echo ""
echo -e "${BLUE}✅ 保护状态已重置${NC}"
echo "========================================"
echo "已执行的操作："
echo "1. ✅ 锁文件已检查/清理"
echo "2. ✅ 状态目录已备份"
echo "3. ✅ 最后重启时间已重置"
echo "4. ✅ 重启记录已清空"
echo ""
echo "现在可以正常使用 smart-restart.sh 了。"
echo ""
echo -e "${YELLOW}⚠️ 注意：请谨慎使用此功能，避免无限循环重启。${NC}"

exit 0