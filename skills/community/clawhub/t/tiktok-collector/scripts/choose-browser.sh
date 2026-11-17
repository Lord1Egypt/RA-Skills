#!/usr/bin/env bash
# choose-browser.sh — save the user's browser choice.
#
# Usage:  bash choose-browser.sh edge|chrome
# Pure manual flow: the user verbally confirmed which browser has the
# MonsterGet extension installed. No disk scan, no validation — whatever
# the user said is saved. The choice persists across sessions.
# Reads:  state.json (browser_pref — nothing read, nothing validated)
# Writes: state.json (browser_pref = the chosen browser)
# Stdout: {"ok":true,"browser":"edge","browser_exe":"msedge","browsers":["edge"],"chosen_by":"preference"}
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

WANT="${1:-}"
case "$WANT" in
  edge|chrome) : ;;
  *) echo '{"ok":false,"error":"usage: choose-browser.sh edge|chrome"}'; exit 1 ;;
esac

# ARCHIVED — pure manual flow. The user confirmed which browser has the
# extension installed (SKILL.md Step I). We save it without any disk scan.
# The old detection+validation code is kept as reference:
#
#   detect_browser
#   if [ "$BROWSER" = "none" ]; then
#     echo '{"ok":false,"error":"no browser has the MonsterGet extension — install it first"}'
#     exit 1
#   fi
#   case " $BROWSERS " in
#     *" $WANT "*) : ;;
#     *)
#       printf '{"ok":false,"error":"%s does not have the MonsterGet extension","browsers":%s}\n' \
#         "$WANT" "$(browser_choices_json)"
#       exit 1
#       ;;
#   esac

state_set browser_pref "$WANT"
detect_browser   # re-resolve so the reported browser/exe reflect the new choice

printf '{"ok":true,"browser":"%s","browser_exe":"%s","browsers":%s,"chosen_by":"%s"}\n' \
  "$BROWSER" "$BROWSER_EXE" "$(browser_choices_json)" "$CHOSEN_BY"
