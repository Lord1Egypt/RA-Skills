#!/bin/bash
# Telegram语音消息 - 音频格式转换脚本
# 版本: 1.0.0
# 创建: 2026-03-09
# 作者: 银月 (Silvermoon)

# ============================================================================
# 重要提醒：
# 1. Telegram语音消息必须使用OGG格式（libopus编码）
# 2. 大多数TTS服务生成WAV格式，需要转换
# 3. 转换参数影响音频质量和文件大小
# ============================================================================

set -e  # 遇到错误立即退出

# ============================================================================
# 配置部分
# ============================================================================

# 默认音频配置（Telegram优化）
DEFAULT_BITRATE="64k"      # 比特率：平衡质量和大小
DEFAULT_SAMPLE_RATE="48000" # 采样率：48kHz标准
DEFAULT_CHANNELS="1"       # 声道：单声道（语音不需要立体声）
DEFAULT_CODEC="libopus"    # 编码：Telegram要求

# 支持的输入格式
SUPPORTED_INPUT_FORMATS=("wav" "mp3" "m4a" "flac" "aac")

# 临时文件目录
TEMP_DIR="/tmp/audio_converter_$(date +%s)"
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

# 检查必需工具
check_dependencies() {
    if ! command -v ffmpeg &> /dev/null; then
        log_error "缺少必需工具: ffmpeg"
        log_info "请安装:"
        echo "  - Ubuntu/Debian: sudo apt-get install ffmpeg"
        echo "  - macOS: brew install ffmpeg"
        echo "  - CentOS/RHEL: sudo yum install ffmpeg"
        exit 1
    fi
    
    if ! command -v file &> /dev/null; then
        log_warning "缺少file命令，无法检测文件格式"
    fi
}

# 获取文件信息
get_file_info() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        log_error "文件不存在: $file"
        return 1
    fi
    
    # 文件大小
    local size=$(stat -c%s "$file" 2>/dev/null || echo "unknown")
    
    # 文件格式
    local format="unknown"
    if command -v file &> /dev/null; then
        format=$(file "$file" | cut -d: -f2 | sed 's/^ //')
    fi
    
    # 使用ffprobe获取详细信息（如果可用）
    local duration="unknown"
    local codec="unknown"
    local sample_rate="unknown"
    local channels="unknown"
    
    if command -v ffprobe &> /dev/null; then
        local probe_output=$(ffprobe -v error -show_format -show_streams "$file" 2>/dev/null)
        
        duration=$(echo "$probe_output" | grep -E "duration=" | head -1 | cut -d= -f2)
        codec=$(echo "$probe_output" | grep -E "codec_name=" | head -1 | cut -d= -f2)
        sample_rate=$(echo "$probe_output" | grep -E "sample_rate=" | head -1 | cut -d= -f2)
        channels=$(echo "$probe_output" | grep -E "channels=" | head -1 | cut -d= -f2)
    fi
    
    echo "size:$size"
    echo "format:$format"
    echo "duration:$duration"
    echo "codec:$codec"
    echo "sample_rate:$sample_rate"
    echo "channels:$channels"
}

# 检查输入格式是否支持
check_input_format() {
    local file="$1"
    
    # 使用file命令检测格式
    if command -v file &> /dev/null; then
        local file_info=$(file "$file")
        
        for format in "${SUPPORTED_INPUT_FORMATS[@]}"; do
            if [[ "$file_info" =~ $format ]] || [[ "$file_info" =~ ${format^^} ]]; then
                return 0
            fi
        done
        
        log_warning "检测到非常规格式: $file_info"
        log_info "尝试转换，但可能失败"
    fi
    
    # 通过文件扩展名检查
    local extension="${file##*.}"
    extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
    
    for format in "${SUPPORTED_INPUT_FORMATS[@]}"; do
        if [ "$extension" = "$format" ]; then
            return 0
        fi
    done
    
    log_error "不支持的输入格式: .$extension"
    log_info "支持的格式: ${SUPPORTED_INPUT_FORMATS[*]}"
    return 1
}

# ============================================================================
# 转换函数
# ============================================================================

# 基础转换函数
convert_audio() {
    local input_file="$1"
    local output_file="$2"
    local bitrate="$3"
    local sample_rate="$4"
    local channels="$5"
    
    log_info "开始转换: $input_file → $output_file"
    
    # 获取输入文件信息
    local input_info=$(get_file_info "$input_file")
    local input_size=$(echo "$input_info" | grep "size:" | cut -d: -f2)
    local input_format=$(echo "$input_info" | grep "format:" | cut -d: -f2)
    
    log_info "输入文件:"
    log_info "  大小: $input_size 字节"
    log_info "  格式: $input_format"
    
    # 执行转换
    log_info "执行ffmpeg转换..."
    
    local ffmpeg_cmd="ffmpeg -i \"$input_file\" \
        -acodec $DEFAULT_CODEC \
        -b:a \"$bitrate\" \
        -ar \"$sample_rate\" \
        -ac \"$channels\" \
        \"$output_file\" \
        -y"
    
    # 运行ffmpeg，捕获输出
    local ffmpeg_output
    if ffmpeg_output=$(eval "$ffmpeg_cmd" 2>&1); then
        # 检查输出文件
        if [ ! -f "$output_file" ] || [ ! -s "$output_file" ]; then
            log_error "转换失败: 输出文件为空或不存在"
            return 1
        fi
        
        # 获取输出文件信息
        local output_info=$(get_file_info "$output_file")
        local output_size=$(echo "$output_info" | grep "size:" | cut -d: -f2)
        local output_format=$(echo "$output_info" | grep "format:" | cut -d: -f2)
        
        # 计算压缩比例
        local compression_ratio="unknown"
        if [ "$input_size" != "unknown" ] && [ "$output_size" != "unknown" ]; then
            compression_ratio=$((output_size * 100 / input_size))
        fi
        
        log_success "转换成功！"
        log_info "输出文件:"
        log_info "  大小: $output_size 字节"
        log_info "  格式: $output_format"
        
        if [ "$compression_ratio" != "unknown" ]; then
            log_info "  压缩比例: $compression_ratio%"
        fi
        
        # 显示参数
        log_info "转换参数:"
        log_info "  比特率: $bitrate"
        log_info "  采样率: ${sample_rate}Hz"
        log_info "  声道: $channels"
        log_info "  编码: $DEFAULT_CODEC"
        
        return 0
    else
        log_error "ffmpeg转换失败"
        log_info "错误信息:"
        echo "$ffmpeg_output" | tail -20
        return 1
    fi
}

# 批量转换函数
batch_convert() {
    local input_dir="$1"
    local output_dir="$2"
    local bitrate="$3"
    local sample_rate="$4"
    local channels="$5"
    
    if [ ! -d "$input_dir" ]; then
        log_error "输入目录不存在: $input_dir"
        return 1
    fi
    
    mkdir -p "$output_dir"
    
    local converted_count=0
    local failed_count=0
    
    log_info "开始批量转换: $input_dir → $output_dir"
    
    # 查找音频文件
    local audio_files=()
    for format in "${SUPPORTED_INPUT_FORMATS[@]}"; do
        while IFS= read -r -d '' file; do
            audio_files+=("$file")
        done < <(find "$input_dir" -name "*.$format" -type f -print0 2>/dev/null)
    done
    
    if [ ${#audio_files[@]} -eq 0 ]; then
        log_warning "未找到支持的音频文件"
        return 0
    fi
    
    log_info "找到 ${#audio_files[@]} 个音频文件"
    
    # 逐个转换
    for input_file in "${audio_files[@]}"; do
        local filename=$(basename "$input_file")
        local name="${filename%.*}"
        local output_file="$output_dir/${name}.ogg"
        
        echo ""
        log_info "处理: $filename"
        
        if convert_audio "$input_file" "$output_file" "$bitrate" "$sample_rate" "$channels"; then
            ((converted_count++))
        else
            ((failed_count++))
            log_warning "跳过: $filename"
        fi
    done
    
    echo ""
    log_success "批量转换完成！"
    log_info "统计:"
    log_info "  成功: $converted_count 个"
    log_info "  失败: $failed_count 个"
    log_info "  总计: ${#audio_files[@]} 个"
    
    if [ $failed_count -gt 0 ]; then
        log_warning "有 $failed_count 个文件转换失败，请检查文件格式"
    fi
    
    return 0
}

# ============================================================================
# 清理函数
# ============================================================================

cleanup() {
    log_info "清理临时文件..."
    rm -rf "$TEMP_DIR" 2>/dev/null || true
    log_success "清理完成"
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 显示标题
    echo "=================================================="
    echo "Telegram音频格式转换器 v1.0.0"
    echo "=================================================="
    echo "用途: 将音频转换为Telegram语音消息兼容的OGG格式"
    echo "=================================================="
    
    # 检查依赖
    check_dependencies
    
    # 解析参数
    local mode="single"
    local input_path=""
    local output_path=""
    local bitrate="$DEFAULT_BITRATE"
    local sample_rate="$DEFAULT_SAMPLE_RATE"
    local channels="$DEFAULT_CHANNELS"
    
    # 参数解析
    while [ $# -gt 0 ]; do
        case "$1" in
            # 输入文件/目录
            -i|--input)
                input_path="$2"
                shift 2
                ;;
            
            # 输出文件/目录
            -o|--output)
                output_path="$2"
                shift 2
                ;;
            
            # 批量模式
            -b|--batch)
                mode="batch"
                shift
                ;;
            
            # 音频参数
            --bitrate)
                bitrate="$2"
                shift 2
                ;;
            
            --sample-rate)
                sample_rate="$2"
                shift 2
                ;;
            
            --channels)
                channels="$2"
                shift 2
                ;;
            
            # 帮助
            -h|--help)
                show_help
                exit 0
                ;;
            
            # 其他参数
            *)
                if [ -z "$input_path" ]; then
                    input_path="$1"
                elif [ -z "$output_path" ]; then
                    output_path="$1"
                fi
                shift
                ;;
        esac
    done
    
    # 检查输入
    if [ -z "$input_path" ]; then
        log_error "未指定输入文件或目录"
        show_help
        exit 1
    fi
    
    if [ ! -e "$input_path" ]; then
        log_error "输入路径不存在: $input_path"
        exit 1
    fi
    
    # 设置输出路径
    if [ -z "$output_path" ]; then
        if [ "$mode" = "single" ] && [ -f "$input_path" ]; then
            # 单个文件：使用相同名称，扩展名改为.ogg
            local dirname=$(dirname "$input_path")
            local filename=$(basename "$input_path")
            local name="${filename%.*}"
            output_path="$dirname/${name}.ogg"
        else
            # 批量模式或目录输入：使用默认输出目录
            output_path="converted_audio"
        fi
    fi
    
    # 执行转换
    case "$mode" in
        "single")
            if [ ! -f "$input_path" ]; then
                log_error "输入不是文件: $input_path"
                exit 1
            fi
            
            check_input_format "$input_path" || exit 1
            
            convert_audio "$input_path" "$output_path" "$bitrate" "$sample_rate" "$channels"
            ;;
        
        "batch")
            if [ ! -d "$input_path" ]; then
                log_error "输入不是目录: $input_path"
                exit 1
            fi
            
            batch_convert "$input_path" "$output_path" "$bitrate" "$sample_rate" "$channels"
            ;;
    esac
    
    # 清理
    cleanup
    
    return 0
}

# 显示帮助
show_help() {
    cat << EOF
Telegram音频格式转换器

用法:
  $0 [选项] <输入文件> [输出文件]
  $0 --batch [选项] <输入目录> [输出目录]

选项:
  -i, --input <路径>      输入文件或目录
  -o, --output <路径>     输出文件或目录
  -b, --batch             批量转换模式
  
  音频参数:
    --bitrate <值>        比特率 (默认: 64k)
    --sample-rate <值>    采样率 (默认: 48000)
    --channels <值>       声道数 (默认: 1)
  
  其他:
    -h, --help            显示此帮助信息

示例:
  1. 转换单个文件:
     $0 input.wav output.ogg
     $0 --input input.mp3 --output message.ogg
  
  2. 批量转换目录中的所有音频:
     $0 --batch audio_input/ converted_audio/
     $0 -b -i audio_files/ -o telegram_audio/
  
  3. 自定义音频参数:
     $0 input.wav --bitrate 128k --sample-rate 44100
  
支持的输入格式: ${SUPPORTED_INPUT_FORMATS[*]}
输出格式: OGG (libopus编码) - Telegram语音消息要求

注意:
  - Telegram语音消息必须使用OGG格式 (libopus编码)
  - 默认参数已优化Telegram语音消息
  - 批量模式会转换目录中所有支持的音频文件
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
# 1. 基本转换：
#    ./audio_converter.sh input.wav
#    输出: input.ogg (相同目录)
#
# 2. 指定输出文件：
#    ./audio_converter.sh input.mp3 output.ogg
#
# 3. 批量转换目录：
#    ./audio_converter.sh --batch audio_input/ converted/
#
# 4. 自定义参数：
#    ./audio_converter.sh --input audio.wav --bitrate 96k --channels 1
#
# 5. 集成使用：
#    # 生成音频
#    audio_file=$(./tts_generator.sh "消息内容")
#    
#    # 转换格式
#    converted_file=$(./audio_converter.sh "$audio_file")
#    
#    # 发送消息
#    send_telegram_message "$converted_file"
# ============================================================================