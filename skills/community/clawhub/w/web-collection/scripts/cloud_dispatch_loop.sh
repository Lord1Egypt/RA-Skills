#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  cloud_dispatch_loop.sh --payload <json> --base-url <url> --device-id <id> --token <token>

Options:
  --payload <json>          Full collect payload JSON
  --payload-file <path>     Read payload JSON from file
  --base-url <url>          Cloud API base URL, e.g. http://127.0.0.1:8016
  --device-id <id>          Target connector device_id
  --token <token>           User API key used as Bearer token
  --action <name>           default: collect
  --poll-sec <n>            default: 3
  --timeout-sec <n>         default: 1200
  -h, --help
USAGE
}

log() {
  printf '[web-collection] %s\n' "$*" >&2
}

die() {
  printf '[web-collection] error: %s\n' "$*" >&2
  exit 1
}

require_bin() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    die "missing required binary: $name"
  fi
}

urlencode() {
  node -e 'process.stdout.write(encodeURIComponent(process.argv[1] || ""));' "$1"
}

json_get_string() {
  local json="$1"
  local expr="$2"
  node -e "
const data = JSON.parse(process.argv[1]);
const value = (${expr});
if (value === undefined || value === null) process.exit(0);
if (typeof value === 'object') process.stdout.write(JSON.stringify(value));
else process.stdout.write(String(value));
" "$json"
}

api_get() {
  local path="$1"
  curl -fsS \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL$path"
}

api_get_optional() {
  local path="$1"
  local raw http_code body
  raw="$(curl -sS -w $'\n%{http_code}' \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL$path")"
  http_code="${raw##*$'\n'}"
  body="${raw%$'\n'*}"
  if [[ "$http_code" == 2* ]]; then
    printf '%s' "$body"
    return 0
  fi
  return 1
}

api_post_json() {
  local path="$1"
  local body="$2"
  curl -fsS -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d "$body" \
    "$BASE_URL$path"
}

extract_command_id() {
  local json="$1"
  node -e '
const data = JSON.parse(process.argv[1]);
const candidates = [
  data.commandId,
  data.command_id,
  data.id,
  data.data?.commandId,
  data.data?.command_id,
  data.data?.id,
  data.command?.commandId,
  data.command?.command_id,
  data.command?.id,
];
const first = candidates.find((value) => typeof value === "string" && value.trim());
if (first) process.stdout.write(first.trim());
' "$json"
}

find_command_state() {
  local json="$1"
  local command_id="$2"
  node -e '
const data = JSON.parse(process.argv[1]);
const commandId = process.argv[2];

const roots = [
  data,
  data.data,
  data.data?.commands,
  data.commands,
  data.items,
  data.list,
];

let entries = [];
for (const root of roots) {
  if (Array.isArray(root)) {
    entries = entries.concat(root);
  } else if (root && typeof root === "object") {
    entries.push(root);
  }
}
entries = entries.filter((entry) => entry && typeof entry === "object");

const match = entries.find((entry) => {
  const ids = [
    entry.commandId,
    entry.command_id,
    entry.id,
    entry.command?.commandId,
    entry.command?.command_id,
    entry.command?.id,
  ];
  return ids.some((value) => typeof value === "string" && value.trim() === commandId);
});

if (!match) {
  process.stdout.write(JSON.stringify({ found: false }));
  process.exit(0);
}

const status = [
  match.status,
  match.state,
  match.commandStatus,
  match.result?.status,
  match.command?.status,
].find((value) => typeof value === "string" && value.trim());

const taskId = [
  match.taskId,
  match.task_id,
  match.result?.taskId,
  match.payload?.taskId,
].find((value) => typeof value === "string" && value.trim()) || null;

const out = {
  found: true,
  status: status ? status.trim() : "",
  taskId,
  command: match,
};

process.stdout.write(JSON.stringify(out));
' "$json" "$command_id"
}

PAYLOAD_JSON=""
PAYLOAD_FILE=""
BASE_URL=""
DEVICE_ID=""
TOKEN=""
ACTION="collect"
POLL_SEC="3"
TIMEOUT_SEC="1200"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payload)
      PAYLOAD_JSON="${2:-}"
      shift 2
      ;;
    --payload-file)
      PAYLOAD_FILE="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --device-id)
      DEVICE_ID="${2:-}"
      shift 2
      ;;
    --token)
      TOKEN="${2:-}"
      shift 2
      ;;
    --action)
      ACTION="${2:-collect}"
      shift 2
      ;;
    --poll-sec)
      POLL_SEC="${2:-3}"
      shift 2
      ;;
    --timeout-sec)
      TIMEOUT_SEC="${2:-1200}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown arg: $1"
      ;;
  esac
done

require_bin curl
require_bin node

[[ -n "$PAYLOAD_JSON" || -n "$PAYLOAD_FILE" ]] || die "--payload or --payload-file is required"
[[ -n "$BASE_URL" ]] || die "--base-url is required"
[[ -n "$DEVICE_ID" ]] || die "--device-id is required"
[[ -n "$TOKEN" ]] || die "--token is required"

if [[ -n "$PAYLOAD_FILE" ]]; then
  [[ -f "$PAYLOAD_FILE" ]] || die "payload file not found: $PAYLOAD_FILE"
  PAYLOAD_JSON="$(cat "$PAYLOAD_FILE")"
fi

node -e 'JSON.parse(process.argv[1]);' "$PAYLOAD_JSON" >/dev/null

encoded_device_id="$(urlencode "$DEVICE_ID")"
status_json="$(api_get "/api/v1/connector/cloud/status?device_id=$encoded_device_id")"
online_hint="$(json_get_string "$status_json" 'data?.data?.online ?? data?.data?.connected ?? data?.online ?? data?.connected ?? data?.data?.status ?? data?.status ?? ""')"
if [[ -n "$online_hint" ]]; then
  log "cloud status=$online_hint device=$DEVICE_ID"
else
  log "cloud status fetched for device=$DEVICE_ID"
fi

dispatch_body="$(node -e '
const deviceId = process.argv[1];
const action = process.argv[2];
const payload = JSON.parse(process.argv[3]);
process.stdout.write(JSON.stringify({ device_id: deviceId, action, payload }));
' "$DEVICE_ID" "$ACTION" "$PAYLOAD_JSON")"

dispatch_json="$(api_post_json "/api/v1/connector/cloud/dispatch" "$dispatch_body")"
command_id="$(extract_command_id "$dispatch_json")"
[[ -n "$command_id" ]] || die "cloud dispatch succeeded but command id was missing in response"

log "cloud dispatch accepted commandId=$command_id device=$DEVICE_ID"

start_ts="$(date +%s)"
while :; do
  if command_detail_json="$(api_get_optional "/api/v1/connector/cloud/commands/$command_id")"; then
    command_state_json="$(find_command_state "$command_detail_json" "$command_id")"
  else
    commands_json="$(api_get "/api/v1/connector/cloud/commands?device_id=$encoded_device_id")"
    command_state_json="$(find_command_state "$commands_json" "$command_id")"
  fi

  found="$(json_get_string "$command_state_json" 'data?.found')"
  if [[ "$found" == "true" ]]; then
    status="$(json_get_string "$command_state_json" 'data?.status')"
    case "$status" in
      completed|success|succeeded)
        log "cloud command completed commandId=$command_id"
        json_get_string "$command_state_json" 'data?.command'
        printf '\n'
        exit 0
        ;;
      error|failed|failure|cancelled|canceled|stopped)
        json_get_string "$command_state_json" 'data?.command'
        printf '\n'
        die "cloud command finished with terminal status=$status commandId=$command_id"
        ;;
      "")
        log "cloud command found without explicit status yet commandId=$command_id"
        ;;
      *)
        log "cloud command status=$status commandId=$command_id"
        ;;
    esac
  else
    log "cloud command pending visibility commandId=$command_id"
  fi

  now_ts="$(date +%s)"
  if (( now_ts - start_ts >= TIMEOUT_SEC )); then
    die "timeout waiting cloud command completion after ${TIMEOUT_SEC}s"
  fi
  sleep "$POLL_SEC"
done
