#!/bin/bash
# RiskShield Auto Approve v3 - Simple fixed refs

SESSION="rs-v3-$$"
CASE_NO=${1:-"2604131000000597537"}
LOG_FILE="/tmp/rs_v3_$$.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== RiskShield Auto Approve v3 ==="
log "Case: $CASE_NO"

agent-browser --session $SESSION close 2>/dev/null

# Step 1: Login - use fixed refs based on known UI
REDIRECT="aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s"
LOGIN_URL="https://riskshield.dcsuat.com/mc/page/login.html?redirect=$REDIRECT"

log "[1/5] Opening login page..."
agent-browser --session $SESSION open "$LOGIN_URL" 2>&1 | tail -1
sleep 5

# On login page: e4=username, e5=password, e3=login button
log "[2/5] Filling username..."
agent-browser --session $SESSION type @e4 "alan.zhang" 2>&1 | tail -1

log "[3/5] Filling password..."
agent-browser --session $SESSION type @e5 "ZIdongshenpi1." 2>&1 | tail -1

log "[4/5] Clicking login..."
agent-browser --session $SESSION click @e3 2>&1 | tail -1
sleep 10

# Check URL
URL=$(agent-browser --session $SESSION get url --json 2>&1 | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
log "URL after login: $URL"

if echo "$URL" | grep -q "anytask-web"; then
    log "✅ Login success"
    
    # On case list page: e3=case number input, e5=search button
    log "[5/5] Entering case number: $CASE_NO"
    agent-browser --session $SESSION type @e3 "$CASE_NO" 2>&1 | tail -1
    sleep 1
    
    log "Clicking search..."
    agent-browser --session $SESSION click @e5 2>&1 | tail -1
    sleep 5
    
    # Check results
    SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
    if echo "$SNAPSHOT" | grep -q "$CASE_NO"; then
        log "✅ Case $CASE_NO found!"
        
        # Find approve link - look for "审批" in the snapshot
        APPROVE_REF=$(echo "$SNAPSHOT" | grep "审批" | head -1 | grep -o 'ref:e[0-9]*' | head -1)
        log "Approve ref: $APPROVE_REF"
        
        if [ -n "$APPROVE_REF" ]; then
            log "Clicking approve button..."
            agent-browser --session $SESSION click @$APPROVE_REF 2>&1 | tail -1
            sleep 3
            
            # Look for confirm dialog
            SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
            CONFIRM=$(echo "$SNAPSHOT" | grep -E "确定|确认" | head -1 | grep -o 'ref:e[0-9]*' | head -1)
            log "Confirm ref: $CONFIRM"
            
            if [ -n "$CONFIRM" ]; then
                agent-browser --session $SESSION click @$CONFIRM 2>&1 | tail -1
                sleep 2
                log "✅ APPROVE COMPLETED!"
            else
                log "No confirm dialog found"
            fi
        fi
    else
        log "❌ Case not found"
    fi
else
    log "❌ Login failed"
fi

log "=== Done ==="
agent-browser --session $SESSION close 2>&1 | tail -1
