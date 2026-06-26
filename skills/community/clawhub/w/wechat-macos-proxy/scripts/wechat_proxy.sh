#!/bin/bash
# WeChat macOS Proxy 主脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用说明
usage() {
    echo "WeChat macOS Proxy - 微信代聊助手"
    echo ""
    echo "用法:"
    echo "  $0 listen                          # 启动消息监听模式"
    echo "  $0 send \"联系人\" \"消息内容\"      # 发送消息给指定联系人"
    echo "  $0 read \"联系人\"                  # 读取指定联系人的最新消息"
    echo "  $0 check                           # 快速检查是否有新消息"
    echo "  $0 stop                            # 停止监听模式"
    echo "  $0 test                            # 测试微信连接"
    echo "  $0 batch-send <csv文件>            # 批量发送消息（CSV格式: 联系人,消息）"
    echo "  $0 export \"联系人\" [数量]         # 导出聊天记录为Markdown"
    echo ""
    echo "示例:"
    echo "  $0 send \"张三\" \"晚上一起吃饭吗？\""
    echo "  $0 read \"李四\""
    echo "  $0 batch-send ./contacts.csv       # CSV格式: 联系人,消息内容"
    echo "  $0 export \"工作群\" 50             # 导出最近50条消息"
}

# 测试微信连接
cmd_test() {
    log "测试微信连接..."
    check_peekaboo
    
    if check_wechat_running; then
        log "✓ 微信正在运行"
        
        # 尝试激活微信
        focus_wechat
        sleep 1
        
        # 截图测试
        local screenshot_path="$TEMP_DIR/test_screenshot.png"
        screenshot "$screenshot_path"
        if [ -f "$screenshot_path" ]; then
            log "✓ 截图成功: $screenshot_path"
            log "请检查截图是否正确显示微信界面"
            return 0
        else
            log "✗ 截图失败"
            return 1
        fi
    else
        log "✗ 微信未运行"
        return 1
    fi
}

# 查找联系人并点击
cmd_find_and_click_chat() {
    local contact_name="$1"
    log "查找联系人: $contact_name"
    
    focus_wechat
    sleep 1
    
    # 打开搜索 (Cmd+F)
    log "打开搜索..."
    peekaboo hotkey --keys "cmd,f" --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.8
    
    # 输入联系人名称
    log "输入搜索关键词: $contact_name"
    peekaboo type "$contact_name" --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 1
    
    # 按回车选中搜索结果
    log "选中搜索结果..."
    peekaboo press return --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.8
    
    # 再次按回车确认打开（或点击）
    log "打开聊天..."
    peekaboo press return --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 1
    
    # 关闭搜索框（如果还在）
    peekaboo press escape --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.5
    
    log "已尝试打开与 $contact_name 的聊天"
}

# 发送消息
cmd_send() {
    local contact_name="$1"
    local message="$2"
    
    if [ -z "$contact_name" ] || [ -z "$message" ]; then
        echo "错误: 需要提供联系人和消息内容"
        usage
        exit 1
    fi
    
    log "准备发送消息给 $contact_name"
    check_peekaboo
    check_wechat_running || exit 1
    
    # 查找并点击联系人
    cmd_find_and_click_chat "$contact_name"
    sleep 1.5
    
    # 点击输入框区域（屏幕底部中央）
    log "聚焦输入框..."
    peekaboo click --coords 960,750 --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.5
    
    # 输入消息
    log "输入消息: $message"
    peekaboo type "$message" --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.5
    
    # 发送（使用回车键）
    log "发送消息..."
    peekaboo press return --app "$WECHAT_APP_NAME" 2>/dev/null
    sleep 0.5
    log "✓ 消息已发送"
}

# 读取最新消息
cmd_read() {
    local contact_name="$1"
    
    if [ -z "$contact_name" ]; then
        echo "错误: 需要提供联系人名称"
        exit 1
    fi
    
    log "读取 $contact_name 的最新消息"
    check_peekaboo
    check_wechat_running || exit 1
    
    # 查找并点击联系人
    cmd_find_and_click_chat "$contact_name"
    sleep 1
    
    # 截图聊天区域
    local chat_screenshot="$TEMP_DIR/chat_${contact_name}_$(date +%s).png"
    screenshot "$chat_screenshot"
    
    log "✓ 已截图聊天界面: $chat_screenshot"
    log "提示: 可以使用 peekaboo see --analyze 来分析消息内容"
    
    # 返回截图路径
    echo "CHAT_SCREENSHOT:$chat_screenshot"
}

# 检查新消息（红点检测）
cmd_check() {
    log "检查新消息..."
    check_peekaboo
    check_wechat_running || exit 1
    
    focus_wechat
    sleep 0.5
    
    # 截图聊天列表面板
    local list_screenshot="$TEMP_DIR/chat_list_$(date +%s).png"
    screenshot "$list_screenshot"
    
    log "已截图聊天列表: $list_screenshot"
    
    # 使用 see 命令分析（可以尝试检测红点或新消息提示）
    local analysis_output="$TEMP_DIR/analysis_$(date +%s).txt"
    peekaboo see --path "$list_screenshot" --analyze "找出有新消息的聊天，列出联系人名称和新消息数量" > "$analysis_output" 2>/dev/null
    
    if [ -f "$analysis_output" ] && [ -s "$analysis_output" ]; then
        log "分析结果:"
        cat "$analysis_output"
    else
        log "未检测到新消息或分析失败"
    fi
}

# 监听模式
cmd_listen() {
    log "启动监听模式 (模式: $MODE)"
    check_peekaboo
    check_wechat_running || exit 1
    
    # 创建 PID 文件
    echo $$ > "$TEMP_DIR/listener.pid"
    log "监听进程 PID: $$"
    
    log "按 Ctrl+C 停止监听"
    echo ""
    
    local last_check_time=0
    
    while [ -f "$TEMP_DIR/listener.pid" ]; do
        current_time=$(date +%s)
        
        # 按间隔检查
        if [ $((current_time - last_check_time)) -ge "$CHECK_INTERVAL" ]; then
            last_check_time=$current_time
            
            # 截图并分析
            focus_wechat
            sleep 0.5
            
            local screenshot_path="$TEMP_DIR/listen_$(date +%s).png"
            screenshot "$screenshot_path"
            
            # 分析是否有新消息（简化实现）
            # 实际实现中这里应该调用更复杂的检测逻辑
            log "[$(date '+%H:%M:%S')] 检查新消息..."
        fi
        
        sleep 1
    done
    
    log "监听已停止"
}

# 停止监听
cmd_stop() {
    if [ -f "$TEMP_DIR/listener.pid" ]; then
        local pid=$(cat "$TEMP_DIR/listener.pid")
        log "停止监听进程: $pid"
        rm -f "$TEMP_DIR/listener.pid"
        kill "$pid" 2>/dev/null
        log "✓ 监听已停止"
    else
        log "没有正在运行的监听进程"
    fi
}

# 批量发送消息
cmd_batch_send() {
    local csv_file="$1"
    
    if [ -z "$csv_file" ] || [ ! -f "$csv_file" ]; then
        echo "错误: 需要提供有效的 CSV 文件路径"
        echo "CSV 格式: 联系人名称,消息内容"
        echo "示例:"
        echo "  张三,晚上一起吃饭吗？"
        echo "  李四,明天会议改到下午"
        exit 1
    fi
    
    log "开始批量发送消息，数据源: $csv_file"
    check_peekaboo
    check_wechat_running || exit 1
    
    local total=0
    local success=0
    local failed=0
    
    # 读取 CSV 文件
    while IFS=',' read -r contact message; do
        # 跳过空行和注释行
        [ -z "$contact" ] && continue
        [[ "$contact" =~ ^# ]] && continue
        
        total=$((total + 1))
        
        # 去除前后空格
        contact=$(echo "$contact" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        message=$(echo "$message" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        
        log "[$total] 发送给 $contact: $message"
        
        # 发送消息
        if cmd_find_and_click_chat "$contact" &>/dev/null; then
            sleep 1.5
            peekaboo click --coords 960,750 --app "$WECHAT_APP_NAME" 2>/dev/null
            sleep 0.5
            peekaboo type "$message" --app "$WECHAT_APP_NAME" 2>/dev/null
            sleep 0.5
            peekaboo press return --app "$WECHAT_APP_NAME" 2>/dev/null
            sleep 1
            success=$((success + 1))
            log "  ✓ 发送成功"
        else
            failed=$((failed + 1))
            log "  ✗ 发送失败"
        fi
        
        # 间隔避免触发风控
        sleep 2
    done < "$csv_file"
    
    log ""
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "批量发送完成"
    log "总计: $total | 成功: $success | 失败: $failed"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 导出聊天记录
cmd_export() {
    local contact_name="$1"
    local message_count="${2:-30}"
    
    if [ -z "$contact_name" ]; then
        echo "错误: 需要提供联系人名称"
        echo "用法: $0 export \"联系人\" [消息数量]"
        exit 1
    fi
    
    log "导出 $contact_name 的聊天记录（最近 $message_count 条）"
    check_peekaboo
    check_wechat_running || exit 1
    
    # 打开聊天
    cmd_find_and_click_chat "$contact_name"
    sleep 2
    
    # 创建导出目录
    local export_dir="$TEMP_DIR/export/$contact_name"
    mkdir -p "$export_dir"
    
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local md_file="$export_dir/${contact_name}_${timestamp}.md"
    
    # Markdown 头部
    cat > "$md_file" << EOF
# $contact_name 聊天记录

- 导出时间: $(date '+%Y-%m-%d %H:%M:%S')
- 消息数量: $message_count
- 导出工具: WeChat macOS Proxy

---

EOF
    
    log "正在截图聊天记录..."
    
    # 滚动并截图
    local screenshot_count=0
    local max_screenshots=$((message_count / 10 + 1))
    
    for i in $(seq 1 $max_screenshots); do
        local screenshot_path="$export_dir/chat_${i}.png"
        screenshot "$screenshot_path"
        
        if [ -f "$screenshot_path" ]; then
            screenshot_count=$((screenshot_count + 1))
            echo "![聊天记录 $i](./chat_${i}.png)" >> "$md_file"
            echo "" >> "$md_file"
            
            # 向上滚动查看更多历史消息
            peekaboo scroll --direction up --amount 5 --smooth --app "$WECHAT_APP_NAME" 2>/dev/null
            sleep 0.5
        fi
    done
    
    # 添加备注
    cat >> "$md_file" << EOF
---

## 备注

- 截图数量: $screenshot_count
- 如需提取文字内容，请使用 OCR 工具分析截图
- 原始图片位置: $export_dir

EOF
    
    log "✓ 聊天记录已导出"
    log "  Markdown 文件: $md_file"
    log "  截图文件夹: $export_dir"
    log ""
    log "提示: 使用以下命令查看"
    log "  open \"$md_file\""
    
    # 返回文件路径
    echo "EXPORT_MD:$md_file"
    echo "EXPORT_DIR:$export_dir"
}

# 主命令分发
case "${1:-}" in
    test)
        cmd_test
        ;;
    send)
        shift
        cmd_send "$@"
        ;;
    batch-send)
        shift
        cmd_batch_send "$@"
        ;;
    read)
        shift
        cmd_read "$@"
        ;;
    check)
        cmd_check
        ;;
    listen)
        cmd_listen
        ;;
    stop)
        cmd_stop
        ;;
    export)
        shift
        cmd_export "$@"
        ;;
    *)
        usage
        exit 1
        ;;
esac
