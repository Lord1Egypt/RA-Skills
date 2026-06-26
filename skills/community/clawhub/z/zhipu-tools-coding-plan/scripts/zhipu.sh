#!/usr/bin/env bash
# 智谱工具统一入口
# 用法: zhipu.sh <command> [args...]
#   search <query> [count]       — 网络搜索
#   reader <url>                 — 网页读取
#   zread search <repo> <query>  — 仓库文档搜索
#   zread structure <repo> [path] — 仓库目录结构
#   zread read <repo> <file>     — 读取仓库文件
#   vision <image> [prompt]      — 图片识别
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 加载 .env 中的 API Key
ENV_FILE="$SCRIPT_DIR/../.env"
if [[ -f "$ENV_FILE" ]]; then
  while IFS='=' read -r key val; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    export "${key}=${val}"
  done < "$ENV_FILE"
fi

CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
  search)
    python3 "$SCRIPT_DIR/zhipu_tool.py" web_search "${1:?搜索关键词不能为空}" --count "${2:-5}"
    ;;
  reader)
    python3 "$SCRIPT_DIR/zhipu_tool.py" web_reader "${1:?URL 不能为空}"
    ;;
  zread)
    python3 "$SCRIPT_DIR/zhipu_tool.py" zread "$@"
    ;;
  vision)
    python3 "$SCRIPT_DIR/zhipu_tool.py" vision "${1:?图片路径不能为空}" --prompt "${2:-请描述这张图片的内容}"
    ;;
  help|*)
    echo "智谱工具 (Coding Plan 免费额度)"
    echo ""
    echo "用法: zhipu.sh <command> [args...]"
    echo ""
    echo "命令:"
    echo "  search <query> [count]         网络搜索"
    echo "  reader <url>                   网页读取"
    echo "  zread search <repo> <query>    仓库文档搜索"
    echo "  zread structure <repo> [path]  仓库目录结构"
    echo "  zread read <repo> <file>       读取仓库文件"
    echo "  vision <image> [prompt]        图片识别"
    ;;
esac
