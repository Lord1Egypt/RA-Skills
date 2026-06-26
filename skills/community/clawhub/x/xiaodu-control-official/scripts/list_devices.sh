#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  list_devices.sh [--server 服务名] [--out 输出文件]

示例:
  list_devices.sh
  list_devices.sh --server xiaodu --out /tmp/xiaodu-devices.json
EOF
}

SERVER="xiaodu"
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="${2:-}"
      shift 2
      ;;
    --out)
      OUT="${2:-}"
      shift 2
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

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

if [[ -n "$OUT" ]]; then
  mcporter call "${SERVER}.list_user_devices" --output json >"$OUT"
  echo "$OUT"
  exit 0
fi

mcporter call "${SERVER}.list_user_devices" --output json
