#!/bin/bash

# =============================================================================
# Whisper Transcriber - 语音转文字脚本
# =============================================================================
# 功能：自动转换音频格式并使用 Whisper.cpp 进行语音识别
# 支持：OGG, WAV, MP3, FLAC, M4A 等格式
# =============================================================================

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置（可通过环境变量覆盖）
# 默认使用 base：速度/精度更均衡（large-v3 首次加载慢且占用更大）
DEFAULT_MODEL="${WHISPER_DEFAULT_MODEL:-base}"
DEFAULT_LANG="${WHISPER_DEFAULT_LANG:-zh}"
# NOTE: actual per-run temp dir is created in main() via mktemp for safety.
TEMP_DIR="${WHISPER_TEMP_DIR:-${TMPDIR:-/tmp}}"

# 技能目录和模型目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_DIR_SKILL="${WHISPER_MODEL_DIR:-$SCRIPT_DIR/assets/models}"
# Default download directory = skill assets/models (portable; repo ignores binaries via .gitignore)
MODEL_DIR_USER="${WHISPER_MODEL_DIR_USER:-$MODEL_DIR_SKILL}"

# 获取模型文件名（兼容老版本 bash）
get_model_file() {
    local model_name="$1"
    case "$model_name" in
        tiny) echo "ggml-tiny.bin" ;;
        base) echo "ggml-base.bin" ;;
        small) echo "ggml-small.bin" ;;
        medium) echo "ggml-medium.bin" ;;
        large) echo "ggml-large-v3.bin" ;;
        *) echo "ggml-base.bin" ;;
    esac
}

# 显示帮助信息
show_help() {
    cat << EOF
🎤 Whisper Transcriber - 语音转文字

用法：$0 <音频文件/目录> [选项]

参数:
  音频文件/目录    要转写的音频文件或包含音频的目录

选项:
  -m, --model MODEL     模型名称 (tiny|base|small|medium|large)
                        默认：$DEFAULT_MODEL
  -l, --lang LANG       语言代码 (zh|en|auto)
                        默认：$DEFAULT_LANG
  -o, --output FILE     输出文件路径
  -b, --batch           批量处理目录中的所有音频
  -s, --srt             输出 SRT 字幕格式
  -t, --txt             输出纯文本格式（无时间戳）
  -j, --json            输出 JSON 格式
  -c, --clean           处理后清理临时文件
  -n, --no-timestamp    不输出时间戳
  -v, --verbose         显示详细输出
  -h, --help            显示此帮助信息

模型说明:
  tiny   - 75MB,   最快，精度一般
  base   - 142MB,  平衡推荐 ⭐
  small  - 466MB,  精度好
  medium - 1.5GB,  精度很好
  large  - 2.9GB,  精度最佳

示例:
  $0 voice.ogg                    # 使用默认配置转写
  $0 voice.ogg -m large           # 使用 large 模型
  $0 voice.ogg -l en              # 识别英语
  $0 ./recordings/ -b -s          # 批量转写并生成 SRT
  $0 meeting.ogg -o notes.txt     # 输出到指定文件

EOF
}

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    local missing=()
    
    if ! command -v whisper-cli &> /dev/null; then
        missing+=("whisper-cpp")
    fi
    
    if ! command -v ffmpeg &> /dev/null; then
        missing+=("ffmpeg")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "缺少依赖：${missing[*]}"
        echo ""
        echo "请运行安装脚本（跨平台自动检测）："
        echo "  $SCRIPT_DIR/scripts/install.sh"
        echo ""
        echo "或使用一键安装脚本："
        echo "  $SCRIPT_DIR/scripts/install.sh"
        exit 1
    fi
}

# sha256 helpers (optional verification)
sha256_file() {
    local f="$1"
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$f" | awk '{print $1}'
        return 0
    fi
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$f" | awk '{print $1}'
        return 0
    fi
    return 1
}

expected_sha256_for_model() {
    local model_name="$1"
    local cfg="$SCRIPT_DIR/config.json"
    if [ -f "$cfg" ]; then
        node -e "
          const fs=require('fs');
          try{
            const j=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
            const v=(j.modelsSha256||{})[process.argv[2]]||'';
            process.stdout.write(String(v));
          }catch(e){process.stdout.write('');}
        " "$cfg" "$model_name"
    fi
}

verify_model_sha256_if_available() {
    local model_name="$1"
    local path="$2"
    local expected
    expected="$(expected_sha256_for_model "$model_name")"
    if [ -z "$expected" ]; then
        return 0
    fi
    local actual
    actual="$(sha256_file "$path" || true)"
    if [ -z "$actual" ]; then
        log_warn "无法计算 sha256（缺少 shasum/sha256sum），跳过校验"
        return 0
    fi
    if [ "$actual" != "$expected" ]; then
        log_error "模型 sha256 校验失败：$path"
        log_error "expected: $expected"
        log_error "actual:   $actual"
        return 1
    fi
    log_success "模型 sha256 校验通过：$model_name"
}

# 检查模型
check_model() {
    local model_name="$1"
    local model_file
    model_file=$(get_model_file "$model_name")
    
    # 优先级：技能目录 > 用户目录 > 下载
    local model_path="$MODEL_DIR_SKILL/$model_file"
    
    if [ ! -f "$model_path" ]; then
        model_path="$MODEL_DIR_USER/$model_file"
    fi
    
    if [ ! -f "$model_path" ]; then
        log_warn "模型不存在：$model_path"
        log_info "正在下载模型 $model_name ..."
        
        mkdir -p "$MODEL_DIR_SKILL"
        model_path="$MODEL_DIR_SKILL/$model_file"
        # Download URL (config.json has downloadBaseUrl; hardcode kept as reliable default)
        local download_url="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$model_file"
        
        if command -v wget &> /dev/null; then
            wget -c "$download_url" -O "$model_path"
        elif command -v curl &> /dev/null; then
            curl -L "$download_url" -o "$model_path"
        else
            log_error "需要 wget 或 curl 下载模型"
            exit 1
        fi
        
        log_success "模型下载完成：$model_path"
    fi

    # Optional integrity check
    verify_model_sha256_if_available "$model_name" "$model_path"

    echo "$model_path"
}

# 转换音频为 WAV（16kHz 单声道）
convert_to_wav() {
    local input="$1"
    local output="$2"
    
    log_info "转换音频格式：$(basename "$input") -> WAV"
    
    ffmpeg -i "$input" -ar 16000 -ac 1 -f wav -y "$output" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        log_error "音频转换失败：$input"
        return 1
    fi
}

# 转写音频
transcribe() {
    local audio_file="$1"
    local model_path="$2"
    local lang="$3"
    local output_format="$4"
    local output_file="$5"
    local no_timestamp="$6"
    local verbose="$7"

    log_info "开始转写：$(basename "$audio_file")"

    # whisper-cli 参数用数组拼，避免 eval（更安全，也更稳）
    local args=("-m" "$model_path" "-l" "$lang")

    # 输出格式
    case "$output_format" in
        "srt") args+=("-osrt") ;;
        "txt") args+=("-otxt") ;;
        "json") args+=("-oj") ;;
        "") : ;;
        *) log_error "未知输出格式：$output_format"; return 1 ;;
    esac

    # 无时间戳
    if [ "$no_timestamp" = "true" ]; then
        args+=("-nt")
    fi

    # 输出文件：如果用户没指定，则我们写到临时文件，最后 cat 出来
    local tmp_out=""
    if [ -n "$output_file" ]; then
        args+=("-of" "$output_file")
    else
        tmp_out="$TEMP_DIR/$(basename "$audio_file").out"
        args+=("-of" "$tmp_out")
    fi

    if [ "$verbose" = "true" ]; then
        whisper-cli "${args[@]}" "$audio_file"
    else
        whisper-cli "${args[@]}" "$audio_file" 2>/dev/null
    fi

    # 如果是文件输出（-of），优先回显文件内容（最可靠）
    local final_out="${output_file:-$tmp_out}"
    if [ -n "$final_out" ] && [ -f "$final_out" ]; then
        cat "$final_out"
        echo ""  # 结尾补个换行，避免粘连提示
    fi

    log_success "转写完成：$(basename "$audio_file")"
}

# 处理单个文件
process_file() {
    local input_file="$1"
    local model_name="$2"
    local lang="$3"
    local output_format="$4"
    local output_file="$5"
    local no_timestamp="$6"
    local verbose="$7"
    local clean="$8"
    
    # 检查文件存在
    if [ ! -f "$input_file" ]; then
        log_error "文件不存在：$input_file"
        return 1
    fi
    
    # 检查模型
    local model_path
    model_path=$(check_model "$model_name")
    
    # 创建临时目录
    mkdir -p "$TEMP_DIR"
    
    # 转换音频（如果不是 WAV）
    local process_file="$input_file"
    local is_temp=false
    
    if [[ ! "$input_file" =~ \.wav$ ]]; then
        local temp_wav="$TEMP_DIR/$(basename "$input_file").wav"
        convert_to_wav "$input_file" "$temp_wav"
        process_file="$temp_wav"
        is_temp=true
    fi
    
    # 转写
    transcribe "$process_file" "$model_path" "$lang" "$output_format" "$output_file" "$no_timestamp" "$verbose"
    
    # 清理临时文件
    if [ "$clean" = "true" ] && [ "$is_temp" = "true" ]; then
        rm -f "$process_file"
        log_info "已清理临时文件"
    fi
}

# 批量处理
batch_process() {
    local input_dir="$1"
    local model_name="$2"
    local lang="$3"
    local output_format="$4"
    local output_dir="$5"
    local no_timestamp="$6"
    local verbose="$7"
    local clean="$8"
    
    # 支持的音频格式
    local audio_extensions=("ogg" "wav" "mp3" "flac" "m4a" "aac" "wma" "opus")
    
    local count=0
    local success=0
    local failed=0
    
    log_info "批量处理目录：$input_dir"
    
    for ext in "${audio_extensions[@]}"; do
        while IFS= read -r -d '' file; do
            ((count++))
            
            local output_file=""
            if [ -n "$output_dir" ]; then
                mkdir -p "$output_dir"
                local base_name="$(basename "$file" ".$ext")"
                case "$output_format" in
                    "srt") output_file="$output_dir/$base_name.srt" ;;
                    "txt") output_file="$output_dir/$base_name.txt" ;;
                    "json") output_file="$output_dir/$base_name.json" ;;
                    *) output_file="" ;;
                esac
            fi
            
            if process_file "$file" "$model_name" "$lang" "$output_format" "$output_file" "$no_timestamp" "$verbose" "$clean"; then
                ((success++))
            else
                ((failed++))
            fi
            
        done < <(find "$input_dir" -maxdepth 1 -type f -name "*.$ext" -print0 2>/dev/null)
    done
    
    echo ""
    log_success "批量处理完成！"
    echo "  总计：$count"
    echo -e "  成功：${GREEN}$success${NC}"
    echo -e "  失败：${RED}$failed${NC}"
}

# 主函数
main() {
    # Create a per-run temp directory (avoid collisions; safer than fixed /tmp path)
    local run_tmp=""
    if command -v mktemp >/dev/null 2>&1; then
        run_tmp="$(mktemp -d "${TEMP_DIR%/}/whisper-transcribe.XXXXXX" 2>/dev/null || true)"
    fi
    if [ -z "$run_tmp" ]; then
        # fallback (best-effort)
        run_tmp="${TEMP_DIR%/}/whisper-transcribe.$$"
        mkdir -p "$run_tmp"
    fi
    TEMP_DIR="$run_tmp"
    trap 'rm -rf "$TEMP_DIR" >/dev/null 2>&1 || true' EXIT

    # 解析参数
    local model="$DEFAULT_MODEL"
    local lang="$DEFAULT_LANG"
    local output=""
    local batch=false
    local output_format=""
    local no_timestamp=false
    local verbose=false
    local clean=false
    
    # 位置参数
    local input=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -m|--model)
                model="$2"
                shift 2
                ;;
            -l|--lang)
                lang="$2"
                shift 2
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            -b|--batch)
                batch=true
                shift
                ;;
            -s|--srt)
                output_format="srt"
                shift
                ;;
            -t|--txt)
                output_format="txt"
                shift
                ;;
            -j|--json)
                output_format="json"
                shift
                ;;
            -n|--no-timestamp)
                no_timestamp=true
                shift
                ;;
            -c|--clean)
                clean=true
                shift
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_error "未知选项：$1"
                show_help
                exit 1
                ;;
            *)
                input="$1"
                shift
                ;;
        esac
    done
    
    # 检查输入
    if [ -z "$input" ]; then
        log_error "请指定音频文件或目录"
        show_help
        exit 1
    fi
    
    # 检查依赖
    check_dependencies
    
    # 处理
    if [ -d "$input" ] || [ "$batch" = "true" ]; then
        # 批量处理
        local output_dir=""
        if [ -n "$output" ]; then
            output_dir="$output"
        fi
        batch_process "$input" "$model" "$lang" "$output_format" "$output_dir" "$no_timestamp" "$verbose" "$clean"
    else
        # 单个文件
        process_file "$input" "$model" "$lang" "$output_format" "$output" "$no_timestamp" "$verbose" "$clean"
    fi
}

# 运行主函数
main "$@"
