#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED — reference only. Pure manual flow: the AI never runs this script.
# The user manually confirms all three conditions (extension, monsterget login,
# TikTok login) without code verification (SKILL.md Step I-III).
# This script is kept for history; do not call it.
# ═══════════════════════════════════════════════════════════════════════════
# preflight.sh — silent programmatic preflight (SKILL.md Step 0.6).
#
# Runs: browser/extension detection → platform reachability → MonsterGet login → TikTok login.
# No user interaction, no questions. Short login probes (3 × 5s) are enough to detect an
# already-finished setup; if they time out, escalate to the interactive Step 0 flow.
#
# Usage:  bash preflight.sh
# Writes: state.json (extension, platform_reachable, monsterget_login, tiktok_login, checked_at)
# Stdout: {"ready":true,"next":"","extension":true,"platform_reachable":true,
#          "monsterget_login":true,"tiktok_login":true,"browser":"edge","os":"windows"}
#   ready = all 3 user-facing steps pass   next = first failing step, "" when ready
#   next is one of: extension | monsterget_login | tiktok_login | platform_reachable
# Exit:   0 = all checks pass, 1 = at least one failed (stdout says which)
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

# ① extension + browser (local file scan, ~0.1s)
bash "$SCRIPT_DIR/detect-browser.sh" >/dev/null 2>&1
EXT=false
[ "$(state_get browser)" != "none" ] && EXT=true

# Several browsers have the extension and the user hasn't picked one. The login
# checks below would run against an arbitrary guess and report false negatives,
# so skip them — the agent must ask the user first (choose-browser.sh).
NEED_CHOICE=false
[ "$EXT" = true ] && [ "$(state_get need_choice)" = true ] && NEED_CHOICE=true

# ② platform reachability
HTTP="$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE_URL/api/agent/generate-task-id" 2>/dev/null)"
REACH=false
[ "$HTTP" = "200" ] && REACH=true

# ③ logins — only meaningful when the extension exists, the browser is settled,
#    and the platform answers
MG=false
TK=false
if [ "$EXT" = true ] && [ "$REACH" = true ] && [ "$NEED_CHOICE" = false ]; then
  MONSTERGET_POLLS=3 bash "$SCRIPT_DIR/check-login.sh" monsterget >/dev/null 2>&1 && MG=true
  # tiktok probe uses more polls because the target-site login check
  # (login-check-target.html) inserts a random 5-10s anti-detection delay
  # before opening the TikTok window, then the extension takes another
  # ~3-5s to check and relay back.  6 polls × 5s = ~30s cap is enough.
  MONSTERGET_POLLS=6 bash "$SCRIPT_DIR/check-login.sh" tiktok    >/dev/null 2>&1 && TK=true
fi

state_set extension "$EXT"
state_set platform_reachable "$REACH"
state_set monsterget_login "$MG"
state_set tiktok_login "$TK"
state_set checked_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# `next` = the first step the agent must guide the user through. Empty string
# means everything passed and the user can scrape right away.
NEXT=""
if [ "$EXT" != true ]; then
  NEXT="extension"
elif [ "$NEED_CHOICE" = true ]; then
  NEXT="choose_browser"
elif [ "$MG" != true ]; then
  NEXT="monsterget_login"
elif [ "$TK" != true ]; then
  NEXT="tiktok_login"
elif [ "$REACH" != true ]; then
  NEXT="platform_reachable"
fi

READY=false
[ -z "$NEXT" ] && READY=true

BROWSER_NAME="$(state_get browser)"
BROWSERS_LIST="$(state_get browsers)"

printf '{"ready":%s,"next":"%s","extension":%s,"platform_reachable":%s,"monsterget_login":%s,"tiktok_login":%s,"browser":"%s","browsers":"%s","need_choice":%s,"os":"%s"}\n' \
  "$READY" "$NEXT" "$EXT" "$REACH" "$MG" "$TK" \
  "$BROWSER_NAME" "$BROWSERS_LIST" "$NEED_CHOICE" "$(detect_os)"

[ -z "$NEXT" ]
