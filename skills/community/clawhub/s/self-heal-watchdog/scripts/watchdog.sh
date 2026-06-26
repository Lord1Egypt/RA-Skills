#!/usr/bin/env bash
# watchdog.sh — Main watchdog script (runs every minute via cron)
# Layers: Process Watchdog → Config Guard → Model Health Check
set -uo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WATCHDOG_DIR="$OPENCLAW_HOME/watchdog"
STATE_FILE="$WATCHDOG_DIR/watchdog-state.json"
LOG_FILE="$WATCHDOG_DIR/watchdog.log"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"
DRY_RUN="${DRY_RUN:-0}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Helpers ──
now() { date '+%Y-%m-%d %H:%M:%S'; }
iso_now() { date '+%Y-%m-%dT%H:%M:%S%z'; }

log() {
    local msg="[$(now)] $*"
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "$msg" >> "$LOG_FILE" 2>/dev/null
    echo "$msg"
}

rotate_log() {
    if [[ -f "$LOG_FILE" ]]; then
        local lines
        lines=$(wc -l < "$LOG_FILE" | tr -d ' ')
        if (( lines > 1000 )); then
            tail -500 "$LOG_FILE" > "${LOG_FILE}.tmp"
            mv "${LOG_FILE}.tmp" "$LOG_FILE"
        fi
    fi
}

read_state() {
    python3 -c "
import json, sys
try:
    with open('$STATE_FILE') as f:
        d = json.load(f)
    for k,v in d.items():
        print(f'{k}={v}')
except:
    print('fail_count=0')
    print('current_model=unknown')
    print('failed_models=[]')
" 2>/dev/null
}

update_state() {
    local key="$1" value="$2"
    python3 -c "
import json
with open('$STATE_FILE') as f:
    d = json.load(f)
d['$key'] = $value
with open('$STATE_FILE', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null
}

# ── DR Mode ──
if [[ "$DRY_RUN" == "1" ]]; then
    log "🔍 [DRY-RUN] Watchdog starting..."
fi

rotate_log

# ═══════════════════════════════════════
# Layer 1: Process Watchdog
# ═══════════════════════════════════════
GW_PID=$(pgrep -f "openclaw" 2>/dev/null | head -1)

if [[ -z "$GW_PID" ]]; then
    log "❌ Gateway process not found!"

    if [[ "$DRY_RUN" == "1" ]]; then
        log "🔍 [DRY-RUN] Would restart gateway: openclaw gateway start"
    else
        log "🔄 Restarting gateway..."
        openclaw gateway restart >> "$LOG_FILE" 2>&1 &
        sleep 5
        NEW_PID=$(pgrep -f "openclaw" 2>/dev/null | head -1)
        if [[ -n "$NEW_PID" ]]; then
            log "✅ Gateway restarted (PID: $NEW_PID)"
        else
            log "❌ Gateway restart failed!"
        fi
    fi
    # Skip health check this round — gateway just started
    exit 0
fi

# ═══════════════════════════════════════
# Layer 2: Config Guard — Backup before check
# ═══════════════════════════════════════
if [[ -f "$CONFIG_FILE" ]]; then
    # Verify config is valid JSON
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    else
        log "⚠️  Config file corrupted! Attempting rollback..."
        if [[ -f "${CONFIG_FILE}.bak" ]]; then
            if [[ "$DRY_RUN" == "1" ]]; then
                log "🔍 [DRY-RUN] Would restore config from .bak"
            else
                cp "${CONFIG_FILE}.bak" "$CONFIG_FILE"
                log "✅ Config restored from .bak"
                openclaw gateway restart >> "$LOG_FILE" 2>&1 &
            fi
        else
            log "❌ No backup available to restore!"
        fi
        exit 1
    fi
fi

# ═══════════════════════════════════════
# Layer 3: Model Health Check
# ═══════════════════════════════════════
HEALTH_RESULT=$("$SCRIPT_DIR/health-check.sh" 2>&1)
HEALTH_EXIT=$?

# Parse current model for logging
CURRENT_MODEL=$(python3 -c "
import json
try:
    with open('$STATE_FILE') as f:
        print(json.load(f).get('current_model','unknown'))
except: print('unknown')
" 2>/dev/null || echo "unknown")

if (( HEALTH_EXIT == 0 )); then
    RESPONSE_MS=$(echo "$HEALTH_RESULT" | grep -oE '[0-9]+' | head -1)
    log "✅ Health check passed (model: $CURRENT_MODEL, response: ${RESPONSE_MS:-?}ms)"
    # Reset fail counter
    update_state "fail_count" "0"
    update_state "last_check" "\"$(iso_now)\""
else
    # Read current fail count
    FAIL_COUNT=$(python3 -c "
import json
try:
    with open('$STATE_FILE') as f:
        print(json.load(f).get('fail_count',0))
except: print(0)
" 2>/dev/null || echo "0")

    FAIL_COUNT=$((FAIL_COUNT + 1))
    log "❌ Health check failed (model: $CURRENT_MODEL) [$FAIL_COUNT/2]"
    update_state "fail_count" "$FAIL_COUNT"
    update_state "last_check" "\"$(iso_now)\""

    if (( FAIL_COUNT >= 2 )); then
        log "⚠️  Threshold reached ($FAIL_COUNT consecutive failures) — triggering failover"

        if [[ "$DRY_RUN" == "1" ]]; then
            log "🔍 [DRY-RUN] Would trigger model-failover.sh"
        else
            FAILOVER_RESULT=$("$SCRIPT_DIR/model-failover.sh" 2>&1)
            FAILOVER_EXIT=$?
            log "$FAILOVER_RESULT"
            if (( FAILOVER_EXIT == 0 )); then
                # Reset counter after successful failover
                update_state "fail_count" "0"
            fi
        fi
    fi
fi

# Final log rotation check
rotate_log
