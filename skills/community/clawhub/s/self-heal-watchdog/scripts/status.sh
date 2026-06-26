#!/usr/bin/env bash
# status.sh — View watchdog status and recent logs
set -uo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WATCHDOG_DIR="$OPENCLAW_HOME/watchdog"
STATE_FILE="$WATCHDOG_DIR/watchdog-state.json"
LOG_FILE="$WATCHDOG_DIR/watchdog.log"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${CYAN}═══════════════════════════════════════${NC}"
echo -e "${BOLD}${CYAN} 🔧 OpenClaw Self-Heal Watchdog${NC}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════${NC}"
echo ""

# ── State ──
echo -e "${BOLD}📊 State:${NC}"
if [[ -f "$STATE_FILE" ]]; then
    python3 -c "
import json
from datetime import datetime

with open('$STATE_FILE') as f:
    d = json.load(f)

cm = d.get('current_model', '?')
om = d.get('original_model', '?')
fc = d.get('fail_count', 0)
lc = d.get('last_check', 'never')
lf = d.get('last_failover', 'never')
fm = d.get('failed_models', [])
bc = d.get('config_backups', 0)

print(f'  Current Model:  {cm}')
print(f'  Original Model: {om}')
print(f'  Fail Count:     {fc}')
print(f'  Last Check:     {lc}')
print(f'  Last Failover:  {lf}')
print(f'  Failed Models:  {fm if fm else \"none\"}')
" 2>/dev/null
else
    echo -e "  ${RED}State file not found! Run setup.sh first.${NC}"
fi
echo ""

# ── Process status ──
echo -e "${BOLD}🔌 Process:${NC}"
GW_PIDS=$(pgrep -f "openclaw" 2>/dev/null | head -5)
if [[ -n "$GW_PIDS" ]]; then
    echo -e "  ${GREEN}✅ Gateway running${NC} (PIDs: $GW_PIDS)"
else
    echo -e "  ${RED}❌ Gateway not running${NC}"
fi

# ── Health endpoint ──
echo ""
echo -e "${BOLD}🏥 Health Endpoint:${NC}"
HEALTH=$(curl -s --connect-timeout 5 --max-time 5 http://localhost:18789/health 2>/dev/null) || HEALTH=""
if [[ "$HEALTH" == *'"ok":true'* ]]; then
    echo -e "  ${GREEN}✅ Responding${NC} ($HEALTH)"
else
    echo -e "  ${RED}❌ Not responding${NC}"
fi

# ── Scheduler status ──
echo ""
echo -e "${BOLD}⏰ Scheduler:${NC}"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/com.openclaw.watchdog.plist"
if [[ -f "$LAUNCHD_PLIST" ]]; then
    if launchctl list | grep -q "com.openclaw.watchdog" 2>/dev/null; then
        echo -e "  ${GREEN}✅ launchd active${NC} (com.openclaw.watchdog, every 60s)"
    else
        echo -e "  ${YELLOW}⚠️  launchd plist exists but not loaded${NC}"
        echo "  Run: launchctl load $LAUNCHD_PLIST"
    fi
elif crontab -l 2>/dev/null | grep -q "openclaw-watchdog"; then
    CRON_LINE=$(crontab -l 2>/dev/null | grep "openclaw-watchdog")
    echo -e "  ${GREEN}✅ Cron registered${NC}"
    echo "  $CRON_LINE"
else
    echo -e "  ${RED}❌ No scheduler registered${NC}"
    echo "  Run setup.sh to install"
fi

# ── Config backup ──
echo ""
echo -e "${BOLD}💾 Config Backups:${NC}"
for ext in .bak .bak.prev; do
    if [[ -f "${CONFIG_FILE}${ext}" ]]; then
        SIZE=$(ls -lh "${CONFIG_FILE}${ext}" | awk '{print $5}')
        TIME=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "${CONFIG_FILE}${ext}" 2>/dev/null || echo "?")
        echo "  ${CONFIG_FILE}${ext} ($SIZE, $TIME)"
    fi
done

# ── Recent logs ──
echo ""
echo -e "${BOLD}📝 Recent Logs:${NC}"
if [[ -f "$LOG_FILE" ]]; then
    if [[ "${1:-}" == "--full" ]]; then
        cat "$LOG_FILE"
    else
        tail -20 "$LOG_FILE"
    fi
else
    echo -e "  ${YELLOW}No log file yet.${NC}"
fi

echo ""
echo -e "${CYAN}Tip: bash status.sh --full for complete log${NC}"
