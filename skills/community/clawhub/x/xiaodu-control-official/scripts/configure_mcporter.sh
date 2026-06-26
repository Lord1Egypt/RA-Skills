#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  configure_mcporter.sh --token ACCESS_TOKEN [--no-verify]
  configure_mcporter.sh --text "授权页复制的整段文本" [--no-verify]
  configure_mcporter.sh --text "授权页复制的整段文本" --check-only
  printf '%s\n' "授权页复制的整段文本" | configure_mcporter.sh

说明:
  只配置 mcporter 的 xiaodu / xiaodu-iot server。
  不安装或升级 OpenClaw/Hermes 插件，不写 OpenClaw channel 配置。
EOF
}

BASE_URL="https://xiaodu.baidu.com/dueros_mcp_server/mcp/"
TOKEN=""
TEXT=""
VERIFY=1
CHECK_ONLY=0

extract_token() {
  local input="$1"
  local token=""

  token="$(
    printf '%s\n' "$input" \
      | grep -Eo 'AccessToken[[:space:]]*为[[:space:]]*xiaodu-[A-Za-z0-9_-]+' \
      | sed -E 's/^.*为[[:space:]]*//' \
      | head -n 1 || true
  )"

  if [[ -z "$token" ]]; then
    token="$(
      printf '%s\n' "$input" \
        | grep -Eo 'xiaodu-[A-Za-z0-9_-]+' \
        | head -n 1 || true
    )"
  fi

  printf '%s\n' "$token"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --token)
      TOKEN="${2:-}"
      shift 2
      ;;
    --text)
      TEXT="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --no-verify)
      VERIFY=0
      shift
      ;;
    --check-only)
      CHECK_ONLY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TOKEN" ]]; then
  if [[ -z "$TEXT" && ! -t 0 ]]; then
    TEXT="$(cat)"
  fi
  TOKEN="$(extract_token "$TEXT")"
fi

if [[ -z "$TOKEN" ]]; then
  echo "未识别到 AccessToken。请粘贴授权页生成的完整文本，格式应包含 AccessToken为xiaodu-..." >&2
  exit 1
fi

if [[ ! "$TOKEN" =~ ^xiaodu-[A-Za-z0-9_-]+$ ]]; then
  echo "AccessToken 格式不合法。期望格式为 xiaodu-xxxx。" >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "当前缺少 mcporter，无法写入小度 MCP 配置。请先安装 mcporter 后重新粘贴授权文本。" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "当前缺少 npx，无法配置 xiaodu-iot。请先安装 Node.js/npm 后重新粘贴授权文本。" >&2
  exit 1
fi

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  echo "[xiaodu-control] check-only：已识别 AccessToken，依赖检查通过；不会写入 mcporter 配置"
  if [[ "$VERIFY" -eq 1 ]]; then
    echo "[xiaodu-control] check-only：真实执行时会验证 xiaodu 和 xiaodu-iot schema"
  fi
  exit 0
fi

echo "[xiaodu-control] 正在写入 mcporter home 配置: xiaodu"
mcporter config add xiaodu \
  --url "$BASE_URL" \
  --header "ACCESS_TOKEN=$TOKEN" \
  --scope home

echo "[xiaodu-control] 正在写入 mcporter home 配置: xiaodu-iot"
mcporter config add xiaodu-iot \
  --command npx \
  --arg -y \
  --arg dueros-iot-mcp \
  --env "ACCESS_TOKEN=$TOKEN" \
  --scope home

if [[ "$VERIFY" -eq 1 ]]; then
  echo "[xiaodu-control] 正在验证 xiaodu schema"
  mcporter list xiaodu --schema

  echo "[xiaodu-control] 正在验证 xiaodu-iot schema"
  mcporter list xiaodu-iot --schema
fi

echo "[xiaodu-control] 配置完成"
