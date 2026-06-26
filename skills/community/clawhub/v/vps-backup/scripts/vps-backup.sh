#!/usr/bin/env bash
#==============================================================================
# VPS Backup Script — OpenClaw Skill
# Full backup of OpenClaw VPS using restic — encrypted, incremental snapshots
#==============================================================================

# === CONFIG — edit these to match your setup ===
BACKUP_ROOT="${BACKUP_ROOT:-/home/dev/backup/vps-daily}"
RESTIC_REPO="${BACKUP_ROOT}/restic-repo"
SESSION_EXPORT="${SESSION_EXPORT:-/home/dev/scripts/export_sessions.py}"

BACKUP_PATHS=(
    "${HOME}/.openclaw"
    "${HOME}/.config/opencode"
    "${HOME}/.ssh"
    "${HOME}/.npm-global/lib/node_modules"
    "/workspace/projects"
)

RETENTION_DAILY="${RETENTION_DAILY:-7}"
RETENTION_WEEKLY="${RETENTION_WEEKLY:-4}"
RETENTION_MONTHLY="${RETENTION_MONTHLY:-6}"
#=== END CONFIG ===

set -euo pipefail

# --- Env ---
export PATH="${HOME}/bin:${PATH}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

log()  { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
logok(){ log "✓ $*"; }
logwr(){ log "⚠ $*"; }
logerr(){ log "✗ $*" >&2; }

# --- Resolve password ---
resolve_password() {
    if [[ -n "${BACKUP_PASSWORD:-}" ]]; then
        echo "$BACKUP_PASSWORD"
    elif [[ -f "${HOME}/.backup-password" ]]; then
        cat "${HOME}/.backup-password"
    else
        logerr "BACKUP_PASSWORD not set and ~/.backup-password not found"
        return 1
    fi
}

# --- Pre-flight ---
if ! command -v restic &>/dev/null; then
    logerr "restic not found. Install: https://restic.net/install/"
    exit 1
fi

RESTIC_PASSWORD=$(resolve_password)
export RESTIC_PASSWORD

# --- Setup directories ---
mkdir -p "$BACKUP_ROOT" "$RESTIC_REPO"
chmod 700 "$BACKUP_ROOT"
chmod 600 "${HOME}/.backup-password" 2>/dev/null || true

# --- Export session transcripts (optional) ---
if [[ -x "$SESSION_EXPORT" ]]; then
    log "Exporting session transcripts..."
    python3 "$SESSION_EXPORT" 2>/dev/null && logok "Sessions exported" || logwr "Session export failed (non-fatal)"
elif [[ -f "$SESSION_EXPORT" ]]; then
    logwr "Session export script not executable — run: chmod +x $SESSION_EXPORT"
fi

# --- Snapshot system state ---
STATE_FILE="${BACKUP_ROOT}/system-state-${TIMESTAMP}.json"
log "Capturing system state..."
{
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"hostname\": \"$(hostname)\","
    echo "  \"uptime\": \"$(uptime -p 2>/dev/null || uptime)\","
    echo "  \"disk_usage\": \"$(df -h / | tail -1 | awk '{print $3}')\","
    echo "  \"node_version\": \"$(node --version 2>/dev/null || echo 'unknown')\""
    echo "}"
} > "$STATE_FILE"
logok "System state: $STATE_FILE"

# --- Init restic repo if needed ---
if [[ ! -f "${RESTIC_REPO}/config" ]]; then
    log "Initializing restic repository..."
    restic init --repo "$RESTIC_REPO" <<< "$RESTIC_PASSWORD"
    logok "Repository initialized"
fi

# --- Run restic backup ---
log "Running restic backup of ${#BACKUP_PATHS[@]} paths..."
BACKUP_START=$(date +%s)

restic backup \
    "${BACKUP_PATHS[@]}" \
    --exclude="node_modules" \
    --exclude="*.log" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".cache" \
    --exclude="tmp/" \
    --exclude="*.tmp" \
    --exclude="*.sqlite" \
    --exclude="dist/node_modules" \
    --repo "$RESTIC_REPO" \
    --tag "daily" \
    --tag "host-$(hostname)" \
    --tag "date-$(date +%Y-%m-%d)" \
    --compression auto \
    2>&1 | tail -5

BACKUP_END=$(date +%s)
BACKUP_DURATION=$((BACKUP_END - BACKUP_START))
logok "Backup complete in ${BACKUP_DURATION}s"

# --- Retention ---
log "Applying retention (${RETENTION_DAILY} daily, ${RETENTION_WEEKLY} weekly, ${RETENTION_MONTHLY} monthly)..."
restic forget \
    --repo "$RESTIC_REPO" \
    --tag "daily" \
    --keep-daily "$RETENTION_DAILY" \
    --keep-weekly "$RETENTION_WEEKLY" \
    --keep-monthly "$RETENTION_MONTHLY" \
    --prune \
    2>&1 | tail -3

# --- Stats ---
BACKUP_SIZE=$(du -sh "$BACKUP_ROOT" 2>/dev/null | cut -f1)
SNAPSHOT_COUNT=$(restic snapshots --repo "$RESTIC_REPO" --json 2>/dev/null \
    | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
logok "Repo: ${BACKUP_SIZE} | Snapshots: ${SNAPSHOT_COUNT}"

# --- Health check ---
cutoff=$(python3 -c "import datetime; print((datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=26)).isoformat())")
SNAPSHOTS_24H=$(restic snapshots --repo "$RESTIC_REPO" --json 2>/dev/null \
    | python3 -c "
import sys,json,datetime
cutoff=datetime.datetime.fromisoformat('${cutoff}')
print(sum(1 for s in json.load(sys.stdin)
  if datetime.datetime.fromisoformat(s['time'].replace('Z','+00:00'))>cutoff))
" 2>/dev/null || echo "0")
if [[ "$SNAPSHOTS_24H" -ge 1 ]]; then
    logok "Health OK: $SNAPSHOTS_24H snapshot(s) in last 24h"
else
    logerr "HEALTH FAILED: no recent snapshots!"
fi

# --- Offsite push ---
if [[ -n "${RCLONE_DEST:-}" ]] && command -v rclone &>/dev/null; then
    log "Pushing to $RCLONE_DEST..."
    rclone sync "$BACKUP_ROOT" "$RCLONE_DEST" --quiet 2>&1 \
        && logok "Offsite push done" \
        || logwr "Offsite push failed"
fi

log ""
log "========== Done =========="
log "  $(date) | ${BACKUP_DURATION}s | ${BACKUP_SIZE} | ${SNAPSHOT_COUNT} snapshots"
log "==========================="

# Notify OpenClaw if available
if command -v openclaw &>/dev/null; then
    openclaw system event --text "VPS backup done: ${BACKUP_SIZE}, ${SNAPSHOT_COUNT} snapshots, ${BACKUP_DURATION}s" --mode now 2>/dev/null || true
fi
