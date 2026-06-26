#!/bin/bash
# Setup script for RUNSTR daily cron job

echo "📅 RUNSTR Daily Update - Cron Setup"
echo "======================================"
echo ""
echo "⚠️  SECURITY NOTICE:"
echo "    This script will use RUNSTR_NSEC from your environment."
echo "    Ensure your system does NOT log environment variables."
echo "    Cache data is stored with restrictive permissions (user-only)."
echo "    For maximum security, use full-disk encryption."
echo ""
read -p "Continue? (y/N): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 7 * * * $SCRIPT_DIR/daily_update.sh >> $HOME/.cache/runstr-analytics/cron.log 2>&1"

echo "This will set up a daily cron job to update RUNSTR analytics."
echo ""
echo "Schedule: Every day at 07:00"
echo "Script: $SCRIPT_DIR/daily_update.sh"
echo "Log: $HOME/.cache/runstr-analytics/daily_update.log"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "runstr-analytics/daily_update.sh"; then
    echo "⚠️  Cron job already exists."
    echo ""
    echo "Current crontab entry:"
    crontab -l | grep "runstr-analytics"
    echo ""
    read -p "Replace existing job? (y/N): " REPLACE
    if [[ $REPLACE =~ ^[Yy]$ ]]; then
        # Remove old entry
        crontab -l 2>/dev/null | grep -v "runstr-analytics/daily_update.sh" | crontab -
        echo "Old job removed."
    else
        echo "Setup cancelled."
        exit 0
    fi
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo ""
echo "The job will run daily at 07:00."
echo ""
echo "Commands:"
echo "  View crontab: crontab -l"
echo "  Edit crontab: crontab -e"
echo "  View logs:    tail -f ~/.cache/runstr-analytics/daily_update.log"
echo "  Run now:      ./daily_update.sh"
echo ""

# Test run
read -p "Run the update now to test? (y/N): " TEST_RUN
if [[ $TEST_RUN =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running update..."
    "$SCRIPT_DIR/daily_update.sh"
fi

echo ""
echo "Setup complete! 🎸"
