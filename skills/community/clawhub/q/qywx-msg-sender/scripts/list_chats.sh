#!/bin/bash
# 列出所有已注册的会话
# 用法: list_chats.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wecom_common.sh"

list_chats
