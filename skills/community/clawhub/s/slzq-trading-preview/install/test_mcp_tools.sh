#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="slzq-trading"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEGACY_MCP_DIR="$(cd "${ROOT_DIR}/.." && pwd)/${SKILL_NAME}-mcp"

if [ -f "${ROOT_DIR}/runtime/mcp/scripts/test-mcp-tools.mjs" ]; then
  cd "${ROOT_DIR}/runtime/mcp"
  if [ ! -d node_modules ]; then
    echo "INFO: runtime/mcp 缺少 node_modules，正在执行 npm ci..."
    npm ci
  fi
  node scripts/test-mcp-tools.mjs
elif [ -f "${LEGACY_MCP_DIR}/scripts/test-mcp-tools.mjs" ]; then
  cd "${LEGACY_MCP_DIR}"
  if [ ! -d node_modules ]; then
    echo "INFO: ${SKILL_NAME}-mcp 缺少 node_modules，正在执行 npm ci..."
    npm ci
  fi
  node scripts/test-mcp-tools.mjs
else
  echo "FAIL: 未找到 MCP tools/list 自检脚本"
  echo "下一步：请确认已下载新版能力包，或重新构建 ${SKILL_NAME}-mcp。"
  exit 1
fi
