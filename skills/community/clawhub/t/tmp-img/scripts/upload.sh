#!/bin/bash
# tmp-img - 临时图床上传脚本
# 用法: upload.sh <图片路径> [过期时间，默认30d]
# 示例: upload.sh ~/Desktop/screenshot.png
#       upload.sh ~/photo.png 7d

IMAGE_PATH="$1"
EXPIRES="${2:-30d}"
API="https://api.imgland.net/v1/images"

if [ -z "$IMAGE_PATH" ]; then
  echo "用法: upload.sh <图片路径> [过期时间]"
  echo "示例: upload.sh ~/Desktop/screenshot.png"
  echo "      upload.sh ~/photo.png 7d"
  echo ""
  echo "过期时间格式: 1d, 7d, 30d 等"
  exit 1
fi

# 展开路径
IMAGE_PATH="${IMAGE_PATH/#\~/$HOME}"

if [ ! -f "$IMAGE_PATH" ]; then
  echo "错误: 文件不存在: $IMAGE_PATH"
  exit 1
fi

FILENAME=$(basename "$IMAGE_PATH")

echo "上传中: $FILENAME (过期: $EXPIRES)..."

# 上传
RESPONSE=$(curl -s -X POST "$API" \
  -H "accept: */*" \
  -F "file=@${IMAGE_PATH}" \
  -F "expiresIn=${EXPIRES}" \
  2>&1)

if [ $? -ne 0 ]; then
  echo "错误: 网络请求失败"
  echo "$RESPONSE"
  exit 1
fi

# 解析响应
URL=$(echo "$RESPONSE" | jq -r '.url // empty' 2>/dev/null)

if [ -z "$URL" ]; then
  echo "错误: 上传失败"
  echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
  exit 1
fi

ID=$(echo "$RESPONSE" | jq -r '.id')
EXPIRES_AT=$(echo "$RESPONSE" | jq -r '.expiresAt')
DELETE_SECRET=$(echo "$RESPONSE" | jq -r '.deleteSecret')
FILE_SIZE=$(echo "$RESPONSE" | jq -r '.fileSize')

# 输出结果（JSON 格式，方便 Claude 解析）
jq -n \
  --arg url "$URL" \
  --arg id "$ID" \
  --arg filename "$FILENAME" \
  --arg file_size "$FILE_SIZE" \
  --arg expires_at "$EXPIRES_AT" \
  --arg delete_url "https://api.imgland.net/v1/images/$ID/file/$DELETE_SECRET" \
  '{url: $url, id: $id, filename: $filename, file_size: $file_size, expires_at: $expires_at, delete_url: $delete_url}'
