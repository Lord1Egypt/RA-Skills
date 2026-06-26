#!/bin/bash

# 会话日志清理脚本
# 清理30天前的会话日志文件

OPENCLAW_DIR="/root/.openclaw"
MEMORY_DIR="$OPENCLAW_DIR/memory"
LOGS_DIR="$OPENCLAW_DIR/logs"
DAYS_TO_KEEP=30

echo "=== 会话日志清理开始 ==="
echo "OpenClaw目录: $OPENCLAW_DIR"
echo "保留天数: $DAYS_TO_KEEP 天"
echo ""

TOTAL_DELETED=0

# 清理memory目录
if [ -d "$MEMORY_DIR" ]; then
    echo "--- 清理 memory 目录 ---"
    OLD_MEMORY=$(find "$MEMORY_DIR" -name "*.md" -type f -mtime +$DAYS_TO_KEEP)
    if [ -z "$OLD_MEMORY" ]; then
        echo "✅ 没有需要清理的memory文件"
    else
        COUNT=$(echo "$OLD_MEMORY" | wc -l)
        echo "找到 $COUNT 个旧memory文件"
        echo "$OLD_MEMORY" | xargs rm -f
        TOTAL_DELETED=$((TOTAL_DELETED + COUNT))
        echo "✅ 已删除 $COUNT 个memory文件"
    fi
else
    echo "⚠️  memory目录不存在: $MEMORY_DIR"
fi

echo ""

# 清理logs目录
if [ -d "$LOGS_DIR" ]; then
    echo "--- 清理 logs 目录 ---"
    OLD_LOGS=$(find "$LOGS_DIR" -type f -mtime +$DAYS_TO_KEEP)
    if [ -z "$OLD_LOGS" ]; then
        echo "✅ 没有需要清理的日志文件"
    else
        COUNT=$(echo "$OLD_LOGS" | wc -l)
        echo "找到 $COUNT 个旧日志文件"
        echo "$OLD_LOGS" | xargs rm -f
        TOTAL_DELETED=$((TOTAL_DELETED + COUNT))
        echo "✅ 已删除 $COUNT 个日志文件"
    fi
else
    echo "⚠️  logs目录不存在: $LOGS_DIR"
fi

echo ""
echo "=== 清理完成 ==="
echo "总共删除了 $TOTAL_DELETED 个文件"

