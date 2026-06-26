#!/bin/bash
# Semantic Memory Search - 搜索记忆

set -e

MEMSEARCH=~/Library/Python/3.14/bin/memsearch

if [ -z "$1" ]; then
    echo "用法: $0 \"搜索词\""
    echo ""
    echo "示例:"
    echo "  $0 \"Discord 频道重组\""
    echo "  $0 \"播客制作流程\""
    echo "  $0 \"财报跟踪配置\""
    exit 1
fi

QUERY="$1"

echo "🔍 搜索: $QUERY"
echo ""

KMP_DUPLICATE_LIB_OK=TRUE $MEMSEARCH search "$QUERY"
