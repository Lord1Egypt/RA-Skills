#!/bin/bash
# download-audio.sh - Plan B: 下载音频用于语音转录
# 用法：./download-audio.sh <视频 URL> [输出文件]

set -e

VIDEO_URL="$1"
OUTPUT_FILE="${2:-/tmp/audio.mp3}"

# 输入校验
if [[ -z "$VIDEO_URL" ]]; then
    echo "❌ 视频 URL 为空" >&2
    exit 1
fi

if [[ ${#VIDEO_URL} -gt 2048 ]]; then
    echo "❌ URL 过长" >&2
    exit 1
fi

# 排除 shell 元字符
if [[ "$VIDEO_URL" =~ [\;\|\&\(\)\{\}\`\$\<\>] ]]; then
    echo "❌ URL 包含非法字符" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 日志级别函数
log_info() { echo "ℹ️  $*"; }
log_warn() { echo "⚠️  $*"; }
log_error() { echo "❌ $*"; }
log_success() { echo "✅ $*"; }

log_info "下载音频 (Plan B)..."

# 检测平台
detect_platform() {
    if [[ "$VIDEO_URL" =~ (xiaohongshu\.com|xhslink\.com) ]]; then
        echo "xhs"
    elif [[ "$VIDEO_URL" =~ (douyin\.com|iesdouyin\.com|v\.douyin\.com) ]]; then
        echo "douyin"
    else
        echo "other"
    fi
}

PLATFORM=$(detect_platform)

# 抖音平台特殊处理：使用专用下载工具（优先）
if [[ "$PLATFORM" == "douyin" ]]; then
    DOUYIN_SCRIPT="$SCRIPT_DIR/douyin_downloader.py"
    
    if [[ -f "$DOUYIN_SCRIPT" ]]; then
        log_info "抖音平台：使用专用工具下载..."
        
        # 获取下载链接
        VIDEO_INFO=$(python3 "$DOUYIN_SCRIPT" --link "$VIDEO_URL" --action info 2>&1)
        DOWNLOAD_URL=$(echo "$VIDEO_INFO" | grep "下载链接" | sed 's/下载链接：//')
        
        if [[ -n "$DOWNLOAD_URL" ]]; then
            TEMP_VIDEO="/tmp/douyin_temp_$$.mp4"
            
            # 下载视频
            if curl -sL -o "$TEMP_VIDEO" "$DOWNLOAD_URL"; then
                log_success "视频下载成功，提取音频..."
                
                # 提取音频
                if ffmpeg -i "$TEMP_VIDEO" -vn -acodec libmp3lame -ab 128k "$OUTPUT_FILE" -y 2>/dev/null; then
                    rm -f "$TEMP_VIDEO"
                    log_success "音频下载完成"
                    exit 0  # 成功则直接退出，不执行 yt-dlp
                else
                    log_warn "音频提取失败，回退到 yt-dlp"
                fi
            else
                log_warn "视频下载失败，回退到 yt-dlp"
            fi
            rm -f "$TEMP_VIDEO" 2>/dev/null
        fi
    fi
fi

# 尝试 1: 根据平台选择最佳格式
log_info "尝试 1/3: 下载分离音轨..."
if [[ "$PLATFORM" == "xhs" || "$PLATFORM" == "douyin" ]]; then
    # 小红书/抖音：使用 best 格式（这些平台可能没有单独的音频流）
    if yt-dlp -f "best" -x --audio-format mp3 -o "$OUTPUT_FILE" "$VIDEO_URL" 2>&1 && \
        [[ -f "$OUTPUT_FILE" ]]; then
        log_success "音频下载完成"
        exit 0
    fi
else
    # 其他平台：优先音频流
    if yt-dlp -f "bestaudio" -x --audio-format mp3 -o "$OUTPUT_FILE" "$VIDEO_URL" 2>&1 && \
        [[ -f "$OUTPUT_FILE" ]]; then
        log_success "音频下载完成"
        exit 0
    fi
fi
rm -f "$OUTPUT_FILE" 2>/dev/null

# 尝试 2: 下载视频并提取音频（通用降级）
log_info "尝试 2/3: 下载视频提取音频..."
TEMP_VIDEO="/tmp/video_temp_$$"
if [[ "$PLATFORM" == "xhs" || "$PLATFORM" == "douyin" ]]; then
    # 小红书/抖音：不限制高度，使用最佳视频
    if yt-dlp -f "best" -o "$TEMP_VIDEO.mp4" "$VIDEO_URL" 2>&1 && \
        ffmpeg -i "$TEMP_VIDEO.mp4" -vn -acodec libmp3lame -ab 128k "$OUTPUT_FILE" -y 2>/dev/null; then
        rm -f "$TEMP_VIDEO.mp4"
        if [[ -f "$OUTPUT_FILE" ]]; then
            log_success "音频下载完成"
            exit 0
        fi
    fi
else
    # 其他平台：限制高度以加快下载
    if yt-dlp -f "best[height<=480]" -o "$TEMP_VIDEO.mp4" "$VIDEO_URL" 2>&1 && \
        ffmpeg -i "$TEMP_VIDEO.mp4" -vn -acodec libmp3lame -ab 128k "$OUTPUT_FILE" -y 2>/dev/null; then
        rm -f "$TEMP_VIDEO.mp4"
        if [[ -f "$OUTPUT_FILE" ]]; then
            log_success "音频下载完成"
            exit 0
        fi
    fi
fi
rm -f "$TEMP_VIDEO.mp4" 2>/dev/null

# 尝试 3: 强制下载（最后手段）
log_info "尝试 3/3: 强制下载..."
if yt-dlp --format-sort "res:desc" -o "$TEMP_VIDEO.mp4" "$VIDEO_URL" 2>&1; then
    if ffmpeg -i "$TEMP_VIDEO.mp4" -vn -acodec libmp3lame -ab 128k "$OUTPUT_FILE" -y 2>/dev/null; then
        rm -f "$TEMP_VIDEO.mp4"
        if [[ -f "$OUTPUT_FILE" ]]; then
            log_success "音频下载完成"
            exit 0
        fi
    fi
fi
rm -f "$TEMP_VIDEO.mp4" 2>/dev/null

log_error "音频下载失败（所有尝试均失败）"
exit 1
