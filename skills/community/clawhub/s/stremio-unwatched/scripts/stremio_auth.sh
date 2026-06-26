#!/usr/bin/env bash
# Stremio authentication: login, cache authKey, validate, logout.
# Usage:
#   stremio_auth.sh              # Interactive login (or use cached key)
#   stremio_auth.sh --logout     # Clear cached credentials
#   stremio_auth.sh --check      # Validate cached key, exit 0 if valid
#   stremio_auth.sh --key        # Print authKey to stdout (for piping)
set -euo pipefail

STREMIO_API="https://api.strem.io/api"
CRED_DIR="${OPENCLAW_CREDENTIALS_DIR:-${HOME}/.openclaw/credentials}"
CRED_FILE="${CRED_DIR}/stremio.json"

die() { echo "error: $*" >&2; exit 1; }

load_key() {
  if [[ -f "$CRED_FILE" ]]; then
    jq -r '.authKey // empty' "$CRED_FILE" 2>/dev/null
  fi
}

save_credentials() {
  local auth_key="$1" user_id="$2" email="$3"
  mkdir -p "$CRED_DIR"
  chmod 700 "$CRED_DIR"
  jq -n \
    --arg key "$auth_key" \
    --arg uid "$user_id" \
    --arg email "$email" \
    '{authKey: $key, userId: $uid, email: $email}' > "$CRED_FILE"
  chmod 600 "$CRED_FILE"
}

validate_key() {
  local key="$1"
  local resp
  resp=$(curl -sf -X POST "${STREMIO_API}/getUser" \
    -H "Content-Type: application/json" \
    -d "{\"authKey\":\"${key}\"}" 2>/dev/null) || return 1
  # Check for error in response
  if echo "$resp" | jq -e '.error' &>/dev/null; then
    return 1
  fi
  return 0
}

do_login() {
  local email password resp auth_key user_id
  # Support env vars for non-interactive use (e.g. from agent or cron)
  email="${STREMIO_EMAIL:-}"
  password="${STREMIO_PASSWORD:-}"
  if [[ -z "$email" || -z "$password" ]]; then
    echo "Stremio login" >&2
    [[ -z "$email" ]] && read -rp "Email: " email
    [[ -z "$password" ]] && read -rsp "Password: " password
    echo >&2
  fi

  resp=$(curl -sf -X POST "${STREMIO_API}/login" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg e "$email" --arg p "$password" \
      '{type:"Login", email:$e, password:$p, facebook:false}')" \
  ) || die "API request failed"

  if echo "$resp" | jq -e '.error' &>/dev/null; then
    die "Login failed: $(echo "$resp" | jq -r '.error.message')"
  fi

  auth_key=$(echo "$resp" | jq -r '.result.authKey')
  user_id=$(echo "$resp" | jq -r '.result.user._id')
  [[ -n "$auth_key" && "$auth_key" != "null" ]] || die "No authKey in response"

  save_credentials "$auth_key" "$user_id" "$email"
  echo "Logged in as ${email}" >&2
  echo "$auth_key"
}

do_logout() {
  local key
  key=$(load_key)
  if [[ -n "$key" ]]; then
    curl -sf -X POST "${STREMIO_API}/logout" \
      -H "Content-Type: application/json" \
      -d "{\"authKey\":\"${key}\"}" &>/dev/null || true
  fi
  rm -f "$CRED_FILE"
  echo "Logged out" >&2
}

# Main
case "${1:-}" in
  --logout)
    do_logout
    ;;
  --check)
    key=$(load_key)
    [[ -n "$key" ]] || die "No cached credentials"
    validate_key "$key" || die "Cached key is invalid"
    echo "Valid ($(jq -r '.email // "unknown"' "$CRED_FILE"))" >&2
    ;;
  --key)
    key=$(load_key)
    if [[ -n "$key" ]] && validate_key "$key"; then
      echo "$key"
    else
      do_login
    fi
    ;;
  "")
    key=$(load_key)
    if [[ -n "$key" ]] && validate_key "$key"; then
      echo "Already logged in ($(jq -r '.email // "unknown"' "$CRED_FILE"))" >&2
      echo "$key"
    else
      do_login
    fi
    ;;
  *)
    die "Unknown option: $1"
    ;;
esac
