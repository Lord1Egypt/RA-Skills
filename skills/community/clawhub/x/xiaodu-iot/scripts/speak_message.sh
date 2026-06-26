#!/bin/bash

# 小度语音播报脚本
# 向指定的小度设备发送语音播报

set -e

# 默认设备信息（请替换为你的设备信息）
DEFAULT_CUID="YOUR_DEVICE_CUID"
DEFAULT_CLIENT_ID="YOUR_CLIENT_ID"

# 显示使用说明
show_help() {
    echo "小度语音播报脚本"
    echo "用法: $0 [选项] <播报文本>"
    echo ""
    echo "选项:"
    echo "  -c, --cuid <cuid>        设备CUID (默认: $DEFAULT_CUID)"
    echo "  -i, --client-id <id>     设备Client ID (默认: $DEFAULT_CLIENT_ID)"
    echo "  -d, --device <name>      使用预定义的设备名称"
    echo "  -l, --list-devices       列出预定义的设备"
    echo "  -h, --help               显示此帮助信息"
    echo ""
    echo "预定义设备:"
    echo "  living-room       客厅设备"
    echo "  master-bedroom    主卧小度音箱"
    echo "  kitchen           厨房小度音箱"
    echo "  children-room     儿童房中控屏"
    echo ""
    echo "示例:"
    echo "  $0 \"你好，我是AI助手\""
    echo "  $0 -d living-room \"现在是下午3点\""
    echo "  $0 -c YOUR_DEVICE_CUID -i YOUR_CLIENT_ID \"测试播报\""
}

# 预定义设备列表
declare -A DEVICES=(
    ["living-room"]="YOUR_DEVICE_CUID YOUR_CLIENT_ID"
    ["master-bedroom"]=""  # 需要填写实际CUID和Client ID
    ["kitchen"]=""         # 需要填写实际CUID和Client ID
    ["children-room"]=""   # 需要填写实际CUID和Client ID
)

# 列出预定义设备
list_devices() {
    echo "预定义设备列表:"
    echo "----------------"
    for device in "${!DEVICES[@]}"; do
        if [ -z "${DEVICES[$device]}" ]; then
            echo "  $device: (未配置)"
        else
            echo "  $device: ${DEVICES[$device]}"
        fi
    done
    exit 0
}

# 解析参数
TEXT=""
CUID="$DEFAULT_CUID"
CLIENT_ID="$DEFAULT_CLIENT_ID"
DEVICE_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--cuid)
            CUID="$2"
            shift 2
            ;;
        -i|--client-id)
            CLIENT_ID="$2"
            shift 2
            ;;
        -d|--device)
            DEVICE_NAME="$2"
            shift 2
            ;;
        -l|--list-devices)
            list_devices
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "错误: 未知选项 $1"
            show_help
            exit 1
            ;;
        *)
            TEXT="$1"
            shift
            ;;
    esac
done

# 检查是否指定了预定义设备
if [ -n "$DEVICE_NAME" ]; then
    if [ -z "${DEVICES[$DEVICE_NAME]}" ]; then
        echo "错误: 未知设备 '$DEVICE_NAME'"
        echo "可用设备: ${!DEVICES[@]}"
        exit 1
    fi
    
    if [ -z "${DEVICES[$DEVICE_NAME]}" ]; then
        echo "错误: 设备 '$DEVICE_NAME' 未配置CUID和Client ID"
        echo "请在脚本中配置设备信息"
        exit 1
    fi
    
    # 解析设备信息
    IFS=' ' read -r CUID CLIENT_ID <<< "${DEVICES[$DEVICE_NAME]}"
fi

# 检查播报文本
if [ -z "$TEXT" ]; then
    echo "错误: 必须提供播报文本"
    show_help
    exit 1
fi

# 检查文本长度
if [ ${#TEXT} -gt 500 ]; then
    echo "警告: 播报文本过长 (${#TEXT}字符)，建议缩短到500字符以内"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "正在发送语音播报..."
echo "设备CUID: $CUID"
echo "Client ID: $CLIENT_ID"
echo "播报内容: $TEXT"
echo ""

# 发送语音播报
if mcporter call xiaodu.xiaodu_speak \
    text="$TEXT" \
    cuid="$CUID" \
    client_id="$CLIENT_ID"; then
    echo "✅ 语音播报发送成功！"
else
    echo "❌ 语音播报发送失败"
    exit 1
fi