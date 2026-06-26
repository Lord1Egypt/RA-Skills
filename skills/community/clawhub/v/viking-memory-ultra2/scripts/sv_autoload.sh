#!/bin/bash
# Viking Memory System - sv_autoload
# 会话开始时自动加载记忆
#
# 用法: sv_autoload.sh [--limit N] [--layer L0,L1] [--promote]

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"
LIMIT=5
LAYERS="L0,L1"
MAX_CONTENT_CHARS=500   # 每条记忆最大内容长度（防Token耗尽）
PROMOTE_AFTER_LOAD=false  # 动态回流开关
UPDATE_WEIGHT=false      # Phase 2 权重更新开关

while [ $# -gt 0 ]; do
    case "$1" in
        --limit) LIMIT="$2"; shift 2 ;;
        --layer) LAYERS="$2"; shift 2 ;;
        --promote) PROMOTE_AFTER_LOAD=true; shift ;;
        --update-weight) UPDATE_WEIGHT=true; shift ;;
        *) shift ;;
    esac
done

echo "=== Viking 记忆自动加载 ==="
echo "工作空间: $WORKSPACE"
echo "加载数量: $LIMIT"
echo "层级: $LAYERS"
echo "---"

SEARCH_DIR="$WORKSPACE/agent/memories"
[ ! -d "$SEARCH_DIR" ] && { echo "⚠ 记忆目录不存在"; exit 0; }

# 安全解析 frontmatter（仅 --- 块内）
parse_fm() {
    awk -v key="$2" -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; next }
        /^---$/ && in_fm { exit }
        in_fm && $0 ~ "^" key ": *" {
            sub("^" key ": *", "")
            gsub(/^[ \t]+|[ \t]+$/, "")
            print; exit
        }
    ' "$1" 2>/dev/null
}

# 收集记忆
declare -a MEMORIES
while IFS= read -r file; do
    WEIGHT=$(parse_fm "$file" "weight")
    LAYER=$(parse_fm "$file" "current_layer")
    [ -z "$WEIGHT" ] && WEIGHT="0"
    [ -z "$LAYER" ] && LAYER="L0"

    # 层级过滤
    MATCH=false
    IFS=',' read -ra LAYER_ARR <<< "$LAYERS"
    for l in "${LAYER_ARR[@]}"; do
        [ "$LAYER" = "$l" ] && MATCH=true
    done
    [ "$MATCH" = false ] && continue

    MEMORIES+=("$WEIGHT|$file")
done < <(find "$SEARCH_DIR" -name "*.md" -type f 2>/dev/null)

# 按权重排序
if [ ${#MEMORIES[@]} -eq 0 ]; then
    SORTED=()
else
    IFS=$'\n' SORTED=($(sort -r <<<"${MEMORIES[*]}")); unset IFS
fi

# 显示并加载
COUNT=0
for entry in "${SORTED[@]}"; do
    [ $COUNT -ge $LIMIT ] && break

    FILE="${entry#*|}"

    LAYER=$(parse_fm "$FILE" "current_layer")
    IMPORTANCE=$(parse_fm "$FILE" "importance")
    WEIGHT=$(parse_fm "$FILE" "weight")
    ACCESS_COUNT=$(parse_fm "$FILE" "access_count")

    [ -z "$LAYER" ] && LAYER="L0"
    [ -z "$IMPORTANCE" ] && IMPORTANCE="medium"
    [ -z "$WEIGHT" ] && WEIGHT="0"
    [ -z "$ACCESS_COUNT" ] || ! [[ "$ACCESS_COUNT" =~ ^[0-9]+$ ]] && ACCESS_COUNT=0

    echo "---"
    echo "📄 $(basename -- "$FILE")"
    echo "   [$LAYER] 重要性: $IMPORTANCE | 权重: $WEIGHT"

    # 显示内容片段（限制行数，防Token耗尽）
    # 跳过 frontmatter，取正文前5行
    CONTENT=$(sed -n '/^---$/,/^---$/d; p' "$FILE" 2>/dev/null | head -5)
    echo "$CONTENT" | sed 's/^/   /'

    # 更新访问计数
    NEW_COUNT=$((ACCESS_COUNT + 1))
    sed -i "s/^access_count:.*/access_count: $NEW_COUNT/" "$FILE" 2>/dev/null || \
        echo "⚠ 访问计数更新失败: $FILE"

    COUNT=$((COUNT + 1))
done

echo ""
echo "✓ 加载完成: $COUNT 条记忆"

# ============ Phase 2: 更新权重（含上下文相关性）============
# 每次加载后，用 sv_weight --update 更新记忆权重
# 上下文相关性默认 1.0，可通过环境变量 CONTEXT_CORRELATION 设置
if [ "$UPDATE_WEIGHT" = true ]; then
    echo ""
    echo "=== Phase 2: 权重更新 ==="
    CONTEXT_CORRELATION="${CONTEXT_CORRELATION:-1.0}"
    for entry in "${SORTED[@]}"; do
        FILE="${entry#*|}"
        "$VIKING_HOME/scripts/sv_weight.sh" "$FILE" --update --context-correlation "$CONTEXT_CORRELATION" 2>/dev/null || true
    done
    echo "✓ 权重更新完成"
fi

# ============ 动态回流机制 ============
# 如果指定 --promote，加载完成后检查 cold/archive 层是否有需要晋升的记忆
if [ "$PROMOTE_AFTER_LOAD" = true ]; then
    echo ""
    echo "=== 动态回流检查 ==="
    # 获取当前加载的记忆内容片段作为上下文
    PROMPT_CONTEXT="近期工作："
    for entry in "${SORTED[@]}"; do
        [ $COUNT -ge 3 ] && break
        FILE="${entry#*|}"
        CONTENT=$(sed -n '/^---$/,/^---$/d; p' "$FILE" 2>/dev/null | head -c 200)
        PROMPT_CONTEXT="$PROMPT_CONTEXT $(basename -- "$FILE"): $CONTENT;"
        COUNT=$((COUNT + 1))
    done

    # 调用晋升脚本（使用 DRY_RUN=false）
    "$VIKING_HOME/scripts/sv_promote.sh" --context "$PROMPT_CONTEXT" --threshold 0.7 --layer cold,archive 2>/dev/null || true
fi

exit 0
