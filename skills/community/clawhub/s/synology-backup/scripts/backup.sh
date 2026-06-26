#!/bin/bash
# Synology Backup — Incremental daily snapshot
# Usage: backup.sh [--dry-run]
#
# Resilience notes:
# - No set -euo pipefail — each path is attempted independently
# - Symlinks are dereferenced (--copy-links) to avoid I/O errors on SMB/NAS
# - rsync exit 23 (partial transfer) is treated as warning, not failure
# - rsync exit 24 (vanished files) is treated as success
# - Mount includes retry loop + health check
# - Failure alerts include per-path details

set -u  # Unset variable detection, but no -e (we handle errors per-path)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${SYNOLOGY_BACKUP_CONFIG:-$HOME/.openclaw/synology-backup.json}"
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_config "$CONFIG"

TIMESTAMP="$(date +%Y-%m-%d)"
BACKUP_DIR="$MOUNT/backups"
SNAP_DIR="$BACKUP_DIR/$TIMESTAMP"

# Build exclude args once for display in dry-run
mapfile -t EXCLUDE_ARGS < <(build_exclude_args)

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Transport:  $TRANSPORT"
    if [[ "$TRANSPORT" == "ssh" ]]; then
        echo "[DRY RUN] Destination: ${SSH_USER}@${SSH_HOST}:${SSH_DEST}/backups/$TIMESTAMP"
    else
        echo "[DRY RUN] Destination: $SNAP_DIR"
    fi
    echo "[DRY RUN] Paths:"
    while IFS= read -r path_raw; do
        path="$(echo "$path_raw" | sed "s|^~|$HOME|")"
        echo "  $path"
    done < <(jq -r '.backupPaths[]' "$CONFIG")
    if [[ "$INCLUDE_SUBAGENT" == "true" ]]; then
        for ws in "$HOME"/.openclaw/workspace-*/; do
            [[ -d "$ws" ]] || continue
            echo "  $ws (sub-agent)"
        done
    fi
    echo "[DRY RUN] Excludes: ${EXCLUDE_ARGS[*]}"
    echo "[DRY RUN] Retention: $RETENTION days (pre-restore: $PRE_RESTORE_RETENTION days)"
    exit 0
fi

# ---------------------------------------------------------------------------
# Tracking arrays for per-path success/failure reporting
# ---------------------------------------------------------------------------
backed_up=0
skipped=0
failed=0
failed_paths=()

# ---------------------------------------------------------------------------
# Mount with retry + health check
# ---------------------------------------------------------------------------
if ! ensure_mounted_with_retry; then
    send_telegram "⚠️ Synology backup FAILED on $(hostname) — could not mount NAS after 3 attempts"
    exit 1
fi

if [[ "$TRANSPORT" == "smb" ]]; then
    if ! mkdir -p -- "$SNAP_DIR"; then
        echo "❌ Failed to create snapshot directory: $SNAP_DIR" >&2
        send_telegram "⚠️ Synology backup FAILED on $(hostname) — could not create snapshot dir $SNAP_DIR (check NAS mount + permissions)"
        exit 1
    fi
    # Verify directory is actually writable before attempting rsync
    if ! touch -- "${SNAP_DIR}/.ping" 2>/dev/null; then
        echo "❌ Snapshot directory not writable: $SNAP_DIR" >&2
        send_telegram "⚠️ Synology backup FAILED on $(hostname) — snapshot dir not writable: $SNAP_DIR"
        exit 1
    fi
    rm -f -- "${SNAP_DIR}/.ping"
fi

# ---------------------------------------------------------------------------
# Helper: run rsync for a single path and handle exit codes
# Returns 0 on success/warning, 1 on hard failure
# ---------------------------------------------------------------------------
do_rsync() {
    local src="$1"
    local dest="$2"
    local name="$3"
    local rc=0

    if [[ "$TRANSPORT" == "ssh" ]]; then
        rsync -a --copy-links --delete \
            -e "ssh -p ${SSH_PORT} -o BatchMode=yes -o StrictHostKeyChecking=yes" \
            "${EXCLUDE_ARGS[@]}" -- \
            "$src" "$(remote_path "$dest")" || rc=$?
    else
        rsync -a --copy-links --delete \
            "${EXCLUDE_ARGS[@]}" -- \
            "$src" "$dest" || rc=$?
    fi

    case $rc in
        0)
            # Perfect success
            return 0
            ;;
        23)
            # Partial transfer — some files transferred, some had issues
            # This is non-fatal: better to have most files than none
            echo "⚠️  rsync warning (exit 23, partial transfer) for: $name"
            return 0
            ;;
        24)
            # Vanished files — source changed during transfer, benign
            echo "⚠️  rsync warning (exit 24, vanished files) for: $name"
            return 0
            ;;
        *)
            # Real failure
            echo "❌ rsync FAILED (exit $rc) for: $name" >&2
            return 1
            ;;
    esac
}

# ---------------------------------------------------------------------------
# Backup configured paths
# ---------------------------------------------------------------------------
while IFS= read -r path_raw; do
    path="$(echo "$path_raw" | sed "s|^~|$HOME|")"

    if [[ ! -e "$path" ]]; then
        echo "⚠️  Skipping (not found): $path"
        (( skipped++ )) || true
        continue
    fi

    name="$(basename -- "$path")"

    if [[ -d "$path" ]]; then
        if do_rsync "${path}/" "${SNAP_DIR}/${name}/" "$name"; then
            echo "✓ $name"
            (( backed_up++ )) || true
        else
            (( failed++ )) || true
            failed_paths+=("$name")
        fi
    else
        # Single file — use cp for local, rsync for SSH
        if [[ "$TRANSPORT" == "ssh" ]]; then
            if rsync -a --copy-links \
                -e "ssh -p ${SSH_PORT} -o BatchMode=yes -o StrictHostKeyChecking=yes" \
                -- "$path" "$(remote_path "backups/$TIMESTAMP/$name")" 2>/dev/null; then
                echo "✓ $name"
                (( backed_up++ )) || true
            else
                echo "❌ Failed to copy file: $name" >&2
                (( failed++ )) || true
                failed_paths+=("$name")
            fi
        else
            if rsync -a --copy-links \
                -- "$path" "${SNAP_DIR}/${name}" 2>/dev/null; then
                echo "✓ $name"
                (( backed_up++ )) || true
            else
                echo "❌ Failed to copy file: $name" >&2
                (( failed++ )) || true
                failed_paths+=("$name")
            fi
        fi
    fi
done < <(jq -r '.backupPaths[]' "$CONFIG")

# ---------------------------------------------------------------------------
# Backup sub-agent workspaces
# ---------------------------------------------------------------------------
if [[ "$INCLUDE_SUBAGENT" == "true" ]]; then
    for ws in "$HOME"/.openclaw/workspace-*/; do
        [[ -d "$ws" ]] || continue
        name="$(basename -- "$ws")"
        if ! [[ "$name" =~ ^workspace-[a-zA-Z0-9_-]+$ ]]; then
            echo "⚠️  Skipping suspicious workspace name: $name"
            continue
        fi
        if do_rsync "${ws}" "${SNAP_DIR}/${name}/" "$name"; then
            echo "✓ $name (sub-agent)"
            (( backed_up++ )) || true
        else
            (( failed++ )) || true
            failed_paths+=("$name")
        fi
    done
fi

# ---------------------------------------------------------------------------
# Total paths attempted
# ---------------------------------------------------------------------------
total_paths=$(( backed_up + skipped + failed ))

# ---------------------------------------------------------------------------
# Write manifest + compute checksum
# ---------------------------------------------------------------------------
if [[ "$TRANSPORT" == "smb" ]]; then
    MANIFEST_PATH="${SNAP_DIR}/manifest.json"
else
    MANIFEST_PATH="/tmp/backup-manifest-$TIMESTAMP.json"
fi

cat > "$MANIFEST_PATH" << MANIFEST
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "snapshot": "$TIMESTAMP",
  "host": "$(hostname)",
  "transport": "$TRANSPORT",
  "backed_up": $backed_up,
  "skipped": $skipped,
  "failed": $failed,
  "failed_paths": $(printf '%s\n' "${failed_paths[@]:-}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
}
MANIFEST

MANIFEST_CHECKSUM="$(md5sum "$MANIFEST_PATH" | cut -d' ' -f1)"

# Upload manifest for SSH transport
if [[ "$TRANSPORT" == "ssh" ]]; then
    rsync -a -e "ssh -p ${SSH_PORT} -o BatchMode=yes -o StrictHostKeyChecking=yes" \
        -- "$MANIFEST_PATH" "$(remote_path "backups/$TIMESTAMP/manifest.json")" 2>/dev/null || true
    rm -f -- "$MANIFEST_PATH"
fi

# ---------------------------------------------------------------------------
# Prune old daily snapshots (SMB only — SSH pruning would need ssh commands)
# ---------------------------------------------------------------------------
if [[ "$TRANSPORT" == "smb" ]]; then
    TRASH_DIR="$BACKUP_DIR/.trash"
    mkdir -p -- "$TRASH_DIR"
    while IFS= read -r old_snap; do
        [[ -z "$old_snap" ]] && continue
        if [[ "$old_snap" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            mv -- "${BACKUP_DIR}/${old_snap}" "${TRASH_DIR}/${old_snap}" 2>/dev/null \
                && echo "Pruned: $old_snap"
        fi
    done < <(ls -1 "$BACKUP_DIR" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r | tail -n +"$((RETENTION + 1))")

    # Prune pre-restore safety snapshots older than preRestoreRetention days
    while IFS= read -r pre_snap; do
        [[ -z "$pre_snap" ]] && continue
        snap_date="$(echo "$pre_snap" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)"
        if [[ -n "$snap_date" ]]; then
            snap_epoch="$(date -d "$snap_date" +%s 2>/dev/null || echo 0)"
            now_epoch="$(date +%s)"
            age_days="$(( (now_epoch - snap_epoch) / 86400 ))"
            if [[ "$age_days" -gt "$PRE_RESTORE_RETENTION" ]]; then
                mv -- "${BACKUP_DIR}/${pre_snap}" "${TRASH_DIR}/${pre_snap}" 2>/dev/null \
                    && echo "Pruned pre-restore: $pre_snap"
            fi
        fi
    done < <(ls -1 "$BACKUP_DIR" | grep -E '^pre-restore-' 2>/dev/null || true)

    # Clean trash older than 3 days
    find "$TRASH_DIR" -maxdepth 1 -mindepth 1 -mtime +3 -exec rm -rf -- {} + 2>/dev/null || true

    TOTAL_SIZE="$(du -sh -- "$SNAP_DIR" 2>/dev/null | cut -f1)"
    SNAP_COUNT="$(ls -1 "$BACKUP_DIR" | grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 2>/dev/null || echo 0)"
else
    TOTAL_SIZE="unknown"
    SNAP_COUNT="unknown"
fi

# ---------------------------------------------------------------------------
# Report results
# ---------------------------------------------------------------------------
echo ""
echo "Backup summary: $TIMESTAMP ($TOTAL_SIZE)"
echo "   ✅ $backed_up backed up | ⏭️  $skipped skipped | ❌ $failed failed"
if [[ ${#failed_paths[@]} -gt 0 ]]; then
    echo "   Failed paths: ${failed_paths[*]}"
fi
echo "   Snapshots: $SNAP_COUNT | Manifest checksum: $MANIFEST_CHECKSUM"

# ---------------------------------------------------------------------------
# Alerts and state
# ---------------------------------------------------------------------------
if [[ "$failed" -gt 0 ]]; then
    # Partial failure — some paths succeeded, some didn't
    failed_list="${failed_paths[*]}"
    send_telegram "⚠️ Synology backup PARTIAL on $(hostname) — $TIMESTAMP
${backed_up}/${total_paths} paths backed up, ${failed} failed: ${failed_list}
Skipped: ${skipped}"
    # Still write state if anything succeeded
    if [[ "$backed_up" -gt 0 ]]; then
        write_success_state "$TIMESTAMP" "$TOTAL_SIZE" "$MANIFEST_CHECKSUM"
    fi
    exit 1
elif [[ "$backed_up" -eq 0 && "$skipped" -gt 0 ]]; then
    # Nothing backed up but nothing failed either (all paths not found)
    send_telegram "⚠️ Synology backup WARNING on $(hostname) — $TIMESTAMP — all $skipped paths skipped (not found)"
    exit 0
else
    # Full success
    write_success_state "$TIMESTAMP" "$TOTAL_SIZE" "$MANIFEST_CHECKSUM"

    echo ""
    echo "✅ Backup complete: $TIMESTAMP ($TOTAL_SIZE)"

    if [[ "$NOTIFY_ON_SUCCESS" == "true" ]]; then
        send_telegram "✅ Synology backup complete — $TIMESTAMP ($TOTAL_SIZE, ${backed_up}/${total_paths} paths)"
    fi
    exit 0
fi
