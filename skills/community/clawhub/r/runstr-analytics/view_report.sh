#!/bin/bash
# Quick command to view latest RUNSTR report

REPORT_FILE="$HOME/.cache/runstr-analytics/latest_report.txt"

if [ -f "$REPORT_FILE" ]; then
    cat "$REPORT_FILE"
else
    echo "No report found. Run ./daily_update.sh first."
    exit 1
fi
