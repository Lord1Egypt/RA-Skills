#!/usr/bin/env sh
set -eu

CONFIG="${1:-config.json}"

if [ -n "${2:-}" ]; then
    MONTH="$2"
else
    # Anchor to the 15th so subtracting one month is safe when the job
    # runs on the 29th-31st (GNU `date -d 'last month'` on Mar 31 yields
    # Mar 3 via Feb 31 normalization, which regenerates the wrong month).
    ANCHOR="$(date +%Y-%m-15)"
    MONTH="$(date -d "$ANCHOR -1 month" +%Y-%m 2>/dev/null || date -j -f "%Y-%m-%d" "$ANCHOR" -v-1m +%Y-%m)"
fi

PYTHON="$(command -v python3 || command -v python)"

"$PYTHON" -m qbo_mileage generate --config "$CONFIG" --month "$MONTH"
