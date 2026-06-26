#!/bin/bash
# Viking Memory System - sv_compress_v2
# 层级压缩调度脚本
#
# 层级结构: hot(0-7天) → warm(8-29天) → cold(30-89天) → archive(90天+)
#
# 用法:
#   sv_compress_v2 --dry-run    # 预览
#   sv_compress_v2 --force      # 执行
#   sv_compress_v2 --shared     # 压缩共享目录
#
# Cron配置 (每周日凌晨2点执行):
#   0 2 * * 0 ~/.openclaw/viking/scripts/sv_compress_v2.sh --force >> ~/.openclaw/viking-global/logs/compress.log 2>&1

set +e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
VIKING_GLOBAL="$HOME/.openclaw/viking-global"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"
DRY_RUN=false
FORCE=false
TARGET="personal"

while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --force) FORCE=true; shift ;;
        --shared) TARGET="shared"; shift ;;
        --both) TARGET="both"; shift ;;
        *) shift ;;
    esac
done

echo "=== Viking 记忆压缩 $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "模式: $([ "$DRY_RUN" = true ] && echo "预览" || echo "执行")"

HOT_MAX=7; WARM_MAX=29; COLD_MAX=89

# 安全解析 frontmatter（仅 --- 块内）
# Bug4 Fix: 不再用 tr -d " " 全删，改用 trim 只去首尾空白
parse_fm() {
    local file="$1"
    local key="$2"
    awk -v key="$key" -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; next }
        /^---$/ && in_fm { exit }
        in_fm && $0 ~ "^" key ": *" {
            sub("^" key ": *", "")
            # trim: 去首尾空白，保留值内的空格（如 ISO 时间）
            gsub(/^[ \t]+|[ \t]+$/, "")
            print; exit
        }
    ' "$file" 2>/dev/null
}

get_target_layer() {
    local days=$1
    if [ "$days" -gt "$COLD_MAX" ]; then echo "archive"
    elif [ "$days" -gt "$WARM_MAX" ]; then echo "cold"
    elif [ "$days" -gt "$HOT_MAX" ]; then echo "warm"
    else echo "hot"
    fi
}

today_ts=$(date +%s)

# Bug3 Fix: 去掉 search_dir 尾斜杠，确保 dirname 计算正确
normalize_dir() {
    local dir="${1%/}"
    echo "$dir"
}

compress_dir() {
    local search_dir="${1%/}"   # Bug3 Fix: 去掉尾斜杠
    local label="$2"
    [ -d "$search_dir" ] || return 0
    echo ""
    echo "【$label】"
    echo "目录: $search_dir"

    local total=0 moved=0 skipped_conflict=0
    local files
    mapfile -t files < <(find "$search_dir" -maxdepth 1 -name "*.md" -type f 2>/dev/null)

    for file in "${files[@]}"; do
        total=$((total + 1))
        local basename_f
        basename_f=$(basename -- "$file")   # Bug5 Fix: 用 -- 分隔
        local current_layer
        current_layer=$(parse_fm "$file" "current_layer")
        local importance
        importance=$(parse_fm "$file" "importance")
        local created
        created=$(parse_fm "$file" "created")

        [ -z "$created" ] && { echo "  ⚠ 无日期: $basename_f"; continue; }

        local created_epoch
        created_epoch=$(date -d "$created" +%s 2>/dev/null) || { echo "  ⚠ 日期错误: $basename_f"; continue; }
        local days=$(( (today_ts - created_epoch) / 86400 ))
        local target_layer
        target_layer=$(get_target_layer $days)

        # 重要记忆跳过自动压缩
        if [ "$importance" = "high" ] && [ "$FORCE" != "true" ]; then
            continue
        fi

        if [ "$target_layer" != "$current_layer" ]; then
            if [ "$DRY_RUN" = true ]; then
                echo "  📄 $basename_f: $current_layer → $target_layer (${days}天)"
            else
                local base_dir
                base_dir=$(dirname -- "$search_dir")   # Bug3 Fix: dirname 也用 --
                local target_subdir="$base_dir/$target_layer"
                local target_path="$target_subdir/$basename_f"
                mkdir -p "$target_subdir"

                # Bug1 Fix: 检查目标文件是否已存在，避免覆盖
                if [ -f "$target_path" ]; then
                    echo "  ⚠ 冲突（同名文件已存在）: $basename_f → 跳过"
                    skipped_conflict=$((skipped_conflict + 1))
                    continue
                fi

                # Bug3 Fix: 原子性更新 — 先写临时文件再移动
                local tmp_file="${file}.compress.tmp"
                sed "s/^current_layer:.*/current_layer: $target_layer/" "$file" > "$tmp_file" && \
                mv -f "$tmp_file" "$target_path" && \
                rm -f "$file" && \
                echo "  ✓ $basename_f → $target_layer (${days}天)" || {
                    rm -f "$tmp_file"
                    echo "  ✗ 移动失败: $basename_f"
                }

                # ============ Phase 3: 归档时生成摘要 ============
                # 如果是归档到 archive 层，调用摘要生成
                if [ "$target_layer" = "archive" ]; then
                    echo "  📝 Phase 3: 正在生成摘要..."
                    "$VIKING_HOME/scripts/sv_archive_summary.sh" "$target_path" --keep 2>/dev/null || \
                        echo "  ⚠ 摘要生成失败（可能缺少 LLM 接口）"
                fi
            fi
            moved=$((moved + 1))
        fi
    done

    echo "统计: 总=$total 移动=$moved 冲突跳过=$skipped_conflict"
}

# 处理个人空间（逐层调用，让 warm/cold/archive 也能被扫描）
if [ "$TARGET" = "personal" ] || [ "$TARGET" = "both" ]; then
    compress_dir "$WORKSPACE/agent/memories/hot" "个人-hot"
    compress_dir "$WORKSPACE/agent/memories/warm" "个人-warm"
    compress_dir "$WORKSPACE/agent/memories/cold" "个人-cold"
    compress_dir "$WORKSPACE/agent/memories/archive" "个人-archive"
fi

# 处理共享空间
if [ "$TARGET" = "shared" ] || [ "$TARGET" = "both" ]; then
    compress_dir "$VIKING_GLOBAL/shared/memory/hot" "共享-hot"
    compress_dir "$VIKING_GLOBAL/shared/memory/warm" "共享-warm"
    compress_dir "$VIKING_GLOBAL/shared/memory/cold" "共享-cold"
    compress_dir "$VIKING_GLOBAL/shared/memory/archive" "共享-archive"
fi

echo ""
echo "=== 完成 ==="
exit 0
