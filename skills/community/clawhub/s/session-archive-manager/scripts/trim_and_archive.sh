#!/bin/bash

# Session 裁剪式智能归档脚本
# 对正在使用的大 session 文件进行裁剪：
# 1. 检测超过大小限制的 session 文件
# 2. 分析整个 session，把旧内容提取总结
# 3. 备份完整文件到归档目录
# 4. 只保留最近 N 条消息在原文件中

set -e

# 配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
ARCHIVE_DIR="/root/.openclaw/agents/main/sessions/archive"
SUMMARY_DIR="/root/.openclaw/agents/main/sessions/summaries"
TRIM_SCRIPT="/root/.openclaw/workspace/session_trimmer.py"

# 裁剪配置
MAX_SIZE_MB=2      # 超过 2MB 才裁剪
KEEP_RECENT=150     # 保留最近 150 条消息

# 创建目录
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$SUMMARY_DIR"

echo "="*70
echo "Session 裁剪式智能归档脚本"
echo "="*70
echo "时间: $(date)"
echo "Session 目录: $SESSIONS_DIR"
echo "裁剪阈值: ${MAX_SIZE_MB}MB"
echo "保留消息数: ${KEEP_RECENT} 条"
echo ""

# 统计当前状态
echo "=== 当前状态 ==="
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo ""
echo "大文件列表 (>${MAX_SIZE_MB}MB):"
find "$SESSIONS_DIR" -name "*.jsonl" -size +${MAX_SIZE_MB}M -type f -exec ls -lh {} \; 2>/dev/null || echo "  (没有超过 ${MAX_SIZE_MB}MB 的文件)"
echo ""

# 检查裁剪脚本是否存在
if [ ! -f "$TRIM_SCRIPT" ]; then
    echo "错误: 裁剪脚本不存在: $TRIM_SCRIPT"
    exit 1
fi

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: python3 不可用"
    exit 1
fi

# 处理单个文件的函数
trim_file() {
    local file="$1"
    local filename=$(basename "$file")
    local lockfile="${file}.lock"
    
    # 检查是否有 lock 文件（正在使用中）
    if [ -f "$lockfile" ]; then
        echo ""
        echo "跳过 (正在使用): $filename"
        return 0
    fi
    
    # 检查文件大小
    local filesize_mb=$(du -m "$file" | cut -f1)
    if [ "$filesize_mb" -lt "$MAX_SIZE_MB" ]; then
        return 0
    fi
    
    echo ""
    echo "="*70
    echo "处理文件: $filename (${filesize_mb}MB)"
    echo "="*70
    
    # 调用 Python 裁剪脚本
    if python3 "$TRIM_SCRIPT" "$file" "$KEEP_RECENT"; then
        echo ""
        echo "✓ $filename 裁剪成功"
    else
        echo ""
        echo "✗ $filename 裁剪失败"
        return 1
    fi
}

# 查找并处理超过大小限制的文件
echo "=== 开始裁剪 ==="
files_processed=0

while IFS= read -r -d '' file; do
    trim_file "$file"
    files_processed=$((files_processed + 1))
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -size +${MAX_SIZE_MB}M -type f -print0)

# 同时也运行一下常规归档（处理旧文件）
echo ""
echo "="*70
echo "运行常规归档（处理旧文件）"
echo "="*70
if [ -f "/root/.openclaw/workspace/archive_with_summary.sh" ]; then
    /root/.openclaw/workspace/archive_with_summary.sh
fi

# 最终统计
echo ""
echo "="*70
echo "完成"
echo "="*70
echo "Session 目录总大小: $(du -sh "$SESSIONS_DIR" | cut -f1)"
echo "归档目录总大小: $(du -sh "$ARCHIVE_DIR" 2>/dev/null || echo "0")"
echo "总结目录总大小: $(du -sh "$SUMMARY_DIR" 2>/dev/null || echo "0")"
echo "完成时间: $(date)"
