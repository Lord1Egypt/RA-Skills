#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED — reference only. Pure manual flow: the AI never runs this script.
# Login conditions are confirmed by the user manually (SKILL.md Step III).
# This script is kept for history; do not call it.
# ═══════════════════════════════════════════════════════════════════════════
# check-login.sh — verify a login by opening the platform's login-check page and polling.
#
# Usage:  bash check-login.sh monsterget|tiktok
# Reads:  state.json (browser_pref)
# Writes: state.json (monsterget_login | tiktok_login)
# Stdout: {"logged_in":true,"task_id":"...","target":"tiktok"}
# Exit:   0 = logged in, 1 = not logged in / could not check
#
# Env: MONSTERGET_POLLS — poll count (default 12 × 5s = 60s).
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

TARGET="${1:-monsterget}"
case "$TARGET" in
  monsterget|tiktok) : ;;
  *) echo '{"logged_in":false,"error":"unknown target"}'; exit 1 ;;
esac

detect_browser
if [ "$BROWSER" = "none" ]; then
  echo '{"logged_in":false,"error":"extension not detected in any browser"}'
  exit 1
fi

TASK_ID="$(generate_task_id)"
if [ -z "$TASK_ID" ]; then
  echo '{"logged_in":false,"error":"platform unreachable"}'
  exit 1
fi

if [ "$TARGET" = "tiktok" ]; then
  TK="$(curl -s --max-time 10 -X POST "$BASE_URL/api/agent/login-check-target" \
        -H "Content-Type: application/json" -d '{"target":"tiktok"}' 2>/dev/null)"
  TK_ID="$(echo "$TK" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')"
  [ -n "$TK_ID" ] && TASK_ID="$TK_ID"
  CHECK_URL="$SITE_URL/login-check-target.html?auto=1&agentTaskId=$TASK_ID&target=tiktok"
else
  CHECK_URL="$SITE_URL/login-check.html?auto=1&agentTaskId=$TASK_ID"
fi

# Fire-and-forget: open the page, then poll. Never wait for the user.
open_url "$CHECK_URL"

LOGIN=false
i=0
while [ "$i" -lt "$POLLS" ]; do
  i=$((i + 1))
  R="$(curl -s --max-time 10 "$BASE_URL/api/agent/login-check/$TASK_ID" 2>/dev/null)"
  if echo "$R" | grep -q '"logged_in":true'; then
    LOGIN=true
    break
  fi
  sleep 5
done

state_set "${TARGET}_login" "$LOGIN"

printf '{"logged_in":%s,"task_id":"%s","target":"%s","browser":"%s"}\n' \
  "$LOGIN" "$TASK_ID" "$TARGET" "$BROWSER"

[ "$LOGIN" = true ]
