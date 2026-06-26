#!/bin/bash
# Tech Weekly Briefing - Weekly Cron Job Script
# Runs every Saturday at 6:00 AM Beijing Time

set -e

echo "=========================================="
echo "Tech Weekly Briefing - Weekly Run"
echo "Started at: $(date)"
echo "=========================================="

# Change to skill directory
cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing

# Run the briefing generator
echo "Generating weekly briefing..."
python3 scripts/generate-briefing.py > /tmp/weekly-briefing-output.txt 2>&1

# Check if report was generated
REPORT_FILE=$(ls -t /tmp/tech-weekly-briefing-*.txt 2>/dev/null | head -1)

if [ -f "$REPORT_FILE" ]; then
    echo "Report generated: $REPORT_FILE"
    
    # Send to Telegram (using OpenClaw message tool)
    # The report content will be read and sent
    cat "$REPORT_FILE"
    
    echo "Briefing completed successfully at: $(date)"
else
    echo "ERROR: Report file not found!"
    exit 1
fi

echo "=========================================="
