#!/usr/bin/env bash
# Space Duck — daily version check + owner nudge.
#
# Why this exists:
#   Apple ships a "Software Update Available" badge automatically. Space Duck
#   users have to remember to run /update or check MC. This daemon closes the
#   gap: once a day it polls the registry, compares to installed version,
#   and if a new version exists it sends a TG nudge to the duck's owner:
#
#       🦆 Space Duck v0.4.2 available
#       Run /update in this chat or tap [Update Now] in Mission Control.
#
# Idempotency: tracks last-nudged version in $HOME/.space-duck/last_nudge.txt
#   so we don't pester the owner about the same version repeatedly. Only one
#   nudge per (version) pair max.
#
# Deployment:
#   • Cron entry installed by setup_listeners_supervised.sh (Phase 5 wiring)
#   • Daily at 03:00 local time (low-traffic window)
#   • Idempotent — safe to invoke manually
#
# Authored 2026-06-15 — Apple-grade update story Phase 5 of 5.

set -uo pipefail

SD_DIR="$HOME/.space-duck"
NUDGE_STATE="$SD_DIR/last_nudge.txt"
CFG="$SD_DIR/config.json"
LOG="$SD_DIR/logs/version_check.log"

mkdir -p "$(dirname "$LOG")"

log() {
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] $*" >> "$LOG"
}

log "== version_check_daemon start =="

# ─── Prereqs ──────────────────────────────────────────────────────────────────
if [[ ! -f "$CFG" ]]; then
  log "no config.json — skipping (duck not paired)"
  exit 0
fi
if ! command -v clawhub >/dev/null 2>&1; then
  log "clawhub CLI missing — skipping"
  exit 0
fi

# ─── Find installed skill location + version ──────────────────────────────────
SKILL_DIR=""
for p in \
  "$HOME/.openclaw/skills/space-duck" \
  "$HOME/.clawhub/skills/space-duck" \
  "/data/.openclaw/workspace/skills/space-duck" \
  "/data/.openclaw/skills/space-duck" \
  "$HOME/.local/share/clawhub/skills/space-duck" \
  "$HOME/skills/space-duck"
do
  if [[ -f "$p/_meta.json" ]]; then
    SKILL_DIR="$p"
    break
  fi
done

if [[ -z "$SKILL_DIR" ]]; then
  log "no installed skill found — skipping"
  exit 0
fi

CUR_VER=$(python3 -c "import json; print(json.load(open('$SKILL_DIR/_meta.json')).get('version','0.0.0'))" 2>/dev/null || echo "0.0.0")

# ─── Fetch latest from registry ───────────────────────────────────────────────
LATEST_VER=$(timeout 10 clawhub inspect space-duck 2>/dev/null | grep -E '^Latest:' | awk '{print $2}')
if [[ -z "$LATEST_VER" ]]; then
  log "registry unreachable — skipping"
  exit 0
fi

log "installed=$CUR_VER latest=$LATEST_VER"

if [[ "$CUR_VER" == "$LATEST_VER" ]]; then
  log "up to date — no nudge"
  exit 0
fi

# ─── Idempotency: don't re-nudge same version ─────────────────────────────────
if [[ -f "$NUDGE_STATE" ]]; then
  LAST_NUDGED=$(cat "$NUDGE_STATE" 2>/dev/null | head -1 | tr -d ' \n')
  if [[ "$LAST_NUDGED" == "$LATEST_VER" ]]; then
    log "already nudged about $LATEST_VER — skipping"
    exit 0
  fi
fi

# ─── Build TG nudge message ───────────────────────────────────────────────────
# We DON'T sign with [OWNER-APPROVED] — this is just a notification. The user
# replies /update to trigger the actual signed flow. Two-step intentional:
# the daemon notifies, the user actively chooses to install.
MSG_BODY=$(cat <<MSG
🦆 *Space Duck update available*

A new version is ready:
• Installed: v$CUR_VER
• Latest:    v$LATEST_VER

Tap *Update* in Mission Control, or reply \`/update\` in this chat.

(You'll get one tap-to-approve prompt, then your duck self-updates.)
MSG
)

# ─── Send via TG — call /beak/tg/notify endpoint (best-effort) ────────────────
# Read beak_key + spaceduck_id from config
BEAK_KEY=$(python3 -c "import json; print(json.load(open('$CFG')).get('beak_key',''))" 2>/dev/null)
SD_ID=$(python3 -c "import json; print(json.load(open('$CFG')).get('spaceduck_id',''))" 2>/dev/null)

if [[ -z "$BEAK_KEY" || -z "$SD_ID" ]]; then
  log "config missing beak_key or spaceduck_id — skipping"
  exit 0
fi

# Use the existing /beak/tg/notify endpoint (sends to owner's TG via platform)
API_BASE="${SPACEDUCK_API_BASE:-https://beak.spaceduckling.com}"
RESP=$(curl -s -m 10 -w "\n%{http_code}" \
  -H "X-Beak-Key: $BEAK_KEY" \
  -H "Content-Type: application/json" \
  -X POST "$API_BASE/beak/tg/notify" \
  -d "{\"spaceduck_id\":\"$SD_ID\",\"message\":$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$MSG_BODY")}" 2>&1)
HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | head -n -1)

if [[ "$HTTP_CODE" == "200" ]]; then
  log "nudge dispatched (HTTP $HTTP_CODE)"
  echo "$LATEST_VER" > "$NUDGE_STATE"
else
  log "nudge dispatch failed (HTTP $HTTP_CODE): $(echo "$RESP_BODY" | head -c 200)"
  # Don't update NUDGE_STATE — we'll retry tomorrow
fi

log "== version_check_daemon end =="
exit 0
