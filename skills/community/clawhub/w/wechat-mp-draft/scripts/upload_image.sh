#!/bin/bash
# 上传图片到微信公众号获取永久素材 media_id
# 使用方法: ./upload_image.sh <access_token> <图片路径>

set -e

ACCESS_TOKEN=$1
IMAGE_PATH=$2

# 参数检查
if [ -z "$ACCESS_TOKEN" ] || [ -z "$IMAGE_PATH" ]; then
    echo "错误：缺少参数"
    echo "用法: $0 <access_token> <图片路径>"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$IMAGE_PATH" ]; then
    echo "错误：图片文件不存在: $IMAGE_PATH"
    exit 1
fi

# 检查文件类型（只接受图片）
FILE_TYPE=$(file -b --mime-type "$IMAGE_PATH")
if [[ ! "$FILE_TYPE" =~ ^image/ ]]; then
    echo "错误：文件不是图片类型: $FILE_TYPE"
    exit 1
fi

echo "正在上传图片: $IMAGE_PATH"

# 调用微信 API 上传永久素材
RESPONSE=$(curl -s -F "media=@$IMAGE_PATH" \
    "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${ACCESS_TOKEN}&type=image")

# 检查返回结果
if echo "$RESPONSE" | grep -q '"media_id"'; then
    echo "✅ 图片上传成功"
    echo "$RESPONSE"
else
    echo "❌ 图片上传失败"
    echo "$RESPONSE"
    exit 1
fi
