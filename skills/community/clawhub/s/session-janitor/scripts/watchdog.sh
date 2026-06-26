#!/usr/bin/env bash
# session-janitor watchdog — detects hung/stale gateway sessions and alerts via Slack
# Invoked by janitor.sh or run standalone via cron.
# A "stuck" session = gateway process alive, but active session updatedAt hasn't changed in STALE_MINUTES.
set -euo pipefail

export PATH="/home/${USER:-$(whoami)}/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
STALE_MINUTES="${1:-5}"   # session must be stale this long to alert
STATE_FILE="${2:-}"        # optional: suppress duplicate alerts

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] watchdog: $*"; }

if [[ ! -f "$CONFIG_FILE" ]]; then
    log "ERROR: $CONFIG_FILE not found"
    exit 1
fi

# Load alert config
read_alert_config() {
    python3 -c "
import json, os, sys
c = json.load(open('$CONFIG_FILE'))
w = c.get('watchdog', {})
print('ALERT_SLACK=' + str(w.get('alertSlack', True)).lower())
print('SLACK_CHANNEL=' + w.get('slackChannel', ''))
print('SLACK_TARGET=' + w.get('slackTarget', ''))
print('AUTO_RESTART=' + str(w.get('autoRestart', False)).lower())
print('RESTART_SCRIPT_SLACK=' + os.path.expanduser(w.get('restartScriptSlack', '~/bin/safe-slack-restart.sh')))
print('RESTART_SCRIPT_DISCORD=' + os.path.expanduser(w.get('restartScriptDiscord', '~/bin/safe-gateway-restart.sh')))
gws = c.get('gateways', [])
print('GATEWAY_COUNT=' + str(len(gws)))
"
}
eval "$(read_alert_config)"

get_gateway() {
    local idx="$1" field="$2"
    python3 -c "
import json, os
c = json.load(open('$CONFIG_FILE'))
gw = c['gateways'][$idx]
v = gw.get('$field', '')
if isinstance(v, str) and '~' in v:
    v = os.path.expanduser(v)
print(v)
"
}

NOW=$(date +%s)
ALERTED=0

check_gateway() {
    local idx="$1"
    local name port token sessions_dir sessions_json service
    name=$(get_gateway "$idx" "name")
    port=$(get_gateway "$idx" "port")
    token=$(get_gateway "$idx" "token")
    sessions_dir=$(get_gateway "$idx" "sessionsDir")
    sessions_json="$sessions_dir/sessions.json"
    service=$(get_gateway "$idx" "service")

    [[ -f "$sessions_json" ]] || return

    # Is gateway process alive?
    if [[ -n "$service" ]]; then
        systemctl --user is-active "$service" >/dev/null 2>&1 || {
            log "$name: service $service is not active — skipping"
            return
        }
    fi

    # Find stale active sessions
    local stale_sids
    stale_sids=$(python3 -c "
import json, time, sys
d = json.load(open('$sessions_json'))
now_ms = int(time.time() * 1000)
stale_ms = $STALE_MINUTES * 60 * 1000
for key, v in d.get('sessions', d).items():
    updated = v.get('updatedAt', 0)
    sid = v.get('sessionId', '')
    if not sid or not updated: continue
    age_ms = now_ms - updated
    if age_ms > stale_ms:
        age_min = age_ms // 60000
        print(f'{sid}|{key}|{age_min}')
" 2>/dev/null)

    [[ -z "$stale_sids" ]] && { log "$name: all sessions current"; return; }

    while IFS='|' read -r sid key age_min; do
        # Check if transcript file exists and is large (implies active work)
        local jsonl="$sessions_dir/$sid.jsonl"
        [[ -f "$jsonl" ]] || continue
        local size_kb=$(( $(stat -c%s "$jsonl" 2>/dev/null || echo 0) / 1024 ))
        (( size_kb < 10 )) && continue  # tiny/empty sessions, not interesting

        # Dedup: skip if we already alerted for this sid+age window (within 10 min)
        local state_key="${name}_${sid}_stuck"
        if [[ -n "$STATE_FILE" ]] && [[ -f "$STATE_FILE" ]]; then
            local last_alert
            last_alert=$(python3 -c "
import json
d = json.load(open('$STATE_FILE'))
print(d.get('watchdog_alerts', {}).get('$state_key', 0))
" 2>/dev/null || echo 0)
            local alert_age=$(( NOW - last_alert ))
            (( alert_age < 600 )) && { log "$name: $sid stuck ${age_min}min — alert suppressed (cooldown)"; continue; }
        fi

        log "$name: SESSION STUCK — $sid stale ${age_min}min, ${size_kb}KB"
        ALERTED=1

        # Send Slack alert
        if [[ "$ALERT_SLACK" == "true" ]]; then
            local msg="⚠️ *Gateway hang detected* — \`$name\` session stale *${age_min} min* (${size_kb}KB transcript)\nSession: \`$sid\`"
            if [[ -n "$SLACK_TARGET" ]]; then
                openclaw message send --channel slack --target "$SLACK_TARGET" -m "$msg" 2>/dev/null || true
            fi
        fi

        # Optionally auto-restart
        if [[ "$AUTO_RESTART" == "true" ]]; then
            log "$name: auto-restart enabled — triggering restart"
            if [[ "$name" == *"slack"* ]]; then
                bash "$RESTART_SCRIPT_SLACK" "watchdog: session stale ${age_min}min" 2>&1 | tail -5 || true
            else
                bash "$RESTART_SCRIPT_DISCORD" "watchdog: session stale ${age_min}min" 2>&1 | tail -5 || true
            fi
        fi

        # Record alert time in state file
        if [[ -n "$STATE_FILE" ]]; then
            python3 -c "
import json, time, os
path = '$STATE_FILE'
d = json.load(open(path)) if os.path.exists(path) else {}
d.setdefault('watchdog_alerts', {})['$state_key'] = int(time.time())
json.dump(d, open(path, 'w'), indent=2)
" 2>/dev/null || true
        fi

    done <<< "$stale_sids"
}

for (( i=0; i<GATEWAY_COUNT; i++ )); do
    check_gateway "$i"
done

(( ALERTED == 0 )) && log "all gateways clean"
exit 0
