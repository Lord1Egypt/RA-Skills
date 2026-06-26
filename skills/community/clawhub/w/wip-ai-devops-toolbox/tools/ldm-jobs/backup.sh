#!/bin/bash
# Job: daily backup
# Calls Lesa's existing backup script

SCRIPT="$HOME/.ldm/bin/ldm-backup.sh"

echo "=== Backup started: $(date) ==="

if [ -f "$SCRIPT" ]; then
  /bin/bash "$SCRIPT"
else
  echo "ERROR: backup script not found at $SCRIPT"
  exit 1
fi

echo "=== Backup finished: $(date) ==="
