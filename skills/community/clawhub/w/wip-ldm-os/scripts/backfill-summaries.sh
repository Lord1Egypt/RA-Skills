#!/bin/bash
# backfill-summaries.sh — Generate all historical summaries from day 1.
# Part of Total Recall. Uses ldm-summary.sh with --force --date.
#
# Usage:
#   backfill-summaries.sh              # full backfill (Feb 5 to yesterday)
#   backfill-summaries.sh --dry-run    # preview
#   backfill-summaries.sh --from 2026-03-01  # partial backfill
#
# Order: dailies first, then weeklies, monthlies, quarterly.
# Each level reads the level below. Must complete in order.

set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

SUMMARY_SCRIPT="$HOME/.ldm/bin/ldm-summary.sh"
DRY_RUN=false
FROM_DATE="2026-02-05"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --from) FROM_DATE="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

if [ ! -f "$SUMMARY_SCRIPT" ]; then
  echo "ERROR: ldm-summary.sh not found. Run ldm install first." >&2
  exit 1
fi

YESTERDAY=$(python3 -c "from datetime import datetime, timedelta; print((datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d'))")
FLAGS="--force"
[ "$DRY_RUN" = true ] && FLAGS="$FLAGS --dry-run"

echo "=== Total Recall: Backfill Summaries ==="
echo "  From: $FROM_DATE"
echo "  To:   $YESTERDAY"
echo "  Mode: $([ "$DRY_RUN" = true ] && echo 'DRY RUN' || echo 'LIVE')"
echo ""

# ── Step 1: Dailies ──

echo "=== STEP 1: Daily summaries ==="
DAILY_COUNT=0
for date in $(python3 -c "
from datetime import datetime, timedelta
d = datetime.strptime('$FROM_DATE', '%Y-%m-%d')
end = datetime.strptime('$YESTERDAY', '%Y-%m-%d')
while d <= end:
  print(d.strftime('%Y-%m-%d'))
  d += timedelta(days=1)
"); do
  echo "--- $date ---"
  bash "$SUMMARY_SCRIPT" daily --date "$date" $FLAGS 2>&1 | grep -E "->|DRY RUN|No data|No git"
  DAILY_COUNT=$((DAILY_COUNT + 1))
done
echo "  Dailies: $DAILY_COUNT days"
echo ""

# ── Step 2: Weeklies (Sunday to Saturday) ──

echo "=== STEP 2: Weekly summaries ==="
WEEKLY_COUNT=0
for date in $(python3 -c "
from datetime import datetime, timedelta
# Start from first Sunday >= FROM_DATE
d = datetime.strptime('$FROM_DATE', '%Y-%m-%d')
while d.weekday() != 6: d += timedelta(days=1)  # find Sunday
end = datetime.now()
while d <= end:
  # Use the Saturday (end of week) as the date
  sat = d + timedelta(days=6)
  print(sat.strftime('%Y-%m-%d'))
  d += timedelta(days=7)
"); do
  echo "--- Week ending $date ---"
  bash "$SUMMARY_SCRIPT" weekly --date "$date" $FLAGS 2>&1 | grep -E "->|DRY RUN|No "
  WEEKLY_COUNT=$((WEEKLY_COUNT + 1))
done
echo "  Weeklies: $WEEKLY_COUNT weeks"
echo ""

# ── Step 3: Monthlies ──

echo "=== STEP 3: Monthly summaries ==="
for date in $(python3 -c "
from datetime import datetime
import calendar
d = datetime.strptime('$FROM_DATE', '%Y-%m-%d')
now = datetime.now()
while d <= now:
  last_day = calendar.monthrange(d.year, d.month)[1]
  print(f'{d.year}-{d.month:02d}-{last_day:02d}')
  if d.month == 12: d = d.replace(year=d.year+1, month=1, day=1)
  else: d = d.replace(month=d.month+1, day=1)
"); do
  echo "--- Month ending $date ---"
  bash "$SUMMARY_SCRIPT" monthly --date "$date" $FLAGS 2>&1 | grep -E "->|DRY RUN|No "
done
echo ""

# ── Step 4: Quarterly ──

echo "=== STEP 4: Quarterly summary ==="
bash "$SUMMARY_SCRIPT" quarterly --date "$(date +%Y-%m-%d)" $FLAGS 2>&1 | grep -E "->|DRY RUN|No "

echo ""
echo "=== Backfill complete ==="
echo "  $DAILY_COUNT dailies processed"
echo "  $WEEKLY_COUNT weeklies processed"
