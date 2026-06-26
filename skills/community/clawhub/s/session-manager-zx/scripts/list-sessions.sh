#!/bin/bash
# 会话列表脚本

set -e

SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"

echo "📋 会话列表"
echo "==========="

if [ ! -d "$SESSIONS_DIR" ]; then
    echo "⚠️  会话目录不存在: $SESSIONS_DIR"
    exit 0
fi

SESSION_FILES=("$SESSIONS_DIR"/*.json)
SESSION_COUNT=${#SESSION_FILES[@]}

if [ "$SESSION_COUNT" -eq 1 ] && [ ! -f "${SESSION_FILES[0]}" ]; then
    echo "✅ 无会话文件"
    exit 0
fi

echo "共 $SESSION_COUNT 个会话:"

for session_file in "${SESSION_FILES[@]}"; do
    if [ ! -f "$session_file" ]; then
        continue
    fi
    
    session_id=$(basename "$session_file" .json)
    
    # 获取最后修改时间
    if command -v stat &> /dev/null; then
        if stat --version 2>/dev/null | grep -q GNU; then
            # GNU stat
            last_modified=$(stat -c %y "$session_file" | cut -d' ' -f1,2)
        else
            # BSD stat (macOS)
            last_modified=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$session_file")
        fi
    else
        last_modified="未知"
    fi
    
    echo "- $session_id (最后活动: $last_modified)"
done

# 显示磁盘占用
TOTAL_SIZE=$(du -sh "$SESSIONS_DIR" 2>/dev/null | cut -f1 || echo "未知")
echo ""
echo "💾 磁盘占用: $TOTAL_SIZE"