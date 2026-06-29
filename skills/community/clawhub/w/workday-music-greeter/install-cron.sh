#!/usr/bin/env bash
#
# install-cron.sh — register weekday (Mon–Fri) system cron entries that run
# workday-music-greeter at each scene slot defined in scenes.conf.
#
# Times below mirror the hour-start column in scenes.conf. Adjust to taste.
# Re-running replaces the previous block (idempotent, tagged with a marker).
#
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="$SKILL_DIR/run.sh"
ENV_FILE="$SKILL_DIR/.env"
MARKER="# >>> workday-music-greeter >>>"
END="# <<< workday-music-greeter <<<"

LOAD_ENV=""
[[ -f "$ENV_FILE" ]] && LOAD_ENV="set -a; . '$ENV_FILE'; set +a; "

# minute hour * * 1-5  (Mon–Fri).  Cols: scene at its hour-start.
read -r -d '' BLOCK <<CRON || true
$MARKER
0 8  * * 1-5 ${LOAD_ENV}"$RUN" morning >> /tmp/wmg.log 2>&1
0 12 * * 1-5 ${LOAD_ENV}"$RUN" chill   >> /tmp/wmg.log 2>&1
0 14 * * 1-5 ${LOAD_ENV}"$RUN" focus   >> /tmp/wmg.log 2>&1
0 18 * * 1-5 ${LOAD_ENV}"$RUN" off     >> /tmp/wmg.log 2>&1
$END
CRON

current="$(crontab -l 2>/dev/null || true)"
cleaned="$(printf '%s\n' "$current" | sed "/$MARKER/,/$END/d")"
printf '%s\n%s\n' "$cleaned" "$BLOCK" | sed '/^$/N;/^\n$/D' | crontab -
echo "Installed weekday cron entries. View with: crontab -l"
