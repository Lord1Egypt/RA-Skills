#!/usr/bin/env bash
# 视觉理解 - GLM-4.6V 图像分析
# 用法: vision.sh <图片路径或URL> [提示词]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IMAGE_PATH="${1:?用法: vision.sh <图片路径或URL> [提示词]}"
PROMPT="${2:-请描述这张图片的内容}"

ZHIPU_API_KEY="${ZHIPU_API_KEY:-}" python3 "$SCRIPT_DIR/zhipu_tool.py" vision "$IMAGE_PATH" --prompt "$PROMPT"
