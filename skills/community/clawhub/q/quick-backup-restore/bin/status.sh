#!/bin/bash
# =============================================================================
# bin/status.sh — Time Clawshine health check
# Run: sudo bin/status.sh
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Early --help (before sourcing lib.sh so it works without config) -------
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            echo "Usage: sudo bin/status.sh"
            echo ""
            echo "Shows: version, snapshots, repo size, disk free, password file,"
            echo "       scheduler status, integrity check counter, update availability,"
            echo "       and recent log lines."
            exit 0
            ;;
    esac
done

source "$TC_ROOT/lib.sh"

tc_check_deps
tc_load_config

VERSION=$(tc_current_version)

echo "╔═════════════════════════════════════════════════╗"
echo "║          Time Clawshine — Status                ║"
echo "╚═════════════════════════════════════════════════╝"
echo ""

# --- Version ----------------------------------------------------------------
echo "  Version         : $VERSION"

# --- Repository info --------------------------------------------------------
echo "  Repository      : $REPO"

if restic_cmd snapshots &>/dev/null; then
    SNAP_JSON=$(restic_cmd snapshots --json 2>/dev/null || echo "[]")
    SNAP_COUNT=$(echo "$SNAP_JSON" | jq 'length' 2>/dev/null || echo "?")
    LAST_SNAP=$(echo "$SNAP_JSON" | jq -r '.[-1].time // "none"' 2>/dev/null | cut -d'.' -f1 | tr 'T' ' ')
    echo "  Snapshots       : $SNAP_COUNT"
    echo "  Last snapshot   : $LAST_SNAP"

    # Repo size (stats can be slow on large repos, so we use du as fallback)
    if [[ -d "$REPO" ]]; then
        REPO_SIZE=$(du -sh "$REPO" 2>/dev/null | awk '{print $1}')
        echo "  Repo size       : $REPO_SIZE"
    fi
else
    echo "  Snapshots       : (repository not initialized)"
fi

# --- Disk space -------------------------------------------------------------
if [[ -d "$REPO" ]]; then
    REPO_DIR=$(dirname "$REPO")
    DISK_FREE=$(df -h "$REPO_DIR" 2>/dev/null | awk 'NR==2{print $4}')
    DISK_USED_PCT=$(df -h "$REPO_DIR" 2>/dev/null | awk 'NR==2{print $5}')
    echo "  Disk free       : $DISK_FREE (${DISK_USED_PCT} used)"
    if [[ "$MIN_DISK_MB" -gt 0 ]] 2>/dev/null; then
        echo "  Min disk guard  : ${MIN_DISK_MB}MB"
    fi
fi

# --- Privacy / egress -------------------------------------------------------
echo ""
echo "  Privacy         : local_only=$PRIVACY_LOCAL_ONLY, error_details=$PRIVACY_SEND_ERROR_DETAILS, hostname=$PRIVACY_INCLUDE_HOSTNAME"
echo "  External egress : telegram=$TG_ENABLED, healthcheck=$HC_ENABLED, update_check=$UPDATE_CHECK"

# --- Password file ----------------------------------------------------------
echo ""
if [[ -f "$PASS_FILE" ]]; then
    PASS_PERMS=$(stat -c '%a' "$PASS_FILE" 2>/dev/null || stat -f '%Lp' "$PASS_FILE" 2>/dev/null || echo "?")
    echo "  Password file   : $PASS_FILE (mode $PASS_PERMS)"
    echo "  ⚠  Back this up separately — without it, no restore is possible."
else
    echo "  Password file   : $PASS_FILE (NOT FOUND — CRITICAL)"
fi

# --- Scheduler (systemd preferred, cron fallback) --------------------------
echo ""
CRON_FILE="/etc/cron.d/time-clawshine"
if command -v systemctl &>/dev/null && systemctl is-active time-clawshine.timer &>/dev/null 2>&1; then
    TIMER_SCHED=$(systemctl show time-clawshine.timer --property=TimersCalendar 2>/dev/null | head -1 || echo "?")
    echo "  Scheduler       : systemd timer (active)"
    echo "  Timer           : $TIMER_SCHED"
elif [[ -f "$CRON_FILE" ]]; then
    echo "  Scheduler       : cron"
    echo "  Cron job        : $CRON_FILE"
    echo "  Schedule        : $CRON_EXPR"
else
    echo "  Scheduler       : not installed (run setup.sh to register)"
fi

# --- Integrity check --------------------------------------------------------
if [[ "$CHECK_EVERY" -gt 0 ]] 2>/dev/null; then
    COUNTER_FILE="/var/tmp/time-clawshine-check-counter"
    if [[ -f "$COUNTER_FILE" ]]; then
        COUNTER=$(cat "$COUNTER_FILE" 2>/dev/null || echo "?")
        echo "  Integrity check : every $CHECK_EVERY backups (counter: $COUNTER)"
    else
        echo "  Integrity check : every $CHECK_EVERY backups (counter not started)"
    fi
else
    echo "  Integrity check : disabled"
fi

# --- Update check -----------------------------------------------------------
if [[ "$UPDATE_CHECK" == "true" ]]; then
    tc_check_update "$VERSION"
    case "$TC_UPDATE_STATE" in
        newer)
            echo "  Update          : v$TC_UPDATE_VERSION available (current: v$VERSION)"
            echo "                    Run: clawhub update quick-backup-restore"
            ;;
        uptodate)
            echo "  Update          : up to date (v$VERSION)"
            ;;
        *)
            echo "  Update          : could not check — $TC_UPDATE_ERROR"
            ;;
    esac
else
    echo "  Update check    : disabled"
fi

# --- Recent log --------------------------------------------------------------
echo ""
echo "  --- Last 10 log lines ---"
if [[ -f "$LOG_FILE" ]]; then
    tail -10 "$LOG_FILE" | sed 's/^/  /'
else
    echo "  (no log file found)"
fi

echo ""
