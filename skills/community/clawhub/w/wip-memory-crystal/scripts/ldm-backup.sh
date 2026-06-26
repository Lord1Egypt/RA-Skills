#!/bin/bash
# Job: ldm-backup
# Backs up the LDM directory (~/.ldm/) to a timestamped snapshot.
# Handles SQLite databases safely (sqlite3 .backup if available, cp otherwise).
#
# Source of truth: memory-crystal-private/scripts/ldm-backup.sh
# Deployed to: ~/.ldm/bin/ldm-backup.sh (via crystal init)
#
# Usage:
#   ldm-backup.sh                     # backup to default location
#   ldm-backup.sh --keep 14           # keep last 14 backups (default: 7)
#   ldm-backup.sh --include-secrets   # include secrets/ dir
#
# Destination: $LDM_BACKUP_DIR or ~/.ldm/backups/

set -euo pipefail

# Cron provides minimal PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

LDM_HOME="$HOME/.ldm"
BACKUP_ROOT="${LDM_BACKUP_DIR:-$LDM_HOME/backups}"
KEEP=7
INCLUDE_SECRETS=false

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep)
      KEEP="$2"
      shift 2
      ;;
    --include-secrets)
      INCLUDE_SECRETS=true
      shift
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 1
      ;;
  esac
done

if [ ! -d "$LDM_HOME" ]; then
  echo "ERROR: LDM home not found at $LDM_HOME" >&2
  exit 1
fi

TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
DEST="$BACKUP_ROOT/$TIMESTAMP"

echo "LDM Backup: $DEST"
mkdir -p "$DEST"

# ── Back up crystal.db (safe copy) ──

CRYSTAL_DB="$LDM_HOME/memory/crystal.db"
if [ -f "$CRYSTAL_DB" ]; then
  mkdir -p "$DEST/memory"
  if command -v sqlite3 &>/dev/null; then
    # Safe backup via sqlite3 .backup (handles WAL mode correctly)
    sqlite3 "$CRYSTAL_DB" ".backup '$DEST/memory/crystal.db'"
    echo "  crystal.db:   backed up (sqlite3 .backup)"
  else
    # Fallback: file copy (may include partial WAL state)
    cp "$CRYSTAL_DB" "$DEST/memory/crystal.db"
    # Copy WAL and SHM if present
    [ -f "$CRYSTAL_DB-wal" ] && cp "$CRYSTAL_DB-wal" "$DEST/memory/crystal.db-wal"
    [ -f "$CRYSTAL_DB-shm" ] && cp "$CRYSTAL_DB-shm" "$DEST/memory/crystal.db-shm"
    echo "  crystal.db:   backed up (file copy)"
  fi
else
  echo "  crystal.db:   not found (skipped)"
fi

# ── Back up config ──

if [ -f "$LDM_HOME/config.json" ]; then
  cp "$LDM_HOME/config.json" "$DEST/config.json"
  echo "  config.json:  backed up"
fi

# ── Back up state files ──

if [ -d "$LDM_HOME/state" ]; then
  cp -a "$LDM_HOME/state" "$DEST/state"
  echo "  state/:       backed up"
fi

# ── Back up agents (transcripts, sessions, daily logs, journals) ──

if [ -d "$LDM_HOME/agents" ]; then
  cp -a "$LDM_HOME/agents" "$DEST/agents"
  echo "  agents/:      backed up"
fi

# ── Back up secrets (optional) ──

if [ "$INCLUDE_SECRETS" = true ] && [ -d "$LDM_HOME/secrets" ]; then
  cp -a "$LDM_HOME/secrets" "$DEST/secrets"
  chmod 700 "$DEST/secrets"
  echo "  secrets/:     backed up"
fi

# ── Retention: remove old backups ──

BACKUP_COUNT=$(ls -1d "$BACKUP_ROOT"/????-??-??-?????? 2>/dev/null | wc -l | tr -d ' ')
if [ "$BACKUP_COUNT" -gt "$KEEP" ]; then
  REMOVE_COUNT=$((BACKUP_COUNT - KEEP))
  ls -1d "$BACKUP_ROOT"/????-??-??-?????? | head -n "$REMOVE_COUNT" | while read OLD; do
    rm -rf "$OLD"
    echo "  Removed old:  $(basename "$OLD")"
  done
fi

echo "Done. $BACKUP_COUNT backups total (keeping $KEEP)."
