#!/usr/bin/env bash
# Space Duck — self-diagnosis report.
#
# Why this exists:
#   When something breaks (listener silent, auto-reply not firing, bridge
#   binding-state stuck), the user has to SSH to their box, locate
#   ~20 different files across 5 possible paths, tail logs, parse output,
#   and guess what's wrong. Then paste it all to support.
#
#   This script collapses that into one command: `./doctor.sh`. The output
#   is paste-ready (single screen, structured, marked with ✓/⚠/✗) so the
#   user or support can read failure modes at a glance.
#
# Apple-grade UX goals:
#   • Run with no arguments
#   • Auto-discover every Space Duck artefact on the box
#   • Categorise findings: ✓ healthy / ⚠ known degraded / ✗ broken
#   • Suggest the next action for each ⚠ or ✗
#   • Output is safe to share publicly (no secrets, no full URLs with tokens)
#
# Doctrine:
#   • Read-only. NEVER mutates state. Doctor diagnoses, never treats.
#   • Bash + standard CLI tools only (curl, ps, head, tail, awk)
#   • Fast — full report under 5 seconds
#
# Authored 2026-06-15 — Apple-grade update story Phase 2 of 5.

set -uo pipefail

# ─── Styling ──────────────────────────────────────────────────────────────────
if [[ -t 1 ]] && command -v tput >/dev/null 2>&1; then
  C_GREEN=$(tput setaf 2 2>/dev/null || echo)
  C_YELLOW=$(tput setaf 3 2>/dev/null || echo)
  C_RED=$(tput setaf 1 2>/dev/null || echo)
  C_BLUE=$(tput setaf 4 2>/dev/null || echo)
  C_DIM=$(tput dim 2>/dev/null || echo)
  C_BOLD=$(tput bold 2>/dev/null || echo)
  C_RESET=$(tput sgr0 2>/dev/null || echo)
else
  C_GREEN= C_YELLOW= C_RED= C_BLUE= C_DIM= C_BOLD= C_RESET=
fi

# All findings collected here; printed at end. Categories: ok/warn/fail.
declare -i HEALTH_OK=0 HEALTH_WARN=0 HEALTH_FAIL=0

row()    { echo "  $*"; }
ok()     { echo "${C_GREEN}✓${C_RESET} $*"; HEALTH_OK=$((HEALTH_OK+1)); }
warn()   { echo "${C_YELLOW}⚠${C_RESET} $*"; HEALTH_WARN=$((HEALTH_WARN+1)); }
fail()   { echo "${C_RED}✗${C_RESET} $*"; HEALTH_FAIL=$((HEALTH_FAIL+1)); }
hint()   { echo "    ${C_DIM}→ $*${C_RESET}"; }
section(){ echo; echo "${C_BLUE}${C_BOLD}── $* ──${C_RESET}"; }

redact_url() {
  # Keep scheme + tld, hide subdomain hash so report is safe to paste publicly
  local u="$1"
  echo "$u" | sed -E 's|(https?://)[^/]+(\.[a-z]+/)|\1<host>\2|; s|(https?://)[^/]+$|\1<host>|'
}

# ─── 0. Banner ────────────────────────────────────────────────────────────────
echo
echo "${C_BOLD}🦆 Space Duck Doctor${C_RESET}"
echo "$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo "Host: $(uname -n) ($(uname -sr))"
echo

# ─── 1. Skill install location + version ──────────────────────────────────────
section "Skill install"
SKILL_DIR=""
for p in \
  "$HOME/.openclaw/skills/space-duck" \
  "$HOME/.clawhub/skills/space-duck" \
  "/data/.openclaw/workspace/skills/space-duck" \
  "/data/.openclaw/skills/space-duck" \
  "$HOME/.local/share/clawhub/skills/space-duck" \
  "$HOME/skills/space-duck" \
  "$(pwd)/skills/space-duck"
do
  if [[ -f "$p/_meta.json" ]]; then
    SKILL_DIR="$p"
    break
  fi
done

if [[ -z "$SKILL_DIR" ]]; then
  fail "No space-duck install found on disk"
  hint "Install: clawhub install space-duck"
else
  ok "Location: $SKILL_DIR"
  CUR_VER=$(python3 -c "import json; print(json.load(open('$SKILL_DIR/_meta.json')).get('version','unknown'))" 2>/dev/null || echo "unknown")
  row "Installed version: ${C_BOLD}$CUR_VER${C_RESET}"
  # 0.4.5 — Sam-feedback fix: prefer the gateway's authoritative
  # /beak/skill/latest registry over peer claims or stale local clawhub
  # inspect output. Fall back to clawhub inspect if the gateway is down.
  LATEST=""
  if command -v curl >/dev/null 2>&1; then
    LATEST=$(timeout 4 curl -fsS https://beak.spaceduckling.com/beak/skill/latest 2>/dev/null \
      | python3 -c "import sys,json; print(json.load(sys.stdin)['skills'].get('space-duck',''))" 2>/dev/null || echo "")
  fi
  if [[ -z "$LATEST" ]] && command -v clawhub >/dev/null 2>&1; then
    LATEST=$(timeout 5 clawhub inspect space-duck 2>/dev/null | grep -E '^Latest:' | awk '{print $2}' || echo "")
  fi
  if [[ -n "$LATEST" ]]; then
    if [[ "$LATEST" == "$CUR_VER" ]]; then
      ok "Up to date (latest=$LATEST, authoritative)"
    else
      warn "Update available: v$CUR_VER → v$LATEST"
      hint "Run: $SKILL_DIR/scripts/update.sh"
    fi
  else
    warn "Registry unreachable (skipping version check)"
  fi
fi

# ─── 2. ClawHub CLI ───────────────────────────────────────────────────────────
section "ClawHub CLI"
if command -v clawhub >/dev/null 2>&1; then
  ok "Installed ($(clawhub -V 2>/dev/null | head -1))"
else
  warn "Not on PATH"
  hint "Install: npm install -g @clawhub/cli"
fi

# ─── 3. Config + Beak Key ─────────────────────────────────────────────────────
section "Identity (~/.space-duck/config.json)"
SD_DIR="$HOME/.space-duck"
CFG="$SD_DIR/config.json"
if [[ -f "$CFG" ]]; then
  CFG_MODE=$(stat -c '%a' "$CFG" 2>/dev/null || stat -f '%A' "$CFG" 2>/dev/null || echo "?")
  if [[ "$CFG_MODE" == "600" ]]; then
    ok "Config present (mode 600)"
  else
    warn "Config present but mode is $CFG_MODE (expected 600)"
    hint "Fix: chmod 600 $CFG"
  fi
  SD_ID=$(python3 -c "import json; d=json.load(open('$CFG')); print(d.get('spaceduck_id','?'))" 2>/dev/null || echo "?")
  DL_ID=$(python3 -c "import json; d=json.load(open('$CFG')); print(d.get('duckling_id','?'))" 2>/dev/null || echo "?")
  BK_OK=$(python3 -c "import json; d=json.load(open('$CFG')); print('yes' if d.get('beak_key','').startswith('bk_') else 'no')" 2>/dev/null || echo "?")
  row "spaceduck_id: ${SD_ID:0:8}…"
  row "duckling_id:  ${DL_ID:0:8}…"
  if [[ "$BK_OK" == "yes" ]]; then
    row "Beak Key:     ${C_GREEN}present${C_RESET}"
  else
    fail "Beak Key missing or malformed"
    hint "Re-pair: python3 $SKILL_DIR/scripts/pair.py"
  fi
else
  fail "$CFG missing"
  hint "Pair this duck first: python3 $SKILL_DIR/scripts/pair.py"
fi

# ─── 4. Listener processes ────────────────────────────────────────────────────
section "Listener processes"
LISTENER_PIDS=$(pgrep -fa 'telegram_listener\.py' 2>/dev/null | grep -v doctor.sh || true)
RESPONDER_PIDS=$(pgrep -fa 'peck_responder\.py' 2>/dev/null | grep -v doctor.sh || true)
PECK_LISTENER_PIDS=$(pgrep -fa 'peck_listener\.py' 2>/dev/null | grep -v doctor.sh || true)

if [[ -n "$LISTENER_PIDS" ]]; then
  ok "telegram_listener.py running"
  echo "$LISTENER_PIDS" | head -3 | sed 's/^/    /'
else
  warn "telegram_listener.py not running"
  hint "Start: $SKILL_DIR/scripts/setup_listeners_supervised.sh"
fi

if [[ -n "$PECK_LISTENER_PIDS" ]]; then
  ok "peck_listener.py running (polling mode)"
fi

# 0.4.7 — verify auto-reply wiring (the "pushed but silent inbox" gap).
# peck_responder.py is per-message (spawned via --on-peck), so we don't expect
# a persistent process. Instead check that peck_listener.py's command line
# includes --on-peck pointing to peck_responder.py AND claude CLI exists.
WIRED_ON_PECK=$(echo "$PECK_LISTENER_PIDS" | grep -c -- '--on-peck.*peck_responder' || true)
WIRED_ON_PECK=${WIRED_ON_PECK:-0}
HAVE_CLAUDE="no"
if command -v claude >/dev/null 2>&1; then HAVE_CLAUDE="yes"; fi
if (( WIRED_ON_PECK > 0 )) && [[ "$HAVE_CLAUDE" == "yes" ]]; then
  ok "Auto-reply wired (peck_listener --on-peck → peck_responder, claude CLI present)"
elif (( WIRED_ON_PECK > 0 )) && [[ "$HAVE_CLAUDE" == "no" ]]; then
  warn "Auto-reply wired but claude CLI missing — responder will fire but cannot compose"
  hint "Install claude CLI: https://docs.claude.com/claude-code/install"
elif [[ -n "$PECK_LISTENER_PIDS" ]]; then
  warn "peck_listener running WITHOUT --on-peck wiring — pecks deliver but nothing auto-replies"
  hint "Restart with 0.4.7 supervisord template: $SKILL_DIR/scripts/setup_listeners_supervised.sh --restart"
else
  row "${C_DIM}peck_listener.py not running — auto-reply check skipped${C_RESET}"
fi
if [[ -n "$RESPONDER_PIDS" ]]; then
  row "${C_DIM}peck_responder.py is per-message (spawned via --on-peck), not persistent${C_RESET}"
fi

# ─── 5. Supervisord ───────────────────────────────────────────────────────────
section "Supervisord"
SUP_PID="$SD_DIR/supervisor/supervisord.pid"
if [[ -f "$SUP_PID" ]] && kill -0 "$(cat "$SUP_PID")" 2>/dev/null; then
  ok "Supervisord up (PID $(cat "$SUP_PID"))"
elif [[ -f "$SUP_PID" ]]; then
  warn "Stale PID file at $SUP_PID (process gone)"
  hint "Clean + restart: $SKILL_DIR/scripts/setup_listeners_supervised.sh"
else
  if [[ -n "$LISTENER_PIDS" ]]; then
    row "Supervisord not used (listener started manually — OK)"
  else
    warn "Supervisord not configured AND no listener running"
    hint "Set up: $SKILL_DIR/scripts/setup_listeners_supervised.sh"
  fi
fi

# ─── 6. Recent logs ───────────────────────────────────────────────────────────
section "Recent activity"
RESP_LOG="$SD_DIR/responder.log"
TL_LOG="$SD_DIR/logs/telegram_listener.log"
TL_ERR="$SD_DIR/logs/telegram_listener.err"

if [[ -f "$RESP_LOG" ]]; then
  LAST_RESP=$(tail -1 "$RESP_LOG" 2>/dev/null | head -c 200)
  ok "responder.log: $(wc -l < "$RESP_LOG") lines, last write $(date -r "$RESP_LOG" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || stat -f '%Sm' "$RESP_LOG" 2>/dev/null || echo '?')"
  if [[ -n "$LAST_RESP" ]]; then
    row "Tail: ${C_DIM}${LAST_RESP:0:120}…${C_RESET}"
  fi
  # 0.4.5 — Sam-feedback fix: distinguish "done marker reached" (intentional
  # chain termination — reply sent fine, then chain ends) from "auto_respond
  # disabled in MC" (true config issue). Done-marker exits log
  # "done_marker_detected" alongside the off-flag; if every off-flag is paired
  # with a done-marker line nearby, this is healthy completion, not a stall.
  AR_OFF=$(tail -100 "$RESP_LOG" 2>/dev/null | grep -cE 'auto_respond_off|auto_respond_explicit_off' | tr -d ' \n')
  AR_OFF=${AR_OFF:-0}
  DONE_MARKERS=$(tail -100 "$RESP_LOG" 2>/dev/null | grep -cE 'done_marker_detected|chain_terminated_by_done|reply_sent_and_done' | tr -d ' \n')
  DONE_MARKERS=${DONE_MARKERS:-0}
  if [[ "$AR_OFF" =~ ^[0-9]+$ ]] && (( AR_OFF > 0 )); then
    if (( DONE_MARKERS >= AR_OFF )); then
      ok "$AR_OFF chain completions in last 100 lines (paired with done markers — healthy)"
    elif (( DONE_MARKERS > 0 )); then
      row "${C_DIM}$AR_OFF auto-respond exits ($DONE_MARKERS done-marker paired, $((AR_OFF - DONE_MARKERS)) unpaired)${C_RESET}"
      if (( AR_OFF - DONE_MARKERS > 0 )); then
        warn "$((AR_OFF - DONE_MARKERS)) unpaired auto-respond exit(s) — may indicate MC config drift"
        hint "Check connection has auto_respond=true in Mission Control"
      fi
    else
      warn "$AR_OFF auto-respond exits with no done markers — likely MC config issue"
      hint "Check connection has auto_respond=true in Mission Control"
    fi
  fi
else
  row "${C_DIM}responder.log not yet written${C_RESET}"
fi

if [[ -f "$TL_ERR" ]] && [[ -s "$TL_ERR" ]]; then
  ERR_CT=$(wc -l < "$TL_ERR")
  if (( ERR_CT > 0 )); then
    warn "telegram_listener.err has $ERR_CT lines"
    hint "Tail: tail -20 $TL_ERR"
  fi
fi

# ─── 7. Bridge tunnel ─────────────────────────────────────────────────────────
section "Bridge tunnel"
# Find cloudflared / trycloudflare process if any
TUNNEL_PROC=$(pgrep -fa 'cloudflared\|tryclou' 2>/dev/null | head -1 || true)
if [[ -n "$TUNNEL_PROC" ]]; then
  ok "Tunnel process running"
  row "${C_DIM}${TUNNEL_PROC:0:140}${C_RESET}"
  if echo "$TUNNEL_PROC" | grep -q 'trycloudflare\|quick'; then
    warn "Quick tunnel detected — URL is ephemeral (will change on restart)"
    hint "Production: switch to named cloudflared tunnel or owner DNS"
  fi
else
  # 0.4.5 — Sam-feedback fix: tunnel is only required for webhook delivery
  # mode. If peck_listener.py is running, the box is polling — no inbound
  # tunnel needed. Don't false-positive warn in that case.
  if [[ -n "$PECK_LISTENER_PIDS" ]]; then
    ok "No tunnel needed (polling mode active via peck_listener.py)"
  else
    warn "No cloudflared/tunnel process detected"
    hint "Bridge may not be exposed externally (or start peck_listener.py for polling mode)"
  fi
fi

# Try local healthz
if command -v curl >/dev/null 2>&1; then
  for port in 8787 8788 8789 8800 8080; do
    if HZ=$(curl -s -m 2 "http://localhost:$port/healthz" 2>/dev/null); then
      if echo "$HZ" | grep -q '"ok"'; then
        ok "Local healthz on :$port → $(echo "$HZ" | head -c 80)"
        break
      fi
    fi
  done
fi

# ─── 8. Summary ───────────────────────────────────────────────────────────────
echo
echo "${C_BOLD}── Summary ──${C_RESET}"
echo "  ${C_GREEN}✓ healthy: $HEALTH_OK${C_RESET}"
echo "  ${C_YELLOW}⚠ warnings: $HEALTH_WARN${C_RESET}"
echo "  ${C_RED}✗ failures: $HEALTH_FAIL${C_RESET}"
echo
echo "${C_DIM}This report contains no secrets and is safe to paste publicly.${C_RESET}"
echo
exit 0
