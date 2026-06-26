#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  control_iot.sh --action 动作 --device 设备名 [--room 房间名] [--attribute 属性] [--value 值] [--server 服务名]

示例:
  control_iot.sh --action turnOn --device "射灯"
  control_iot.sh --action set --device "射灯" --attribute brightness --value 30 --server xiaodu-iot
EOF
}

SERVER="xiaodu-iot"
ACTION=""
DEVICE=""
ROOM=""
ATTRIBUTE=""
VALUE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="${2:-}"
      shift 2
      ;;
    --action)
      ACTION="${2:-}"
      shift 2
      ;;
    --device)
      DEVICE="${2:-}"
      shift 2
      ;;
    --room)
      ROOM="${2:-}"
      shift 2
      ;;
    --attribute)
      ATTRIBUTE="${2:-}"
      shift 2
      ;;
    --value)
      VALUE="${2:-}"
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

if [[ -z "$ACTION" ]]; then
  echo "必须提供 --action" >&2
  usage >&2
  exit 1
fi

if [[ -z "$DEVICE" ]]; then
  echo "必须提供 --device，IOT_CONTROL_DEVICES 的 applianceName 是必填字段" >&2
  usage >&2
  exit 1
fi

if [[ "$ACTION" == "set" ]]; then
  if [[ -z "$ATTRIBUTE" || -z "$VALUE" ]]; then
    echo "当 --action=set 时，必须同时提供 --attribute 和 --value" >&2
    usage >&2
    exit 1
  fi
fi

if [[ -n "$VALUE" && -z "$ATTRIBUTE" ]]; then
  echo "提供了 --value 时，必须同时提供 --attribute" >&2
  usage >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

ARGS=("action=$ACTION")
ARGS+=("applianceName=$DEVICE")
if [[ -n "$ROOM" ]]; then
  ARGS+=("roomName=$ROOM")
fi
if [[ -n "$ATTRIBUTE" ]]; then
  ARGS+=("attribute=$ATTRIBUTE")
fi
if [[ -n "$VALUE" ]]; then
  ARGS+=("value=$VALUE")
fi

mcporter call "${SERVER}.IOT_CONTROL_DEVICES" "${ARGS[@]}"
