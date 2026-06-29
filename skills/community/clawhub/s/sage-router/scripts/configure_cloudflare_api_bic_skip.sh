#!/usr/bin/env bash
set -euo pipefail

load_local_env_file() {
  local path="$1"
  [[ -f "$path" ]] || return 0

  local key value current
  while IFS='=' read -r -d '' key value; do
    case "$key" in
      CLOUDFLARE_API_TOKEN|CLOUDFLARE_ZONE_ID|SAGEROUTER_CLOUDFLARE_ZONE_ID|SAGEROUTER_API_HOST)
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

usage() {
  cat <<'EOF'
Usage: scripts/configure_cloudflare_api_bic_skip.sh [--check|--audit-local-tokens]

Creates or verifies a host-scoped Cloudflare configuration rule that disables
Browser Integrity Check for api.sagerouter.dev only.

Options:
  --check               Verify token permissions and the existing rule without modifying Cloudflare.
  --audit-local-tokens  Test local Cloudflare token candidates by API status
                        without printing token values.
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 2
  fi
}

cloudflare_error_summary() {
  local body="$1"
  if jq -e '.errors? | length > 0' "$body" >/dev/null 2>&1; then
    jq -r '.errors[] | "- " + ((.code // "unknown")|tostring) + ": " + (.message // "unknown error")' "$body" >&2
  fi
}

api_get() {
  local url="$1"
  local label="${2:-Cloudflare API request}"
  local body status
  body="$(mktemp)"
  status="$(curl -sS -o "$body" -w '%{http_code}' "$url" -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}")"
  if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
    cat "$body"
    rm -f "$body"
    return 0
  fi
  printf '%s failed with HTTP %s.\n' "$label" "$status" >&2
  cloudflare_error_summary "$body"
  rm -f "$body"
  return 1
}

api_put_json() {
  local url="$1"
  local payload="$2"
  local body status
  body="$(mktemp)"
  status="$(curl -sS -o "$body" -w '%{http_code}' -X PUT "$url" \
    -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data-binary @"$payload")"
  if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
    cat "$body"
    rm -f "$body"
    return 0
  fi
  printf 'Cloudflare ruleset update failed with HTTP %s.\n' "$status" >&2
  printf 'The token must have Zone:Zone:Read and Zone Rulesets:Edit for %s.\n' "$ZONE_NAME" >&2
  cloudflare_error_summary "$body"
  rm -f "$body"
  return 1
}

api_get_ruleset_entrypoint() {
  local url="$1"
  local body status
  body="$(mktemp)"
  status="$(curl -sS -o "$body" -w '%{http_code}' "$url" -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}")"
  if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
    cat "$body"
    rm -f "$body"
    return 0
  fi
  if [[ "$status" == "404" ]]; then
    rm -f "$body"
    return 2
  fi
  printf 'Cloudflare %s ruleset lookup for %s failed with HTTP %s.\n' "$PHASE" "$ZONE_NAME" "$status" >&2
  printf 'The token must have Zone:Zone:Read and Zone Rulesets:Read/Edit for %s.\n' "$ZONE_NAME" >&2
  if [[ "$status" == "403" ]]; then
    printf 'If zone lookup succeeded before this step, the token can see the zone but is missing Zone Rulesets permissions. Rotate CLOUDFLARE_API_TOKEN to a token scoped to %s with Zone:Zone:Read plus Zone Rulesets:Read/Edit, then rerun this script.\n' "$ZONE_NAME" >&2
  fi
  cloudflare_error_summary "$body"
  rm -f "$body"
  return 1
}

load_local_env_file "${SAGEROUTER_SECRET_ENV_FILE:-/home/digit/.openclaw/.env}"

MODE="apply"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      MODE="check"
      shift
      ;;
    --audit-local-tokens)
      MODE="audit-local-tokens"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

require_cmd curl
require_cmd jq

if [[ "$MODE" == "audit-local-tokens" ]]; then
  require_cmd python3
  python3 - <<'PY'
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse

zone_name = os.environ.get('SAGEROUTER_CLOUDFLARE_ZONE_NAME') or 'sagerouter.dev'
audit_dir = Path(os.environ.get('SAGEROUTER_CLOUDFLARE_TOKEN_AUDIT_DIR') or '/home/digit/.openclaw')
audit_globs = [
    item.strip()
    for item in (os.environ.get('SAGEROUTER_CLOUDFLARE_TOKEN_AUDIT_GLOBS') or '.env*,gateway.systemd.env*').split(',')
    if item.strip()
]
token_keys = {
    'CLOUDFLARE_API_TOKEN',
    'CLOUDFLARE_SAGEROUTER_PAGES_KEY',
    'SAGEROUTER_CLOUDFLARE_API_TOKEN',
    'CF_API_TOKEN',
}


def parse_env_value(line):
    if '=' not in line:
        return None, None
    key, value = line.split('=', 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    return key, value


def cf_get(token, url):
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode('utf-8') or '{}')
            return resp.status, body
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode('utf-8', errors='replace')
        try:
            body = json.loads(raw or '{}')
        except Exception:
            body = {}
        return exc.code, body
    except Exception as exc:
        return 0, {'errors': [{'message': type(exc).__name__}]}


candidates = {}
if audit_dir.exists():
    for pattern in audit_globs:
        for path in sorted(audit_dir.glob(pattern)):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = parse_env_value(line)
                if key in token_keys and value:
                    candidates.setdefault(value, []).append(f'{path.name}:{key}')

print(json.dumps({
    'kind': 'cloudflare_token_candidate_audit',
    'zone': zone_name,
    'auditDir': str(audit_dir),
    'uniqueTokenCandidates': len(candidates),
    'printsTokenValues': False,
}))

zone_readable_candidates = 0
usable_ruleset_candidates = 0
for idx, (token, sources) in enumerate(candidates.items(), start=1):
    zone_status, zone_body = cf_get(
        token,
        'https://api.cloudflare.com/client/v4/zones?name=' + urllib.parse.quote(zone_name),
    )
    zone_id = ''
    if 200 <= int(zone_status or 0) < 300:
        rows = zone_body.get('result') or []
        if rows:
            zone_id = rows[0].get('id') or ''
    ruleset_status = 'skipped'
    ruleset_error = ''
    if zone_id:
        zone_readable_candidates += 1
        ruleset_status, ruleset_body = cf_get(
            token,
            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_config_settings/entrypoint',
        )
        ruleset_error = ','.join(
            str(err.get('code') or err.get('message') or '')
            for err in (ruleset_body.get('errors') or [])[:3]
        )
        if isinstance(ruleset_status, int) and 200 <= ruleset_status < 300:
            usable_ruleset_candidates += 1
    zone_error = ','.join(
        str(err.get('code') or err.get('message') or '')
        for err in (zone_body.get('errors') or [])[:3]
    )
    print(json.dumps({
        'candidate': idx,
        'sourceCount': len(sources),
        'sourceKinds': sorted({source.split(':', 1)[1] for source in sources}),
        'zoneStatus': zone_status,
        'zoneReadable': bool(zone_id),
        'zoneError': zone_error,
        'rulesetStatus': ruleset_status,
        'rulesetReadableOrExists': isinstance(ruleset_status, int) and 200 <= ruleset_status < 300,
        'rulesetError': ruleset_error,
    }))

print(json.dumps({
    'kind': 'cloudflare_token_candidate_audit_summary',
    'zone': zone_name,
    'uniqueTokenCandidates': len(candidates),
    'zoneReadableCandidates': zone_readable_candidates,
    'usableRulesetTokenCandidates': usable_ruleset_candidates,
    'printsTokenValues': False,
    'recommendedAction': (
        'use_candidate_with_rulesets_permissions'
        if usable_ruleset_candidates
        else 'rotate_CLOUDFLARE_API_TOKEN_with_Zone_Zone_Read_and_Zone_Rulesets_Read_Edit'
    ),
}))
PY
  exit 0
fi

CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:?Set CLOUDFLARE_API_TOKEN with Zone Rulesets read/edit permissions.}"
ZONE_NAME="${SAGEROUTER_CLOUDFLARE_ZONE_NAME:-sagerouter.dev}"
API_HOST="${SAGEROUTER_API_HOST:-api.sagerouter.dev}"
RULE_REF="${SAGEROUTER_CLOUDFLARE_API_BIC_RULE_REF:-sage-router-api-disable-bic}"
RULE_DESCRIPTION="${SAGEROUTER_CLOUDFLARE_API_BIC_RULE_DESCRIPTION:-Disable Browser Integrity Check for Sage Router API clients}"
PHASE="http_config_settings"

ZONE_ID="${SAGEROUTER_CLOUDFLARE_ZONE_ID:-${CLOUDFLARE_ZONE_ID:-}}"
if [[ -z "$ZONE_ID" ]]; then
  ZONE_ID="$(
    api_get "https://api.cloudflare.com/client/v4/zones?name=${ZONE_NAME}" "Cloudflare zone lookup for ${ZONE_NAME}" \
      | jq -r '.result[0].id // empty'
  )"
fi
if [[ -z "$ZONE_ID" ]]; then
  printf 'Could not resolve Cloudflare zone id for %s. The token must have Zone:Zone:Read for this zone, or set SAGEROUTER_CLOUDFLARE_ZONE_ID/CLOUDFLARE_ZONE_ID.\n' "$ZONE_NAME" >&2
  exit 2
fi

entrypoint_url="https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets/phases/${PHASE}/entrypoint"
current="$(mktemp)"
payload="$(mktemp)"
trap 'rm -f "$current" "$payload"' EXIT

set +e
api_get_ruleset_entrypoint "$entrypoint_url" >"$current"
entrypoint_status="$?"
set -e
if [[ "$entrypoint_status" == "2" ]]; then
  if [[ "$MODE" == "check" ]]; then
    printf 'Cloudflare %s ruleset entrypoint does not exist for %s; run this script without --check to create the host-scoped BIC skip rule.\n' "$PHASE" "$ZONE_NAME" >&2
    exit 1
  fi
  cat >"$current" <<'JSON'
{
  "success": true,
  "result": {
    "name": "default",
    "description": "Zone configuration rules",
    "kind": "zone",
    "phase": "http_config_settings",
    "rules": []
  }
}
JSON
elif [[ "$entrypoint_status" != "0" ]]; then
  exit "$entrypoint_status"
fi

if [[ "$MODE" == "check" ]]; then
  rule_ok="$(
    jq -r \
      --arg host "$API_HOST" \
      --arg ref "$RULE_REF" \
      --arg description "$RULE_DESCRIPTION" \
      '
      ((.result.rules // .rules // []) | any(
        ((.ref // "") == $ref or (.description // "") == $description) and
        (.enabled != false) and
        (.action == "set_config") and
        (.action_parameters.bic == false) and
        ((.expression // "") | contains($host))
      ))
      ' "$current"
  )"
  if [[ "$rule_ok" == "true" ]]; then
    printf 'Cloudflare Browser Integrity Check is disabled for %s by a host-scoped configuration rule.\n' "$API_HOST"
    exit 0
  fi
  printf 'Cloudflare Browser Integrity Check skip rule is missing or disabled for %s; run this script without --check to apply it.\n' "$API_HOST" >&2
  exit 1
fi

jq \
  --arg phase "$PHASE" \
  --arg host "$API_HOST" \
  --arg ref "$RULE_REF" \
  --arg description "$RULE_DESCRIPTION" \
  '
  def new_rule:
    {
      ref: $ref,
      description: $description,
      expression: "(http.host eq \"" + $host + "\")",
      action: "set_config",
      action_parameters: {bic: false},
      enabled: true
    };

  (.result // .) as $root
  | {
      name: ($root.name // "default"),
      description: ($root.description // "Zone configuration rules"),
      kind: ($root.kind // "zone"),
      phase: ($root.phase // $phase),
      rules: ((($root.rules // []) | map(select((.ref // "") != $ref and (.description // "") != $description))) + [new_rule])
    }
  ' "$current" >"$payload"

result="$(api_put_json "$entrypoint_url" "$payload")"
success="$(printf '%s' "$result" | jq -r '.success // false')"
if [[ "$success" != "true" ]]; then
  printf '%s\n' "$result" | jq >&2
  exit 1
fi

printf 'Configured Cloudflare Browser Integrity Check skip for %s in zone %s\n' "$API_HOST" "$ZONE_NAME"
