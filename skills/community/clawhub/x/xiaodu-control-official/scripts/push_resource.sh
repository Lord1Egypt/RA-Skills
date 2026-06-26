#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  push_resource.sh --resource-type 类型 [--device-name 设备名 | --cuid ID --client-id ID] [资源参数] [--timeout 秒数] [--server 服务名]

资源类型:
  image            需要 --image-url
  image_with_bgm   需要 --image-url 和 --bgm-url
  video            需要 --video-url
  audio            需要 --audio-url

示例:
  push_resource.sh --resource-type image --image-url "https://example.com/a.jpg" --device-name "小度智能屏2"
  push_resource.sh --resource-type video --video-url "https://example.com/a.mp4" --cuid abc --client-id xyz
EOF
}

SERVER="xiaodu"
RESOURCE_TYPE=""
DEVICE_NAME=""
CUID=""
CLIENT_ID=""
IMAGE_URL=""
BGM_URL=""
VIDEO_URL=""
AUDIO_URL=""
TIMEOUT=""

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
    --resource-type)
      RESOURCE_TYPE="${2:-}"
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
    --image-url)
      IMAGE_URL="${2:-}"
      shift 2
      ;;
    --bgm-url)
      BGM_URL="${2:-}"
      shift 2
      ;;
    --video-url)
      VIDEO_URL="${2:-}"
      shift 2
      ;;
    --audio-url)
      AUDIO_URL="${2:-}"
      shift 2
      ;;
    --timeout)
      TIMEOUT="${2:-}"
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

if [[ -z "$RESOURCE_TYPE" ]]; then
  echo "必须提供 --resource-type" >&2
  usage >&2
  exit 1
fi

if [[ -z "$DEVICE_NAME" && ( -z "$CUID" || -z "$CLIENT_ID" ) ]]; then
  echo "必须提供 --device-name，或者同时提供 --cuid 和 --client-id" >&2
  usage >&2
  exit 1
fi

case "$RESOURCE_TYPE" in
  image)
    [[ -n "$IMAGE_URL" ]] || { echo "image 类型必须提供 --image-url" >&2; exit 1; }
    ;;
  image_with_bgm)
    [[ -n "$IMAGE_URL" ]] || { echo "image_with_bgm 类型必须提供 --image-url" >&2; exit 1; }
    [[ -n "$BGM_URL" ]] || { echo "image_with_bgm 类型必须提供 --bgm-url" >&2; exit 1; }
    ;;
  video)
    [[ -n "$VIDEO_URL" ]] || { echo "video 类型必须提供 --video-url" >&2; exit 1; }
    ;;
  audio)
    [[ -n "$AUDIO_URL" ]] || { echo "audio 类型必须提供 --audio-url" >&2; exit 1; }
    ;;
  *)
    echo "不支持的资源类型: $RESOURCE_TYPE" >&2
    exit 1
    ;;
esac

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

if [[ -n "$DEVICE_NAME" ]]; then
  resolve_device_identifiers
fi

ARGS=("resource_type=$RESOURCE_TYPE" "cuid=$CUID" "client_id=$CLIENT_ID")
if [[ -n "$IMAGE_URL" ]]; then
  ARGS+=("image_url=$IMAGE_URL")
fi
if [[ -n "$BGM_URL" ]]; then
  ARGS+=("bgm_url=$BGM_URL")
fi
if [[ -n "$VIDEO_URL" ]]; then
  ARGS+=("video_url=$VIDEO_URL")
fi
if [[ -n "$AUDIO_URL" ]]; then
  ARGS+=("audio_url=$AUDIO_URL")
fi
if [[ -n "$TIMEOUT" ]]; then
  ARGS+=("timeout=$TIMEOUT")
fi

mcporter call "${SERVER}.push_resource_to_xiaodu" "${ARGS[@]}"
