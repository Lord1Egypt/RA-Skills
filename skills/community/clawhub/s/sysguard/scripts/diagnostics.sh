#!/usr/bin/env bash
#===============================================================================
# Diagnostics Engine - 8 Hidden Events Detection
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/util.sh"

DATA_DIR="$(dirname "${BASH_SOURCE[0]}")/../data"
HISTORY_DIR="$DATA_DIR/history"

# === Run Diagnostics ===
run_diagnostics() {
    local timestamp=$(get_timestamp)
    local issues=()
    local issue_index=0
    
    # --- Event 1: Gateway 无响应 ---
    if [[ "$(check_gateway)" != "up" ]]; then
        issues[issue_index++]="[1/8] 🚨 Gateway 无响应 | 当前状态: ❌ 未运行 | 建议: 执行 'openclaw gateway restart'"
    fi
    
    # --- Event 2: 磁盘空间不足 ---
    local disk_usage=$(get_disk_usage)
    if [[ $(check_threshold "$disk_usage" "$TH_DISK_WARN" "$TH_DISK_CRIT") != "normal" ]]; then
        issues[issue_index++]="[2/8] ⚠️ 系统盘空间不足 | 当前: ${disk_usage}% | 阈值: ${TH_DISK_WARN}% 警告 / ${TH_DISK_CRIT}% 严重 | 建议: 清理日志或扩展磁盘"
    fi
    
    # --- Event 3: 内存泄漏 ---
    if [[ -f "$HISTORY_DIR/$(get_date_key).json" ]]; then
        local mem_values=$(grep -o '"mem":.*"value":[0-9]*' "$HISTORY_DIR/$(get_date_key).json" 2>/dev/null | grep -o '[0-9]*$' | tail -3)
        if [[ $(echo "$mem_values" | wc -l) -ge 3 ]]; then
            local avg_mem=$(echo "$mem_values" | awk '{sum+=$1} END {printf "%.0f", sum/NR}')
            if [[ $avg_mem -gt $TH_MEM_WARN ]]; then
                issues[issue_index++]="[3/8] ⚠️ 内存使用率偏高 | 当前: ${avg_mem}% (连续检测) | 可能原因: 缓存未清理 | 建议: 执行 'sysguard clean' 或重启 Gateway"
            fi
        fi
    fi
    
    # --- Event 4: API 响应超时 ---
    local api_time=$(probe_http "https://api.minimaxi.com" 5 2>/dev/null || echo "10")
    if (( $(echo "$api_time > 5" | bc -l 2>/dev/null || echo 0) )); then
        issues[issue_index++]="[4/8] ⚠️ API 响应超时 | 当前: ${api_time}s | 阈值: 5s | 可能原因: 网络延迟或服务商问题"
    fi
    
    # --- Event 5: 进程数异常 ---
    local proc_count=$(get_process_count)
    if [[ $proc_count -gt 500 ]]; then
        issues[issue_index++]="[5/8] ⚠️ 进程数异常 | 当前: $proc_count | 阈值: 500 | 可能原因: 进程泄漏 | 建议: 检查异常进程"
    fi
    
    # --- Event 6: 日志暴涨 ---
    local log_size=$(du -sb "$LOG_DIR" 2>/dev/null | awk '{print $1}' || echo 0)
    if [[ $log_size -gt 1073741824 ]]; then  # 1GB
        issues[issue_index++]="[6/8] ⚠️ 日志文件过大 | 当前: $(du -h "$LOG_DIR" 2>/dev/null | tail -1 | awk '{print $1}') | 阈值: 1GB | 建议: 执行 'journalctl --vacuum-time=7d'"
    fi
    
    # --- Event 7: Cron 堆积 ---
    local cron_count=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
    if [[ $cron_count -gt 20 ]]; then
        issues[issue_index++]="[7/8] ℹ️ 定时任务较多 | 当前: $cron_count 个 | 可能影响: 系统负载 | 建议: 清理不必要的定时任务"
    fi
    
    # --- Event 8: 网络丢包 ---
    local ping_result=$(ping -c 5 -W 2 api.minimaxi.com 2>/dev/null | grep "loss" | grep -o '[0-9]*%' | tr -d '%' || echo "100")
    if [[ $ping_result -gt 20 ]]; then
        issues[issue_index++]="[8/8] ⚠️ 网络延迟/丢包 | 当前: ${ping_result}% 丢包 | 阈值: 20% | 可能原因: 网络不稳定"
    fi
    
    # === Output Report ===
    echo "🔍 SysGuard 诊断报告"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⏰ 时间: $timestamp"
    echo ""
    
    if [[ ${#issues[@]} -eq 0 ]]; then
        echo "✅ 未发现明显问题"
    else
        echo "🚨 发现 ${#issues[@]} 个潜在问题:"
        echo ""
        for issue in "${issues[@]}"; do
            echo "$issue"
            echo ""
        done
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💡 执行 'sgch' 进行详细检查"
}

export -f run_diagnostics
