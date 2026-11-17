# warapp-api helper — source me (bash or zsh), then pipe into jq:
#
#   source <skill>/scripts/warapp.sh
#   warapp_game 45670418 | jq '{name, state}'
#   warapp_map 45670418 | jq '.bonuses | length'
#
# Every call is POST https://war.app/API/GameFeed?GameID=<n> with the form body
# Email=<email>&APIToken=<token>. Credentials come from WARAPP_EMAIL /
# WARAPP_API_TOKEN, else from the dotenv file WARAPP_ENV_FILE (default
# ~/.config/warapp-mcp/.env — the same file warapp-mcp reads). The environment
# wins over the file. The file is parsed, never sourced, and the credentials
# live only in function-local variables: they are never exported, never put
# on curl's command line (the body goes in on stdin) and never printed — an
# upstream error has both scrubbed before it reaches stderr.
#
# Extra Param=value arguments are checked against a conservative character set, and
# curl runs with URL globbing off, reads no config file (-q, which must come first),
# speaks only the checked origin's protocol and follows no redirect, so every request
# of a call (one, or two when curl's single retry answers a transient error) goes to
# the checked origin and nowhere else. A loopback test origin bypasses every proxy;
# war.app keeps the environment's proxy settings.
#
# Return codes: 0 ok · 1 usage (bad game id, bad extra argument, refused
# WARAPP_BASE_URL) · 2 no credentials ·
# 3 Auth failed (wrong email/token) · 4 no such game · 5 anything else
# (network, HTTP error, non-JSON answer, other GameFeed error).
#
# war.app answers errors as HTTP 200 {"termsOfUse": …, "error": …}; these
# functions turn that into the codes above, so a 0 means a real game body.
#
# Variable names avoid `path` and `status` (special in zsh).

# Character classes are spelled out, never ranges: under a UTF-8 locale some shells
# (macOS /bin/bash 3.2) match [A-Za-z0-9] by collation order, letting accented and
# fullwidth letters through. Spelled out, the sets hold ASCII only in every shell and locale.

# _warapp_gameid <id>: a positive whole number below 2^31.
_warapp_gameid() {
  case "${1:-}" in
    '' | *[!0123456789]* | 0*)
      echo "warapp: game id must be a positive whole number, got '${1:-}'" >&2
      return 1
      ;;
  esac
  if [ "${#1}" -gt 10 ] || [ "$1" -gt 2147483647 ]; then
    echo "warapp: game id must be below 2^31, got '$1'" >&2
    return 1
  fi
}

# _warapp_base: print the GameFeed origin. WARAPP_BASE_URL is a test seam only: the
# credentials go in every request, so it is honoured only when it is exactly
# https://war.app or a loopback stand-in (http://127.0.0.1:<port> or
# http://localhost:<port>). Anything else is refused before a request is made.
_warapp_base() {
  local url="${WARAPP_BASE_URL:-https://war.app}" port=''
  case "$url" in
    https://war.app) printf '%s' "$url"; return 0 ;;
    http://127.0.0.1:*) port="${url#http://127.0.0.1:}" ;;
    http://localhost:*) port="${url#http://localhost:}" ;;
  esac
  case "$port" in
    '' | *[!0123456789]*) ;;
    *)
      if [ "${#port}" -le 5 ] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ]; then
        printf '%s' "$url"
        return 0
      fi
      ;;
  esac
  echo "warapp: refusing WARAPP_BASE_URL: it must be https://war.app or http://127.0.0.1:<port> / http://localhost:<port>" >&2
  return 1
}

# _warapp_arg <Name=value>: an extra query parameter. Name is a letter then letters or
# digits; value is letters, digits, '.', '_' or '-' (possibly empty). Nothing that could
# change the query, the URL or the shell's reading of it gets through.
_warapp_arg() {
  local name="${1%%=*}" val="${1#*=}" ok=1
  case "$1" in *=*) ;; *) ok=0 ;; esac
  case "$name" in
    '' | [!ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]* | *[!ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789]*) ok=0 ;;
  esac
  case "$val" in
    *[!ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-]*) ok=0 ;;
  esac
  if [ "$ok" -ne 1 ]; then
    echo "warapp: refusing extra argument: expected Name=value (letters/digits, value also . _ -)" >&2
    return 1
  fi
}

# _warapp_load: fill the CALLER's local _warapp_email/_warapp_token.
_warapp_load() {
  local file line key val
  _warapp_email="${WARAPP_EMAIL:-}"
  _warapp_token="${WARAPP_API_TOKEN:-}"
  file="${WARAPP_ENV_FILE:-$HOME/.config/warapp-mcp/.env}"
  if [ -r "$file" ] && [ -f "$file" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
      line="${line%$'\r'}"
      line="${line#export }"
      case "$line" in *=*) ;; *) continue ;; esac
      key="${line%%=*}"
      val="${line#*=}"
      case "$val" in
        \"*\") val="${val#\"}"; val="${val%\"}" ;;
        \'*\') val="${val#\'}"; val="${val%\'}" ;;
      esac
      case "$key" in
        WARAPP_EMAIL) [ -n "$_warapp_email" ] || _warapp_email="$val" ;;
        WARAPP_API_TOKEN) [ -n "$_warapp_token" ] || _warapp_token="$val" ;;
      esac
    done <"$file"
  fi
  if [ -z "$_warapp_email" ] || [ -z "$_warapp_token" ]; then
    echo "warapp: set WARAPP_EMAIL and WARAPP_API_TOKEN (or put them in $file)." >&2
    echo "warapp: the token is shown at https://war.app/API/GetAPIToken while signed in." >&2
    return 2
  fi
}

# _warapp_uri: URL-encode stdin (kept off argv).
_warapp_uri() {
  jq -sRr @uri
}

# warapp_feed <game-id> [Param=value …]: the raw GameFeed body for one game.
# Extra arguments are appended to the query, e.g. GetSettings=true GetMap=false
# GetHistory=true GetChat=true (each checked by _warapp_arg; anything else exits 1).
warapp_feed() {
  local game="${1:-}" query='' arg body rc err origin proto noproxy _warapp_email _warapp_token
  _warapp_gameid "$game" || return 1
  shift
  origin="$(_warapp_base)" || return 1
  case "$origin" in
    https://*) proto='=https' noproxy="${no_proxy-${NO_PROXY-}}" ;;
    *) proto='=http' noproxy='*' ;;
  esac
  for arg in "$@"; do
    _warapp_arg "$arg" || return 1
    query="$query&$arg"
  done
  _warapp_load || return 2
  body="$(
    printf 'Email=%s&APIToken=%s' \
      "$(printf '%s' "$_warapp_email" | _warapp_uri)" \
      "$(printf '%s' "$_warapp_token" | _warapp_uri)" |
      curl -q --globoff --proto "$proto" --max-redirs 0 --noproxy "$noproxy" \
        -sS --fail-with-body --max-time 30 --retry 1 \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        --data-binary @- \
        "$origin/API/GameFeed?GameID=$game$query"
  )"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "warapp: request to war.app failed (curl exit $rc)" >&2
    return 5
  fi
  if ! printf '%s' "$body" | jq -e 'type == "object"' >/dev/null 2>&1; then
    echo "warapp: war.app answered with something that is not JSON" >&2
    return 5
  fi
  err="$(printf '%s' "$body" | jq -r '.error // empty | tostring')"
  case "$err" in
    '') ;;
    'Auth failed')
      echo "warapp: Auth failed — wrong email or API token. Get the current token at https://war.app/API/GetAPIToken while signed in (changing the password rotates it)." >&2
      return 3
      ;;
    *ServerGameKeyNotFound*)
      echo "warapp: no game $game (or it is not visible to you)" >&2
      return 4
      ;;
    *)
      err="${err//"$_warapp_token"/[redacted]}"
      err="${err//"$_warapp_email"/[redacted]}"
      echo "warapp: war.app error: $err" >&2
      return 5
      ;;
  esac
  printf '%s\n' "$body"
}

# warapp_game <game-id> [Param=value …]: game, players and settings, without the
# map (GetSettings=true GetMap=false). Use warapp_map for the map.
warapp_game() {
  local game="${1:-}"
  _warapp_gameid "$game" || return 1
  shift
  warapp_feed "$game" GetSettings=true GetMap=false "$@"
}

# warapp_map <game-id>: the game's map object. Maps never change for a map id,
# and war.app asks callers to cache, so it is kept in WARAPP_CACHE_DIR
# (default ~/.cache/warapp-mcp) and fetched once per game.
warapp_map() {
  local game="${1:-}" dir mapid out rc
  _warapp_gameid "$game" || return 1
  dir="${WARAPP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/warapp-mcp}"
  if [ -r "$dir/game-$game.map" ]; then
    mapid="$(cat "$dir/game-$game.map")"
    case "$mapid" in
      '' | *[!0123456789]*) ;;
      *)
        if [ -r "$dir/map-$mapid.json" ]; then
          cat "$dir/map-$mapid.json"
          return 0
        fi
        ;;
    esac
  fi
  out="$(warapp_feed "$game")"
  rc=$?
  [ "$rc" -eq 0 ] || return "$rc"
  mapid="$(printf '%s' "$out" | jq -r '.map.id // empty | tostring')"
  case "$mapid" in
    '' | *[!0123456789]*)
      echo "warapp: the response for game $game carries no usable map id" >&2
      return 5
      ;;
  esac
  mkdir -p "$dir" &&
    printf '%s' "$out" | jq '.map' >"$dir/map-$mapid.json.tmp" &&
    mv "$dir/map-$mapid.json.tmp" "$dir/map-$mapid.json" &&
    printf '%s\n' "$mapid" >"$dir/game-$game.map"
  printf '%s' "$out" | jq '.map'
}
