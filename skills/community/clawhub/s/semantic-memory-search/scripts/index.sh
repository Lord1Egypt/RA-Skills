#!/bin/bash
# Semantic Memory Search - 索引记忆文件

set -e

MEMSEARCH=~/Library/Python/3.14/bin/memsearch
MEMORY_PATH=~/.openclaw/workspace/memory/

echo "🔍 索引 OpenClaw 记忆文件..."
echo "📁 路径: $MEMORY_PATH"
echo ""

KMP_DUPLICATE_LIB_OK=TRUE $MEMSEARCH index "$MEMORY_PATH"

echo ""
echo "✅ 索引完成！"
echo ""
echo "搜索示例:"
echo "  KMP_DUPLICATE_LIB_OK=TRUE $MEMSEARCH search \"你的搜索词\""
