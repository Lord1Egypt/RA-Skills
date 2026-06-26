#!/bin/bash
# 清理超过 7 天的 memory 日志文件
# 移动到 memory/archive/ 目录

WORKSPACE="${OPENCLAW_WORKSPACE:-/home/lenovo/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
CUTOFF_DAYS=7

mkdir -p "$ARCHIVE_DIR"

count=0
for f in "$MEMORY_DIR"/2???-??-??.md; do
    [ -f "$f" ] || continue
    # 提取日期部分
    basename=$(basename "$f" .md)
    # 计算文件天数
    file_epoch=$(date -d "$basename" +%s 2>/dev/null) || continue
    now_epoch=$(date +%s)
    days_old=$(( (now_epoch - file_epoch) / 86400 ))

    if [ "$days_old" -gt "$CUTOFF_DAYS" ]; then
        mv "$f" "$ARCHIVE_DIR/"
        echo "归档: $basename.md (${days_old}天前)"
        count=$((count + 1))
    fi
done

echo "共归档 $count 个文件"
