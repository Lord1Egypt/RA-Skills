#!/bin/bash
# Viking Memory System - sv_write v2
# 支持自动路由到共享目录的记忆写入脚本
#
# 路由规则:
#   默认 → 个人 workspace memory/YYYY-MM-DD.md
#   --hot/--important → 个人 hot/ + 同步到 viking-global/shared/memory/hot/
#
# 用法:
#   sv_write_v2 <path> <content> [options]
#   sv_write_v2 --hot <path> <content>    # 重要记忆，自动同步到共享hot
#   sv_write_v2 --shared <content>        # 直接写入共享hot
#
# 示例:
#   sv_write_v2 "memory/2026-03-23.md" "# 今日工作"
#   sv_write_v2 --hot "agent/memories/daily/2026-03-23.md" "# 重要决策"

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
VIKING_GLOBAL="$HOME/.openclaw/viking-global"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"
SYNC_TO_SHARED=false
AUTO_HOT=false
LAYER="hot"

# 解析参数
if [ $# -lt 1 ]; then
    echo "用法: sv_write_v2 <path> <content> [options]"
    echo "   or: sv_write_v2 --hot <path> <content>"
    echo "   or: sv_write_v2 --shared <content>"
    echo ""
    echo "选项:"
    echo "   --hot      重要记忆，自动同步到共享hot目录"
    echo "   --shared   直接写入共享hot目录"
    echo "   --layer L  指定层级 (hot/warm/cold/archive)"
    exit 1
fi

# 参数解析
POSITIONAL_ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --hot)
            AUTO_HOT=true
            SYNC_TO_SHARED=true
            shift
            ;;
        --shared)
            SYNC_TO_SHARED=true
            shift
            ;;
        --layer)
            LAYER="$2"
            shift 2
            ;;
        -*)
            echo "未知选项: $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}"

# 设置默认值
PATH_ARG="${1:-}"
CONTENT="${2:-}"

# 自动生成日期文件名
if [ -z "$PATH_ARG" ]; then
    TODAY=$(date +%Y-%m-%d)
    PATH_ARG="memory/${TODAY}.md"
fi

# 解析 viking:// 协议或绝对路径
if [[ "$PATH_ARG" == viking://* ]]; then
    REL_PATH="${PATH_ARG#viking://}"
    FULL_PATH="$WORKSPACE/$REL_PATH"
elif [[ "$PATH_ARG" == /* ]]; then
    FULL_PATH="$PATH_ARG"
else
    FULL_PATH="$WORKSPACE/$PATH_ARG"
fi

# 路径遍历检测
if [[ "$FULL_PATH" == *"/../"* ]] || [[ "$FULL_PATH" == "../"* ]]; then
    echo "✗ 禁止路径遍历"
    exit 1
fi

# 确定层级
if [[ "$FULL_PATH" == *"/hot/"* ]]; then
    LAYER="hot"
elif [[ "$FULL_PATH" == *"/warm/"* ]]; then
    LAYER="warm"
elif [[ "$FULL_PATH" == *"/cold/"* ]]; then
    LAYER="cold"
elif [[ "$FULL_PATH" == *"/archive/"* ]]; then
    LAYER="archive"
fi

# 如果是重要标记，自动路由到 hot
if [ "$AUTO_HOT" = true ]; then
    LAYER="hot"
fi

# 确保目录存在
mkdir -p "$(dirname "$FULL_PATH")"

# 生成元数据
MEMORY_ID="mem_$(date +%Y%m%d_%H%M%S)"
CREATED_AT="$(date -Iseconds)"
CURRENT_LAYER="L0"
# 防止 YAML 注入：只接受合法值
case "${IMPORTANCE:-medium}" in
    high|medium|low) ;;
    *) IMPORTANCE="medium" ;;
esac
IMPORTANCE="${IMPORTANCE:-medium}"
WEIGHT=10.0

# CONTENT转义防止注入
CONTENT_ESCAPED=$(printf '%s' "$CONTENT" | sed 's/\\/\\\\/g; s/"/\\"/g; s/`/\\`/g; s/\$/\\$/g')

# 写入记忆文件
cat > "$FULL_PATH" << 'EOF'
---
id: $MEMORY_ID
title: "$(basename "$FULL_PATH" .md)"
importance: $IMPORTANCE
important: $AUTO_HOT
tags: []
created: $CREATED_AT
last_access: $CREATED_AT
access_count: 1
retention: 90
current_layer: $CURRENT_LAYER
target_layer: $LAYER
weight: $WEIGHT
---

$CONTENT_ESCAPED
EOF

echo "✓ 记忆已写入: $FULL_PATH"
echo "  目标层级: $LAYER"
echo "  ID: $MEMORY_ID"

# 自动同步到共享目录（重要记忆）
if [ "$SYNC_TO_SHARED" = true ]; then
    SHARED_DIR="$VIKING_GLOBAL/shared/memory/$LAYER"
    SHARED_PATH="$SHARED_DIR/$(basename "$FULL_PATH")"
    
    mkdir -p "$SHARED_DIR"
    
    # 复制到共享目录（保留完整信息）
    cp "$FULL_PATH" "$SHARED_PATH"
    
    echo "✓ 已同步到共享: $SHARED_PATH"
    
    # 更新共享索引
    INDEX_FILE="$VIKING_GLOBAL/shared/memory/SHARED_INDEX.md"
    if [ -f "$INDEX_FILE" ]; then
        # 检查是否已存在此记录
        if ! grep -q "$MEMORY_ID" "$INDEX_FILE" 2>/dev/null; then
            echo "- $MEMORY_ID | $(basename "$FULL_PATH") | $LAYER | $CREATED_AT" >> "$INDEX_FILE"
        fi
    fi
fi

exit 0
