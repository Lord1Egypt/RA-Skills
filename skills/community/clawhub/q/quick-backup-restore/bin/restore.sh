#!/bin/bash
# =============================================================================
# bin/restore.sh — Time Clawshine interactive restore helper
# Usage: sudo bin/restore.sh [snapshot_id] [--file path] [--target dir]
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Early --help (before sourcing lib.sh so it works without config) -------
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            echo "Usage: sudo bin/restore.sh [snapshot_id] [--file path] [--target dir]"
            echo ""
            echo "  snapshot_id   Restic snapshot ID, 'latest', or relative time ('2h ago', '1d ago', 'yesterday')"
            echo "  --file path   Restore only this file/directory"
            echo "  --target dir  Restore to this directory (default: /)"
            echo ""
            echo "Examples:"
            echo "  sudo bin/restore.sh                          # interactive"
            echo "  sudo bin/restore.sh latest                   # restore latest to /"
            echo "  sudo bin/restore.sh '2h ago'                 # restore closest to 2 hours ago"
            echo "  sudo bin/restore.sh yesterday                # restore closest to yesterday midnight"
            echo "  sudo bin/restore.sh abc123 --target /tmp/r   # restore snapshot to /tmp/r"
            echo "  sudo bin/restore.sh latest --file /root/.openclaw/workspace/MEMORY.md"
            exit 0
            ;;
    esac
done

source "$TC_ROOT/lib.sh"

tc_check_deps
tc_load_config

SNAPSHOT_ID=""
FILE_FILTER="${TC_FILE:-}"
TARGET="${TC_TARGET:-/}"

# --- Parse flags ------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --file)
            [[ $# -ge 2 ]] || { echo "ERROR: --file requires an argument"; exit 1; }
            FILE_FILTER="$2"; shift 2
            ;;
        --target)
            [[ $# -ge 2 ]] || { echo "ERROR: --target requires an argument"; exit 1; }
            TARGET="$2"; shift 2
            ;;
        -*) echo "Unknown flag: $1"; exit 1 ;;
        *)  SNAPSHOT_ID="$1"; shift ;;
    esac
done

echo "╔═════════════════════════════════════════════════════╗"
echo "║          Time Clawshine — Restore                ║"
echo "╚═════════════════════════════════════════════════════╝"
echo ""

# --- Show available snapshots -----------------------------------------------
echo "Available snapshots:"
echo ""
restic_cmd snapshots --compact
echo ""

# --- Pick snapshot interactively if not provided ----------------------------
if [[ -z "$SNAPSHOT_ID" ]]; then
    read -rp "Snapshot ID (or 'latest', '2h ago', 'yesterday'): " SNAPSHOT_ID
    [[ -z "$SNAPSHOT_ID" ]] && { echo "Aborted."; exit 0; }
fi

# --- Resolve relative time to closest snapshot ------------------------------
_resolve_time_snapshot() {
    local time_spec="$1"
    local target_ts

    case "$time_spec" in
        yesterday)
            target_ts=$(date -d "yesterday 00:00" '+%s' 2>/dev/null) || \
            target_ts=$(date -v-1d -j '+%s' 2>/dev/null) || \
            { echo "ERROR: Cannot parse 'yesterday' — use a snapshot ID instead"; exit 1; }
            ;;
        *h\ ago|*h)
            local hours="${time_spec%%h*}"
            target_ts=$(date -d "$hours hours ago" '+%s' 2>/dev/null) || \
            target_ts=$(date -v-"${hours}"H -j '+%s' 2>/dev/null) || \
            { echo "ERROR: Cannot parse '$time_spec'"; exit 1; }
            ;;
        *d\ ago|*d)
            local days="${time_spec%%d*}"
            target_ts=$(date -d "$days days ago" '+%s' 2>/dev/null) || \
            target_ts=$(date -v-"${days}"d -j '+%s' 2>/dev/null) || \
            { echo "ERROR: Cannot parse '$time_spec'"; exit 1; }
            ;;
        *)
            return 1  # not a time spec
            ;;
    esac

    # Find the snapshot closest to target_ts
    local best_id="" best_diff=999999999
    while IFS=$'\t' read -r sid stime; do
        local sts
        if ! sts=$(date -d "$stime" '+%s' 2>/dev/null); then
            sts=$(date -j -f '%Y-%m-%dT%H:%M:%S' "$stime" '+%s' 2>/dev/null) || continue
        fi
        local diff=$(( sts - target_ts ))
        [[ $diff -lt 0 ]] && diff=$(( -diff ))
        if [[ $diff -lt $best_diff ]]; then
            best_diff=$diff
            best_id="$sid"
        fi
    done < <(restic_cmd snapshots --json 2>/dev/null | jq -r '.[] | [.short_id, .time[:19]] | @tsv')

    if [[ -z "$best_id" ]]; then
        echo "ERROR: No snapshots found matching '$time_spec'"
        exit 1
    fi

    echo "  → Resolved '$time_spec' to snapshot $best_id (closest match, Δ ${best_diff}s)"
    SNAPSHOT_ID="$best_id"
}

# Check if SNAPSHOT_ID looks like a time expression
if [[ "$SNAPSHOT_ID" != "latest" ]] && [[ "$SNAPSHOT_ID" =~ (ago|yesterday|^[0-9]+[hd]$) ]]; then
    _resolve_time_snapshot "$SNAPSHOT_ID"
fi

# --- Build restore args -----------------------------------------------------
RESTORE_ARGS=(restore "$SNAPSHOT_ID" --target "$TARGET")
[[ -n "$FILE_FILTER" ]] && RESTORE_ARGS+=(--include "$FILE_FILTER")

echo ""
echo "Restore plan:"
echo "  Snapshot : $SNAPSHOT_ID"
echo "  Target   : $TARGET"
if [[ -n "$FILE_FILTER" ]]; then
    echo "  Scope    : $FILE_FILTER"
else
    echo "  Scope    : full snapshot"
fi
if [[ "$TARGET" == "/" ]]; then
    echo ""
    echo "WARNING: target is /. Existing files may be overwritten or reverted."
fi

# --- Dry run first ----------------------------------------------------------
echo ""
echo "==> Dry run preview:"
echo ""
DRY_RUN_OUTPUT=$(restic_cmd "${RESTORE_ARGS[@]}" --dry-run 2>&1)
DRY_RUN_LINES=$(wc -l <<< "$DRY_RUN_OUTPUT")
head -40 <<< "$DRY_RUN_OUTPUT"
if [[ $DRY_RUN_LINES -gt 40 ]]; then
    echo "  ... ($((DRY_RUN_LINES - 40)) more lines not shown)"
fi
echo ""

if [[ "$TARGET" == "/" ]]; then
    read -rp "Type RESTORE TO / to proceed: " CONFIRM
    [[ "$CONFIRM" == "RESTORE TO /" ]] || { echo "Aborted."; exit 0; }
else
    read -rp "Proceed with restore? [y/N]: " CONFIRM
    [[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi

# --- Real restore -----------------------------------------------------------
echo ""
echo "==> Restoring snapshot $SNAPSHOT_ID to $TARGET ..."

RESTORE_OUTPUT=$(restic_cmd "${RESTORE_ARGS[@]}" 2>&1)
RESTORE_EXIT=$?

if [[ $RESTORE_EXIT -ne 0 ]]; then
    echo ""
    echo "✗ Restore FAILED (exit $RESTORE_EXIT)"
    echo "$RESTORE_OUTPUT"
    log_error "Restore failed: snapshot=$SNAPSHOT_ID target=$TARGET exit=$RESTORE_EXIT"
    tg_failure "Restore failed (exit $RESTORE_EXIT):\nsnapshot=$SNAPSHOT_ID\ntarget=$TARGET\n\n$RESTORE_OUTPUT"
    exit 1
fi

echo ""
echo "✓ Restore complete."
[[ "$TARGET" != "/" ]] && echo "  Files restored to: $TARGET"

# Notify via Telegram if explicitly enabled. Keep external content minimal by
# default; snapshot/target details are local unless send_error_details is true.
log_info "Restore completed: snapshot=$SNAPSHOT_ID target=$TARGET"
HOST_LINE=$(_external_hostname_line)
DETAILS=""
if [[ "$PRIVACY_SEND_ERROR_DETAILS" == "true" ]]; then
    DETAILS=$'\nSnapshot: `'"$SNAPSHOT_ID"$'`\nTarget: `'"$TARGET"$'`'
fi
tg_send "🔄 *Time Clawshine — Restore complete*
${HOST_LINE}Time: $(timestamp)
Status: restore completed. Check local logs for details.${DETAILS}"
