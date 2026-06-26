#!/bin/bash
# Install Quant Engine Cron Jobs

# Get absolute path
WORK_DIR="$(pwd)/workspace/quant_engine"
CRON_FILE="quant.cron"

echo "Detected Quant Engine path: $WORK_DIR"

# 1. Daily Quant Selection (Weekdays 09:15)
# Note: Source .zshrc or .bash_profile to ensure env vars (like PATH for python) are correct if needed.
# But run_task.sh uses absolute path to venv python, so it should be fine.
JOB1="15 09 * * 1-5 cd $WORK_DIR && ./run_task.sh >> run.log 2>&1"

# 2. Weekly Hot Pool Update (Monday 08:30)
JOB2="30 08 * * 1 cd $WORK_DIR && ./update_hot.sh >> pool_update.log 2>&1"

# Backup existing cron
crontab -l > mycron.bak 2>/dev/null

# Create new cron file from existing (excluding old quant jobs to avoid duplicates)
grep -v "quant_engine" mycron.bak > "$CRON_FILE" 2>/dev/null || true

# Append new jobs
echo "# --- Hangzhou AI Quant Engine ---" >> "$CRON_FILE"
echo "$JOB1" >> "$CRON_FILE"
echo "$JOB2" >> "$CRON_FILE"
echo "" >> "$CRON_FILE" # Newline

# Install
crontab "$CRON_FILE"

echo "✅ Crontab installed successfully:"
crontab -l | grep "quant_engine"
rm "$CRON_FILE"
