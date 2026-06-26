#!/bin/bash
# Viking Memory System - sv_read
# 读取记忆内容并刷新权重
# 
# 用法: sv_read <path>
#       sv_read viking://agent/memories/daily/2026-03-16.md

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"

if [ $# -lt 1 ]; then
    echo "用法: sv_read <path>"
    exit 1
fi

PATH_ARG="$1"

# 解析路径
if [[ "$PATH_ARG" == viking://* ]]; then
    REL_PATH="${PATH_ARG#viking://}"
    WORKSPACE="${SV_WORKSPACE:-$VIKING_HOME}"
    FULL_PATH="$WORKSPACE/$REL_PATH"
else
    FULL_PATH="$PATH_ARG"
fi

if [ ! -f "$FULL_PATH" ]; then
    echo "✗ 记忆文件不存在: $FULL_PATH"
    exit 1
fi

# 提取 frontmatter 元数据
IMPORTANCE=$(grep "^importance:" "$FULL_PATH" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "medium")
LAYER=$(grep "^current_layer:" "$FULL_PATH" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "L0")
WEIGHT=$(grep "^weight:" "$FULL_PATH" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "0")
ACCESS_COUNT=$(grep "^access_count:" "$FULL_PATH" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "1")

echo "=== 记忆读取 ==="
echo "文件: $(basename "$FULL_PATH")"
echo "重要性: $IMPORTANCE | 层级: $LAYER | 权重: $WEIGHT | 访问: $ACCESS_COUNT"
echo "---"

# 显示内容 (跳过 frontmatter - 找到第二个 --- 之后的内容)
CONTENT=$(awk '/^---$/{c++;next} c>=2' "$FULL_PATH")
echo "$CONTENT"

# 刷新访问计数
if [ -z "$ACCESS_COUNT" ] || ! [[ "$ACCESS_COUNT" =~ ^[0-9]+$ ]]; then
    ACCESS_COUNT=1
fi
NEW_COUNT=$((ACCESS_COUNT + 1))
if ! sed -i "s/^access_count:.*/access_count: $NEW_COUNT/" "$FULL_PATH" 2>/dev/null; then
    echo "⚠ 警告: access_count 更新失败: $FULL_PATH"
fi
if ! sed -i "s/^last_access:.*/last_access: $(date -Iseconds)/" "$FULL_PATH" 2>/dev/null; then
    echo "⚠ 警告: last_access 更新失败: $FULL_PATH"
fi

echo ""
echo "✓ 访问计数已更新: $ACCESS_COUNT → $NEW_COUNT"

exit 0
