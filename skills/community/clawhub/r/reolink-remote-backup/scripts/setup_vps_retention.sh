#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sudo ./setup_vps_retention.sh [days]
# Default days: 30

DAYS="${1:-30}"

( crontab -l 2>/dev/null | grep -v '/srv/reolink/incoming -type f -mtime' ; \
  echo "30 3 * * * find /srv/reolink/incoming -type f -mtime +${DAYS} -delete" ) | crontab -

echo "Installed VPS retention prune: delete files older than ${DAYS} days"
crontab -l
