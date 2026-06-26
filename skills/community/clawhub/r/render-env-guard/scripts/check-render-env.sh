#!/usr/bin/env bash
set -euo pipefail

API_BASE="${RENDER_API_BASE_URL:-https://api.render.com/v1}"
TOKEN="${RENDER_API_KEY:-}"
SERVICE_ID="${RENDER_SERVICE_ID:-}"
SERVICE_NAME="${RENDER_SERVICE_NAME:-}"
REQUIRED_KEYS="${REQUIRED_ENV_KEYS:-DATABASE_URL,DIRECT_URL,SHADOW_DATABASE_URL,NEXT_PUBLIC_APP_URL}"

if [[ -z "$TOKEN" ]]; then
  echo "FAIL: RENDER_API_KEY is required"
  exit 1
fi

if [[ -z "$SERVICE_ID" && -z "$SERVICE_NAME" ]]; then
  echo "FAIL: set RENDER_SERVICE_ID or RENDER_SERVICE_NAME"
  exit 1
fi

api_get() {
  local path="$1"
  curl -fsSL \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Accept: application/json" \
    "${API_BASE}${path}"
}

resolve_service_id() {
  if [[ -n "$SERVICE_ID" ]]; then
    echo "$SERVICE_ID"
    return
  fi

  local services_json
  services_json="$(api_get "/services")"

  local matches
  matches="$(python3 - "$SERVICE_NAME" <<'PY' <<<"$services_json"
import json, sys
name = sys.argv[1]
rows = json.load(sys.stdin)
for row in rows:
    svc = row.get("service") or {}
    if svc.get("name") == name and svc.get("id"):
        print(svc["id"])
PY
)"

  local count
  count="$(grep -c . <<<"$matches" || true)"

  if [[ "$count" -eq 0 ]]; then
    echo ""
    return
  fi
  if [[ "$count" -gt 1 ]]; then
    echo "FAIL: multiple services matched name '${SERVICE_NAME}'. Use RENDER_SERVICE_ID." >&2
    exit 1
  fi

  echo "$matches"
}

is_placeholder() {
  local v="$1"

  [[ -z "$v" ]] && return 0
  [[ "$v" =~ ^[[:space:]]+$ ]] && return 0
  [[ "$v" =~ \$\{[A-Za-z_][A-Za-z0-9_]*\} ]] && return 0
  [[ "$v" =~ \$[A-Za-z_][A-Za-z0-9_]* ]] && return 0
  [[ "$v" == *"changeme"* ]] && return 0
  [[ "$v" == *"example"* ]] && return 0
  [[ "$v" == *"template"* ]] && return 0
  [[ "$v" == *"your_"* ]] && return 0
  [[ "$v" == *"localhost"* ]] && return 0
  [[ "$v" == *"127.0.0.1"* ]] && return 0

  return 1
}

SERVICE_ID="$(resolve_service_id)"
if [[ -z "$SERVICE_ID" ]]; then
  echo "FAIL: could not resolve target service"
  exit 1
fi

echo "Render service: $SERVICE_ID"

env_json="$(api_get "/services/${SERVICE_ID}/env-vars")"

fail=0

IFS=',' read -r -a keys <<< "$REQUIRED_KEYS"
for raw_key in "${keys[@]}"; do
  key="$(xargs <<<"$raw_key")"
  [[ -z "$key" ]] && continue

  value="$(python3 - "$key" <<'PY' <<<"$env_json"
import json, sys
k = sys.argv[1]
rows = json.load(sys.stdin)
for row in rows:
    env = row.get("envVar") or {}
    if env.get("key") == k:
        print(env.get("value") or "")
        break
PY
)"

  if [[ -z "$value" ]]; then
    echo "FAIL: missing or empty ${key}"
    fail=1
    continue
  fi

  if is_placeholder "$value"; then
    echo "FAIL: ${key} looks like placeholder/template value"
    fail=1
    continue
  fi

  echo "PASS: ${key}"
done

if [[ "$fail" -ne 0 ]]; then
  echo "Result: FAIL"
  exit 1
fi

echo "Result: PASS"
