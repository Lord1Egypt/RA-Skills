#!/bin/bash
# Synology Backup — Restore from snapshot
# Usage: restore.sh [date]  (date = YYYY-MM-DD, omit to list snapshots)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${SYNOLOGY_BACKUP_CONFIG:-$HOME/.openclaw/synology-backup.json}"

# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_config "$CONFIG"

BACKUP_DIR="$MOUNT/backups"

ensure_mounted

# No date given — list available snapshots
if [[ -z "${1:-}" ]]; then
    echo "Available snapshots:"
    echo ""
    while IFS= read -r snap_name; do
        [[ -z "$snap_name" ]] && continue
        snap="${BACKUP_DIR}/${snap_name}"
        size="$(du -sh -- "$snap" 2>/dev/null | cut -f1)"
        manifest="${snap}/manifest.json"
        if [[ -f "$manifest" ]]; then
            ts="$(jq -r '.timestamp' "$manifest")"
            n_backed="$(jq -r '.backed_up // "?"' "$manifest")"
            echo "  $snap_name  ($size)  $ts  [$n_backed paths]"
        else
            echo "  $snap_name  ($size)"
        fi
    done < <(ls -1 "$BACKUP_DIR" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r)
    echo ""
    echo "Usage: $0 <date>  (e.g., $0 2026-02-20)"
    exit 0
fi

DATE="$1"

# Strict date format validation (no injection possible with this pattern)
if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-02-20)" >&2
    exit 1
fi

SNAP_DIR="${BACKUP_DIR}/${DATE}"

if [[ ! -d "$SNAP_DIR" ]]; then
    echo "Error: No snapshot found for $DATE" >&2
    echo "Run without arguments to list available snapshots." >&2
    exit 1
fi

echo "⚠️  This will overwrite current files with snapshot from $DATE"
echo "   Source: $SNAP_DIR"
echo ""
read -r -p "Continue? [y/N] " confirm
if ! [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Pre-restore snapshot of current state
PRE_RESTORE_DATE="pre-restore-$(date +%Y-%m-%d-%H%M%S)"
PRE_SNAP="${BACKUP_DIR}/${PRE_RESTORE_DATE}"
echo ""
echo "Creating safety snapshot of current state → $PRE_RESTORE_DATE"
mkdir -p -- "$PRE_SNAP"

# Save current workspace and config (pre-restore safety net)
for src_dir in workspace cron agents; do
    if [[ -d "$HOME/.openclaw/${src_dir}" ]]; then
        rsync -a -- "$HOME/.openclaw/${src_dir}/" "${PRE_SNAP}/${src_dir}/"
        echo "  saved: $src_dir"
    fi
done
for src_file in openclaw.json .env; do
    if [[ -f "$HOME/.openclaw/${src_file}" ]]; then
        cp -- "$HOME/.openclaw/${src_file}" "${PRE_SNAP}/${src_file}"
        echo "  saved: $src_file"
    fi
done
cat > "${PRE_SNAP}/manifest.json" << MANIFEST
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "snapshot": "$PRE_RESTORE_DATE",
  "host": "$(hostname)",
  "note": "pre-restore safety snapshot before restoring from $DATE"
}
MANIFEST
echo "Safety snapshot complete."
echo ""

# Restore workspace
if [[ -d "${SNAP_DIR}/workspace" ]]; then
    rsync -a --delete -- "${SNAP_DIR}/workspace/" "$HOME/.openclaw/workspace/"
    echo "✓ workspace"
fi

# Restore sub-agent workspaces (explicit allowlist pattern)
for ws in "${SNAP_DIR}"/workspace-*/; do
    [[ -d "$ws" ]] || continue
    name="$(basename -- "$ws")"
    if ! [[ "$name" =~ ^workspace-[a-zA-Z0-9_-]+$ ]]; then
        echo "⚠️  Skipping suspicious workspace name: $name"
        continue
    fi
    rsync -a --delete -- "${ws}" "$HOME/.openclaw/${name}/"
    echo "✓ $name"
done

# Restore config files (explicit allowlist only)
for file in openclaw.json .env; do
    if [[ -f "${SNAP_DIR}/${file}" ]]; then
        cp -- "${SNAP_DIR}/${file}" "$HOME/.openclaw/${file}"
        echo "✓ $file"
    fi
done

# Restore directories (explicit allowlist only)
for dir in cron agents; do
    if [[ -d "${SNAP_DIR}/${dir}" ]]; then
        rsync -a --delete -- "${SNAP_DIR}/${dir}/" "$HOME/.openclaw/${dir}/"
        echo "✓ $dir"
    fi
done

echo ""
echo "✅ Restore complete from $DATE"
echo "   Safety snapshot saved as: $PRE_RESTORE_DATE (to undo this restore, run: $0 $PRE_RESTORE_DATE)"
echo "   Restart OpenClaw to apply config changes: openclaw gateway restart"
