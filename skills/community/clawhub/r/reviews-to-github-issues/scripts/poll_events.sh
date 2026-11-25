# Poll AppGoat events (GET /v1/events, free) and remember which ones were handled.
#
#   bash poll_events.sh poll [--type negative_review_spike,review_spike,rating_drop] [--app <app>] [--state <file>]
#   bash poll_events.sh ack  [--state <file>]
#
# poll   prints the events not handled yet, oldest first, one JSON object per line, and keeps them
#        as "pending" in the state file. First run: events of the last 24 hours.
# ack    marks the pending events as handled: `since` moves to the newest created_at and their ids
#        are remembered (since= is inclusive, so the newest ones come back once and are skipped).
#
# Run ack only after the events were handled; if a run fails, the next poll returns them again.
# State file default: .appgoat/events-state.json (add .appgoat/ to .gitignore).
# Requires curl, jq and APPGOAT_API_KEY. CURL overrides the binary, APPGOAT_API_URL the base URL.

set -euo pipefail

CURL=${CURL:-curl}
API=${APPGOAT_API_URL:-https://api.appgoat.ai/v1}

cmd=${1:-}
shift || true
types=negative_review_spike,review_spike,rating_drop
app='' state=.appgoat/events-state.json
while [ $# -gt 0 ]; do
  case "$1" in
    --type) types=$2; shift 2 ;;
    --app) app=$2; shift 2 ;;
    --state) state=$2; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -f "$state" ] || { mkdir -p "$(dirname "$state")"; echo '{}' >"$state"; }

save() { # jq filter applied to the state file
  local tmp
  tmp=$(mktemp)
  jq "$@" "$state" >"$tmp" && mv "$tmp" "$state"
}

case "$cmd" in
  poll)
    : "${APPGOAT_API_KEY:?set APPGOAT_API_KEY}"
    since=$(jq -r '.since // empty' "$state")
    if [ -z "$since" ]; then
      since=$(jq -nr 'now - 86400 | strftime("%Y-%m-%dT%H:%M:%SZ")')
    fi
    pages=$(mktemp)
    trap 'rm -f "$pages"' EXIT
    cursor=
    while :; do
      page=$($CURL -sS -f -G -H "x-api-key: $APPGOAT_API_KEY" "$API/events" \
        --data-urlencode "since=$since" --data-urlencode "type=$types" -d limit=200 \
        ${app:+--data-urlencode "app=$app"} ${cursor:+--data-urlencode "cursor=$cursor"})
      printf '%s\n' "$page" | jq -c '.data[]' >>"$pages"
      cursor=$(printf '%s\n' "$page" | jq -r '.meta.next_cursor // empty')
      [ -n "$cursor" ] || break
    done
    new=$(jq -s --slurpfile st "$state" \
      '($st[0].seen // []) as $seen | unique_by(.id) | map(select(.id as $id | $seen | index($id) | not)) | sort_by(.created_at)' \
      "$pages")
    save --argjson new "$new" '.pending = $new'
    printf '%s\n' "$new" | jq -c '.[]'
    ;;
  ack)
    save '(.pending // []) as $p
      | if ($p | length) == 0 then .
        else .since = ([$p[].created_at, (.since // empty)] | max)
          | .seen = (((.seen // []) + [$p[].id]) | .[-500:])
        end
      | .pending = []'
    jq -r '"handled up to \(.since // "nothing yet")"' "$state"
    ;;
  *)
    echo "usage: poll_events.sh poll|ack [--type a,b] [--app <app>] [--state <file>]" >&2
    exit 2
    ;;
esac
