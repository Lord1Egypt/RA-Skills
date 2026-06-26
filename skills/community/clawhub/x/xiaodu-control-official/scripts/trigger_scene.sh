#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  trigger_scene.sh --scene-name 场景名 [--server 服务名]

示例:
  trigger_scene.sh --scene-name "回家"
  trigger_scene.sh --scene-name "睡眠模式" --server xiaodu-iot
EOF
}

SERVER="xiaodu-iot"
SCENE_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --server)
      SERVER="${2:-}"
      shift 2
      ;;
    --scene-name)
      SCENE_NAME="${2:-}"
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

if [[ -z "$SCENE_NAME" ]]; then
  echo "必须提供 --scene-name" >&2
  usage >&2
  exit 1
fi

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

mcporter call "${SERVER}.TRIGGER_SCENES" "sceneName=$SCENE_NAME"
