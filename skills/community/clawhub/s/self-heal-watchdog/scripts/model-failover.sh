#!/usr/bin/env bash
# model-failover.sh — Switch to fallback model when current one fails
set -uo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WATCHDOG_DIR="$OPENCLAW_HOME/watchdog"
STATE_FILE="$WATCHDOG_DIR/watchdog-state.json"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"
LOG_FILE="$WATCHDOG_DIR/watchdog.log"
DRY_RUN="${DRY_RUN:-0}"

now() { date '+%Y-%m-%d %H:%M:%S'; }
iso_now() { date '+%Y-%m-%dT%H:%M:%S%z'; }

log() {
    local msg="[$(now)] $*"
    echo "$msg" >> "$LOG_FILE"
    echo "$msg"
}

# ── Read current state ──
eval "$(python3 -c "
import json
try:
    with open('$STATE_FILE') as f:
        d = json.load(f)
    print(f'CURRENT_MODEL=\"{d.get(\"current_model\",\"unknown\")}\"')
    print(f'ORIGINAL_MODEL=\"{d.get(\"original_model\",\"unknown\")}\"')
    print(f'FAILED_MODELS_RAW=\"{json.dumps(d.get(\"failed_models\",[]))}\"')
except Exception as e:
    print(f'CURRENT_MODEL=\"unknown\"')
    print(f'ORIGINAL_MODEL=\"unknown\"')
    print(f'FAILED_MODELS_RAW=\"[]\"')
" 2>/dev/null)"

# ── Get all available models from config ──
AVAILABLE_MODELS=$(python3 -c "
import json
try:
    with open('$CONFIG_FILE') as f:
        d = json.load(f)
    models = []
    for provider, pdata in d.get('models',{}).get('providers',{}).items():
        for m in pdata.get('models',[]):
            mid = m.get('id','')
            if mid:
                models.append(f'{provider}/{mid}')
    # Also add short IDs
    for provider, pdata in d.get('models',{}).get('providers',{}).items():
        for m in pdata.get('models',[]):
            mid = m.get('id','')
            if mid and '/' not in mid:
                models.append(f'{provider}/{mid}')
    print(' '.join(models))
except:
    print('')
" 2>/dev/null)

# ── Parse failed models list ──
FAILED_MODELS=$(python3 -c "
import json
raw = '$FAILED_MODELS_RAW'
try:
    lst = json.loads(raw)
    print(' '.join(lst))
except:
    print('')
" 2>/dev/null)

# ── Find next available model ──
NEXT_MODEL=""

for candidate in $AVAILABLE_MODELS; do
    # Skip current model
    [[ "$candidate" == "$CURRENT_MODEL" ]] && continue
    # Skip already-failed models
    SKIP=0
    for fm in $FAILED_MODELS; do
        [[ "$candidate" == "$fm" ]] && SKIP=1
    done
    (( SKIP )) && continue
    # Skip the original model (don't cycle back)
    [[ "$candidate" == "$ORIGINAL_MODEL" ]] && continue
    NEXT_MODEL="$candidate"
    break
done

# Fallback: if no other model, try healer-alpha as last resort
if [[ -z "$NEXT_MODEL" ]]; then
    for candidate in $AVAILABLE_MODELS; do
        [[ "$candidate" == "$CURRENT_MODEL" ]] && continue
        NEXT_MODEL="$candidate"
        break
    done
fi

if [[ -z "$NEXT_MODEL" ]]; then
    log "❌ No alternative model available for failover!"
    exit 1
fi

log "🔄 FAILOVER: $CURRENT_MODEL → $NEXT_MODEL"

if [[ "$DRY_RUN" == "1" ]]; then
    log "🔍 [DRY-RUN] Would update config and restart gateway"
    exit 0
fi

# ── Backup config before modifying ──
cp "$CONFIG_FILE" "${CONFIG_FILE}.bak.prev"

# ── Update model in config ──
python3 -c "
import json

with open('$CONFIG_FILE') as f:
    d = json.load(f)

# Update the primary model
if 'agents' not in d:
    d['agents'] = {}
if 'defaults' not in d['agents']:
    d['agents']['defaults'] = {}
if 'model' not in d['agents']['defaults']:
    d['agents']['defaults']['model'] = {}

d['agents']['defaults']['model']['primary'] = '$NEXT_MODEL'

with open('$CONFIG_FILE', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null

if (( $? != 0 )); then
    log "❌ Failed to update config! Rolling back..."
    cp "${CONFIG_FILE}.bak.prev" "$CONFIG_FILE"
    exit 1
fi

log "✅ Config updated to use $NEXT_MODEL"

# ── Update state file ──
python3 -c "
import json
with open('$STATE_FILE') as f:
    d = json.load(f)
d['current_model'] = '$NEXT_MODEL'
d['last_failover'] = '$(iso_now)'
d['fail_count'] = 0
failed = d.get('failed_models', [])
if '$CURRENT_MODEL' not in failed:
    failed.append('$CURRENT_MODEL')
d['failed_models'] = failed
with open('$STATE_FILE', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null

# ── Restart gateway ──
log "🔄 Restarting gateway with new model..."
openclaw gateway restart >> "$LOG_FILE" 2>&1 &

# Wait briefly then verify
sleep 5
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout 10 --max-time 10 \
    "http://localhost:18789/health" 2>/dev/null) || HEALTH_CHECK="000"

if [[ "$HEALTH_CHECK" == "200" ]]; then
    log "✅ Gateway restarted successfully with $NEXT_MODEL"
else
    log "⚠️  Gateway health check returned HTTP $HEALTH_CHECK after restart (may still be starting)"
fi

# ── Try to notify via OpenClaw (best effort, don't fail if it doesn't work) ──
log "📢 Model failover complete: $CURRENT_MODEL → $NEXT_MODEL"

exit 0
