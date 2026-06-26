#!/bin/bash
# rustfs-upload - 使用 rc 上传文件到 RustFS
# 用法: upload.sh <文件路径> [目标前缀]
# 示例: upload.sh ~/Desktop/photo.png
#       upload.sh ~/photo.png "images/2026/"

set -euo pipefail

FILE_PATH="$1"
PREFIX="${2:-}"

# 环境变量检查与默认值
ENDPOINT="${RUSTFS_ENDPOINT:-http://127.0.0.1:9000}"
ACCESS_KEY="${RUSTFS_ACCESS_KEY:-}"
SECRET_KEY="${RUSTFS_SECRET_KEY:-}"
BUCKET="${RUSTFS_BUCKET:-}"
PUBLIC_DOMAIN="${RUSTFS_PUBLIC_DOMAIN:-http://127.0.0.1:9001}"

# 验证必要参数
if [ -z "$FILE_PATH" ]; then
    echo "用法: upload.sh <文件路径> [目标前缀]"
    exit 1
fi

# 展开波浪号
FILE_PATH="${FILE_PATH/#\~/$HOME}"

if [ ! -f "$FILE_PATH" ]; then
    echo "错误: 文件不存在: $FILE_PATH"
    exit 1
fi

# 检查 rc 命令是否可用
if ! command -v rc &> /dev/null; then
    echo "错误: rc 命令未找到，请先安装 rustfs-cli (cargo install rustfs-cli)"
    exit 1
fi

# 配置 rc 别名（如果环境变量提供了密钥，优先使用）
ALIAS_NAME="rustfs-temp"
if [ -n "$ACCESS_KEY" ] && [ -n "$SECRET_KEY" ]; then
    rc alias set "$ALIAS_NAME" "$ENDPOINT" "$ACCESS_KEY" "$SECRET_KEY" --quiet 2>/dev/null || true
else
    # 尝试使用已存在的别名，若无则报错
    if ! rc alias list | grep -q "$ALIAS_NAME"; then
        echo "错误: 未设置 RUSTFS_ACCESS_KEY / RUSTFS_SECRET_KEY，且别名 '$ALIAS_NAME' 不存在。"
        echo "请先配置环境变量或手动设置 rc 别名。"
        exit 1
    fi
fi

# 准备目标路径
FILENAME=$(basename "$FILE_PATH")
OBJECT_KEY="${PREFIX}${FILENAME}"
REMOTE_PATH="${ALIAS_NAME}/${BUCKET}/${OBJECT_KEY}"

# 检查桶是否存在，不存在则创建
if ! rc ls "${ALIAS_NAME}/${BUCKET}" &>/dev/null; then
    echo "桶 '${BUCKET}' 不存在，正在创建..."
    rc mb "${ALIAS_NAME}/${BUCKET}" --quiet || {
        echo "错误: 无法创建桶 '${BUCKET}'"
        exit 1
    }
fi

# 上传文件
echo "上传中: $FILENAME -> $REMOTE_PATH"
rc cp --quiet "$FILE_PATH" "$REMOTE_PATH"

if [ $? -ne 0 ]; then
    echo "错误: 上传失败"
    exit 1
fi

# 获取文件大小（可选）
SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null || echo "0")

# 拼接公开 URL
PUBLIC_URL="${PUBLIC_DOMAIN}/${BUCKET}/${OBJECT_KEY}"

# 输出 JSON 结果
jq -n \
    --arg url "$PUBLIC_URL" \
    --arg bucket "$BUCKET" \
    --arg object "$OBJECT_KEY" \
    --arg size "$SIZE" \
    --arg endpoint "$ENDPOINT" \
    '{url: $url, bucket: $bucket, object: $object, size: $size, endpoint: $endpoint}'

echo "上传成功！"