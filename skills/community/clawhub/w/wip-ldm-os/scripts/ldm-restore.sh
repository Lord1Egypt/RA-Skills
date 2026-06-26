#!/bin/bash
# ldm-restore.sh — Restore from an LDM OS backup
# Restores: ~/.ldm/, ~/.openclaw/, ~/.claude/, ~/wipcomputerinc/
#
# Source of truth: wip-ldm-os-private/scripts/ldm-restore.sh
# Deployed to: ~/.ldm/bin/ldm-restore.sh (via ldm install)
#
# Usage:
#   ldm-restore.sh                          # list available backups
#   ldm-restore.sh 2026-03-24--09-50-22     # restore from specific backup
#   ldm-restore.sh --from-icloud <file>     # restore from iCloud tar
#   ldm-restore.sh --dry-run <backup>       # preview what would be restored
#   ldm-restore.sh --only ldm <backup>      # restore only ~/.ldm/ data
#   ldm-restore.sh --only openclaw <backup> # restore only ~/.openclaw/ data
#   ldm-restore.sh --only claude <backup>   # restore only ~/.claude/ data
#   ldm-restore.sh --only workspace <backup># restore only workspace

set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

LDM_HOME="$HOME/.ldm"
BACKUP_ROOT="$LDM_HOME/backups"
DRY_RUN=false
ONLY=""
FROM_ICLOUD=""
BACKUP_NAME=""

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --only) ONLY="$2"; shift 2 ;;
    --from-icloud) FROM_ICLOUD="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: ldm-restore.sh [options] [backup-name]"
      echo ""
      echo "Options:"
      echo "  --dry-run              Preview what would be restored"
      echo "  --only <section>       Restore only: ldm, openclaw, claude, workspace"
      echo "  --from-icloud <file>   Restore from iCloud .tar.gz"
      echo ""
      echo "Examples:"
      echo "  ldm-restore.sh                           # list backups"
      echo "  ldm-restore.sh 2026-03-24--09-50-22      # restore from local"
      echo "  ldm-restore.sh --only ldm 2026-03-24--09-50-22  # restore only crystal.db + agents"
      echo "  ldm-restore.sh --from-icloud ~/path/to/backup.tar.gz"
      exit 0
      ;;
    *) BACKUP_NAME="$1"; shift ;;
  esac
done

# If restoring from iCloud tar, extract to temp dir first
if [ -n "$FROM_ICLOUD" ]; then
  if [ ! -f "$FROM_ICLOUD" ]; then
    echo "ERROR: File not found: $FROM_ICLOUD" >&2
    exit 1
  fi
  echo "Extracting iCloud backup to temp dir..."
  TEMP_DIR=$(mktemp -d)
  tar -xzf "$FROM_ICLOUD" -C "$TEMP_DIR"
  # Find the backup dir inside (should be one dated folder)
  BACKUP_NAME=$(ls "$TEMP_DIR" | head -1)
  BACKUP_ROOT="$TEMP_DIR"
  echo "  Extracted: $BACKUP_NAME"
fi

# List mode (no backup specified)
if [ -z "$BACKUP_NAME" ]; then
  echo "Available backups:"
  echo ""
  if [ -d "$BACKUP_ROOT" ]; then
    for d in $(ls -1d "$BACKUP_ROOT"/20??-??-??--* 2>/dev/null | sort -r); do
      SIZE=$(du -sh "$d" | cut -f1)
      echo "  $(basename "$d")  ($SIZE)"
    done
  fi
  echo ""
  echo "Usage: ldm-restore.sh <backup-name>"
  echo "  e.g. ldm-restore.sh 2026-03-24--09-50-22"
  exit 0
fi

SRC="$BACKUP_ROOT/$BACKUP_NAME"

if [ ! -d "$SRC" ]; then
  echo "ERROR: Backup not found: $SRC" >&2
  exit 1
fi

echo "=== LDM Restore: $BACKUP_NAME ==="
echo "  Source: $SRC"
echo "  Mode:  ${ONLY:-all}"
echo ""

# Read workspace path
WORKSPACE=""
if [ -f "$LDM_HOME/config.json" ]; then
  WORKSPACE=$(python3 -c "import json; print(json.load(open('$LDM_HOME/config.json')).get('workspace',''))" 2>/dev/null || true)
fi

if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Would restore:"
  [ -z "$ONLY" ] || [ "$ONLY" = "ldm" ] && {
    [ -f "$SRC/ldm/memory/crystal.db" ] && echo "  crystal.db -> ~/.ldm/memory/crystal.db"
    [ -d "$SRC/ldm/agents" ] && echo "  agents/ -> ~/.ldm/agents/"
    [ -d "$SRC/ldm/state" ] && echo "  state/ -> ~/.ldm/state/"
    [ -f "$SRC/ldm/config.json" ] && echo "  config.json -> ~/.ldm/config.json"
  }
  [ -z "$ONLY" ] || [ "$ONLY" = "openclaw" ] && {
    [ -f "$SRC/openclaw/memory/main.sqlite" ] && echo "  main.sqlite -> ~/.openclaw/memory/main.sqlite"
    [ -f "$SRC/openclaw/memory/context-embeddings.sqlite" ] && echo "  context-embeddings.sqlite -> ~/.openclaw/memory/"
    [ -f "$SRC/openclaw/workspace.tar" ] && echo "  workspace.tar -> ~/.openclaw/workspace/"
    [ -f "$SRC/openclaw/sessions.tar" ] && echo "  sessions.tar -> ~/.openclaw/agents/main/sessions/"
    [ -f "$SRC/openclaw/openclaw.json" ] && echo "  openclaw.json -> ~/.openclaw/"
  }
  [ -z "$ONLY" ] || [ "$ONLY" = "claude" ] && {
    [ -f "$SRC/claude/CLAUDE.md" ] && echo "  CLAUDE.md -> ~/.claude/CLAUDE.md"
    [ -f "$SRC/claude/settings.json" ] && echo "  settings.json -> ~/.claude/settings.json"
    [ -f "$SRC/claude/projects.tar" ] && echo "  projects.tar -> ~/.claude/projects/"
  }
  [ -z "$ONLY" ] || [ "$ONLY" = "workspace" ] && {
    [ -f "$SRC/wipcomputerinc.tar" ] && echo "  wipcomputerinc.tar -> $WORKSPACE/"
  }
  echo ""
  echo "[DRY RUN] No files modified."
  exit 0
fi

echo "WARNING: This will overwrite existing files. Press Ctrl+C to cancel."
echo "Restoring in 5 seconds..."
sleep 5

# ── Restore ~/.ldm/ ──

if [ -z "$ONLY" ] || [ "$ONLY" = "ldm" ]; then
  echo "--- Restoring ~/.ldm/ ---"

  if [ -f "$SRC/ldm/memory/crystal.db" ]; then
    cp "$SRC/ldm/memory/crystal.db" "$LDM_HOME/memory/crystal.db"
    echo "  crystal.db:              OK"
  fi

  if [ -d "$SRC/ldm/agents" ]; then
    cp -a "$SRC/ldm/agents/"* "$LDM_HOME/agents/" 2>/dev/null
    echo "  agents/:                 OK"
  fi

  if [ -d "$SRC/ldm/state" ]; then
    cp -a "$SRC/ldm/state/"* "$LDM_HOME/state/" 2>/dev/null
    echo "  state/:                  OK"
  fi

  [ -f "$SRC/ldm/config.json" ] && cp "$SRC/ldm/config.json" "$LDM_HOME/config.json" && echo "  config.json:             OK"
fi

# ── Restore ~/.openclaw/ ──

if [ -z "$ONLY" ] || [ "$ONLY" = "openclaw" ]; then
  echo "--- Restoring ~/.openclaw/ ---"

  OC_HOME="$HOME/.openclaw"

  if [ -f "$SRC/openclaw/memory/main.sqlite" ]; then
    cp "$SRC/openclaw/memory/main.sqlite" "$OC_HOME/memory/main.sqlite"
    echo "  main.sqlite:             OK"
  fi

  if [ -f "$SRC/openclaw/memory/context-embeddings.sqlite" ]; then
    cp "$SRC/openclaw/memory/context-embeddings.sqlite" "$OC_HOME/memory/context-embeddings.sqlite"
    echo "  context-embeddings:      OK"
  fi

  if [ -f "$SRC/openclaw/workspace.tar" ]; then
    tar -xf "$SRC/openclaw/workspace.tar" -C "$OC_HOME/"
    echo "  workspace/:              OK"
  fi

  if [ -f "$SRC/openclaw/sessions.tar" ]; then
    mkdir -p "$OC_HOME/agents/main"
    tar -xf "$SRC/openclaw/sessions.tar" -C "$OC_HOME/agents/main/"
    echo "  sessions/:               OK"
  fi

  [ -f "$SRC/openclaw/openclaw.json" ] && cp "$SRC/openclaw/openclaw.json" "$OC_HOME/openclaw.json" && echo "  openclaw.json:           OK"

  for f in session-export-state.json cc-export-watermark.json cc-capture-watermark.json memory-capture-state.json; do
    [ -f "$SRC/openclaw/memory/$f" ] && cp "$SRC/openclaw/memory/$f" "$OC_HOME/memory/$f"
  done
  echo "  state files:             OK"
fi

# ── Restore ~/.claude/ ──

if [ -z "$ONLY" ] || [ "$ONLY" = "claude" ]; then
  echo "--- Restoring ~/.claude/ ---"

  [ -f "$SRC/claude/CLAUDE.md" ] && cp "$SRC/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md" && echo "  CLAUDE.md:               OK"
  [ -f "$SRC/claude/settings.json" ] && cp "$SRC/claude/settings.json" "$HOME/.claude/settings.json" && echo "  settings.json:           OK"

  if [ -f "$SRC/claude/projects.tar" ]; then
    tar -xf "$SRC/claude/projects.tar" -C "$HOME/.claude/"
    echo "  projects/:               OK"
  fi
fi

# ── Restore workspace ──

if [ -z "$ONLY" ] || [ "$ONLY" = "workspace" ]; then
  if [ -f "$SRC/wipcomputerinc.tar" ] && [ -n "$WORKSPACE" ]; then
    echo "--- Restoring workspace ---"
    tar -xf "$SRC/wipcomputerinc.tar" -C "$(dirname "$WORKSPACE")"
    echo "  workspace:               OK"
  fi
fi

# Clean up temp dir if from iCloud
[ -n "${TEMP_DIR:-}" ] && rm -rf "$TEMP_DIR"

echo ""
echo "=== Restore complete ==="
echo "  Restart the gateway: openclaw gateway restart"
echo "  Verify crystal: crystal status"
