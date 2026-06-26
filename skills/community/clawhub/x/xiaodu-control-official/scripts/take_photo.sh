#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  take_photo.sh [--device-name 设备名 | --cuid ID --client-id ID] [--server 服务名] [--out 输出文件]

示例:
  take_photo.sh --device-name "小度智能屏3"
  take_photo.sh --cuid abc --client-id xyz --out /tmp/xiaodu-photo.json
EOF
}

SERVER="xiaodu"
DEVICE_NAME=""
CUID=""
CLIENT_ID=""
OUT=""

resolve_device_identifiers() {
  local resolved_fields=()
  local field=""
  while IFS= read -r -d '' field; do
    resolved_fields+=("$field")
  done < <(
    python3 "$(dirname "$0")/device_resolver.py" \
      --server "$SERVER" \
      --device-name "$DEVICE_NAME" \
      --format nul
  )

  if [[ "${#resolved_fields[@]}" -ne 3 ]]; then
    echo "设备解析返回了意外字段数: ${#resolved_fields[@]}" >&2
    exit 1
  fi

  DEVICE_NAME="${resolved_fields[0]}"
  CUID="${resolved_fields[1]}"
  CLIENT_ID="${resolved_fields[2]}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="${2:-}"
      shift 2
      ;;
    --device-name)
      DEVICE_NAME="${2:-}"
      shift 2
      ;;
    --cuid)
      CUID="${2:-}"
      shift 2
      ;;
    --client-id)
      CLIENT_ID="${2:-}"
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

if [[ -z "$DEVICE_NAME" && ( -z "$CUID" || -z "$CLIENT_ID" ) ]]; then
  echo "必须提供 --device-name，或者同时提供 --cuid 和 --client-id" >&2
  usage >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

if [[ -n "$DEVICE_NAME" ]]; then
  resolve_device_identifiers
fi

if [[ -n "$OUT" ]]; then
  mcporter call "${SERVER}.xiaodu_take_photo" "cuid=$CUID" "client_id=$CLIENT_ID" >"$OUT"
  echo "$OUT"
  exit 0
fi

mcporter call "${SERVER}.xiaodu_take_photo" "cuid=$CUID" "client_id=$CLIENT_ID"
