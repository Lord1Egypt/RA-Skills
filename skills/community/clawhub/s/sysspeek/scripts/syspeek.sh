#!/bin/sh
# syspeek — compact system health dashboard

# Uptime (human-readable)
UPTIME=$(uptime -p 2>/dev/null || uptime)

# Load average
LOAD=$(cut -d' ' -f1-3 /proc/loadavg 2>/dev/null || echo "N/A")
CORES=$(nproc 2>/dev/null || echo "?")

# Memory: used / total (%)
MEM_TOTAL=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{printf "%.0f", $2/1024/1024}')
MEM_AVAIL=$(grep MemAvailable /proc/meminfo 2>/dev/null | awk '{printf "%.0f", $2/1024/1024}')
if [ -n "$MEM_TOTAL" ] && [ -n "$MEM_AVAIL" ]; then
    MEM_USED=$(echo "$MEM_TOTAL $MEM_AVAIL" | awk '{printf "%.1f", $1-$2}')
    MEM_PCT=$(echo "$MEM_TOTAL $MEM_AVAIL" | awk '{printf "%.0f", ($1-$2)/$1*100}')
    MEM_STR="${MEM_USED}G / ${MEM_TOTAL}G (${MEM_PCT}%)"
else
    MEM_STR="N/A"
fi

# Disk: used / total for root (%)
DISK=$(df -h / 2>/dev/null | tail -1 | awk '{print $3 " / " $2 " (" $5 ")"}' || echo "N/A")

# Top TCP listening ports
PORTS=$(ss -tln 2>/dev/null | grep LISTEN | awk '{print $4}' | sed 's/.*://' | sort -n | uniq | tr '\n' ',' | sed 's/,$//' | cut -c1-40)
[ -z "$PORTS" ] && PORTS="none"

# Trim uptime prefix
UPTIME=$(echo "$UPTIME" | sed 's/up /up /' | cut -c1-50)

# Output
echo ""
echo "╔══════════════════════════════════════╗"
echo "║           SYSTEM PEEK                ║"
echo "╠══════════════════════════════════════╣"
printf "║ %-10s │ %-28s ║\n" "uptime"   "$UPTIME"
printf "║ %-10s │ %-28s ║\n" "load"     "$LOAD (1/$CORES)"
printf "║ %-10s │ %-28s ║\n" "memory"   "$MEM_STR"
printf "║ %-10s │ %-28s ║\n" "disk /"   "$DISK"
printf "║ %-10s │ %-28s ║\n" "tcp ports" "$PORTS"
echo "╚══════════════════════════════════════╝"
echo ""
