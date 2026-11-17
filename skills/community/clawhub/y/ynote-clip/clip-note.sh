#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# clip-note.sh — 网页剪藏入口（三阶段流水线主控）
#
# 职责：
#   1. 读取环境变量，通过 argv 传给 clip-note.mjs
#   2. 对不涉及图片的模式（--clip-web-page / --create-note）直接透传
#   3. 对图片剪藏模式，执行三阶段流水线：
#      阶段 1: clip-note.mjs --download-images（并发下载图片）
#      阶段 2: compress-image.sh（sips/convert 压缩 + base64）
#      阶段 3: clip-note.mjs --upload（stdin 接收 payload → MCP 上传）
#
# 用法：bash clip-note.sh [所有原 clip-note.mjs 参数]
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── env → argv ──
ENV_ARGS=()
[ -n "${YOUDAONOTE_API_KEY:-}" ]      && ENV_ARGS+=(--api-key "$YOUDAONOTE_API_KEY")
[ -n "${YOUDAONOTE_MCP_URL:-}" ]      && ENV_ARGS+=(--sse-url "$YOUDAONOTE_MCP_URL")
[ -n "${YOUDAONOTE_MCP_TIMEOUT:-}" ]  && ENV_ARGS+=(--mcp-timeout "$YOUDAONOTE_MCP_TIMEOUT")
[ -n "${YOUDAONOTE_CLIP_DEBUG:-}" ]   && ENV_ARGS+=(--debug-dir "$YOUDAONOTE_CLIP_DEBUG")

# ── 透传模式：不涉及图片处理的模式直接转发给 .mjs ──
for arg in "$@"; do
  if [[ "$arg" == "--clip-web-page" || "$arg" == "--create-note" ]]; then
    exec node "$SCRIPT_DIR/clip-note.mjs" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} "$@"
  fi
done

# ── 图片剪藏模式：解析参数 ──
DATA_FILE=""
BODY_FILE=""
SOURCE_URL=""
TITLE=""
IMAGE_URLS="[]"
MARKDOWN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --data-file)    DATA_FILE="$2"; shift 2 ;;
    --body-file)    BODY_FILE="$2"; shift 2 ;;
    --source-url)   SOURCE_URL="$2"; shift 2 ;;
    --title)        TITLE="$2"; shift 2 ;;
    --image-urls)   IMAGE_URLS="$2"; shift 2 ;;
    --markdown)     MARKDOWN=true; shift ;;
    *)              shift ;;  # 忽略未识别参数
  esac
done

# ── 预读 data-file / body-file（.sh 层读文件，.mjs 不再 readFileSync）──
BODY_HTML=""
DEBUG_KEY=""

sanitize_title() {
  local raw="$1"
  local max_len="${2:-80}"
  local sanitized
  sanitized=$(echo "$raw" | sed 's/[\\/<>:*?""]/_/g')
  if [ ${#sanitized} -gt "$max_len" ]; then
    sanitized="${sanitized:0:$max_len}"
  fi
  echo "${sanitized}.clip"
}

if [ -n "$DATA_FILE" ]; then
  if [ ! -f "$DATA_FILE" ]; then
    echo "错误：data-file 不存在: $DATA_FILE" >&2
    exit 1
  fi
  BODY_HTML=$(jq -r '.content // ""' "$DATA_FILE")
  IMAGE_URLS=$(jq -r '.imageUrls // [] | tojson' "$DATA_FILE")
  TITLE=$(sanitize_title "$(jq -r '.title // ""' "$DATA_FILE")")
  SOURCE_URL_DATA=$(jq -r '.source // ""' "$DATA_FILE")
  [ -z "$SOURCE_URL" ] && SOURCE_URL="$SOURCE_URL_DATA"
  DEBUG_KEY=$(jq -r '._debugKey // ""' "$DATA_FILE")

  if [ -z "$TITLE" ] || [ "$TITLE" = ".clip" ]; then
    echo "错误：data-file 中缺少 title" >&2
    exit 1
  fi
  if [ -z "$BODY_HTML" ]; then
    echo "错误：data-file 中缺少 content" >&2
    exit 1
  fi

  # 调试：复制 data-file 到日志目录
  if [ -n "${YOUDAONOTE_CLIP_DEBUG:-}" ] && [ -n "$DEBUG_KEY" ]; then
    LOG_DIR="${YOUDAONOTE_CLIP_DEBUG}/${DEBUG_KEY}"
    mkdir -p "$LOG_DIR" 2>/dev/null || true
    jq '{title, source, imageUrls: (.imageUrls | length), contentLength: (.content | length), _debugKey, _source}' "$DATA_FILE" > "$LOG_DIR/data-file.json" 2>/dev/null || true
  fi

elif [ -n "$BODY_FILE" ]; then
  if [ ! -f "$BODY_FILE" ]; then
    echo "错误：body-file 不存在: $BODY_FILE" >&2
    exit 1
  fi
  BODY_HTML=$(cat "$BODY_FILE")
  if [ -z "$TITLE" ]; then
    echo "错误：缺少 --title" >&2
    exit 1
  fi
  if [ -z "$SOURCE_URL" ]; then
    echo "错误：缺少 --source-url" >&2
    exit 1
  fi
else
  echo "错误：缺少 --data-file 或 --body-file" >&2
  exit 1
fi

# ── 三阶段流水线 ──

TMP_DIR=$(mktemp -d /tmp/youdaonote-clip-XXXXXX)
trap 'rm -rf "$TMP_DIR"' EXIT

# 阶段 1：下载图片
node "$SCRIPT_DIR/clip-note.mjs" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} \
  --download-images \
  --image-urls "$IMAGE_URLS" \
  --source-url "$SOURCE_URL" \
  --tmp-dir "$TMP_DIR"

# 阶段 2：压缩 + base64
if [ -f "$TMP_DIR/manifest.json" ]; then
  MANIFEST_COUNT=$(jq 'length' "$TMP_DIR/manifest.json")
  if [ "$MANIFEST_COUNT" -gt 0 ]; then
    bash "$SCRIPT_DIR/compress-image.sh" "$TMP_DIR/manifest.json"
  fi
fi

# 阶段 3：组装 payload + 上传（bodyHtml 写入临时文件避免 ARG_MAX 限制）
printf '%s' "$BODY_HTML" > "$TMP_DIR/body.html"
jq -n \
  --arg title "$TITLE" \
  --rawfile bodyHtml "$TMP_DIR/body.html" \
  --arg sourceUrl "$SOURCE_URL" \
  --argjson markdown "$MARKDOWN" \
  --arg debugKey "$DEBUG_KEY" \
  --slurpfile images "$TMP_DIR/manifest.json" \
  '{title:$title, bodyHtml:$bodyHtml, sourceUrl:$sourceUrl, markdown:$markdown, _debugKey:$debugKey, images:$images[0]}' \
| node "$SCRIPT_DIR/clip-note.mjs" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} --upload
