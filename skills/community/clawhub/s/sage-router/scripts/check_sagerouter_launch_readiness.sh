#!/usr/bin/env bash
set -euo pipefail

load_local_env_file() {
  local path="$1"
  [[ -f "$path" ]] || return 0

  local key value current
  while IFS='=' read -r -d '' key value; do
    case "$key" in
      SAGEROUTER_API_BASE_URL|SAGEROUTER_APP_BASE_URL|SAGEROUTER_MARKETING_BASE_URL|SAGEROUTER_ORIGIN_BASE_URL|\
      SAGEROUTER_ORIGIN_AUTO_DISCOVER|SAGEROUTER_CLOUD_RUN_PROJECT|SAGEROUTER_CLOUD_RUN_REGION|SAGEROUTER_CLOUD_RUN_SERVICE|\
      SAGE_ROUTER_GCP_PROJECT_ID|SUPABASE_PROJECT_REF|SAGE_ROUTER_SUPABASE_URL|SAGE_ROUTER_SUPABASE_ANON_KEY|\
      PUBLIC_SUPABASE_ANON_KEY|VITE_SUPABASE_PUBLISHABLE_KEY|AOPS_SUPABASE_ANON_KEY|SUPABASE_ACCESS_TOKEN|\
      SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY|SUPABASE_SERVICE_ROLE_KEY|SAGE_ROUTER_API_KEY|SAGE_ROUTER_EDGE_TOKEN|\
      SAGE_ROUTER_API_KEY_HASH_PEPPER|SAGE_ROUTER_SIGNING_SECRET|\
      CLOUDFLARE_API_TOKEN|CLOUDFLARE_ZONE_ID|SAGEROUTER_CLOUDFLARE_ZONE_ID|SAGEROUTER_API_HOST|\
      SAGE_ROUTER_OPERATOR_TOKEN|SAGE_ROUTER_CLIENT_API_KEY|SAGE_ROUTER_CLIENT_API_KEYS|SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED|\
      SAGEROUTER_PROVIDER_RESALE_TERMS_URL|SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL|\
      SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED|SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS)
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

API_BASE="${SAGEROUTER_API_BASE_URL:-https://api.sagerouter.dev}"
APP_BASE="${SAGEROUTER_APP_BASE_URL:-https://app.sagerouter.dev}"
MARKETING_BASE="${SAGEROUTER_MARKETING_BASE_URL:-https://sagerouter.dev}"
ORIGIN_BASE="${SAGEROUTER_ORIGIN_BASE_URL:-}"
ORIGIN_AUTO_DISCOVER="${SAGEROUTER_ORIGIN_AUTO_DISCOVER:-1}"
CLOUD_RUN_PROJECT="${SAGEROUTER_CLOUD_RUN_PROJECT:-${SAGE_ROUTER_GCP_PROJECT_ID:-sage-router-demo-20260428}}"
CLOUD_RUN_REGION="${SAGEROUTER_CLOUD_RUN_REGION:-us-central1}"
CLOUD_RUN_SERVICE="${SAGEROUTER_CLOUD_RUN_SERVICE:-sage-router}"
SUPABASE_PROJECT_REF="${SUPABASE_PROJECT_REF:-awtangrlqqsdpksarhwo}"
SUPABASE_URL="${SAGE_ROUTER_SUPABASE_URL:-https://${SUPABASE_PROJECT_REF}.supabase.co}"
SUPABASE_ANON_KEY="${SAGE_ROUTER_SUPABASE_ANON_KEY:-}"
SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:-}"
SUPABASE_SERVICE_ROLE_KEY="${SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY:-${SUPABASE_SERVICE_ROLE_KEY:-}}"
ADMIN_TOKEN="${SAGE_ROUTER_API_KEY:-${SAGE_ROUTER_EDGE_TOKEN:-}}"
OPERATOR_TOKEN="${SAGE_ROUTER_OPERATOR_TOKEN:-${SAGE_ROUTER_CLIENT_API_KEY:-}}"
MANAGED_PROVIDER_RESALE_ENABLED="${SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED:-0}"
PROVIDER_RESALE_TERMS_URL="${SAGEROUTER_PROVIDER_RESALE_TERMS_URL:-}"
PROVIDER_RESALE_MARGIN_POLICY_URL="${SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL:-}"
PROVIDER_RESALE_TERMS_ACKNOWLEDGED="${SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED:-0}"
PROVIDER_RESALE_ALLOWED_PROVIDERS="${SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS:-}"
SUPABASE_PUBLIC_GITHUB_ENABLED=""
FAILURES=0

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

http_code() {
  local url="$1"
  shift
  curl -sS -o /tmp/sage-router-readiness-body -w '%{http_code}' "$url" "$@"
}

http_code_follow() {
  local url="$1"
  shift
  curl -sSL -o /tmp/sage-router-readiness-body -w '%{http_code}' "$url" "$@"
}

python_http_code() {
  local url="$1"
  local user_agent="${2:-}"
  URL="$url" USER_AGENT="$user_agent" python3 - <<'PY'
import os
import urllib.error
import urllib.request

url = os.environ.get("URL", "")
user_agent = os.environ.get("USER_AGENT", "")
headers = {"accept": "application/json"}
if user_agent:
    headers["user-agent"] = user_agent
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read(4096).decode("utf-8", errors="replace")
        code = resp.status
except urllib.error.HTTPError as exc:
    body = exc.read(4096).decode("utf-8", errors="replace")
    code = exc.code
except Exception as exc:
    body = str(exc)
    code = 0
with open("/tmp/sage-router-readiness-body", "w", encoding="utf-8") as handle:
    handle.write(body)
print(code)
PY
}

require_jq() {
  if ! command -v jq >/dev/null 2>&1; then
    fail "jq is required"
    exit 2
  fi
}

first_csv_token() {
  VALUE="$1" python3 - <<'PY'
import os

for item in os.environ.get("VALUE", "").split(","):
    item = item.strip()
    if item:
        print(item)
        break
PY
}

cloud_run_secret_ref() {
  local env_name="$1"
  if ! command -v gcloud >/dev/null 2>&1; then
    return
  fi
  gcloud run services describe "$CLOUD_RUN_SERVICE" \
    --project="$CLOUD_RUN_PROJECT" \
    --region="$CLOUD_RUN_REGION" \
    --format=json 2>/dev/null |
    jq -r --arg name "$env_name" '
      (.spec.template.spec.containers[0].env // [])
      | map(select(.name == $name))
      | .[0].valueFrom.secretKeyRef.name // empty
    '
}

resolve_operator_token() {
  local token secret_name secret_value
  token="$(first_csv_token "$OPERATOR_TOKEN")"
  if [[ -n "$token" ]]; then
    printf '%s\n' "$token"
    return
  fi
  token="$(first_csv_token "${SAGE_ROUTER_CLIENT_API_KEYS:-}")"
  if [[ -n "$token" ]]; then
    printf '%s\n' "$token"
    return
  fi

  secret_name="$(cloud_run_secret_ref SAGE_ROUTER_CLIENT_API_KEYS)"
  if [[ -n "$secret_name" ]] && command -v gcloud >/dev/null 2>&1; then
    secret_value="$(gcloud secrets versions access latest --secret="$secret_name" --project="$CLOUD_RUN_PROJECT" 2>/dev/null || true)"
    token="$(first_csv_token "$secret_value")"
    if [[ -n "$token" ]]; then
      printf '%s\n' "$token"
      return
    fi
  fi

  first_csv_token "$ADMIN_TOKEN"
}

discover_supabase_anon_key() {
  local path key env_name env_value
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
  for path in web/public/account.js web/public/auth.js web/public/analytics.js; do
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

supabase_key_for_project() {
  KEY="$1" PROJECT_REF="$SUPABASE_PROJECT_REF" python3 - <<'PY'
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

check_edge_health() {
  local body
  body="$(curl -fsS "${API_BASE%/}/edge/health")"
  local status auth_mode selected health_urls_redacted rate_limit_enabled auth_attempt_rate_limit_enabled auth_attempt_rate_limit quota_enabled api_key_auth_cache api_key_auth_cache_zero cors_wildcard_blocked cors_explicit_origin_required cors_allowed_origins_count failover_ok model_modalities_shared model_modalities_rpc
  status="$(printf '%s' "$body" | jq -r '.status // empty')"
  auth_mode="$(printf '%s' "$body" | jq -r '.authMode // empty')"
  selected="$(printf '%s' "$body" | jq -r '.selected // empty')"
  health_urls_redacted="$(printf '%s' "$body" | jq -r '
    ([.upstreams[]? | has("url")] | any) == false and
    ((.controlPlane // {}) | has("url") | not)
  ')"
  rate_limit_enabled="$(printf '%s' "$body" | jq -r '.enforcement.rateLimitEnabled // false')"
  auth_attempt_rate_limit_enabled="$(printf '%s' "$body" | jq -r '.enforcement.authAttemptRateLimitEnabled // false')"
  auth_attempt_rate_limit="$(printf '%s' "$body" | jq -r '.enforcement.authAttemptRateLimit // 0')"
  quota_enabled="$(printf '%s' "$body" | jq -r '.enforcement.quotaEnabled // false')"
  api_key_auth_cache="$(printf '%s' "$body" | jq -r '.enforcement.apiKeyAuthCacheSeconds // empty')"
  api_key_auth_cache_zero="$(printf '%s' "$body" | jq -r '(.enforcement.apiKeyAuthCacheSeconds // -1) == 0')"
  cors_wildcard_blocked="$(printf '%s' "$body" | jq -r '.enforcement.corsWildcardAllowed == false')"
  cors_explicit_origin_required="$(printf '%s' "$body" | jq -r '.enforcement.corsExplicitOriginRequired == true')"
  cors_allowed_origins_count="$(printf '%s' "$body" | jq -r '.enforcement.corsAllowedOriginsCount // 0')"
  failover_ok="$(printf '%s' "$body" | jq -r '
    ((.failover // {}) | .mode == "lowest-latency-healthy") and
    ((.failover // {}) | .retryEnabled == true) and
    ((.failover.retryStatuses // []) | index(502) and index(503) and index(504)) and
    ((.failover // {}) | .retryHeader == "X-Sage-Router-Retry-Count")
  ')"
  model_modalities_shared="$(printf '%s' "$body" | jq -r '.modelModalities.sharedEnabled // false')"
  model_modalities_rpc="$(printf '%s' "$body" | jq -r '.modelModalities.rpcConfigured // false')"
  if [[ "$status" == "ok" && "$auth_mode" == "supabase" && -n "$selected" && "$health_urls_redacted" == "true" && "$rate_limit_enabled" == "true" && "$auth_attempt_rate_limit_enabled" == "true" && "$auth_attempt_rate_limit" -gt 0 && "$quota_enabled" == "true" && "$api_key_auth_cache_zero" == "true" && "$cors_wildcard_blocked" == "true" && "$cors_explicit_origin_required" == "true" && "$cors_allowed_origins_count" -gt 0 && "$failover_ok" == "true" && "$model_modalities_shared" == "true" && "$model_modalities_rpc" == "true" ]]; then
    pass "edge healthy with supabase auth, redacted health snapshots, rate limits, auth-attempt throttling, durable quotas, immediate generated-key revocation, non-wildcard browser CORS, retry failover, and shared model modality persistence; selected ${selected}"
  else
    fail "edge health unexpected: status=${status:-missing} authMode=${auth_mode:-missing} selected=${selected:-missing} healthUrlsRedacted=${health_urls_redacted:-missing} rateLimit=${rate_limit_enabled:-missing} authAttemptRateLimit=${auth_attempt_rate_limit_enabled:-missing}/${auth_attempt_rate_limit:-missing} quota=${quota_enabled:-missing} apiKeyAuthCache=${api_key_auth_cache:-missing} corsWildcardBlocked=${cors_wildcard_blocked:-missing} corsExplicitOrigin=${cors_explicit_origin_required:-missing} corsAllowedOrigins=${cors_allowed_origins_count:-missing} failover=${failover_ok:-missing} modelModalities=${model_modalities_shared:-missing}/${model_modalities_rpc:-missing}"
  fi
}

check_public_edge_layer_headers() {
  local headers code tailnet_edge selected_upstream worker_edge worker_origin worker_origin_kind content_type
  headers="$(mktemp)"
  code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$headers" -w '%{http_code}' \
      "${API_BASE%/}/edge/health"
  )"
  tailnet_edge="$(awk 'tolower($1)=="x-sage-router-edge:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  selected_upstream="$(awk 'tolower($1)=="x-sage-router-selected-upstream:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  worker_edge="$(awk 'tolower($1)=="x-sage-router-cloudflare-edge:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  worker_origin="$(awk 'tolower($1)=="x-sage-router-api-origin:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  worker_origin_kind="$(awk 'tolower($1)=="x-sage-router-api-origin-kind:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  content_type="$(awk 'tolower($1)=="content-type:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  rm -f "$headers" /tmp/sage-router-readiness-body

  if [[ "$code" == "200" &&
        "$content_type" == application/json* &&
        "$tailnet_edge" == "tailnet-lowest-latency" &&
        "$selected_upstream" == upstream-* ]]; then
    pass "public edge layer is visible as Tailnet lowest-latency router without exposing raw upstream URLs"
  elif [[ "$code" == "200" &&
          "$content_type" == application/json* &&
          "$worker_edge" == "api.sagerouter.dev" &&
          "$worker_origin" == origin-* &&
          -n "$worker_origin_kind" ]]; then
    pass "public edge layer is visible as Cloudflare Worker origin selector without exposing raw upstream URLs"
  else
    fail "public edge layer headers missing or unsafe: code=${code} type=${content_type:-missing} tailnetEdge=${tailnet_edge:-missing} selectedUpstream=${selected_upstream:-missing} workerEdge=${worker_edge:-missing} workerOrigin=${worker_origin:-missing} workerOriginKind=${worker_origin_kind:-missing}"
  fi
}

check_public_auth_gate() {
  local code analytics_code funnel_code account_analytics_code error account_url pricing_url api_key_prefix
  code="$(http_code "${API_BASE%/}/v1/models")"
  error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  account_url="$(jq -r '.accountUrl // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  pricing_url="$(jq -r '.pricingUrl // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  api_key_prefix="$(jq -r '.apiKeyPrefix // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  analytics_code="$(http_code "${API_BASE%/}/analytics?days=7")"
  rm -f /tmp/sage-router-readiness-body
  funnel_code="$(http_code "${API_BASE%/}/analytics/funnel?days=30")"
  rm -f /tmp/sage-router-readiness-body
  account_analytics_code="$(http_code "${API_BASE%/}/account/analytics?days=7")"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$code" == "401" && "$error" == "unauthorized" && "$account_url" == "${APP_BASE%/}/account.html" && "$pricing_url" == "${MARKETING_BASE%/}/pricing" && "$api_key_prefix" == "sk_sage_" && "$analytics_code" == "401" && "$funnel_code" == "401" && "$account_analytics_code" == "401" ]]; then
    pass "anonymous model and analytics APIs are blocked with hosted onboarding guidance"
  else
    fail "anonymous auth gate incomplete: /v1/models=${code} error=${error:-missing} accountUrl=${account_url:-missing} pricingUrl=${pricing_url:-missing} apiKeyPrefix=${api_key_prefix:-missing} /analytics=${analytics_code} /analytics/funnel=${funnel_code} /account/analytics=${account_analytics_code}, expected guided 401"
  fi
}

check_api_client_user_agent_gate() {
  local sdk_code raw_python_code raw_error raw_error_code
  sdk_code="$(python_http_code "${API_BASE%/}/v1/models" "OpenAI/Python 1.0.0")"
  rm -f /tmp/sage-router-readiness-body
  raw_python_code="$(python_http_code "${API_BASE%/}/v1/models")"
  raw_error="$(jq -r '.error_name // .title // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  raw_error_code="$(jq -r '.error_code // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$sdk_code" == "401" ]]; then
    pass "OpenAI/Python-style API clients reach the edge auth gate"
  else
    fail "OpenAI/Python-style API client probe failed before guided auth gate: HTTP ${sdk_code}"
  fi
  if [[ "$raw_python_code" == "403" && "$raw_error_code" == "1010" ]]; then
    if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
      if bash scripts/configure_cloudflare_api_bic_skip.sh --check >/tmp/sage-router-cloudflare-bic-check 2>&1; then
        warn "Cloudflare Browser Integrity Check still blocks raw Python urllib even though the host-scoped BIC skip rule is present; wait for propagation or inspect Cloudflare security events"
      else
        warn "Cloudflare Browser Integrity Check blocks raw Python urllib's default signature, but OpenAI/Python-style API clients reach the guided auth gate; the available Cloudflare token cannot verify the host-scoped BIC skip rule: $(tr '\n' ' ' </tmp/sage-router-cloudflare-bic-check)"
      fi
      rm -f /tmp/sage-router-cloudflare-bic-check
    else
      warn "Cloudflare Browser Integrity Check blocks Python urllib's default signature; raw HTTP clients should send a normal SDK User-Agent or run scripts/configure_cloudflare_api_bic_skip.sh with a Zone Rulesets token for api.sagerouter.dev"
    fi
  elif [[ "$raw_python_code" == "401" ]]; then
    pass "raw Python urllib-style API clients reach the edge auth gate"
  else
    warn "raw Python urllib-style API client probe returned HTTP ${raw_python_code} (${raw_error:-no structured error})"
  fi
}

check_public_router_profile_contract() {
  local responses_body stream_body responses_ok responses_status responses_model responses_prefix responses_text stream_ok stream_status stream_model stream_prefix stream_text stream_events smoke_key
  smoke_key="${SAGEROUTER_SMOKE_API_KEY:-${SAGE_ROUTER_CLIENT_API_KEY:-${SAGE_ROUTER_API_KEY:-}}}"
  if [[ -z "$smoke_key" && ( -z "$SUPABASE_SERVICE_ROLE_KEY" || -z "${SAGE_ROUTER_API_KEY_HASH_PEPPER:-${SAGE_ROUTER_SIGNING_SECRET:-}}" ) ]]; then
    warn "No smoke API key and Supabase generated-key credentials incomplete; skipped live generated-key router-profile contract smoke"
    return
  fi

  responses_body="$(mktemp)"
  stream_body="$(mktemp)"
  if ! SAGEROUTER_API_BASE_URL="${API_BASE%/}" \
      SAGE_ROUTER_SUPABASE_URL="$SUPABASE_URL" \
      SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY="$SUPABASE_SERVICE_ROLE_KEY" \
      SAGE_ROUTER_API_KEY_HASH_PEPPER="${SAGE_ROUTER_API_KEY_HASH_PEPPER:-${SAGE_ROUTER_SIGNING_SECRET:-}}" \
      SAGEROUTER_SMOKE_API_KEY="$smoke_key" \
      python3 scripts/smoke_public_profile_alias.py \
      --api-base "${API_BASE%/}" \
      --model sage-router/frontier \
      --mode responses >"$responses_body"; then
    fail "public Responses profile smoke failed to execute"
    rm -f "$responses_body" "$stream_body"
    return
  fi
  if ! SAGEROUTER_API_BASE_URL="${API_BASE%/}" \
      SAGE_ROUTER_SUPABASE_URL="$SUPABASE_URL" \
      SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY="$SUPABASE_SERVICE_ROLE_KEY" \
      SAGE_ROUTER_API_KEY_HASH_PEPPER="${SAGE_ROUTER_API_KEY_HASH_PEPPER:-${SAGE_ROUTER_SIGNING_SECRET:-}}" \
      SAGEROUTER_SMOKE_API_KEY="$smoke_key" \
      python3 scripts/smoke_public_profile_alias.py \
      --api-base "${API_BASE%/}" \
      --model sage-router/frontier \
      --mode responses-stream >"$stream_body"; then
    fail "public streaming Responses profile smoke failed to execute"
    rm -f "$responses_body" "$stream_body"
    return
  fi

  responses_ok="$(jq -r '.profileContractOk // false' "$responses_body" 2>/dev/null || true)"
  responses_status="$(jq -r '.status // empty' "$responses_body" 2>/dev/null || true)"
  responses_model="$(jq -r '.headerModel // .bodyModel // empty' "$responses_body" 2>/dev/null || true)"
  responses_prefix="$(jq -r '.prefixLeak // true' "$responses_body" 2>/dev/null || true)"
  responses_text="$(jq -r '.visibleText // empty' "$responses_body" 2>/dev/null | head -c 120 || true)"
  stream_ok="$(jq -r '.profileContractOk // false' "$stream_body" 2>/dev/null || true)"
  stream_status="$(jq -r '.status // empty' "$stream_body" 2>/dev/null || true)"
  stream_model="$(jq -r '.headerModel // empty' "$stream_body" 2>/dev/null || true)"
  stream_prefix="$(jq -r '.prefixLeak // true' "$stream_body" 2>/dev/null || true)"
  stream_text="$(jq -r '.visibleText // empty' "$stream_body" 2>/dev/null | head -c 120 || true)"
  stream_events="$(jq -r '(.streamEvents // []) | join(",")' "$stream_body" 2>/dev/null | head -c 180 || true)"
  rm -f "$responses_body" "$stream_body"

  if [[ "$responses_ok" == "true" && "$stream_ok" == "true" ]]; then
    pass "public generated-key Responses profile contract is clean for buffered and streaming Codex/OpenClaw calls"
  else
    fail "public Responses profile contract failed: responses status=${responses_status:-missing} model=${responses_model:-missing} prefixLeak=${responses_prefix:-missing} text=${responses_text:-empty}; stream status=${stream_status:-missing} model=${stream_model:-missing} prefixLeak=${stream_prefix:-missing} text=${stream_text:-empty} events=${stream_events:-missing}"
  fi
}

check_public_api_browser_boundary() {
  local root_headers dashboard_headers root_code dashboard_code root_type dashboard_type root_error dashboard_error root_html dashboard_html
  root_headers="$(mktemp)"
  dashboard_headers="$(mktemp)"
  root_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$root_headers" -w '%{http_code}' \
      "${API_BASE%/}/" \
      -H "Accept: text/html"
  )"
  root_error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  root_html="$(grep -Eiq '<html|Sage Router Dashboard|id="dashboard"' /tmp/sage-router-readiness-body && printf true || printf false)"
  rm -f /tmp/sage-router-readiness-body
  dashboard_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$dashboard_headers" -w '%{http_code}' \
      "${API_BASE%/}/dashboard" \
      -H "Accept: text/html"
  )"
  dashboard_error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  dashboard_html="$(grep -Eiq '<html|Sage Router Dashboard|id="dashboard"' /tmp/sage-router-readiness-body && printf true || printf false)"
  root_type="$(awk 'tolower($1)=="content-type:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$root_headers" | tail -n1)"
  dashboard_type="$(awk 'tolower($1)=="content-type:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$dashboard_headers" | tail -n1)"
  rm -f "$root_headers" "$dashboard_headers" /tmp/sage-router-readiness-body

  if [[ "$root_code" == "401" &&
        "$dashboard_code" == "401" &&
        "$root_error" == "unauthorized" &&
        "$dashboard_error" == "unauthorized" &&
        "$root_type" == application/json* &&
        "$dashboard_type" == application/json* &&
        "$root_html" == "false" &&
        "$dashboard_html" == "false" ]]; then
    pass "public API root and dashboard paths stay JSON-auth gated; browser app remains on app.sagerouter.dev"
  else
    fail "public API browser boundary incomplete: / code=${root_code} type=${root_type:-missing} error=${root_error:-missing} html=${root_html}; /dashboard code=${dashboard_code} type=${dashboard_type:-missing} error=${dashboard_error:-missing} html=${dashboard_html}"
  fi
}

check_browser_api_cors() {
  local headers code allow_origin allow_methods allow_headers chat_headers chat_code chat_allow_origin chat_allow_methods chat_allow_headers funnel_headers funnel_code funnel_allow_origin funnel_allow_headers admin_headers admin_code admin_allow_origin admin_allow_methods admin_allow_headers admin_post_headers admin_post_code admin_post_allow_origin admin_post_allow_methods admin_post_allow_headers
  headers="$(mktemp)"
  code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$headers" -w '%{http_code}' \
      -X OPTIONS "${API_BASE%/}/v1/models" \
      -H "Origin: ${APP_BASE%/}" \
      -H "Access-Control-Request-Method: GET" \
      -H "Access-Control-Request-Headers: authorization,content-type"
  )"
  allow_origin="$(awk 'tolower($1)=="access-control-allow-origin:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  allow_methods="$(awk 'tolower($1)=="access-control-allow-methods:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  allow_headers="$(awk 'tolower($1)=="access-control-allow-headers:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  rm -f "$headers" /tmp/sage-router-readiness-body

  chat_headers="$(mktemp)"
  chat_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$chat_headers" -w '%{http_code}' \
      -X OPTIONS "${API_BASE%/}/v1/chat/completions" \
      -H "Origin: ${APP_BASE%/}" \
      -H "Access-Control-Request-Method: POST" \
      -H "Access-Control-Request-Headers: authorization,content-type"
  )"
  chat_allow_origin="$(awk 'tolower($1)=="access-control-allow-origin:" {sub(/\r$/,"",$2); print $2}' "$chat_headers" | tail -n1)"
  chat_allow_methods="$(awk 'tolower($1)=="access-control-allow-methods:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$chat_headers" | tail -n1)"
  chat_allow_headers="$(awk 'tolower($1)=="access-control-allow-headers:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$chat_headers" | tail -n1)"
  rm -f "$chat_headers" /tmp/sage-router-readiness-body

  funnel_headers="$(mktemp)"
  funnel_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$funnel_headers" -w '%{http_code}' \
      -X OPTIONS "${API_BASE%/}/analytics/funnel?days=30" \
      -H "Origin: ${APP_BASE%/}" \
      -H "Access-Control-Request-Method: GET" \
      -H "Access-Control-Request-Headers: authorization"
  )"
  funnel_allow_origin="$(awk 'tolower($1)=="access-control-allow-origin:" {sub(/\r$/,"",$2); print $2}' "$funnel_headers" | tail -n1)"
  funnel_allow_headers="$(awk 'tolower($1)=="access-control-allow-headers:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$funnel_headers" | tail -n1)"
  rm -f "$funnel_headers" /tmp/sage-router-readiness-body

  admin_headers="$(mktemp)"
  admin_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$admin_headers" -w '%{http_code}' \
      -X OPTIONS "${API_BASE%/}/admin/customers?limit=1" \
      -H "Origin: ${APP_BASE%/}" \
      -H "Access-Control-Request-Method: GET" \
      -H "Access-Control-Request-Headers: authorization"
  )"
  admin_allow_origin="$(awk 'tolower($1)=="access-control-allow-origin:" {sub(/\r$/,"",$2); print $2}' "$admin_headers" | tail -n1)"
  admin_allow_methods="$(awk 'tolower($1)=="access-control-allow-methods:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$admin_headers" | tail -n1)"
  admin_allow_headers="$(awk 'tolower($1)=="access-control-allow-headers:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$admin_headers" | tail -n1)"
  rm -f "$admin_headers" /tmp/sage-router-readiness-body

  admin_post_headers="$(mktemp)"
  admin_post_code="$(
    curl -sS -o /tmp/sage-router-readiness-body -D "$admin_post_headers" -w '%{http_code}' \
      -X OPTIONS "${API_BASE%/}/admin/customers/customer_1/suspend" \
      -H "Origin: ${APP_BASE%/}" \
      -H "Access-Control-Request-Method: POST" \
      -H "Access-Control-Request-Headers: authorization,content-type"
  )"
  admin_post_allow_origin="$(awk 'tolower($1)=="access-control-allow-origin:" {sub(/\r$/,"",$2); print $2}' "$admin_post_headers" | tail -n1)"
  admin_post_allow_methods="$(awk 'tolower($1)=="access-control-allow-methods:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$admin_post_headers" | tail -n1)"
  admin_post_allow_headers="$(awk 'tolower($1)=="access-control-allow-headers:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$admin_post_headers" | tail -n1)"
  rm -f "$admin_post_headers" /tmp/sage-router-readiness-body

  if [[ "$code" == "204" && "$allow_origin" == "${APP_BASE%/}" && "$allow_methods" == *"GET"* && "$allow_methods" == *"OPTIONS"* && "$allow_headers" == *"Authorization"* &&
        "$chat_code" == "204" && "$chat_allow_origin" == "${APP_BASE%/}" && "$chat_allow_methods" == *"POST"* && "$chat_allow_methods" == *"OPTIONS"* && "$chat_allow_headers" == *"Authorization"* &&
        "$funnel_code" == "204" && "$funnel_allow_origin" == "${APP_BASE%/}" && "$funnel_allow_headers" == *"Authorization"* &&
        "$admin_code" == "204" && "$admin_allow_origin" == "${APP_BASE%/}" && "$admin_allow_methods" == *"GET"* && "$admin_allow_headers" == *"Authorization"* &&
        "$admin_post_code" == "204" && "$admin_post_allow_origin" == "${APP_BASE%/}" && "$admin_post_allow_methods" == *"POST"* && "$admin_post_allow_headers" == *"Authorization"* && "$admin_post_allow_headers" == *"Content-Type"* ]]; then
    pass "browser API-key verification, first routed request, operator launch funnel CORS preflights are enabled, and operator customer review CORS preflights are enabled"
  else
    fail "browser CORS preflight failed: /v1/models code=${code} allowOrigin=${allow_origin:-missing} allowMethods=${allow_methods:-missing} allowHeaders=${allow_headers:-missing}; /v1/chat/completions code=${chat_code} allowOrigin=${chat_allow_origin:-missing} allowMethods=${chat_allow_methods:-missing} allowHeaders=${chat_allow_headers:-missing}; /analytics/funnel code=${funnel_code} allowOrigin=${funnel_allow_origin:-missing} allowHeaders=${funnel_allow_headers:-missing}; /admin/customers code=${admin_code} allowOrigin=${admin_allow_origin:-missing} allowMethods=${admin_allow_methods:-missing} allowHeaders=${admin_allow_headers:-missing}; /admin/customers suspend code=${admin_post_code} allowOrigin=${admin_post_allow_origin:-missing} allowMethods=${admin_post_allow_methods:-missing} allowHeaders=${admin_post_allow_headers:-missing}"
  fi
}

check_account_mutation_origin_guard() {
  local code error
  code="$(curl -sS -o /tmp/sage-router-readiness-body -w '%{http_code}' \
    -X POST "${API_BASE%/}/account/api-keys" \
    -H "Origin: https://evil.example" \
    -H "Authorization: Bearer invalid-readiness-probe" \
    -H "Content-Type: application/json" \
    --data '{"name":"origin-guard-probe"}')"
  error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body

  if [[ "$code" == "403" && "$error" == "origin_not_allowed" ]]; then
    pass "account and billing browser mutations reject untrusted origins before auth lookup"
  else
    fail "account mutation origin guard failed: code=${code} error=${error:-missing}, expected 403 origin_not_allowed"
  fi
}

check_static_security_headers() {
  local url="$1"
  local label="$2"
  local headers code hsts csp nosniff referrer frame permissions csp_state
  headers="$(mktemp)"
  code="$(curl -sSL -o /tmp/sage-router-readiness-body -D "$headers" -w '%{http_code}' "$url")"
  hsts="$(awk 'tolower($1)=="strict-transport-security:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  csp="$(awk 'tolower($1)=="content-security-policy:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  nosniff="$(awk 'tolower($1)=="x-content-type-options:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  referrer="$(awk 'tolower($1)=="referrer-policy:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  frame="$(awk 'tolower($1)=="x-frame-options:" {sub(/\r$/,"",$2); print $2}' "$headers" | tail -n1)"
  permissions="$(awk 'tolower($1)=="permissions-policy:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  csp_state="$([[ -n "$csp" ]] && printf present || printf missing)"
  rm -f "$headers" /tmp/sage-router-readiness-body

  if [[ "$code" == "200" &&
        "$hsts" == *"max-age="* &&
        "$csp" == *"default-src 'self'"* &&
        "$csp" == *"object-src 'none'"* &&
        "$csp" == *"frame-ancestors 'none'"* &&
        "$csp" == *"connect-src"* &&
        "$csp" == *"https://api.sagerouter.dev"* &&
        "$csp" == *"https://awtangrlqqsdpksarhwo.supabase.co"* &&
        "$nosniff" == "nosniff" &&
        "$referrer" == "strict-origin-when-cross-origin" &&
        "$frame" == "DENY" &&
        "$permissions" == *"camera=()"* ]]; then
    pass "${label} static security headers include HSTS, CSP, nosniff, frame, referrer, and permissions policy"
  else
    fail "${label} static security headers incomplete: code=${code} hsts=${hsts:-missing} csp=${csp_state} nosniff=${nosniff:-missing} referrer=${referrer:-missing} frame=${frame:-missing} permissions=${permissions:-missing}"
  fi
}

check_public_pricing_metadata() {
  local code plans api_base openai_base checkout_path portal_path api_key_limit limits_ok stripe_ok billing_ok billing_secret_free launch_ok activation_email_ok activation_email_configured activation_email_provider activation_email_setup
  code="$(http_code "${API_BASE%/}/pricing")"
  if [[ "$code" != "200" ]]; then
    rm -f /tmp/sage-router-readiness-body
    fail "public /pricing returned HTTP ${code}, expected 200"
    return
  fi
  plans="$(jq -r '((.plans // {}) | keys | length)' /tmp/sage-router-readiness-body)"
  api_base="$(jq -r '.apiBaseUrl // empty' /tmp/sage-router-readiness-body)"
  openai_base="$(jq -r '.openaiBaseUrl // empty' /tmp/sage-router-readiness-body)"
  checkout_path="$(jq -r '.checkoutPath // empty' /tmp/sage-router-readiness-body)"
  portal_path="$(jq -r '.billingPortalPath // empty' /tmp/sage-router-readiness-body)"
  api_key_limit="$(jq -r '.maxActiveApiKeysPerCustomer // 0' /tmp/sage-router-readiness-body)"
  limits_ok="$(jq -r '
    (.plans.lite.limits.monthlyRequests == 10000) and
    (.plans.lite.limits.rateLimitPerMinute == 60) and
    (.plans.pro.limits.monthlyRequests == 50000) and
    (.plans.pro.limits.rateLimitPerMinute == 180) and
    (.plans.max.limits.monthlyRequests == 200000) and
    (.plans.max.limits.rateLimitPerMinute == 600)
  ' /tmp/sage-router-readiness-body)"
  stripe_ok="$(jq -r '
    (.plans.lite.stripeConfigured == true) and
    (.plans.pro.stripeConfigured == true) and
    (.plans.max.stripeConfigured == true)
  ' /tmp/sage-router-readiness-body)"
  billing_ok="$(jq -r '
    (.billing.stripe.configured == true) and
    (.billing.stripe.checkoutReady == true) and
    (.billing.stripe.billingPortalReady == true) and
    (.billing.stripe.checkoutPath == "/billing/stripe/checkout") and
    (.billing.stripe.billingPortalPath == "/billing/stripe/portal") and
    (.billing.stripe.requiresSignedInUser == true) and
    (.billing.stripe.requiresVerifiedEmail == true) and
    ((.billing.stripe.configuredPlans // []) | index("lite")) and
    ((.billing.stripe.configuredPlans // []) | index("pro")) and
    ((.billing.stripe.configuredPlans // []) | index("max")) and
    (.billing.manualSettlement.intentPath == "/billing/crypto/intent") and
    (.billing.manualSettlement.statusPath == "/billing/crypto/status") and
    (.billing.manualSettlement.requiresOperatorApproval == true) and
    ((.billing.activation.activeStatuses // []) | index("active")) and
    ((.billing.activation.activeStatuses // []) | index("trialing")) and
    ((.billing.activation.apiPlans // []) | index("lite")) and
    ((.billing.activation.apiPlans // []) | index("pro")) and
    ((.billing.activation.apiPlans // []) | index("max")) and
    ((.billing.activation.apiPlans // []) | index("metered")) and
    (.billing.activation.generatedApiKeyPrefix == "sk_sage_") and
    (.billing.activation.maxActiveApiKeysPerCustomer == 5)
  ' /tmp/sage-router-readiness-body)"
  billing_secret_free="$(grep -Eq 'price_|sk_live_|sk_test_|rk_live_|rk_test_' /tmp/sage-router-readiness-body && printf false || printf true)"
  launch_ok="$(jq -r '
    (.publicLaunch.targetMrrUsd == 10000) and
    (.publicLaunch.recommendedMix.monthlyRevenueUsd == 10200) and
    ((.publicLaunch.revenuePaths // []) | length == 4) and
    ((.publicLaunch.revenuePaths // []) | any(.label == "Pro-only" and .mix.proCustomers == 334 and .monthlyRevenueUsd == 10020)) and
    ((.publicLaunch.revenuePaths // []) | any(.label == "Max-only" and .mix.maxCustomers == 139 and .monthlyRevenueUsd == 10008)) and
    ((.publicLaunch.revenuePaths // []) | any(.label == "Recommended mixed path" and .mix.liteCustomers == 100 and .mix.proCustomers == 200 and .mix.maxCustomers == 50 and .monthlyRevenueUsd == 10200)) and
    ((.publicLaunch.conversionFunnelTargets // []) | length == 5) and
    ((.publicLaunch.conversionFunnelTargets // []) | any(.stage == "visitor_to_signup" and .targetRate == 0.05)) and
    ((.publicLaunch.conversionFunnelTargets // []) | any(.stage == "signup_to_generated_key" and .targetRate == 0.60)) and
    ((.publicLaunch.conversionFunnelTargets // []) | any(.stage == "generated_key_to_first_routed_request" and .targetRate == 0.50)) and
    ((.publicLaunch.conversionFunnelTargets // []) | any(.stage == "trial_or_free_to_paid" and .targetRate == 0.15)) and
    ((.publicLaunch.conversionFunnelTargets // []) | any(.stage == "paid_logo_monthly_retention" and .targetRate == 0.85)) and
    (.publicLaunch.primaryRevenueModel == "hosted_routing_control_plane") and
    (.publicLaunch.pricingPage == "https://sagerouter.dev/pricing") and
    (.publicLaunch.modelCatalogPage == "https://sagerouter.dev/models") and
    ((.publicLaunch.complianceBoundary // "") | contains("does not grant unauthorized model access"))
  ' /tmp/sage-router-readiness-body)"
  activation_email_configured="$(jq -r '.activationEmailReadiness.configured // false' /tmp/sage-router-readiness-body)"
  activation_email_provider="$(jq -r '.activationEmailReadiness.provider // empty' /tmp/sage-router-readiness-body)"
  activation_email_setup="$(jq -r '.activationEmailReadiness.setupScript // empty' /tmp/sage-router-readiness-body)"
  activation_email_ok="$(jq -r '
    (.activationEmailReadiness.configured == true) and
    ((.activationEmailReadiness.provider == "resend") or (.activationEmailReadiness.provider == "supabase-recovery")) and
    (.activationEmailReadiness.sendsEmailWhenConfigured == true) and
    (
      (
        (.activationEmailReadiness.provider == "resend") and
        (.activationEmailReadiness.fromConfigured == true) and
        (.activationEmailReadiness.apiKeyConfigured == true)
      ) or (
        (.activationEmailReadiness.provider == "supabase-recovery") and
        (.activationEmailReadiness.supabaseConfigured == true) and
        (.activationEmailReadiness.recoveryRedirectConfigured == true)
      )
    ) and
    (.activationEmailReadiness.dryRunSupported == true) and
    (.activationEmailReadiness.setupScript == "scripts/configure_activation_email_sender.sh") and
    (.activationEmailReadiness.privacy.containsSecrets == false) and
    (.activationEmailReadiness.privacy.containsEmails == false) and
    (.activationEmailReadiness.privacy.containsAdminCommands == false)
  ' /tmp/sage-router-readiness-body)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$plans" =~ ^[0-9]+$ && "$plans" -gt 0 && "$api_key_limit" =~ ^[0-9]+$ && "$api_key_limit" -gt 0 && "$api_base" == "${API_BASE%/}" && "$openai_base" == "${API_BASE%/}/v1" && "$checkout_path" == "/billing/stripe/checkout" && "$portal_path" == "/billing/stripe/portal" && "$limits_ok" == "true" && "$stripe_ok" == "true" && "$billing_ok" == "true" && "$billing_secret_free" == "true" && "$launch_ok" == "true" && "$activation_email_ok" == "true" ]]; then
    pass "public /pricing exposes hosted plan, secret-free Stripe checkout readiness, activation email sender readiness, endpoint, limit, and launch metadata"
  else
    fail "public /pricing metadata incomplete: plans=${plans:-missing} apiBaseUrl=${api_base:-missing} openaiBaseUrl=${openai_base:-missing} checkoutPath=${checkout_path:-missing} billingPortalPath=${portal_path:-missing} apiKeyLimit=${api_key_limit:-missing} limits=${limits_ok:-missing} stripe=${stripe_ok:-missing} billing=${billing_ok:-missing} billingSecretFree=${billing_secret_free:-missing} launch=${launch_ok:-missing} activationEmail=${activation_email_ok:-missing} activationEmailConfigured=${activation_email_configured:-missing} activationEmailProvider=${activation_email_provider:-missing} activationEmailSetup=${activation_email_setup:-missing}. Configure with scripts/configure_activation_email_sender.sh before treating signup recovery as launch-ready."
  fi
}

check_public_model_catalog() {
  local code families auth_required page openai_base boundary_ok
  code="$(http_code "${API_BASE%/}/model-catalog")"
  if [[ "$code" != "200" ]]; then
    rm -f /tmp/sage-router-readiness-body
    fail "public /model-catalog returned HTTP ${code}, expected 200"
    return
  fi
  families="$(jq -r '((.modelCatalog.families // []) | length)' /tmp/sage-router-readiness-body)"
  auth_required="$(jq -r '.modelCatalog.modelApiRequiresGeneratedKey // false' /tmp/sage-router-readiness-body)"
  page="$(jq -r '.modelCatalog.catalogPage // empty' /tmp/sage-router-readiness-body)"
  openai_base="$(jq -r '.modelCatalog.openaiBaseUrl // empty' /tmp/sage-router-readiness-body)"
  boundary_ok="$(jq -r '
    ((.modelCatalog.safetyBoundary // "") | contains("not a promise of bundled model resale")) and
    ((.modelCatalog.families // []) | any(.id == "sage-router-profiles")) and
    ((.modelCatalog.families // []) | any(.id == "ollama")) and
    ((.modelCatalog.families // []) | any(.id == "byok-compatible"))
  ' /tmp/sage-router-readiness-body)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$families" =~ ^[0-9]+$ && "$families" -ge 5 && "$auth_required" == "true" && "$page" == "${MARKETING_BASE%/}/models" && "$openai_base" == "${API_BASE%/}/v1" && "$boundary_ok" == "true" ]]; then
    pass "public /model-catalog exposes safe model-family discovery while /v1/models remains key-gated"
  else
    fail "public /model-catalog metadata incomplete: families=${families:-missing} authRequired=${auth_required:-missing} page=${page:-missing} openaiBaseUrl=${openai_base:-missing} boundary=${boundary_ok:-missing}"
  fi
}

check_managed_provider_access_guard() {
  local code enabled requested readiness_satisfied status terms_url terms_ack terms_ack_env_ok allowlist_count margin_url acceptable_url controls_ok margin_percent unit_economics_ok cost_model_configured unit_economics_satisfied unit_economics_plans_ok unit_economics_safe_thresholds_ok cost_controls_ok provider_family_boundary_ok readiness_setup_ok missing_controls_explain_blockers_ok one_subscription_action_ok missing_count
  code="$(http_code "${API_BASE%/}/pricing")"
  if [[ "$code" != "200" ]]; then
    rm -f /tmp/sage-router-readiness-body
    fail "managed provider access guard could not read /pricing: HTTP ${code}"
    return
  fi
  enabled="$(jq -r '.publicLaunch.managedProviderAccess.enabled // false' /tmp/sage-router-readiness-body)"
  requested="$(jq -r '.publicLaunch.managedProviderAccess.requested // false' /tmp/sage-router-readiness-body)"
  readiness_satisfied="$(jq -r '.publicLaunch.managedProviderAccess.readinessSatisfied // false' /tmp/sage-router-readiness-body)"
  status="$(jq -r '.publicLaunch.managedProviderAccess.status // empty' /tmp/sage-router-readiness-body)"
  terms_url="$(jq -r '.publicLaunch.managedProviderAccess.providerTermsUrl // empty' /tmp/sage-router-readiness-body)"
  terms_ack="$(jq -r '.publicLaunch.managedProviderAccess.providerTermsAcknowledged // false' /tmp/sage-router-readiness-body)"
  auth_evidence="$(jq -r '.publicLaunch.managedProviderAccess.providerAuthorizationEvidenceConfigured // false' /tmp/sage-router-readiness-body)"
  allowlist_count="$(jq -r '(.publicLaunch.managedProviderAccess.allowedProviderFamilies // []) | length' /tmp/sage-router-readiness-body)"
  margin_url="$(jq -r '.publicLaunch.managedProviderAccess.marginPolicyUrl // empty' /tmp/sage-router-readiness-body)"
  acceptable_url="$(jq -r '.publicLaunch.managedProviderAccess.acceptableUseUrl // empty' /tmp/sage-router-readiness-body)"
  margin_percent="$(jq -r '.publicLaunch.managedProviderAccess.minimumGrossMarginPercent // 0' /tmp/sage-router-readiness-body)"
  unit_economics_ok="$(jq -r '.publicLaunch.managedProviderAccess.requiresPositiveUnitEconomics // false' /tmp/sage-router-readiness-body)"
  cost_model_configured="$(jq -r '.publicLaunch.managedProviderAccess.unitEconomics.costModelConfigured // false' /tmp/sage-router-readiness-body)"
  unit_economics_satisfied="$(jq -r '.publicLaunch.managedProviderAccess.unitEconomics.satisfied // false' /tmp/sage-router-readiness-body)"
  unit_economics_plans_ok="$(jq -r '
    ((.publicLaunch.managedProviderAccess.unitEconomics.evaluatedPlans // []) | length) >= 3 and
    ((.publicLaunch.managedProviderAccess.unitEconomics.evaluatedPlans // []) | all(.meetsMinimumGrossMargin == true))
  ' /tmp/sage-router-readiness-body)"
  unit_economics_safe_thresholds_ok="$(jq -r '
    ((.publicLaunch.managedProviderAccess.unitEconomics.evaluatedPlans // []) | length) >= 3 and
    ((.publicLaunch.managedProviderAccess.unitEconomics.evaluatedPlans // []) | all(
      (.maximumProviderCostCentsPerThousandRequests // 0) > 0 and
      (.revenueCentsPerThousandRequests // 0) >= (.maximumProviderCostCentsPerThousandRequests // 0)
    ))
  ' /tmp/sage-router-readiness-body)"
  controls_ok="$(jq -r '
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("provider_resale_terms")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("margin_policy")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("positive_unit_economics")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("provider_terms_acknowledgment")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("provider_authorization_evidence")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("authorized_provider_allowlist")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("provider_cost_metering")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("per_plan_usage_caps")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("rate_limits_and_durable_quotas")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("generated_key_revocation")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("operator_abuse_review")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("operator_audit_events")) and
    ((.publicLaunch.managedProviderAccess.requiredControls // []) | index("acceptable_use_managed_access_terms"))
  ' /tmp/sage-router-readiness-body)"
  cost_controls_ok="$(jq -r '
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("per_plan_monthly_quotas")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("request_per_minute_limits")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("durable_usage_accounting")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("generated_key_revocation")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("operator_customer_review")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("operator_audit_events")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("authorized_provider_allowlist")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("provider_resale_terms")) and
    ((.publicLaunch.managedProviderAccess.costControls // []) | index("managed_access_acceptable_use"))
  ' /tmp/sage-router-readiness-body)"
  provider_family_boundary_ok="$(jq -r '
    ((.publicLaunch.managedProviderAccess.providerFamilyReadiness // []) | length) >= 5 and
    ((.publicLaunch.managedProviderAccess.providerFamilyReadiness // []) | any(
      .family == "openrouter" and
      .byokOnly == true and
      .resaleEligible == false and
      .ready == false and
      .status == "byok_supported_not_managed_resale"
    )) and
    ((.publicLaunch.managedProviderAccess.providerFamilyReadiness // []) | any(.family == "ollama" and .resaleEligible == true)) and
    ((.publicLaunch.managedProviderAccess.providerFamilyReadiness // []) | any(.family == "openai" and .resaleEligible == true)) and
    ((.publicLaunch.managedProviderAccess.providerFamilyReadiness // []) | any(.family == "anthropic" and .resaleEligible == true)) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.safeForPublicDisplay // false) == true) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.commercialPreference // "") == "one-subscription") and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.byokOnlyProviderFamilies // []) | index("openrouter")) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.resaleEligibleProviderFamilies // []) | index("ollama")) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.resaleEligibleProviderFamilies // []) | index("openai")) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.resaleEligibleProviderFamilies // []) | index("anthropic"))
  ' /tmp/sage-router-readiness-body)"
  one_subscription_action_ok="$(MARKETING_BASE="${MARKETING_BASE%/}" jq -r '
    (.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.safeForPublicDisplay // false) == true and
    (.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.managedAccessUrl == (env.MARKETING_BASE + "/managed-access")) and
    ((.publicLaunch.managedProviderAccess.oneSubscriptionReadiness.blockedProviderFamilies // []) | length) > 0 and
    ((.publicLaunch.managedProviderAccess.providerBoundary // "") | contains("OpenRouter")) and
    ((.publicLaunch.managedProviderAccess.providerBoundary // "") | contains("BYOK-compatible"))
  ' /tmp/sage-router-readiness-body)"
  missing_controls_explain_blockers_ok="$(jq -r '
    .publicLaunch.managedProviderAccess as $managed |
    ($managed.missingControls // []) as $missing |
    (
      ($managed.providerTermsUrl // "") != "" or
      ($missing | index("provider_resale_terms"))
    ) and
    (
      ($managed.providerTermsAcknowledged == true) or
      ($missing | index("provider_terms_acknowledgment"))
    ) and
    (
      ($managed.providerAuthorizationEvidenceConfigured == true) or
      ($missing | index("provider_authorization_evidence"))
    ) and
    (
      (($managed.allowedProviderFamilies // []) | length) > 0 or
      ($missing | index("authorized_provider_allowlist"))
    ) and
    (
      ($managed.marginPolicyUrl // "") != "" or
      ($missing | index("margin_policy"))
    ) and
    (
      ($managed.unitEconomics.costModelConfigured == true) or
      ($missing | index("provider_cost_model"))
    ) and
    (
      ($managed.unitEconomics.satisfied == true) or
      ($missing | index("positive_unit_economics"))
    )
  ' /tmp/sage-router-readiness-body)"
  readiness_setup_ok="$(jq -r '
    (.publicLaunch.managedProviderAccess.readinessSetup.setupScript == "scripts/configure_managed_provider_resale_readiness.sh") and
    ((.publicLaunch.managedProviderAccess.readinessSetup.dryRunCommand // "") | contains("scripts/configure_managed_provider_resale_readiness.sh --check")) and
    ((.publicLaunch.managedProviderAccess.readinessSetup.enableCommandTemplate // "") | contains("SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC")) and
    (
      (.publicLaunch.managedProviderAccess.enabled == true) or
      ((.publicLaunch.managedProviderAccess.readinessSetup.requiredEnv // []) | index("SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS"))
    ) and
    ((.publicLaunch.managedProviderAccess.readinessSetup.secretManagerNames // []) | index("SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS")) and
    (.publicLaunch.managedProviderAccess.readinessSetup.defaultPublicEnable == false) and
    (.publicLaunch.managedProviderAccess.readinessSetup.requiresExplicitPublicEnableEnv == "SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC") and
    (.publicLaunch.managedProviderAccess.readinessSetup.privacy.containsSecrets == false) and
    (.publicLaunch.managedProviderAccess.readinessSetup.privacy.containsActualProviderCosts == false)
  ' /tmp/sage-router-readiness-body)"
  missing_count="$(jq -r '(.publicLaunch.managedProviderAccess.missingControls // []) | length' /tmp/sage-router-readiness-body)"
  rm -f /tmp/sage-router-readiness-body
  case "${PROVIDER_RESALE_TERMS_ACKNOWLEDGED,,}" in
    1|true|yes|on) terms_ack_env_ok="true" ;;
    *) terms_ack_env_ok="false" ;;
  esac

  case "${MANAGED_PROVIDER_RESALE_ENABLED,,}" in
    1|true|yes|on)
      if [[ "$enabled" == "true" &&
            "$requested" == "true" &&
            "$readiness_satisfied" == "true" &&
            "$status" == "ready_for_private_beta" &&
            -n "$PROVIDER_RESALE_TERMS_URL" &&
            -n "$PROVIDER_RESALE_MARGIN_POLICY_URL" &&
            -n "$PROVIDER_RESALE_ALLOWED_PROVIDERS" &&
            "$terms_url" == "$PROVIDER_RESALE_TERMS_URL" &&
            "$terms_ack" == "true" &&
            "$auth_evidence" == "true" &&
            "$terms_ack_env_ok" == "true" &&
            "$margin_url" == "$PROVIDER_RESALE_MARGIN_POLICY_URL" &&
            "$acceptable_url" == "${MARKETING_BASE%/}/acceptable-use" &&
            "$allowlist_count" =~ ^[0-9]+$ &&
            "$allowlist_count" -gt 0 &&
            "$controls_ok" == "true" &&
            "$cost_controls_ok" == "true" &&
            "$unit_economics_ok" == "true" &&
            "$cost_model_configured" == "true" &&
            "$unit_economics_satisfied" == "true" &&
            "$unit_economics_plans_ok" == "true" &&
            "$unit_economics_safe_thresholds_ok" == "true" &&
            "$provider_family_boundary_ok" == "true" &&
            "$one_subscription_action_ok" == "true" &&
            "$missing_controls_explain_blockers_ok" == "true" &&
            "$readiness_setup_ok" == "true" &&
            "$margin_percent" =~ ^[0-9]+$ &&
            "$margin_percent" -ge 30 &&
            "$missing_count" == "0" ]]; then
        pass "managed provider access is explicitly enabled with acknowledged resale terms, provider authorization evidence, a provider allowlist, positive unit economics, provider-family BYOK boundary, margin policy, quotas, operator audit events, and acceptable-use controls"
      else
        fail "managed provider access enabled without complete controls, including acknowledged resale terms, provider authorization evidence, provider allowlist, positive unit economics, provider-family BYOK boundary, one-subscription action link, operator audit events, managed-access setup guard, and managed-access acceptable-use boundary: enabled=${enabled} requested=${requested:-missing} readinessSatisfied=${readiness_satisfied:-missing} status=${status:-missing} terms=${terms_url:+present} termsAcknowledged=${terms_ack:-missing} authorizationEvidence=${auth_evidence:-missing} allowedProviderFamilies=${allowlist_count:-missing} margin=${margin_url:+present} minimumGrossMarginPercent=${margin_percent:-missing} positiveUnitEconomics=${unit_economics_ok:-missing} costModelConfigured=${cost_model_configured:-missing} unitEconomicsSatisfied=${unit_economics_satisfied:-missing} unitEconomicsPlans=${unit_economics_plans_ok:-missing} unitEconomicsSafeThresholds=${unit_economics_safe_thresholds_ok:-missing} providerFamilyBoundary=${provider_family_boundary_ok:-missing} oneSubscriptionAction=${one_subscription_action_ok:-missing} missingControlsExplainBlockers=${missing_controls_explain_blockers_ok:-missing} readinessSetup=${readiness_setup_ok:-missing} acceptableUse=${acceptable_url:-missing} controls=${controls_ok:-missing} costControls=${cost_controls_ok:-missing} missingControls=${missing_count:-missing}"
      fi
      ;;
    *)
      if [[ "$enabled" == "false" && "$requested" == "false" && "$readiness_satisfied" == "false" && "$status" == "disabled_pending_provider_terms" && "$terms_ack" == "false" && "$controls_ok" == "true" && "$cost_controls_ok" == "true" && "$unit_economics_ok" == "true" && "$unit_economics_safe_thresholds_ok" == "true" && "$provider_family_boundary_ok" == "true" && "$one_subscription_action_ok" == "true" && "$missing_controls_explain_blockers_ok" == "true" && "$readiness_setup_ok" == "true" && "$margin_percent" =~ ^[0-9]+$ && "$margin_percent" -ge 30 && "$missing_count" =~ ^[0-9]+$ && "$missing_count" -gt 0 ]]; then
        pass "managed provider access remains disabled until provider resale terms are acknowledged, provider authorization evidence, provider allowlist, positive unit economics, provider-family BYOK boundary, margin policy, quotas, operator audit events, setup guard, and acceptable-use controls are ready"
      else
        fail "managed provider access guard unexpected: enabled=${enabled} requested=${requested:-missing} readinessSatisfied=${readiness_satisfied:-missing} status=${status:-missing} termsAcknowledged=${terms_ack:-missing} authorizationEvidence=${auth_evidence:-missing} allowedProviderFamilies=${allowlist_count:-missing} minimumGrossMarginPercent=${margin_percent:-missing} positiveUnitEconomics=${unit_economics_ok:-missing} unitEconomicsSafeThresholds=${unit_economics_safe_thresholds_ok:-missing} providerFamilyBoundary=${provider_family_boundary_ok:-missing} oneSubscriptionAction=${one_subscription_action_ok:-missing} missingControlsExplainBlockers=${missing_controls_explain_blockers_ok:-missing} readinessSetup=${readiness_setup_ok:-missing} controls=${controls_ok:-missing} costControls=${cost_controls_ok:-missing} missingControls=${missing_count:-missing}, expected disabled_pending_provider_terms"
      fi
      ;;
  esac
}

check_stripe_webhook_guard() {
  local code error
  code="$(http_code "${API_BASE%/}/billing/stripe/webhook" \
    -H "Content-Type: application/json" \
    --data '{"id":"evt_readiness_unsigned","type":"readiness.probe"}')"
  error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$code" == "400" && "$error" == "invalid_signature" ]]; then
    pass "Stripe webhook endpoint is configured and rejects unsigned events"
  else
    fail "Stripe webhook guard returned HTTP ${code} error=${error:-missing}, expected 400 invalid_signature"
  fi
}

check_hosted_onboarding_pages() {
  local login_code account_code analytics_code launch_funnel_code launch_funnel_js_code manifest_code status_code status_js_code
  login_code="$(http_code_follow "${APP_BASE%/}/login.html")"
  if [[ "$login_code" == "200" ]] && ! grep -q "Login · Sage Router" /tmp/sage-router-readiness-body; then
    login_code="200:unexpected-body"
  fi
  if [[ "$login_code" == "200" ]] && ! grep -q "Finish setup key" /tmp/sage-router-readiness-body; then
    login_code="200:missing-login-key-recovery"
  fi
  if [[ "$login_code" == "200" ]] && ! grep -q "No provider key or checkout is required until your" /tmp/sage-router-readiness-body; then
    login_code="200:missing-login-key-recovery-copy"
  fi
  rm -f /tmp/sage-router-readiness-body

  account_code="$(http_code_follow "${APP_BASE%/}/account.html")"
  if [[ "$account_code" == "200" ]] && ! grep -q "Sage Router Account" /tmp/sage-router-readiness-body; then
    account_code="200:unexpected-body"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Verify API key" /tmp/sage-router-readiness-body; then
    account_code="200:missing-api-key-verification"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Pro activation path selected" /tmp/sage-router-readiness-body; then
    account_code="200:missing-selected-plan-intent"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "No provider key or credit card is required until your generated" /tmp/sage-router-readiness-body; then
    account_code="200:missing-no-provider-key-or-card-signup-copy"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "key first, then complete checkout" /tmp/sage-router-readiness-body; then
    account_code="200:missing-key-first-account-copy"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "intent-email-form" /tmp/sage-router-readiness-body; then
    account_code="200:missing-direct-email-setup-form"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "intent-email-status" /tmp/sage-router-readiness-body; then
    account_code="200:missing-direct-email-status"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "intent-oauth-actions" /tmp/sage-router-readiness-body; then
    account_code="200:missing-direct-oauth-signup"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Continue with GitHub" /tmp/sage-router-readiness-body; then
    account_code="200:missing-github-signup-shortcut"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Email API key setup link" /tmp/sage-router-readiness-body; then
    account_code="200:missing-magic-link-primary-cta"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "preauth-setup-code" /tmp/sage-router-readiness-body; then
    account_code="200:missing-preauth-setup-code"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Copy setup before signup" /tmp/sage-router-readiness-body; then
    account_code="200:missing-preauth-setup-copy"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "Email setup link next" /tmp/sage-router-readiness-body; then
    account_code="200:missing-preauth-setup-next"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "data-preauth-focus-email" /tmp/sage-router-readiness-body; then
    account_code="200:missing-preauth-email-focus"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "email-verification-status" /tmp/sage-router-readiness-body; then
    account_code="200:missing-email-verification-status"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "resend-verification-email" /tmp/sage-router-readiness-body; then
    account_code="200:missing-email-verification-resend"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "post-key-activation-panel" /tmp/sage-router-readiness-body; then
    account_code="200:missing-post-key-activation-panel"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "post-key-verify-button" /tmp/sage-router-readiness-body; then
    account_code="200:missing-post-key-verify-button"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "post-key-first-request-button" /tmp/sage-router-readiness-body; then
    account_code="200:missing-post-key-first-request-button"
  fi
  if [[ "$account_code" == "200" ]] && ! grep -q "post-key-copy-codex-button" /tmp/sage-router-readiness-body; then
    account_code="200:missing-post-key-codex-copy"
  fi
  rm -f /tmp/sage-router-readiness-body

  analytics_code="$(http_code_follow "${APP_BASE%/}/analytics.html")"
  if [[ "$analytics_code" == "200" ]] && ! grep -q "Router analytics that prove the best route" /tmp/sage-router-readiness-body; then
    analytics_code="200:unexpected-body"
  fi
  rm -f /tmp/sage-router-readiness-body

  launch_funnel_code="$(http_code_follow "${APP_BASE%/}/launch-funnel.html")"
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Private operator dashboard" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:unexpected-body"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "SAGE_ROUTER_API_KEY or analytics token" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-token-boundary"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Launch bottlenecks" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-launch-bottlenecks"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Conversion Actions" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-conversion-actions"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Setup copy to first request" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-setup-copy-activation"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Customer Review" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-customer-review"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "OAuth onboarding state" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-auth-provider-state"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Operator launch brief" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-operator-launch-brief"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "Execution packet" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-operator-execution-packet"
  fi
  if [[ "$launch_funnel_code" == "200" ]] && ! grep -q "operator-execution-packet" /tmp/sage-router-readiness-body; then
    launch_funnel_code="200:missing-operator-execution-packet-container"
  fi
  rm -f /tmp/sage-router-readiness-body

  launch_funnel_js_code="$(http_code_follow "${APP_BASE%/}/launch-funnel.js")"
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "/analytics/funnel" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-funnel-call"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "/admin/customers" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-customer-review-call"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "/admin/customers/send-activation-followups" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-activation-followup-sender"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "Activation email sender" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-activation-email-readiness"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "data-send-followups" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-activation-followup-send-controls"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "operator_no_key_followup_sent" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-activation-followup-send-telemetry"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderReviewFlags" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-customer-review-flags"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "sessionStorage" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-tab-scoped-token-storage"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderBottlenecks" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-bottleneck-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderConversionActions" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-conversion-action-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderRevenueActions" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-revenue-action-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderAcquisitionActions" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-acquisition-action-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderAuthProviderState" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-auth-provider-state-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "setupSnippetCopiesBySnippet" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-setup-copy-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "buildLaunchBrief" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-launch-brief-builder"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "No secrets or customer data" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-launch-brief-privacy-boundary"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "renderOperatorExecutionPacket" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-operator-execution-packet-renderer"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "operator_execution_packet_copied" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-operator-execution-packet-telemetry"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "operatorAuthPosture" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-operator-auth-posture"
  fi
  if [[ "$launch_funnel_js_code" == "200" ]] && ! grep -q "Auth provider state unknown" /tmp/sage-router-readiness-body; then
    launch_funnel_js_code="200:missing-operator-auth-posture-fallback"
  fi
  rm -f /tmp/sage-router-readiness-body

  status_code="$(http_code_follow "${APP_BASE%/}/status")"
  if [[ "$status_code" == "200" ]] && ! grep -q "CDN-style reliability evidence" /tmp/sage-router-readiness-body; then
    status_code="200:missing-reliability-evidence"
  fi
  if [[ "$status_code" == "200" ]] && ! grep -q "SaaS Launch Readiness" /tmp/sage-router-readiness-body; then
    status_code="200:missing-status-launch-readiness"
  fi
  if [[ "$status_code" == "200" ]] && ! grep -q "Operator Launch Actions" /tmp/sage-router-readiness-body; then
    status_code="200:missing-status-operator-launch-actions"
  fi
  rm -f /tmp/sage-router-readiness-body

  status_js_code="$(http_code_follow "${APP_BASE%/}/status.js")"
  if [[ "$status_js_code" == "200" ]] && ! grep -q "renderReliabilityEvidence" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-reliability-renderer"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "cloud fallback" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-cloud-fallback-evidence"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "X-Sage-Router-Retry-Count" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-retry-failover-evidence"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "renderLaunchReadiness" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-status-launch-readiness-renderer"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "activationEmailReadiness" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-status-activation-readiness"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "renderOperatorLaunchActions" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-status-operator-launch-action-renderer"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "One-subscription managed access" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-status-managed-resale-action"
  fi
  if [[ "$status_js_code" == "200" ]] && ! grep -q "Browser Integrity Check" /tmp/sage-router-readiness-body; then
    status_js_code="200:missing-status-bic-guidance"
  fi
  rm -f /tmp/sage-router-readiness-body

  local analytics_js_code
  analytics_js_code="$(http_code_follow "${APP_BASE%/}/analytics.js")"
  if [[ "$analytics_js_code" == "200" ]] && ! grep -q "/account/analytics" /tmp/sage-router-readiness-body; then
    analytics_js_code="200:missing-account-analytics"
  fi
  rm -f /tmp/sage-router-readiness-body

  local account_js_code
  account_js_code="$(http_code_follow "${APP_BASE%/}/account.js")"
  if [[ "$account_js_code" == "200" ]] && ! grep -q "testApiKey" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-api-key-test"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "emailVerification" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-email-verification-flow"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "resendVerificationEmail" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-email-verification-resend-flow"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "account_email_verification_resent" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-email-verification-resend-funnel"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "/account/api-keys/.*revoke" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-api-key-revoke"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "canonicalAccountPageUrl" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-canonical-account-redirect"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "accountPageUrlWithPlan" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-plan-preserving-account-redirect"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "inferredStartActionFromReferrer" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-trusted-referrer-activation"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "create the key first and complete checkout" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-key-first-intent-copy"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "Finish your Sage Router setup key" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-key-recovery-title"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "This recovery link is set to create the generated sk_sage setup key first" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-key-recovery-copy"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "Continue with .* to create setup key" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-key-recovery-oauth-label"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "https://app.sagerouter.dev/account.html" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-app-account-url"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "account_intent_primary_clicked" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-account-intent-funnel"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "account_intent_create_key_clicked" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-account-intent-key-create-funnel"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "account_activation_nudge_shown" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-account-activation-nudge"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "account_auto_oauth_started" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-account-auto-oauth"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "Create the key before checkout" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-account-activation-nudge-copy"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "AUTO_KEY_ATTEMPT_STORAGE_KEY" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-auto-key-intent-guard"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "maybeCreateKeyFromIntent" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-saved-intent-key-create"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "saved_intent_auto_key" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-saved-intent-key-funnel"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "Creating your sk_sage key" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-direct-key-create-status"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "await createKey()" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-direct-key-create-action"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "setAuthStatus" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-inline-auth-status"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "intent_.*button.dataset.oauth" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-intent-oauth-tracking"
  fi
  if [[ "$account_js_code" == "200" ]] && ! grep -q "data-after-key-action" /tmp/sage-router-readiness-body; then
    account_js_code="200:missing-post-key-next-actions"
  fi
  rm -f /tmp/sage-router-readiness-body

  manifest_code="$(http_code_follow "${APP_BASE%/}/github-app-manifest")"
  if [[ "$manifest_code" == "200" ]] && ! grep -q "Finish GitHub auth setup" /tmp/sage-router-readiness-body; then
    manifest_code="200:unexpected-body"
  fi
  if [[ "$manifest_code" == "200" ]] && ! grep -q "bash scripts/bootstrap_github_supabase_auth.sh" /tmp/sage-router-readiness-body; then
    manifest_code="200:missing-github-credential-save-command"
  fi
  if [[ "$manifest_code" == "200" ]] && ! grep -q "/home/digit/.openclaw/sage-router-github-auth.env" /tmp/sage-router-readiness-body; then
    manifest_code="200:missing-github-credential-save-path"
  fi
  if [[ "$manifest_code" == "200" ]] && ! grep -q "preserve the one-time client secret" /tmp/sage-router-readiness-body; then
    manifest_code="200:missing-github-secret-preservation-guidance"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$login_code" == "200" && "$account_code" == "200" && "$analytics_code" == "200" && "$launch_funnel_code" == "200" && "$launch_funnel_js_code" == "200" && "$status_code" == "200" && "$status_js_code" == "200" && "$analytics_js_code" == "200" && "$account_js_code" == "200" && "$manifest_code" == "200" ]]; then
    pass "hosted login, account, API-key verification, analytics, operator launch funnel, reliability status, and GitHub auth callback pages are live; email verification resend, self-service API-key revocation, operator customer review, and GitHub credential preservation guidance are live"
  else
    fail "hosted onboarding pages incomplete: login=${login_code} account=${account_code} account.js=${account_js_code} analytics=${analytics_code} analytics.js=${analytics_js_code} launch-funnel=${launch_funnel_code} launch-funnel.js=${launch_funnel_js_code} status=${status_code} status.js=${status_js_code} github-app-manifest=${manifest_code}"
  fi
}

check_marketing_account_redirects() {
  local headers account_code login_code account_location login_location
  headers="$(mktemp)"
  account_code="$(curl -sS -o /tmp/sage-router-readiness-body -D "$headers" -w '%{http_code}' "${MARKETING_BASE%/}/account.html?plan=pro")"
  account_location="$(awk 'tolower($1)=="location:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  rm -f "$headers" /tmp/sage-router-readiness-body

  headers="$(mktemp)"
  login_code="$(curl -sS -o /tmp/sage-router-readiness-body -D "$headers" -w '%{http_code}' "${MARKETING_BASE%/}/login.html")"
  login_location="$(awk 'tolower($1)=="location:" {$1=""; sub(/^ /,""); sub(/\r$/,""); print}' "$headers" | tail -n1)"
  rm -f "$headers" /tmp/sage-router-readiness-body

  if [[ "$account_code" == "308" && "$account_location" == "${APP_BASE%/}/account.html?plan=pro" && "$login_code" == "308" && "$login_location" == "${APP_BASE%/}/login.html" ]]; then
    pass "marketing-host account and login URLs redirect to canonical app host"
  else
    fail "marketing-host app redirects incomplete: account=${account_code} location=${account_location:-missing}; login=${login_code} location=${login_location:-missing}"
  fi
}

check_public_supabase_auth_settings() {
  local anon_key code email_enabled github_enabled external_type
  anon_key="$(discover_supabase_anon_key)"
  if [[ -z "$anon_key" ]]; then
    warn "Supabase anon key not set and not discoverable from hosted app scripts; skipped public auth settings probe"
    return
  fi

  code="$(http_code "${SUPABASE_URL%/}/auth/v1/settings" -H "apikey: ${anon_key}")"
  if [[ "$code" != "200" ]]; then
    rm -f /tmp/sage-router-readiness-body
    fail "public Supabase auth settings returned HTTP ${code}, expected 200"
    return
  fi
  external_type="$(jq -r '(.external // null) | type' /tmp/sage-router-readiness-body)"
  email_enabled="$(jq -r '.external.email // false' /tmp/sage-router-readiness-body)"
  github_enabled="$(jq -r '.external.github // false' /tmp/sage-router-readiness-body)"
  rm -f /tmp/sage-router-readiness-body
  SUPABASE_PUBLIC_GITHUB_ENABLED="$github_enabled"

  if [[ "$external_type" == "object" && "$email_enabled" == "true" && "$github_enabled" == "true" ]]; then
    pass "public Supabase auth settings expose browser-visible email and GitHub OAuth provider state"
  else
    fail "public Supabase auth settings incomplete: external=${external_type:-missing} email=${email_enabled:-missing} github=${github_enabled:-missing}"
  fi
}

check_waitlist_endpoint() {
  local code ok service turnstile_required turnstile_site_key qualification_ok write_guard referer_fallback preview_suffix
  code="$(http_code "${APP_BASE%/}/api/waitlist")"
  ok="$(jq -r '.ok // false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  service="$(jq -r '.service // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  turnstile_required="$(jq -r '.turnstileRequired // false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  turnstile_site_key="$(jq -r '.turnstileSiteKey // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  write_guard="$(jq -r '.writeGuard.browserOriginRequired == true' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  referer_fallback="$(jq -r '.writeGuard.refererFallbackAccepted == false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  preview_suffix="$(jq -r '.writeGuard.previewHostSuffix // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  qualification_ok="$(jq -r '
    ((.allowedQualificationBuckets.deployment // []) | index("hybrid")) and
    ((.allowedQualificationBuckets.monthlyVolume // []) | index("1m-plus")) and
    ((.allowedQualificationBuckets.providerAccess // []) | index("needs-managed-access")) and
    ((.allowedQualificationBuckets.targetProviderFamily // []) | index("mixed-frontier")) and
    ((.allowedQualificationBuckets.commercialPreference // []) | index("one-subscription"))
  ' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$code" == "200" && "$ok" == "true" && "$service" == "sage-router-waitlist" && "$qualification_ok" == "true" && "$write_guard" == "true" && "$referer_fallback" == "true" && "$preview_suffix" == ".sage-router-web.pages.dev" && ( "$turnstile_required" != "true" || -n "$turnstile_site_key" ) ]]; then
    pass "hosted waitlist endpoint is configured with browser origin guard"
  else
    fail "hosted waitlist endpoint returned HTTP ${code} ok=${ok:-missing} service=${service:-missing} qualificationBuckets=${qualification_ok:-missing} writeGuard=${write_guard:-missing} refererFallbackDisabled=${referer_fallback:-missing} previewSuffix=${preview_suffix:-missing} turnstileRequired=${turnstile_required:-missing} turnstileSiteKey=${turnstile_site_key:+present}"
  fi
}

check_funnel_event_endpoint() {
  local code ok service primary_table privacy_ok allowed_events write_guard referer_fallback preview_suffix smoke_events_persisted
  code="$(http_code "${APP_BASE%/}/api/funnel-event")"
  ok="$(jq -r '.ok // false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  service="$(jq -r '.service // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  primary_table="$(jq -r '.primaryTable // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  privacy_ok="$(jq -r '(.privacy.promptsStored == false) and (.privacy.messageBodiesStored == false) and (.privacy.containsApiKeys == false)' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  allowed_events="$(jq -r '
    ((.allowedEvents // []) | index("calculator_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("calculator_checkout_clicked") != null) and
    ((.allowedEvents // []) | index("calculator_checkout_unavailable") != null) and
    ((.allowedEvents // []) | index("calculator_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("calculator_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("pricing_setup_next_clicked") != null) and
    ((.allowedEvents // []) | index("fusion_viewed") != null) and
    ((.allowedEvents // []) | index("fusion_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("fusion_checkout_clicked") != null) and
    ((.allowedEvents // []) | index("fusion_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("fusion_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("gateway_migration_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("gateway_migration_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("agent_native_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("agent_native_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("integrations_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("integrations_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_viewed") != null) and
    ((.allowedEvents // []) | index("content_article_inline_offer_viewed") != null) and
    ((.allowedEvents // []) | index("content_article_activation_dock_viewed") != null) and
    ((.allowedEvents // []) | index("content_article_quickstart_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("content_article_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_oauth_failed") != null) and
    ((.allowedEvents // []) | index("managed_access_quick_request_submitted") != null) and
    ((.allowedEvents // []) | index("managed_access_quick_request_received") != null) and
    ((.allowedEvents // []) | index("managed_access_quick_request_failed") != null) and
    ((.allowedEvents // []) | index("content_article_ollama_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_pricing_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_status_clicked") != null) and
    ((.allowedEvents // []) | index("content_article_launch_plan_clicked") != null) and
    ((.allowedEvents // []) | index("codex_docs_viewed") != null) and
    ((.allowedEvents // []) | index("codex_docs_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("quickstart_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("quickstart_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("quickstart_setup_next_clicked") != null) and
    ((.allowedEvents // []) | index("codex_docs_account_clicked") != null) and
    ((.allowedEvents // []) | index("codex_docs_snippet_copied") != null) and
    ((.allowedEvents // []) | index("codex_docs_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("api_reference_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("api_reference_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("api_troubleshooting_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("api_troubleshooting_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("launch_plan_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("launch_plan_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("launch_plan_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("landing_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("landing_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("landing_key_first_direct_clicked") != null) and
    ((.allowedEvents // []) | index("landing_activation_nudge_shown") != null) and
    ((.allowedEvents // []) | index("landing_activation_nudge_clicked") != null) and
    ((.allowedEvents // []) | index("landing_activation_nudge_dismissed") != null) and
    ((.allowedEvents // []) | index("landing_post_copy_prompt_shown") != null) and
    ((.allowedEvents // []) | index("landing_setup_next_clicked") != null) and
    ((.allowedEvents // []) | index("gateway_compare_migration_clicked") != null) and
    ((.allowedEvents // []) | index("gateway_compare_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("gateway_compare_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("gateway_compare_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("model_catalog_magic_link_sent") != null) and
    ((.allowedEvents // []) | index("model_catalog_oauth_clicked") != null) and
    ((.allowedEvents // []) | index("model_catalog_key_activation_clicked") != null) and
    ((.allowedEvents // []) | index("model_catalog_setup_next_clicked") != null) and
    ((.allowedEvents // []) | index("account_viewed") != null) and
    ((.allowedEvents // []) | index("account_setup_handoff_viewed") != null) and
    ((.allowedEvents // []) | index("account_auto_oauth_started") != null) and
    ((.allowedEvents // []) | index("account_oauth_failed") != null) and
    ((.allowedEvents // []) | index("account_login_failed") != null) and
    ((.allowedEvents // []) | index("account_signup_failed") != null) and
    ((.allowedEvents // []) | index("account_magic_link_failed") != null) and
    ((.allowedEvents // []) | index("login_key_recovery_shown") != null) and
    ((.allowedEvents // []) | index("login_key_recovery_clicked") != null) and
    ((.allowedEvents // []) | index("account_activation_nudge_shown") != null) and
    ((.allowedEvents // []) | index("account_activation_nudge_clicked") != null) and
    ((.allowedEvents // []) | index("account_activation_nudge_dismissed") != null) and
    ((.allowedEvents // []) | index("account_intent_primary_clicked") != null) and
    ((.allowedEvents // []) | index("account_preauth_setup_next_clicked") != null) and
    ((.allowedEvents // []) | index("account_api_key_create_failed") != null) and
    ((.allowedEvents // []) | index("account_checkout_unavailable") != null) and
    ((.allowedEvents // []) | index("account_email_verification_resent") != null) and
    ((.allowedEvents // []) | index("account_snippet_copied") != null) and
    ((.allowedEvents // []) | index("account_support_context_copied") != null)
  ' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  write_guard="$(jq -r '.writeGuard.browserOriginRequired == true' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  referer_fallback="$(jq -r '.writeGuard.refererFallbackAccepted == false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  preview_suffix="$(jq -r '.writeGuard.previewHostSuffix // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  smoke_events_persisted="$(jq -r '.dataQuality.smokeEventsPersisted == false' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$code" == "200" && "$ok" == "true" && "$service" == "sage-router-funnel-event" && "$primary_table" == "sage_router_funnel_events" && "$privacy_ok" == "true" && "$allowed_events" == "true" && "$write_guard" == "true" && "$referer_fallback" == "true" && "$preview_suffix" == ".sage-router-web.pages.dev" && "$smoke_events_persisted" == "true" ]]; then
    pass "privacy-safe marketing funnel event endpoint is configured with browser origin guard"
  else
    fail "marketing funnel event endpoint returned HTTP ${code} ok=${ok:-missing} service=${service:-missing} table=${primary_table:-missing} privacy=${privacy_ok:-missing} allowedEvents=${allowed_events:-missing} writeGuard=${write_guard:-missing} refererFallbackDisabled=${referer_fallback:-missing} previewSuffix=${preview_suffix:-missing} smokeEventsPersisted=${smoke_events_persisted:-missing}"
  fi
}

check_marketing_email_activation_helper() {
  local code
  code="$(http_code_follow "${MARKETING_BASE%/}/marketing-email-activation.js")"
  if [[ "$code" == "200" ]] && ! grep -q "insertSageRouterOauthButton" /tmp/sage-router-readiness-body; then
    code="200:missing-shared-oauth-helper"
  fi
  if [[ "$code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" /tmp/sage-router-readiness-body; then
    code="200:missing-github-pro-copy"
  fi
  if [[ "$code" == "200" ]] && ! grep -q "start=create_key" /tmp/sage-router-readiness-body; then
    code="200:missing-key-first-intent"
  fi
  if [[ "$code" == "200" ]] && ! grep -q "signInWithOAuth" /tmp/sage-router-readiness-body; then
    code="200:missing-github-oauth-login"
  fi
  if [[ "$code" == "200" ]] && ! grep -q "_oauth_clicked" /tmp/sage-router-readiness-body; then
    code="200:missing-oauth-clicked-funnel"
  fi
  if [[ "$code" == "200" ]] && ! grep -q "_oauth_failed" /tmp/sage-router-readiness-body; then
    code="200:missing-oauth-failed-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$code" == "200" ]]; then
    pass "shared marketing email activation helper exposes GitHub Pro OAuth activation"
  else
    fail "shared marketing email activation helper incomplete: helper=${code}"
  fi
}

check_marketing_homepage_activation() {
  local page_code bundle_path bundle_code homepage_body bundle_body
  homepage_body="$(mktemp)"
  bundle_body="$(mktemp)"
  page_code="$(http_code_follow "${MARKETING_BASE%/}/")"
  cp /tmp/sage-router-readiness-body "$homepage_body"
  bundle_path="$(grep -Eo 'src="/assets/[^"]+\.js"' "$homepage_body" | head -n1 | sed -E 's/^src="([^"]+)"$/\1/' || true)"
  if [[ "$page_code" == "200" && -n "$bundle_path" ]]; then
    bundle_code="$(http_code_follow "${MARKETING_BASE%/}${bundle_path}")"
    cp /tmp/sage-router-readiness-body "$bundle_body"
    if [[ "$bundle_code" != "200" ]]; then
      page_code="200:homepage-bundle-${bundle_code}"
    fi
  else
    : > "$bundle_body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Start API key activation" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-pro-activation-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://app.sagerouter.dev/account.html?plan=pro" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-pro-account-link"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=create_key" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-key-first-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_account_clicked" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-account-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_key_first_direct_clicked" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-direct-key-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-github-pro-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_oauth_clicked" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-landing-oauth-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_activation_nudge_shown" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-activation-nudge-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Ready to try the live edge" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-activation-nudge-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "hero-email-form" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-email-start-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_magic_link_sent" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-landing-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/v1/models" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-edge-verification-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copy hosted setup bundle" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-setup-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copy 60-second setup bundle" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-hero-setup-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing-full-setup-bundle" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-setup-copy-snippet"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing-hero-setup-bundle" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-hero-setup-copy-snippet"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Create API key next" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-post-copy-account-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Setup copied. Create your key now." "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-post-copy-panel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "landing_post_copy_prompt_shown" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-post-copy-prompt-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "stickyActivationBar" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-sticky-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Sticky create API key" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-sticky-account-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-setup-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Max implementation review" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-max-implementation-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "managed-access?intent=max-implementation" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-max-implementation-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Choose your route path" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-route-paths"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/cursor-ai-model-router" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-cursor-route-path"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/coding-agent-model-router" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-coding-agent-route-path"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/gemini-api-router" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-gemini-route-path"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "route-path-cursor" "$homepage_body" "$bundle_body"; then
    page_code="200:missing-homepage-route-path-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body "$homepage_body" "$bundle_body"

  if [[ "$page_code" == "200" ]]; then
    pass "marketing homepage exposes a measured Pro activation path"
  else
    fail "marketing homepage activation path incomplete: page=${page_code}"
  fi
}

check_marketing_comparison_page() {
  local page_code openrouter_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/compare/model-gateways")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router model gateway" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/compare/openrouter" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openrouter-comparison-link"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway-compare-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-compare-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway_compare_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-compare-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-compare-github-pro-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway_compare_oauth_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-compare-oauth-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway-copy-migration" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copy 60-second gateway setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-copy-first-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway-copy-next-account" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-post-copy-account-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway-compare-migration-bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-copy-snippet"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-copy-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  openrouter_code="$(http_code_follow "${MARKETING_BASE%/}/compare/openrouter")"
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "Sage Router vs OpenRouter" /tmp/sage-router-readiness-body; then
    openrouter_code="200:unexpected-openrouter-body"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "OpenRouter can be used as a BYOK-compatible provider route" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-byok-boundary"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "managed-access?intent=one-subscription" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-one-subscription-managed-access"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "not a public pooled-provider entitlement" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-one-subscription-boundary"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "gateway_compare_viewed" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-funnel-event"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "openrouter-email-form" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-openrouter-email-form"
  fi
  if [[ "$openrouter_code" == "200" ]] && ! grep -q "gateway_compare_magic_link_sent" /tmp/sage-router-readiness-body; then
    openrouter_code="200:missing-gateway-compare-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/compare/model-gateways" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-compare-url"
  fi
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/compare/openrouter" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-openrouter-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "OpenRouter comparison: ${MARKETING_BASE%/}/compare/openrouter" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-openrouter-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$openrouter_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing model gateway and OpenRouter comparison pages are live in sitemap and LLM discovery"
  else
    fail "marketing model gateway comparison incomplete: page=${page_code} openrouter=${openrouter_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_local_first_article_page() {
  local page_code dock_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/local-first-routing-for-ai-agents")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Local-first routing for AI agents" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_key_activation_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-article-key-activation-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=create_key" /tmp/sage-router-readiness-body; then
    page_code="200:missing-article-generated-key-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'id="article-copy-setup"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-article-setup-copy-button"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-article-setup-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local-first-hero-setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-article-setup-copy-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Hosted Sage Router monetizes routing convenience" /tmp/sage-router-readiness-body; then
    page_code="200:missing-commercial-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  dock_code="$(http_code_follow "${MARKETING_BASE%/}/article-activation-dock.js")"
  if [[ "$dock_code" == "200" ]] && ! grep -q "article-activation-email-form" /tmp/sage-router-readiness-body; then
    dock_code="200:missing-article-email-form"
  fi
  if [[ "$dock_code" == "200" ]] && ! grep -q "content_article_magic_link_sent" /tmp/sage-router-readiness-body; then
    dock_code="200:missing-article-magic-link-funnel"
  fi
  if [[ "$dock_code" == "200" ]] && ! grep -q "content_article_key_activation_clicked" /tmp/sage-router-readiness-body; then
    dock_code="200:missing-article-key-activation-funnel"
  fi
  if [[ "$dock_code" == "200" ]] && ! grep -q "upgradePlainAccountLinks" /tmp/sage-router-readiness-body; then
    dock_code="200:missing-article-account-link-upgrade"
  fi
  if [[ "$dock_code" == "200" ]] && ! grep -q "signInWithOtp" /tmp/sage-router-readiness-body; then
    dock_code="200:missing-article-magic-link-send"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/local-first-routing-for-ai-agents" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-local-first-article-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Local-first routing guide: ${MARKETING_BASE%/}/local-first-routing-for-ai-agents" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-local-first-article-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$dock_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing local-first routing article and shared article email activation are live in sitemap and LLM discovery"
  else
    fail "marketing local-first routing article incomplete: page=${page_code} dock=${dock_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_self_hosted_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/self-hosted-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Self-hosted AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multiple API keys" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multi-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "self-hosted-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-self-hosted-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-self-hosted-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "self-hosted-copy-local-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-self-hosted-copy-local-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-self-hosted-copy-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/self-hosted-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-self-hosted-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Self-hosted AI model router: ${MARKETING_BASE%/}/self-hosted-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-self-hosted-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing self-hosted AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing self-hosted AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_ollama_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/ollama-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Ollama AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Ollama Cloud" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-cloud-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local Ollama" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-ollama-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "multiple API keys" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multi-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "ollama-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "ollama-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/ollama-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-ollama-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Ollama AI model router: ${MARKETING_BASE%/}/ollama-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-ollama-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Ollama AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing Ollama AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_openai_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/openai-api-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI API router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Responses API compatible" /tmp/sage-router-readiness-body; then
    page_code="200:missing-responses-api-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI key load balancing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-key-load-balancing"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openai-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openai-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/openai-api-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-openai-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "OpenAI API router: ${MARKETING_BASE%/}/openai-api-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-openai-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing OpenAI API router page is live in sitemap and LLM discovery"
  else
    fail "marketing OpenAI API router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_azure_openai_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/azure-openai-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Azure OpenAI router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "AZURE_OPENAI_API_KEY" /tmp/sage-router-readiness-body; then
    page_code="200:missing-azure-api-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "AZURE_OPENAI_ENDPOINT" /tmp/sage-router-readiness-body; then
    page_code="200:missing-azure-endpoint-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Deployment routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-deployment-routing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Credential load balancing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-credential-load-balancing"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant Azure, OpenAI, or Microsoft subscription access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "azure-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-azure-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "azure-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-azure-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/azure-openai-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-azure-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Azure OpenAI router: ${MARKETING_BASE%/}/azure-openai-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-azure-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Azure OpenAI router page is live in sitemap and LLM discovery"
  else
    fail "marketing Azure OpenAI router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_anthropic_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/anthropic-api-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Anthropic API router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "ANTHROPIC_BASE_URL=https://api.sagerouter.dev" /tmp/sage-router-readiness-body; then
    page_code="200:missing-anthropic-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Claude Code" /tmp/sage-router-readiness-body; then
    page_code="200:missing-claude-code-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Dario-ready routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-dario-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "unauthorized Anthropic access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "anthropic-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-anthropic-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "anthropic-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-anthropic-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/anthropic-api-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-anthropic-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Anthropic API router: ${MARKETING_BASE%/}/anthropic-api-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-anthropic-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Anthropic API router page is live in sitemap and LLM discovery"
  else
    fail "marketing Anthropic API router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_aws_bedrock_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/aws-bedrock-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "AWS Bedrock router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "AWS_PROFILE" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aws-profile-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "AWS_REGION" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aws-region-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Bedrock model routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-bedrock-routing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Credential load balancing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-credential-load-balancing"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant AWS, Bedrock, Anthropic, Meta, or Amazon Nova access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "bedrock-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-bedrock-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "bedrock-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-bedrock-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/aws-bedrock-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-bedrock-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "AWS Bedrock router: ${MARKETING_BASE%/}/aws-bedrock-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-bedrock-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing AWS Bedrock router page is live in sitemap and LLM discovery"
  else
    fail "marketing AWS Bedrock router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_github_copilot_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/github-copilot-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "GitHub Copilot router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "GITHUB_COPILOT_TOKEN" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copilot-token-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized GitHub Copilot access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copilot-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copilot-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copilot-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copilot-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/github-copilot-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-copilot-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "GitHub Copilot router: ${MARKETING_BASE%/}/github-copilot-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-copilot-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing GitHub Copilot router page is live in sitemap and LLM discovery"
  else
    fail "marketing GitHub Copilot router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_codex_cli_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/codex-cli-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Codex CLI router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'wire_api = "responses"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-responses-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'base_url = "https://api.sagerouter.dev/v1/"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local port 8790" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-port-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Tailnet" /tmp/sage-router-readiness-body; then
    page_code="200:missing-tailnet-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal requests" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not implement its own" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-oauth-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex-cli-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex-cli-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/codex-cli-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-codex-cli-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Codex CLI router: ${MARKETING_BASE%/}/codex-cli-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-codex-cli-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Codex CLI router page is live in sitemap and LLM discovery"
  else
    fail "marketing Codex CLI router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_claude_code_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/claude-code-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Claude Code router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "ANTHROPIC_BASE_URL=https://api.sagerouter.dev" /tmp/sage-router-readiness-body; then
    page_code="200:missing-anthropic-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Dario-ready subscription paths" /tmp/sage-router-readiness-body; then
    page_code="200:missing-dario-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "unauthorized Claude, Anthropic, or Dario access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "claude-code-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-claude-code-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "claude-code-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-claude-code-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/claude-code-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-claude-code-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Claude Code router: ${MARKETING_BASE%/}/claude-code-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-claude-code-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Claude Code router page is live in sitemap and LLM discovery"
  else
    fail "marketing Claude Code router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_gemini_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/gemini-api-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Gemini API router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Google AI and Vertex AI" /tmp/sage-router-readiness-body; then
    page_code="200:missing-google-vertex-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Function-tool routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-function-tool-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "unauthorized Gemini or Google Cloud access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gemini-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gemini-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gemini-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gemini-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/gemini-api-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-gemini-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Gemini API router: ${MARKETING_BASE%/}/gemini-api-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-gemini-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Gemini API router page is live in sitemap and LLM discovery"
  else
    fail "marketing Gemini API router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_xai_grok_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/xai-grok-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "xAI Grok router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "XAI_API_KEY" /tmp/sage-router-readiness-body; then
    page_code="200:missing-xai-api-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not proxy xAI SSO sessions" /tmp/sage-router-readiness-body; then
    page_code="200:missing-sso-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "grok-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-grok-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "grok-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-grok-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/xai-grok-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-grok-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "xAI Grok router: ${MARKETING_BASE%/}/xai-grok-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-grok-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing xAI Grok router page is live in sitemap and LLM discovery"
  else
    fail "marketing xAI Grok router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_mistral_ai_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/mistral-ai-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Mistral AI router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "MISTRAL_API_KEY" /tmp/sage-router-readiness-body; then
    page_code="200:missing-mistral-api-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Codestral routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codestral-routing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Credential load balancing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-credential-load-balancing"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized Mistral, Codestral, or La Plateforme access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "mistral-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-mistral-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "mistral-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-mistral-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/mistral-ai-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-mistral-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Mistral AI router: ${MARKETING_BASE%/}/mistral-ai-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-mistral-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Mistral AI router page is live in sitemap and LLM discovery"
  else
    fail "marketing Mistral AI router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_groq_ai_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/groq-ai-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Groq AI router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "GROQ_API_KEY" /tmp/sage-router-readiness-body; then
    page_code="200:missing-groq-api-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Low-latency Llama routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-low-latency-routing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Credential load balancing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-credential-load-balancing"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal safeguards" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized GroqCloud, Llama, or Mixtral access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "groq-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-groq-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "groq-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-groq-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/groq-ai-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-groq-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Groq AI router: ${MARKETING_BASE%/}/groq-ai-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-groq-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Groq AI router page is live in sitemap and LLM discovery"
  else
    fail "marketing Groq AI router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_nvidia_nim_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/nvidia-nim-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "NVIDIA NIM router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "NVIDIA Cloud" /tmp/sage-router-readiness-body; then
    page_code="200:missing-nvidia-cloud-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "NVIDIA_API_KEY" /tmp/sage-router-readiness-body; then
    page_code="200:missing-nvidia-api-key-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not resell unauthorized NVIDIA access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "nvidia-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-nvidia-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "nvidia-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-nvidia-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/nvidia-nim-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-nvidia-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "NVIDIA NIM router: ${MARKETING_BASE%/}/nvidia-nim-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-nvidia-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing NVIDIA NIM router page is live in sitemap and LLM discovery"
  else
    fail "marketing NVIDIA NIM router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_coding_agent_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/coding-agent-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Coding agent model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Codex, Cursor, Aider, Continue, Claude Code, and OpenHands" /tmp/sage-router-readiness-body; then
    page_code="200:missing-coding-agent-targets"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'wire_api = "responses"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-responses-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "coding-agent-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-coding-agent-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "coding-agent-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-coding-agent-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/coding-agent-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-coding-agent-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Coding agent model router: ${MARKETING_BASE%/}/coding-agent-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-coding-agent-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing coding agent model router page is live in sitemap and LLM discovery"
  else
    fail "marketing coding agent model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_aider_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/aider-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Aider AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_API_BASE=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aider-openai-base"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "aider --model openai/auto" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aider-auto-model"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local port 8790" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-port-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Local Ollama fallback" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-fallback"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "multimodal" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "aider-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aider-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "aider-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-aider-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/aider-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-aider-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Aider AI model router: ${MARKETING_BASE%/}/aider-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-aider-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Aider AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing Aider AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_continue_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/continue-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q '"apiBase": "https://api.sagerouter.dev/v1"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-continue-api-base"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q '"model": "auto"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-continue-auto-model"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local port 8790" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-port-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Local Ollama fallback" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-fallback"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "multimodal" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "continue-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-continue-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "continue-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-continue-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/continue-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-continue-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Continue AI model router: ${MARKETING_BASE%/}/continue-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-continue-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Continue AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing Continue AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_openhands_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/openhands-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenHands AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openhands-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'model = "auto"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-openhands-auto-model"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "local port 8790" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-port-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Local Ollama fallback" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-fallback"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "multimodal" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openhands-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openhands-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openhands-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openhands-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/openhands-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-openhands-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "OpenHands AI model router: ${MARKETING_BASE%/}/openhands-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-openhands-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing OpenHands AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing OpenHands AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_openclaw_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/openclaw-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenClaw AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openclaw skill add sage-router --from clawhub" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openclaw-skill-setup"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=http://localhost:8790/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "ANTHROPIC_BASE_URL=http://localhost:8790" /tmp/sage-router-readiness-body; then
    page_code="200:missing-anthropic-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Codex OAuth passthrough" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-oauth-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "multimodal" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openclaw-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openclaw-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "openclaw-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openclaw-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/openclaw-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-openclaw-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "OpenClaw AI model router: ${MARKETING_BASE%/}/openclaw-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-openclaw-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing OpenClaw AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing OpenClaw AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_cursor_router_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/cursor-ai-model-router")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Cursor AI model router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Cursor custom OpenAI endpoint" /tmp/sage-router-readiness-body; then
    page_code="200:missing-cursor-openai-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Anthropic-compatible path" /tmp/sage-router-readiness-body; then
    page_code="200:missing-cursor-anthropic-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Multimodal routing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "cursor-router-copy-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-cursor-copy-start"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "cursor-router-start" /tmp/sage-router-readiness-body; then
    page_code="200:missing-cursor-snippet-id"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/cursor-ai-model-router" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-cursor-router-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Cursor AI model router: ${MARKETING_BASE%/}/cursor-ai-model-router" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-cursor-router-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Cursor AI model router page is live in sitemap and LLM discovery"
  else
    fail "marketing Cursor AI model router page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_reddit_evaluation_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/reddit-ai-gateway-evaluation")"
  if [[ "$page_code" == "200" ]] && ! grep -q "AI gateway evaluation kit" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Reddit evaluation kit" /tmp/sage-router-readiness-body; then
    page_code="200:missing-reddit-positioning"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenRouter BYOK boundary" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openrouter-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "429 failover" /tmp/sage-router-readiness-body; then
    page_code="200:missing-429-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reddit-copy-evaluation-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-evaluation-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reddit-copy-ollama-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-ollama-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_ollama_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-ollama-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reddit-copy-sideproject-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-sideproject-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_pricing_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-sideproject-pricing-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reddit-copy-setup-proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-setup-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_managed_access_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-managed-access-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "managed-access?intent=max-implementation" /tmp/sage-router-readiness-body; then
    page_code="200:missing-max-implementation-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/reddit-ai-gateway-evaluation" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-reddit-evaluation-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "AI gateway evaluation kit: ${MARKETING_BASE%/}/reddit-ai-gateway-evaluation" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-reddit-evaluation-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Reddit AI gateway evaluation page is live in sitemap and LLM discovery"
  else
    fail "marketing Reddit AI gateway evaluation page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_reliability_proof_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/reliability-proof")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Reliability Proof" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Reliability proof kit" /tmp/sage-router-readiness-body; then
    page_code="200:missing-proof-positioning"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable 429 failover proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-failover-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reliability-copy-failover-proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-failover-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable credential load balancing proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-balancing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reliability-copy-balancing-proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-balancing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable multimodal routing proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reliability-copy-multimodal-proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-multimodal-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Reddit proof reply" /tmp/sage-router-readiness-body; then
    page_code="200:missing-reddit-proof-reply"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "reliability-copy-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-reddit-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=reliability-proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-proof-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/reliability-proof" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-reliability-proof-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Reliability proof kit: ${MARKETING_BASE%/}/reliability-proof" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-reliability-proof-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing reliability proof kit is live in sitemap and LLM discovery"
  else
    fail "marketing reliability proof kit incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_community_launch_kit_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/community-launch-kit")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Community Launch Kit" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Show HN post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-show-hn-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-showhn-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-showhn-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Indie Hackers post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-indiehackers-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-indiehackers-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-indiehackers-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Dev.to post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-devto-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-devto-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-devto-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable X thread" /tmp/sage-router-readiness-body; then
    page_code="200:missing-x-thread-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-x-thread-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-x-thread-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable LinkedIn post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-linkedin-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-linkedin-post" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-linkedin-post"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=hackernews" /tmp/sage-router-readiness-body; then
    page_code="200:missing-hackernews-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=indiehackers" /tmp/sage-router-readiness-body; then
    page_code="200:missing-indiehackers-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=devto" /tmp/sage-router-readiness-body; then
    page_code="200:missing-devto-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=x" /tmp/sage-router-readiness-body; then
    page_code="200:missing-x-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=linkedin" /tmp/sage-router-readiness-body; then
    page_code="200:missing-linkedin-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-launch-kit-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-launch-kit-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/community-launch-kit" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-community-launch-kit-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Community launch kit: ${MARKETING_BASE%/}/community-launch-kit" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-community-launch-kit-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing community launch kit is live in sitemap and LLM discovery"
  else
    fail "marketing community launch kit incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_gateway_migration_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/docs/gateway-migration")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Migrate from an existing gateway to Sage Router" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://gateway.example/api/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-legacy-gateway-before"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-sage-router-after"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sk_sage_" /tmp/sage-router-readiness-body; then
    page_code="200:missing-generated-key-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router/frontier" /tmp/sage-router-readiness-body; then
    page_code="200:missing-frontier-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "does not grant unauthorized provider access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-provider-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "api-troubleshooting" /tmp/sage-router-readiness-body; then
    page_code="200:missing-troubleshooting-link"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway-migration-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "gateway_migration_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-migration-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/docs/gateway-migration" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-gateway-migration-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Gateway migration: ${MARKETING_BASE%/}/docs/gateway-migration" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-gateway-migration-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Gateway migration guide is live in sitemap and LLM discovery"
  else
    fail "marketing Gateway migration guide incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_pricing_page() {
  local page_code sitemap_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/pricing")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Hosted Pricing" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Start API key activation" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pro-activation-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://app.sagerouter.dev/account.html?plan=pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pro-account-link"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=checkout" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-saved-checkout-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=create_key" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-generated-key-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing_key_activation_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-key-activation-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing_checkout_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-checkout-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Key-first activation proof" /tmp/sage-router-readiness-body; then
    page_code="200:missing-key-first-pricing-proof"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Create the key before checkout" /tmp/sage-router-readiness-body; then
    page_code="200:missing-key-first-pricing-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Create API key first" /tmp/sage-router-readiness-body; then
    page_code="200:missing-key-first-pricing-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing-github-pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-github-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing_oauth_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-oauth-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-email-start-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "data-pricing-plan-email" /tmp/sage-router-readiness-body; then
    page_code="200:missing-plan-specific-email-start-forms"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sendPricingMagicLink" /tmp/sage-router-readiness-body; then
    page_code="200:missing-plan-specific-magic-link-handler"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing-copy-setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-setup-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copy 60-second setup bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-copy-first-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing-copy-next-account" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-post-copy-account-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "pricing-full-setup-bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-setup-copy-snippet"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-setup-copy-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/pricing" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-pricing-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" ]]; then
    pass "marketing hosted pricing page is live and in sitemap"
  else
    fail "marketing hosted pricing page incomplete: page=${page_code} sitemap=${sitemap_code}"
  fi
}

check_marketing_fusion_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/fusion")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Fusion" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router/fusion" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-model"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router:fusion" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-tool"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "fusion_plan_required" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-plan-gate"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "fusion_checkout_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "fusion-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "fusion_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-github-pro-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "fusion_oauth_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-fusion-oauth-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/fusion" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-fusion-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Fusion: ${MARKETING_BASE%/}/fusion" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-fusion-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Fusion premium page is live in sitemap and LLM discovery"
  else
    fail "marketing Fusion premium page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_founder_sales_kit_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/founder-sales-kit")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Founder Sales Kit" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Pro activation email" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pro-email-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-founder-pro-email" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-founder-pro-email"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable Max implementation DM" /tmp/sage-router-readiness-body; then
    page_code="200:missing-max-dm-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-founder-max-dm" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-founder-max-dm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable gateway migration reply" /tmp/sage-router-readiness-body; then
    page_code="200:missing-gateway-reply-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-founder-gateway-reply" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-founder-gateway-reply"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copyable calculator follow-up" /tmp/sage-router-readiness-body; then
    page_code="200:missing-calculator-followup-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "copy-founder-calculator-followup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-copy-founder-calculator-followup"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "utm_source=founder-sales" /tmp/sage-router-readiness-body; then
    page_code="200:missing-founder-sales-utm"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "outreach_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-founder-sales-copy-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "content_article_viewed" /tmp/sage-router-readiness-body; then
    page_code="200:missing-founder-sales-view-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/founder-sales-kit" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-founder-sales-kit-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Founder sales kit: ${MARKETING_BASE%/}/founder-sales-kit" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-founder-sales-kit-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing founder sales kit is live in sitemap and LLM discovery"
  else
    fail "marketing founder sales kit incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_launch_plan_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/launch-plan")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Launch Plan" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "The Sage Router path to \$10k MRR" /tmp/sage-router-readiness-body; then
    page_code="200:missing-10k-mrr-positioning"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "100 Lite, 200 Pro, and 50 Max customers produces \$10,200 MRR" /tmp/sage-router-readiness-body; then
    page_code="200:missing-plan-mix"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Managed provider access is a separate guarded beta path" /tmp/sage-router-readiness-body; then
    page_code="200:missing-managed-access-boundary"
  fi
  if [[ "$page_code" == "200" ]] &&
    { ! grep -q "/analytics/funnel" /tmp/sage-router-readiness-body ||
      ! grep -q "/edge/health" /tmp/sage-router-readiness-body ||
      ! grep -q "/admin/customers" /tmp/sage-router-readiness-body; }; then
    page_code="200:missing-operator-evidence"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "launch_plan_checkout_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "launch-plan-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-launch-plan-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-launch-plan-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "launch_plan_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-launch-plan-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/launch-plan" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-launch-plan-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Launch plan: ${MARKETING_BASE%/}/launch-plan" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-launch-plan-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing launch plan page is live in sitemap and LLM discovery"
  else
    fail "marketing launch plan page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_billing_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/billing")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Billing" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Stripe billing portal" /tmp/sage-router-readiness-body; then
    page_code="200:missing-stripe-portal"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "manual or crypto settlement" /tmp/sage-router-readiness-body; then
    page_code="200:missing-manual-crypto-settlement"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Payment recovery" /tmp/sage-router-readiness-body; then
    page_code="200:missing-payment-recovery"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sk_sage_" /tmp/sage-router-readiness-body; then
    page_code="200:missing-generated-key-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://app.sagerouter.dev/account.html" /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-account-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Do not send prompts" /tmp/sage-router-readiness-body; then
    page_code="200:missing-no-secrets-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/billing" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-billing-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Billing help: ${MARKETING_BASE%/}/billing" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-billing-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing billing help page is live in sitemap and LLM discovery"
  else
    fail "marketing billing help page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_managed_access_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/managed-access")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Managed Access Private Beta" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "interest.*managed-access" /tmp/sage-router-readiness-body; then
    page_code="200:missing-managed-access-interest"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/api/waitlist" /tmp/sage-router-readiness-body; then
    page_code="200:missing-waitlist-submit"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "managed-access-quick-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quick-review-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "managed_access_quick_request_received" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quick-review-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Do not submit prompts" /tmp/sage-router-readiness-body; then
    page_code="200:missing-no-secrets-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Target provider family" /tmp/sage-router-readiness-body; then
    page_code="200:missing-target-provider-family"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Commercial preference" /tmp/sage-router-readiness-body; then
    page_code="200:missing-commercial-preference"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "one-subscription" /tmp/sage-router-readiness-body; then
    page_code="200:missing-one-subscription-demand"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Ollama, OpenAI, and Anthropic" /tmp/sage-router-readiness-body; then
    page_code="200:missing-target-provider-copy"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/managed-access" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-managed-access-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Managed-access private beta: ${MARKETING_BASE%/}/managed-access" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-managed-access-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing managed-access private beta intake page is live in sitemap and LLM discovery"
  else
    fail "marketing managed-access private beta intake incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_model_catalog_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/models")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Model Catalog" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/v1/models" /tmp/sage-router-readiness-body; then
    page_code="200:missing-authenticated-model-api-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model-catalog-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model_catalog_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-github-pro-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model_catalog_oauth_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-oauth-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model-catalog-copy-setup" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-setup-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model-catalog-setup-bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-setup-copy-snippet"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "model_catalog_setup_next_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-setup-next-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Create API key next" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-setup-next-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-catalog-setup-copy-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/models" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-models-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Model catalog: ${MARKETING_BASE%/}/models" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-model-catalog-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing model catalog page is live in sitemap and LLM discovery"
  else
    fail "marketing model catalog page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_quickstart_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/quickstart")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router API Quickstart" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OPENAI_BASE_URL=https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sk_sage_" /tmp/sage-router-readiness-body; then
    page_code="200:missing-generated-key-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "/v1/models" /tmp/sage-router-readiness-body; then
    page_code="200:missing-model-api-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://app.sagerouter.dev/account.html?plan=pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pro-account-link"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=create_key" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-generated-key-intent"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_account_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-account-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "data-quickstart-plan=\"pro\"" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pro-plan-telemetry"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Continue with GitHub for Pro" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-github-pro-activation"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_oauth_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-oauth-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart-copy-bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-bundle-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Copy 60-second setup bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-copy-first-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart-copy-next-account" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-post-copy-account-cta"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart-full-setup-bundle" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-bundle-telemetry"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "quickstart_managed_access_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-managed-access-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "managed-access?intent=max-implementation" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quickstart-max-implementation-cta"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/quickstart" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-quickstart-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "API quickstart: ${MARKETING_BASE%/}/quickstart" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-quickstart-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing API quickstart is live in sitemap and LLM discovery"
  else
    fail "marketing API quickstart incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_api_troubleshooting_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/api-troubleshooting")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router API Troubleshooting" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Do not paste prompts" /tmp/sage-router-readiness-body; then
    page_code="200:missing-no-secrets-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "WWW-Authenticate" /tmp/sage-router-readiness-body; then
    page_code="200:missing-auth-header-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "X-RateLimit-" /tmp/sage-router-readiness-body; then
    page_code="200:missing-rate-limit-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "X-Quota-Remaining" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quota-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "accountUrl" /tmp/sage-router-readiness-body; then
    page_code="200:missing-onboarding-links"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sk_sage_" /tmp/sage-router-readiness-body; then
    page_code="200:missing-generated-key-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "api-troubleshooting-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-troubleshooting-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-troubleshooting-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "api_troubleshooting_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-troubleshooting-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/api-troubleshooting" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-api-troubleshooting-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "API troubleshooting: ${MARKETING_BASE%/}/api-troubleshooting" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-api-troubleshooting-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing API troubleshooting page is live in sitemap and LLM discovery"
  else
    fail "marketing API troubleshooting incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_api_reference_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/docs/api-reference")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Hosted API Reference" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "GET /v1/models" /tmp/sage-router-readiness-body; then
    page_code="200:missing-models-endpoint"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "POST /v1/chat/completions" /tmp/sage-router-readiness-body; then
    page_code="200:missing-chat-endpoint"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "POST /v1/responses" /tmp/sage-router-readiness-body; then
    page_code="200:missing-responses-endpoint"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "X-RateLimit-" /tmp/sage-router-readiness-body; then
    page_code="200:missing-rate-limit-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "X-Quota-Remaining" /tmp/sage-router-readiness-body; then
    page_code="200:missing-quota-guidance"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Anonymous .*/v1/.* model traffic is blocked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-authenticated-model-api-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "api-reference-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-reference-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-reference-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "api_reference_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-api-reference-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/docs/api-reference" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-api-reference-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Hosted API reference: ${MARKETING_BASE%/}/docs/api-reference" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-api-reference-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing hosted API reference is live in sitemap and LLM discovery"
  else
    fail "marketing hosted API reference incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_codex_docs_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/docs/codex")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Codex Setup" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'base_url = "https://api.sagerouter.dev/v1/"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'base_url = "http://127.0.0.1:8790/v1/"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-8790-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'wire_api = "responses"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-responses-wire-api"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router/frontier" /tmp/sage-router-readiness-body; then
    page_code="200:missing-frontier-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "data-copy-code=\"codex-hosted\"" /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-copy-button"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex_docs_snippet_copied" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-snippet-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex_docs_key_activation_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-key-activation-funnel-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex-docs-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "codex_docs_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-codex-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Do not paste prompts" /tmp/sage-router-readiness-body; then
    page_code="200:missing-no-secrets-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/docs/codex" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-codex-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Codex setup: ${MARKETING_BASE%/}/docs/codex" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-codex-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing Codex setup page is live in sitemap and LLM discovery"
  else
    fail "marketing Codex setup page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_agent_native_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/agent-native")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Agent-native model routing" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router/frontier" /tmp/sage-router-readiness-body; then
    page_code="200:missing-frontier-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'wire_api = "responses"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-responses-wire-api"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://api.sagerouter.dev/features/agent-native" /tmp/sage-router-readiness-body; then
    page_code="200:missing-feature-metadata"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "agent-native-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-agent-native-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-agent-native-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "agent_native_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-agent-native-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/agent-native" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-agent-native-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Agent-native routing: ${MARKETING_BASE%/}/agent-native" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-agent-native-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing agent-native routing page is live in sitemap and LLM discovery"
  else
    fail "marketing agent-native routing page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_marketing_integrations_page() {
  local page_code sitemap_code llms_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/integrations")"
  if [[ "$page_code" == "200" ]] && ! grep -q "Sage Router Integrations" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://api.sagerouter.dev/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-hosted-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "http://127.0.0.1:8790/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-local-8790-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "http://&lt;tailnet-host&gt;:8790/v1" /tmp/sage-router-readiness-body; then
    page_code="200:missing-tailnet-base-url"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "sage-router/frontier" /tmp/sage-router-readiness-body; then
    page_code="200:missing-frontier-profile"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "OpenAI-compatible" /tmp/sage-router-readiness-body; then
    page_code="200:missing-openai-compatible"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Cursor, Aider, Continue, Claude Code, and OpenHands" /tmp/sage-router-readiness-body; then
    page_code="200:missing-code-agent-list"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Do not paste prompts" /tmp/sage-router-readiness-body; then
    page_code="200:missing-no-secrets-boundary"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "integrations-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-integrations-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-integrations-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "integrations_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-integrations-magic-link-funnel"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/integrations" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-integrations-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  llms_code="$(http_code_follow "${MARKETING_BASE%/}/llms.txt")"
  if [[ "$llms_code" == "200" ]] && ! grep -q "Integrations: ${MARKETING_BASE%/}/integrations" /tmp/sage-router-readiness-body; then
    llms_code="200:missing-integrations-discovery"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" && "$llms_code" == "200" ]]; then
    pass "marketing integrations page is live in sitemap and LLM discovery"
  else
    fail "marketing integrations page incomplete: page=${page_code} sitemap=${sitemap_code} llms=${llms_code}"
  fi
}

check_model_routing_calculator() {
  local page_code sitemap_code
  page_code="$(http_code_follow "${MARKETING_BASE%/}/model-routing-calculator")"
  if [[ "$page_code" == "200" ]] && ! grep -q "AI Model Routing Calculator" /tmp/sage-router-readiness-body; then
    page_code="200:unexpected-body"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "Workflow text and prompt bodies stay in your browser." /tmp/sage-router-readiness-body; then
    page_code="200:missing-private-workflow-copy"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "calculator_key_activation_clicked" /tmp/sage-router-readiness-body; then
    page_code="200:missing-key-activation-event"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "start=create_key" /tmp/sage-router-readiness-body; then
    page_code="200:missing-key-first-calculator-handoff"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "calculator-email-form" /tmp/sage-router-readiness-body; then
    page_code="200:missing-calculator-email-form"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q 'data-oauth-activation="github"' /tmp/sage-router-readiness-body; then
    page_code="200:missing-calculator-github-oauth-opt-in"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "calculator_magic_link_sent" /tmp/sage-router-readiness-body; then
    page_code="200:missing-calculator-magic-link-funnel"
  fi
  if [[ "$page_code" == "200" ]] && ! grep -q "https://api.sagerouter.dev/pricing" /tmp/sage-router-readiness-body; then
    page_code="200:missing-pricing-metadata-fetch"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] && ! grep -q "${MARKETING_BASE%/}/model-routing-calculator" /tmp/sage-router-readiness-body; then
    sitemap_code="200:missing-calculator-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$page_code" == "200" && "$sitemap_code" == "200" ]]; then
    pass "marketing model routing calculator is live and in sitemap"
  else
    fail "marketing model routing calculator incomplete: page=${page_code} sitemap=${sitemap_code}"
  fi
}

check_legal_pages() {
  local security_code support_code terms_code privacy_code acceptable_code sitemap_code
  security_code="$(http_code_follow "${MARKETING_BASE%/}/security")"
  if [[ "$security_code" == "200" ]] && ! grep -q "Sage Router Security" /tmp/sage-router-readiness-body; then
    security_code="200:unexpected-body"
  fi
  if [[ "$security_code" == "200" ]] && ! grep -q "hosted public API edge" /tmp/sage-router-readiness-body; then
    security_code="200:missing-public-edge-boundary"
  fi
  if [[ "$security_code" == "200" ]] && ! grep -q "active generated" /tmp/sage-router-readiness-body; then
    security_code="200:missing-generated-key-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  support_code="$(http_code_follow "${MARKETING_BASE%/}/support")"
  if [[ "$support_code" == "200" ]] && ! grep -q "Sage Router Support" /tmp/sage-router-readiness-body; then
    support_code="200:unexpected-body"
  fi
  if [[ "$support_code" == "200" ]] && ! grep -q "Do Not Send Secrets" /tmp/sage-router-readiness-body; then
    support_code="200:missing-no-secrets-boundary"
  fi
  if [[ "$support_code" == "200" ]] && ! grep -q "Account and Billing" /tmp/sage-router-readiness-body; then
    support_code="200:missing-billing-support"
  fi
  if [[ "$support_code" == "200" ]] && ! grep -q "Reliability and 503s" /tmp/sage-router-readiness-body; then
    support_code="200:missing-reliability-support"
  fi
  rm -f /tmp/sage-router-readiness-body

  terms_code="$(http_code_follow "${MARKETING_BASE%/}/terms")"
  if [[ "$terms_code" == "200" ]] && ! grep -q "Sage Router Terms" /tmp/sage-router-readiness-body; then
    terms_code="200:unexpected-body"
  fi
  if [[ "$terms_code" == "200" ]] && ! grep -q "does not grant unauthorized" /tmp/sage-router-readiness-body; then
    terms_code="200:missing-service-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  privacy_code="$(http_code_follow "${MARKETING_BASE%/}/privacy")"
  if [[ "$privacy_code" == "200" ]] && ! grep -q "Sage Router Privacy" /tmp/sage-router-readiness-body; then
    privacy_code="200:unexpected-body"
  fi
  if [[ "$privacy_code" == "200" ]] && ! grep -q "prompt bodies" /tmp/sage-router-readiness-body; then
    privacy_code="200:missing-privacy-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  acceptable_code="$(http_code_follow "${MARKETING_BASE%/}/acceptable-use")"
  if [[ "$acceptable_code" == "200" ]] && ! grep -q "Sage Router Acceptable Use" /tmp/sage-router-readiness-body; then
    acceptable_code="200:unexpected-body"
  fi
  if [[ "$acceptable_code" == "200" ]] && ! grep -q "authorized to use" /tmp/sage-router-readiness-body; then
    acceptable_code="200:missing-authorized-use"
  fi
  if [[ "$acceptable_code" == "200" ]] && ! grep -q "Managed Provider Access" /tmp/sage-router-readiness-body; then
    acceptable_code="200:missing-managed-provider-access-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] &&
      { ! grep -q "${MARKETING_BASE%/}/security" /tmp/sage-router-readiness-body ||
        ! grep -q "${MARKETING_BASE%/}/support" /tmp/sage-router-readiness-body ||
        ! grep -q "${MARKETING_BASE%/}/terms" /tmp/sage-router-readiness-body ||
        ! grep -q "${MARKETING_BASE%/}/privacy" /tmp/sage-router-readiness-body ||
        ! grep -q "${MARKETING_BASE%/}/acceptable-use" /tmp/sage-router-readiness-body; }; then
    sitemap_code="200:missing-legal-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$security_code" == "200" && "$support_code" == "200" && "$terms_code" == "200" && "$privacy_code" == "200" && "$acceptable_code" == "200" && "$sitemap_code" == "200" ]]; then
    pass "marketing security, support, terms, privacy, and acceptable-use pages are live and in sitemap"
  else
    fail "marketing legal pages incomplete: security=${security_code} support=${support_code} terms=${terms_code} privacy=${privacy_code} acceptable-use=${acceptable_code} sitemap=${sitemap_code}"
  fi
}

check_managed_provider_prerequisite_pages() {
  local provider_code margin_code sitemap_code
  provider_code="$(http_code_follow "${MARKETING_BASE%/}/provider-resale-terms")"
  if [[ "$provider_code" == "200" ]] && ! grep -q "Sage Router Provider Resale Terms" /tmp/sage-router-readiness-body; then
    provider_code="200:unexpected-body"
  fi
  if [[ "$provider_code" == "200" ]] && ! grep -q "authorized to resell or operate" /tmp/sage-router-readiness-body; then
    provider_code="200:missing-authorized-resale-boundary"
  fi
  if [[ "$provider_code" == "200" ]] && ! grep -q "does not authorize pooled accounts" /tmp/sage-router-readiness-body; then
    provider_code="200:missing-pooled-account-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  margin_code="$(http_code_follow "${MARKETING_BASE%/}/margin-policy")"
  if [[ "$margin_code" == "200" ]] && ! grep -q "Sage Router Managed Access Margin Policy" /tmp/sage-router-readiness-body; then
    margin_code="200:unexpected-body"
  fi
  if [[ "$margin_code" == "200" ]] && ! grep -q "positive unit economics" /tmp/sage-router-readiness-body; then
    margin_code="200:missing-positive-unit-economics"
  fi
  if [[ "$margin_code" == "200" ]] && ! grep -q "not unlimited unmetered resale" /tmp/sage-router-readiness-body; then
    margin_code="200:missing-unmetered-resale-boundary"
  fi
  rm -f /tmp/sage-router-readiness-body

  sitemap_code="$(http_code_follow "${MARKETING_BASE%/}/sitemap.xml")"
  if [[ "$sitemap_code" == "200" ]] &&
      { ! grep -q "${MARKETING_BASE%/}/provider-resale-terms" /tmp/sage-router-readiness-body ||
        ! grep -q "${MARKETING_BASE%/}/margin-policy" /tmp/sage-router-readiness-body; }; then
    sitemap_code="200:missing-managed-provider-prerequisite-url"
  fi
  rm -f /tmp/sage-router-readiness-body

  if [[ "$provider_code" == "200" && "$margin_code" == "200" && "$sitemap_code" == "200" ]]; then
    pass "marketing provider resale terms and margin policy pages are live and in sitemap"
  else
    fail "marketing managed-provider prerequisite pages incomplete: provider-resale-terms=${provider_code} margin-policy=${margin_code} sitemap=${sitemap_code}"
  fi
}

check_admin_token() {
  if [[ -z "$ADMIN_TOKEN" ]]; then
    warn "SAGE_ROUTER_API_KEY/SAGE_ROUTER_EDGE_TOKEN not set; skipped private admin token probe"
    return
  fi
  local model_code model_error funnel_code funnel_ok customer_base customer_code customer_ok operator_token contact_export_code contact_export_ok
  model_code="$(http_code "${API_BASE%/}/v1/models" -H "Authorization: Bearer ${ADMIN_TOKEN}")"
  model_error="$(jq -r '.error // empty' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  funnel_code="$(http_code "${API_BASE%/}/analytics/funnel?days=30" -H "Authorization: Bearer ${ADMIN_TOKEN}")"
  funnel_ok="$(jq -r '
    ((.stages // {}) | has("signups")) and
    ((.stages // {}) | has("managedAccessBetaInterest")) and
    ((.waitlistInterest // {}) | has("managedAccess")) and
    ((.managedAccessDemand.targetProviderFamily // {}) | has("mixed-frontier") and has("ollama") and has("openai") and has("anthropic") and has("byok-compatible") and has("unknown")) and
    ((.managedAccessDemand.commercialPreference // {}) | has("one-subscription") and has("byok-plus-routing") and has("private-contract") and has("unknown")) and
    ((.managedAccessDemand.supportNeed // {}) | has("implementation-support") and has("private-deployment") and has("migration-help") and has("managed-provider-review") and has("unknown")) and
    ((.managedAccessDemand.targetLaunchWindow // {}) | has("this-week") and has("this-month") and has("this-quarter") and has("exploring") and has("unknown")) and
    ((.managedAccessDemand.intent // {}) | has("max-implementation") and has("private-deployment") and has("gateway-migration") and has("one-subscription") and has("ollama") and has("openai") and has("anthropic") and has("unknown")) and
    ((.rates // {}) | has("managedAccessShareOfWaitlist")) and
    ((.stages // {}) | has("setupSnippetCopies")) and
    ((.rates // {}) | has("setupCopyToFirstRequest")) and
    ((.targets // {}) | has("signupToGeneratedKey") and has("generatedKeyToFirstRequest") and has("setupCopyToFirstRequest") and has("signupToPaidConversion") and has("paidRecentUsage") and has("mrrTargetAttainment")) and
    ((.targets.signupToGeneratedKey // {}) | .targetRate == 0.6) and
    ((.targets.setupCopyToFirstRequest // {}) | .targetRate == 0.35) and
    ((.bottlenecks // []) | type == "array") and
    ((.conversionActions // []) | type == "array") and
    ((.conversionActions // []) | all(has("metric") and has("owner") and has("surface") and has("ctaPath") and has("action") and has("successMetric"))) and
    ((.acquisitionActions // []) | type == "array") and
    ((.authProviderState // {}) | has("total") and has("githubEnabled") and has("githubDisabled") and has("source") and has("githubAvailable") and has("recommendedRecoveryAuth") and has("operatorGuidance")) and
    ((.authProviderState.enabledProviders // {}) | has("github") and has("google") and has("discord") and has("none") and has("other")) and
    ((.authProviderState.disabledProviders // {}) | has("github") and has("google") and has("discord") and has("none") and has("other")) and
    ((.marketingIntent.authProviderState // {}) | has("total") and has("githubEnabled") and has("githubDisabled")) and
    ((.marketingIntent // {}) | has("setupSnippetCopies") and has("setupSnippetCopiesBySnippet")) and
    ((.marketingIntent.authProviderState.enabledProviders // {}) | has("github") and has("google") and has("discord") and has("none") and has("other")) and
    ((.marketingIntent.authProviderState.disabledProviders // {}) | has("github") and has("google") and has("discord") and has("none") and has("other")) and
    ((.privacy // {}) | .containsEmails == false) and
    ((.mrr // {}) | .targetMrrUsd == 10000) and
    ((.mrr // {}) | has("estimatedCurrentMrrUsd")) and
    ((.mrr.byPlan // {}) | has("lite") and has("pro") and has("max"))
  ' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  customer_base="$(discover_origin_base || true)"
  customer_base="${customer_base:-$API_BASE}"
  operator_token="$(resolve_operator_token)"
  customer_code="$(http_code "${customer_base%/}/admin/customers?limit=1" -H "Authorization: Bearer ${operator_token}")"
  customer_ok="$(jq -r '
    (.count | type == "number") and
    ((.customers // []) | type == "array") and
    ((.customers // []) | all(has("auditEvents") and has("latestAuditEvent"))) and
    ((.privacy // {}) | .containsRawApiKeys == false and .containsApiKeyHashes == false and .containsProviderCredentials == false and .containsPrompts == false and .operatorOnly == true) and
    ((tostring | contains("api_key_hash")) | not)
  ' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  contact_export_code="$(http_code "${API_BASE%/}/admin/customers?status=inactive&limit=20&contactExport=activation" -H "Authorization: Bearer ${ADMIN_TOKEN}")"
  contact_export_ok="$(jq -r '
    (.kind == "activation_contact_export") and
    (.count | type == "number") and
    ((.contacts // []) | type == "array") and
    ((.customers // []) | length == 0) and
    ((.csv // "") | type == "string") and
    ((.privacy // {}) | .operatorOnly == true and .explicitContactExport == true and .containsEmails == true and .containsCustomerIds == false and .containsRawApiKeys == false and .containsApiKeyHashes == false and .containsProviderCredentials == false and .containsPrompts == false and .containsRawProviderResponses == false) and
    ((tostring | contains("api_key_hash")) | not)
  ' /tmp/sage-router-readiness-body 2>/dev/null || true)"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$model_code" == "401" && "$model_error" == "unauthorized" && "$funnel_code" == "200" && "$funnel_ok" == "true" && "$customer_code" == "200" && "$customer_ok" == "true" && "$contact_export_code" == "200" && "$contact_export_ok" == "true" ]]; then
    pass "private admin token is rejected from generated-key model catalog while still reaching privacy-safe launch funnel, bounded customer review, and explicit activation contact export"
  else
    fail "private admin token probe failed: /v1/models=${model_code} error=${model_error:-missing} /analytics/funnel=${funnel_code} funnel=${funnel_ok:-missing} /admin/customers=${customer_code} customer=${customer_ok:-missing} /admin/customers?contactExport=activation=${contact_export_code} contactExport=${contact_export_ok:-missing}, expected catalog 401 unauthorized and admin surfaces 200/true"
  fi
}

discover_origin_base() {
  if [[ -n "$ORIGIN_BASE" ]]; then
    printf '%s\n' "$ORIGIN_BASE"
    return
  fi
  if [[ "$ORIGIN_AUTO_DISCOVER" == "0" || "$ORIGIN_AUTO_DISCOVER" == "false" || "$ORIGIN_AUTO_DISCOVER" == "no" ]]; then
    return
  fi
  if ! command -v gcloud >/dev/null 2>&1; then
    return
  fi
  gcloud run services describe "$CLOUD_RUN_SERVICE" \
    --project="$CLOUD_RUN_PROJECT" \
    --region="$CLOUD_RUN_REGION" \
    --format='value(status.url)' 2>/dev/null || true
}

check_origin_auth_gate() {
  local origin_base
  origin_base="$(discover_origin_base)"
  if [[ -z "$origin_base" ]]; then
    warn "SAGEROUTER_ORIGIN_BASE_URL not set and Cloud Run origin auto-discovery unavailable; skipped direct origin auth-gate probe"
    return
  fi
  local models_code setup_code admin_code
  models_code="$(http_code "${origin_base%/}/v1/models")"
  rm -f /tmp/sage-router-readiness-body
  setup_code="$(http_code "${origin_base%/}/setup/state")"
  rm -f /tmp/sage-router-readiness-body
  admin_code="$(http_code "${origin_base%/}/admin/blocks")"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$models_code" == "401" && "$setup_code" == "401" && "$admin_code" == "401" ]]; then
    pass "direct hosted origin blocks anonymous model, setup, and admin routes at ${origin_base%/}"
  else
    fail "direct hosted origin auth gate incomplete at ${origin_base%/}: /v1/models=${models_code} /setup/state=${setup_code} /admin/blocks=${admin_code}"
  fi
}

check_supabase_auth_config() {
  if [[ -z "$SUPABASE_ACCESS_TOKEN" ]]; then
    warn "SUPABASE_ACCESS_TOKEN not set; skipped Supabase auth config probe"
    return
  fi
  local config
  config="$(curl -fsS "https://api.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}/config/auth" \
    -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}")"
  local site signup_disabled email_enabled github app_redirect api_redirect
  site="$(printf '%s' "$config" | jq -r '.site_url // empty')"
  signup_disabled="$(printf '%s' "$config" | jq -r 'if has("disable_signup") then .disable_signup else true end')"
  email_enabled="$(printf '%s' "$config" | jq -r '.external_email_enabled // false')"
  github="$(printf '%s' "$config" | jq -r '.external_github_enabled // false')"
  app_redirect="$(printf '%s' "$config" | jq -r '((.uri_allow_list // "") | contains("https://app.sagerouter.dev/**"))')"
  api_redirect="$(printf '%s' "$config" | jq -r '((.uri_allow_list // "") | contains("https://api.sagerouter.dev/**"))')"

  [[ "$site" == "https://app.sagerouter.dev" ]] && pass "Supabase site_url is app.sagerouter.dev" || fail "Supabase site_url is ${site:-missing}"
  [[ "$signup_disabled" == "false" && "$email_enabled" == "true" ]] && pass "Supabase email signup is enabled" || fail "Supabase email signup disabled: disable_signup=${signup_disabled:-missing} external_email_enabled=${email_enabled:-missing}"
  [[ "$app_redirect" == "true" && "$api_redirect" == "true" ]] && pass "Supabase redirect allow-list includes app/api hosts" || fail "Supabase redirect allow-list missing app/api hosts"
  if [[ -n "$SUPABASE_PUBLIC_GITHUB_ENABLED" && "$SUPABASE_PUBLIC_GITHUB_ENABLED" != "$github" ]]; then
    fail "Supabase GitHub provider mismatch: management=${github} public=${SUPABASE_PUBLIC_GITHUB_ENABLED}"
  fi
  [[ "$github" == "true" ]] && pass "GitHub OAuth provider enabled" || fail "GitHub OAuth provider disabled; run bash scripts/check_github_supabase_auth_status.sh for the owner handoff"
}

check_quota_schema() {
  if [[ -z "$SUPABASE_SERVICE_ROLE_KEY" ]]; then
    warn "Supabase service role key not set; skipped quota, funnel-event, and operator-audit schema probe"
    return
  fi
  local table_code rpc_code funnel_table_code audit_table_code modalities_table_code modalities_rpc_code
  table_code="$(http_code "${SUPABASE_URL%/}/rest/v1/sage_router_usage_counters?select=id&limit=1" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}")"
  rm -f /tmp/sage-router-readiness-body
  funnel_table_code="$(http_code "${SUPABASE_URL%/}/rest/v1/sage_router_funnel_events?select=id&limit=1" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}")"
  rm -f /tmp/sage-router-readiness-body
  audit_table_code="$(http_code "${SUPABASE_URL%/}/rest/v1/sage_router_operator_audit_events?select=id&limit=1" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}")"
  rm -f /tmp/sage-router-readiness-body
  modalities_table_code="$(http_code "${SUPABASE_URL%/}/rest/v1/sage_router_model_modalities?select=key&limit=1" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}")"
  rm -f /tmp/sage-router-readiness-body
  rpc_code="$(http_code "${SUPABASE_URL%/}/rest/v1/rpc/sage_router_increment_usage" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Content-Type: application/json" \
    --data '{"p_customer_id":"readiness-probe","p_user_id":"readiness-probe","p_plan":"readiness","p_period":"2099-01","p_increment":1,"p_quota":1}')"
  rm -f /tmp/sage-router-readiness-body
  modalities_rpc_code="$(http_code "${SUPABASE_URL%/}/rest/v1/rpc/sage_router_record_model_modalities" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Content-Type: application/json" \
    --data '{"provider_name":"","model_name":"","modalities_in":[],"seen_at_epoch_ms":0}')"
  rm -f /tmp/sage-router-readiness-body
  if [[ "$table_code" == "200" && ( "$rpc_code" == "200" || "$rpc_code" == "409" ) ]]; then
    pass "Supabase quota table and RPC are installed"
  else
    warn "Supabase quota schema not ready: table HTTP ${table_code}, RPC HTTP ${rpc_code}; apply supabase/migrations/20260619021500_sage_router_usage_quotas.sql before enabling quotas"
  fi
  if [[ "$funnel_table_code" == "200" ]]; then
    pass "Supabase anonymous funnel event table is installed"
  else
    warn "Supabase funnel event schema not ready: table HTTP ${funnel_table_code}; apply supabase/migrations/20260619053000_sage_router_funnel_events.sql before relying on pre-signup conversion analytics"
  fi
  if [[ "$audit_table_code" == "200" ]]; then
    pass "Supabase operator audit table is installed"
  else
    warn "Supabase operator audit schema not ready: table HTTP ${audit_table_code}; apply supabase/migrations/20260620092000_operator_audit_events.sql before relying on durable operator audit events"
  fi
  if [[ "$modalities_table_code" == "200" && ( "$modalities_rpc_code" == "200" || "$modalities_rpc_code" == "204" ) ]]; then
    pass "Supabase model modality table and RPC are installed"
  else
    warn "Supabase model modality schema not ready: table HTTP ${modalities_table_code}, RPC HTTP ${modalities_rpc_code}; apply supabase/migrations/20260626003000_model_modalities.sql before relying on CDN-wide learned modalities"
  fi
}

require_jq
check_edge_health
check_public_edge_layer_headers
check_public_auth_gate
check_api_client_user_agent_gate
check_public_router_profile_contract
check_public_api_browser_boundary
check_browser_api_cors
check_account_mutation_origin_guard
check_static_security_headers "${APP_BASE%/}/login" "hosted app"
check_static_security_headers "${MARKETING_BASE%/}/pricing" "marketing"
check_public_pricing_metadata
check_public_model_catalog
check_managed_provider_access_guard
check_stripe_webhook_guard
check_hosted_onboarding_pages
check_marketing_account_redirects
check_public_supabase_auth_settings
check_waitlist_endpoint
check_funnel_event_endpoint
check_marketing_email_activation_helper
check_marketing_homepage_activation
check_marketing_comparison_page
check_marketing_gateway_migration_page
check_marketing_pricing_page
check_marketing_fusion_page
check_marketing_local_first_article_page
check_marketing_self_hosted_router_page
check_marketing_ollama_router_page
check_marketing_openai_router_page
check_marketing_azure_openai_router_page
check_marketing_anthropic_router_page
check_marketing_aws_bedrock_router_page
check_marketing_github_copilot_router_page
check_marketing_codex_cli_router_page
check_marketing_claude_code_router_page
check_marketing_gemini_router_page
check_marketing_xai_grok_router_page
check_marketing_mistral_ai_router_page
check_marketing_groq_ai_router_page
check_marketing_nvidia_nim_router_page
check_marketing_coding_agent_router_page
check_marketing_aider_router_page
check_marketing_continue_router_page
check_marketing_openhands_router_page
check_marketing_openclaw_router_page
check_marketing_cursor_router_page
check_marketing_reddit_evaluation_page
check_marketing_reliability_proof_page
check_marketing_community_launch_kit_page
check_marketing_founder_sales_kit_page
check_marketing_launch_plan_page
check_marketing_billing_page
check_marketing_managed_access_page
check_marketing_model_catalog_page
check_marketing_quickstart_page
check_marketing_api_troubleshooting_page
check_marketing_api_reference_page
check_marketing_codex_docs_page
check_marketing_agent_native_page
check_marketing_integrations_page
check_model_routing_calculator
check_legal_pages
check_managed_provider_prerequisite_pages
check_admin_token
check_origin_auth_gate
check_supabase_auth_config
check_quota_schema

if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi
