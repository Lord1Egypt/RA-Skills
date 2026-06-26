#!/usr/bin/env bash
# Sentinal Redis — Full Health Check
# Usage: bash redis-health.sh [REDIS_URL]

set -euo pipefail

REDIS_URL="${1:-redis://localhost:6379}"
CLI="redis-cli -u $REDIS_URL"

# Mask credentials in URL for display (redis://:password@host → redis://***@host)
SAFE_URL=$(echo "$REDIS_URL" | sed -E 's|(://)[^@]*@|\1***@|')

divider() { echo "────────────────────────────────────────"; }
header() { echo ""; divider; echo "  $1"; divider; }
warn() { echo "  ⚠ WARNING: $1"; }
ok() { echo "  ✓ $1"; }

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     Sentinal Redis Health Report       ║"
echo "╚════════════════════════════════════════╝"
echo "  Target: $SAFE_URL"
echo "  Time:   $(date -u '+%Y-%m-%d %H:%M:%S UTC')"

# 1. Connectivity
header "CONNECTIVITY"
if $CLI ping 2>/dev/null | grep -q PONG; then
    ok "Redis is reachable"
else
    echo "  ✗ CRITICAL: Cannot connect to Redis at $SAFE_URL"
    exit 1
fi

# 2. Server Info
header "SERVER"
server_info=$($CLI info server 2>/dev/null)
version=$(echo "$server_info" | grep "redis_version:" | cut -d: -f2 | tr -d '\r')
uptime_days=$(echo "$server_info" | grep "uptime_in_days:" | cut -d: -f2 | tr -d '\r')
echo "  Version:    $version"
echo "  Uptime:     ${uptime_days} days"

# 3. Memory
header "MEMORY"
mem_info=$($CLI info memory 2>/dev/null)
used=$(echo "$mem_info" | grep "used_memory_human:" | cut -d: -f2 | tr -d '\r')
peak=$(echo "$mem_info" | grep "used_memory_peak_human:" | cut -d: -f2 | tr -d '\r')
rss=$(echo "$mem_info" | grep "used_memory_rss_human:" | cut -d: -f2 | tr -d '\r')
frag=$(echo "$mem_info" | grep "mem_fragmentation_ratio:" | cut -d: -f2 | tr -d '\r')
maxmem=$(echo "$mem_info" | grep "maxmemory_human:" | cut -d: -f2 | tr -d '\r')
policy=$(echo "$mem_info" | grep "maxmemory_policy:" | cut -d: -f2 | tr -d '\r')

echo "  Used:           $used"
echo "  Peak:           $peak"
echo "  RSS:            $rss"
echo "  Fragmentation:  $frag"
echo "  Max Memory:     ${maxmem:-not set}"
echo "  Eviction Policy: ${policy:-noeviction}"

# Memory warnings
frag_num=$(echo "$frag" | sed 's/[^0-9.]//g')
if [ -n "$frag_num" ]; then
    if awk "BEGIN {exit !($frag_num > 1.5)}"; then
        warn "High memory fragmentation ($frag) — consider restarting Redis"
    fi
    if awk "BEGIN {exit !($frag_num < 1.0)}"; then
        warn "Fragmentation < 1.0 — Redis may be swapping to disk!"
    fi
fi

# 4. Clients
header "CLIENTS"
client_info=$($CLI info clients 2>/dev/null)
connected=$(echo "$client_info" | grep "connected_clients:" | cut -d: -f2 | tr -d '\r')
blocked=$(echo "$client_info" | grep "blocked_clients:" | cut -d: -f2 | tr -d '\r')
echo "  Connected: $connected"
echo "  Blocked:   $blocked"

if [ "${connected:-0}" -gt 1000 ] 2>/dev/null; then
    warn "High client count ($connected) — check connection pooling"
fi
if [ "${blocked:-0}" -gt 0 ] 2>/dev/null; then
    warn "Blocked clients detected ($blocked) — check BLPOP/BRPOP consumers"
fi

# 5. Slow Log
header "SLOW QUERIES"
slowlog_len=$($CLI slowlog len 2>/dev/null | tr -d '\r')
echo "  Total slow queries recorded: $slowlog_len"

if [ "${slowlog_len:-0}" -gt 0 ] 2>/dev/null; then
    echo "  Last 3 slow queries:"
    $CLI slowlog get 3 2>/dev/null | head -20 | sed 's/^/    /'
fi

# 6. Keyspace
header "KEYSPACE"
$CLI info keyspace 2>/dev/null | grep "^db" | while IFS= read -r line; do
    echo "  $line"
done

# 7. BullMQ Queues
header "BULLMQ QUEUES"
queue_found=false

# Use scan to find bull queue meta keys
cursor=0
declare -a queues=()
while true; do
    result=$($CLI scan $cursor match "bull:*:meta" count 100 2>/dev/null)
    cursor=$(echo "$result" | head -1 | tr -d '\r')
    keys=$(echo "$result" | tail -n +2 | tr -d '\r')

    for key in $keys; do
        if [ -n "$key" ]; then
            queue_name=$(echo "$key" | sed 's/^bull:\(.*\):meta$/\1/')
            queues+=("$queue_name")
            queue_found=true
        fi
    done

    if [ "$cursor" = "0" ]; then
        break
    fi
done

if [ "$queue_found" = true ]; then
    printf "  %-30s %8s %8s %8s %8s %8s\n" "QUEUE" "WAIT" "ACTIVE" "DELAYED" "FAILED" "DONE"
    divider

    for q in "${queues[@]}"; do
        wait=$($CLI llen "bull:$q:wait" 2>/dev/null | tr -d '\r')
        active=$($CLI llen "bull:$q:active" 2>/dev/null | tr -d '\r')
        delayed=$($CLI zcard "bull:$q:delayed" 2>/dev/null | tr -d '\r')
        failed=$($CLI zcard "bull:$q:failed" 2>/dev/null | tr -d '\r')
        completed=$($CLI zcard "bull:$q:completed" 2>/dev/null | tr -d '\r')

        printf "  %-30s %8s %8s %8s %8s %8s\n" "$q" "${wait:-0}" "${active:-0}" "${delayed:-0}" "${failed:-0}" "${completed:-0}"

        # Warnings
        if [ "${wait:-0}" -gt 100 ] 2>/dev/null; then
            warn "Queue '$q' has $wait waiting jobs — possible backlog"
        fi
        if [ "${failed:-0}" -gt 10 ] 2>/dev/null; then
            warn "Queue '$q' has $failed failed jobs — inspect with: zrange bull:$q:failed 0 9"
        fi
    done
else
    echo "  No BullMQ queues found"
fi

# 8. Summary
header "SUMMARY"
has_warnings=false

if [ "${slowlog_len:-0}" -gt 100 ] 2>/dev/null; then
    warn "High slow query count — review slow log"
    has_warnings=true
fi

if [ "$has_warnings" = false ]; then
    ok "No critical issues detected"
fi

echo ""
echo "Report generated by Sentinal Redis v1.0.0"
echo ""
