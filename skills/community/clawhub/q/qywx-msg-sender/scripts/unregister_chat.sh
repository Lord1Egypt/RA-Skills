#!/bin/bash
# 删除已注册的会话
# 用法: unregister_chat.sh <name>
# 示例: unregister_chat.sh "研发群"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

if [ $# -eq 0 ]; then
    echo "删除已注册的会话"
    echo ""
    echo "使用方法: $0 <name>"
    echo ""
    echo "示例:"
    echo "  $0 \"研发群\""
    echo ""
    echo "查看已注册的会话: list_chats.sh"
    exit 1
fi

NAME="$1"

unregister_chat "$NAME"
