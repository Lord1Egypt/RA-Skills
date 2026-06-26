#!/bin/bash
# 杭州AI投资社-每日量化选股 (Daily Quant Selection)
# 
# Usage: ./run_task.sh

LOG_FILE="workspace/quant_engine/run.log"
OUTPUT_FILE="workspace/quant_engine/daily_report.txt"
PYTHON_SCRIPT="workspace/quant_engine/main.py"
PYTHON_BIN="workspace/quant_engine/venv/bin/python3"
PIP_BIN="workspace/quant_engine/venv/bin/pip"

# Ensure Python dependencies are installed (first run check)
if ! $PIP_BIN freeze | grep -q "akshare"; then
    echo "Installing dependencies..."
    $PIP_BIN install akshare pandas requests lxml
fi

# Run the Python Analysis Engine
$PYTHON_BIN "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "Python script failed with code $EXIT_CODE. Retrying in 30 seconds..." >> "$LOG_FILE"
    sleep 30
    $PYTHON_BIN "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1
    EXIT_CODE=$?
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo "Task completed successfully." >> "$LOG_FILE"
    
    # Read report content
    REPORT_CONTENT=$(cat "$OUTPUT_FILE")
    
    # Send to Feishu via OpenClaw CLI
    echo "Sending report via OpenClaw..." >> "$LOG_FILE"
    openclaw message send --target "oc_9fc66a80f86a4b97f925e526ca35887e" --message "$REPORT_CONTENT" --channel feishu >> "$LOG_FILE" 2>&1
else
    echo "Task failed. Check logs." >> "$LOG_FILE"
    openclaw message send --target "oc_9fc66a80f86a4b97f925e526ca35887e" --message "⚠️ Quant Task Failed: Check $LOG_FILE" --channel feishu >> "$LOG_FILE" 2>&1
fi
