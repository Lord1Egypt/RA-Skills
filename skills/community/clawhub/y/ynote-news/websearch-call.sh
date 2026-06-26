#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# websearch-call.sh — 调用 open-websearch MCP（stdio，不依赖 OpenClaw mcpServers）
#
# 用法与 mcp-call.sh 一致：<tool_name> '<json_args>'。当前仅支持 tool：search。
# 依赖：Node.js（含 npx）、同目录下 websearch-call.mjs
#
# 示例：
#   bash websearch-call.sh search '{"query":"关键词","limit":10,"engines":["duckduckgo","bing"]}'
# ─────────────────────────────────────────────

# 兼容两种用法：双参数 search '{"query":"..."}' 或 单参数 '{"query":"..."}'（默认 tool 为 search）
if [ -n "${2+set}" ]; then
  TOOL_NAME="$1"
  TOOL_ARGS="$2"
else
  TOOL_NAME="search"
  TOOL_ARGS="${1:-{}}"
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/websearch-call.mjs" "$TOOL_NAME" "$TOOL_ARGS"
