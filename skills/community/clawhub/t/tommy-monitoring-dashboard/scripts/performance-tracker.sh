#!/bin/bash

# Performance Analytics & Alerts (Slice 4)
# Historical tracking and trend analysis for system metrics

set -e

# Configuration
DASHBOARD_DIR="$HOME/.openclaw/workspace/skills/live-monitoring-dashboard"
PERF_DATA_DIR="$DASHBOARD_DIR/data/performance"
ALERTS_LOG="$DASHBOARD_DIR/data/alerts.log"
CONFIG_FILE="$DASHBOARD_DIR/config/performance-config.json"

# Create directories
mkdir -p "$PERF_DATA_DIR"
mkdir -p "$(dirname "$ALERTS_LOG")"

# Default thresholds
DEFAULT_CPU_WARNING=70
DEFAULT_CPU_CRITICAL=85
DEFAULT_MEM_WARNING=75
DEFAULT_MEM_CRITICAL=90
DEFAULT_DISK_WARNING=80
DEFAULT_DISK_CRITICAL=95

# Load configuration with defaults
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        # Parse JSON config (simplified)
        CPU_WARNING=$(jq -r '.cpu_warning // 70' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_CPU_WARNING)
        CPU_CRITICAL=$(jq -r '.cpu_critical // 85' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_CPU_CRITICAL)
        MEM_WARNING=$(jq -r '.mem_warning // 75' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_MEM_WARNING)
        MEM_CRITICAL=$(jq -r '.mem_critical // 90' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_MEM_CRITICAL)
        DISK_WARNING=$(jq -r '.disk_warning // 80' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_DISK_WARNING)
        DISK_CRITICAL=$(jq -r '.disk_critical // 95' "$CONFIG_FILE" 2>/dev/null || echo $DEFAULT_DISK_CRITICAL)
    else
        # Use defaults
        CPU_WARNING=$DEFAULT_CPU_WARNING
        CPU_CRITICAL=$DEFAULT_CPU_CRITICAL
        MEM_WARNING=$DEFAULT_MEM_WARNING
        MEM_CRITICAL=$DEFAULT_MEM_CRITICAL
        DISK_WARNING=$DEFAULT_DISK_WARNING
        DISK_CRITICAL=$DEFAULT_DISK_CRITICAL
    fi
}

# Get current metrics
get_current_metrics() {
    local timestamp=$(date +%s)
    local human_time=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Memory
    local mem_line=$(top -l 1 -n 0 | grep PhysMem | head -1)
    local used_gb=$(echo "$mem_line" | grep -o '[0-9]\+G used' | grep -o '[0-9]\+')
    local unused_mb=$(echo "$mem_line" | grep -o '[0-9]\+M unused' | grep -o '[0-9]\+')
    local unused_gb=$((unused_mb / 1024))
    local total_gb=$((used_gb + unused_gb))
    local mem_percent=$(( (used_gb * 100) / total_gb ))
    
    # CPU
    local cpu_line=$(top -l 1 -n 0 | grep "CPU usage" | head -1)
    local user_cpu=$(echo "$cpu_line" | grep -o '[0-9]\+\.[0-9]\+% user' | grep -o '[0-9]\+\.[0-9]\+')
    local sys_cpu=$(echo "$cpu_line" | grep -o '[0-9]\+\.[0-9]\+% sys' | grep -o '[0-9]\+\.[0-9]\+')
    local cpu_percent=$(echo "$user_cpu + $sys_cpu" | bc 2>/dev/null | cut -d. -f1 || echo "0")
    
    # Disk
    local disk_line=$(df -h / | tail -1)
    local disk_percent=$(echo "$disk_line" | awk '{print $5}' | tr -d '%')
    
    # Store metrics
    echo "${timestamp},${human_time},${cpu_percent},${mem_percent},${disk_percent}" >> "$PERF_DATA_DIR/$(date +%Y-%m-%d).csv"
    
    echo "$timestamp|$human_time|$cpu_percent|$mem_percent|$disk_percent"
}

# Check for alerts
check_alerts() {
    local metrics="$1"
    local timestamp=$(echo "$metrics" | cut -d'|' -f1)
    local human_time=$(echo "$metrics" | cut -d'|' -f2)
    local cpu_percent=$(echo "$metrics" | cut -d'|' -f3)
    local mem_percent=$(echo "$metrics" | cut -d'|' -f4)
    local disk_percent=$(echo "$metrics" | cut -d'|' -f5)
    
    local alerts=""
    
    # CPU alerts
    if [[ $cpu_percent -ge $CPU_CRITICAL ]]; then
        alerts="$alerts🔴 CPU CRITICAL: ${cpu_percent}% (>=${CPU_CRITICAL}%)\n"
        echo "${timestamp},CRITICAL,CPU,${cpu_percent}%" >> "$ALERTS_LOG"
    elif [[ $cpu_percent -ge $CPU_WARNING ]]; then
        alerts="$alerts🟡 CPU WARNING: ${cpu_percent}% (>=${CPU_WARNING}%)\n"
        echo "${timestamp},WARNING,CPU,${cpu_percent}%" >> "$ALERTS_LOG"
    fi
    
    # Memory alerts
    if [[ $mem_percent -ge $MEM_CRITICAL ]]; then
        alerts="$alerts🔴 MEMORY CRITICAL: ${mem_percent}% (>=${MEM_CRITICAL}%)\n"
        echo "${timestamp},CRITICAL,MEMORY,${mem_percent}%" >> "$ALERTS_LOG"
    elif [[ $mem_percent -ge $MEM_WARNING ]]; then
        alerts="$alerts🟡 MEMORY WARNING: ${mem_percent}% (>=${MEM_WARNING}%)\n"
        echo "${timestamp},WARNING,MEMORY,${mem_percent}%" >> "$ALERTS_LOG"
    fi
    
    # Disk alerts
    if [[ $disk_percent -ge $DISK_CRITICAL ]]; then
        alerts="$alerts🔴 DISK CRITICAL: ${disk_percent}% (>=${DISK_CRITICAL}%)\n"
        echo "${timestamp},CRITICAL,DISK,${disk_percent}%" >> "$ALERTS_LOG"
    elif [[ $disk_percent -ge $DISK_WARNING ]]; then
        alerts="$alerts🟡 DISK WARNING: ${disk_percent}% (>=${DISK_WARNING}%)\n"
        echo "${timestamp},WARNING,DISK,${disk_percent}%" >> "$ALERTS_LOG"
    fi
    
    echo -e "$alerts"
}

# Get trend analysis
get_trends() {
    local today=$(date +%Y-%m-%d)
    local today_file="$PERF_DATA_DIR/${today}.csv"
    
    if [[ ! -f "$today_file" ]] || [[ ! -s "$today_file" ]]; then
        echo "No trend data available"
        return
    fi
    
    # Get last 10 entries for trend calculation
    local recent_data=$(tail -10 "$today_file")
    
    # Calculate averages
    local avg_cpu=$(echo "$recent_data" | awk -F',' '{sum+=$3; count++} END {if(count>0) print int(sum/count); else print 0}')
    local avg_mem=$(echo "$recent_data" | awk -F',' '{sum+=$4; count++} END {if(count>0) print int(sum/count); else print 0}')
    local avg_disk=$(echo "$recent_data" | awk -F',' '{sum+=$5; count++} END {if(count>0) print int(sum/count); else print 0}')
    
    # Get max values today
    local max_cpu=$(awk -F',' 'BEGIN{max=0} {if($3>max) max=$3} END{print max}' "$today_file")
    local max_mem=$(awk -F',' 'BEGIN{max=0} {if($4>max) max=$4} END{print max}' "$today_file")
    local max_disk=$(awk -F',' 'BEGIN{max=0} {if($5>max) max=$5} END{print max}' "$today_file")
    
    # Simple trend detection (last 5 vs previous 5)
    local last_5_cpu=$(echo "$recent_data" | tail -5 | awk -F',' '{sum+=$3} END {print int(sum/5)}')
    local prev_5_cpu=$(echo "$recent_data" | head -5 | awk -F',' '{sum+=$3} END {print int(sum/5)}')
    local cpu_trend="→"
    [[ $last_5_cpu -gt $((prev_5_cpu + 5)) ]] && cpu_trend="↗️"
    [[ $last_5_cpu -lt $((prev_5_cpu - 5)) ]] && cpu_trend="↘️"
    
    echo "📈 **Performance Trends (Last 10 samples)**
├─ CPU: Avg ${avg_cpu}% | Peak ${max_cpu}% | Trend ${cpu_trend}
├─ Memory: Avg ${avg_mem}% | Peak ${max_mem}% | Trend →
└─ Disk: Avg ${avg_disk}% | Peak ${max_disk}% | Trend →"
}

# Get recent alerts
get_recent_alerts() {
    local alert_count=0
    local recent_alerts=""
    
    if [[ -f "$ALERTS_LOG" ]]; then
        # Get alerts from last hour
        local hour_ago=$(($(date +%s) - 3600))
        recent_alerts=$(awk -F',' -v cutoff="$hour_ago" '$1 >= cutoff {print $2 " " $3 " " $4}' "$ALERTS_LOG" | tail -3)
        alert_count=$(echo "$recent_alerts" | grep -c . || echo "0")
    fi
    
    if [[ $alert_count -gt 0 ]]; then
        echo "🚨 **Active Alerts (Last hour)**"
        while IFS= read -r alert; do
            echo "├─ $alert"
        done <<< "$recent_alerts"
        echo ""
    else
        echo "✅ **No recent alerts**"
        echo ""
    fi
}

# Initialize config file if it doesn't exist
init_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << EOF
{
    "cpu_warning": $DEFAULT_CPU_WARNING,
    "cpu_critical": $DEFAULT_CPU_CRITICAL,
    "mem_warning": $DEFAULT_MEM_WARNING,
    "mem_critical": $DEFAULT_MEM_CRITICAL,
    "disk_warning": $DEFAULT_DISK_WARNING,
    "disk_critical": $DEFAULT_DISK_CRITICAL,
    "retention_days": 7
}
EOF
    fi
}

# Clean old data
cleanup_old_data() {
    local retention_days=$(jq -r '.retention_days // 7' "$CONFIG_FILE" 2>/dev/null || echo "7")
    find "$PERF_DATA_DIR" -name "*.csv" -mtime +$retention_days -delete 2>/dev/null || true
}

# Main function
main() {
    local action="${1:-track}"
    
    load_config
    init_config
    
    case "$action" in
        "track")
            local metrics=$(get_current_metrics)
            local alerts=$(check_alerts "$metrics")
            
            if [[ -n "$alerts" ]]; then
                echo "ALERTS DETECTED:"
                echo -e "$alerts"
            fi
            
            echo "Metrics logged: $metrics"
            ;;
        "trends")
            get_trends
            ;;
        "alerts")
            get_recent_alerts
            ;;
        "cleanup")
            cleanup_old_data
            echo "Old data cleaned up"
            ;;
        *)
            echo "Usage: $0 {track|trends|alerts|cleanup}"
            exit 1
            ;;
    esac
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi