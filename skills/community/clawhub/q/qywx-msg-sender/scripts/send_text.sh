#!/bin/bash
# 发送企业微信文本消息（群机器人 Webhook）
# 用法: send_text.sh [--url <url>] [--chatid <id>] [--to <name>] <content> [@mention_user ...]
# 示例: send_text.sh "服务器异常，请及时处理"
#       send_text.sh "部署完成" "zhangsan"           # @指定人
#       send_text.sh "紧急告警" "@all"               # @所有人
#       send_text.sh --url "https://..." "消息内容"  # 指定 webhook URL
#       send_text.sh --chatid "CHATID_xxx" "消息"    # 发送到指定会话
#       send_text.sh --to "研发群" "消息"            # 通过名称发送（需先注册）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

# 解析参数
ARGS=$(parse_wecom_args "$@")
eval "set -- $ARGS"

if [ $# -eq 0 ]; then
    echo "错误: 缺少消息内容"
    echo "使用方法: $0 [--url <url>] [--chatid <id>] [--to <name>] <content> [mention_user]"
    echo "示例: $0 \"服务异常\""
    echo "      $0 --to \"研发群\" \"消息内容\""
    echo "      $0 --chatid \"CHATID_xxx\" \"消息内容\""
    exit 1
fi

check_wecom_url

CONTENT="$1"
MENTION="${2:-}"

# 构建 mentioned_list
if [ "$MENTION" = "@all" ]; then
    MENTIONED_LIST='["@all"]'
elif [ -n "$MENTION" ]; then
    MENTIONED_LIST=$(echo "$MENTION" | tr '|' '\n' | jq -R . | jq -s .)
else
    MENTIONED_LIST='[]'
fi

BODY=$(jq -n \
    --arg content "$CONTENT" \
    --argjson mentioned_list "$MENTIONED_LIST" \
    '{
        msgtype: "text",
        text: {
            content: $content,
            mentioned_list: $mentioned_list
        }
    }')

if wecom_send "$BODY"; then
    echo "✅ 消息发送成功"
else
    exit 1
fi
