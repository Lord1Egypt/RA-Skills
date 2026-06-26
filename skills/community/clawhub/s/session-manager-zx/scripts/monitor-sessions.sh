#!/bin/bash
# 会话监控脚本

set -e

CONFIG_DIR="$HOME/.openclaw/session-manager"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
LOG_FILE="$CONFIG_DIR/cleanup.log"

echo "📊 会话监控"
echo "==========="

# 会话统计
if [ -d "$SESSIONS_DIR" ]; then
    SESSION_FILES=("$SESSIONS_DIR"/*.json)
    SESSION_COUNT=${#SESSION_FILES[@]}
    
    if [ "$SESSION_COUNT" -eq 1 ] && [ ! -f "${SESSION_FILES[0]}" ]; then
        SESSION_COUNT=0
    fi
    
    echo "活跃会话数: $SESSION_COUNT"
else
    echo "活跃会话数: 0"
fi

# 磁盘占用
if [ -d "$SESSIONS_DIR" ]; then
    TOTAL_SIZE=$(du -sh "$SESSIONS_DIR" 2>/dev/null | cut -f1 || echo "未知")
    echo "磁盘占用: $TOTAL_SIZE"
fi

# 清理日志
if [ -f "$LOG_FILE" ]; then
    LOG_LINES=$(wc -l < "$LOG_FILE")
    LAST_CLEANUP=$(tail -1 "$LOG_FILE" 2>/dev/null || echo "无记录")
    echo "清理日志: $LOG_LINES 行"
    echo "最后清理: $LAST_CLEANUP"
else
    echo "清理日志: 无"
fi

# Cron 任务状态
echo ""
echo "📅 定时任务:"
if command -v openclaw &> /dev/null; then
    if openclaw cron list 2>/dev/null | grep -q "会话清理"; then
        echo "✅ 会话清理任务已配置"
    else
        echo "⚠️  会话清理任务未配置"
    fi
else
    echo "⚠️  openclaw 命令不可用"
fi

echo ""
echo "💡 使用建议:"
echo "- 定期运行清理脚本保持系统整洁"
echo "- 监控磁盘空间使用情况"
echo "- 检查定时任务是否正常运行"