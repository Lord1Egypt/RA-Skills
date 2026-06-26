#!/bin/bash
# Nova Snapshot Tool - 状态快照管理
# 用法: snapshot.sh create <描述> <目标路径>
#        snapshot.sh cleanup

SNAP_DIR="/tmp/nova-snapshots"

create_snapshot() {
    local desc="${1:-unnamed}"
    local target="${2:-.}"
    
    mkdir -p "$SNAP_DIR"
    local stamp=$(date +%s)
    local snap_path="$SNAP_DIR/${stamp}_${desc}"
    
    if [ -e "$target" ]; then
        cp -r "$target" "$snap_path" 2>/dev/null
        echo "[$(date '+%H:%M:%S')] snapshot created: $snap_path"
        
        # 保留最近3个
        ls -dt "$SNAP_DIR"/*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null
        echo "[$(date '+%H:%M:%S')] cleanup complete (kept last 3)"
    else
        echo "[$(date '+%H:%M:%S')] target not found: $target"
        return 1
    fi
}

cleanup_snapshots() {
    [ -d "$SNAP_DIR" ] || { echo "no snapshots to clean"; return 0; }
    local removed=$(find "$SNAP_DIR" -maxdepth 1 -type d -mmin +1440 -exec rm -rf {} \; 2>/dev/null | wc -l)
    echo "[$(date '+%H:%M:%S')] cleaned $removed old snapshots (>24h)"
}

case "${1:-}" in
    create)  create_snapshot "$2" "$3" ;;
    cleanup)  cleanup_snapshots ;;
    list)    ls -lt "$SNAP_DIR" 2>/dev/null || echo "no snapshots" ;;
    *)       echo "Usage: snapshot.sh create <desc> <target> | cleanup | list" ;;
esac
