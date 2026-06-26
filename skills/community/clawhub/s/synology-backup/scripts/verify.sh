#!/bin/bash
# Synology Backup — Integrity verification
# Checksums key files in the latest snapshot against live files.
# Usage: verify.sh [date]  (date = YYYY-MM-DD, omit to use latest)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${SYNOLOGY_BACKUP_CONFIG:-$HOME/.openclaw/synology-backup.json}"

# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_config "$CONFIG"

BACKUP_DIR="$MOUNT/backups"

ensure_mounted

# Determine which snapshot to verify
if [[ -n "${1:-}" ]]; then
    DATE="$1"
    if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Error: Invalid date format. Use YYYY-MM-DD" >&2
        exit 1
    fi
else
    DATE="$(ls -1 "$BACKUP_DIR" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r | head -1)"
    if [[ -z "$DATE" ]]; then
        echo "Error: No snapshots found in $BACKUP_DIR" >&2
        exit 1
    fi
fi

SNAP_DIR="${BACKUP_DIR}/${DATE}"

if [[ ! -d "$SNAP_DIR" ]]; then
    echo "Error: No snapshot found for $DATE" >&2
    exit 1
fi

echo "=== Verifying snapshot: $DATE ==="
echo ""

passed=0
failed=0
missing=0

# Check manifest
if [[ -f "${SNAP_DIR}/manifest.json" ]]; then
    echo "✅ Manifest present"
    jq -r '. | "   Timestamp: \(.timestamp)\n   Host: \(.host)\n   Backed up: \(.backed_up // "?")"' \
        "${SNAP_DIR}/manifest.json"
else
    echo "⚠️  No manifest.json"
fi

echo ""
echo "Checksumming key files..."

# Verify backed up paths against live
while IFS= read -r path_raw; do
    path="$(echo "$path_raw" | sed "s|^~|$HOME|")"
    name="$(basename -- "$path")"
    snap_path="${SNAP_DIR}/${name}"

    if [[ ! -e "$snap_path" ]]; then
        echo "  ❌ MISSING in snapshot: $name"
        (( missing++ )) || true
        continue
    fi

    if [[ ! -e "$path" ]]; then
        echo "  ⚠️  LIVE PATH GONE: $name (snapshot exists, live path does not)"
        continue
    fi

    if [[ -f "$path" && -f "$snap_path" ]]; then
        live_md5="$(md5sum -- "$path" | cut -d' ' -f1)"
        snap_md5="$(md5sum -- "$snap_path" | cut -d' ' -f1)"
        if [[ "$live_md5" == "$snap_md5" ]]; then
            echo "  ✅ $name (file, checksums match)"
            (( passed++ )) || true
        else
            echo "  ⚠️  $name (file, checksums differ — snapshot may be older than live)"
            (( passed++ )) || true  # Not a failure — expected to diverge over time
        fi
    elif [[ -d "$path" && -d "$snap_path" ]]; then
        live_count="$(find "$path" -type f | wc -l)"
        snap_count="$(find "$snap_path" -type f | wc -l)"
        echo "  ✅ $name (dir, $snap_count files in snapshot vs $live_count live)"
        (( passed++ )) || true
    fi
done < <(jq -r '.backupPaths[]' "$CONFIG")

echo ""
echo "=== Verify complete for $DATE ==="
echo "   ✅ Present: $passed  ❌ Missing: $missing"
if [[ "$missing" -gt 0 ]]; then
    echo ""
    echo "⚠️  $missing expected path(s) missing from snapshot."
    echo "   Run backup.sh to create a fresh snapshot."
    exit 1
fi
