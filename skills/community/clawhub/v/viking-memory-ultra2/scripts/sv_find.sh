#!/bin/bash
# Viking Memory System - sv_find
# 搜索记忆关键词，支持 LLM 回忆
#
# 用法: sv_find <关键词> [选项]
#       sv_find "项目" --layer hot
#       sv_find --archived "关键词"

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"

# 加载 LLM 接口（如果存在）
[ -f "$VIKING_HOME/scripts/llm_interface.sh" ] && source "$VIKING_HOME/scripts/llm_interface.sh"

# 默认参数
QUERY=""
LAYER=""
SEARCH_ARCHIVED=false
MAX_RESULTS=20
MAX_CONTENT_CHARS=500  # 防Token耗尽

# 解析参数
while [ $# -gt 0 ]; do
    case "$1" in
        --layer) LAYER="$2"; shift 2 ;;
        --archived)
            SEARCH_ARCHIVED=true
            QUERY="$2"; shift 2 ;;
        --max) MAX_RESULTS="$2"; shift 2 ;;
        --*) echo "未知选项: $1"; exit 1 ;;
        *) [ -z "$QUERY" ] && QUERY="$1"; shift ;;
    esac
done

[ -z "$QUERY" ] && { echo "用法: sv_find <关键词> [--layer hot] [--archived]"; exit 1; }

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

echo "=== Viking 记忆搜索 ==="
echo "关键词: $QUERY"
[ -n "$LAYER" ] && echo "层级过滤: $LAYER"
echo "---"

# 确定搜索目录（Bug Fix: 原来漏了 hot/warm/cold 层！）
if [ "$SEARCH_ARCHIVED" = true ]; then
    SEARCH_DIRS="$WORKSPACE/agent/memories/archive $WORKSPACE/memory"
    echo "📂 归档目录"
else
    # 默认搜索所有活跃层级
    SEARCH_DIRS="$WORKSPACE/agent/memories/hot $WORKSPACE/agent/memories/warm $WORKSPACE/agent/memories/cold $WORKSPACE/agent/memories/daily $WORKSPACE/memory"
    echo "📂 全量搜索"
fi

# 收集文件
RESULTS=""
for dir in $SEARCH_DIRS; do
    [ -d "$dir" ] && RESULTS="$RESULTS$(find "$dir" -name "*.md" -type f 2>/dev/null)"$'\n'
done

[ -z "$(echo "$RESULTS" | tr -d '\n')" ] && { echo "未找到任何记忆文件"; exit 0; }

COUNT=0
ALL_MATCH_CONTENT=""
while IFS= read -r file; do
    [ -z "$file" ] && continue
    [ $COUNT -ge $MAX_RESULTS ] && break

    # 层级过滤（从目录路径推断，而非 frontmatter——因为迁移后 current_layer 可能未同步）
    if [ -n "$LAYER" ]; then
        FILE_LAYER=$(basename "$(dirname -- "$file")")
        # 特殊：daily/long-term 的父目录是 memories，需要再往上
        if [ "$FILE_LAYER" = "memories" ]; then
            FILE_LAYER=$(basename "$(dirname -- "$(dirname -- "$file")")")
        fi
        [ "$FILE_LAYER" != "$LAYER" ] && continue
    fi

    # 读取内容并搜索
    FILE_CONTENT=$(cat "$file" 2>/dev/null || continue)
    if ! echo "$FILE_CONTENT" | grep -Fiq "$QUERY" 2>/dev/null; then
        continue
    fi

    # 安全提取 frontmatter
    IMPORTANCE=$(parse_fm "$file" "importance")
    FILE_WEIGHT=$(parse_fm "$file" "weight")
    FILE_LAYER=$(parse_fm "$file" "current_layer")
    [ -z "$IMPORTANCE" ] && IMPORTANCE="medium"
    [ -z "$FILE_WEIGHT" ] && FILE_WEIGHT="0"
    [ -z "$FILE_LAYER" ] && FILE_LAYER="L0"

    echo "---"
    echo "📄 $(basename -- "$file")"
    echo "   [$FILE_LAYER] imp:$IMPORTANCE w:$FILE_WEIGHT"

    # 显示匹配片段（前3行）
    MATCH_LINES=$(echo "$FILE_CONTENT" | grep -Fi "$QUERY" 2>/dev/null | head -3 || true)
    [ -n "$MATCH_LINES" ] && echo "$MATCH_LINES" | sed 's/^/   /'

    # 收集内容（跳过 frontmatter，限制长度）
    CONTENT=$(echo "$FILE_CONTENT" | sed -n '/^---$/,/^---$/d; p' | head -c $MAX_CONTENT_CHARS)
    [ -z "$CONTENT" ] && CONTENT="(无正文)"
    ALL_MATCH_CONTENT="${ALL_MATCH_CONTENT}
=== $(basename -- "$file") ===
${CONTENT}
"

    COUNT=$((COUNT + 1))
done <<< "$RESULTS"

echo ""
echo "✓ 找到 $COUNT 条匹配记忆"

# LLM 语义增强（如果有 llm_recall 函数）
if [ $COUNT -gt 0 ] && declare -f llm_recall > /dev/null 2>&1; then
    echo ""
    echo "=== LLM 语义增强 ==="
    printf '%s' "$ALL_MATCH_CONTENT" | llm_recall /dev/stdin "$QUERY" 2>/dev/null || true
fi

exit 0
