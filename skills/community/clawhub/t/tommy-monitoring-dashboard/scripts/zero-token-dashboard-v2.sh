#!/bin/bash

# Zero-Token Dashboard Updater v2
# Uses Discord REST API directly via curl — no openclaw CLI dependency
# Works from any execution context (cron, exec, interactive)

set -e

# Configuration
DASHBOARD_DIR="$HOME/.openclaw/workspace/skills/live-monitoring-dashboard"
ACTIVITY_MSG_ID="1479037476805804182"
HEALTH_MSG_ID="1479040445819392000"
CHANNEL_ID="1479037438813802618"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# Extract Discord bot token from config
get_bot_token() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "ERROR: Config file not found: $CONFIG_FILE" >&2
        return 1
    fi
    jq -r '.channels.discord.token // empty' "$CONFIG_FILE"
}

BOT_TOKEN=$(get_bot_token)
if [ -z "$BOT_TOKEN" ]; then
    echo "$(date): ERROR — Could not extract Discord bot token" >&2
    exit 1
fi

# Discord REST API edit — direct PATCH, no CLI dependency
update_discord_message() {
    local msg_id="$1"
    local content="$2"

    # Escape content for JSON
    local json_content
    json_content=$(printf '%s' "$content" | jq -Rsa .)

    local response
    response=$(curl -s -w "\n%{http_code}" -X PATCH \
        "https://discord.com/api/v10/channels/${CHANNEL_ID}/messages/${msg_id}" \
        -H "Authorization: Bot ${BOT_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"content\": ${json_content}}")

    local http_code
    http_code=$(echo "$response" | tail -1)
    
    if [ "$http_code" != "200" ]; then
        echo "$(date): Discord edit failed for $msg_id (HTTP $http_code)" >&2
        echo "$response" | head -1 >&2
        return 1
    fi
}

# Gather activity dashboard data
get_activity_dashboard() {
    local cron_count
    cron_count=$(openclaw cron list 2>/dev/null | wc -l | tr -d ' ' || echo "?")
    local process_count
    process_count=$(ps aux | grep -i openclaw | grep -v grep | wc -l | tr -d ' ')
    local timestamp
    timestamp=$(date +"%a, %b %d, %I:%M:%S %p PT")

    cat <<EOF
🤖 **OpenClaw Live Dashboard**

👥 **Active Sessions: 1**
└─ Main Session (shell monitoring)

🔄 **Active Subagents: 0**
└─ All quiet

⏰ **Cron Jobs**
├─ Total active: ${cron_count}
└─ Recent:
   ├─ Pre-market research (active)
   ├─ Post-market review (active)
   ├─ Memory curation (active)
   ├─ Tesla monitoring (active)
   ├─ BP reminder (active)
   └─ Dashboard updates (active)

📊 **System**
├─ OpenClaw processes: ${process_count}
├─ Dashboard: 🟢 Shell-based (zero tokens)
└─ Updated: ${timestamp}
EOF
}

# Gather system health data
get_system_health() {
    # Memory
    local mem_line used_gb unused_mb total_gb mem_percent
    mem_line=$(top -l 1 -n 0 2>/dev/null | grep PhysMem | head -1)
    used_gb=$(echo "$mem_line" | grep -o '[0-9]\+G used' | grep -o '[0-9]\+')
    unused_mb=$(echo "$mem_line" | grep -o '[0-9]\+M unused' | grep -o '[0-9]\+')
    total_gb=$(( used_gb + unused_mb / 1024 ))
    [ "$total_gb" -eq 0 ] && total_gb=1
    mem_percent=$(( used_gb * 100 / total_gb ))

    # CPU
    local cpu_line user_cpu sys_cpu cpu_percent
    cpu_line=$(top -l 1 -n 0 2>/dev/null | grep "CPU usage" | head -1)
    user_cpu=$(echo "$cpu_line" | grep -o '[0-9]*\.[0-9]*% user' | grep -o '[0-9]*\.[0-9]*')
    sys_cpu=$(echo "$cpu_line"  | grep -o '[0-9]*\.[0-9]*% sys'  | grep -o '[0-9]*\.[0-9]*')
    cpu_percent=$(awk "BEGIN {printf \"%.0f\", ${user_cpu:-0} + ${sys_cpu:-0}}")

    # Disk
    local disk_line disk_used disk_total disk_percent
    disk_line=$(df -h / | tail -1)
    disk_used=$(echo  "$disk_line" | awk '{print $3}' | sed 's/Gi/GB/')
    disk_total=$(echo "$disk_line" | awk '{print $2}' | sed 's/Gi/GB/')
    disk_percent=$(echo "$disk_line" | awk '{print $5}' | tr -d '%')

    # Uptime
    local uptime_line days time_part hours minutes uptime_str
    uptime_line=$(uptime)
    days=$(echo "$uptime_line" | grep -o '[0-9]\+ days' | grep -o '[0-9]\+' || echo "0")
    time_part=$(echo "$uptime_line" | grep -o '[0-9]\+:[0-9]\+' | head -1)
    hours=$(echo "$time_part" | cut -d: -f1)
    minutes=$(echo "$time_part" | cut -d: -f2)
    uptime_str="${days}d ${hours}h ${minutes}m"
    [ "${days:-0}" -eq 0 ] && uptime_str="${hours}h ${minutes}m"

    # Status indicators
    local mem_status="✅ Normal" cpu_status="✅ Normal" disk_status="✅ Normal"
    [ "$mem_percent"  -gt 80 ] && mem_status="⚠️ High"
    [ "$mem_percent"  -gt 60 ] && [ "$mem_percent"  -le 80 ] && mem_status="🟡 Medium"
    [ "$cpu_percent"  -gt 70 ] && cpu_status="⚠️ High"
    [ "$cpu_percent"  -gt 40 ] && [ "$cpu_percent"  -le 70 ] && cpu_status="🟡 Active"
    [ "$disk_percent" -gt 80 ] && disk_status="⚠️ High"
    [ "$disk_percent" -gt 60 ] && [ "$disk_percent" -le 80 ] && disk_status="🟡 Medium"

    local timestamp
    timestamp=$(date +"%a, %b %d, %I:%M:%S %p PT")

    cat <<EOF
🖥️ **System Health & Performance**

💾 **Memory Usage**
├─ Used: ${used_gb}GB / ${total_gb}GB (${mem_percent}%)
└─ Status: ${mem_status}

⚡ **CPU Usage**
├─ Current: ${cpu_percent}%
└─ Status: ${cpu_status}

💿 **Disk Usage**
├─ Used: ${disk_used} / ${disk_total} (${disk_percent}%)
└─ Status: ${disk_status}

⏰ **System Uptime**
└─ ${uptime_str}

📈 **Performance Analytics**
└─ Available via \`performance-tracker.sh\`

└─ Updated: ${timestamp}
EOF
}

# --- Main ---
echo "$(date): Dashboard v2 starting..."

activity_content=$(get_activity_dashboard)
health_content=$(get_system_health)

update_discord_message "$ACTIVITY_MSG_ID" "$activity_content"
update_discord_message "$HEALTH_MSG_ID"   "$health_content"

echo "$(date): Dashboard v2 update complete"
exit 0
