#!/bin/bash
# 系统监控对比脚本 - 对比最近两次快照

HISTORY_DIR="/home/app/.openclaw/skills/skill-system-monitor/history"

# 获取最近两个 JSON 文件
LATEST_FILES=($(ls -t $HISTORY_DIR/*.json 2>/dev/null | head -2))

if [ ${#LATEST_FILES[@]} -lt 2 ]; then
    echo "⚠️ 历史记录不足，无法对比（需要至少2条记录）"
    exit 0
fi

CURRENT=${LATEST_FILES[0]}
PREVIOUS=${LATEST_FILES[1]}

# 读取数据
CURRENT_DISK=$(cat $CURRENT | grep -o '"percent": [0-9]*' | head -1 | grep -o '[0-9]*')
PREVIOUS_DISK=$(cat $PREVIOUS | grep -o '"percent": [0-9]*' | head -1 | grep -o '[0-9]*')

CURRENT_MEM=$(cat $CURRENT | grep -o '"percent": [0-9]*' | tail -1 | grep -o '[0-9]*')
PREVIOUS_MEM=$(cat $PREVIOUS | grep -o '"percent": [0-9]*' | tail -1 | grep -o '[0-9]*')

CURRENT_TIME=$(cat $CURRENT | grep -o '"timestamp": "[^"]*"' | cut -d'"' -f4)
PREVIOUS_TIME=$(cat $PREVIOUS | grep -o '"timestamp": "[^"]*"' | cut -d'"' -f4)

# 计算变化
DISK_DIFF=$((CURRENT_DISK - PREVIOUS_DISK))
MEM_DIFF=$((CURRENT_MEM - PREVIOUS_MEM))

# 输出对比结果
echo "📈 变化趋势对比"
echo "=================="
echo "对比时间: $PREVIOUS_TIME → $CURRENT_TIME"
echo ""
echo "💾 硬盘: ${PREVIOUS_DISK}% → ${CURRENT_DISK}% ($([ $DISK_DIFF -gt 0 ] && echo "+"; echo "$DISK_DIFF")%)"
echo "🧠 内存: ${PREVIOUS_MEM}% → ${CURRENT_MEM}% ($([ $MEM_DIFF -gt 0 ] && echo "+"; echo "$MEM_DIFF")%)"

# 预警判断
if [ $DISK_DIFF -gt 5 ]; then
    echo ""
    echo "⚠️ 硬盘使用增长较快 (+${DISK_DIFF}%)，建议检查！"
fi

if [ $MEM_DIFF -gt 10 ]; then
    echo ""
    echo "⚠️ 内存使用增长较快 (+${MEM_DIFF}%)，建议检查！"
fi
