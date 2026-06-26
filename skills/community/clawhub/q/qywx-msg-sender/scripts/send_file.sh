#!/bin/bash
# 发送企业微信文件消息（群机器人 Webhook）
# 先上传文件获取 media_id，再发送消息
# 用法: send_file.sh [--url <url>] [--chatid <id>] [--to <name>] <file_path>
# 示例: send_file.sh /path/to/report.pdf
#       send_file.sh data.xlsx
#       send_file.sh --url "https://..." /path/to/report.pdf
#       send_file.sh --chatid "CHATID_xxx" /path/to/report.pdf
#       send_file.sh --to "研发群" /path/to/report.pdf
#
# 文件大小限制: 20MB

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

# 解析参数
ARGS=$(parse_wecom_args "$@")
eval "set -- $ARGS"

if [ $# -eq 0 ]; then
    echo "错误: 缺少文件路径"
    echo "使用方法: $0 [--url <url>] [--chatid <id>] [--to <name>] <file_path>"
    echo "示例: $0 /path/to/report.pdf"
    echo "      $0 --to \"研发群\" /path/to/report.pdf"
    exit 1
fi

check_wecom_url

FILE_PATH="$1"

if [ ! -f "$FILE_PATH" ]; then
    echo "错误: 文件不存在: ${FILE_PATH}" >&2
    exit 1
fi

# 检查文件大小（20MB 限制）
FILE_SIZE=$(wc -c < "$FILE_PATH" | tr -d ' ')
if [ "$FILE_SIZE" -gt 20971520 ]; then
    echo "错误: 文件超出 20MB 限制（当前 $((FILE_SIZE / 1024 / 1024))MB）" >&2
    exit 1
fi

FILENAME=$(basename "$FILE_PATH")
echo "正在上传文件: ${FILENAME}"

# 从 URL 提取 key
WEBHOOK_KEY=$(echo "$WECOM_CURRENT_URL" | sed 's/.*key=//')

# 上传文件
UPLOAD_RESP=$(curl -s -X POST \
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=${WEBHOOK_KEY}&type=file" \
    -F "media=@${FILE_PATH}")

ERRCODE=$(echo "$UPLOAD_RESP" | jq -r '.errcode // -1')
if [ "$ERRCODE" != "0" ]; then
    ERRMSG=$(echo "$UPLOAD_RESP" | jq -r '.errmsg // "未知错误"')
    echo "错误: 文件上传失败 (errcode=${ERRCODE}): ${ERRMSG}" >&2
    exit 1
fi

MEDIA_ID=$(echo "$UPLOAD_RESP" | jq -r '.media_id')
echo "上传成功，正在发送..."

BODY=$(jq -n \
    --arg media_id "$MEDIA_ID" \
    '{
        msgtype: "file",
        file: { media_id: $media_id }
    }')

if wecom_send "$BODY"; then
    echo "✅ 文件发送成功: ${FILENAME}"
else
    exit 1
fi
