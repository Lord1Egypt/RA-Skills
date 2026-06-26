#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_SCRIPT="$SCRIPT_DIR/report.sh"
LOG_FILE="${HOME}/.openclaw/ranking-of-claws-cron.log"
MARKER="# ranking-of-claws"
CRON_LINE="*/10 * * * * bash \"$REPORT_SCRIPT\" >> \"$LOG_FILE\" 2>&1 $MARKER"

CURRENT_CRON="$(crontab -l 2>/dev/null || true)"

if printf '%s\n' "$CURRENT_CRON" | grep -Fq "$MARKER"; then
  echo "ranking-of-claws: cron already configured."
  exit 0
fi

{
  printf '%s\n' "$CURRENT_CRON"
  printf '%s\n' "$CRON_LINE"
} | sed '/^[[:space:]]*$/N;/^\n$/D' | crontab -

echo "ranking-of-claws: cron installed (every 10 min)."
