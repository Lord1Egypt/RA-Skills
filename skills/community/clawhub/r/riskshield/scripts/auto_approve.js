#!/bin/bash
# RiskShield Auto Approve - Headless Background Mode
# Case: 2604131000000597537

SESSION="rs-auto-$$"
REDIRECT="aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s"
LOGIN_URL="https://riskshield.dcsuat.com/mc/page/login.html?redirect=$REDIRECT"
CASE_NO=${1:-"2604131000000597537"}

LOG_FILE="/tmp/rs_auto_approve_$$.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Starting RiskShield Auto Approve ==="
log "Case: $CASE_NO"
log "Session: $SESSION"

# Clean up any existing sessions
agent-browser --session $SESSION close 2>/dev/null

# Step 1: Login
log "[1/6] Opening login page..."
agent-browser --session $SESSION open "$LOGIN_URL" 2>&1 | tail -1
sleep 5

log "[2/6] Filling credentials..."
agent-browser --session $SESSION type @e4 "alan.zhang" 2>&1 | tail -1
agent-browser --session $SESSION type @e5 "ZIdongshenpi1." 2>&1 | tail -1

log "[3/6] Clicking login..."
agent-browser --session $SESSION click @e3 2>&1 | tail -1
sleep 10

# Check URL
URL=$(agent-browser --session $SESSION get url --json 2>&1 | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
log "Current URL: $URL"

# Step 2: Enter case number in the search box (ref=e3)
log "[4/6] Entering case number: $CASE_NO"
agent-browser --session $SESSION type @e3 "$CASE_NO" 2>&1 | tail -1
sleep 1

# Step 3: Click search button (ref=e5)
log "[5/6] Clicking search button..."
agent-browser --session $SESSION click @e5 2>&1 | tail -1
sleep 5

# Check if case appears
SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
if echo "$SNAPSHOT" | grep -q "$CASE_NO"; then
    log "✅ Case $CASE_NO found in results!"
    
    # Find and click the case row
    # Look for the case link or cell containing the case number
    log "[6/6] Clicking on case row..."
    
    # The case should appear in a cell - try clicking on it
    # We'll look for the "审批" link associated with this case
    agent-browser --session $SESSION snapshot -i --json 2>&1 | grep -E "(审批|cell.*$CASE_NO)" | head -5
    
    # Try to find and click the approve link
    # Since we know the case is found, let's look at what links are available
    echo "$SNAPSHOT" | grep -o 'ref:e[0-9]*".*审批' | head -3
    
else
    log "❌ Case $CASE_NO NOT found in search results"
    echo "$SNAPSHOT" | head -50
fi

log "=== Done ==="
log "Log file: $LOG_FILE"

agent-browser --session $SESSION close 2>&1 | tail -1
