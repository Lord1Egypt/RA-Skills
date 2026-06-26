#!/bin/bash
# 发送企业微信 Markdown 消息（群机器人 Webhook）
# 用法: send_markdown.sh [--url <url>] [--chatid <id>] [--to <name>] <content>
# 示例: send_markdown.sh "## 告警\n服务异常"
#       send_markdown.sh "$(cat report.md)"
#       send_markdown.sh --url "https://..." "## 标题"
#       send_markdown.sh --chatid "CHATID_xxx" "## 标题"
#       send_markdown.sh --to "研发群" "## 标题"
#
# Markdown 支持: # 标题、**加粗**、*斜体*、`代码`、[链接](url)、> 引用
# 内容最长 4096 字节（UTF-8）
# 注意: 不支持表格，需要表格请用 send_markdown_v2.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

# 解析参数
ARGS=$(parse_wecom_args "$@")
eval "set -- $ARGS"

if [ $# -eq 0 ]; then
    echo "错误: 缺少消息内容"
    echo "使用方法: $0 [--url <url>] [--chatid <id>] [--to <name>] <content>"
    echo "示例: $0 \"## 标题\n正文内容\""
    echo "      $0 --to \"研发群\" \"## 标题\""
    exit 1
fi

check_wecom_url

CONTENT="$1"

# 检查内容长度
BYTE_LEN=$(echo -n "$CONTENT" | wc -c | tr -d ' ')
if [ "$BYTE_LEN" -gt 4096 ]; then
    echo "错误: 内容超出 4096 字节限制（当前 ${BYTE_LEN} 字节）" >&2
    exit 1
fi

BODY=$(jq -n \
    --arg content "$CONTENT" \
    '{
        msgtype: "markdown",
        markdown: { content: $content }
    }')

if wecom_send "$BODY"; then
    echo "✅ 消息发送成功"
else
    exit 1
fi
