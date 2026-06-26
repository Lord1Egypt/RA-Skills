#!/bin/bash
# Daily memo summary script
# Runs at 10:00 daily, summarizes pending items

TODO_FILE="$HOME/.openclaw/workspace/pending-items.md"
LOG_FILE="$HOME/.openclaw/workspace/memo-log.txt"

# Log execution time
echo "=== Daily Memo Summary $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# Read pending items
if [ -f "$TODO_FILE" ]; then
    # Extract item list
    echo "Reading pending items file..." >> "$LOG_FILE"
    
    # Check if there are pending items
    if grep -q "^[0-9]\+\. " "$TODO_FILE"; then
        # Extract all items
        TODOS=$(grep "^[0-9]\+\. " "$TODO_FILE")
        COUNT=$(echo "$TODOS" | wc -l | tr -d ' ')
        
        echo "Found $COUNT pending items:" >> "$LOG_FILE"
        echo "$TODOS" >> "$LOG_FILE"
        
        # Build summary message
        SUMMARY="📋 Pending items summary ($(date '+%Y-%m-%d %H:%M'))\\n\\n"
        
        while IFS= read -r line; do
            SUMMARY="${SUMMARY}${line}\\n"
        done <<< "$TODOS"
        
        SUMMARY="${SUMMARY}\\nTotal: $COUNT pending items."
        
        echo "Summary content built" >> "$LOG_FILE"
        
        # Output to stdout (for OpenClaw cron capture)
        echo "{{summary}}"
        echo "$SUMMARY"
        
    else
        echo "No pending items" >> "$LOG_FILE"
        
        SUMMARY="📋 Pending items summary ($(date '+%Y-%m-%d %H:%M'))\\n\\n_No pending items_"
        
        echo "{{summary}}"
        echo "$SUMMARY"
    fi
else
    echo "Error: Pending items file not found" >> "$LOG_FILE"
    echo "{{error}}Memo file not found"
fi

echo "Summary completed" >> "$LOG_FILE"