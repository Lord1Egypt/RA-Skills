#!/usr/bin/env bash
#===============================================================================
# UI Formatter - IM-friendly Output
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"

# === Format Status for IM ===
format_status() {
    local timestamp=$(get_timestamp)
    local cpu=$(get_cpu_usage)
    local mem=$(get_mem_usage)
    local disk=$(get_disk_usage)
    local gateway_status=$(check_gateway)
    local pid=$(get_gateway_pid)
    local uptime=$(get_uptime)
    
    # Progress bar helper
    bar() {
        local pct="$1"
        local filled=$((${pct%%.*} / 10))
        local empty=$((10 - filled))
        printf "█%.0s" $(seq 1 $filled 2>/dev/null) 2>/dev/null || true
        printf "░%.0s" $(seq 1 $empty 2>/dev/null) 2>/dev/null || true
    }
    
    # Status emoji
    cpu_emoji() { [[ $(echo "$cpu >= $TH_CPU_CRIT" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "🔴" || [[ $(echo "$cpu >= $TH_CPU_WARN" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "⚠️" || echo "✅"; }
    mem_emoji() { [[ $(echo "$mem >= $TH_MEM_CRIT" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "🔴" || [[ $(echo "$mem >= $TH_MEM_WARN" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "⚠️" || echo "✅"; }
    disk_emoji() { [[ $(echo "$disk >= $TH_DISK_CRIT" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "🔴" || [[ $(echo "$disk >= $TH_DISK_WARN" | bc -l 2>/dev/null || echo 0) -eq 1 ]] && echo "⚠️" || echo "✅"; }
    gw_emoji() { [[ "$gateway_status" = "up" ]] && echo "✅" || echo "❌"; }
    
    cat <<EOF
📊 **SysGuard 状态面板**
━━━━━━━━━━━━━━━━━━━━━━
🕐 $timestamp | $uptime
━━━━━━━━━━━━━━━━━━━━━━
CPU   $(bar $cpu) $(printf '%3s%%' "$cpu") $(cpu_emoji)
内存  $(bar $mem) $(printf '%3s%%' "$mem") $(mem_emoji)
磁盘  $(bar $disk) $(printf '%3s%%' "$disk") $(disk_emoji)
Gateway $(gw_emoji) $( [ "$gateway_status" = "up" ] && echo "运行中 (PID:$pid)" || echo "已停止" )
━━━━━━━━━━━━━━━━━━━━━━
EOF
}

export -f format_status
