#!/bin/bash

# File Manager Skill - 移动文件到正确位置
# 用法: bash scripts/move.sh <源文件> <类型> <描述> <日期>
# 示例: bash scripts/move.sh /path/to/file.pdf pdf invoice 20250325

SOURCE="$1"
TYPE="$2"
DESC="$3"
DATE="$4"

if [ -z "$SOURCE" ] || [ -z "$TYPE" ] || [ -z "$DESC" ] || [ -z "$DATE" ]; then
  echo "用法: bash scripts/move.sh <源文件> <类型> <描述> <日期>"
  echo "类型: images, videos, pdfs, excels, others"
  echo "示例: bash scripts/move.sh /path/to/file.pdf pdf invoice 20250325"
  exit 1
fi

# 确定目标目录
case "$TYPE" in
  images) TARGET_DIR="/workspace/user_input_files/images" ;;
  videos) TARGET_DIR="/workspace/user_input_files/videos" ;;
  pdfs)   TARGET_DIR="/workspace/user_input_files/pdfs" ;;
  excels) TARGET_DIR="/workspace/user_input_files/excels" ;;
  others) TARGET_DIR="/workspace/user_input_files/others" ;;
  *)
    echo "❌ 未知类型: $TYPE"
    exit 1
    ;;
esac

# 获取文件扩展名
EXT="${SOURCE##*.}"
FILENAME="input-${DESC}-${DATE}.${EXT}"

# 移动文件
cp "$SOURCE" "$TARGET_DIR/$FILENAME"
echo "✅ 已复制: $SOURCE -> $TARGET_DIR/$FILENAME"

# 运行验证
bash "$(dirname "$0")/verify.sh"
