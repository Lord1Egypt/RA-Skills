#!/bin/bash
# Trainer Buddy Pro — Workout Data Backup Script
# Creates a timestamped backup of all user data files.
# Usage: ./backup-workout-data.sh

set -euo pipefail
umask 077

# --- Workspace Root Detection ---
# Walk up the directory tree looking for AGENTS.md or SOUL.md markers
find_workspace_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/AGENTS.md" ] || [ -f "$dir/SOUL.md" ]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  # Fallback: try relative to script location
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [ -f "$script_dir/../AGENTS.md" ]; then
    echo "$(cd "$script_dir/.." && pwd)"
  elif [ -f "$script_dir/../../../AGENTS.md" ]; then
    echo "$(cd "$script_dir/../../.." && pwd)"
  else
    echo "ERROR: Could not find workspace root." >&2
    exit 1
  fi
}

WORKSPACE_ROOT="$(find_workspace_root)"
# Find the skill's data directory
SKILL_MD_PATH="$(find "$WORKSPACE_ROOT" -path "*/skills/trainer-buddy-pro/SKILL.md" -type f -print -quit 2>/dev/null)"
if [ -z "$SKILL_MD_PATH" ]; then
  echo "❌ Error: Cannot find trainer-buddy-pro skill directory."
  exit 1
fi
SKILL_DIR="$(dirname "$SKILL_MD_PATH")"

DATA_DIR="$SKILL_DIR/data"

if [ ! -d "$DATA_DIR" ]; then
  echo "❌ Error: No data directory found at $DATA_DIR"
  echo "   Have you used Trainer Buddy Pro yet? Data is created on first use."
  exit 1
fi

# Create backup directory
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
BACKUP_DIR="$SKILL_DIR/backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"
chmod 700 "$SKILL_DIR/backups"
chmod 700 "$BACKUP_DIR"

# Copy all data files
shopt -s nullglob dotglob
data_files=("$DATA_DIR"/*)
if [ "${#data_files[@]}" -gt 0 ]; then
  cp -R "${data_files[@]}" "$BACKUP_DIR/"
fi
shopt -u nullglob dotglob

# Set permissions on backup
find "$BACKUP_DIR" -type f -exec chmod 600 {} \;
find "$BACKUP_DIR" -type d -exec chmod 700 {} \;

# Count files backed up
FILE_COUNT=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')

echo "✅ Backup complete!"
echo "   Location: $BACKUP_DIR"
echo "   Files backed up: $FILE_COUNT"
echo "   Timestamp: $TIMESTAMP"

# Clean up old backups — keep last 10
BACKUP_ROOT="$SKILL_DIR/backups"
mapfile -t backup_dirs < <(find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sort)
BACKUP_COUNT="${#backup_dirs[@]}"
if [ "$BACKUP_COUNT" -gt 10 ]; then
  REMOVE_COUNT=$((BACKUP_COUNT - 10))
  echo "   Cleaning up $REMOVE_COUNT old backup(s)..."
  for old_backup in "${backup_dirs[@]:0:$REMOVE_COUNT}"; do
    rm -rf -- "$old_backup"
  done
fi
