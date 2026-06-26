#!/bin/bash
# ldm-backup.sh — Unified backup for LDM OS
# Backs up: ~/.ldm/, ~/.openclaw/, ~/.claude/, $WORKSPACE/
# Handles SQLite safely (sqlite3 .backup). Tars to iCloud for offsite.
#
# Source of truth: wip-ldm-os-private/scripts/ldm-backup.sh
# Deployed to: ~/.ldm/bin/ldm-backup.sh (via ldm install)
#
# Usage:
#   ldm-backup.sh                     # run backup
#   ldm-backup.sh --dry-run           # preview what would be backed up
#   ldm-backup.sh --keep 14           # keep last 14 backups (default: 7)
#   ldm-backup.sh --include-secrets   # include ~/.ldm/secrets/
#
# Config: ~/.ldm/config.json (workspace path, backup settings, iCloud path)

set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

LDM_HOME="$HOME/.ldm"
OC_HOME="$HOME/.openclaw"
CLAUDE_HOME="$HOME/.claude"
BACKUP_ROOT="$LDM_HOME/backups"
KEEP=7
INCLUDE_SECRETS=false
DRY_RUN=false

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep) KEEP="$2"; shift 2 ;;
    --include-secrets) INCLUDE_SECRETS=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# Read workspace path from ~/.ldm/config.json
WORKSPACE=""
if [ -f "$LDM_HOME/config.json" ]; then
  WORKSPACE=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('workspace',''))" 2>/dev/null || true)
fi
if [ -z "$WORKSPACE" ]; then
  echo "WARNING: No workspace in ~/.ldm/config.json. Skipping workspace backup."
fi

# Read org name from config (used for tar filename)
ORG=""
if [ -f "$LDM_HOME/config.json" ]; then
  ORG=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('org',''))" 2>/dev/null || true)
fi
if [ -z "$ORG" ]; then
  ORG="workspace"
fi

# Read iCloud backup path from ~/.ldm/config.json
ICLOUD_BACKUP=""
if [ -f "$LDM_HOME/config.json" ]; then
  ICLOUD_BACKUP=$(python3 -c "
import json, os
c = json.load(open('$LDM_HOME/config.json'))
p = c.get('paths',{}).get('icloudBackup','')
print(os.path.expanduser(p))
" 2>/dev/null || true)
fi

# Read keep from ~/.ldm/config.json (override if set there)
if [ -f "$LDM_HOME/config.json" ]; then
  CONFIG_KEEP=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('backup',{}).get('keep',0))" 2>/dev/null || true)
  if [ -n "$CONFIG_KEEP" ] && [ "$CONFIG_KEEP" -gt 0 ] 2>/dev/null; then
    KEEP="$CONFIG_KEEP"
  fi
fi

DATE=$(date +%Y-%m-%d--%H-%M-%S)
DEST="$BACKUP_ROOT/$DATE"

echo "=== LDM Backup: $DATE ==="
echo "  Local:     $DEST"
echo "  iCloud:    ${ICLOUD_BACKUP:-not configured}"
echo "  Keep:      $KEEP days"
echo "  Workspace: ${WORKSPACE:-not configured}"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Would back up:"
  echo "  ~/.ldm/memory/crystal.db (sqlite3 .backup)"
  echo "  ~/.ldm/agents/ (cp -a)"
  echo "  ~/.ldm/state/ (cp -a)"
  echo "  ~/.ldm/config.json (cp)"
  [ -f "$OC_HOME/memory/main.sqlite" ] && echo "  ~/.openclaw/memory/main.sqlite (sqlite3 .backup) [$(du -sh "$OC_HOME/memory/main.sqlite" | cut -f1)]"
  [ -f "$OC_HOME/memory/context-embeddings.sqlite" ] && echo "  ~/.openclaw/memory/context-embeddings.sqlite (sqlite3 .backup) [$(du -sh "$OC_HOME/memory/context-embeddings.sqlite" | cut -f1)]"
  [ -d "$OC_HOME/workspace" ] && echo "  ~/.openclaw/workspace/ (tar) [$(du -sh "$OC_HOME/workspace" | cut -f1)]"
  [ -d "$OC_HOME/agents/main/sessions" ] && echo "  ~/.openclaw/agents/main/sessions/ (tar) [$(du -sh "$OC_HOME/agents/main/sessions" | cut -f1)]"
  [ -f "$OC_HOME/openclaw.json" ] && echo "  ~/.openclaw/openclaw.json (cp)"
  [ -f "$CLAUDE_HOME/CLAUDE.md" ] && echo "  ~/.claude/CLAUDE.md (cp)"
  [ -f "$CLAUDE_HOME/settings.json" ] && echo "  ~/.claude/settings.json (cp)"
  [ -d "$CLAUDE_HOME/projects" ] && echo "  ~/.claude/projects/ (tar) [$(du -sh "$CLAUDE_HOME/projects" | cut -f1)]"
  if [ -n "$WORKSPACE" ] && [ -d "$WORKSPACE" ]; then
    # macOS du uses -I for exclusions (not --exclude)
    WS_KB=$(du -sk -I "node_modules" -I ".git" -I "_temp" -I "_trash" "$WORKSPACE" 2>/dev/null | cut -f1 || echo "?")
    WS_MB=$((WS_KB / 1024))
    echo "  $WORKSPACE/ (tar, excludes node_modules/.git/objects/_temp/_trash)"
    echo "    estimated size: ${WS_MB}MB (${WS_KB}KB)"
    if [ "$WS_KB" -gt 10000000 ] 2>/dev/null; then
      echo "    WARNING: exceeds 10GB limit. Backup would abort."
    fi
  fi
  [ "$INCLUDE_SECRETS" = true ] && echo "  ~/.ldm/secrets/ (cp -a)"
  echo ""
  echo "[DRY RUN] No files modified."
  exit 0
fi

# Preflight
if [ ! -d "$LDM_HOME" ]; then
  echo "ERROR: ~/.ldm/ not found" >&2
  exit 1
fi

mkdir -p "$DEST/ldm/memory" "$DEST/openclaw/memory" "$DEST/claude"

# ── 1. Back up ~/.ldm/ ──

echo "--- ~/.ldm/ ---"

# Crystal DB (safe sqlite3 .backup)
CRYSTAL_DB="$LDM_HOME/memory/crystal.db"
if [ -f "$CRYSTAL_DB" ]; then
  if command -v sqlite3 &>/dev/null; then
    sqlite3 "$CRYSTAL_DB" ".backup '$DEST/ldm/memory/crystal.db'"
    echo "  crystal.db:              sqlite3 .backup OK"
  else
    cp "$CRYSTAL_DB" "$DEST/ldm/memory/crystal.db"
    [ -f "$CRYSTAL_DB-wal" ] && cp "$CRYSTAL_DB-wal" "$DEST/ldm/memory/crystal.db-wal"
    [ -f "$CRYSTAL_DB-shm" ] && cp "$CRYSTAL_DB-shm" "$DEST/ldm/memory/crystal.db-shm"
    echo "  crystal.db:              file copy (no sqlite3)"
  fi
else
  echo "  crystal.db:              not found (skipped)"
fi

# Config
[ -f "$LDM_HOME/config.json" ] && cp "$LDM_HOME/config.json" "$DEST/ldm/config.json" && echo "  config.json:             OK"

# State
[ -d "$LDM_HOME/state" ] && cp -a "$LDM_HOME/state" "$DEST/ldm/state" && echo "  state/:                  OK"

# Agents (identity, journals, daily logs)
[ -d "$LDM_HOME/agents" ] && cp -a "$LDM_HOME/agents" "$DEST/ldm/agents" && echo "  agents/:                 OK"

# Secrets (optional)
if [ "$INCLUDE_SECRETS" = true ] && [ -d "$LDM_HOME/secrets" ]; then
  cp -a "$LDM_HOME/secrets" "$DEST/ldm/secrets"
  chmod 700 "$DEST/ldm/secrets"
  echo "  secrets/:                OK"
fi

# ── 2. Back up ~/.openclaw/ ──

echo "--- ~/.openclaw/ ---"

# main.sqlite (safe sqlite3 .backup)
if [ -f "$OC_HOME/memory/main.sqlite" ]; then
  if command -v sqlite3 &>/dev/null; then
    sqlite3 "$OC_HOME/memory/main.sqlite" ".backup '$DEST/openclaw/memory/main.sqlite'"
    echo "  main.sqlite:             sqlite3 .backup OK"
  else
    cp "$OC_HOME/memory/main.sqlite" "$DEST/openclaw/memory/main.sqlite"
    [ -f "$OC_HOME/memory/main.sqlite-wal" ] && cp "$OC_HOME/memory/main.sqlite-wal" "$DEST/openclaw/memory/main.sqlite-wal"
    echo "  main.sqlite:             file copy"
  fi
fi

# context-embeddings.sqlite
if [ -f "$OC_HOME/memory/context-embeddings.sqlite" ]; then
  if command -v sqlite3 &>/dev/null; then
    sqlite3 "$OC_HOME/memory/context-embeddings.sqlite" ".backup '$DEST/openclaw/memory/context-embeddings.sqlite'"
    echo "  context-embeddings:      sqlite3 .backup OK"
  else
    cp "$OC_HOME/memory/context-embeddings.sqlite" "$DEST/openclaw/memory/context-embeddings.sqlite"
    echo "  context-embeddings:      file copy"
  fi
fi

# Workspace
[ -d "$OC_HOME/workspace" ] && tar -cf "$DEST/openclaw/workspace.tar" -C "$OC_HOME" workspace 2>/dev/null && echo "  workspace/:              tar OK"

# OC sessions
[ -d "$OC_HOME/agents/main/sessions" ] && tar -cf "$DEST/openclaw/sessions.tar" -C "$OC_HOME/agents/main" sessions 2>/dev/null && echo "  sessions/:               tar OK"

# OC config
[ -f "$OC_HOME/openclaw.json" ] && cp "$OC_HOME/openclaw.json" "$DEST/openclaw/openclaw.json" && echo "  openclaw.json:           OK"

# State files
for f in session-export-state.json cc-export-watermark.json cc-capture-watermark.json memory-capture-state.json; do
  [ -f "$OC_HOME/memory/$f" ] && cp "$OC_HOME/memory/$f" "$DEST/openclaw/memory/$f"
done
echo "  state files:             OK"

# ── 3. Back up ~/.claude/ ──

echo "--- ~/.claude/ ---"

[ -f "$CLAUDE_HOME/CLAUDE.md" ] && cp "$CLAUDE_HOME/CLAUDE.md" "$DEST/claude/CLAUDE.md" && echo "  CLAUDE.md:               OK"
[ -f "$CLAUDE_HOME/settings.json" ] && cp "$CLAUDE_HOME/settings.json" "$DEST/claude/settings.json" && echo "  settings.json:           OK"
[ -d "$CLAUDE_HOME/projects" ] && tar -cf "$DEST/claude/projects.tar" -C "$CLAUDE_HOME" projects 2>/dev/null && echo "  projects/:               tar OK"

# ── 4. Back up workspace ──

if [ -n "$WORKSPACE" ] && [ -d "$WORKSPACE" ]; then
  echo "--- $WORKSPACE/ ---"

  # Size guard: estimate workspace size before tarring
  # macOS du uses -I for exclusions (not --exclude)
  ESTIMATED_KB=$(du -sk -I "node_modules" -I ".git" -I "_temp" -I "_trash" "$WORKSPACE" 2>/dev/null | cut -f1 || echo "0")
  MAX_KB=10000000  # 10GB
  if [ "$ESTIMATED_KB" -gt "$MAX_KB" ] 2>/dev/null; then
    echo "  ERROR: Workspace estimated at ${ESTIMATED_KB}KB (>10GB). Aborting tar to prevent disk fill."
    echo "  Check for large directories: du -sh $WORKSPACE/*/"
  else
    tar -cf "$DEST/$ORG.tar" \
      --exclude "node_modules" \
      --exclude ".git/objects" \
      --exclude ".DS_Store" \
      --exclude "*/staff/cc-mini/documents/backups" \
      --exclude "*/_temp/backups" \
      --exclude "*/_temp/_archive" \
      --exclude "*/_trash" \
      -C "$(dirname "$WORKSPACE")" "$(basename "$WORKSPACE")" 2>/dev/null \
      && echo "  workspace:               tar OK (est ${ESTIMATED_KB}KB)" \
      || echo "  workspace:               tar FAILED"
  fi
fi

# ── 5. iCloud offsite ──

if [ -n "$ICLOUD_BACKUP" ] && [ -d "$(dirname "$ICLOUD_BACKUP")" ]; then
  echo "--- iCloud offsite ---"
  mkdir -p "$ICLOUD_BACKUP"
  ORG=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('org','ldmos'))" 2>/dev/null || echo "ldmos")
  DEVICE=$(hostname -s)
  TAR_NAME="${ORG}-${DEVICE}-${DATE}.tar.gz"
  tar -czf "$ICLOUD_BACKUP/$TAR_NAME" -C "$BACKUP_ROOT" "$DATE" 2>/dev/null \
    && echo "  $TAR_NAME: OK" \
    || echo "  iCloud tar: FAILED"

  # Rotate iCloud tars
  ICLOUD_COUNT=$(ls -1 "$ICLOUD_BACKUP"/*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
  if [ "$ICLOUD_COUNT" -gt "$KEEP" ]; then
    REMOVE_COUNT=$((ICLOUD_COUNT - KEEP))
    ls -1t "$ICLOUD_BACKUP"/*.tar.gz | tail -n "$REMOVE_COUNT" | while read OLD; do
      rm -f "$OLD"
      echo "  Rotated: $(basename "$OLD")"
    done
  fi
fi

# ── 6. Rotate local backups ──

echo "--- Rotation ---"
BACKUP_COUNT=$(ls -1d "$BACKUP_ROOT"/20??-??-??--* 2>/dev/null | wc -l | tr -d ' ')
if [ "$BACKUP_COUNT" -gt "$KEEP" ]; then
  REMOVE_COUNT=$((BACKUP_COUNT - KEEP))
  ls -1d "$BACKUP_ROOT"/20??-??-??--* | head -n "$REMOVE_COUNT" | while read OLD; do
    # Skip pinned backups
    if [ -f "$OLD/.pinned" ]; then
      echo "  Skipped (pinned): $(basename "$OLD")"
      continue
    fi
    rm -rf "$OLD"
    echo "  Removed: $(basename "$OLD")"
  done
fi

# ── Summary ──

TOTAL_SIZE=$(du -sh "$DEST" | cut -f1)
echo ""
echo "=== Backup complete ==="
echo "  Location: $DEST"
echo "  Size:     $TOTAL_SIZE"
echo "  Backups:  $BACKUP_COUNT total (keeping $KEEP)"
[ -n "$ICLOUD_BACKUP" ] && echo "  iCloud:   $ICLOUD_BACKUP/"
