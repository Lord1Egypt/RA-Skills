#!/usr/bin/env bash
set -euo pipefail

API_URL="https://agent.mathmind.cn/minimalist/api/tywx/zImage"
DEFAULT_SIZE="1024*1536"
DEFAULT_PROFILE="1280"

prompt=""
size=""
ratio=""
count="1"
profile="$DEFAULT_PROFILE"

resolve_size_from_ratio() {
  local input_ratio="$1"
  local input_profile="$2"

  case "$input_profile:$input_ratio" in
    1024:1:1) echo "1024*1024" ;;
    1024:2:3) echo "832*1248" ;;
    1024:3:2) echo "1248*832" ;;
    1024:3:4) echo "864*1152" ;;
    1024:4:3) echo "1152*864" ;;
    1024:7:9) echo "896*1152" ;;
    1024:9:7) echo "1152*896" ;;
    1024:9:16) echo "720*1280" ;;
    1024:9:21) echo "576*1344" ;;
    1024:16:9) echo "1280*720" ;;
    1024:21:9) echo "1344*576" ;;
    1280:1:1) echo "1280*1280" ;;
    1280:2:3) echo "1024*1536" ;;
    1280:3:2) echo "1536*1024" ;;
    1280:3:4) echo "1104*1472" ;;
    1280:4:3) echo "1472*1104" ;;
    1280:7:9) echo "1120*1440" ;;
    1280:9:7) echo "1440*1120" ;;
    1280:9:16) echo "864*1536" ;;
    1280:9:21) echo "720*1680" ;;
    1280:16:9) echo "1536*864" ;;
    1280:21:9) echo "1680*720" ;;
    1536:1:1) echo "1536*1536" ;;
    1536:2:3) echo "1248*1872" ;;
    1536:3:2) echo "1872*1248" ;;
    1536:3:4) echo "1296*1728" ;;
    1536:4:3) echo "1728*1296" ;;
    1536:7:9) echo "1344*1728" ;;
    1536:9:7) echo "1728*1344" ;;
    1536:9:16) echo "1152*2048" ;;
    1536:9:21) echo "864*2016" ;;
    1536:16:9) echo "2048*1152" ;;
    1536:21:9) echo "2016*864" ;;
    *) echo "" ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      prompt="${2:-}"
      shift 2
      ;;
    --size)
      size="${2:-}"
      shift 2
      ;;
    --ratio)
      ratio="${2:-}"
      shift 2
      ;;
    --count)
      count="${2:-}"
      shift 2
      ;;
    --profile)
      profile="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: $0 --prompt <text> [--size <width*height>] [--ratio <ratio>] [--count <number>] [--profile 1024|1280|1536]"
      exit 1
      ;;
  esac
done

if [[ -z "$prompt" ]]; then
  echo "Error: --prompt is required"
  exit 1
fi

if [[ -z "${X_API_KEY:-}" && -f "$HOME/.config/z-image/.env" ]]; then
  set -a
  . "$HOME/.config/z-image/.env"
  set +a
fi

if [[ -z "${X_API_KEY:-}" ]]; then
  echo "Error: missing X_API_KEY. Get x-api-key from kexiangai.com"
  exit 1
fi

case "$profile" in
  1024|1280|1536) ;;
  *)
    echo "Warning: invalid --profile '$profile', fallback to 1280"
    profile="$DEFAULT_PROFILE"
    ;;
esac

if [[ -n "$ratio" && -z "$size" ]]; then
  size="$(resolve_size_from_ratio "$ratio" "$profile")"
  if [[ -z "$size" ]]; then
    echo "Warning: unsupported --ratio '$ratio', fallback to $DEFAULT_SIZE"
    size="$DEFAULT_SIZE"
  fi
fi

if [[ -z "$size" ]]; then
  size="$DEFAULT_SIZE"
fi

if ! [[ "$size" =~ ^[0-9]+\*[0-9]+$ ]]; then
  echo "Error: invalid --size '$size'. Expected format WIDTH*HEIGHT"
  exit 1
fi

width="${size%%\**}"
height="${size##*\*}"
pixels=$((width * height))
min_pixels=$((512 * 512))
max_pixels=$((2048 * 2048))

if (( pixels < min_pixels || pixels > max_pixels )); then
  echo "Error: size '$size' is outside allowed pixel range"
  exit 1
fi

if ! [[ "$count" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: invalid --count '$count'. Expected positive integer"
  exit 1
fi

for ((i = 1; i <= count; i++)); do
  payload=$(cat <<EOF
{
  "prompt": "${prompt//"/\\\"}",
  "size": "$size"
}
EOF
)

  curl --location "$API_URL" \
    --header "x-api-key: $X_API_KEY" \
    --header 'Content-Type: application/json' \
    --data "$payload"
done