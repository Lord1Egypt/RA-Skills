#!/bin/bash
# Automated daily backup via cron
# Add to crontab: crontab -e
# 0 2 * * * /path/to/automated-backup.sh >> /tmp/soul-backup.log 2>&1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

# Create daily backup
DATE=$(date +%Y-%m-%d)
node scripts/backup.mjs --name "daily-$DATE" --desc "Automated daily backup"

# Optional: Prune backups older than 30 days
find backups/ -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null

echo "$(date): Daily backup complete"
