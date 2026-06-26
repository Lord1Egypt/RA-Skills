#!/bin/bash
# 注册会话：绑定名称、webhook URL、chatid 和会话类型
# 用法: register_chat.sh <name> <webhook_url> [chatid] [chat_type]
# 示例: register_chat.sh "研发群" "https://...?key=xxx"
#       register_chat.sh "张三" "https://...?key=yyy" "wrkSFfCgAAxxxxxx" "single"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

if [ $# -lt 2 ]; then
    echo "注册会话：绑定名称、webhook URL、chatid 和会话类型"
    echo ""
    echo "使用方法: $0 <name> <webhook_url> [chatid] [chat_type]"
    echo ""
    echo "参数说明:"
    echo "  name        - 会话名称（用于 --to 参数）"
    echo "  webhook_url - 群机器人的 Webhook URL"
    echo "  chatid      - 可选，指定会话 ID（不提供则发送到 webhook 默认群）"
    echo "  chat_type   - 可选，会话类型：group（群聊，默认）或 single（私聊）"
    echo ""
    echo "示例:"
    echo "  # 注册群聊（发送到创建机器人的默认群）"
    echo "  $0 \"研发群\" \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx\""
    echo ""
    echo "  # 注册群聊（发送到指定会话）"
    echo "  $0 \"告警群\" \"https://...?key=yyy\" \"wrkSFfCgAAxxxxxx\""
    echo ""
    echo "  # 注册私聊"
    echo "  $0 \"张三\" \"https://...?key=zzz\" \"wokSFfCgAAyyyyyy\" \"single\""
    echo ""
    echo "注册后可通过 --to 参数按名称发送:"
    echo "  send_text.sh --to \"研发群\" \"消息内容\""
    echo "  send_text.sh --to \"张三\" \"私聊消息\""
    echo ""
    echo "注册表位置: $WECOM_REGISTRY_FILE"
    exit 1
fi

NAME="$1"
URL="$2"
CHATID="${3:-}"
CHAT_TYPE="${4:-group}"

register_chat "$NAME" "$URL" "$CHATID" "$CHAT_TYPE"
