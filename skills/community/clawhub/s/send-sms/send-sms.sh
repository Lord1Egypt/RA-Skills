#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

usage() {
    echo "用法: send-sms.sh --phone <手机号> --template <模板ID> [--vars <变量JSON>]"
    echo ""
    echo "参数:"
    echo "  --phone    接收手机号（必填）"
    echo "  --template 模板ID（必填）"
    echo "  --vars     变量JSON（可选），格式: {\"param1\":\"value1\"}"
    echo ""
    echo "示例:"
    echo "  # 有变量模板"
    echo "  send-sms.sh --phone 13800138000 --template 1021143438 --vars '{\"param1\":\"验证码\",\"param2\":\"123456\"}'"
    echo ""
    echo "  # 常量模板"
    echo "  send-sms.sh --phone 13800138000 --template 1021701163"
    exit 1
}

# 默认值
VARS=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --phone)
            PHONE="$2"
            shift 2
            ;;
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        --vars)
            VARS="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            usage
            ;;
    esac
done

# 验证必填参数
if [[ -z "$PHONE" ]] || [[ -z "$TEMPLATE" ]]; then
    echo "错误: 缺少必填参数"
    usage
fi

# 读取配置（优先环境变量，其次 .env 文件）
load_config() {
    # 优先使用环境变量
    if [[ -z "$CHANGLAN_ACCOUNT" ]] || [[ -z "$CHANGLAN_PASSWORD" ]]; then
        # 尝试读取 .env 文件
        if [[ -f "$ENV_FILE" ]]; then
            source "$ENV_FILE"
        fi
    fi

    # 验证必填配置
    if [[ -z "$CHANGLAN_ACCOUNT" ]]; then
        echo "错误: 未配置 CHANGLAN_ACCOUNT"
        echo ""
        echo "请通过以下方式配置："
        echo "  方式一（推荐）：export CHANGLAN_ACCOUNT=你的账号"
        echo "  方式二：在同目录下创建 .env 文件"
        exit 1
    fi

    if [[ -z "$CHANGLAN_PASSWORD" ]]; then
        echo "错误: 未配置 CHANGLAN_PASSWORD"
        echo ""
        echo "请通过以下方式配置："
        echo "  方式一（推荐）：export CHANGLAN_PASSWORD=你的密码"
        echo "  方式二：在同目录下创建 .env 文件"
        exit 1
    fi

    # 设置默认 API URL
    : "${CHANGLAN_API_URL:=https://smssh.253.com/msg/sms/v2/tpl/send}"
}

# 发送短信
send_sms() {
    local phone="$1"
    local template="$2"
    local vars="$3"

    # 生成时间戳和随机字符串
    local timestamp=$(date +%s)
    local nonce=$(openssl rand -hex 16 2>/dev/null)

    # 构建请求体
    local request_body
    if [[ -z "$vars" || "$vars" == "{}" ]]; then
        # 无变量模板
        request_body=$(cat <<EOF
{
    "account": "${CHANGLAN_ACCOUNT}",
    "password": "${CHANGLAN_PASSWORD}",
    "timestamp": "${timestamp}",
    "nonce": "${nonce}",
    "phoneNumbers": "${phone}",
    "templateId": "${template}",
    "report": "true"
}
EOF
)
    else
        # 有变量模板
        local vars_array="[${vars}]"
        request_body=$(cat <<EOF
{
    "account": "${CHANGLAN_ACCOUNT}",
    "password": "${CHANGLAN_PASSWORD}",
    "timestamp": "${timestamp}",
    "nonce": "${nonce}",
    "phoneNumbers": "${phone}",
    "templateId": "${template}",
    "templateParamJson": "${vars_array}",
    "report": "true"
}
EOF
)
    fi

    # 调用 API
    local response=$(curl -s -m 30 -X POST "${CHANGLAN_API_URL}" \
        -H "Content-Type: application/json" \
        -d "${request_body}")

    # 解析响应
    parse_response "$response"
}

# 解析响应
parse_response() {
    local response="$1"

    # 使用 jq 解析响应
    local code=$(echo "$response" | jq -r '.code // "null"')

    if [[ "$code" == "null" ]]; then
        echo "发送失败!"
        echo "错误信息: API 响应格式错误"
        echo "原始响应: $response"
        exit 1
    fi

    if [[ "$code" == "000000" ]]; then
        local msg_id=$(echo "$response" | jq -r '.msgId // "未知"')
        local success_num=$(echo "$response" | jq -r '.successNum // "0"')
        echo "发送成功!"
        echo "消息ID: $msg_id"
        echo "成功数量: $success_num"
    else
        local error_msg=$(echo "$response" | jq -r '.errorMsg // "未知错误"')
        echo "发送失败!"
        echo "错误码: $code"
        echo "错误信息: $error_msg"
        exit 1
    fi
}

# 主流程
load_config
send_sms "$PHONE" "$TEMPLATE" "$VARS"
