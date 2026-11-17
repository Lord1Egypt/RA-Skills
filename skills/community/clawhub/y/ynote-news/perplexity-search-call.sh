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

# ─── 1. 读取 API Key（env → 传给 .mjs，避免 .mjs 直接访问 env） ───

API_KEY="${PERPLEXITY_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo '错误：未设置 PERPLEXITY_API_KEY' >&2
  echo '请在 OpenClaw config 的 youdaonote-news.env 中配置 PERPLEXITY_API_KEY，或在 shell 中 export。Key 获取：https://www.perplexity.ai/settings/api' >&2
  exit 1
fi

# ─── 2. 读取参数 JSON（stdin / argv / 临时文件 → 解析后传给 .mjs） ───

ARGS_JSON=""
if [ ! -t 0 ]; then
  # stdin 模式：从 pipe / heredoc 读取 JSON（推荐，可安全传递中文等非 ASCII）
  ARGS_JSON="$(cat)"
elif [ $# -gt 0 ] && [ -n "${1:-}" ]; then
  # 检查 argv 是否为临时文件路径
  if [ -f "$1" ]; then
    TMPDIR_RESOLVED="$(cd "${TMPDIR:-/tmp}" && pwd)"
    RESOLVED_PATH="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
    case "$RESOLVED_PATH" in
      "$TMPDIR_RESOLVED"/*)
        ARGS_JSON="$(cat "$1")"
        rm -f "$1"
        ;;
      *)
        # 非 tmp 目录的文件路径，当做内联 JSON
        ARGS_JSON="$1"
        ;;
    esac
  else
    # argv 模式：向后兼容（仅适用于纯 ASCII 参数）
    ARGS_JSON="$1"
  fi
else
  ARGS_JSON='{}'
fi

# ─── 3. 调用 .mjs（传递 apiKey 和 argsJson 作为 argv） ───

exec node "$SCRIPT_DIR/perplexity-search-call.mjs" "$API_KEY" "$ARGS_JSON"
