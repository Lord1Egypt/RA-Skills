#!/bin/bash
# 小红书图片下载脚本
# 用法: ./download_images.sh <日记标题> <图片URL列表>

TITLE="$1"
ACCOUNT="学未教育"
SAVE_DIR="$HOME/Downloads/铁头/$ACCOUNT/$TITLE"
UPLOAD_DIR="/tmp/openclaw/uploads"

# 创建保存目录
mkdir -p "$SAVE_DIR"

# 清空上传目录
rm -rf "$UPLOAD_DIR/*"
mkdir -p "$UPLOAD_DIR"

# 下载图片
for url in "${@:2}"; do
    filename=$(basename "$url" | sed 's/webp$/jpg/')
    
    # 带 Referer 下载
    curl -H "Referer: https://www.xiaohongshu.com/" \
         -o "$SAVE_DIR/$filename" "$url"
    
    # 复制到上传目录
    cp "$SAVE_DIR/$filename" "$UPLOAD_DIR/"
    
    echo "下载: $filename"
done

echo "保存位置: $SAVE_DIR"
echo "上传位置: $UPLOAD_DIR"