#!/usr/bin/env bash
#===============================================================================
# Utility Library
#===============================================================================

# === JSON Escape ===
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/\\r}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# === Get CPU Usage ===
get_cpu_usage() {
    top -bn1 2>/dev/null | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 || echo "0"
}

# === Get Memory Usage ===
get_mem_usage() {
    free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}'
}

# === Get Disk Usage ===
get_disk_usage() {
    df / | tail -1 | awk '{print $5}' | tr -d '%'
}

# === Get Data Disk Usage ===
get_data_disk_usage() {
    if df "$DATA_DISK" &>/dev/null; then
        df "$DATA_DISK" | tail -1 | awk '{print $5}' | tr -d '%'
    else
        echo "0"
    fi
}

# === Check OpenClaw Gateway ===
check_gateway() {
    if openclaw gateway probe &>/dev/null; then
        echo "up"
    else
        echo "down"
    fi
}

# === Get Gateway PID ===
get_gateway_pid() {
    pgrep -f "openclaw.*gateway" 2>/dev/null | head -1 || echo "0"
}

# === Get System Uptime ===
get_uptime() {
    uptime -p 2>/dev/null || uptime
}

# === Get Load Average ===
get_load_avg() {
    uptime | awk -F'load average:' '{print $2}' | sed 's/^ //'
}

# === Get Process Count ===
get_process_count() {
    ps aux | wc -l
}

# === HTTP Probe with Timing ===
probe_http() {
    local url="$1"
    local timeout="${2:-5}"
    curl -sf -w "\n%{time_total}" --max-time "$timeout" "$url" 2>/dev/null | tail -1
}

# === Get Timestamp ===
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# === Get Date Key ===
get_date_key() {
    date '+%Y-%m-%d'
}

# === Threshold Check ===
check_threshold() {
    local value="$1"
    local warn="$2"
    local crit="$3"
    
    if (( $(echo "$value >= $crit" | bc -l 2>/dev/null || echo 0) )); then
        echo "critical"
    elif (( $(echo "$value >= $warn" | bc -l 2>/dev/null || echo 0) )); then
        echo "warning"
    else
        echo "normal"
    fi
}

# === Progress Bar ===
progress_bar() {
    local percent="$1"
    local total=10
    local filled=$((percent * total / 100))
    local empty=$((total - filled))
    
    printf "█%.0s" $(seq 1 $filled 2>/dev/null) 2>/dev/null || true
    printf "░%.0s" $(seq 1 $empty 2>/dev/null) 2>/dev/null || true
}
