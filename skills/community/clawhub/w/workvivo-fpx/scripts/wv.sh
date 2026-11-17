# workvivo-fpx helper — source me (bash or zsh):
#
#   export WORKVIVO_HOST=acme.workvivo.us     # your org's Workvivo host
#   source <skill>/scripts/wv.sh
#   wv_get user | jq '{full_name, job_title}'
#   wv_search 'benefits enrollment' article event | jq '.data[] | {type, title, url}'
#
# Every call goes through the user's signed-in Workvivo tab via `fpx` (profile
# `workvivo`, override with WV_PROFILE). Workvivo's /api/* routes are
# authenticated by the browser's session cookie PLUS a CSRF header: the
# Laravel session token the page embeds as <meta name="csrf_token">. GETs need
# it too — without it every /api call answers 401 {"message":"Unauthenticated."}.
# The token is read once from the home page (the SPA shell, ~600 KB) and kept
# in WV_CSRF for this shell; a 401 refreshes it once and retries.
#
# Return codes: 0 ok · 1 usage · 2 bridge down · 3 bot wall · 4 upstream HTTP
# error (body on stdout) · 5 not signed in to Workvivo in the paired browser.
#
# Nothing is written to disk: no state file, so nothing can collide with
# workvivo-mcp's own state.

WV_PROFILE="${WV_PROFILE:-workvivo}"

_wv_base() {
  if [ -z "${WORKVIVO_HOST:-}" ]; then
    echo 'wv: set WORKVIVO_HOST to your Workvivo host, e.g. acme.workvivo.us' >&2
    return 1
  fi
  printf 'https://%s' "${WORKVIVO_HOST#https://}"
}

# Read the session CSRF token off the signed-in home page into WV_CSRF.
wv_init() {
  local base page rc
  base="$(_wv_base)" || return 1
  page="$(fpx get "$base/" -p "$WV_PROFILE" 2>/dev/null)"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "wv: fetching $base/ failed (fpx exit $rc) — run 'fpx health -p $WV_PROFILE'" >&2
    return "$rc"
  fi
  WV_CSRF="$(printf '%s' "$page" | grep -oE 'name="csrf_token" content="[^"]+"' | head -n 1 | sed -E 's/.*content="([^"]+)"/\1/')"
  if [ -z "$WV_CSRF" ]; then
    echo "wv: no session token on $base/ — sign in to Workvivo (SSO) in the browser paired with fpx profile '$WV_PROFILE', then retry" >&2
    return 5
  fi
  export WV_CSRF
}

# _wv_call <get|post-json> <api-path> [json-body]
_wv_call() {
  local verb="$1" api="$2" body="${3:-}" base out rc attempt
  base="$(_wv_base)" || return 1
  # (not `path` — in zsh that name is tied to $PATH)
  api="${api#/}"
  api="${api#api/}"
  for attempt in 1 2; do
    if [ -z "${WV_CSRF:-}" ]; then
      wv_init || return $?
    fi
    if [ "$verb" = get ]; then
      out="$(fpx get "$base/api/$api" -p "$WV_PROFILE" \
        -H 'X-Requested-With: XMLHttpRequest' -H 'Accept: application/json' \
        -H "X-CSRF-Token: $WV_CSRF" 2>/dev/null)"
    else
      out="$(fpx post-json "$base/api/$api" "$body" -p "$WV_PROFILE" \
        -H 'X-Requested-With: XMLHttpRequest' -H 'Accept: application/json' \
        -H "X-CSRF-Token: $WV_CSRF" 2>/dev/null)"
    fi
    rc=$?
    # A stale token (or a signed-out browser) answers 401 Unauthenticated:
    # re-read the token once, then give up and let the caller see it.
    if [ "$rc" -eq 4 ] && [ "$attempt" -eq 1 ] && printf '%s' "$out" | grep -q 'Unauthenticated'; then
      WV_CSRF=''
      continue
    fi
    printf '%s\n' "$out"
    return "$rc"
  done
}

# wv_get <api-path>   e.g. wv_get 'activity'  /  wv_get 'people?query=smith&page=1'
wv_get() {
  if [ -z "${1:-}" ]; then echo 'usage: wv_get <api-path>' >&2; return 1; fi
  _wv_call get "$1"
}

# wv_search <query> [type…] — federated search. Types (default: the common
# set): article update event user space docs page kudos question_post term
# goal comment livestream podcast file welcome anniversary birthday apps
# question_post_answer. Optional WV_PAGE (default 1).
# NOTE: Workvivo records each search in the user's own search history.
wv_search() {
  local q="${1:-}" types body t first=1
  if [ -z "$q" ]; then echo 'usage: wv_search <query> [type…]' >&2; return 1; fi
  shift
  if [ "$#" -eq 0 ]; then
    set -- article update event user space docs page kudos question_post
  fi
  types=''
  for t in "$@"; do
    if [ "$first" -eq 1 ]; then first=0; else types="$types,"; fi
    types="$types\"$t\""
  done
  # JSON-escape the query (backslash and double quote).
  q="$(printf '%s' "$q" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')"
  body="{\"page\":${WV_PAGE:-1},\"query\":\"$q\",\"types\":[$types]}"
  _wv_call post-json federated-search "$body"
}
