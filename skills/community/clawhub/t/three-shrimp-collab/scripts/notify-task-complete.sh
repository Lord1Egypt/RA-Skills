#!/bin/bash

# 📢 任务完成通知脚本
# 发送飞书消息通知老板任务完成

set -e

# 参数
TASK_NAME="$1"
ASSIGNEE="$2"
COMPLETION_TIME="$3"
DETAILS="$4"

# 飞书配置（从环境变量或配置文件读取）
FEISHU_WEBHOOK="${FEISHU_WEBHOOK:-}"
FEISHU_USER_ID="${FEISHU_USER_ID:-ou_967d17eccf0faa8814004cc4f0458140}"

# 生成通知消息
generate_message() {
    local task="$1"
    local assignee="$2"
    local time="$3"
    local details="$4"
    
    cat << EOF
✅ 任务完成通知

📋 任务：$task
🦞 执行者：$assignee
⏰ 完成时间：$time

📝 详情：
$details

---
_三只虾协同系统自动通知_
EOF
}

# 发送飞书消息（使用 OpenClaw message 工具）
send_feishu_message() {
    local message="$1"
    
    # 使用 OpenClaw 的 message 工具发送
    # 注意：这需要在 OpenClaw 会话中执行
    echo "$message"
}

# 主函数
main() {
    if [ -z "$TASK_NAME" ]; then
        echo "用法：$0 <任务名称> <执行者> <完成时间> [详情]"
        exit 1
    fi
    
    MESSAGE=$(generate_message "$TASK_NAME" "$ASSIGNEE" "$COMPLETION_TIME" "$DETAILS")
    
    # 输出消息（可以被调用者捕获）
    echo "$MESSAGE"
    
    # 如果有飞书 webhook，直接发送
    if [ -n "$FEISHU_WEBHOOK" ]; then
        curl -s -X POST "$FEISHU_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"$MESSAGE\"}}"
        echo ""
        echo "✅ 已发送飞书消息"
    else
        echo ""
        echo "ℹ️  飞书 webhook 未配置，消息已输出到标准输出"
        echo "💡 配置方法：设置环境变量 FEISHU_WEBHOOK"
    fi
}

main "$@"
