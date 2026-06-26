#!/bin/bash
# 发送企业微信 Markdown V2 消息（群机器人 Webhook）
# 支持比 markdown 更丰富的语法，包括表格和多行代码块
# 用法: send_markdown_v2.sh [--url <url>] [--chatid <id>] [--to <name>] <content>
# 示例: send_markdown_v2.sh "## 标题\n| 列1 | 列2 |\n|-----|-----|\n| a | b |"
#       send_markdown_v2.sh "$(cat report.md)"
#       send_markdown_v2.sh --url "https://..." "## 标题"
#       send_markdown_v2.sh --chatid "CHATID_xxx" "## 标题"
#       send_markdown_v2.sh --to "研发群" "## 标题"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

# 解析参数
ARGS=$(parse_wecom_args "$@")
eval "set -- $ARGS"

if [ $# -eq 0 ]; then
    echo "错误: 缺少消息内容"
    echo "使用方法: $0 [--url <url>] [--chatid <id>] [--to <name>] <content>"
    echo "示例: $0 \"## 标题\n| 列1 | 列2 |\n|-----|-----|\n| a | b |\""
    echo "      $0 --to \"研发群\" \"## 标题\""
    exit 1
fi

check_wecom_url

CONTENT="$1"

BODY=$(jq -n \
    --arg content "$CONTENT" \
    '{
        msgtype: "markdown_v2",
        markdown_v2: { content: $content }
    }')

if wecom_send "$BODY"; then
    echo "✅ 消息发送成功"
else
    exit 1
fi
