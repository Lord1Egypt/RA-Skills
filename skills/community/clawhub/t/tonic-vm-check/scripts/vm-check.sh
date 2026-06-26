#!/bin/bash
# vm-check - Docker VM Resource Check Script
# Usage: bash vm-check.sh [section]
# Sections: all (default), system, containers, db, disk, cleanup
#
# Configure via environment variables:
#   VM_HOST   - VM IP or hostname (required)
#   VM_USER   - SSH username (default: ubuntu)
#   SSH_KEY   - Path to SSH private key (default: ~/.ssh/id_rsa)
#
# Example:
#   VM_HOST=10.0.0.1 VM_USER=ubuntu SSH_KEY=~/.ssh/mykey bash vm-check.sh
#   VM_HOST=10.0.0.1 bash vm-check.sh containers
#   VM_HOST=10.0.0.1 bash vm-check.sh cleanup

SSH_KEY="${SSH_KEY:-~/.ssh/id_rsa}"
VM_HOST="${VM_HOST:?VM_HOST is required. Set it via: VM_HOST=<host> bash vm-check.sh}"
VM_USER="${VM_USER:-ubuntu}"
SECTION="${1:-all}"

SSH_CMD="ssh -i $SSH_KEY -o StrictHostKeyChecking=no $VM_USER@$VM_HOST"

run_section() {
  local name="$1"
  local cmd="$2"
  echo "=== $name ==="
  $SSH_CMD "$cmd" 2>/dev/null
  echo ""
}

if [[ "$SECTION" == "all" || "$SECTION" == "system" ]]; then
  run_section "SYSTEM OVERVIEW" "
    echo '--- Uptime & Load ---'
    uptime
    echo ''
    echo '--- CPU (1s snapshot) ---'
    top -bn1 | grep '%Cpu'
    echo ''
    echo '--- Memory ---'
    free -h
  "
fi

if [[ "$SECTION" == "all" || "$SECTION" == "disk" ]]; then
  run_section "DISK USAGE" "df -h /"
fi

if [[ "$SECTION" == "all" || "$SECTION" == "containers" ]]; then
  run_section "DOCKER CONTAINERS (status)" "
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
  "
  run_section "DOCKER STATS (CPU/MEM snapshot, top 20 by MEM)" "
    docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}' \
    | (head -1; tail -n +2 | sort -t$'\t' -k3 -rh) | head -21
  "
fi

if [[ "$SECTION" == "all" || "$SECTION" == "docker-df" ]]; then
  run_section "DOCKER DISK USAGE" "docker system df"
fi

if [[ "$SECTION" == "all" || "$SECTION" == "db" ]]; then
  echo "=== MYSQL DB SIZES (all containers named *mysql*) ==="
  $SSH_CMD "
    for ctr in \$(docker ps --format '{{.Names}}' | grep -i mysql); do
      echo \"--- \$ctr ---\"
      # Try root with empty password first, then skip if no access
      docker exec \$ctr mysql -uroot --connect-expired-password \
        -e 'SELECT table_schema AS db, ROUND(SUM(data_length+index_length)/1024/1024,1) AS size_mb FROM information_schema.tables GROUP BY table_schema ORDER BY size_mb DESC;' 2>/dev/null \
        || echo '  (no root access without password — set MYSQL_ROOT_PASSWORD in container env)'
    done
  " 2>/dev/null
  echo ""
  echo "=== POSTGRES DB SIZES (all containers named *postgres*) ==="
  $SSH_CMD "
    for ctr in \$(docker ps --format '{{.Names}}' | grep -i postgres); do
      echo \"--- \$ctr ---\"
      docker exec \$ctr psql -U postgres -c \
        'SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC;' 2>/dev/null \
        || echo '  (could not connect as postgres user)'
    done
  " 2>/dev/null
  echo ""
fi

if [[ "$SECTION" == "cleanup" ]]; then
  echo "=== CLEANUP: Prune unused images + build cache ==="
  echo "WARNING: This removes unused images and all build cache."
  echo "Running in 3s... Ctrl+C to cancel."
  sleep 3
  echo ""
  echo "--- Pruning unused images ---"
  $SSH_CMD "docker image prune -af" 2>/dev/null
  echo ""
  echo "--- Pruning build cache ---"
  $SSH_CMD "docker builder prune -f" 2>/dev/null
  echo ""
  echo "--- After cleanup ---"
  $SSH_CMD "docker system df && df -h /"
fi
