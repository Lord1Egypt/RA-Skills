#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CLI_SCRIPT="$SCRIPT_DIR/replicate_cli.js"
DEFAULT_PROMPT='生成一个探店打卡照片，要求：提取图1中的美女人物角色，她的姿势可以随意自由变化，站姿或者坐姿都可以，放入场景参考图2中，图2里的场景保持不变，不要漏出手指，远景镜头，去除无关水印，iphone 手机拍摄质感。'

usage() {
  cat <<'EOF'
Usage:
  scripts/run_tandian.sh <scene-image> [output-file] [--template-preset lucy] [--template-url https://...] [--aspect 2:3] [--prompt "..."]

Examples:
  scripts/run_tandian.sh test/input/1.png
  scripts/run_tandian.sh test/input/1.png test/output/1.webp --template-preset lucy
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "${REPLICATE_API_TOKEN:-}" ]]; then
  echo "Missing REPLICATE_API_TOKEN in environment" >&2
  exit 2
fi

SCENE_IMAGE="$1"
shift

OUTPUT_FILE=""
if [[ $# -gt 0 && "$1" != --* ]]; then
  OUTPUT_FILE="$1"
  shift
fi

if [[ -z "$OUTPUT_FILE" ]]; then
  scene_basename="$(basename "$SCENE_IMAGE")"
  scene_name="${scene_basename%.*}"
  OUTPUT_FILE="$SKILL_DIR/output/${scene_name}_tandian_$(date +%Y%m%d_%H%M%S).webp"
fi

ARGS=(--image "$SCENE_IMAGE" --out "$OUTPUT_FILE" --prompt "$DEFAULT_PROMPT")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template-preset)
      [[ $# -ge 2 ]] || { echo "Missing value for --template-preset" >&2; exit 1; }
      ARGS+=(--templatePreset "$2")
      shift 2
      ;;
    --template)
      [[ $# -ge 2 ]] || { echo "Missing value for --template" >&2; exit 1; }
      ARGS+=(--template "$2")
      shift 2
      ;;
    --aspect)
      [[ $# -ge 2 ]] || { echo "Missing value for --aspect" >&2; exit 1; }
      ARGS+=(--aspect "$2")
      shift 2
      ;;
    --prompt)
      [[ $# -ge 2 ]] || { echo "Missing value for --prompt" >&2; exit 1; }
      ARGS+=(--prompt "$2")
      shift 2
      ;;
    --template-url)
      [[ $# -ge 2 ]] || { echo "Missing value for --template-url" >&2; exit 1; }
      ARGS+=(--templateUrl "$2")
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

echo "Scene image: $SCENE_IMAGE"
echo "Output file: $OUTPUT_FILE"

node "$CLI_SCRIPT" "${ARGS[@]}"
