#!/usr/bin/env bash
set -euo pipefail

TAPAUTH_BASE="${TAPAUTH_BASE_URL:-https://tapauth.ai}"
TAPAUTH_AGENT="${TAPAUTH_AGENT_NAME:-tapauth-skill}"
TAPAUTH_POLL_TIMEOUT="${TAPAUTH_POLL_TIMEOUT_SECONDS:-600}"
if [ -n "${TAPAUTH_HOME:-}" ]; then
  TAPAUTH_DIR="$TAPAUTH_HOME"
elif [ -n "${CLAUDE_PLUGIN_DATA:-}" ]; then
  TAPAUTH_DIR="$CLAUDE_PLUGIN_DATA"
else
  TAPAUTH_DIR="./.tapauth"
fi
mkdir -p "$TAPAUTH_DIR" && chmod 700 "$TAPAUTH_DIR"

mode="url"
if [ "${1:-}" = "--token" ]; then
  mode="token"
  shift
fi

die() {
  echo "tapauth: $*" >&2
  exit 1
}

emit_token() {
  [ -n "${TAPAUTH_TOKEN_B64:-}" ] || die "no token in response"
  printf '%s' "$TAPAUTH_TOKEN_B64" | base64 --decode 2>/dev/null || printf '%s' "$TAPAUTH_TOKEN_B64" | base64 -D
  printf '\n'
  exit 0
}

parse_env_response() {
  while IFS='=' read -r key value; do
    value="${value%$'\r'}"
    case "$key" in
      TAPAUTH_GRANT_ID)     TAPAUTH_GRANT_ID="$value" ;;
      TAPAUTH_GRANT_SECRET) TAPAUTH_GRANT_SECRET="$value" ;;
      TAPAUTH_APPROVE_URL)  TAPAUTH_APPROVE_URL="$value" ;;
      TAPAUTH_STATUS)       TAPAUTH_STATUS="$value" ;;
      TAPAUTH_EXPIRES)      TAPAUTH_EXPIRES="$value" ;;
      TAPAUTH_TOKEN_B64)    TAPAUTH_TOKEN_B64="$value" ;;
    esac
  done <<< "$1"
}

save_grant() {
  install -m 600 /dev/null "$env_file"
  cat > "$env_file" <<EOF
TAPAUTH_GRANT_ID=${TAPAUTH_GRANT_ID}
TAPAUTH_GRANT_SECRET=${TAPAUTH_GRANT_SECRET}
TAPAUTH_EXPIRES=${TAPAUTH_EXPIRES:-}
EOF
}

fetch_grant() {
  TAPAUTH_TOKEN_B64="" TAPAUTH_STATUS="" TAPAUTH_EXPIRES="" TAPAUTH_APPROVE_URL=""
  local resp
  resp="$(curl --silent --show-error --write-out "\n%{http_code}" \
    -H "Authorization: Bearer ${TAPAUTH_GRANT_SECRET}" \
    -H 'Accept: text/plain' "${TAPAUTH_BASE}/api/v1/grants/${TAPAUTH_GRANT_ID}" || true)"
  TAPAUTH_HTTP="${resp##*$'\n'}"
  parse_env_response "${resp%$'\n'*}"
  [ "$TAPAUTH_HTTP" != "000" ] || die "failed to contact TapAuth"
}

emit_url() {
  if [ "$provider" = "secret" ]; then
    echo "Approve secret request: ${TAPAUTH_APPROVE_URL:-${TAPAUTH_BASE}/approve/${TAPAUTH_GRANT_ID}}"
  else
    echo "Approve access: ${TAPAUTH_APPROVE_URL:-${TAPAUTH_BASE}/approve/${TAPAUTH_GRANT_ID}}"
  fi
  echo ""
  if [ "${TAPAUTH_STATUS:-}" = "expired" ]; then
    echo "Show this URL to the user, then start --token immediately; it waits until re-authorization completes."
  else
    echo "Show this URL to the user, then start --token immediately; it waits until approval completes."
  fi
  exit 0
}

create_grant() {
  if [ "$provider" = "secret" ]; then
    echo "Creating secret request..." >&2
  else
    echo "Creating grant for ${provider}${sorted_scopes:+ (${sorted_scopes})}..." >&2
  fi
  TAPAUTH_GRANT_ID="" TAPAUTH_GRANT_SECRET="" TAPAUTH_APPROVE_URL="" TAPAUTH_EXPIRES="" TAPAUTH_STATUS=""
  create_args=(curl --silent --show-error --write-out "\n%{http_code}" -X POST -H 'Accept: text/plain'
    --data-urlencode "provider=${provider}"
    --data-urlencode "agent_name=${TAPAUTH_AGENT}")
  if [ "$provider" = "secret" ]; then
    create_args+=(--data-urlencode "secret_description=${secret_description}")
    [ -n "$validation_regex" ] && create_args+=(--data-urlencode "validation_regex=${validation_regex}")
    [ -n "$validation_hint" ] && create_args+=(--data-urlencode "validation_hint=${validation_hint}")
  else
    [ -n "$sorted_scopes" ] && create_args+=(--data-urlencode "scopes=${sorted_scopes}")
  fi
  create_args+=("${TAPAUTH_BASE}/api/v1/grants")
  local resp
  resp="$("${create_args[@]}" || true)"
  TAPAUTH_HTTP="${resp##*$'\n'}"
  parse_env_response "${resp%$'\n'*}"
  case "$TAPAUTH_HTTP" in
    200|201) ;;
    000) die "failed to contact TapAuth" ;;
    *) die "failed to create grant (${TAPAUTH_HTTP})" ;;
  esac
  if [ -z "${TAPAUTH_GRANT_ID:-}" ] || [ -z "${TAPAUTH_GRANT_SECRET:-}" ]; then
    die "failed to create grant"
  fi
  save_grant
}

provider="${1:-}"
raw_scopes="${2:-}"
validation_regex="${3:-}"
validation_hint="${4:-}"

if [ -z "${provider:-}" ]; then
  echo "usage: tapauth [--token] <provider> [scopes] | tapauth [--token] secret <description> [validation_regex] [validation_hint]" >&2
  echo "  providers: google, github, linear, vercel, slack, notion, asana, sentry, discord, apify, atlassian, secret" >&2
  exit 1
fi

if [ "$provider" = "secret" ]; then
  if [ -z "${raw_scopes:-}" ]; then
    echo "tapauth: description is required for secret" >&2
    echo "usage: tapauth [--token] secret <description> [validation_regex] [validation_hint]" >&2
    exit 1
  fi
  secret_description="$raw_scopes"
  sorted_scopes=""
  safe_scopes=$(printf '%s' "secret-${secret_description}-${validation_regex}-${validation_hint}" | sed 's/[^A-Za-z0-9._-]/_/g' | cut -c1-180)
else
  scopes="$raw_scopes"
  sorted_scopes=$(echo "$scopes" | tr "," "\n" | sort | tr "\n" "," | sed "s/,$//")
  safe_scopes=$(echo "$sorted_scopes" | tr '/:' '__')
fi
env_file="${TAPAUTH_DIR}/${provider}-${safe_scopes}.env"

TAPAUTH_GRANT_ID="" TAPAUTH_GRANT_SECRET="" TAPAUTH_EXPIRES="" TAPAUTH_APPROVE_URL="" TAPAUTH_STATUS="" TAPAUTH_TOKEN_B64=""
[ -f "$env_file" ] && parse_env_response "$(cat "$env_file")"

if [ -z "${TAPAUTH_GRANT_ID:-}" ] || [ -z "${TAPAUTH_GRANT_SECRET:-}" ]; then
  [ "$mode" = "token" ] && die "run without --token first to get an approval URL"
  create_grant
  emit_url
fi

fetch_grant
case "$TAPAUTH_HTTP:${TAPAUTH_STATUS:-}" in
  200:*)
    if [ "$mode" = "url" ]; then
      echo "Already authorized for ${provider}${sorted_scopes:+ (${sorted_scopes})}. Use --token to retrieve it."
      exit 0
    fi
    save_grant
    emit_token
    ;;
  202:*) ;;
  410:expired)
    [ "$mode" = "token" ] && die "cached grant expired; run without --token first to re-authorize it"
    emit_url
    ;;
  401:*|404:*|410:revoked|410:denied|410:link_expired|410:*)
    [ "$mode" = "token" ] && die "cached grant is no longer usable; run without --token first to get a new approval URL"
    create_grant
    emit_url
    ;;
  *) die "grant fetch failed (${TAPAUTH_HTTP})" ;;
esac

[ "$mode" = "url" ] && emit_url

poll_start=$SECONDS
while true; do
  sleep 2
  elapsed=$((SECONDS - poll_start))
  [ "$elapsed" -ge "$TAPAUTH_POLL_TIMEOUT" ] && { echo "tapauth: timed out" >&2; exit 1; }
  echo "Waiting for approval... (${elapsed}s)" >&2
  fetch_grant
  case "$TAPAUTH_HTTP:${TAPAUTH_STATUS:-}" in
    200:*)
      save_grant
      emit_token
      ;;
    202:*) ;;
    410:expired) die "grant expired; run without --token first to re-authorize it" ;;
    410:revoked|410:denied|410:link_expired) die "grant ${TAPAUTH_STATUS}" ;;
    401:*|404:*|410:*) die "grant is no longer usable; run without --token first to get a new approval URL" ;;
    *) die "grant fetch failed (${TAPAUTH_HTTP})" ;;
  esac
done
