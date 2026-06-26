#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# perplexity-search-call.sh — 调用 Perplexity Search API
#
# 直接返回结构化文章列表（title、url、date、snippet），不经过 OpenClaw web_search。
# 需设置环境变量 PERPLEXITY_API_KEY（可在 openclaw.json 的 env 块中配置）。
#
# 依赖：Node.js >= 18，同目录下 perplexity-search-call.mjs
#
# 用法（推荐 stdin 方式，避免 exec 工具传中文 argv 时编码损坏）：
#   bash perplexity-search-call.sh <<'ARGS_EOF'
#   {"query":"AI 大模型 最新进展","max_results":10,"search_recency_filter":"day"}
#   ARGS_EOF
#
# 兼容 argv 方式（仅适用于纯 ASCII 参数）：
#   bash perplexity-search-call.sh '{"query":"keyword","max_results":10}'
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

TMP_ARGS="$(mktemp)"

if [ ! -t 0 ]; then
  # stdin 模式：从 pipe / heredoc 读取 JSON（推荐，可安全传递中文等非 ASCII）
  cat > "$TMP_ARGS"
elif [ $# -gt 0 ] && [ -n "${1:-}" ]; then
  # argv 模式：向后兼容（仅适用于纯 ASCII 参数）
  printf '%s' "$1" > "$TMP_ARGS"
else
  printf '{}' > "$TMP_ARGS"
fi

exec node "$SCRIPT_DIR/perplexity-search-call.mjs" "$TMP_ARGS"
