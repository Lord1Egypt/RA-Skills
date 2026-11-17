#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED — reference only. Pure manual flow: the AI never runs this script.
# The user confirms which browser has the MonsterGet extension installed
# (SKILL.md Step I). This script is kept for history; do not call it.
# Its behavior is now a no-op: detect_browser() in lib.sh only reads the
# saved `browser_pref` (no disk scan, no extension probe).
# ═══════════════════════════════════════════════════════════════════════════
# detect-browser.sh — detect which browser(s) have the MonsterGet extension.
#
# Usage:  bash detect-browser.sh
# Reads:  state.json (browser_pref — the user's saved choice, honored when valid)
# Writes: state.json (os, browser, browser_exe, browser_fullpath, extension, multiple)
# Stdout: {"os":"windows","browser":"edge","browsers":["edge","chrome"],
#          "browser_exe":"msedge","extension":true,"multiple":true,
#          "chosen_by":"default","need_choice":true}
#   browser      = the chosen browser (pref if still valid, else first found)
#   browsers     = ALL browsers that have the extension
#   multiple     = more than one browser has the extension
#   chosen_by    = preference | default | only_one
#   need_choice  = multiple browsers AND no valid saved choice — caller should
#                  ask the user (see choose-browser.sh), do NOT scrape yet
# Exit:   0 = extension found, 1 = not found (stdout still valid JSON)
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

detect_browser
EXT=false
[ "$BROWSER" != "none" ] && EXT=true

MULTIPLE=false
[ "$(printf '%s' "$BROWSERS" | tr -cd ' ' | wc -c)" -gt 0 ] && MULTIPLE=true

NEED=false
[ "$EXT" = true ] && [ "$MULTIPLE" = true ] && [ "$CHOSEN_BY" = "default" ] && NEED=true

state_set os "$(detect_os)"
state_set browser "$BROWSER"
state_set browser_exe "$BROWSER_EXE"
state_set browser_fullpath "$BROWSER_FULLPATH"
state_set extension "$EXT"
state_set multiple "$MULTIPLE"
state_set chosen_by "$CHOSEN_BY"
state_set need_choice "$NEED"
state_set browsers "$BROWSERS"

printf '{"os":"%s","browser":"%s","browsers":%s,"browser_exe":"%s","extension":%s,"multiple":%s,"chosen_by":"%s","need_choice":%s}\n' \
  "$(detect_os)" "$BROWSER" "$(browser_choices_json)" "$BROWSER_EXE" \
  "$EXT" "$MULTIPLE" "$CHOSEN_BY" "$NEED"

[ "$EXT" = true ]
