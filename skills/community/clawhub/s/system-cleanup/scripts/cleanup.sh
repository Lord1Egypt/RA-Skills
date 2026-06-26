#!/bin/bash

# 系统清理脚本
# 用于定期清理OpenClaw系统的临时文件、备份文件等

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查OpenClaw目录是否存在
OPENCLAW_DIR="$HOME/.openclaw"
if [ ! -d "$OPENCLAW_DIR" ]; then
    log_error "OpenClaw目录不存在: $OPENCLAW_DIR"
    exit 1
fi

log "开始系统清理..."
log "OpenClaw目录: $OPENCLAW_DIR"

# 1. 分析磁盘使用情况
log "=== 磁盘使用分析 ==="
total_size=$(du -sh "$OPENCLAW_DIR" | cut -f1)
log "总大小: $total_size"

echo ""
log "按目录大小排序:"
du -sh "$OPENCLAW_DIR"/* 2>/dev/null | sort -h || true

# 2. 备份文件清理
log ""
log "=== 备份文件清理 ==="
backup_dir="${OPENCLAW_DIR}"
backup_files=$(find "$backup_dir" -maxdepth 1 -type f \( -name "*.bak*" -o -name "*.backup*" -o -name "*.clobbered*" \) -mtime +7 2>/dev/null | sort)

if [ -n "$backup_files" ]; then
    log "找到可清理的备份文件 (超过7天):"
    echo "$backup_files" | while read -r file; do
        size=$(du -h "$file" | cut -f1)
        mtime=$(stat -c %y "$file" | cut -d' ' -f1)
        log_warning "  $file (${size}, 修改于: $mtime)"
    done
    echo ""
    read -p "是否删除这些备份文件? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo "$backup_files" | while read -r file; do
            rm -v "$file"
        done
        log_success "备份文件清理完成"
    else
        log "跳过备份文件清理"
    fi
else
    log "未找到超过7天的旧备份文件"
fi

# 3. 临时文件清理
log ""
log "=== 临时文件清理 ==="

# 清理vim交换文件
swp_files=$(find "$OPENCLAW_DIR" -name "*.swp" -o -name "*.swx" 2>/dev/null)
if [ -n "$swp_files" ]; then
    log "找到vim交换文件:"
    echo "$swp_files" | while read -r file; do
        log_warning "  $file"
    done
    echo "$swp_files" | xargs -r rm -v
    log_success "临时文件清理完成"
else
    log "未找到vim交换文件"
fi

# 4. /tmp目录清理
log ""
log "=== /tmp目录清理 ==="
tmp_files=$(find /tmp -name "*openclaw*" -type f -mtime +3 2>/dev/null | head -10)
if [ -n "$tmp_files" ]; then
    log "找到可清理的/tmp文件 (超过3天):"
    echo "$tmp_files" | while read -r file; do
        size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "unknown")
        mtime=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        log_warning "  $file (${size}, 修改于: $mtime)"
    done
    log_warning "注意: /tmp文件可能正在使用，请谨慎清理"
else
    log "未找到超过3天的/tmp文件"
fi

# 5. 会话文件检查
log ""
log "=== 会话文件检查 ==="
sessions_dir="${OPENCLAW_DIR}/agents"
if [ -d "$sessions_dir" ]; then
    session_files=$(find "$sessions_dir" -name "*.jsonl" -type f -mtime +14 2>/dev/null)
    if [ -n "$session_files" ]; then
        log "找到可清理的旧会话文件 (超过14天):"
        count=$(echo "$session_files" | wc -l)
        total_size=$(echo "$session_files" | xargs -r du -ch 2>/dev/null | tail -1 | cut -f1)
        log_warning "  找到 $count 个文件，总大小约 $total_size"
    else
        log "未找到超过14天的旧会话文件"
    fi
    
    # 检查当前会话大小
    recent_sessions=$(find "$sessions_dir" -name "*.jsonl" -type f -mtime -1 2>/dev/null)
    if [ -n "$recent_sessions" ]; then
        log "最近24小时的会话文件:"
        echo "$recent_sessions" | while read -r file; do
            size=$(du -h "$file" | cut -f1)
            name=$(basename "$file")
            log "  $name (${size})"
        done
    fi
fi

# 6. 检查系统状态
log ""
log "=== 系统状态检查 ==="
if command -v openclaw &> /dev/null; then
    log "检查OpenClaw状态..."
    openclaw gateway status 2>&1 | grep -E "(Service:|Gateway:|Runtime:|RPC probe:|Service config issue:)" || true
else
    log_warning "openclaw命令未找到"
fi

# 7. 清理后的磁盘使用
log ""
log "=== 清理完成 ==="
log "系统清理执行完成"
log "可考虑的运行频率："
log "  - 备份文件清理：每周一次"
log "  - 临时文件清理：每天一次"
log "  - 磁盘使用分析：每周一次"

log ""
log_success "系统清理脚本执行完成！"

# 退出代码
exit 0