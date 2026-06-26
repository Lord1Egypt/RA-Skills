#!/usr/bin/env bash
#===============================================================================
# Health Check Script
# Checks: CPU, Memory, Disk, Gateway, Process
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/util.sh"

# === Data Directory ===
DATA_DIR="$(dirname "${BASH_SOURCE[0]}")/../data"
HISTORY_DIR="$DATA_DIR/history"
mkdir -p "$HISTORY_DIR"

# === Run Health Check ===
run_health_check() {
    local timestamp=$(get_timestamp)
    local date_key=$(get_date_key)
    
    # Gather metrics
    local cpu=$(get_cpu_usage)
    local mem=$(get_mem_usage)
    local disk=$(get_disk_usage)
    local data_disk=$(get_data_disk_usage)
    local gateway=$(check_gateway)
    local pid=$(get_gateway_pid)
    local uptime=$(get_uptime)
    local load_avg=$(get_load_avg)
    local proc_count=$(get_process_count)
    
    # Check thresholds
    local cpu_status=$(check_threshold "$cpu" "$TH_CPU_WARN" "$TH_CPU_CRIT")
    local mem_status=$(check_threshold "$mem" "$TH_MEM_WARN" "$TH_MEM_CRIT")
    local disk_status=$(check_threshold "$disk" "$TH_DISK_WARN" "$TH_DISK_CRIT")
    
    # Build JSON record
    local json_record=$(cat <<EOF
{
  "timestamp": "$timestamp",
  "cpu": {"value": $cpu, "status": "$cpu_status"},
  "mem": {"value": $mem, "status": "$mem_status"},
  "disk": {"value": $disk, "status": "$disk_status"},
  "data_disk": {"value": $data_disk, "status": "normal"},
  "gateway": "$gateway",
  "pid": $pid,
  "uptime": "$uptime",
  "load_avg": "$load_avg",
  "processes": $proc_count
}
EOF
)
    
    # Save to history
    local history_file="$HISTORY_DIR/${date_key}.json"
    if [[ -f "$history_file" ]]; then
        # Append, remove trailing ] and add comma
        sed -i 's/\]$/,/' "$history_file" 2>/dev/null
        echo "  $json_record" >> "$history_file"
        echo "]" >> "$history_file"
    else
        echo "[ $json_record ]" > "$history_file"
    fi
    
    # Output for display
    cat <<EOF
SysGuard Health Check
========================================
Check Time: $timestamp
========================================

✅ CPU:    ${cpu}% $( [ "$cpu_status" = "normal" ] && echo "(正常)" || echo "(${cpu_status^^})" )
✅ 内存:    ${mem}% $( [ "$mem_status" = "normal" ] && echo "(正常)" || echo "(${mem_status^^})" )
✅ 系统盘:  ${disk}% $( [ "$disk_status" = "normal" ] && echo "(正常)" || echo "(${disk_status^^})" )
✅ 数据盘:  ${data_disk}% (正常)
✅ Gateway: $( [ "$gateway" = "up" ] && echo "运行中 (PID: $pid)" || echo "❌ 未运行" )

========================================
运行时长: $uptime
系统负载: $load_avg
进程数:   $proc_count
========================================
EOF
}

# === Export ===
export -f run_health_check
