#!/bin/bash

# Session 文件归档脚本
# 当 session 文件大于指定大小后，自动进行归档和压缩

set -e

# 配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
ARCHIVE_DIR="/root/.openclaw/agents/main/sessions/archive"
MAX_SIZE_MB=1  # 超过 1MB 就归档
MAX_AGE_DAYS=2 # 超过 2 天的文件也归档（缩短时间，更快归档）
ARCHIVE_RESET_FILES=true # 是否归档 .reset 备份文件

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

echo "=== Session 归档脚本开始运行 ==="
echo "时间: $(date)"
echo "Session 目录: $SESSIONS_DIR"
echo "归档目录: $ARCHIVE_DIR"
echo "最大文件大小: ${MAX_SIZE_MB}MB"
echo "最大文件天数: ${MAX_AGE_DAYS}天"
echo ""

# 统计当前状态
echo "=== 当前状态 ==="
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo "归档目录总大小: $(du -sh "$ARCHIVE_DIR" 2>/dev/null || echo "0")"
echo ""

# 查找需要归档的文件
echo "=== 查找需要归档的文件 ==="

# 1. 查找大于 MAX_SIZE_MB 的 .jsonl 文件（排除当前正在使用的文件 - 有 .lock 文件的）
echo "1. 查找大于 ${MAX_SIZE_MB}MB 的文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    lockfile="${file}.lock"
    
    # 检查是否有 lock 文件（正在使用中）
    if [ -f "$lockfile" ]; then
        echo "  跳过 (正在使用): $filename"
        continue
    fi
    
    # 检查是否已经是压缩文件
    if [[ "$filename" == *.gz ]]; then
        echo "  跳过 (已压缩): $filename"
        continue
    fi
    
    # 检查是否已经在归档目录
    if [[ "$file" == *"/archive/"* ]]; then
        continue
    fi
    
    filesize_mb=$(du -m "$file" | cut -f1)
    echo "  发现大文件: $filename (${filesize_mb}MB)"
    
    # 移动到归档目录并压缩
    mv "$file" "$ARCHIVE_DIR/"
    gzip "$ARCHIVE_DIR/$filename"
    echo "    → 已归档并压缩: $ARCHIVE_DIR/$filename.gz"
    
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -size +${MAX_SIZE_MB}M -type f -print0)

# 1.5 归档 .reset 备份文件（如果启用）
if [ "$ARCHIVE_RESET_FILES" = true ]; then
    echo ""
    echo "1.5 归档 .reset 备份文件..."
    while IFS= read -r -d '' file; do
        filename=$(basename "$file")
        
        # 检查是否已经是压缩文件
        if [[ "$filename" == *.gz ]]; then
            echo "  跳过 (已压缩): $filename"
            continue
        fi
        
        # 检查是否已经在归档目录
        if [[ "$file" == *"/archive/"* ]]; then
            continue
        fi
        
        echo "  发现备份文件: $filename"
        
        # 移动到归档目录并压缩
        mv "$file" "$ARCHIVE_DIR/"
        gzip "$ARCHIVE_DIR/$filename"
        echo "    → 已归档并压缩: $ARCHIVE_DIR/$filename.gz"
        
    done < <(find "$SESSIONS_DIR" -name "*.reset.*" -type f -print0)
fi

# 2. 查找超过 MAX_AGE_DAYS 天的文件
echo ""
echo "2. 查找超过 ${MAX_AGE_DAYS} 天的文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    lockfile="${file}.lock"
    
    # 检查是否有 lock 文件（正在使用中）
    if [ -f "$lockfile" ]; then
        echo "  跳过 (正在使用): $filename"
        continue
    fi
    
    # 检查是否已经是压缩文件
    if [[ "$filename" == *.gz ]]; then
        echo "  跳过 (已压缩): $filename"
        continue
    fi
    
    # 检查是否已经在归档目录
    if [[ "$file" == *"/archive/"* ]]; then
        continue
    fi
    
    fileage=$(stat -c %Y "$file")
    currenttime=$(date +%s)
    agedays=$(( (currenttime - fileage) / 86400 ))
    
    echo "  发现旧文件: $filename (${agedays}天)"
    
    # 移动到归档目录并压缩
    mv "$file" "$ARCHIVE_DIR/"
    gzip "$ARCHIVE_DIR/$filename"
    echo "    → 已归档并压缩: $ARCHIVE_DIR/$filename.gz"
    
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -type f -mtime +${MAX_AGE_DAYS} -print0)

# 3. 压缩归档目录中未压缩的文件
echo ""
echo "3. 检查归档目录中未压缩的文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    echo "  压缩: $filename"
    gzip "$file"
done < <(find "$ARCHIVE_DIR" -name "*.jsonl" -type f -print0 2>/dev/null || true)

# 4. 清理归档目录中超过 30 天的压缩文件
echo ""
echo "4. 清理归档目录中超过 30 天的压缩文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    fileage=$(stat -c %Y "$file" 2>/dev/null || echo 0)
    currenttime=$(date +%s)
    agedays=$(( (currenttime - fileage) / 86400 ))
    
    if [ "$agedays" -gt 30 ]; then
        echo "  删除: $filename (${agedays}天)"
        rm -f "$file"
    fi
done < <(find "$ARCHIVE_DIR" -name "*.jsonl.gz" -type f -print0 2>/dev/null || true)

# 最终统计
echo ""
echo "=== 完成 ==="
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo "归档目录总大小: $(du -sh "$ARCHIVE_DIR" 2>/dev/null || echo "0")"
echo "归档文件数量: $(ls -1 "$ARCHIVE_DIR" 2>/dev/null | wc -l)"
echo "完成时间: $(date)"
