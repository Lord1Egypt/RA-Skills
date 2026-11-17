#!/usr/bin/env bash
# Shell helpers for talking to the SimpliSafe API with curl.
#
# Source this, then use `ss_api`:
#
#   source references/ss-helpers.sh
#   ss_api GET /api/authCheck | jq
#
# Portable across bash and zsh. Requires: curl, jq.
#
# CREDENTIAL HANDLING
#   Reads SIMPLISAFE_REFRESH_TOKEN from the environment, falling back to the
#   simplisafe-mcp repo's .env. It only ever READS that file — SimpliSafe does
#   not rotate refresh tokens, so there is nothing to write back, and the MCP
#   server's own state is never touched.
#
#   The minted access token is cached in this skill's OWN state file under
#   TMPDIR (mode 0600), never in the repo's .env.

SS_CLIENT_ID='42aBZ5lYrVW12jfOuu3CQROitwxg9sN5'
SS_AUTH_URL='https://auth.simplisafe.com/oauth/token'
SS_API_BASE='https://api.simplisafe.com/v1'
SS_TOKEN_CACHE="${TMPDIR:-/tmp}/simplisafe-skill-token.json"

# Resolve the refresh token. Prints it, or fails with an actionable message.
ss_refresh_token() {
  if [ -n "${SIMPLISAFE_REFRESH_TOKEN:-}" ]; then
    printf '%s' "$SIMPLISAFE_REFRESH_TOKEN"
    return 0
  fi

  local env_file="${SIMPLISAFE_ENV_FILE:-$HOME/git/simplisafe-mcp/.env}"
  if [ -f "$env_file" ]; then
    # cut -d= -f2- keeps any '=' inside the token itself.
    local token
    token=$(grep -E '^SIMPLISAFE_REFRESH_TOKEN=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2-)
    if [ -n "$token" ]; then
      printf '%s' "$token"
      return 0
    fi
  fi

  echo "ss_refresh_token: no credential found." >&2
  echo "  Set SIMPLISAFE_REFRESH_TOKEN, or run the one-time login:" >&2
  echo "  node ~/git/simplisafe-mcp/scripts/bootstrap-auth.mjs" >&2
  return 1
}

# Print a valid access token, minting one only when the cache is cold or stale.
# SimpliSafe access tokens last 3600s; refresh 120s early to avoid a race.
ss_access_token() {
  local now
  now=$(date +%s)

  if [ -f "$SS_TOKEN_CACHE" ]; then
    local cached_exp cached_tok
    cached_exp=$(jq -r '.expiresAt // 0' "$SS_TOKEN_CACHE" 2>/dev/null || echo 0)
    cached_tok=$(jq -r '.accessToken // ""' "$SS_TOKEN_CACHE" 2>/dev/null || echo '')
    # 10# forces base-10 so a value with a leading zero can't be read as octal,
    # which is a real bash failure mode (zsh has no such rule, so an untested
    # helper works for its author and breaks for everyone else).
    if [ -n "$cached_tok" ] && [ "$((10#${cached_exp:-0}))" -gt "$((now + 120))" ]; then
      printf '%s' "$cached_tok"
      return 0
    fi
  fi

  local rt
  rt=$(ss_refresh_token) || return 1

  local body response access expires
  # Build the JSON with jq so a token containing quotes/backslashes can't break it.
  body=$(jq -nc --arg cid "$SS_CLIENT_ID" --arg rt "$rt" \
    '{grant_type:"refresh_token", client_id:$cid, refresh_token:$rt}')

  response=$(curl -sS -X POST "$SS_AUTH_URL" -H 'Content-Type: application/json' -d "$body") || return 1
  access=$(printf '%s' "$response" | jq -r '.access_token // ""')

  if [ -z "$access" ]; then
    echo "ss_access_token: refresh failed." >&2
    # Echo only the error fields, never the whole body.
    printf '%s' "$response" | jq -r '"  \(.error // "?"): \(.error_description // "?")"' >&2
    echo "  If the token was revoked, re-run scripts/bootstrap-auth.mjs." >&2
    return 1
  fi

  expires=$(printf '%s' "$response" | jq -r '.expires_in // 3600')
  ( umask 077; jq -nc --arg t "$access" --argjson e "$((now + expires))" \
      '{accessToken:$t, expiresAt:$e}' > "$SS_TOKEN_CACHE" )

  printf '%s' "$access"
}

# ss_api <METHOD> <PATH> [JSON_BODY]
#   ss_api GET  /api/authCheck
#   ss_api POST /ss3/subscriptions/123/state/away
#   ss_api POST /doorlock/123/ABC/state '{"state":"lock"}'
#
# Prints the response body on stdout (pipe to jq). Non-2xx goes to stderr and
# returns 1, so a failure can't be mistaken for an empty result.
ss_api() {
  # NB: `api_path`, never `path`. In zsh (the macOS default shell) `path` is a
  # special variable tied to PATH, so `local path=/api/authCheck` would replace
  # PATH for this function and everything it calls — date/head/cut then vanish
  # and every call fails with "command not found". bash has no such tie, so this
  # bug is invisible there.
  local method="$1" api_path="$2" json="${3:-}"
  local token
  token=$(ss_access_token) || return 1

  # An array, not a string: a string would word-split a body containing spaces.
  local args=(-sS -w '\n%{http_code}' -X "$method" "${SS_API_BASE}${api_path}"
              -H "Authorization: Bearer ${token}")
  if [ -n "$json" ]; then
    args+=(-H 'Content-Type: application/json' -d "$json")
  fi

  local out code payload
  out=$(curl "${args[@]}") || return 1
  code="${out##*$'\n'}"
  payload="${out%$'\n'*}"

  if [ "$code" -lt 200 ] || [ "$code" -ge 300 ]; then
    echo "ss_api: HTTP $code for $method $api_path" >&2
    printf '%s\n' "$payload" | head -c 500 >&2
    echo >&2
    return 1
  fi

  printf '%s\n' "$payload"
}

# Resolve the single active system id (fails loudly if the account has several).
ss_sid() {
  local uid sids count
  uid=$(ss_api GET /api/authCheck | jq -r '.userId') || return 1
  sids=$(ss_api "GET" "/users/${uid}/subscriptions?activeOnly=true" | jq -r '.subscriptions[].sid') || return 1
  count=$(printf '%s\n' "$sids" | grep -c . )
  if [ "$count" -ne 1 ]; then
    echo "ss_sid: expected 1 active system, found $count:" >&2
    printf '  %s\n' $sids >&2
    echo "  Pass the sid explicitly instead of using ss_sid." >&2
    return 1
  fi
  printf '%s' "$sids"
}
