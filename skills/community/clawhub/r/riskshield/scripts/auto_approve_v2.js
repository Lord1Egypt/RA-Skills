#!/bin/bash
# RiskShield Auto Approve v2 - Dynamic element discovery
# Uses snapshot to find refs dynamically

SESSION="rs-auto2-$$"
CASE_NO=${1:-"2604131000000597537"}
LOG_FILE="/tmp/rs_auto2_$$.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

get_ref_by_placeholder() {
    local placeholder="$1"
    echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*${placeholder}" | head -1 | grep -o 'ref:e[0-9]*' | head -1
}

get_ref_by_role() {
    local role="$1"
    local name="$2"
    echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.${role}.*${name}" | head -1 | grep -o 'ref:e[0-9]*'
}

log "=== RiskShield Auto Approve v2 ==="
log "Case: $CASE_NO"

agent-browser --session $SESSION close 2>/dev/null

# Step 1: Login
REDIRECT="aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s"
LOGIN_URL="https://riskshield.dcsuat.com/mc/page/login.html?redirect=$REDIRECT"

log "[1/5] Opening login page..."
agent-browser --session $SESSION open "$LOGIN_URL" 2>&1 | tail -1
sleep 4

# Get fresh refs from login page
SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
USER_INPUT=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*textbox.*user" | grep -o 'ref:e[0-9]*' | head -1)
PASS_INPUT=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*textbox.*password" | grep -o 'ref:e[0-9]*' | head -1)
LOGIN_BTN=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*button.*login" | grep -o 'ref:e[0-9]*' | head -1)

log "Login refs: user=$USER_INPUT, pass=$PASS_INPUT, btn=$LOGIN_BTN"

log "[2/5] Filling credentials..."
agent-browser --session $SESSION type @$USER_INPUT "alan.zhang" 2>&1 | tail -1
agent-browser --session $SESSION type @$PASS_INPUT "ZIdongshenpi1." 2>&1 | tail -1

log "[3/5] Clicking login button..."
agent-browser --session $SESSION click @$LOGIN_BTN 2>&1 | tail -1
sleep 12

# Verify we're on the case list page
URL=$(agent-browser --session $SESSION get url --json 2>&1 | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
log "Current URL: $URL"

if ! echo "$URL" | grep -q "anytask-web"; then
    log "❌ Login failed - not on case list page"
    agent-browser --session $SESSION close 2>&1 | tail -1
    exit 1
fi

# Step 4: Get refs for the case list page
log "[4/5] Getting case list refs..."
SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)

# Find case number input (textbox with empty placeholder or the one for case search)
CASE_INPUT=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*textbox" | grep -v "请选择\|select\|Select" | grep -o 'ref:e[0-9]*' | head -3 | tail -1)
SEARCH_BTN=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*搜索\|ref:e[0-9]*.*search" | grep -o 'ref:e[0-9]*' | head -1)

log "Case input ref: $CASE_INPUT"
log "Search btn ref: $SEARCH_BTN"

# If refs are empty, try alternative approach
if [ -z "$CASE_INPUT" ]; then
    # Try ref=e3 which is often the search input on this UI
    CASE_INPUT="e3"
fi
if [ -z "$SEARCH_BTN" ]; then
    # Try ref=e5 which is often the search button
    SEARCH_BTN="e5"
fi

log "[5/5] Searching for case: $CASE_NO"
agent-browser --session $SESSION type @$CASE_INPUT "$CASE_NO" 2>&1 | tail -1
sleep 1
agent-browser --session $SESSION click @$SEARCH_BTN 2>&1 | tail -1
sleep 5

# Check results
SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
if echo "$SNAPSHOT" | grep -q "$CASE_NO"; then
    log "✅ Case $CASE_NO found!"
    log "Looking for approve button..."
    
    # Find the "审批" link next to this case
    # In the snapshot, cases with "审理中" status have an "审批" link
    echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*审批" | head -5
    
    # Try to find and click the approve link
    APPROVE_REF=$(echo "$SNAPSHOT" | grep -B5 "审批.*link" | grep -o 'ref:e[0-9]*' | head -1)
    if [ -n "$APPROVE_REF" ]; then
        log "Clicking approve: @$APPROVE_REF"
        agent-browser --session $SESSION click @$APPROVE_REF 2>&1 | tail -1
        sleep 5
        
        # Check for approve confirmation dialog
        SNAPSHOT=$(agent-browser --session $SESSION snapshot -i --json 2>&1)
        if echo "$SNAPSHOT" | grep -q "确认\|确定"; then
            CONFIRM_REF=$(echo "$SNAPSHOT" | grep -o "ref:e[0-9]*.*确定\|ref:e[0-9]*.*确认" | grep -o 'ref:e[0-9]*' | head -1)
            if [ -n "$CONFIRM_REF" ]; then
                log "Confirming: @$CONFIRM_REF"
                agent-browser --session $SESSION click @$CONFIRM_REF 2>&1 | tail -1
                sleep 3
                log "✅ APPROVE SUCCESSFUL!"
            fi
        fi
    fi
else
    log "❌ Case $CASE_NO not found in search results"
fi

log "=== Done ==="
agent-browser --session $SESSION close 2>&1 | tail -1
cat "$LOG_FILE"
