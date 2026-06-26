#!/bin/bash
# Telegram语音消息 - TTS生成脚本
# 版本: 1.0.0
# 创建: 2026-03-09
# 作者: 银月 (Silvermoon)

# ============================================================================
# 重要提醒：
# 1. 本脚本是模板，不包含真实的API密钥
# 2. 使用前请配置环境变量或修改配置部分
# 3. TTS服务URL可能很快过期，必须立即下载
# ============================================================================

set -e  # 遇到错误立即退出

# ============================================================================
# 配置部分（请根据实际情况配置）
# ============================================================================

# 方式1：使用环境变量（推荐）
# export ALIYUN_TTS_API_KEY="your_api_key_here"
# export TELEGRAM_BOT_TOKEN="your_bot_token_here"
# export TELEGRAM_CHAT_ID="your_chat_id_here"

# 方式2：直接在这里配置（不推荐用于生产环境）
# ALIYUN_TTS_API_KEY="your_api_key_here"
# TELEGRAM_BOT_TOKEN="your_bot_token_here"
# TELEGRAM_CHAT_ID="your_chat_id_here"

# TTS服务配置
TTS_SERVICE="aliyun"  # 可选: aliyun, openai, google
TTS_MODEL="qwen3-tts-flash"
TTS_VOICE="Maia"
TTS_LANGUAGE="Chinese"

# 音频配置
AUDIO_BITRATE="64k"
AUDIO_SAMPLE_RATE="48000"
AUDIO_CHANNELS="1"

# 临时文件目录
TEMP_DIR="/tmp/telegram_voice_$(date +%s)"
mkdir -p "$TEMP_DIR"

# ============================================================================
# 工具函数
# ============================================================================

# 打印带颜色的日志
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

# 检查必需工具
check_dependencies() {
    local missing_tools=()
    
    for tool in curl ffmpeg; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "缺少必需工具: ${missing_tools[*]}"
        log_info "请安装:"
        for tool in "${missing_tools[@]}"; do
            echo "  - $tool: sudo apt-get install $tool 或 brew install $tool"
        done
        exit 1
    fi
}

# 检查配置
check_config() {
    if [ -z "$ALIYUN_TTS_API_KEY" ] && [ "$TTS_SERVICE" = "aliyun" ]; then
        log_error "请设置ALIYUN_TTS_API_KEY环境变量"
        log_info "使用方法: export ALIYUN_TTS_API_KEY=\"your_api_key_here\""
        exit 1
    fi
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        log_warning "未设置TELEGRAM_BOT_TOKEN，将只生成音频不发送"
    fi
    
    if [ -z "$TELEGRAM_CHAT_ID" ]; then
        log_warning "未设置TELEGRAM_CHAT_ID，将只生成音频不发送"
    fi
}

# ============================================================================
# TTS服务函数
# ============================================================================

# 阿里云TTS
generate_aliyun_tts() {
    local text="$1"
    local output_file="$2"
    
    log_info "调用阿里云TTS API..."
    
    # 构建请求数据
    local request_data=$(cat <<EOF
{
    "model": "$TTS_MODEL",
    "input": {
        "text": "$text",
        "voice": "$TTS_VOICE",
        "language_type": "$TTS_LANGUAGE"
    }
}
EOF
)
    
    # 调用API
    local response_file="$TEMP_DIR/tts_response.json"
    curl -s -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
        -H "Authorization: Bearer $ALIYUN_TTS_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$request_data" > "$response_file"
    
    # 检查响应
    if [ ! -s "$response_file" ]; then
        log_error "TTS API响应为空"
        return 1
    fi
    
    # 解析响应获取音频URL
    local audio_url=$(python3 -c "
import json, sys
try:
    with open('$response_file', 'r') as f:
        data = json.load(f)
    
    # 检查错误
    if 'code' in data and data['code'] != '':
        print(f'ERROR: {data.get(\"message\", \"Unknown error\")}')
        sys.exit(1)
    
    # 获取音频URL
    url = data.get('output', {}).get('audio', {}).get('url')
    if url:
        print(url)
    else:
        print('ERROR: 未找到音频URL')
        sys.exit(1)
        
except Exception as e:
    print(f'ERROR: 解析响应失败: {str(e)}')
    sys.exit(1)
")
    
    if [[ "$audio_url" == ERROR* ]]; then
        log_error "TTS API错误: $audio_url"
        return 1
    fi
    
    log_info "获取音频URL: ${audio_url:0:80}..."
    
    # 立即下载音频（URL可能很快过期）
    download_audio "$audio_url" "$output_file"
}

# OpenAI TTS
generate_openai_tts() {
    local text="$1"
    local output_file="$2"
    
    log_info "调用OpenAI TTS API..."
    
    if [ -z "$OPENAI_API_KEY" ]; then
        log_error "请设置OPENAI_API_KEY环境变量"
        return 1
    fi
    
    curl -s https://api.openai.com/v1/audio/speech \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"tts-1\",
            \"input\": \"$text\",
            \"voice\": \"alloy\"
        }" \
        --output "$output_file"
    
    if [ ! -s "$output_file" ]; then
        log_error "OpenAI TTS生成失败"
        return 1
    fi
}

# 通用下载函数（带重试）
download_audio() {
    local url="$1"
    local output_file="$2"
    local max_retries=3
    
    log_info "下载音频文件..."
    
    for i in $(seq 1 $max_retries); do
        log_info "尝试 $i/$max_retries..."
        
        if curl -s --max-time 10 -o "$output_file" "$url"; then
            if [ -s "$output_file" ]; then
                local file_size=$(stat -c%s "$output_file" 2>/dev/null || echo "unknown")
                log_success "下载成功: $output_file ($file_size 字节)"
                return 0
            else
                log_warning "下载的文件为空"
            fi
        else
            log_warning "下载失败"
        fi
        
        if [ $i -lt $max_retries ]; then
            sleep 1
        fi
    done
    
    log_error "下载失败，URL可能已过期"
    return 1
}

# 主生成函数
generate_audio() {
    local text="$1"
    local output_file="$2"
    
    case "$TTS_SERVICE" in
        "aliyun")
            generate_aliyun_tts "$text" "$output_file"
            ;;
        "openai")
            generate_openai_tts "$text" "$output_file"
            ;;
        *)
            log_error "不支持的TTS服务: $TTS_SERVICE"
            log_info "支持的服务: aliyun, openai"
            return 1
            ;;
    esac
}

# ============================================================================
# 格式转换函数
# ============================================================================

convert_to_ogg() {
    local input_file="$1"
    local output_file="$2"
    
    log_info "转换音频格式: WAV → OGG"
    
    if [ ! -f "$input_file" ]; then
        log_error "输入文件不存在: $input_file"
        return 1
    fi
    
    # 检查输入文件格式
    local file_info=$(file "$input_file")
    if [[ ! "$file_info" =~ "WAVE audio" ]] && [[ ! "$file_info" =~ "MPEG ADTS" ]]; then
        log_warning "输入文件可能不是标准音频格式: $file_info"
    fi
    
    # 转换为OGG格式（Telegram语音消息要求）
    ffmpeg -i "$input_file" \
        -acodec libopus \
        -b:a "$AUDIO_BITRATE" \
        -ar "$AUDIO_SAMPLE_RATE" \
        -ac "$AUDIO_CHANNELS" \
        "$output_file" \
        -y 2>/dev/null
    
    if [ ! -s "$output_file" ]; then
        log_error "格式转换失败"
        return 1
    fi
    
    local input_size=$(stat -c%s "$input_file" 2>/dev/null || echo "unknown")
    local output_size=$(stat -c%s "$output_file" 2>/dev/null || echo "unknown")
    
    log_success "转换成功: $output_file"
    log_info "  输入大小: $input_size 字节"
    log_info "  输出大小: $output_size 字节"
    log_info "  压缩比例: $((output_size * 100 / input_size))%"
    
    return 0
}

# ============================================================================
# 清理函数
# ============================================================================

cleanup() {
    log_info "清理临时文件..."
    rm -rf "$TEMP_DIR" 2>/dev/null || true
    
    # 可选：清理旧的临时文件
    find /tmp -name "telegram_voice_*" -type d -mtime +1 2>/dev/null | xargs rm -rf 2>/dev/null || true
    
    log_success "清理完成"
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        echo "用法: $0 \"要说的文本\" [输出文件]"
        echo "示例: $0 \"你好，我是AI助手\" output.ogg"
        echo ""
        echo "选项:"
        echo "  --service aliyun|openai   选择TTS服务（默认: aliyun）"
        echo "  --voice 音色名称         设置TTS音色"
        echo "  --help                   显示帮助信息"
        exit 1
    fi
    
    # 解析参数
    local text="$1"
    local output_file="${2:-$TEMP_DIR/output.ogg}"
    
    # 显示启动信息
    echo "=================================================="
    echo "Telegram语音消息生成器 v1.0.0"
    echo "=================================================="
    echo "文本: ${text:0:100}..."
    echo "长度: ${#text} 字符"
    echo "服务: $TTS_SERVICE"
    echo "输出: $output_file"
    echo "=================================================="
    
    # 执行检查
    check_dependencies
    check_config
    
    # 生成临时文件名
    local temp_wav="$TEMP_DIR/audio_$(date +%s).wav"
    
    # 生成音频
    if ! generate_audio "$text" "$temp_wav"; then
        log_error "音频生成失败"
        cleanup
        exit 1
    fi
    
    # 转换格式
    if ! convert_to_ogg "$temp_wav" "$output_file"; then
        log_error "格式转换失败"
        cleanup
        exit 1
    fi
    
    # 显示结果
    echo ""
    echo "=================================================="
    log_success "音频生成完成！"
    echo "文件: $output_file"
    echo "大小: $(stat -c%s "$output_file" 2>/dev/null || echo "unknown") 字节"
    echo "格式: $(file "$output_file")"
    echo ""
    echo "下一步:"
    echo "1. 检查音频格式是否为OGG (libopus)"
    echo "2. 使用正确的参数发送到Telegram"
    echo "3. 确保使用 asVoice=true 参数"
    echo "=================================================="
    
    # 清理临时文件
    cleanup
    
    # 输出文件路径（便于其他脚本使用）
    echo "$output_file"
}

# 设置退出时清理
trap cleanup EXIT

# 运行主函数
main "$@"

# ============================================================================
# 使用示例：
# ============================================================================
# 1. 基本使用：
#    ./tts_generator.sh "你好，世界"
#
# 2. 指定输出文件：
#    ./tts_generator.sh "测试消息" /tmp/message.ogg
#
# 3. 使用环境变量：
#    export ALIYUN_TTS_API_KEY="your_key"
#    ./tts_generator.sh "环境变量测试"
#
# 4. 集成到其他脚本：
#    output=$(./tts_generator.sh "要发送的消息")
#    echo "生成的音频: $output"
# ============================================================================