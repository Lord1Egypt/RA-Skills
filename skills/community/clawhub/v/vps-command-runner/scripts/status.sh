#!/bin/bash
# Health check: uptime, load, disk, memory, docker across fleet
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"
load_inventory

REMOTE_CHECK='
echo "  Uptime: $(uptime -p)"
echo "  Load: $(cut -d" " -f1-3 /proc/loadavg)"
echo "  Disk: $(df -h / | awk "NR==2{print \$5\" used, \"\$4\" free\"}")"
echo "  Mem:  $(free -h | awk "/^Mem/{print \$3\"/\"\$2}")"
if command -v docker >/dev/null; then
    echo "  Docker containers: $(docker ps -q | wc -l) running"
else
    echo "  Docker: not installed"
fi
'

for HOST in "${HOSTS[@]}"; do
    echo "=== $HOST ==="
    if ssh "${SSH_OPTS[@]}" "$HOST" "$REMOTE_CHECK" 2>/dev/null; then
        :
    else
        echo "  ❌ Unreachable"
    fi
    echo
done
