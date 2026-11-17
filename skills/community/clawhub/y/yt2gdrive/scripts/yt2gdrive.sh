#!/bin/bash
# yt2gdrive.sh — YouTube 频道自动下载媒体（音频/视频）并上传 Google Drive
# 用法: yt2gdrive.sh [--dry-run] [--keep-local]
# 模式: MEDIA_MODE=audio（默认 mp3）或 MEDIA_MODE=video（mp4）
#
# 环境变量可覆盖配置（见下方 CONFIG 区块，默认值适合大多数场景）
# 频道列表: CHANNELS_FILE（每行一个频道 URL，# 开头为注释）
# 归档文件: ARCHIVE_FILE（记录已下载 ID，防止重复）
# 日志文件: LOG_FILE

set -euo pipefail

# ===== 配置（可用环境变量覆盖）=====
CHANNELS_FILE="${CHANNELS_FILE:-$HOME/.config/yt2gdrive/channels.conf}"
MEDIA_MODE="${MEDIA_MODE:-audio}"      # audio=mp3 音频, video=mp4 视频
# 归档按模式分离：音频 archive.txt，视频 archive-video.txt（互不干扰）
ARCHIVE_FILE="${ARCHIVE_FILE:-}"
if [[ -z "$ARCHIVE_FILE" ]]; then
    if [[ "$MEDIA_MODE" == "video" ]]; then
        ARCHIVE_FILE="$HOME/.config/yt2gdrive/archive-video.txt"
    else
        ARCHIVE_FILE="$HOME/.config/yt2gdrive/archive.txt"
    fi
fi
LOCAL_DIR="${LOCAL_DIR:-$HOME/yt-uploads}"
REMOTE_NAME="${REMOTE_NAME:-gdrive}"
REMOTE_PATH="${REMOTE_PATH:-油管}"
LOG_DIR="${LOG_DIR:-$HOME/.config/yt2gdrive}"
LOG_FILE="$LOG_DIR/last.log"
CLEANUP_DAYS="${CLEANUP_DAYS:-3}"     # 本地文件保留天数
MEDIA_MODE="${MEDIA_MODE:-audio}"      # audio=mp3 音频, video=mp4 视频
AUDIO_FORMAT="${AUDIO_FORMAT:-mp3}"
AUDIO_QUALITY="${AUDIO_QUALITY:-0}"    # 0=最佳, 9=最差
VIDEO_FORMAT="${VIDEO_FORMAT:-bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best}"  # 最佳 mp4
MAX_DOWNLOADS="${MAX_DOWNLOADS:-50}"   # 每个频道最多下载数（安全阀）
RECENT_DAYS="${RECENT_DAYS:-3}"        # 只下载最近 N 天内的更新（避免回捞旧视频）
BWLIMIT="${BWLIMIT:-8.5M}"             # 上传限速
MAX_DURATION="${MAX_DURATION:-7200}"  # 跳过时长超过 N 秒的视频（默认 2 小时）
MAX_FILESIZE="${MAX_FILESIZE:-2G}"     # 单文件最大 2GB（视频模式下生效）

# ===== 参数解析 =====
DRY_RUN=""
KEEP_LOCAL=""
for arg in "$@"; do
    case $arg in
        --dry-run)  DRY_RUN="--dry-run"; echo "⚡ DRY RUN 模式，不实际下载/上传" ;;
        --keep-local) KEEP_LOCAL=1 ;;
    esac
done

# ===== 函数 =====
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE" >&2; }
die() { log "❌ FATAL: $*"; exit 1; }

check_deps() {
    for cmd in yt-dlp rclone ffmpeg; do
        command -v "$cmd" &>/dev/null || die "缺少依赖: $cmd"
    done
}

check_drive() {
    rclone ls "${REMOTE_NAME}:${REMOTE_PATH}/" --max-depth 0 &>/dev/null 2>&1 || \
        rclone mkdir "${REMOTE_NAME}:${REMOTE_PATH}/" 2>/dev/null
}

download_channels() {
    local total_new=0
    while IFS= read -r url || [[ -n "$url" ]]; do
        # 跳过空行和注释
        [[ -z "$url" || "$url" =~ ^[[:space:]]*# ]] && continue
        
        url=$(echo "$url" | xargs)  # trim 空白
        local channel_name
        channel_name=$(echo "$url" | sed 's|.*/||')
        log "📥 开始处理频道: $channel_name"
        
        local before_count
        before_count=$(wc -l < "$ARCHIVE_FILE" 2>/dev/null || echo 0)
        
        local date_min
        date_min=$(date -v-${RECENT_DAYS}d '+%Y%m%d' 2>/dev/null || date -d "-${RECENT_DAYS} days" '+%Y%m%d')

        # 根据 MEDIA_MODE 组装下载参数
        local media_args=()
        if [[ "$MEDIA_MODE" == "video" ]]; then
            media_args=(
                -f "$VIDEO_FORMAT"
                --merge-output-format mp4
                --max-filesize "$MAX_FILESIZE"
            )
        else
            media_args=(
                -x
                --audio-format "$AUDIO_FORMAT"
                --audio-quality "$AUDIO_QUALITY"
            )
        fi

        yt-dlp \
            --download-archive "$ARCHIVE_FILE" \
            --dateafter "$date_min" \
            --match-filter "duration < $MAX_DURATION" \
            --break-on-reject \
            --playlist-end "$MAX_DOWNLOADS" \
            "${media_args[@]}" \
            --no-overwrites \
            --ignore-errors \
            --no-warnings \
            --progress \
            -o "${LOCAL_DIR}/%(uploader)s/%(upload_date>%Y%m%d)s - %(title).120s.%(ext)s" \
            "$url" \
            >> "$LOG_FILE" 2>&1 || log "⚠️  频道 $channel_name 部分下载失败（已记录）"
        
        local after_count
        after_count=$(wc -l < "$ARCHIVE_FILE" 2>/dev/null || echo 0)
        local new=$((after_count - before_count))
        total_new=$((total_new + new))
        
        if [[ $new -gt 0 ]]; then
            local kind=音频; [[ "$MEDIA_MODE" == "video" ]] && kind=视频
            log "✅ $channel_name: 新下载 $new 个$kind"
        else
            log "⏭️  $channel_name: 无新内容"
        fi
    done < "$CHANNELS_FILE"
    
    # 清理频道目录名尾随空格（部分频道 uploader 名带尾随空格）
    find "$LOCAL_DIR" -depth -type d -name '* ' -exec bash -c 'd="$1"; mv "$d" "${d%"${d##*[! ]}"}"' _ {} \; 2>/dev/null || true

    echo "$total_new"
}

upload_to_drive() {
    local new_count=$1
    if [[ $new_count -eq 0 ]]; then
        log "📭 无新文件，跳过上传"
        return 0
    fi
    
    log "☁️  上传 $new_count 个新文件到 Google Drive..."
    
    rclone copy "$LOCAL_DIR/" "${REMOTE_NAME}:${REMOTE_PATH}/" \
        --fast-list \
        --transfers=4 \
        --checkers=8 \
        --bwlimit="$BWLIMIT" \
        --log-file="$LOG_FILE" \
        --log-level=INFO \
        $DRY_RUN
    
    log "✅ 上传完成"
}

cleanup_local() {
    if [[ -n "$KEEP_LOCAL" ]]; then
        log "📦 本地文件保留（--keep-local）"
        return 0
    fi
    
    log "🧹 清理本地 ${CLEANUP_DAYS} 天前的文件..."
    find "$LOCAL_DIR" -type f -mtime "+${CLEANUP_DAYS}" -delete 2>/dev/null || true
    find "$LOCAL_DIR" -type d -empty -delete 2>/dev/null || true
    log "🧹 清理完成"
}

# ===== 主流程 =====
log "===== yt2gdrive 开始 ====="

check_deps
check_drive

[[ ! -f "$CHANNELS_FILE" ]] && die "频道列表不存在: $CHANNELS_FILE"

log "📂 下载目录: $LOCAL_DIR"
log "📋 频道列表: $CHANNELS_FILE"
log "🎛️ 模式: $MEDIA_MODE"

# 确保归档文件存在
touch "$ARCHIVE_FILE"

# 下载
new_count=$(download_channels)

# 上传
upload_to_drive "$new_count"

# 清理本地
cleanup_local

log "===== yt2gdrive 完成 ====="
