#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

DIR_INPUT="${1:-$HOME/Pictures/WallpaperAuto}"
DIR_PATH="$(expand_path "$DIR_INPUT")"
FILE="$(pick_random_image "$DIR_PATH")"

set_wallpaper_file "$FILE"

echo "状态: 成功"
echo "目录: $DIR_PATH"
echo "已设置壁纸: $FILE"
