#!/usr/bin/env bash
set -euo pipefail

API_BASE="${RENDER_API_BASE_URL:-https://api.render.com/v1}"
TOKEN="${RENDER_API_KEY:-}"
SERVICE_ID="${RENDER_SERVICE_ID:-}"
SERVICE_NAME="${RENDER_SERVICE_NAME:-}"
REQUIRED_ENV_KEYS="${REQUIRED_ENV_KEYS:-}"
REQUIRED_ENV_FILES="${REQUIRED_ENV_FILES:-.env.example,.env.production}"
RENDER_ENV_VARS_JSON_PATH="${RENDER_ENV_VARS_JSON_PATH:-}"

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || {
    echo "FAIL: required binary not found: ${bin}" >&2
    exit 1
  }
}

require_bin python3
require_bin bash

if [[ -z "$RENDER_ENV_VARS_JSON_PATH" ]]; then
  require_bin curl
  if [[ -z "$TOKEN" ]]; then
    echo "FAIL: RENDER_API_KEY is required (or set RENDER_ENV_VARS_JSON_PATH for offline mode)"
    exit 1
  fi
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

  if [[ -z "$SERVICE_NAME" ]]; then
    echo ""
    return
  fi

  local services_json
  services_json="$(api_get "/services")"

  python3 - "$SERVICE_NAME" "$services_json" <<'PY'
import json, sys
name = sys.argv[1]
rows = json.loads(sys.argv[2])
matches = []
for row in rows:
    svc = row.get("service") or {}
    svc_name = (svc.get("name") or "").strip()
    if svc_name == name and svc.get("id"):
        matches.append(svc["id"])

if len(matches) == 1:
    print(matches[0])
elif len(matches) > 1:
    print("__MULTIPLE__")
PY
}

collect_required_keys() {
  if [[ -n "$REQUIRED_ENV_KEYS" ]]; then
    python3 - "$REQUIRED_ENV_KEYS" <<'PY'
import sys
raw = sys.argv[1]
seen = set()
for token in raw.split(","):
    key = token.strip()
    if not key:
        continue
    if key not in seen:
        seen.add(key)
        print(key)
PY
    return
  fi

  python3 - "$REQUIRED_ENV_FILES" <<'PY'
import os, re, sys
files = [f.strip() for f in sys.argv[1].split(",") if f.strip()]
pat = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=")
seen = set()
for path in files:
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = pat.match(line)
            if m:
                key = m.group(1)
                if key not in seen:
                    seen.add(key)
                    print(key)
PY
}

collect_remote_keys_from_json() {
  local json_input="$1"
  python3 - "$json_input" <<'PY'
import json, sys
rows = json.loads(sys.argv[1])
seen = set()
for row in rows:
    env = row.get("envVar") or {}
    key = (env.get("key") or "").strip()
    if key and key not in seen:
        seen.add(key)
        print(key)
PY
}

if [[ -n "$RENDER_ENV_VARS_JSON_PATH" ]]; then
  if [[ ! -f "$RENDER_ENV_VARS_JSON_PATH" ]]; then
    echo "FAIL: RENDER_ENV_VARS_JSON_PATH does not exist: $RENDER_ENV_VARS_JSON_PATH"
    exit 1
  fi
  SERVICE_LABEL="offline-json"
  env_json="$(cat "$RENDER_ENV_VARS_JSON_PATH")"
else
  SERVICE_ID="$(resolve_service_id)"
  if [[ "$SERVICE_ID" == "__MULTIPLE__" ]]; then
    echo "FAIL: multiple Render services matched name '${SERVICE_NAME}'. Use RENDER_SERVICE_ID."
    exit 1
  fi
  if [[ -z "$SERVICE_ID" ]]; then
    echo "FAIL: set RENDER_SERVICE_ID or RENDER_SERVICE_NAME"
    exit 1
  fi

  SERVICE_LABEL="$SERVICE_ID"
  env_json="$(api_get "/services/${SERVICE_ID}/env-vars")"
fi

required_keys="$(collect_required_keys || true)"
if [[ -z "$required_keys" ]]; then
  echo "FAIL: no required env keys found. Set REQUIRED_ENV_KEYS or provide REQUIRED_ENV_FILES with KEY=value lines."
  exit 1
fi

remote_keys="$(collect_remote_keys_from_json "$env_json" || true)"
if [[ -z "$remote_keys" ]]; then
  echo "WARN: no remote env keys found for service ${SERVICE_LABEL}"
fi

missing_keys="$(comm -23 <(printf '%s\n' "$required_keys" | sort -u) <(printf '%s\n' "$remote_keys" | sort -u) || true)"
extra_keys="$(comm -13 <(printf '%s\n' "$required_keys" | sort -u) <(printf '%s\n' "$remote_keys" | sort -u) || true)"

required_count="$(printf '%s\n' "$required_keys" | sed '/^$/d' | wc -l | tr -d ' ')"
remote_count="$(printf '%s\n' "$remote_keys" | sed '/^$/d' | wc -l | tr -d ' ')"

echo "Render service: ${SERVICE_LABEL}"
echo "Required keys: ${required_count}"
echo "Remote keys: ${remote_count}"

if [[ -n "$missing_keys" ]]; then
  echo ""
  echo "Missing on Render (required locally):"
  printf '  - %s\n' $missing_keys
else
  echo ""
  echo "Missing on Render: none"
fi

if [[ -n "$extra_keys" ]]; then
  echo ""
  echo "Extra on Render (not currently required locally):"
  printf '  - %s\n' $extra_keys
else
  echo ""
  echo "Extra on Render: none"
fi

if [[ -n "$missing_keys" ]]; then
  echo ""
  echo "Result: FAIL"
  exit 1
fi

echo ""
echo "Result: PASS"
