#!/bin/bash
# HIIC 产业日报生成器启动脚本（带代理）
# 用法: ./run-with-proxy.sh "关键词1,关键词2" [maxResults] [output]

# 配置代理
export HTTP_PROXY=http://127.0.0.1:7899
export HTTPS_PROXY=http://127.0.0.1:7899

# 设置 Node.js 选项
export NODE_OPTIONS="--max-old-space-size=4096"

# 运行脚本
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$1" ]; then
  echo "用法: $0 <keywords> [maxResults] [output]"
  echo ""
  echo "示例:"
  echo "  $0 \"油价,石油,原油,OPEC,中石油,炼油\" 30"
  echo "  $0 \"油价,石油\" 20 report.md"
  exit 1
fi

KEYWORDS="$1"
MAX_RESULTS="${2:-30}"
OUTPUT="${3:-}"

CMD="node \"$SCRIPT_DIR/generate-report-v7.1.mjs\" --keywords \"$KEYWORDS\" --maxResults \"$MAX_RESULTS\" --proxy \"http://127.0.0.1:7899\" --verbose"

if [ -n "$OUTPUT" ]; then
  CMD="$CMD --output \"$OUTPUT\""
fi

echo "🚀 启动日报生成器（代理模式）"
echo "📍 代理: $HTTP_PROXY"
echo "🔍 关键词: $KEYWORDS"
echo "📊 最大结果: $MAX_RESULTS"
echo ""

eval $CMD
