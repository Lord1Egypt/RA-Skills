#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  probe_xiaodu.sh --url URL [--name 名称] [--no-schema]

示例:
  probe_xiaodu.sh --url "https://speaker.example.com/mcp" --name xiaodu
  probe_xiaodu.sh --url "https://iot.example.com/mcp" --name xiaodu-iot --no-schema
EOF
}

URL=""
NAME="xiaodu"
WITH_SCHEMA=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url)
      URL="${2:-}"
      shift 2
      ;;
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --no-schema)
      WITH_SCHEMA=0
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

if [[ -z "$URL" ]]; then
  echo "必须提供 --url" >&2
  usage >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

echo "[xiaodu-control] 正在探测服务 '$NAME'"
mcporter list --http-url "$URL" --name "$NAME"

if [[ "$WITH_SCHEMA" -eq 1 ]]; then
  echo
  echo "[xiaodu-control] 正在获取 '$NAME' 的 schema"
  mcporter list --http-url "$URL" --name "$NAME" --schema
fi

cat <<EOF

[xiaodu-control] 下一步建议
- 如果这个端点使用 OAuth，可以这样保存：
  mcporter config add $NAME --url "$URL" --scope home --auth oauth
  mcporter auth $NAME
- 如果这个端点使用 bearer 鉴权，把 header 写进 mcporter 配置后再重试：
  mcporter list $NAME --schema
EOF
