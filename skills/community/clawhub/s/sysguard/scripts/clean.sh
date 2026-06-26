#!/usr/bin/env bash
#===============================================================================
# Clean Script - Cache & Temp Cleanup
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"

# === Run Clean ===
run_clean() {
    local timestamp=$(get_timestamp)
    local freed=0
    
    log_info "Starting cleanup at $timestamp"
    
    # Clean OpenClaw temp files
    if [[ -d "/tmp/openclaw" ]]; then
        local before=$(du -sb /tmp/openclaw 2>/dev/null | awk '{print $1}')
        find /tmp/openclaw -type f -mtime +1 -delete 2>/dev/null || true
        local after=$(du -sb /tmp/openclaw 2>/dev/null | awk '{print $1}')
        freed=$((freed + before - after))
        echo "🧹 清理 OpenClaw 临时文件..."
    fi
    
    # Clean npm cache
    if command -v npm &>/dev/null; then
        npm cache clean --force 2>/dev/null || true
        echo "🧹 清理 NPM 缓存..."
    fi
    
    # Clean journal logs (older than 7 days)
    if command -v journalctl &>/dev/null; then
        journalctl --vacuum-time=7d 2>/dev/null || true
        echo "🧹 清理系统日志 (保留7天)..."
    fi
    
    # Clean old history data
    local history_dir="$(dirname "${BASH_SOURCE[0]}")/../data/history"
    if [[ -d "$history_dir" ]]; then
        find "$history_dir" -name "*.json" -mtime +${HISTORY_RETENTION_DAYS} -delete 2>/dev/null || true
        echo "🧹 清理历史数据 (保留${HISTORY_RETENTION_DAYS}天)..."
    fi
    
    echo ""
    echo "✅ 清理完成"
    [[ $freed -gt 0 ]] && echo "💾 释放空间: $(numfmt --to=iec $freed 2>/dev/null || echo "${freed} bytes")"
}

export -f run_clean
