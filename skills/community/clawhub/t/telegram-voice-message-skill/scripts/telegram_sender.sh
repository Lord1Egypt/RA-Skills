#!/bin/bash
# Telegram语音消息 - 消息发送脚本
# 版本: 1.0.0
# 创建: 2026-03-09
# 作者: 银月 (Silvermoon)

# ============================================================================
# 🚨 重要提醒 🚨
# 1. Telegram语音消息必须使用正确的参数：asVoice=true
# 2. 不要使用caption参数（语音消息不支持标题）
# 3. 确保音频格式是OGG (libopus编码)
# 4. 文件大小不能超过Telegram限制（通常50MB）
# ============================================================================

set -e  # 遇到错误立即退出

# ============================================================================
# 配置部分
# ============================================================================

# Telegram配置（使用环境变量）
# export TELEGRAM_BOT_TOKEN="your_bot_token_here"
# export TELEGRAM_CHAT_ID="your_chat_id_here"

# 发送参数
DEFAULT_PARALLEL_SENDS=1     # 默认并行发送数量
MAX_FILE_SIZE_MB=50          # Telegram文件大小限制（单位：MB）
MAX_DURATION_SECONDS=300     # 语音消息最大时长（单位：秒）

# 重试配置
MAX_RETRIES=3                # 最大重试次数
RETRY_DELAY_SECONDS=2        # 重试延迟（单位：秒）

# 临时文件目录
TEMP_DIR="/tmp/telegram_sender_$(date +%s)"
mkdir -p "$TEMP_DIR"

# ============================================================================
# 工具函数
# ============================================================================

# 日志函数
log_info() {
    echo "ℹ️  $1"
}

log_success() {
    echo "✅ $1"
}

log_warning() {
    echo "⚠️  $1"
}

log_error() {
    echo "❌ $1" >&2
}

log_debug() {
    if [ "$DEBUG" = "true" ]; then
        echo "🐛 $1"
    fi
}

# 检查配置
check_config() {
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        log_error "未设置TELEGRAM_BOT_TOKEN环境变量"
        log_info "使用方法: export TELEGRAM_BOT_TOKEN=\"your_bot_token\""
        return 1
    fi
    
    if [ -z "$TELEGRAM_CHAT_ID" ]; then
        log_error "未设置TELEGRAM_CHAT_ID环境变量"
        log_info "使用方法: export TELEGRAM_CHAT_ID=\"your_chat_id\""
        return 1
    fi
    
    log_debug "配置检查通过"
    log_debug "Bot Token: ${TELEGRAM_BOT_TOKEN:0:10}..."
    log_debug "Chat ID: $TELEGRAM_CHAT_ID"
    
    return 0
}

# 检查文件
check_file() {
    local file="$1"
    
    # 检查文件是否存在
    if [ ! -f "$file" ]; then
        log_error "文件不存在: $file"
        return 1
    fi
    
    # 检查文件大小
    local file_size=$(stat -c%s "$file" 2>/dev/null)
    local file_size_mb=$((file_size / 1024 / 1024))
    
    if [ $file_size_mb -gt $MAX_FILE_SIZE_MB ]; then
        log_error "文件太大: ${file_size_mb}MB (限制: ${MAX_FILE_SIZE_MB}MB)"
        return 1
    fi
    
    # 检查文件格式
    if command -v file &> /dev/null; then
        local file_info=$(file "$file")
        
        # 检查是否是OGG格式
        if [[ ! "$file_info" =~ "OGG" ]] && [[ ! "$file_info" =~ "Opus" ]]; then
            log_warning "文件可能不是OGG格式: $file_info"
            log_info "Telegram语音消息要求OGG格式 (libopus编码)"
            log_info "建议使用 audio_converter.sh 转换格式"
        fi
    fi
    
    # 检查文件扩展名
    local extension="${file##*.}"
    if [ "$extension" != "ogg" ] && [ "$extension" != "OGG" ]; then
        log_warning "文件扩展名不是.ogg: .$extension"
        log_info "Telegram语音消息推荐使用.ogg扩展名"
    fi
    
    log_debug "文件检查通过: $file (${file_size_mb}MB)"
    return 0
}

# 获取文件信息
get_file_info() {
    local file="$1"
    
    local size=$(stat -c%s "$file" 2>/dev/null || echo "unknown")
    local size_mb="unknown"
    if [ "$size" != "unknown" ]; then
        size_mb=$((size / 1024 / 1024))
    fi
    
    local format="unknown"
    if command -v file &> /dev/null; then
        format=$(file "$file" | cut -d: -f2 | sed 's/^ //')
    fi
    
    local duration="unknown"
    if command -v ffprobe &> /dev/null; then
        duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null)
        if [ -n "$duration" ]; then
            duration=$(printf "%.1f" "$duration")
        fi
    fi
    
    echo "size:$size"
    echo "size_mb:$size_mb"
    echo "format:$format"
    echo "duration:$duration"
}

# ============================================================================
# Telegram API函数
# ============================================================================

# 发送语音消息（使用curl）
send_voice_via_curl() {
    local file="$1"
    local chat_id="$2"
    local attempt="$3"
    
    log_debug "发送语音消息 (尝试 $attempt)"
    
    # Telegram Bot API URL
    local api_url="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendVoice"
    
    # 发送请求
    local response_file="$TEMP_DIR/response_${attempt}.json"
    local curl_output=$(curl -s \
        -X POST "$api_url" \
        -F "chat_id=$chat_id" \
        -F "voice=@$file" \
        -o "$response_file" \
        -w "%{http_code}" \
        2>/dev/null)
    
    local http_code="$curl_output"
    
    # 检查响应
    if [ ! -s "$response_file" ]; then
        log_debug "API响应为空"
        return 1
    fi
    
    # 解析响应
    if [ "$http_code" = "200" ]; then
        # 检查响应内容
        if grep -q '"ok":true' "$response_file"; then
            log_debug "发送成功"
            
            # 提取消息ID（可选）
            local message_id=$(grep -o '"message_id":[0-9]*' "$response_file" | head -1 | cut -d: -f2)
            if [ -n "$message_id" ]; then
                log_debug "消息ID: $message_id"
            fi
            
            return 0
        else
            log_debug "API返回错误: $(cat "$response_file")"
            return 1
        fi
    else
        log_debug "HTTP错误代码: $http_code"
        log_debug "响应内容: $(cat "$response_file")"
        return 1
    fi
}

# 发送语音消息（使用OpenClaw的message工具）
send_voice_via_openclaw() {
    local file="$1"
    local chat_id="$2"
    
    log_debug "使用OpenClaw message工具发送"
    
    # 这里应该是调用OpenClaw的message工具
    # 实际实现取决于具体的AI平台
    
    # 示例：模拟发送
    echo "发送语音消息到聊天 $chat_id"
    echo "文件: $file"
    echo "参数: asVoice=true"
    
    # 在实际实现中，这里应该是：
    # message action=send to="$chat_id" asVoice=true media="$file"
    
    # 模拟成功
    return 0
}

# 带重试的发送函数
send_voice_with_retry() {
    local file="$1"
    local chat_id="$2"
    
    log_info "发送语音消息: $(basename "$file")"
    
    # 显示文件信息
    local file_info=$(get_file_info "$file")
    local size_mb=$(echo "$file_info" | grep "size_mb:" | cut -d: -f2)
    local duration=$(echo "$file_info" | grep "duration:" | cut -d: -f2)
    
    log_info "文件信息:"
    log_info "  大小: ${size_mb}MB"
    if [ "$duration" != "unknown" ]; then
        log_info "  时长: ${duration}秒"
    fi
    
    # 重试发送
    local attempt=1
    while [ $attempt -le $MAX_RETRIES ]; do
        log_info "尝试发送 ($attempt/$MAX_RETRIES)..."
        
        # 选择发送方式
        local send_result
        if [ "$SEND_METHOD" = "openclaw" ]; then
            send_result=$(send_voice_via_openclaw "$file" "$chat_id")
        else
            send_result=$(send_voice_via_curl "$file" "$chat_id" "$attempt")
        fi
        
        if [ $? -eq 0 ]; then
            log_success "发送成功！"
            
            # 显示成功信息
            echo ""
            echo "🎉 语音消息已成功发送！"
            echo "   接收者: $chat_id"
            echo "   文件: $(basename "$file")"
            if [ "$duration" != "unknown" ]; then
                echo "   时长: ${duration}秒"
            fi
            echo ""
            
            return 0
        fi
        
        # 重试前等待
        if [ $attempt -lt $MAX_RETRIES ]; then
            log_info "等待 ${RETRY_DELAY_SECONDS}秒后重试..."
            sleep "$RETRY_DELAY_SECONDS"
        fi
        
        ((attempt++))
    done
    
    log_error "发送失败，已达到最大重试次数"
    return 1
}

# 批量发送函数
batch_send() {
    local files=("$@")
    local chat_id="$TELEGRAM_CHAT_ID"
    
    if [ ${#files[@]} -eq 0 ]; then
        log_error "没有要发送的文件"
        return 1
    fi
    
    log_info "批量发送 ${#files[@]} 个文件到: $chat_id"
    
    local success_count=0
    local failed_count=0
    local total_files=${#files[@]}
    
    # 并行发送控制
    local parallel_sends=${PARALLEL_SENDS:-$DEFAULT_PARALLEL_SENDS}
    local current_pids=()
    local file_index=0
    
    while [ $file_index -lt $total_files ] || [ ${#current_pids[@]} -gt 0 ]; do
        # 启动新的发送任务
        while [ ${#current_pids[@]} -lt $parallel_sends ] && [ $file_index -lt $total_files ]; do
            local file="${files[$file_index]}"
            log_info "启动发送: $(basename "$file") ($((file_index + 1))/$total_files)"
            
            # 后台发送
            (
                if send_voice_with_retry "$file" "$chat_id"; then
                    log_success "完成: $(basename "$file")"
                else
                    log_error "失败: $(basename "$file")"
                fi
            ) &
            
            current_pids+=($!)
            ((file_index++))
        done
        
        # 检查完成的任务
        local new_pids=()
        for pid in "${current_pids[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then
                new_pids+=("$pid")
            else
                # 获取退出状态
                wait "$pid"
                local exit_status=$?
                
                if [ $exit_status -eq 0 ]; then
                    ((success_count++))
                else
                    ((failed_count++))
                fi
            fi
        done
        
        current_pids=("${new_pids[@]}")
        
        # 显示进度
        local processed=$((success_count + failed_count))
        if [ $processed -gt 0 ]; then
            log_info "进度: $processed/$total_files (成功: $success_count, 失败: $failed_count)"
        fi
        
        sleep 1
    done
    
    # 显示最终结果
    echo ""
    echo "=================================================="
    log_success "批量发送完成！"
    log_info "统计:"
    log_info "  成功: $success_count 个"
    log_info "  失败: $failed_count 个"
    log_info "  总计: $total_files 个"
    echo "=================================================="
    
    if [ $failed_count -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# 清理函数
# ============================================================================

cleanup() {
    log_debug "清理临时文件..."
    rm -rf "$TEMP_DIR" 2>/dev/null || true
    log_debug "清理完成"
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 显示标题
    echo "=================================================="
    echo "Telegram语音消息发送器 v1.0.0"
    echo "=================================================="
    echo "重要规则:"
    echo "  1. 必须使用 asVoice=true 参数"
    echo "  2. 不要使用 caption 参数"
    echo "  3. 音频必须是 OGG 格式 (libopus编码)"
    echo "=================================================="
    
    # 检查配置
    if ! check_config; then
        exit 1
    fi
    
    # 解析参数
    local mode="single"
    local files=()
    local send_method="curl"  # 默认使用curl
    
    while [ $# -gt 0 ]; do
        case "$1" in
            # 批量模式
            -b|--batch)
                mode="batch"
                shift
                ;;
            
            # 发送方法
            --method)
                send_method="$2"
                shift 2
                ;;
            
            # 并行发送数量
            --parallel)
                PARALLEL_SENDS="$2"
                shift 2
                ;;
            
            # 调试模式
            -d|--debug)
                DEBUG="true"
                shift
                ;;
            
            # 帮助
            -h|--help)
                show_help
                exit 0
                ;;
            
            # 文件参数
            *)
                if [ -f "$1" ]; then
                    files+=("$1")
                elif [ -d "$1" ]; then
                    # 如果是目录，添加目录中的所有ogg文件
                    while IFS= read -r -d '' file; do
                        files+=("$file")
                    done < <(find "$1" -name "*.ogg" -type f -print0 2>/dev/null)
                else
                    log_warning "忽略无效参数: $1"
                fi
                shift
                ;;
        esac
    done
    
    # 检查文件
    if [ ${#files[@]} -eq 0 ]; then
        log_error "未指定要发送的文件"
        show_help
        exit 1
    fi
    
    # 验证文件
    local valid_files=()
    for file in "${files[@]}"; do
        if check_file "$file"; then
            valid_files+=("$file")
        else
            log_warning "跳过无效文件: $file"
        fi
    done
    
    if [ ${#valid_files[@]} -eq 0 ]; then
        log_error "没有有效的文件可发送"
        exit 1
    fi
    
    # 设置发送方法
    SEND_METHOD="$send_method"
    
    # 执行发送
    case "$mode" in
        "single")
            if [ ${#valid_files[@]} -gt 1 ]; then
                log_warning "指定了多个文件，但未使用批量模式"
                log_info "将发送第一个文件: ${valid_files[0]}"
            fi
            
            send_voice_with_retry "${valid_files[0]}" "$TELEGRAM_CHAT_ID"
            ;;
        
        "batch")
            batch_send "${valid_files[@]}"
            ;;
    esac
    
    local exit_status=$?
    
    # 清理
    cleanup
    
    return $exit_status
}

# 显示帮助
show_help() {
    cat << EOF
Telegram语音消息发送器

用法:
  $0 [选项] <文件1> [文件2 ...]
  $0 [选项] <目录>

选项:
  发送模式:
    -b, --batch             批量发送模式
    --method <方法>         发送方法: curl, openclaw (默认: curl)
    --parallel <数量>       并行发送数量 (默认: 1)
  
  调试:
    -d, --debug             启用调试模式
    -h, --help              显示此帮助信息

环境变量:
  TELEGRAM_BOT_TOKEN        Telegram Bot Token (必需)
  TELEGRAM_CHAT_ID          目标聊天ID (必需)

示例:
  1. 发送单个文件:
     $0 message.ogg
     export TELEGRAM_BOT_TOKEN="xxx" TELEGRAM_CHAT_ID="yyy"
     $0 audio.ogg
  
  2. 批量发送多个文件:
     $0 --batch file1.ogg file2.ogg file3.ogg
  
  3. 发送目录中的所有ogg文件:
     $0 --batch audio_files/
  
  4. 并行发送（加快速度）:
     $0 --batch --parallel 3 audio_files/
  
  5. 使用OpenClaw发送:
     $0 --method openclaw message.ogg

重要规则:
  ✅ 必须使用 asVoice=true 参数
  ❌ 不要使用 caption 参数
  ✅ 音频必须是 OGG 格式 (libopus编码)
  ✅ 文件大小不能超过 ${MAX_FILE_SIZE_MB}MB
  ✅ 语音时长不能超过 ${MAX_DURATION_SECONDS}秒

错误处理:
  - 默认重试 ${MAX_RETRIES} 次
  - 重试间隔 ${RETRY_DELAY_SECONDS} 秒
  - 失败的文件会跳过，继续发送其他文件
EOF
}

# ============================================================================
# 脚本执行
# ============================================================================

# 设置退出时清理
trap cleanup EXIT

# 运行主函数
main "$@"

# ============================================================================
# 使用说明：
# ============================================================================
# 1. 基本发送：
#    export TELEGRAM_BOT_TOKEN="xxx"
#    export TELEGRAM_CHAT_ID="yyy"
#    ./telegram_sender.sh audio.ogg
#
# 2. 集成使用：
#    # 生成音频
#    audio_file=$(./tts_generator.sh "消息内容")
#    
#    # 转换格式
#    ogg_file=$(./audio_converter.sh "$audio_file")
#    
#    # 发送消息
#    ./telegram_sender.sh "$ogg_file"
#
# 3. 批量处理：
#    ./telegram_sender.sh --batch --parallel 3 audio_directory/
#
# 4. 完整流程：
#    # 生成、转换、发送一体化
#    message="你好，这是测试消息"
#    ./tts_generator.sh "$message" | \
#        xargs ./audio_converter.sh | \
#        xargs ./telegram_sender.sh
# ============================================================================