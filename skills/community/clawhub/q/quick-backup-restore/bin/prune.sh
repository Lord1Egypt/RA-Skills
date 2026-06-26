#!/bin/bash
# =============================================================================
# bin/prune.sh — Time Clawshine manual repository cleanup
# Usage: sudo bin/prune.sh [options]
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Early --help (before sourcing lib.sh so it works without config) -------
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            echo "Usage: sudo bin/prune.sh [options]"
            echo ""
            echo "Options:"
            echo "  --keep-last N       Keep the last N snapshots (default: from config.yaml)"
            echo "  --older-than DURATION  Remove snapshots older than duration (e.g. 7d, 24h, 30d)"
            echo "  --dry-run           Show what would be removed without removing"
            echo "  --yes, -y           Skip confirmation prompt"
            echo ""
            echo "Examples:"
            echo "  sudo bin/prune.sh                     # use config retention"
            echo "  sudo bin/prune.sh --keep-last 24      # keep only last 24 snapshots"
            echo "  sudo bin/prune.sh --older-than 7d     # remove snapshots older than 7 days"
            echo "  sudo bin/prune.sh --dry-run            # preview without deleting"
            exit 0
            ;;
    esac
done

source "$TC_ROOT/lib.sh"

tc_check_deps
tc_load_config

# --- Parse flags ------------------------------------------------------------
KEEP_LAST_OVERRIDE=""
OLDER_THAN=""
DRY_RUN=false
ASSUME_YES=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep-last)
            [[ $# -ge 2 ]] || { echo "ERROR: --keep-last requires an argument"; exit 1; }
            KEEP_LAST_OVERRIDE="$2"; shift 2
            ;;
        --older-than)
            [[ $# -ge 2 ]] || { echo "ERROR: --older-than requires an argument (e.g. 7d, 24h)"; exit 1; }
            OLDER_THAN="$2"; shift 2
            ;;
        --dry-run)
            DRY_RUN=true; shift
            ;;
        --yes|-y)
            ASSUME_YES=true; shift
            ;;
        *) echo "Unknown flag: $1. Use --help for usage."; exit 1 ;;
    esac
done

if [[ -n "$KEEP_LAST_OVERRIDE" ]] && { ! [[ "$KEEP_LAST_OVERRIDE" =~ ^[0-9]+$ ]] || [[ "$KEEP_LAST_OVERRIDE" -le 0 ]]; }; then
    echo "ERROR: --keep-last must be a positive integer (got: $KEEP_LAST_OVERRIDE)"
    exit 1
fi

if [[ -n "$OLDER_THAN" ]] && ! [[ "$OLDER_THAN" =~ ^[0-9]+[smhdwMy]$ ]]; then
    echo "ERROR: --older-than must look like a restic duration (examples: 24h, 7d, 4w, 6M, 1y)"
    exit 1
fi

echo "╔═════════════════════════════════════════════════════╗"
echo "║        Time Clawshine — Repository Cleanup          ║"
echo "╚═════════════════════════════════════════════════════╝"
echo ""
echo "  WARNING: cleanup can permanently remove old recovery points."
echo "  A dry-run preview is shown before any deletion unless --dry-run is used."
echo ""

# --- Show current state -----------------------------------------------------
SNAP_COUNT=$(restic_cmd snapshots --json 2>/dev/null | jq 'length' 2>/dev/null || echo "?")
REPO_SIZE="?"
[[ -d "$REPO" ]] && REPO_SIZE=$(du -sh "$REPO" 2>/dev/null | awk '{print $1}' || echo "?")

echo "  Current snapshots : $SNAP_COUNT"
echo "  Repository size   : $REPO_SIZE"
echo ""

# --- Build forget args ------------------------------------------------------
FORGET_ARGS=(forget)

if [[ -n "$OLDER_THAN" ]]; then
    # Parse duration: convert to restic format
    FORGET_ARGS+=(--keep-within "$OLDER_THAN")
    echo "  Policy            : remove snapshots older than $OLDER_THAN"
elif [[ -n "$KEEP_LAST_OVERRIDE" ]]; then
    FORGET_ARGS+=(--keep-last "$KEEP_LAST_OVERRIDE")
    echo "  Policy            : keep last $KEEP_LAST_OVERRIDE snapshots"
else
    FORGET_ARGS+=(--keep-last "$KEEP_LAST")
    echo "  Policy            : keep last $KEEP_LAST snapshots (from config.yaml)"
fi

FORGET_ARGS+=(--prune)

if [[ "$DRY_RUN" == "true" ]]; then
    FORGET_ARGS+=(--dry-run)
    echo "  Mode              : DRY RUN (no changes will be made)"
fi

echo ""

# --- Dry-run preview --------------------------------------------------------
if [[ "$DRY_RUN" != "true" ]]; then
    echo "==> Preview (dry run):"
    echo ""
    PREVIEW_TMP=$(mktemp)
    restic_cmd "${FORGET_ARGS[@]}" --dry-run > "$PREVIEW_TMP" 2>&1 || true
    head -30 "$PREVIEW_TMP"
    PREVIEW_LINES=$(wc -l < "$PREVIEW_TMP")
    [[ $PREVIEW_LINES -gt 30 ]] && echo "  ... ($((PREVIEW_LINES - 30)) more lines)"
    rm -f "$PREVIEW_TMP"
    echo ""

    # --- Confirm ----------------------------------------------------------------
    if [[ "$ASSUME_YES" != "true" ]]; then
        read -rp "Proceed with cleanup? [y/N]: " CONFIRM
        [[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
    fi
fi

# --- Execute ----------------------------------------------------------------
echo ""
echo "==> Running cleanup..."
PRUNE_TMP=$(mktemp)
restic_cmd "${FORGET_ARGS[@]}" > "$PRUNE_TMP" 2>&1
PRUNE_EXIT=$?

if [[ $PRUNE_EXIT -ne 0 ]]; then
    echo "ERROR: Prune failed (exit $PRUNE_EXIT)"
    cat "$PRUNE_TMP"
    log_error "prune.sh: restic forget/prune failed (exit $PRUNE_EXIT)"
    PRUNE_ERR=$(cat "$PRUNE_TMP")
    tg_failure "prune.sh: restic forget/prune failed (exit $PRUNE_EXIT):\n\n$PRUNE_ERR"
    rm -f "$PRUNE_TMP"
    exit 1
fi

head -30 "$PRUNE_TMP"
rm -f "$PRUNE_TMP"
echo ""

# --- Report -----------------------------------------------------------------
NEW_SNAP_COUNT=$(restic_cmd snapshots --json 2>/dev/null | jq 'length' 2>/dev/null || echo "?")
NEW_REPO_SIZE="?"
[[ -d "$REPO" ]] && NEW_REPO_SIZE=$(du -sh "$REPO" 2>/dev/null | awk '{print $1}' || echo "?")

if [[ "$DRY_RUN" == "true" ]]; then
    echo "✓ Dry run complete — no changes made."
else
    echo "✓ Cleanup complete."
    echo "  Snapshots : $SNAP_COUNT → $NEW_SNAP_COUNT"
    echo "  Repo size : $REPO_SIZE → $NEW_REPO_SIZE"
    log_info "prune.sh: cleanup done — snapshots $SNAP_COUNT→$NEW_SNAP_COUNT, size $REPO_SIZE→$NEW_REPO_SIZE"
    HOST_LINE=$(_external_hostname_line)
    DETAILS=""
    if [[ "$PRIVACY_SEND_ERROR_DETAILS" == "true" ]]; then
        DETAILS=$'\nSnapshots: '"$SNAP_COUNT -> $NEW_SNAP_COUNT"$'\nRepository size: '"$REPO_SIZE -> $NEW_REPO_SIZE"
    fi
    tg_send "🧹 *Time Clawshine — Cleanup complete*
${HOST_LINE}Status: repository cleanup completed. Check local logs for details.${DETAILS}"
fi
