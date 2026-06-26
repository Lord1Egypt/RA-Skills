#!/bin/bash
# =============================================================================
# bin/uninstall.sh — Time Clawshine clean removal
# Removes all system artifacts created by setup.sh.
# Usage: sudo bin/uninstall.sh [options]
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$TC_ROOT/lib.sh"

# --- Parse flags ------------------------------------------------------------
ASSUME_YES=false
PURGE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --yes|-y)   ASSUME_YES=true; shift ;;
        --purge)    PURGE=true; shift ;;
        --help|-h)
            echo "Usage: sudo bin/uninstall.sh [options]"
            echo ""
            echo "Options:"
            echo "  --yes, -y    Skip confirmation prompts (removes system files, preserves data)"
            echo "  --purge      Also remove repository, password file, and logs (DESTRUCTIVE)"
            echo "  --help, -h   Show this help"
            echo ""
            echo "What gets removed by default:"
            echo "  - Systemd timer + service (time-clawshine.timer/service)"
            echo "  - Installed binary (/usr/local/bin/time-clawshine + symlink)"
            echo "  - Cron job (/etc/cron.d/time-clawshine)"
            echo "  - Logrotate config (/etc/logrotate.d/time-clawshine)"
            echo "  - Lock and marker files (/var/lock/, /var/tmp/)"
            echo ""
            echo "What is preserved (unless --purge):"
            echo "  - Backup repository (your snapshots)"
            echo "  - Password file (encryption key)"
            echo "  - Log file"
            echo "  - config.yaml and skill source files"
            exit 0
            ;;
        *) echo "Unknown flag: $1. Use --help for usage."; exit 1 ;;
    esac
done

# Must run as root
[[ $EUID -eq 0 ]] || { echo "ERROR: Run as root (sudo bin/uninstall.sh)"; exit 1; }

# Load config to get paths
tc_load_config 2>/dev/null || true

echo "╔═════════════════════════════════════════════════════╗"
echo "║        Time Clawshine — Uninstall                    ║"
echo "╚═════════════════════════════════════════════════════╝"
echo ""

# --- Show what will be removed -----------------------------------------------
echo "  The following will be removed:"
echo ""

REMOVABLE=()

# Systemd units
if systemctl is-active time-clawshine.timer &>/dev/null 2>&1 || [[ -f "/etc/systemd/system/time-clawshine.timer" ]]; then
    echo "    - Systemd timer:    time-clawshine.timer (active)"
    echo "    - Systemd service:  time-clawshine.service"
    REMOVABLE+=("systemd")
fi

# Binary (v3 name + v2 backward-compat symlink)
for bin_file in "/usr/local/bin/time-clawshine" "/usr/local/bin/quick-backup-restore"; do
    [[ -f "$bin_file" || -L "$bin_file" ]] && echo "    - Binary:           $bin_file" && REMOVABLE+=("binary:$bin_file")
done

# Cron (v3 or legacy v2)
for cron_file in "/etc/cron.d/time-clawshine" "/etc/cron.d/quick-backup-restore"; do
    [[ -f "$cron_file" ]] && echo "    - Cron job:         $cron_file" && REMOVABLE+=("cron:$cron_file")
done

# Logrotate (v3 or legacy v2)
for lr_file in "/etc/logrotate.d/time-clawshine" "/etc/logrotate.d/quick-backup-restore"; do
    [[ -f "$lr_file" ]] && echo "    - Logrotate:        $lr_file" && REMOVABLE+=("logrotate:$lr_file")
done

# Lock file
for lock_file in "/var/lock/time-clawshine.lock" "/var/lock/quick-backup-restore.lock"; do
    [[ -f "$lock_file" ]] && echo "    - Lock file:        $lock_file" && REMOVABLE+=("lock:$lock_file")
done

# Marker files
for marker in /var/tmp/time-clawshine-* /var/tmp/quick-backup-restore-*; do
    [[ -f "$marker" ]] && echo "    - Marker:           $marker" && REMOVABLE+=("marker:$marker")
done

if [[ ${#REMOVABLE[@]} -eq 0 ]]; then
    echo "    (no system artifacts found)"
    echo ""
    echo "  Nothing to uninstall."
    exit 0
fi

echo ""

# --- Show what will be preserved ----------------------------------------------
if [[ "$PURGE" != "true" ]]; then
    echo "  The following will be PRESERVED:"
    [[ -n "${REPO:-}" && -d "${REPO:-}" ]] && echo "    - Repository:       $REPO ($(du -sh "$REPO" 2>/dev/null | awk '{print $1}' || echo '?'))"
    [[ -n "${PASS_FILE:-}" && -f "${PASS_FILE:-}" ]] && echo "    - Password file:    $PASS_FILE"
    [[ -n "${LOG_FILE:-}" && -f "${LOG_FILE:-}" ]] && echo "    - Log file:         $LOG_FILE"
    echo ""
else
    echo "  ⚠  --purge: The following will ALSO be DELETED:"
    [[ -n "${REPO:-}" && -d "${REPO:-}" ]] && echo "    - Repository:       $REPO ($(du -sh "$REPO" 2>/dev/null | awk '{print $1}' || echo '?'))"
    [[ -n "${PASS_FILE:-}" && -f "${PASS_FILE:-}" ]] && echo "    - Password file:    $PASS_FILE"
    [[ -n "${LOG_FILE:-}" && -f "${LOG_FILE:-}" ]] && echo "    - Log file:         $LOG_FILE"
    echo ""
    echo "  ⚠  THIS IS IRREVERSIBLE. Your snapshots will be permanently destroyed."
    echo ""
fi

# --- Confirm ------------------------------------------------------------------
if [[ "$ASSUME_YES" != "true" ]]; then
    if [[ "$PURGE" == "true" ]]; then
        read -rp "  Type YES to confirm purge (system + data): " PURGE_CONFIRM
        [[ "$PURGE_CONFIRM" == "YES" ]] || { echo "  Aborted."; exit 0; }
    else
        read -rp "  Proceed with uninstall? [y/N]: " CONFIRM
        [[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "  Aborted."; exit 0; }
    fi
fi

echo ""
echo "==> Removing system artifacts..."

# --- Stop and disable systemd ------------------------------------------------
if [[ " ${REMOVABLE[*]} " == *" systemd "* ]]; then
    systemctl stop time-clawshine.timer 2>/dev/null || true
    systemctl disable time-clawshine.timer 2>/dev/null || true
    rm -f /etc/systemd/system/time-clawshine.service /etc/systemd/system/time-clawshine.timer
    systemctl daemon-reload 2>/dev/null || true
    echo "    ✓ Systemd timer + service removed"
fi

# --- Remove binary -----------------------------------------------------------
for item in "${REMOVABLE[@]}"; do
    if [[ "$item" == binary:* ]]; then
        rm -f "${item#binary:}"
        echo "    ✓ Binary removed: ${item#binary:}"
    fi
done

# --- Remove cron -------------------------------------------------------------
for item in "${REMOVABLE[@]}"; do
    if [[ "$item" == cron:* ]]; then
        rm -f "${item#cron:}"
        echo "    ✓ Cron removed: ${item#cron:}"
    fi
done

# --- Remove logrotate --------------------------------------------------------
for item in "${REMOVABLE[@]}"; do
    if [[ "$item" == logrotate:* ]]; then
        rm -f "${item#logrotate:}"
        echo "    ✓ Logrotate removed: ${item#logrotate:}"
    fi
done

# --- Remove lock and markers -------------------------------------------------
for item in "${REMOVABLE[@]}"; do
    if [[ "$item" == lock:* ]]; then
        rm -f "${item#lock:}"
        echo "    ✓ Lock removed: ${item#lock:}"
    fi
    if [[ "$item" == marker:* ]]; then
        rm -f "${item#marker:}"
        echo "    ✓ Marker removed: ${item#marker:}"
    fi
done

# --- Purge user data (only with --purge) -------------------------------------
if [[ "$PURGE" == "true" ]]; then
    echo ""
    echo "==> Purging user data..."
    if [[ -n "${REPO:-}" && -d "${REPO:-}" ]]; then
        rm -rf "$REPO"
        echo "    ✓ Repository deleted: $REPO"
    fi
    if [[ -n "${PASS_FILE:-}" && -f "${PASS_FILE:-}" ]]; then
        rm -f "$PASS_FILE"
        echo "    ✓ Password file deleted: $PASS_FILE"
    fi
    if [[ -n "${LOG_FILE:-}" && -f "${LOG_FILE:-}" ]]; then
        rm -f "$LOG_FILE"
        echo "    ✓ Log file deleted: $LOG_FILE"
    fi
fi

echo ""
echo "✓ Uninstall complete."
[[ "$PURGE" != "true" ]] && echo "  Your backup repository and password file are preserved."
echo "  No external uninstall notification was sent."
echo "  Source files in $TC_ROOT are untouched — you can re-install with: sudo bin/setup.sh"
