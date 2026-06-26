#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  reexport_task.sh --task-id <id> --export-target <csv|bitable> [options]

Options:
  --task-id <id>                 Existing connector task id with cached records
  --export-target <csv|bitable>  Re-export target
  --base-url <url>               default: http://127.0.0.1:19820
  --deduplication <true|false>   default for bitable: true
  --deduplication-strategy <keepOld|keepNew> default: keepOld
  --table-name <text>            optional target table name
  --new-table                    derive a new target table name from the cached task
  --poll-sec <n>                 default: 3
  --timeout-sec <n>              default: 600
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
  command -v "$1" >/dev/null 2>&1 || die "missing required binary: $1"
}

normalize_bool() {
  local raw="${1:-}"
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    true|1|yes|y) echo "true" ;;
    false|0|no|n) echo "false" ;;
    *) die "invalid boolean value: $raw" ;;
  esac
}

normalize_strategy() {
  local raw="${1:-keepOld}"
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    keepold|old) echo "keepOld" ;;
    keepnew|new) echo "keepNew" ;;
    *) die "invalid deduplication strategy: $raw" ;;
  esac
}

json_get() {
  local json="$1"
  local expr="$2"
  node -e "const data=JSON.parse(process.argv[1]); const v=($expr); if (v===undefined||v===null) { process.stdout.write(''); } else if (typeof v === 'object') { process.stdout.write(JSON.stringify(v)); } else { process.stdout.write(String(v)); }" "$json"
}

resolve_admin_token() {
  if [[ -n "${WEB_COLLECTION_ADMIN_TOKEN:-}" ]]; then
    printf '%s' "$WEB_COLLECTION_ADMIN_TOKEN"
    return 0
  fi

  local token_file="${HOME}/.meixi-connector/bridge-admin-token.txt"
  if [[ -f "$token_file" ]]; then
    tr -d '\r\n' <"$token_file"
  fi
}

build_auth_args() {
  AUTH_ARGS=()
  ADMIN_TOKEN="$(resolve_admin_token || true)"
  if [[ -n "$ADMIN_TOKEN" ]]; then
    AUTH_ARGS=(-H "x-connector-admin-token: $ADMIN_TOKEN")
  fi
}

api_get() {
  local path="$1"
  curl -sS "${AUTH_ARGS[@]}" "$BASE_URL$path"
}

api_post_json() {
  local path="$1"
  local body="$2"
  curl -sS -X POST "${AUTH_ARGS[@]}" "$BASE_URL$path" -H 'Content-Type: application/json' -d "$body"
}

TASK_ID=""
EXPORT_TARGET=""
BASE_URL="${WEB_COLLECTION_BRIDGE_URL:-http://127.0.0.1:19820}"
DEDUPLICATION=""
DEDUPLICATION_STRATEGY="keepOld"
TABLE_NAME=""
NEW_TABLE="false"
POLL_SEC="3"
TIMEOUT_SEC="600"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id)
      TASK_ID="${2:-}"
      shift 2
      ;;
    --export-target)
      EXPORT_TARGET="${2:-}"
      shift 2
      ;;
    --base-url|--bridge-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --deduplication)
      DEDUPLICATION="${2:-}"
      shift 2
      ;;
    --deduplication-strategy)
      DEDUPLICATION_STRATEGY="${2:-}"
      shift 2
      ;;
    --table-name)
      TABLE_NAME="${2:-}"
      shift 2
      ;;
    --new-table)
      NEW_TABLE="true"
      shift 1
      ;;
    --poll-sec)
      POLL_SEC="${2:-3}"
      shift 2
      ;;
    --timeout-sec)
      TIMEOUT_SEC="${2:-600}"
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

[[ -n "$TASK_ID" ]] || die "--task-id is required"
case "$EXPORT_TARGET" in
  csv|bitable) ;;
  *) die "--export-target must be csv or bitable" ;;
esac

build_auth_args

if [[ "$NEW_TABLE" == "true" && "$EXPORT_TARGET" != "bitable" ]]; then
  die "--new-table can only be used with --export-target bitable"
fi

if [[ "$NEW_TABLE" == "true" && -z "$TABLE_NAME" ]]; then
  task_snapshot="$(api_get "/api/tasks/$TASK_ID")"
  TABLE_NAME="$(node -e '
const data = JSON.parse(process.argv[1]);
const base = [
  data.tableName,
  data.export?.tableName,
  data.method ? `${data.platform || "采集"}-${data.method}` : "",
  "采集结果",
].find((value) => typeof value === "string" && value.trim()) || "采集结果";
const now = new Date();
const pad = (n) => String(n).padStart(2, "0");
const suffix = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}`;
process.stdout.write(`${base.trim()}-${suffix}`);
' "$task_snapshot")"
fi

if [[ "$EXPORT_TARGET" == "csv" ]]; then
  EXPORT_MODE="csv"
else
  EXPORT_MODE="personal"
  [[ -n "$DEDUPLICATION" ]] || DEDUPLICATION="true"
fi

DEDUPLICATION_BOOL=""
if [[ -n "$DEDUPLICATION" ]]; then
  DEDUPLICATION_BOOL="$(normalize_bool "$DEDUPLICATION")"
fi
DEDUPLICATION_STRATEGY="$(normalize_strategy "$DEDUPLICATION_STRATEGY")"

body="$(node -e '
const target = process.argv[1];
const mode = process.argv[2];
const tableName = process.argv[3];
const dedupe = process.argv[4];
const strategy = process.argv[5];
const body = { exportMode: mode };
if (tableName) body.tableName = tableName;
if (target === "bitable") {
  body.deduplication = {
    enabled: dedupe === "" ? true : dedupe === "true",
    strategy: strategy || "keepOld",
  };
}
process.stdout.write(JSON.stringify(body));
' "$EXPORT_TARGET" "$EXPORT_MODE" "$TABLE_NAME" "$DEDUPLICATION_BOOL" "$DEDUPLICATION_STRATEGY")"

start_json="$(api_post_json "/api/tasks/$TASK_ID/export" "$body")"
ok="$(json_get "$start_json" 'data?.ok')"
if [[ "$ok" != "true" ]]; then
  printf '%s\n' "$start_json"
  die "re-export request failed"
fi

log "re-export accepted taskId=$TASK_ID target=$EXPORT_TARGET"

start_ts="$(date +%s)"
while :; do
  task_json="$(api_get "/api/tasks/$TASK_ID")"
  status="$(json_get "$task_json" 'data?.status')"
  export_status="$(json_get "$task_json" 'data?.export?.status')"

  case "$status:$export_status" in
    completed:completed|completed:)
      printf '%s\n' "$task_json"
      exit 0
      ;;
    error:error|error:*)
      printf '%s\n' "$task_json"
      die "re-export finished with error"
      ;;
    *)
      log "waiting re-export taskId=$TASK_ID status=$status export=$export_status"
      ;;
  esac

  now_ts="$(date +%s)"
  if (( now_ts - start_ts >= TIMEOUT_SEC )); then
    printf '%s\n' "$task_json"
    die "timeout waiting re-export completion after ${TIMEOUT_SEC}s"
  fi
  sleep "$POLL_SEC"
done
