#!/usr/bin/env bash
# run-scrape.sh — run one scrape end-to-end and download the CSV.
#
# Usage:  bash run-scrape.sh <pagePath> <param> <value> [count]
#   bash run-scrape.sh /tiktok-search-video query "mike tyson" 20
#   bash run-scrape.sh /tiktok-tag query beauty 30
#   bash run-scrape.sh /tiktok-profile usernames "mike,jenifer,tiktok" 3
#
# Reads:  state.json (browser_pref) — which browser the user chose during installation
# Writes: state.json (last_task_id, last_scrape_url)
# Stdout: {"status":"ready","taskId":"...","file":"mike-20-....csv","rowCount":20,"url":"..."}
# Exit:   0 = CSV downloaded, 1 = failed (stdout has status + error)
#
# Fire-and-forget: opens the browser, verifies the process started, polls until ready,
# downloads. Never asks the user anything.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

if [ $# -lt 3 ]; then
  echo '{"status":"failed","error":"usage: run-scrape.sh <pagePath> <param> <value> [count]"}'
  exit 2
fi

PAGEPATH="$1"
PARAM="$2"
VALUE="$3"
COUNT="${4:-}"

detect_browser
if [ "$BROWSER" = "none" ]; then
  echo '{"status":"failed","error":"no browser preference saved — run choose-browser.sh first"}'
  exit 1
fi

# ARCHIVED — pure manual flow. We never scan the disk for the extension and
# never refuse based on "more than one browser detected". The user already
# confirmed which browser to use (SKILL.md Step I-II); browser_pref above IS
# that confirmation.
#
# if [ "$CHOSEN_BY" = "default" ]; then
#   printf '{"status":"need_browser_choice","browsers":%s,"error":"more than one browser has the MonsterGet extension — ask the user which to use, save it with choose-browser.sh, then re-run"}\n' \
#     "$(browser_choices_json)"
#   exit 1
# fi

TASK_ID="$(generate_task_id)"
if [ -z "$TASK_ID" ]; then
  echo '{"status":"failed","error":"platform unreachable"}'
  exit 1
fi
state_set last_task_id "$TASK_ID"

COUNT_ARG=""
[ -n "$COUNT" ] && COUNT_ARG="&count=$COUNT"
URL="$SITE_URL${PAGEPATH}?auto=1&agentTaskId=${TASK_ID}&${PARAM}=$(urlencode "$VALUE")${COUNT_ARG}"
state_set last_scrape_url "$URL"

# ---- open + verify the browser process actually started (never ask the user) ----
open_url "$URL"
STARTED=false
for _ in 1 2 3; do
  if browser_running; then STARTED=true; break; fi
  sleep 1
done
if [ "$STARTED" != true ]; then
  # the launch can fail silently (exe not in PATH) — retry via the full path
  open_url "$URL"
  sleep 2
  browser_running && STARTED=true
fi
if [ "$STARTED" != true ]; then
  printf '{"status":"failed","taskId":"%s","url":"%s","error":"browser did not start — open the URL manually in the extension browser"}\n' \
    "$TASK_ID" "$URL"
  exit 1
fi

# ---- poll until ready (up to 5 minutes) ----
# Note: `not_found` (task not created YET) is NOT terminal — the page takes 10-20s
# to load and POST the task after the browser opens. Treat it as "keep waiting";
# only give up when the full loop expires (the final STATUS then reports it below).
STATUS="{}"
for _ in $(seq 1 60); do
  STATUS="$(curl -s --max-time 10 "$BASE_URL/api/agent/delivery/task/$TASK_ID/status" 2>/dev/null)"
  case "$STATUS" in
    *'"status":"ready"'*)      break ;;
    *'"status":"downloaded"'*) break ;;
    *'"status":"failed"'*)     break ;;
  esac
  sleep 5
done

FILENAME="$(echo "$STATUS" | sed -n 's/.*"filename":"\([^"]*\)".*/\1/p')"
ROWCOUNT="$(echo "$STATUS" | sed -n 's/.*"resultCount":\([0-9]*\).*/\1/p')"
STATUSVAL="$(echo "$STATUS" | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')"

case "$STATUSVAL" in
  ready)
    DL_DIR="$(resolve_download_dir)"
    if ! mkdir -p "$DL_DIR" 2>/dev/null; then
      printf '{"status":"failed","taskId":"%s","url":"%s","error":"cannot create download dir: %s"}\n' \
        "$TASK_ID" "$URL" "$DL_DIR"
      exit 1
    fi
    (cd "$DL_DIR" && curl -s --max-time 60 -OJ "$BASE_URL/api/agent/delivery/task/$TASK_ID/data" 2>/dev/null)
    printf '{"status":"ready","taskId":"%s","file":"%s","dir":"%s","rowCount":%s,"url":"%s"}\n' \
      "$TASK_ID" "$FILENAME" "$DL_DIR" "${ROWCOUNT:-0}" "$URL"
    ;;
  downloaded)
    printf '{"status":"already_downloaded","taskId":"%s","error":"CSV is tombstoned (one download only) — generate a new taskId and scrape again"}\n' \
      "$TASK_ID"
    exit 1
    ;;
  failed)
    printf '{"status":"failed","taskId":"%s","url":"%s","error":"task failed on the platform"}\n' \
      "$TASK_ID" "$URL"
    exit 1
    ;;
  *)
    if echo "$STATUS" | grep -q 'not_found'; then
      printf '{"status":"not_found","taskId":"%s","url":"%s","error":"task was never created — the page did not load or the extension is not ready"}\n' \
        "$TASK_ID" "$URL"
    else
      printf '{"status":"timeout","taskId":"%s","url":"%s","error":"not ready within 5 minutes — extension missing, not logged in, or the tab was closed"}\n' \
        "$TASK_ID" "$URL"
    fi
    exit 1
    ;;
esac
