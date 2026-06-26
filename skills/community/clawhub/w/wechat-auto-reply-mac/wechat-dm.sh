#!/bin/bash

# WeChat Auto Reply Skill - CLI Wrapper
# 用法: 
#   ./wechat-dm.sh "联系人名称"              # OCR 半自动回复（置信度>85%自动发送）
#   ./wechat-dm.sh "联系人名称" "消息内容"    # 直接发送消息

CONTACT="$1"
MESSAGE="$2"

if [ -z "$CONTACT" ]; then
    echo "用法:"
    echo "  ./wechat-dm.sh \"联系人名称\"              # OCR 半自动回复（置信度>85%自动发送）"
    echo "  ./wechat-dm.sh \"联系人名称\" \"消息内容\"    # 直接发送消息"
    echo ""
    echo "示例:"
    echo "  ./wechat-dm.sh \"小王\"                    # 半自动模式"
    echo "  ./wechat-dm.sh \"小李\" \"什么时候下班\"    # 主动发送"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLESCRIPT="$SCRIPT_DIR/wechat-dm.applescript"

if [ ! -f "$APPLESCRIPT" ]; then
    echo "错误: 找不到 applescript 文件: $APPLESCRIPT"
    exit 1
fi

# 运行 AppleScript
if [ -n "$MESSAGE" ]; then
    # 带消息内容，直接发送
    osascript "$APPLESCRIPT" "$CONTACT" "$MESSAGE"
else
    # 不带消息内容，OCR 自动回复
    osascript "$APPLESCRIPT" "$CONTACT"
fi

echo "执行完成"
