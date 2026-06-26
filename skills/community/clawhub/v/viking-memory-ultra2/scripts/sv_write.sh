#!/bin/bash
# Viking Memory System - sv_write
# 写入记忆到 Viking 工作空间

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
CONFIG_FILE="$VIKING_HOME/config.yaml"

# 解析参数
DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    shift
fi

if [ $# -lt 2 ]; then
    echo "用法: sv_write [--dry-run] <path> <content>"
    echo "示例: sv_write --dry-run viking://agent/memories/hot/2026-03-16.md '# 今日工作'"
    exit 1
fi

PATH_ARG="$1"
CONTENT="$2"
LAYER="hot"

# 解析 viking:// 协议
if [[ "$PATH_ARG" == viking://* ]]; then
    REL_PATH="${PATH_ARG#viking://}"
    WORKSPACE="${SV_WORKSPACE:-$VIKING_HOME}"
    FULL_PATH="$WORKSPACE/$REL_PATH"
else
    FULL_PATH="$PATH_ARG"
    REL_PATH="$PATH_ARG"
fi

# 路径遍历检测 + realpath 安全边界检查
if [[ "$FULL_PATH" == *"/../"* ]] || [[ "$FULL_PATH" == "../"* ]]; then
    echo "✗ 禁止路径遍历"
    exit 1
fi
# 使用 realpath 确保路径不逃逸 SV_WORKSPACE
RESOLVED=$(realpath "$FULL_PATH" 2>/dev/null) || RESOLVED="$FULL_PATH"
WORKSPACE_ABS=$(realpath "$WORKSPACE" 2>/dev/null || echo "$WORKSPACE")
if [[ ! "$RESOLVED" =~ ^"$WORKSPACE_ABS" ]]; then
    echo "✗ 路径超出工作空间边界: $RESOLVED"
    exit 1
fi

# 自动分类到正确层级
if [[ "$FULL_PATH" == *"/hot/"* ]]; then
    LAYER="hot"
elif [[ "$FULL_PATH" == *"/warm/"* ]]; then
    LAYER="warm"
elif [[ "$FULL_PATH" == *"/cold/"* ]]; then
    LAYER="cold"
elif [[ "$FULL_PATH" == *"/archive/"* ]]; then
    LAYER="archive"
fi

# 确保目录存在
mkdir -p "$(dirname "$FULL_PATH")"

# 生成元数据（提前到Dry-run前）
# Bug Fix: current_layer 应该跟随实际目录层级，而非固定 L0
MEMORY_ID="mem_$(date +%Y%m%d_%H%M%S)"
CREATED_AT="$(date -Iseconds)"
CURRENT_LAYER="$LAYER"   # current_layer 与目录路径保持一致
case "${IMPORTANCE:-medium}" in
    high|medium|low) IMPORTANCE="${IMPORTANCE:-medium}" ;;
    *) IMPORTANCE="medium" ;;
esac
WEIGHT=10.0

# Dry-run 模式预览
if [ "$DRY_RUN" = true ]; then
    echo "🔍 [DRY-RUN] 记忆预览:"
    echo "  路径: $FULL_PATH"
    echo "  层级: $LAYER"
    echo "  ID: $MEMORY_ID"
    echo "  标题: $(basename "$FULL_PATH" .md)"
    echo "  内容: ${CONTENT:0:80}${CONTENT:+...}"
    echo ""
    echo "如需实际写入，去掉 --dry-run"
    exit 0
fi

# CONTENT转义防止注入（保留换行等格式）
CONTENT_SAFE=$(printf '%s' "$CONTENT" | sed 's/\\/\\\\/g; s/"/\\"/g')

# 写入记忆文件（使用<<-EOF允许变量展开，-表示去除tab缩进）
cat > "$FULL_PATH" <<-FRONTMATTER
	---
	id: $MEMORY_ID
	title: "$(basename "$FULL_PATH" .md)"
	importance: $IMPORTANCE
	important: false
	tags: []
	created: $CREATED_AT
	last_access: $CREATED_AT
	access_count: 1
	retention: 90
	current_layer: $CURRENT_LAYER
	target_layer: $LAYER
	weight: $WEIGHT
	---
	
	$CONTENT_SAFE
FRONTMATTER

echo "✓ 记忆已写入: $FULL_PATH"
echo "  目标层级: $LAYER"
echo "  ID: $MEMORY_ID"

exit 0
