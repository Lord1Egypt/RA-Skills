#!/bin/bash

# Session 智能总结 + 归档脚本
# 1. 对需要归档的 session 文件进行智能总结提取
# 2. 保存总结到 summaries/ 目录
# 3. 然后压缩归档原文件

set -e

# 配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
ARCHIVE_DIR="/root/.openclaw/agents/main/sessions/archive"
SUMMARY_DIR="/root/.openclaw/agents/main/sessions/summaries"
MAX_SIZE_MB=1  # 超过 1MB 就归档
MAX_AGE_DAYS=2  # 超过 2 天的文件也归档
SUMMARIZE_SCRIPT="/root/.openclaw/workspace/session_summarizer.py"

# 创建目录
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$SUMMARY_DIR"

echo "=== Session 智能总结归档脚本开始运行 ==="
echo "时间: $(date)"
echo "Session 目录: $SESSIONS_DIR"
echo "归档目录: $ARCHIVE_DIR"
echo "总结目录: $SUMMARY_DIR"
echo "最大文件大小: ${MAX_SIZE_MB}MB"
echo "最大文件天数: ${MAX_AGE_DAYS}天"
echo ""

# 统计当前状态
echo "=== 当前状态 ==="
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo "归档目录总大小: $(du -sh "$ARCHIVE_DIR" 2>/dev/null || echo "0")"
echo "总结目录总大小: $(du -sh "$SUMMARY_DIR" 2>/dev/null || echo "0")"
echo ""

# 检查总结脚本是否存在
if [ ! -f "$SUMMARIZE_SCRIPT" ]; then
    echo "警告: 总结脚本不存在: $SUMMARIZE_SCRIPT"
    echo "将只进行压缩归档，不生成总结"
    SUMMARIZE_SCRIPT=""
fi

# 检查 Python 是否可用
if [ -n "$SUMMARIZE_SCRIPT" ] && ! command -v python3 &> /dev/null; then
    echo "警告: python3 不可用"
    echo "将只进行压缩归档，不生成总结"
    SUMMARIZE_SCRIPT=""
fi

# 处理单个文件的函数
process_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo ""
    echo "处理文件: $filename"
    
    # 1. 生成总结（如果可用）
    if [ -n "$SUMMARIZE_SCRIPT" ]; then
        echo "  正在生成总结..."
        if python3 "$SUMMARIZE_SCRIPT" "$file" "$SUMMARY_DIR"; then
            echo "  ✓ 总结生成成功"
        else
            echo "  ✗ 总结生成失败，继续归档"
        fi
    fi
    
    # 2. 移动到归档目录
    echo "  移动到归档目录..."
    mv "$file" "$ARCHIVE_DIR/"
    
    # 3. 压缩
    echo "  压缩中..."
    gzip "$ARCHIVE_DIR/$filename"
    
    echo "  ✓ 完成: $ARCHIVE_DIR/$filename.gz"
}

# 1. 查找大于 MAX_SIZE_MB 的 .jsonl 文件（排除当前正在使用的文件）
echo "=== 查找需要归档的文件 ==="
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
        continue
    fi
    
    # 检查是否已经在归档目录或总结目录
    if [[ "$file" == *"/archive/"* ]] || [[ "$file" == *"/summaries/"* ]]; then
        continue
    fi
    
    filesize_mb=$(du -m "$file" | cut -f1)
    echo "  发现大文件: $filename (${filesize_mb}MB)"
    
    process_file "$file"
    
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -size +${MAX_SIZE_MB}M -type f -print0)

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
        continue
    fi
    
    # 检查是否已经在归档目录或总结目录
    if [[ "$file" == *"/archive/"* ]] || [[ "$file" == *"/summaries/"* ]]; then
        continue
    fi
    
    fileage=$(stat -c %Y "$file")
    currenttime=$(date +%s)
    agedays=$(( (currenttime - fileage) / 86400 ))
    
    echo "  发现旧文件: $filename (${agedays}天)"
    
    process_file "$file"
    
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -type f -mtime +${MAX_AGE_DAYS} -print0)

# 3. 归档 .reset 备份文件
echo ""
echo "3. 归档 .reset 备份文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    
    # 检查是否已经是压缩文件
    if [[ "$filename" == *.gz ]]; then
        continue
    fi
    
    # 检查是否已经在归档目录
    if [[ "$file" == *"/archive/"* ]]; then
        continue
    fi
    
    echo "  发现备份文件: $filename"
    
    # 这些是备份文件，不生成总结，直接归档
    mv "$file" "$ARCHIVE_DIR/"
    gzip "$ARCHIVE_DIR/$filename"
    echo "    → 已归档并压缩: $ARCHIVE_DIR/$filename.gz"
    
done < <(find "$SESSIONS_DIR" -name "*.reset.*" -type f -print0)

# 4. 压缩归档目录中未压缩的文件
echo ""
echo "4. 检查归档目录中未压缩的文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    echo "  压缩: $filename"
    gzip "$file"
done < <(find "$ARCHIVE_DIR" -name "*.jsonl" -type f -print0 2>/dev/null || true)

# 5. 清理归档目录中超过 30 天的压缩文件
echo ""
echo "5. 清理归档目录中超过 30 天的压缩文件..."
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

# 6. 清理总结目录中超过 60 天的总结文件
echo ""
echo "6. 清理总结目录中超过 60 天的总结文件..."
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    fileage=$(stat -c %Y "$file" 2>/dev/null || echo 0)
    currenttime=$(date +%s)
    agedays=$(( (currenttime - fileage) / 86400 ))
    
    if [ "$agedays" -gt 60 ]; then
        echo "  删除: $filename (${agedays}天)"
        rm -f "$file"
    fi
done < <(find "$SUMMARY_DIR" -name "*_summary_*.json" -type f -print0 2>/dev/null || true)

# 最终统计
echo ""
echo "=== 完成 ==="
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo "归档目录总大小: $(du -sh "$ARCHIVE_DIR" 2>/dev/null || echo "0")"
echo "总结目录总大小: $(du -sh "$SUMMARY_DIR" 2>/dev/null || echo "0")"
echo "归档文件数量: $(ls -1 "$ARCHIVE_DIR" 2>/dev/null | wc -l)"
echo "总结文件数量: $(ls -1 "$SUMMARY_DIR" 2>/dev/null | wc -l)"
echo "完成时间: $(date)"
