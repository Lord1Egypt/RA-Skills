#!/bin/bash
# Skillhub 搜索脚本 - 仅搜索，不访问本地文件
# 用法: ./search.sh <关键词> [数量限制]

QUERY="$1"
LIMIT="${2:-10}"

if [ -z "$QUERY" ]; then
    echo "用法: $0 <关键词> [数量限制]"
    echo ""
    echo "示例:"
    echo "  $0 calendar"
    echo "  $0 \"code review\" 5"
    exit 1
fi

# 使用环境变量或默认值
API_URL="${SKILLS_API_URL:-https://skills.volces.com/v1}"

echo "🔍 搜索 Skillhub: $QUERY"
echo ""

# 纯搜索操作，不访问本地文件
SKILLS_API_URL="$API_URL" npx -y skills find "$QUERY" --limit "$LIMIT" 2>/dev/null || {
    echo "搜索失败，请检查网络连接"
    exit 1
}
