#!/bin/bash
# 自动归档 90 天前的日志

LOGS_DIR="$(dirname "$0")/../logs"
ARCHIVE_DIR="$LOGS_DIR/archive"
DAYS_OLD=90

mkdir -p "$ARCHIVE_DIR"

echo "🔍 查找 $DAYS_OLD 天前的日志..."

# 查找并移动旧日志
find "$LOGS_DIR" -type f -name "*.md" -mtime +$DAYS_OLD ! -path "*/archive/*" | while read -r file; do
    relative_path="${file#$LOGS_DIR/}"
    target_dir="$ARCHIVE_DIR/$(dirname "$relative_path")"
    
    mkdir -p "$target_dir"
    mv "$file" "$target_dir/"
    echo "📦 已归档: $relative_path"
done

echo "✅ 归档完成"
