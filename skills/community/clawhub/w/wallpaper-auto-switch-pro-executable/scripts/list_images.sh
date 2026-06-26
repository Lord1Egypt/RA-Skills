#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

DIR_INPUT="${1:-$HOME/Pictures/WallpaperAuto}"
DIR_PATH="$(expand_path "$DIR_INPUT")"

ensure_dir_exists "$DIR_PATH"
IMAGES="$(collect_images "$DIR_PATH")"
COUNT=$(printf '%s
' "$IMAGES" | sed '/^$/d' | wc -l | tr -d ' ')

echo "目录: $DIR_PATH"
echo "可用图片数量: $COUNT"

if [[ "$COUNT" -eq 0 ]]; then
  echo "状态: 没有可用图片"
  exit 1
fi

echo "前 10 个文件示例:"
printf '%s
' "$IMAGES" | head -n 10
