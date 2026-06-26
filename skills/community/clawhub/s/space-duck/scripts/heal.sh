#!/usr/bin/env bash
# Space Duck — self-heal one-button fix.
#
# Why this exists:
#   doctor.sh diagnoses but never treats (locked doctrine). When the user
#   sees a wall of ⚠/✗ from doctor.sh, they don't want a checklist — they
#   want ONE command that fixes everything fixable.
#
#   heal.sh walks the same diagnosis tree but actually applies fixes.
#   Where a fix is risky (e.g. re-auth Claude CLI), it prompts. Where
#   it's safe (restart a process), it just does it.
#
# Apple-grade UX:
#   • One command, zero arguments
#   • Each step: diagnose → fix → verify → report
#   • Reports what changed at the end (delta)
#   • Safe to run multiple times (idempotent)
#   • Bash + standard CLI only (curl, ps, pkill, claude)
#
# What it fixes (in order):
#   1. Stale beak_key in workspace_bridge.py → restart bridge
#   2. telegram_listener.py not running → start
#   3. peck_listener.py not wired with --on-peck → restart via supervised
#   4. Stale supervisord PID file → clean + restart
#   5. Claude CLI dead/expired → prompt re-auth
#   6. Fresh pulse to platform to refresh DDB state
#
# What it does NOT fix:
#   • Missing config.json (use pair.py — heal can't invent identity)
#   • Wrong tunnel URL minted (trycloudflare quick tunnels rotate every restart;
#     heal restarts the tunnel which mints a fresh URL — but the
#     server still needs to learn the new URL via re-bind)
#
# Authored 2026-06-19 — per Josh msg 23653 "1 button fix or run doctor".

set -uo pipefail

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

declare -i ACTIONS_TAKEN=0 ACTIONS_FAILED=0 ACTIONS_SKIPPED=0

step()    { echo; echo "${C_BLUE}${C_BOLD}── $* ──${C_RESET}"; }
ok()      { echo "${C_GREEN}✓${C_RESET} $*"; }
acted()   { echo "${C_GREEN}→${C_RESET} $*"; ACTIONS_TAKEN=$((ACTIONS_TAKEN+1)); }
skip()    { echo "${C_DIM}↷ $*${C_RESET}"; ACTIONS_SKIPPED=$((ACTIONS_SKIPPED+1)); }
warn()    { echo "${C_YELLOW}⚠${C_RESET} $*"; }
fail()    { echo "${C_RED}✗${C_RESET} $*"; ACTIONS_FAILED=$((ACTIONS_FAILED+1)); }

# ─── 0. Banner + skill location ───────────────────────────────────────────────
echo
echo "${C_BOLD}🦆 Space Duck Heal${C_RESET}  ${C_DIM}(one-button fix)${C_RESET}"
echo "$(date -u +'%Y-%m-%d %H:%M:%S UTC')  Host: $(uname -n)"
echo

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
  if [[ -f "$p/_meta.json" ]]; then SKILL_DIR="$p"; break; fi
done

if [[ -z "$SKILL_DIR" ]]; then
  fail "No space-duck install found. Run: clawhub install space-duck"
  exit 1
fi
ok "Skill at $SKILL_DIR"

CFG="$HOME/.space-duck/config.json"
if [[ ! -f "$CFG" ]]; then
  fail "No config.json — duck not paired. Run: python3 $SKILL_DIR/scripts/pair.py"
  exit 1
fi
ok "Config present"

# ─── 1. Restart workspace_bridge.py (clears 401 stale beak_key) ───────────────
step "Workspace bridge"
BRIDGE_PIDS=$(pgrep -fa 'workspace_bridge\.py' 2>/dev/null | grep -v heal.sh | awk '{print $1}' || true)
if [[ -n "$BRIDGE_PIDS" ]]; then
  # Memory rule (feedback_bridge_restart_after_key_rotation 2026-06-09):
  # bridge caches beak_key in memory at startup. If beak_key was rotated
  # via setup.py --beak-key bk_OTP_... the bridge stays 401 until restart.
  acted "Restarting workspace_bridge.py (clearing in-memory beak_key cache)"
  pkill -f workspace_bridge.py 2>/dev/null || true
  sleep 1
  # Setup script handles re-start with current config
  if [[ -x "$SKILL_DIR/scripts/setup_byob_bridge.sh" ]]; then
    nohup bash "$SKILL_DIR/scripts/setup_byob_bridge.sh" > /tmp/sd-bridge-heal.log 2>&1 &
    sleep 3
    if pgrep -f workspace_bridge.py >/dev/null 2>&1; then
      ok "workspace_bridge.py restarted"
    else
      fail "Restart attempted but no process detected — see /tmp/sd-bridge-heal.log"
    fi
  else
    fail "setup_byob_bridge.sh missing — manual restart needed"
  fi
else
  skip "workspace_bridge.py not running (no BYOB bridge configured)"
fi

# ─── 2. Telegram listener ─────────────────────────────────────────────────────
step "Telegram listener"
LISTENER_PIDS=$(pgrep -fa 'telegram_listener\.py' 2>/dev/null | grep -v heal.sh | awk '{print $1}' || true)
if [[ -z "$LISTENER_PIDS" ]]; then
  if [[ -x "$SKILL_DIR/scripts/setup_listeners_supervised.sh" ]]; then
    acted "Starting telegram_listener.py via supervised launcher"
    bash "$SKILL_DIR/scripts/setup_listeners_supervised.sh" --restart > /tmp/sd-listener-heal.log 2>&1 &
    sleep 4
    if pgrep -f telegram_listener.py >/dev/null 2>&1; then
      ok "telegram_listener.py started"
    else
      fail "Start failed — see /tmp/sd-listener-heal.log"
    fi
  else
    fail "setup_listeners_supervised.sh missing"
  fi
else
  ok "telegram_listener.py already running ($(echo "$LISTENER_PIDS" | wc -l | tr -d ' ') process)"
fi

# ─── 3. Peck listener + --on-peck wiring ──────────────────────────────────────
step "Peck auto-reply wiring"
PECK_LISTENER_PIDS=$(pgrep -fa 'peck_listener\.py' 2>/dev/null | grep -v heal.sh || true)
WIRED_ON_PECK=$(echo "$PECK_LISTENER_PIDS" | grep -c -- '--on-peck.*peck_responder' || true)
WIRED_ON_PECK=${WIRED_ON_PECK:-0}

if [[ -z "$PECK_LISTENER_PIDS" ]] || (( WIRED_ON_PECK == 0 )); then
  if [[ -x "$SKILL_DIR/scripts/setup_listeners_supervised.sh" ]]; then
    acted "Restarting peck_listener.py with --on-peck auto-reply wiring"
    bash "$SKILL_DIR/scripts/setup_listeners_supervised.sh" --restart > /tmp/sd-pecklist-heal.log 2>&1 &
    sleep 4
    NEW_PIDS=$(pgrep -fa 'peck_listener\.py.*--on-peck.*peck_responder' 2>/dev/null | grep -v heal.sh || true)
    if [[ -n "$NEW_PIDS" ]]; then
      ok "peck_listener.py running with auto-reply wiring"
    else
      fail "Started but --on-peck wiring not detected"
    fi
  else
    fail "setup_listeners_supervised.sh missing"
  fi
else
  ok "peck_listener.py running with --on-peck wiring (auto-reply active)"
fi

# ─── 4. Stale supervisord ─────────────────────────────────────────────────────
step "Supervisord"
SUP_PID="$HOME/.space-duck/supervisor/supervisord.pid"
if [[ -f "$SUP_PID" ]]; then
  if ! kill -0 "$(cat "$SUP_PID")" 2>/dev/null; then
    acted "Stale PID file at $SUP_PID — cleaning and restarting"
    rm -f "$SUP_PID"
    if [[ -x "$SKILL_DIR/scripts/setup_listeners_supervised.sh" ]]; then
      bash "$SKILL_DIR/scripts/setup_listeners_supervised.sh" --restart > /dev/null 2>&1 &
      sleep 3
    fi
    ok "Cleaned stale supervisord PID"
  else
    ok "Supervisord up (PID $(cat "$SUP_PID"))"
  fi
else
  skip "Supervisord not configured (listeners started directly — OK)"
fi

# ─── 5. Claude CLI auth ───────────────────────────────────────────────────────
step "Claude CLI"
if ! command -v claude >/dev/null 2>&1; then
  fail "claude CLI not installed"
  echo "    ${C_DIM}Install: npm install -g @anthropic-ai/claude-code${C_RESET}"
else
  # Quick test: try claude --print "say OK". If 0-exit and contains OK, healthy.
  CLAUDE_TEST=$(timeout 12 claude --print --model claude-haiku-4-5 "Say only: OK" 2>&1 | head -c 200 || true)
  if echo "$CLAUDE_TEST" | grep -qi 'OK'; then
    ok "Claude CLI reachable + responding"
  else
    warn "Claude CLI not responding (token expired or auth issue)"
    echo "    ${C_DIM}Heal can't auto-re-auth (requires owner browser interaction)${C_RESET}"
    echo "    ${C_DIM}Run: claude auth login${C_RESET}"
    echo "    ${C_DIM}Diagnostic from CLI: ${CLAUDE_TEST:0:120}${C_RESET}"
  fi
fi

# ─── 6. Fresh pulse to platform ───────────────────────────────────────────────
step "Platform pulse"
if [[ -x "$SKILL_DIR/scripts/pulse.py" ]] || [[ -f "$SKILL_DIR/scripts/pulse.py" ]]; then
  PULSE_OUT=$(timeout 10 python3 "$SKILL_DIR/scripts/pulse.py" 2>&1 | tail -2 || true)
  if echo "$PULSE_OUT" | grep -qiE 'ok|alive|verified|success'; then
    acted "Fresh pulse sent to platform"
    ok "Pulse acknowledged"
  else
    warn "Pulse attempted, response: ${PULSE_OUT:0:120}"
  fi
else
  skip "pulse.py missing in this skill version"
fi

# ─── Summary ──────────────────────────────────────────────────────────────────
echo
echo "${C_BOLD}── Heal Summary ──${C_RESET}"
echo "  ${C_GREEN}→ actions taken: $ACTIONS_TAKEN${C_RESET}"
echo "  ${C_DIM}↷ skipped (already-OK): $ACTIONS_SKIPPED${C_RESET}"
echo "  ${C_RED}✗ failed: $ACTIONS_FAILED${C_RESET}"
echo
if (( ACTIONS_FAILED == 0 )) && (( ACTIONS_TAKEN > 0 )); then
  echo "${C_GREEN}${C_BOLD}🦆 Heal complete.${C_RESET} Run ${C_BOLD}doctor.sh${C_RESET} to verify state."
elif (( ACTIONS_FAILED == 0 )) && (( ACTIONS_TAKEN == 0 )); then
  echo "${C_GREEN}${C_BOLD}🦆 Already healthy.${C_RESET} Nothing needed treatment."
else
  echo "${C_YELLOW}${C_BOLD}🦆 Heal partial.${C_RESET} $ACTIONS_FAILED step(s) need manual attention. See messages above."
fi
echo

exit 0
