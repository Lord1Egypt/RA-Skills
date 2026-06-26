#!/bin/bash
# video-summarize.sh - 视频总结生成完整流程 v1.0.13
# 更新日期：2026-05-06
# 用法：./video-summarize.sh <视频 URL> [输出目录] [cookies 文件] [选项]

set -e

# ============== 错误处理与日志 ==============

# 日志级别函数（ERROR_LOG 为空时不写入文件）
log_info() { echo "ℹ️  $*"; if [[ -n "$ERROR_LOG" ]]; then echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "$ERROR_LOG" 2>/dev/null; fi; }
log_warn() { echo "⚠️  $*"; if [[ -n "$ERROR_LOG" ]]; then echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "$ERROR_LOG" 2>/dev/null; fi; }
log_error() { echo "❌ $*"; if [[ -n "$ERROR_LOG" ]]; then echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "$ERROR_LOG" 2>/dev/null; fi; }
log_debug() { if [[ "$VERBOSE" == "true" ]]; then echo "🔍 $*"; if [[ -n "$ERROR_LOG" ]]; then echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "$ERROR_LOG" 2>/dev/null; fi; fi; }

# 错误捕获 trap
ERROR_LOG=""  # 在 OUTPUT_DIR 确定后设置
cleanup_on_error() {
    local exit_code=$?
    if [[ $exit_code -ne 0 && -n "$ERROR_LOG" && -f "$ERROR_LOG" ]]; then
        log_error "脚本执行失败 (退出码：$exit_code)"
        log_error "详细错误日志：$ERROR_LOG"
        [[ "$VERBOSE" == "true" ]] && tail -30 "$ERROR_LOG"
    fi
    exit $exit_code
}
trap cleanup_on_error ERR

# 平台标识映射（统一小写）
# bilibili, xhs, douyin, youtube

# 解析参数
VIDEO_URL=""
OUTPUT_DIR=""
USER_SPECIFIED_OUTPUT="false"  # 标记用户是否手动指定了输出目录
BILI_COOKIES_FILE="$HOME/.cookies/bilibili_cookies.txt"
DOUYIN_COOKIES_FILE="$HOME/.cookies/douyin_cookies.txt"
COOKIES_FILE=""  # 将根据平台自动选择
VERBOSE="false"
KEEP_VIDEO="false"
AUTO_PUSH="false"
RESUME="false"

for arg in "$@"; do
    case $arg in
        --verbose|-v)
            VERBOSE="true"
            ;;
        --keep-video)
            KEEP_VIDEO="true"
            ;;
        --push|--auto-push)
            AUTO_PUSH="true"
            ;;
        --resume)
            RESUME="true"
            ;;
        *)
            if [[ -z "$VIDEO_URL" ]]; then
                VIDEO_URL="$arg"
            elif [[ "$USER_SPECIFIED_OUTPUT" == "false" ]]; then
                OUTPUT_DIR="$arg"
                USER_SPECIFIED_OUTPUT="true"
            elif [[ "$COOKIES_FILE" == "$HOME/.cookies/bilibili_cookies.txt" ]]; then
                COOKIES_FILE="$arg"
            fi
            ;;
    esac
done

if [[ -z "$VIDEO_URL" ]]; then
    echo "用法：./video-summarize.sh <视频 URL> [输出目录] [cookies 文件] [选项]"
    echo ""
    echo "选项:"
    echo "  --verbose, -v      显示详细日志（包括错误信息）"
    echo "  --keep-video       保留视频/音频文件（默认清理）"
    echo "  --push, --auto-push  完成后自动推送到 Notion"
    echo "  --resume           从中断点恢复（检测进度文件）"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============== 输入安全校验 ==============

# URL 安全校验（阻断注入攻击）
validate_url() {
    local url="$1"
    
    # 最大长度 2048 字符
    if [[ ${#url} -gt 2048 ]]; then
        log_error "URL 过长 (>2048 字符)"
        exit 1
    fi
    
    # 字符黑名单：排除 shell 元字符
    if [[ "$url" =~ [\;\|\&\(\)\{\}\`\$\<\>] ]]; then
        log_error "URL 包含非法字符"
        exit 1
    fi
    
    # 协议白名单
    if [[ ! "$url" =~ ^https?:// ]]; then
        log_error "仅支持 http/https 协议"
        exit 1
    fi
    
    # 平台白名单
    if [[ "$url" =~ ^(https?://)([a-zA-Z0-9.-]*\.)?(bilibili\.com|b23\.tv|xiaohongshu\.com|xhslink\.com|douyin\.com|iesdouyin\.com|v\.douyin\.com|youtube\.com|youtu\.be)/ ]]; then
        return 0
    fi
    
    log_error "不支持的平台"
    exit 1
}

# 输出目录安全校验（阻止路径遍历）
validate_output_dir() {
    local dir="$1"
    
    # 禁止路径遍历
    if [[ "$dir" =~ \.\. ]]; then
        log_error "输出目录包含路径遍历字符 '..'"
        exit 1
    fi
    
    # 确保绝对路径
    if [[ "$dir" != /* ]]; then
        dir="$(pwd)/$dir"
    fi
    
    # 禁止写入系统敏感路径
    case "$dir" in
        /etc/*|/usr/*|/bin/*|/sbin/*|/root/*|/boot/*|/proc/*|/sys/*)
            log_error "禁止写入系统目录"
            exit 1
            ;;
    esac
    
    OUTPUT_DIR="$dir"
}

# ============== 平台识别与输出目录生成 ==============

# 提取平台标识
extract_platform() {
    local url="$1"
    
    # B 站：bilibili.com 或 b23.tv
    if [[ "$url" =~ (bilibili\.com|b23\.tv) ]]; then
        echo "bilibili"
        return
    fi
    
    # 小红书：xiaohongshu.com 或 xhslink.com
    if [[ "$url" =~ (xiaohongshu\.com|xhslink\.com) ]]; then
        echo "xhs"
        return
    fi
    
    # 抖音：douyin.com、iesdouyin.com 或 v.douyin.com（短链）
    if [[ "$url" =~ (douyin\.com|iesdouyin\.com|v\.douyin\.com) ]]; then
        echo "douyin"
        return
    fi
    
    # YouTube：youtube.com 或 youtu.be
    if [[ "$url" =~ (youtube\.com|youtu\.be) ]]; then
        echo "youtube"
        return
    fi
    
    # 未知平台
    echo "unknown"
}

# 提取视频 ID
extract_video_id() {
    local url="$1"
    local platform="$2"
    
    case "$platform" in
        bilibili)
            # 提取 BV 号或 av 号
            if [[ "$url" =~ (BV[a-zA-Z0-9]+) ]]; then
                echo "${BASH_REMATCH[1]}"
            elif [[ "$url" =~ av([0-9]+) ]]; then
                echo "av${BASH_REMATCH[1]}"
            else
                # 短链：使用路径作为 ID
                local path=$(echo "$url" | sed -E 's|https?://[^/]+/||' | cut -d'?' -f1)
                echo "${path:-b23_shortlink}"
            fi
            ;;
        xhs)
            # 小红书笔记 ID（数字或带字母）
            if [[ "$url" =~ /([a-zA-Z0-9]{10,})(\?|$|\&|/) ]]; then
                echo "${BASH_REMATCH[1]}"
            else
                # 短链：使用路径作为 ID
                local path=$(echo "$url" | sed -E 's|https?://[^/]+/||' | cut -d'?' -f1)
                echo "${path:-xhs_shortlink}"
            fi
            ;;
        douyin)
            # 抖音：提取视频 ID（支持多种格式）
            # 格式 1: /video/1234567890
            if [[ "$url" =~ /video/([0-9]+) ]]; then
                echo "${BASH_REMATCH[1]}"
            # 格式 2: ?modal_id=1234567890 (课程/精选视频)
            elif [[ "$url" =~ modal_id=([0-9]+) ]]; then
                echo "${BASH_REMATCH[1]}"
            # 格式 3: 短链或其他
            elif [[ "$url" =~ /([a-zA-Z0-9_-]{10,})(\?|$) ]]; then
                echo "${BASH_REMATCH[1]}"
            else
                # 短链：使用路径作为 ID
                local path=$(echo "$url" | sed -E 's|https?://[^/]+/||' | cut -d'?' -f1)
                echo "${path:-douyin_shortlink}"
            fi
            ;;
        youtube)
            # YouTube 视频 ID
            if [[ "$url" =~ v=([a-zA-Z0-9_-]+) ]]; then
                echo "${BASH_REMATCH[1]}"
            elif [[ "$url" =~ youtu\.be/([a-zA-Z0-9_-]+) ]]; then
                echo "${BASH_REMATCH[1]}"
            else
                echo "unknown"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# URL 安全校验
validate_url "$VIDEO_URL"

# 生成输出目录
PLATFORM=$(extract_platform "$VIDEO_URL")
VIDEO_ID=$(extract_video_id "$VIDEO_URL" "$PLATFORM")

if [[ "$USER_SPECIFIED_OUTPUT" == "true" ]]; then
    validate_output_dir "$OUTPUT_DIR"
else
    OUTPUT_DIR="/tmp/video-summarizer/$PLATFORM/$VIDEO_ID"
fi

mkdir -p "$OUTPUT_DIR"

# 安全校验：.env 文件权限
ENV_FILE_CHECK="$HOME/.openclaw/.env"
if [[ -f "$ENV_FILE_CHECK" ]]; then
    ENV_PERMS=$(stat -c '%a' "$ENV_FILE_CHECK" 2>/dev/null)
    if [[ "$ENV_PERMS" != "600" && "$ENV_PERMS" != "400" ]]; then
        log_warn ".env 文件权限不安全 (当前: $ENV_PERMS)，已修复为 600"
        chmod 600 "$ENV_FILE_CHECK"
    fi
fi

# 安全校验：Cookie 文件权限
if [[ -n "$COOKIES_FILE" && -f "$COOKIES_FILE" ]]; then
    COOKIE_PERMS=$(stat -c '%a' "$COOKIES_FILE" 2>/dev/null)
    if [[ "$COOKIE_PERMS" != "600" && "$COOKIE_PERMS" != "400" ]]; then
        log_warn "Cookie 文件权限不安全 (当前: $COOKIE_PERMS)，建议 600"
    fi
fi

# 初始化错误日志文件（OUTPUT_DIR 已确定）
ERROR_LOG="$OUTPUT_DIR/error.log"
echo "" > "$ERROR_LOG"  # 清空旧日志

# 根据平台选择 Cookies（抖音不使用 cookies，使用专用下载器）
if [[ "$PLATFORM" == "douyin" ]]; then
    COOKIES_FILE=""  # 抖音不使用 cookies
else
    COOKIES_FILE="$BILI_COOKIES_FILE"
fi

# 进度文件
PROGRESS_FILE="$OUTPUT_DIR/.progress.json"

echo "📁 输出目录：$OUTPUT_DIR"
echo "🏷️  平台：$PLATFORM | 视频 ID: $VIDEO_ID"
if [[ -n "$COOKIES_FILE" && -f "$COOKIES_FILE" ]]; then
    echo "🍪 Cookies: $COOKIES_FILE"
else
    echo "🍪 Cookies: 无"
fi

# 检查环境变量（自动推送）
if [[ "$AUTO_PUSH" == "true" ]]; then
    if [[ -z "$NOTION_VIDEO_SUMMARY_DATABASE_ID" ]]; then
        NOTION_VIDEO_SUMMARY_DATABASE_ID=$(grep "^NOTION_VIDEO_SUMMARY_DATABASE_ID=" "$HOME/.openclaw/.env" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    fi
fi

[[ "$VERBOSE" == "true" ]] && echo "🔍 详细模式 | "
[[ "$KEEP_VIDEO" == "true" ]] && echo "💾 保留视频 | "
[[ "$AUTO_PUSH" == "true" ]] && echo "📤 自动推送 | "
[[ "$RESUME" == "true" ]] && echo "♻️  恢复模式"
echo ""

# 进度保存函数（环境变量传递，无 shell 注入）
save_progress() {
    local step=$1
    local status=$2
    local timestamp
    timestamp=$(date -Iseconds)
    PROGRESS_STEP="$step" \
    PROGRESS_STATUS="$status" \
    PROGRESS_TIMESTAMP="$timestamp" \
    VIDEO_URL="$VIDEO_URL" \
    OUTPUT_DIR="$OUTPUT_DIR" \
    PROGRESS_FILE="$PROGRESS_FILE" \
    python3 -c "
import os, json
data = {
    'video_url': os.environ['VIDEO_URL'],
    'current_step': os.environ['PROGRESS_STEP'],
    'status': os.environ['PROGRESS_STATUS'],
    'timestamp': os.environ['PROGRESS_TIMESTAMP'],
    'output_dir': os.environ['OUTPUT_DIR']
}
with open(os.environ['PROGRESS_FILE'], 'w') as f:
    json.dump(data, f, indent=2)
"
}

# 检查进度（恢复模式，环境变量传递）
check_progress() {
    if [[ "$RESUME" == "true" && -f "$PROGRESS_FILE" ]]; then
        local last_step
        last_step=$(PROGRESS_FILE="$PROGRESS_FILE" python3 -c "
import os, json
with open(os.environ['PROGRESS_FILE']) as f:
    print(json.load(f).get('current_step', ''))
" 2>/dev/null)
        if [[ -n "$last_step" ]]; then
            echo "♻️  检测到上次运行到：Step $last_step"
            echo "   将跳过已完成的步骤..."
            return 0
        fi
    fi
    return 1
}

echo "🎬 Video Summarizer v1.0.13"
echo ""

# Step 1: 元数据
if check_progress && [[ -f "$OUTPUT_DIR/metadata.json" && -s "$OUTPUT_DIR/metadata.json" ]]; then
    echo "⏭️  Step 1 跳过"
else
    echo "📥 Step 1: 元数据..."
    save_progress "1" "running"
    
    # 抖音平台特殊处理：使用专用工具获取元数据
    if [[ "$PLATFORM" == "douyin" ]]; then
        DOUYIN_SCRIPT="$SCRIPT_DIR/douyin_downloader.py"
        
        if [[ -f "$DOUYIN_SCRIPT" ]]; then
            log_info "抖音平台：使用专用工具获取元数据..."
            
            # 获取视频信息（JSON 格式，便于解析）
            VIDEO_JSON=$(python3 "$DOUYIN_SCRIPT" --link "$VIDEO_URL" --action info --json 2>/dev/null)
            
            # 使用 stdin 管道传递 JSON，环境变量传递路径（无 shell 注入）
            echo "$VIDEO_JSON" | VIDEO_URL="$VIDEO_URL" OUTPUT_DIR="$OUTPUT_DIR" python3 -c "
import sys, json, os

try:
    data = json.loads(sys.stdin.read())
    
    metadata = {
        'title': str(data.get('title', '')).replace('\\n', ' ').replace('\\r', '').strip(),
        'uploader': str(data.get('author', '')),
        'uploader_id': str(data.get('video_id', '')),
        'duration': 0,
        'duration_string': str(data.get('duration_string', '')),
        'thumbnail': str(data.get('cover', '')),
        'webpage_url': os.environ['VIDEO_URL'],
        'platform': 'douyin',
        'download_url': str(data.get('url', '')),
        'upload_date': str(data.get('upload_date', ''))
    }
    
    with open(os.path.join(os.environ['OUTPUT_DIR'], 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f\"✅ 元数据完成 | 标题：{metadata['title']} | 视频 ID: {metadata['uploader_id']}\")
except Exception as e:
    print(f'❌ 元数据解析失败：{e}', file=sys.stderr)
    sys.exit(1)
"
        else
            log_warn "抖音下载脚本不存在，使用 yt-dlp"
            if [[ -f "$COOKIES_FILE" ]]; then
                yt-dlp --cookies "$COOKIES_FILE" --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json" 2>/dev/null || echo '{}' > "$OUTPUT_DIR/metadata.json"
            else
                yt-dlp --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json" 2>/dev/null || echo '{}' > "$OUTPUT_DIR/metadata.json"
            fi
        fi
    else
        # 非抖音平台：使用 yt-dlp
        if [[ -f "$COOKIES_FILE" ]]; then
            if [[ "$VERBOSE" == "true" ]]; then
                yt-dlp --cookies "$COOKIES_FILE" --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json"
            else
                yt-dlp --cookies "$COOKIES_FILE" --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json" 2>/dev/null
            fi
        else
            if [[ "$VERBOSE" == "true" ]]; then
                yt-dlp --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json"
            else
                yt-dlp --dump-json "$VIDEO_URL" > "$OUTPUT_DIR/metadata.json" 2>/dev/null
            fi
        fi
        
        # 为小红书提取 upload_date（从笔记 ID 解析，环境变量传递路径）
        if [[ "$PLATFORM" == "xhs" ]]; then
            OUTPUT_DIR="$OUTPUT_DIR" python3 -c "
import json, os
from datetime import datetime

output_dir = os.environ['OUTPUT_DIR']
with open(os.path.join(output_dir, 'metadata.json'), 'r') as f:
    meta = json.load(f)

note_id = meta.get('id', '') or meta.get('display_id', '') or meta.get('webpage_url', '').split('/')[-1].split('?')[0]
if len(note_id) >= 8:
    try:
        ts = int(note_id[:8], 16)
        upload_date = datetime.fromtimestamp(ts).strftime('%Y%m%d')
        meta['upload_date'] = upload_date
    except:
        meta['upload_date'] = ''
else:
    meta['upload_date'] = meta.get('upload_date', '')

with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)
"
        fi
    fi
    
    TITLE=$(python3 -c "import json; print(json.load(open('$OUTPUT_DIR/metadata.json')).get('title', 'Unknown'))" 2>/dev/null || echo "Unknown")
    UPLOADER=$(python3 -c "import json; print(json.load(open('$OUTPUT_DIR/metadata.json')).get('uploader', 'Unknown'))" 2>/dev/null || echo "Unknown")
    DURATION=$(python3 -c "import json; print(json.load(open('$OUTPUT_DIR/metadata.json')).get('duration_string', 'Unknown'))" 2>/dev/null || echo "Unknown")
    DURATION_SEC=$(python3 -c "import json; print(int(json.load(open('$OUTPUT_DIR/metadata.json')).get('duration', 0)))" 2>/dev/null || echo "0")
    THUMBNAIL=$(python3 -c "import json; print(json.load(open('$OUTPUT_DIR/metadata.json')).get('thumbnail', ''))" 2>/dev/null || echo "")
    
    echo "✅ 元数据完成 | 标题：$TITLE | UP 主：$UPLOADER | 时长：$DURATION"
    [[ "$VERBOSE" == "true" ]] && echo "   📄 $OUTPUT_DIR/metadata.json"
    save_progress "1" "done"
fi

# Step 2 & 3: 并行执行 - 视频下载 + 字幕处理
# 两者互不依赖，可以并行执行以节省时间

# 检查是否可以跳过
if check_progress && [[ -f "$OUTPUT_DIR/video.mp4" && -n "$(find "$OUTPUT_DIR" -name "*.vtt" -o -name "audio.txt" 2>/dev/null | head -1)" ]]; then
    echo "⏭️  Step 2-3 跳过"
    VIDEO_FILE="$OUTPUT_DIR/video.mp4"
    SUBTITLE_FILE=$(find "$OUTPUT_DIR" -name "*.vtt" -o -name "audio.txt" 2>/dev/null | head -1)
    SUBTITLE_SOURCE="已存在"
else
    echo "🚀 Step 2-3: 并行执行 - 视频下载 + 字幕处理..."
    save_progress "2" "running"
    
    # 初始化变量
    SUBTITLE_FILE=""
    SUBTITLE_SOURCE=""
    SUBTITLE_LOG="$OUTPUT_DIR/subtitle_download.log"
    VIDEO_FILE="$OUTPUT_DIR/video.mp4"
    VIDEO_LOG="$OUTPUT_DIR/video_download.log"
    
    # ========== 任务 A: 视频下载（后台）==========
    (
        # 子进程中重新定义日志函数
        log_info() { echo "ℹ️  $*"; }
        log_warn() { echo "⚠️  $*"; }
        log_error() { echo "❌ $*"; }
        log_success() { echo "✅ $*"; }
        
        log_info "[视频任务] 开始下载视频..."
        DOWNLOAD_SUCCESS=false
        
        # 抖音平台特殊处理
        if [[ "$PLATFORM" == "douyin" ]]; then
            log_info "[视频任务] 抖音平台：使用专用下载工具..."
            DOUYIN_SCRIPT="$SCRIPT_DIR/douyin_downloader.py"
            
            if [[ -f "$DOUYIN_SCRIPT" ]]; then
                python3 "$DOUYIN_SCRIPT" --link "$VIDEO_URL" --action info > "$VIDEO_LOG" 2>&1
                DOWNLOAD_URL=$(grep "下载链接" "$VIDEO_LOG" | sed 's/下载链接：//')
                
                if [[ -n "$DOWNLOAD_URL" ]]; then
                    log_info "[视频任务] 下载链接已获取"
                    log_info "[视频任务] 开始 curl 下载..." >> "$VIDEO_LOG"
                    curl -L -o "$VIDEO_FILE" "$DOWNLOAD_URL" 2>&1 | tee -a "$VIDEO_LOG"
                    CURL_EXIT=$?
                    log_info "[视频任务] curl 退出码：$CURL_EXIT" >> "$VIDEO_LOG"
                    log_info "[视频任务] 检查文件：$VIDEO_FILE" >> "$VIDEO_LOG"
                    ls -lh "$VIDEO_FILE" >> "$VIDEO_LOG" 2>&1
                    # 检查文件是否存在且大小 > 0
                    if [[ -f "$VIDEO_FILE" && -s "$VIDEO_FILE" ]]; then
                        log_info "[视频任务] 文件检查通过，设置 DOWNLOAD_SUCCESS=true" >> "$VIDEO_LOG"
                        DOWNLOAD_SUCCESS=true
                        FILE_SIZE=$(ls -lh "$VIDEO_FILE" 2>/dev/null | awk '{print $5}')
                        log_success "[视频任务] 抖音视频下载成功 | $FILE_SIZE" >> "$VIDEO_LOG"
                    else
                        log_warn "[视频任务] 文件检查失败" >> "$VIDEO_LOG"
                    fi
                    log_info "[视频任务] DOWNLOAD_SUCCESS=$DOWNLOAD_SUCCESS" >> "$VIDEO_LOG"
                fi
            else
                log_warn "[视频任务] 抖音下载脚本不存在，回退到 yt-dlp"
            fi
        fi
        
        # 非抖音平台或抖音下载失败
        if [[ "$DOWNLOAD_SUCCESS" != "true" ]]; then
            for i in 1 2 3; do
                log_info "[视频任务] 尝试 $i/3..."
                if [[ -n "$COOKIES_FILE" && -f "$COOKIES_FILE" ]]; then
                    if [[ "$VERBOSE" == "true" ]]; then
                        yt-dlp --cookies "$COOKIES_FILE" -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
                               --merge-output-format mp4 \
                               -o "$VIDEO_FILE" "$VIDEO_URL" 2>&1 | tee -a "$VIDEO_LOG" && { DOWNLOAD_SUCCESS=true; break; } || {
                            rm -f "$VIDEO_FILE"* 2>/dev/null
                        }
                    else
                        yt-dlp --cookies "$COOKIES_FILE" -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
                               --merge-output-format mp4 \
                               -o "$VIDEO_FILE" "$VIDEO_URL" 2>/dev/null && { DOWNLOAD_SUCCESS=true; break; } || {
                            rm -f "$VIDEO_FILE"* 2>/dev/null
                        }
                    fi
                else
                    if [[ "$VERBOSE" == "true" ]]; then
                        yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
                               --merge-output-format mp4 \
                               -o "$VIDEO_FILE" "$VIDEO_URL" 2>&1 | tee -a "$VIDEO_LOG" && { DOWNLOAD_SUCCESS=true; break; } || {
                            rm -f "$VIDEO_FILE"* 2>/dev/null
                        }
                    else
                        yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
                               --merge-output-format mp4 \
                               -o "$VIDEO_FILE" "$VIDEO_URL" 2>/dev/null && { DOWNLOAD_SUCCESS=true; break; } || {
                            rm -f "$VIDEO_FILE"* 2>/dev/null
                        }
                    fi
                fi
            done
            
            if [[ "$DOWNLOAD_SUCCESS" != "true" ]]; then
                log_warn "[视频任务] 降级尝试..."
                if [[ -n "$COOKIES_FILE" && -f "$COOKIES_FILE" ]]; then
                    if [[ "$VERBOSE" == "true" ]]; then
                        yt-dlp --cookies "$COOKIES_FILE" -f "best" --merge-output-format mp4 -o "$VIDEO_FILE" "$VIDEO_URL" 2>&1 | tee -a "$VIDEO_LOG" || {
                            log_error "[视频任务] 视频下载失败"
                            exit 1
                        }
                    else
                        yt-dlp --cookies "$COOKIES_FILE" -f "best" --merge-output-format mp4 -o "$VIDEO_FILE" "$VIDEO_URL" 2>/dev/null || {
                            log_error "[视频任务] 视频下载失败"
                            exit 1
                        }
                    fi
                else
                    if [[ "$VERBOSE" == "true" ]]; then
                        yt-dlp -f "best" --merge-output-format mp4 -o "$VIDEO_FILE" "$VIDEO_URL" 2>&1 | tee -a "$VIDEO_LOG" || {
                            log_error "[视频任务] 视频下载失败"
                            exit 1
                        }
                    else
                        yt-dlp -f "best" --merge-output-format mp4 -o "$VIDEO_FILE" "$VIDEO_URL" 2>/dev/null || {
                            log_error "[视频任务] 视频下载失败"
                            exit 1
                        }
                    fi
                fi
            fi
        fi
        
        log_success "[视频任务] 视频下载完成 | $(ls -lh "$VIDEO_FILE" 2>/dev/null | awk '{print $5}')"
        echo "VIDEO_DONE" > "$OUTPUT_DIR/.video_done"
    ) &
    VIDEO_PID=$!
    
    # ========== 任务 B: 字幕处理（后台）==========
    (
        # 子进程中重新定义日志函数
        log_info() { echo "ℹ️  $*"; }
        log_warn() { echo "⚠️  $*"; }
        log_error() { echo "❌ $*"; }
        log_success() { echo "✅ $*"; }
        
        log_info "[字幕任务] 开始处理字幕..."
        
        # 尝试 1: Cookies + 官方字幕
        if [[ -f "$COOKIES_FILE" ]]; then
            log_info "[字幕任务] 尝试使用 Cookies 下载官方字幕..."
            if [[ "$VERBOSE" == "true" ]]; then
                yt-dlp --cookies "$COOKIES_FILE" \
                       --write-sub --write-auto-sub \
                       --sub-lang "ai-zh,zh-Hans,zh,en" \
                       --skip-download \
                       --convert-subs vtt \
                       -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>&1 | tee -a "$SUBTITLE_LOG" || true
            else
                yt-dlp --cookies "$COOKIES_FILE" \
                       --write-sub --write-auto-sub \
                       --sub-lang "ai-zh,zh-Hans,zh,en" \
                       --skip-download \
                       --convert-subs vtt \
                       -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>/dev/null || true
            fi
            
            SUBTITLE_FILE=$(find "$OUTPUT_DIR" -name "*.vtt" 2>/dev/null | head -1)
            [[ -n "$SUBTITLE_FILE" && -s "$SUBTITLE_FILE" ]] && SUBTITLE_SOURCE="官方字幕"
        fi
        
        # 尝试 2: 自动字幕
        if [[ -z "$SUBTITLE_FILE" ]]; then
            log_info "[字幕任务] 尝试下载自动字幕..."
            if [[ -n "$COOKIES_FILE" && -f "$COOKIES_FILE" ]]; then
                if [[ "$VERBOSE" == "true" ]]; then
                    yt-dlp --cookies "$COOKIES_FILE" --write-auto-sub \
                           --sub-lang "zh-Hans,zh,en" \
                           --skip-download \
                           --convert-subs vtt \
                           -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>&1 | tee -a "$SUBTITLE_LOG" || true
                else
                    yt-dlp --cookies "$COOKIES_FILE" --write-auto-sub \
                           --sub-lang "zh-Hans,zh,en" \
                           --skip-download \
                           --convert-subs vtt \
                           -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>/dev/null || true
                fi
            else
                if [[ "$VERBOSE" == "true" ]]; then
                    yt-dlp --write-auto-sub \
                           --sub-lang "zh-Hans,zh,en" \
                           --skip-download \
                           --convert-subs vtt \
                           -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>&1 | tee -a "$SUBTITLE_LOG" || true
                else
                    yt-dlp --write-auto-sub \
                           --sub-lang "zh-Hans,zh,en" \
                           --skip-download \
                           --convert-subs vtt \
                           -o "$OUTPUT_DIR/video" "$VIDEO_URL" 2>/dev/null || true
                fi
            fi
            
            SUBTITLE_FILE=$(find "$OUTPUT_DIR" -name "*.vtt" 2>/dev/null | head -1)
            [[ -n "$SUBTITLE_FILE" && -s "$SUBTITLE_FILE" ]] && SUBTITLE_SOURCE="自动字幕"
        fi
        
        # Plan B: 语音转录
        if [[ -z "$SUBTITLE_FILE" ]]; then
            log_warn "[字幕任务] 未找到可用字幕，启动 Plan B 语音转录..."
            
            AUDIO_FILE="$OUTPUT_DIR/audio.mp3"
            SUBTITLE_FILE="$OUTPUT_DIR/audio.txt"
            
            # 下载音频
            "$SCRIPT_DIR/download-audio.sh" "$VIDEO_URL" "$AUDIO_FILE"
            
            # 语音转录
            python3 "$SCRIPT_DIR/transcribe-audio.py" "$AUDIO_FILE" "$SUBTITLE_FILE"
            
            SUBTITLE_SOURCE="语音转录 (Plan B)"
            log_success "[字幕任务] 语音转录完成"
        fi
        
        log_success "[字幕任务] 字幕处理完成 | 来源：$SUBTITLE_SOURCE"
        echo "SUBTITLE_DONE" > "$OUTPUT_DIR/.subtitle_done"
    ) &
    SUBTITLE_PID=$!
    
    # ========== 等待两个任务完成 ==========
    echo "⏳ 等待视频下载和字幕处理完成..."
    wait $VIDEO_PID
    VIDEO_EXIT=$?
    wait $SUBTITLE_PID
    SUBTITLE_EXIT=$?
    
    # 检查任务结果
    if [[ $VIDEO_EXIT -ne 0 ]]; then
        log_error "视频下载任务失败"
        exit 1
    fi
    
    # 检查视频文件是否真的存在（修复：yt-dlp 可能报错但仍返回 0）
    if [[ ! -f "$VIDEO_FILE" ]]; then
        log_warn "视频文件不存在，检查是否仅有音频"
        # 如果有音频文件，继续使用（截图将使用封面图代替）
        if [[ -f "$OUTPUT_DIR/audio.mp3" ]]; then
            log_info "检测到音频文件，继续处理（截图将使用封面图）"
        else
            log_error "视频和音频文件都不存在，无法继续"
            exit 1
        fi
    fi
    
    if [[ $SUBTITLE_EXIT -ne 0 ]]; then
        log_error "字幕处理任务失败"
        exit 1
    fi
    
    # 重新查找字幕文件（可能在子进程中生成）
    SUBTITLE_FILE=$(find "$OUTPUT_DIR" -name "*.vtt" -o -name "audio.txt" 2>/dev/null | head -1)
    
    echo "✅ 视频下载完成 | $(ls -lh "$VIDEO_FILE" 2>/dev/null | awk '{print $5}')"
    echo "✅ 字幕处理完成 | 来源：${SUBTITLE_SOURCE:-未知}"
    save_progress "2" "done"
fi

# Step 3: 文本提取（原 Step 3，现在是 Step 3）
if check_progress && [[ -f "$OUTPUT_DIR/transcript.txt" ]]; then
    echo "⏭️  Step 3 跳过"
    WORD_COUNT=$(wc -w < "$OUTPUT_DIR/transcript.txt")
else
    echo "📝 Step 3: 文本提取..."
    save_progress "3" "running"
    
    # 重新查找字幕文件（可能在并行任务中生成）
    if [[ -z "$SUBTITLE_FILE" ]]; then
        SUBTITLE_FILE=$(find "$OUTPUT_DIR" -name "*.vtt" -o -name "audio.txt" 2>/dev/null | head -1)
    fi
    
    # 检查是否有 VTT 字幕文件
    if [[ "$SUBTITLE_FILE" =~ \.vtt$ ]]; then
        # VTT 格式：提取纯文本
        awk '/^WEBVTT/{next} /^[0-9]/{next} /^$/{next} /-->/ {next} {print}' "$SUBTITLE_FILE" | \
            sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v "^$" > "$OUTPUT_DIR/transcript.txt"
    else
        # 纯文本格式（硅基流动等 API 返回）
        cp "$SUBTITLE_FILE" "$OUTPUT_DIR/transcript.txt"
    fi
    
    WORD_COUNT=$(wc -w < "$OUTPUT_DIR/transcript.txt")
    LINE_COUNT=$(wc -l < "$OUTPUT_DIR/transcript.txt")
    
    if [[ $WORD_COUNT -eq 0 ]]; then
        echo "   ❌ 字幕文本为空"
        exit 1
    fi
    
    echo "✅ 文本提取完成 | $LINE_COUNT 行 | $WORD_COUNT 字"
    save_progress "3" "done"
fi

# Step 4: AI 分析
if check_progress && [[ -f "$OUTPUT_DIR/ai_result.json" ]]; then
    echo "⏭️  Step 4 跳过（AI 结果已存在）"
else
    echo "🤖 Step 4: AI 分析（生成 JSON）..."
    save_progress "4" "running"
    
    AI_SCRIPT="$SCRIPT_DIR/analyze-subtitles-ai.py"
    AI_JSON_FILE="$OUTPUT_DIR/ai_result.json"
    AI_LOG="$OUTPUT_DIR/ai_analysis.log"
    TEMP_SUMMARY="$OUTPUT_DIR/summary_temp.md"
    
    if [[ -f "$AI_SCRIPT" ]]; then
        if [[ "$VERBOSE" == "true" ]]; then
            python3 "$AI_SCRIPT" "$SUBTITLE_FILE" "$OUTPUT_DIR/metadata.json" "$TEMP_SUMMARY" 2>&1 | tee -a "$AI_LOG"
        else
            python3 "$AI_SCRIPT" "$SUBTITLE_FILE" "$OUTPUT_DIR/metadata.json" "$TEMP_SUMMARY" 2>/dev/null
        fi
        
        if [[ -f "$AI_JSON_FILE" ]]; then
            echo "✅ AI 分析完成 | JSON: $AI_JSON_FILE"
            AI_SUCCESS="true"
        else
            log_warn "AI 分析失败，使用基础版总结（无 AI 分析）"
            [[ "$VERBOSE" == "true" ]] && cat "$AI_LOG" | tail -10
            AI_SUCCESS="false"
            # 创建空的 AI 结果文件，供后续步骤使用
            cat > "$AI_JSON_FILE" << 'AIJSON'
{
  "note": "AI 分析失败，无法生成概述。",
  "key_points": [],
  "concepts": [],
  "warnings": [],
  "summary": "AI 分析失败，无法生成总结。"
}
AIJSON
        fi
    else
        log_warn "AI 脚本不存在，使用基础版总结"
        AI_SUCCESS="false"
    fi
    save_progress "4" "done"
fi

# Step 5: 截图（基于 AI 分析的时间戳）
if check_progress && [[ -d "$OUTPUT_DIR/screenshots" && -n "$(ls -A "$OUTPUT_DIR/screenshots" 2>/dev/null)" ]]; then
    echo "⏭️  Step 5 跳过"
else
    echo "🎬 Step 5: 截图（基于 AI 分析结果）..."
    save_progress "5" "running"
    
    mkdir -p "$OUTPUT_DIR/screenshots"
    
    # 从 AI 分析结果中提取时间戳（核心要点 + 注意事项，支持最多 30 张）
    SCREENSHOT_TIMES=()
    AI_JSON="$OUTPUT_DIR/ai_result.json"
    MAX_SCREENSHOTS=30
    
    if [[ -f "$AI_JSON" ]]; then
        echo "   📊 从 AI 分析结果提取时间戳..."
        # DURATION_SEC 数字校验
        if [[ ! "$DURATION_SEC" =~ ^[0-9]+$ ]]; then
            log_warn "DURATION_SEC 异常，设为默认值 600"
            DURATION_SEC=600
        fi
        # 使用环境变量传递路径和数值（无 shell 注入）
        SCREENSHOT_TIMES=($(AI_JSON="$AI_JSON" DURATION_SEC="$DURATION_SEC" MAX_SCREENSHOTS="$MAX_SCREENSHOTS" python3 -c "
import json, os, sys

try:
    with open(os.environ['AI_JSON'], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    times = []
    for point in data.get('key_points', []):
        time_str = point.get('time', '')
        if time_str:
            times.append(time_str)
    
    for warning in data.get('warnings', []):
        time_str = warning.get('time', '')
        if time_str:
            times.append(time_str)
    
    max_ss = int(os.environ.get('MAX_SCREENSHOTS', '30'))
    unique_times = list(dict.fromkeys(times))[:max_ss]
    
    if len(unique_times) < 10:
        duration = int(os.environ['DURATION_SEC'])
        interval = duration // 11
        for i in range(1, 11):
            t = interval * i
            mm = t // 60
            ss = t % 60
            fallback = f'{mm:02d}:{ss:02d}'
            if fallback not in unique_times:
                unique_times.append(fallback)
            if len(unique_times) >= 10:
                break
    
    for t in unique_times[:max_ss]:
        print(t)
except Exception as e:
    duration = int(os.environ['DURATION_SEC'])
    interval = duration // 11
    for i in range(1, 11):
        t = interval * i
        mm = t // 60
        ss = t % 60
        print(f'{mm:02d}:{ss:02d}')
"
))
        echo "   ✅ 提取到 ${#SCREENSHOT_TIMES[@]} 个时间点"
    else
        echo "   ⚠️  AI 结果不存在，使用均匀分布兜底"
    fi
    
    # 如果提取失败，使用均匀分布
    if [[ ${#SCREENSHOT_TIMES[@]} -eq 0 ]]; then
        if [[ $DURATION_SEC -lt 120 ]]; then
            SCREENSHOT_TIMES=("00:02" "00:30" "01:00" "01:30" "02:00")
        elif [[ $DURATION_SEC -lt 300 ]]; then
            SCREENSHOT_TIMES=("00:02" "00:30" "01:00" "01:30" "02:00" "02:30" "03:00" "03:30" "04:00" "04:30")
        else
            INTERVAL=$((DURATION_SEC / 11))
            SCREENSHOT_TIMES=()
            for i in {1..10}; do
                T=$((INTERVAL * i))
                SCREENSHOT_TIMES+=($(printf "%02d:%02d" $((T/60)) $((T%60))))
            done
        fi
        echo "   📊 使用均匀分布：${#SCREENSHOT_TIMES[@]} 个时间点"
    fi
    
    # 执行截图
    SUCCESS_COUNT=0
    
    # 检查是否有视频文件
    if [[ ! -f "$VIDEO_FILE" ]]; then
        log_warn "视频文件不存在，使用封面图代替截图"
        # 从元数据获取封面 URL
        COVER_URL=$(python3 -c "import json; print(json.load(open('$OUTPUT_DIR/metadata.json')).get('thumbnail', ''))" 2>/dev/null)
        
        if [[ -n "$COVER_URL" ]]; then
            # 下载封面图作为所有截图
            for i in "${!SCREENSHOT_TIMES[@]}"; do
                OUT="$OUTPUT_DIR/screenshots/screenshot_$(printf "%02d" $((i+1))).jpg"
                if curl -L -o "$OUT" "$COVER_URL" 2>/dev/null && [[ -s "$OUT" ]]; then
                    echo "   📸 ${SCREENSHOT_TIMES[$i]} → 封面图 (视频不可用)"
                    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                fi
            done
        else
            log_warn "封面 URL 也不存在，截图将为空"
        fi
    else
        # 正常截图流程
        for i in "${!SCREENSHOT_TIMES[@]}"; do
            TIME="${SCREENSHOT_TIMES[$i]}"
            # 转换为 HH:MM:SS 格式（ffmpeg 需要）
            if [[ "$TIME" =~ ^([0-9]+):([0-9]+)$ ]]; then
                FFMPEG_TIME="00:${BASH_REMATCH[1]}:${BASH_REMATCH[2]}"
            elif [[ "$TIME" =~ ^([0-9]+):([0-9]+):([0-9]+)$ ]]; then
                FFMPEG_TIME="${BASH_REMATCH[1]}:${BASH_REMATCH[2]}:${BASH_REMATCH[3]}"
            else
                FFMPEG_TIME="00:$TIME"
            fi
            
            OUT="$OUTPUT_DIR/screenshots/screenshot_$(printf "%02d" $((i+1))).jpg"
            ffmpeg -ss "$FFMPEG_TIME" -i "$VIDEO_FILE" -vframes 1 -update 1 -q:v 2 "$OUT" -y 2>/dev/null && {
                echo "   📸 $TIME → screenshot_$(printf "%02d" $((i+1))).jpg"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            }
        done
    fi
    
    [[ $SUCCESS_COUNT -eq 0 ]] && { echo "❌ 截图失败"; exit 1; }
    echo "✅ 截图完成 | $SUCCESS_COUNT 张"
    
    # 保存截图时间戳（供 Markdown 渲染使用）
    SCREENSHOT_TIMES_FILE="$OUTPUT_DIR/screenshot_times.txt"
    printf '%s\n' "${SCREENSHOT_TIMES[@]}" > "$SCREENSHOT_TIMES_FILE"
    echo "   💾 截图时间戳已保存：$SCREENSHOT_TIMES_FILE"
    
    save_progress "5" "done"
fi

# Step 6: OSS 上传
if check_progress && [[ -f "$OUTPUT_DIR/screenshot_urls.txt" ]]; then
    echo "⏭️  Step 6 跳过"
else
    echo "☁️  Step 6: OSS 上传..."
    save_progress "6" "running"
    
    OSS_SCRIPT="$SCRIPT_DIR/upload-to-oss.py"
    OSS_URLS_FILE="$OUTPUT_DIR/screenshot_urls.txt"
    OSS_LOG_FILE="$OUTPUT_DIR/oss_upload.log"

if [[ -f "$OSS_SCRIPT" ]]; then
    # 使用 auto 模式，自动识别平台并生成规范路径
    # 错误日志保存到 oss_upload.log
    python3 "$OSS_SCRIPT" auto "$OUTPUT_DIR/screenshots" \
        --video-url "$VIDEO_URL" --metadata "$OUTPUT_DIR/metadata.json" \
        --public --format json > "$OSS_URLS_FILE" 2> "$OSS_LOG_FILE"
    
    EXIT_CODE=$?
    
    if [[ -s "$OSS_URLS_FILE" ]]; then
        URL_COUNT=$(python3 -c "import json; print(len([x for x in json.load(open('$OSS_URLS_FILE')) if x.get('success')]))" 2>/dev/null || echo "0")
        [[ "$URL_COUNT" -gt 0 ]] && echo "✅ OSS 上传成功 | $URL_COUNT 张" || { echo "⚠️  OSS 上传失败"; echo "[]" > "$OSS_URLS_FILE"; }
    else
        echo "⚠️  OSS 上传失败，使用本地路径"
        echo "[]" > "$OSS_URLS_FILE"
    fi
    
    # 上传封面图
    COVER_FILE="$OUTPUT_DIR/cover_url.txt"
    echo "🖼️  上传封面图..." >> "$OSS_LOG_FILE"
    python3 "$OSS_SCRIPT" thumbnail "$OUTPUT_DIR/metadata.json" \
        --public --format json > "$COVER_FILE" 2>> "$OSS_LOG_FILE"
    
    if [[ -f "$COVER_FILE" ]]; then
        COVER_URL=$(python3 -c "import json; print(json.load(open('$COVER_FILE')).get('oss_url', ''))" 2>/dev/null)
        if [[ -n "$COVER_URL" ]]; then
            echo "✅ 封面上传成功：$COVER_URL" >> "$OSS_LOG_FILE"
            # 更新元数据中的 thumbnail 字段（环境变量传递，无 shell 注入）
            OUTPUT_DIR="$OUTPUT_DIR" COVER_URL="$COVER_URL" python3 -c "
import json, os
with open(os.path.join(os.environ['OUTPUT_DIR'], 'metadata.json'), 'r+', encoding='utf-8') as f:
    data = json.load(f)
    data['thumbnail'] = os.environ['COVER_URL']
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.truncate()
print('✅ 元数据已更新')
" >> "$OSS_LOG_FILE" 2>&1
        else
            echo "⚠️  封面上传失败，使用原始 URL" >> "$OSS_LOG_FILE"
        fi
    fi
else
    echo "⚠️  OSS 脚本不存在，使用本地路径"
    echo "[]" > "$OSS_URLS_FILE"
fi
save_progress "6" "done"
fi

# Step 7: 渲染最终 Markdown（截图和 OSS 完成后）
echo "📝 Step 7: 渲染 Markdown..."
SUMMARY_FILE="$OUTPUT_DIR/summary.md"

# 重新调用 AI 脚本，让它读取已上传的截图 URL 并渲染最终 Markdown
python3 "$AI_SCRIPT" "$SUBTITLE_FILE" "$OUTPUT_DIR/metadata.json" "$SUMMARY_FILE" 2>/dev/null || true

if [[ -f "$SUMMARY_FILE" ]]; then
    echo "✅ Markdown 渲染完成"
    rm -f "$TEMP_SUMMARY" 2>/dev/null
else
    echo "⚠️  Markdown 渲染失败，使用临时文件"
    [[ -f "$TEMP_SUMMARY" ]] && mv "$TEMP_SUMMARY" "$SUMMARY_FILE"
fi

# Step 8: 输出
echo "📁 Step 8: 整理输出..."
save_progress "8" "done"

echo ""
echo "================================"
echo "✅ 处理完成！"
echo "================================"
echo "📁 $OUTPUT_DIR"
echo ""

[[ "$VERBOSE" == "true" ]] && { echo "📄 文件:"; ls -lh "$OUTPUT_DIR"; echo "📸 截图:"; ls "$OUTPUT_DIR/screenshots/"; } || echo "📄 总结：$SUMMARY_FILE | 截图：$(ls "$OUTPUT_DIR/screenshots/" 2>/dev/null | wc -l) 张"

# 安全清理（限制目录范围）
if [[ "$KEEP_VIDEO" != "true" ]]; then
    if [[ "$OUTPUT_DIR" == /tmp/video-summarizer/* ]]; then
        rm -f "$OUTPUT_DIR/video.mp4" "$OUTPUT_DIR/audio.mp3" "$OUTPUT_DIR/audio.webm" "$OUTPUT_DIR/video.f"* 2>/dev/null
        echo "🧹 已清理视频/音频"
    else
        log_warn "跳过清理：输出目录不在预期范围内"
    fi
else
    echo "💾 保留视频/音频"
fi

# 截图状态
[[ $(python3 -c "import json; print(len([x for x in json.load(open('$OSS_URLS_FILE')) if x.get('success')]))" 2>/dev/null || echo 0) -gt 0 ]] && echo "📸 截图：✅ 已上传" || echo "📸 截图：⚠️  本地"
echo ""

# Step 9: 推送到 Notion（自动检测配置）
echo "📤 Step 9: 检查 Notion 配置..."

# 检查 Notion 配置（环境变量或 .env 文件）
NOTION_CONFIGURED="false"
NOTION_DB_ID=""
NOTION_KEY=""

# 1. 优先使用环境变量
if [[ -n "$NOTION_VIDEO_SUMMARY_DATABASE_ID" && -n "$NOTION_API_KEY" ]]; then
    NOTION_CONFIGURED="true"
    NOTION_DB_ID="$NOTION_VIDEO_SUMMARY_DATABASE_ID"
    NOTION_KEY="$NOTION_API_KEY"
    log_info "   使用环境变量配置"
else
    # 2. 尝试从 .env 文件读取
    ENV_FILE="$HOME/.openclaw/.env"
    if [[ -f "$ENV_FILE" ]]; then
        ENV_DB_ID=$(grep -E "^NOTION_VIDEO_SUMMARY_DATABASE_ID=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        ENV_KEY=$(grep -E "^NOTION_API_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        
        if [[ -n "$ENV_DB_ID" && -n "$ENV_KEY" ]]; then
            NOTION_CONFIGURED="true"
            NOTION_DB_ID="$ENV_DB_ID"
            NOTION_KEY="$ENV_KEY"
            log_info "   使用 .env 文件配置 ($ENV_FILE)"
        fi
    fi
fi

# 执行推送或跳过
if [[ "$NOTION_CONFIGURED" == "true" ]]; then
    echo "ℹ️     Notion 配置已检测，开始推送..."
    save_progress "9" "running"
    
    NOTION_VIDEO_SUMMARY_DATABASE_ID="$NOTION_DB_ID" \
    python3 "$SCRIPT_DIR/push-to-notion.py" "$SUMMARY_FILE"
    PUSH_EXIT=$?
    
    if [[ $PUSH_EXIT -eq 0 ]]; then
        echo "✅ Notion 推送成功"
        save_progress "9" "done"
    else
        echo "❌ Notion 推送失败"
        save_progress "9" "failed"
    fi
else
    echo "⚠️     未检测到 Notion 配置，跳过推送"
    echo "   💡 提示：如需自动推送，请配置以下任一方式："
    echo "      方式 1 - 环境变量："
    echo "        export NOTION_VIDEO_SUMMARY_DATABASE_ID=your_database_id"
    echo "        export NOTION_API_KEY=your_api_key"
    echo "      方式 2 - .env 文件："
    echo "        在 $HOME/.openclaw/.env 中添加："
    echo "        NOTION_VIDEO_SUMMARY_DATABASE_ID=your_database_id"
    echo "        NOTION_API_KEY=your_api_key"
fi
echo ""
