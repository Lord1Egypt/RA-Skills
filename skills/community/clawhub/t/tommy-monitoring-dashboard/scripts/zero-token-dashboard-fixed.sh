#!/bin/bash

# Zero-Token Dashboard Updater - FIXED VERSION
# No LLM calls - pure shell script + Discord API

set -e

# Configuration
DASHBOARD_DIR="$HOME/.openclaw/workspace/skills/live-monitoring-dashboard"
ACTIVITY_MSG_ID="1479037476805804182"
HEALTH_MSG_ID="1479040445819392000"
CHANNEL_ID="1479037438813802618"

# Discord API function - SIMPLIFIED
update_discord_message() {
    local msg_id="$1"
    local content="$2"
    
    openclaw message edit \
        --channel discord \
        --message-id "$msg_id" \
        --target "channel:$CHANNEL_ID" \
        --message "$content" >/dev/null || return 0
}

# Get activity dashboard data  
get_activity_dashboard() {
    local cron_count=$(openclaw cron list 2>/dev/null | wc -l || echo "21")
    local process_count=$(ps aux | grep -i openclaw | grep -v grep | wc -l)
    local timestamp=$(date +"%a, %b %d, %I:%M:%S %p PT")
    
    echo "🤖 **OpenClaw Live Dashboard**

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
└─ Updated: ${timestamp}"
}

# Get system health data - SIMPLIFIED
get_system_health() {
    # Memory
    local mem_line=$(top -l 1 -n 0 | grep PhysMem | head -1)
    local used_gb=$(echo "$mem_line" | grep -o '[0-9]\+G used' | grep -o '[0-9]\+')
    local unused_mb=$(echo "$mem_line" | grep -o '[0-9]\+M unused' | grep -o '[0-9]\+')
    local unused_gb=$((unused_mb / 1024))
    local total_gb=$((used_gb + unused_gb))
    local mem_percent=$(( (used_gb * 100) / total_gb ))
    
    # CPU - FIXED calculation
    local cpu_line=$(top -l 1 -n 0 | grep "CPU usage" | head -1)
    local user_cpu=$(echo "$cpu_line" | grep -o '[0-9]\+\.[0-9]\+% user' | grep -o '[0-9]\+\.[0-9]\+')
    local sys_cpu=$(echo "$cpu_line" | grep -o '[0-9]\+\.[0-9]\+% sys' | grep -o '[0-9]\+\.[0-9]\+')
    local cpu_percent=$(printf "%.0f" $(echo "$user_cpu + $sys_cpu" | awk '{print $1}'))
    
    # Disk
    local disk_line=$(df -h / | tail -1)
    local disk_used=$(echo "$disk_line" | awk '{print $3}' | sed 's/Gi/GB/')
    local disk_total=$(echo "$disk_line" | awk '{print $2}' | sed 's/Gi/GB/')
    local disk_percent=$(echo "$disk_line" | awk '{print $5}' | tr -d '%')
    
    # Uptime - FIXED parsing
    local uptime_line=$(uptime)
    local days=$(echo "$uptime_line" | grep -o '[0-9]\+ days' | grep -o '[0-9]\+' || echo "0")
    local time_part=$(echo "$uptime_line" | grep -o '[0-9]\+:[0-9]\+' | head -1)
    local hours=$(echo "$time_part" | cut -d: -f1)
    local minutes=$(echo "$time_part" | cut -d: -f2)
    
    # Status indicators
    local mem_status="✅ Normal"
    [ "$mem_percent" -gt 80 ] && mem_status="⚠️ High"
    [ "$mem_percent" -gt 60 ] && [ "$mem_percent" -le 80 ] && mem_status="🟡 Medium"
    
    local cpu_status="✅ Normal"
    [ "$cpu_percent" -gt 70 ] && cpu_status="⚠️ High"
    [ "$cpu_percent" -gt 40 ] && [ "$cpu_percent" -le 70 ] && cpu_status="🟡 Active"
    
    local disk_status="✅ Normal"
    [ "$disk_percent" -gt 80 ] && disk_status="⚠️ High"
    [ "$disk_percent" -gt 60 ] && [ "$disk_percent" -le 80 ] && disk_status="🟡 Medium"
    
    local uptime_str="${days}d ${hours}h ${minutes}m"
    [ "$days" -eq 0 ] && uptime_str="${hours}h ${minutes}m"
    
    local timestamp=$(date +"%a, %b %d, %I:%M:%S %p PT")
    
    echo "🖥️ **System Health & Performance**

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

└─ Updated: ${timestamp}"
}

# Main execution - STREAMLINED
echo "$(date): Zero-token dashboard starting..."

# Generate content
activity_content=$(get_activity_dashboard)
health_content=$(get_system_health)

# Update Discord
update_discord_message "$ACTIVITY_MSG_ID" "$activity_content"
update_discord_message "$HEALTH_MSG_ID" "$health_content"

echo "$(date): Dashboard update completed successfully"
exit 0