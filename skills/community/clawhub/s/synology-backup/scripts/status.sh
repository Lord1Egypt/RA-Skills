#!/bin/bash
# Synology Backup — Status check
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${SYNOLOGY_BACKUP_CONFIG:-$HOME/.openclaw/synology-backup.json}"

# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_config "$CONFIG"

BACKUP_DIR="$MOUNT/backups"

echo "=== Synology Backup Status ==="
echo ""

# Check mount
if mountpoint -q "$MOUNT" 2>/dev/null; then
    echo "Mount:     ✅ $MOUNT → //${HOST}/${SHARE}"
else
    echo "Mount:     ❌ Not mounted — attempting..."
    mkdir -p -- "$MOUNT"
    if ensure_mounted 2>/dev/null; then
        echo "           ✅ Mounted successfully"
    else
        echo "           ❌ Mount failed — check host, share, and credentials"
        exit 1
    fi
fi

# Disk space
if mountpoint -q "$MOUNT" 2>/dev/null; then
    DISK_INFO="$(df -h -- "$MOUNT" | tail -1)"
    DISK_SIZE="$(echo "$DISK_INFO" | awk '{print $2}')"
    DISK_AVAIL="$(echo "$DISK_INFO" | awk '{print $4}')"
    DISK_PCT="$(echo "$DISK_INFO" | awk '{print $5}')"
    echo "Disk:      $DISK_AVAIL available of $DISK_SIZE ($DISK_PCT used)"
fi

# Last success from state file
LAST_SUCCESS="$(read_last_success)"
if [[ "$LAST_SUCCESS" == "never" ]]; then
    echo "Last backup: ⚠️  Never (or state file missing)"
else
    echo "Last backup: ✅ $LAST_SUCCESS"
fi
echo ""

# Snapshots
if [[ -d "$BACKUP_DIR" ]]; then
    SNAP_COUNT="$(ls -1 "$BACKUP_DIR" | grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 2>/dev/null || echo 0)"
    TOTAL_SIZE="$(du -sh -- "$BACKUP_DIR" 2>/dev/null | cut -f1)"

    echo "Snapshots: $SNAP_COUNT (retention: $RETENTION days)"
    echo "Total:     $TOTAL_SIZE"
    echo ""

    # Latest snapshot
    LATEST_NAME="$(ls -1 "$BACKUP_DIR" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r | head -1)"
    if [[ -n "$LATEST_NAME" ]]; then
        LATEST="${BACKUP_DIR}/${LATEST_NAME}"
        LATEST_SIZE="$(du -sh -- "$LATEST" 2>/dev/null | cut -f1)"

        if [[ -f "${LATEST}/manifest.json" ]]; then
            LATEST_TS="$(jq -r '.timestamp' "${LATEST}/manifest.json")"
            N_BACKED="$(jq -r '.backed_up // "?"' "${LATEST}/manifest.json")"
            echo "Latest:    $LATEST_NAME ($LATEST_SIZE) at $LATEST_TS [$N_BACKED paths]"
        else
            echo "Latest:    $LATEST_NAME ($LATEST_SIZE)"
        fi

        # Age check
        LATEST_EPOCH="$(date -d "$LATEST_NAME" +%s 2>/dev/null || echo 0)"
        NOW_EPOCH="$(date +%s)"
        AGE_HOURS="$(( (NOW_EPOCH - LATEST_EPOCH) / 3600 ))"

        if [[ "$AGE_HOURS" -gt 48 ]]; then
            echo "⚠️  WARNING: Last backup is ${AGE_HOURS}h old!"
        fi
    else
        echo "Latest:    None"
    fi

    echo ""
    echo "All snapshots:"
    while IFS= read -r snap_name; do
        [[ -z "$snap_name" ]] && continue
        size="$(du -sh -- "${BACKUP_DIR}/${snap_name}" 2>/dev/null | cut -f1)"
        echo "  $snap_name  $size"
    done < <(ls -1 "$BACKUP_DIR" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r)

    # Pre-restore safety snapshots
    PRE_SNAPS="$(ls -1 "$BACKUP_DIR" | grep -cE '^pre-restore-' 2>/dev/null || echo 0)"
    if [[ "$PRE_SNAPS" -gt 0 ]]; then
        echo ""
        echo "Pre-restore safety snapshots: $PRE_SNAPS"
        ls -1 "$BACKUP_DIR" | grep -E '^pre-restore-' | sort -r | while IFS= read -r snap; do
            size="$(du -sh -- "${BACKUP_DIR}/${snap}" 2>/dev/null | cut -f1)"
            echo "  $snap  $size"
        done
    fi
else
    echo "Snapshots: None (backup directory does not exist yet)"
fi
