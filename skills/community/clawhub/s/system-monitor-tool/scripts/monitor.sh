#!/bin/bash
# System Monitor - Resource monitoring
# Version: 1.0.0

# Get OS type
get_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        MINGW*|MSYS*|CYGWIN*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# System status overview
system_status() {
    local os=$(get_os)
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    echo "🖥️  System Status ($timestamp)"
    echo ""
    
    case "$os" in
        macos)
            # CPU
            local cpu=$(ps -A -o %cpu | awk '{s+=$1} END {print s / NR * 100}' | cut -d. -f1)
            local cores=$(sysctl -n hw.ncpu)
            echo "**CPU:** ${cpu}% ($cores cores)"
            
            # Memory
            local mem_used=$(vm_stat | awk '/Pages active/ {print $3}' | tr -d '.')
            local mem_total=$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024}')
            echo "**Memory:** ${mem_used}GB / ${mem_total}GB"
            
            # Disk
            df -h / | awk 'NR==2 {print "**Disk:** " $3 " / " $2 " (" $5 ")"}'
            
            # Uptime
            uptime | awk -F',' '{print "**Uptime:** " $1}' | sed 's/up/Uptime:/'
            ;;
            
        linux)
            # CPU
            local cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d% -f1)
            local cores=$(nproc)
            echo "**CPU:** ${cpu}% ($cores cores)"
            
            # Memory
            free -h | awk 'NR==2 {print "**Memory:** " $3 " / " $2 " (" $3/$2*100 "%)"}'
            
            # Disk
            df -h / | awk 'NR==2 {print "**Disk:** " $3 " / " $2 " (" $5 ")"}'
            
            # Uptime
            uptime -p 2>/dev/null || uptime | awk -F',' '{print "**Uptime:** " $1 $2}'
            ;;
            
        windows)
            echo "**OS:** Windows"
            echo "Note: Full monitoring requires PowerShell scripts"
            ;;
    esac
    
    echo ""
    echo "**Network:** $(check_network)"
}

# Check network status
check_network() {
    if ping -c 1 8.8.8.8 &>/dev/null; then
        echo "🟢 Connected"
    else
        echo "🔴 Disconnected"
    fi
}

# CPU details
cpu_info() {
    local os=$(get_os)
    
    echo "📊 CPU Information"
    echo ""
    
    case "$os" in
        macos)
            sysctl -n machdep.cpu.brand_string
            echo "Cores: $(sysctl -n hw.ncpu)"
            echo "Threads: $(sysctl -n hw.logicalcpu)"
            ;;
        linux)
            lscpu | grep -E "Model name|CPU\(s\)|Thread"
            ;;
    esac
    
    echo ""
    echo "Current Usage:"
    case "$os" in
        macos)
            top -l 1 | grep -E "CPU usage|Load Avg"
            ;;
        linux)
            top -bn1 | head -5
            ;;
    esac
}

# Memory details
memory_info() {
    local os=$(get_os)
    
    echo "📊 Memory Information"
    echo ""
    
    case "$os" in
        macos)
            vm_stat | head -10
            echo ""
            echo "Total: $(sysctl -n hw.memsize | awk '{printf "%.1f GB", $1/1024/1024/1024}')"
            ;;
        linux)
            free -h
            echo ""
            cat /proc/meminfo | head -10
            ;;
    esac
}

# Disk details
disk_info() {
    echo "📊 Disk Information"
    echo ""
    df -h
    echo ""
    echo "Top 5 largest folders in home:"
    du -sh ~/* 2>/dev/null | sort -hr | head -5
}

# Network details
network_info() {
    local os=$(get_os)
    
    echo "📊 Network Information"
    echo ""
    
    case "$os" in
        macos)
            ifconfig | grep -E "inet |flags" | head -20
            ;;
        linux)
            ip addr | grep -E "inet |state" | head -20
            ;;
    esac
    
    echo ""
    echo "Default Gateway:"
    netstat -rn | grep default | head -3
}

# Process list
process_list() {
    local top="${2:-10}"
    
    echo "📊 Top $top Processes by CPU"
    echo ""
    
    case "$(get_os)" in
        macos|linux)
            ps aux --sort=-%cpu | head -$((top + 1))
            ;;
    esac
}

# Temperature (if available)
temp_info() {
    local os=$(get_os)
    
    echo "📊 Temperature"
    echo ""
    
    case "$os" in
        linux)
            if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
                cat /sys/class/thermal/thermal_zone0/temp | awk '{printf "CPU: %.1f°C\n", $1/1000}'
            else
                echo "Temperature sensor not available"
            fi
            ;;
        macos)
            echo "Install iStats for temperature monitoring:"
            echo "  gem install iStats"
            ;;
    esac
}

# Watch mode
watch_mode() {
    local interval="${2:-5}"
    
    echo "Starting monitor (Ctrl+C to stop)..."
    while true; do
        clear
        system_status
        sleep "$interval"
    done
}

# Show help
show_help() {
    echo "System Monitor - Resource monitoring"
    echo ""
    echo "Usage:"
    echo "  monitor.sh status      - System overview"
    echo "  monitor.sh cpu         - CPU information"
    echo "  monitor.sh memory      - Memory information"
    echo "  monitor.sh disk        - Disk usage"
    echo "  monitor.sh network     - Network status"
    echo "  monitor.sh processes   - Top processes"
    echo "  monitor.sh temp        - Temperature"
    echo "  monitor.sh watch       - Continuous monitoring"
    echo ""
}

# Main
case "$1" in
    status)
        system_status
        ;;
    cpu)
        cpu_info
        ;;
    memory)
        memory_info
        ;;
    disk)
        disk_info
        ;;
    network)
        network_info
        ;;
    processes)
        process_list "$@"
        ;;
    temp)
        temp_info
        ;;
    watch)
        watch_mode "$@"
        ;;
    *)
        show_help
        ;;
esac
