#!/bin/bash
# slack_fetch_and_print.sh — Download files from a Slack channel and send to printer.
#
# Basic usage (print latest file):
#   PRINTER=MyPrinter ./slack_fetch_and_print.sh
#
# Smart-matching usage (agent sets env vars based on user intent):
#   PRINTER=MyPrinter LIMIT=2 ./slack_fetch_and_print.sh                  # latest 2 files
#   PRINTER=MyPrinter NAME_PREFIX=report ./slack_fetch_and_print.sh       # files starting with "report"
#   PRINTER=MyPrinter MINUTES=5 FILE_TYPE=pdf ./slack_fetch_and_print.sh  # PDFs from last 5 minutes
#   PRINTER=MyPrinter LIMIT=3 MINUTES=10 ./slack_fetch_and_print.sh       # up to 3 files from last 10 minutes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOADER="$SCRIPT_DIR/../shared/slack_downloader.py"
INBOUND_DIR="${INBOUND_DIR:-$HOME/.openclaw/media/inbound}"
PRINTER="${PRINTER:-}"

mkdir -p "$INBOUND_DIR"

if [ -z "$PRINTER" ]; then
    echo "Error: set the PRINTER environment variable to specify a printer, e.g.: PRINTER=MyPrinter ./slack_fetch_and_print.sh"
    echo "Available printers: $(lpstat -a 2>/dev/null | awk '{print $1}' | tr '\n' ' ')"
    exit 1
fi

source "$SCRIPT_DIR/../shared/slack_args.sh"

# Download files and collect successful paths
DOWNLOADED=()
while IFS= read -r line; do
    echo "$line"
    if [[ "$line" == SUCCESS:* ]]; then
        filepath="${line#SUCCESS: }"
        DOWNLOADED+=("$filepath")
    fi
done < <(python3 "$DOWNLOADER" "${SLACK_ARGS[@]}" "$INBOUND_DIR")

if [ ${#DOWNLOADED[@]} -eq 0 ]; then
    echo "Error: no files to print"
    exit 1
fi

# Send each file to the printer
for f in "${DOWNLOADED[@]}"; do
    lp -d "$PRINTER" "$f"
    echo "Sent to printer: $(basename "$f")"
done
