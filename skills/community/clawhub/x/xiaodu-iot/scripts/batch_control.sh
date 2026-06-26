#!/bin/bash

# 小度设备批量控制脚本
# 批量控制多个IoT设备

set -e

# 显示使用说明
show_help() {
    echo "小度设备批量控制脚本"
    echo "用法: $0 [选项] <操作> <设备列表>"
    echo ""
    echo "操作:"
    echo "  turnOn         打开设备"
    echo "  turnOff        关闭设备"
    echo "  up             向上/打开（窗帘）"
    echo "  down           向下/关闭（窗帘）"
    echo "  toggle         切换开关状态"
    echo ""
    echo "选项:"
    echo "  -r, --room <房间名>     指定房间（默认: 客厅）"
    echo "  -f, --file <文件>       从文件读取设备列表"
    echo "  -d, --delay <秒>        设备间操作延迟（默认: 1秒）"
    echo "  -h, --help              显示此帮助信息"
    echo ""
    echo "设备列表格式:"
    echo "  可以直接在命令行指定设备，如: \"书桌灯 走廊灯 面板灯\""
    echo "  或从文件读取，每行一个设备"
    echo ""
    echo "示例:"
    echo "  $0 turnOn \"书桌灯 走廊灯\""
    echo "  $0 turnOff -r 主卧 \"布帘 纱帘\""
    echo "  $0 up -f curtains.txt"
    echo "  $0 turnOn -d 2 \"书桌灯 洗衣机灯 镜前灯\""
}

# 默认参数
ROOM="客厅"
DELAY=1
ACTION=""
DEVICES=()
DEVICE_FILE=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--room)
            ROOM="$2"
            shift 2
            ;;
        -f|--file)
            DEVICE_FILE="$2"
            shift 2
            ;;
        -d|--delay)
            DELAY="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        turnOn|turnOff|up|down|toggle)
            ACTION="$1"
            shift
            ;;
        -*)
            echo "错误: 未知选项 $1"
            show_help
            exit 1
            ;;
        *)
            # 将剩余参数作为设备列表
            while [[ $# -gt 0 ]]; do
                DEVICES+=("$1")
                shift
            done
            ;;
    esac
done

# 检查操作类型
if [ -z "$ACTION" ]; then
    echo "错误: 必须指定操作类型"
    show_help
    exit 1
fi

# 检查设备列表
if [ -n "$DEVICE_FILE" ]; then
    # 从文件读取设备列表
    if [ ! -f "$DEVICE_FILE" ]; then
        echo "错误: 设备文件不存在: $DEVICE_FILE"
        exit 1
    fi
    
    echo "从文件读取设备列表: $DEVICE_FILE"
    mapfile -t DEVICES < "$DEVICE_FILE"
elif [ ${#DEVICES[@]} -eq 0 ]; then
    echo "错误: 必须指定设备列表"
    show_help
    exit 1
fi

# 显示操作信息
echo "批量控制操作"
echo "============="
echo "操作类型: $ACTION"
echo "房间: $ROOM"
echo "设备数量: ${#DEVICES[@]}"
echo "设备列表: ${DEVICES[*]}"
echo "操作延迟: ${DELAY}秒"
echo ""

# 确认操作
read -p "确认执行批量控制? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "操作已取消"
    exit 0
fi

# 执行批量控制
SUCCESS_COUNT=0
FAIL_COUNT=0

for i in "${!DEVICES[@]}"; do
    DEVICE="${DEVICES[$i]}"
    
    echo ""
    echo "[$((i+1))/${#DEVICES[@]}] 控制设备: $DEVICE"
    
    # 执行控制命令
    if mcporter call xiaodu-iot.IOT_CONTROL_DEVICES \
        action="$ACTION" \
        applianceName="$DEVICE" \
        roomName="$ROOM" 2>/dev/null; then
        echo "  ✅ 成功: $DEVICE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "  ❌ 失败: $DEVICE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    # 添加延迟（最后一个设备不延迟）
    if [ $i -lt $((${#DEVICES[@]} - 1)) ]; then
        sleep "$DELAY"
    fi
done

# 显示结果
echo ""
echo "批量控制完成"
echo "============="
echo "成功: $SUCCESS_COUNT 个设备"
echo "失败: $FAIL_COUNT 个设备"
echo "总计: ${#DEVICES[@]} 个设备"

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✅ 所有设备控制成功！"
else
    echo "⚠️  部分设备控制失败，请检查设备名称和状态"
    exit 1
fi