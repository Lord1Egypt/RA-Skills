#!/bin/bash
# 发送企业微信图片消息（群机器人 Webhook）
# 图片以 base64 编码直传，无需上传
# 用法: send_image.sh [--url <url>] [--chatid <id>] [--to <name>] <image_path>
# 示例: send_image.sh /path/to/image.png
#       send_image.sh screenshot.jpg
#       send_image.sh --url "https://..." /path/to/image.png
#       send_image.sh --chatid "CHATID_xxx" /path/to/image.png
#       send_image.sh --to "研发群" /path/to/image.png
#
# 支持格式: jpg、png
# 图片大小限制: 2MB

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

# 解析参数
ARGS=$(parse_wecom_args "$@")
eval "set -- $ARGS"

if [ $# -eq 0 ]; then
    echo "错误: 缺少图片路径"
    echo "使用方法: $0 [--url <url>] [--chatid <id>] [--to <name>] <image_path>"
    echo "示例: $0 /path/to/image.png"
    echo "      $0 --to \"研发群\" /path/to/image.png"
    exit 1
fi

check_wecom_url

IMAGE_PATH="$1"

if [ ! -f "$IMAGE_PATH" ]; then
    echo "错误: 文件不存在: ${IMAGE_PATH}" >&2
    exit 1
fi

# 检查文件大小（2MB 限制）
FILE_SIZE=$(wc -c < "$IMAGE_PATH" | tr -d ' ')
if [ "$FILE_SIZE" -gt 2097152 ]; then
    echo "错误: 图片超出 2MB 限制（当前 $((FILE_SIZE / 1024))KB）" >&2
    exit 1
fi

echo "正在发送图片消息: $(basename "$IMAGE_PATH")"

IMG_BASE64=$(base64 -i "$IMAGE_PATH")
IMG_MD5=$(md5 -q "$IMAGE_PATH" 2>/dev/null || md5sum "$IMAGE_PATH" | awk '{print $1}')

BODY=$(jq -n \
    --arg base64 "$IMG_BASE64" \
    --arg md5 "$IMG_MD5" \
    '{
        msgtype: "image",
        image: { base64: $base64, md5: $md5 }
    }')

if wecom_send "$BODY"; then
    echo "✅ 图片发送成功"
else
    exit 1
fi
