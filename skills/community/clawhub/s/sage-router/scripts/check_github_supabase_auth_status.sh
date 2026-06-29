#!/usr/bin/env bash
set -euo pipefail

load_local_env_file() {
  local path="$1"
  [[ -f "$path" ]] || return 0

  local key value current
  while IFS='=' read -r -d '' key value; do
    case "$key" in
      SUPABASE_ACCESS_TOKEN|SAGE_ROUTER_SUPABASE_URL|SAGE_ROUTER_SUPABASE_ANON_KEY|PUBLIC_SUPABASE_ANON_KEY|VITE_SUPABASE_PUBLISHABLE_KEY|SUPABASE_ANON_KEY|AOPS_SUPABASE_ANON_KEY)
        ;;
      *)
        continue
        ;;
    esac
    current="${!key:-}"
    if [[ -z "$current" && -n "$value" ]]; then
      printf -v "$key" '%s' "$value"
      export "$key"
    fi
  done < <(set +u; set -a; source "$path" >/dev/null 2>&1; env -0)
}

load_local_env_file "${SAGEROUTER_SECRET_ENV_FILE:-/home/digit/.openclaw/.env}"

PROJECT_REF="${SUPABASE_PROJECT_REF:-awtangrlqqsdpksarhwo}"
AUTH_SITE_URL="${SAGEROUTER_AUTH_SITE_URL:-https://app.sagerouter.dev}"
SUPABASE_URL="${SAGE_ROUTER_SUPABASE_URL:-https://${PROJECT_REF}.supabase.co}"
SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:-}"
SUPABASE_ANON_KEY="${SAGE_ROUTER_SUPABASE_ANON_KEY:-}"
FAILURES=0
GITHUB_MANAGEMENT_ENABLED=""
GITHUB_PUBLIC_ENABLED=""

pass() {
  printf 'PASS %s\n' "$1"
}

warn() {
  printf 'WARN %s\n' "$1"
}

fail() {
  printf 'FAIL %s\n' "$1"
  FAILURES=$((FAILURES + 1))
}

print_github_oauth_handoff() {
  if [[ "$GITHUB_MANAGEMENT_ENABLED" == "true" && "$GITHUB_PUBLIC_ENABLED" == "true" ]]; then
    return
  fi

  cat <<EOF

GitHub OAuth owner handoff:
  1. From the sage-router repo, run:
     SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE=0 bash scripts/bootstrap_github_supabase_auth.sh
  2. Approve the GitHub App in the browser as the owner.
  3. On https://app.sagerouter.dev/github-app-manifest?code=..., run the printed exchange command within one hour.
  4. Recheck:
     bash scripts/check_github_supabase_auth_status.sh
     scripts/check_sagerouter_launch_readiness.sh

Email signup remains enabled while GitHub OAuth is pending.
EOF
}

require_tools() {
  local missing=()
  for tool in curl jq python3; do
    command -v "$tool" >/dev/null 2>&1 || missing+=("$tool")
  done
  if (( ${#missing[@]} > 0 )); then
    printf 'Missing required tool(s): %s\n' "${missing[*]}" >&2
    exit 2
  fi
}

supabase_key_for_project() {
  KEY="$1" PROJECT_REF="$PROJECT_REF" python3 - <<'PY'
import base64
import json
import os

key = os.environ.get("KEY", "").strip()
project_ref = os.environ.get("PROJECT_REF", "").strip()
if not key or not project_ref:
    raise SystemExit(0)

try:
    payload = key.split(".")[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)
    data = json.loads(base64.urlsafe_b64decode(payload.encode()))
except Exception:
    raise SystemExit(0)

if data.get("ref") == project_ref:
    print(key)
PY
}

discover_supabase_anon_key() {
  local repo_root path key env_name env_value
  for key in \
    "${SUPABASE_ANON_KEY:-}" \
    "${SAGE_ROUTER_SUPABASE_ANON_KEY:-}" \
    "${PUBLIC_SUPABASE_ANON_KEY:-}" \
    "${VITE_SUPABASE_PUBLISHABLE_KEY:-}" \
    "${AOPS_SUPABASE_ANON_KEY:-}"; do
    if supabase_key_can_read_settings "$key"; then
      printf '%s\n' "$key"
      return
    fi
  done
  while IFS='=' read -r env_name env_value; do
    case "$env_name" in
      *_SUPABASE_ANON_KEY|*_SUPABASE_PUBLISHABLE_KEY)
        if supabase_key_can_read_settings "$env_value"; then
          printf '%s\n' "$env_value"
          return
        fi
        ;;
    esac
  done < <(env)

  local repo_root
  repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  for path in "${repo_root}/web/public/account.js" "${repo_root}/web/public/auth.js" "${repo_root}/web/public/analytics.js"; do
    if [[ -f "$path" ]]; then
      key="$(sed -n "s/^const SUPABASE_ANON_KEY = '\([^']*\)';$/\1/p" "$path" | head -n1)"
      if supabase_key_can_read_settings "$key"; then
        printf '%s\n' "$key"
        return
      fi
    fi
  done
}

supabase_key_can_read_settings() {
  local key="$1"
  [[ -n "$key" ]] || return 1
  curl -fsS -o /dev/null "${SUPABASE_URL%/}/auth/v1/settings" -H "apikey: ${key}" >/dev/null 2>&1
}

check_management_config() {
  if [[ -z "$SUPABASE_ACCESS_TOKEN" ]]; then
    warn "SUPABASE_ACCESS_TOKEN not set; skipped Supabase Management API auth config probe"
    return
  fi

  local config site signup_disabled email_enabled github app_redirect api_redirect
  config="$(curl -fsS "https://api.supabase.com/v1/projects/${PROJECT_REF}/config/auth" \
    -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}")"
  site="$(printf '%s' "$config" | jq -r '.site_url // empty')"
  signup_disabled="$(printf '%s' "$config" | jq -r 'if has("disable_signup") then .disable_signup else true end')"
  email_enabled="$(printf '%s' "$config" | jq -r '.external_email_enabled // false')"
  github="$(printf '%s' "$config" | jq -r '.external_github_enabled // false')"
  app_redirect="$(printf '%s' "$config" | jq -r '((.uri_allow_list // "") | contains("https://app.sagerouter.dev/**"))')"
  api_redirect="$(printf '%s' "$config" | jq -r '((.uri_allow_list // "") | contains("https://api.sagerouter.dev/**"))')"

  [[ "$site" == "$AUTH_SITE_URL" ]] && pass "Supabase site_url is ${AUTH_SITE_URL}" || fail "Supabase site_url is ${site:-missing}, expected ${AUTH_SITE_URL}"
  [[ "$signup_disabled" == "false" && "$email_enabled" == "true" ]] && pass "Supabase email signup is enabled" || fail "Supabase email signup disabled: disable_signup=${signup_disabled:-missing} external_email_enabled=${email_enabled:-missing}"
  [[ "$app_redirect" == "true" && "$api_redirect" == "true" ]] && pass "Supabase redirect allow-list includes app/api hosts" || fail "Supabase redirect allow-list missing app/api hosts"
  GITHUB_MANAGEMENT_ENABLED="$github"
  [[ "$github" == "true" ]] && pass "Supabase Management API shows GitHub OAuth enabled" || warn "Supabase Management API shows GitHub OAuth disabled"
}

check_public_settings() {
  local anon_key settings email github
  anon_key="$(discover_supabase_anon_key)"
  if [[ -z "$anon_key" ]]; then
    warn "Supabase anon key not set and not discoverable from hosted app scripts; skipped public /auth/v1/settings probe"
    return
  fi

  settings="$(curl -fsS "${SUPABASE_URL%/}/auth/v1/settings" -H "apikey: ${anon_key}")"
  email="$(printf '%s' "$settings" | jq -r '.external.email // false')"
  github="$(printf '%s' "$settings" | jq -r '.external.github // false')"

  [[ "$email" == "true" ]] && pass "Browser-visible Supabase email signup is enabled" || fail "Browser-visible Supabase email signup disabled"
  GITHUB_PUBLIC_ENABLED="$github"
  [[ "$github" == "true" ]] && pass "Browser-visible Supabase GitHub OAuth is enabled" || warn "Browser-visible Supabase GitHub OAuth is disabled"
}

require_tools
printf 'Checking Sage Router GitHub/Supabase auth status for project %s\n' "$PROJECT_REF"
check_management_config
check_public_settings

if (( FAILURES > 0 )); then
  printf 'GitHub/Supabase auth status found %s hard failure(s).\n' "$FAILURES" >&2
  exit 1
fi

print_github_oauth_handoff
printf 'GitHub/Supabase auth status check complete.\n'
