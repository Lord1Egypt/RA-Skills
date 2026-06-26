#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  collect_and_export_loop.sh [options]

Start one web-collection task via /api/collect, then poll /api/tasks/<taskId>
until completed/error. Handles TASK_RUNNING with stop -> wait idle -> retry.

Input options:
  --payload <json>               Full collect payload JSON (preferred)
  --payload-file <path>          Read full payload JSON from file

Build payload with flags (alternative to --payload/--payload-file):
  --platform <name>              e.g. douyin|tiktok|xiaohongshu (required)
  --method <name>                e.g. videoKeyword (required)
  --keyword <text>               repeatable
  --link <url>                   repeatable
  --max-items <n>
  --feature <text>
  --mode <text>
  --interval <n>
  --fetch-detail <true|false>
  --detail-speed <text>
  --detail-delay <n>
  --reply-level <n>
  --auto-export <true|false>
  --export-mode <text>
  --table-name <text>
  --fields-json <json-array>     e.g. '["title","author"]'
  --filters-json <json-object>   e.g. '{"minLikes":100}'

Runtime options:
  --base-url <url>               default: http://localhost:19820
  --poll-sec <n>                 default: 3
  --timeout-sec <n>              default: 1200
  --start-retries <n>            default: 3
  --idle-timeout-sec <n>         default: 180
  --ensure-bridge                auto-start bridge when /api/status is unreachable
  --bridge-cmd <command>         command used to start bridge (required with --ensure-bridge)
  --bridge-ready-timeout-sec <n> default: 30
  --bridge-log <path>            default: /tmp/web-collection-bridge.log
  --force-stop-before-start      call /api/stop before waiting idle
  -h, --help

Output:
  - Prints final task JSON to stdout on completion/error.
  - Logs progress to stderr.
USAGE
}

log() {
  printf '[web-collection] %s\n' "$*" >&2
}

die() {
  printf '[web-collection] error: %s\n' "$*" >&2
  exit 1
}

ADMIN_TOKEN=""
AUTH_ARGS=()

require_bin() {
  local b="$1"
  if ! command -v "$b" >/dev/null 2>&1; then
    die "missing required binary: $b"
  fi
}

is_int() {
  [[ "${1:-}" =~ ^[0-9]+$ ]]
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

json_get() {
  local json="$1"
  local expr="$2"
  node -e "const data=JSON.parse(process.argv[1]); const v=($expr); if (v===undefined||v===null) { process.stdout.write(''); } else if (typeof v === 'object') { process.stdout.write(JSON.stringify(v)); } else { process.stdout.write(String(v)); }" "$json"
}

json_validate() {
  local json="$1"
  node -e 'JSON.parse(process.argv[1]);' "$json" >/dev/null
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
    log "using connector admin token for local bridge requests"
  else
    log "local bridge admin token not found; requests will be sent without auth header"
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

api_post_empty() {
  local path="$1"
  curl -sS -X POST "${AUTH_ARGS[@]}" "$BASE_URL$path"
}

api_post_reset() {
  local reason="${1:-桥接状态已重置}"
  curl -sS -X POST "${AUTH_ARGS[@]}" "$BASE_URL/api/reset" -H 'Content-Type: application/json' \
    -d "{\"reason\":\"$reason\"}"
}

fetch_status_safe() {
  curl -fsS --max-time 2 "${AUTH_ARGS[@]}" "$BASE_URL/api/status"
}

ensure_bridge() {
  local start now status

  if status="$(fetch_status_safe)"; then
    log "bridge reachable"
    return 0
  fi

  if [[ "$ENSURE_BRIDGE" != "true" ]]; then
    die "bridge not reachable at $BASE_URL (use --ensure-bridge + --bridge-cmd)"
  fi

  if [[ -z "$BRIDGE_CMD" ]]; then
    die "--bridge-cmd is required when --ensure-bridge is enabled"
  fi

  log "bridge unreachable, starting bridge command"
  nohup bash -lc "$BRIDGE_CMD" >"$BRIDGE_LOG" 2>&1 &
  BRIDGE_PID=$!
  log "bridge start pid=$BRIDGE_PID log=$BRIDGE_LOG"

  start="$(date +%s)"
  while :; do
    if status="$(fetch_status_safe)"; then
      log "bridge ready"
      return 0
    fi

    now="$(date +%s)"
    if (( now - start >= BRIDGE_READY_TIMEOUT_SEC )); then
      if [[ -f "$BRIDGE_LOG" ]]; then
        log "bridge log tail:"
        tail -n 40 "$BRIDGE_LOG" >&2 || true
      fi
      die "timeout waiting bridge ready after ${BRIDGE_READY_TIMEOUT_SEC}s"
    fi
    sleep 1
  done
}

extract_running() {
  local status_json="$1"
  json_get "$status_json" 'data?.tasks?.running ?? data?.runningTasks ?? 0'
}

extract_exporting() {
  local status_json="$1"
  json_get "$status_json" 'data?.tasks?.exporting ?? data?.exportingTasks ?? 0'
}

wait_idle() {
  local start now status connected running exporting saw_disconnected reset_attempted
  start="$(date +%s)"
  saw_disconnected="false"
  reset_attempted="false"

  while :; do
    if ! status="$(fetch_status_safe)"; then
      die "bridge became unreachable at $BASE_URL during wait_idle"
    fi

    connected="$(json_get "$status" 'data?.pluginConnected')"
    if [[ "$connected" != "true" ]]; then
      if [[ "$saw_disconnected" != "true" ]]; then
        log "pluginConnected=false, waiting for extension websocket connection"
        saw_disconnected="true"
      fi
      now="$(date +%s)"
      if (( now - start >= IDLE_TIMEOUT_SEC )); then
        die "timeout waiting pluginConnected=true"
      fi
      sleep 1
      continue
    fi

    running="$(extract_running "$status")"
    exporting="$(extract_exporting "$status")"

    if [[ "$running" == "0" && "$exporting" == "0" ]]; then
      return 0
    fi

    now="$(date +%s)"
    if (( now - start >= IDLE_TIMEOUT_SEC )); then
      if [[ "$reset_attempted" != "true" ]]; then
        log "idle timeout reached, attempting bridge reset"
        api_post_reset "wait_idle timeout: running=$running exporting=$exporting" >/dev/null || true
        reset_attempted="true"
        start="$(date +%s)"
        sleep 1
        continue
      fi
      die "timeout waiting idle (running=$running exporting=$exporting)"
    fi

    sleep 1
  done
}

build_payload_from_flags() {
  PAYLOAD_JSON="$(node -e '
const out = {};
const pushJSON = (v, fallback) => {
  if (!v) return fallback;
  try { return JSON.parse(v); } catch { process.stderr.write("invalid json input\n"); process.exit(2); }
};

const keywords = pushJSON(process.env.KEYWORDS_JSON, []);
const links = pushJSON(process.env.LINKS_JSON, []);
const fields = process.env.FIELDS_JSON ? pushJSON(process.env.FIELDS_JSON, null) : null;
const filters = process.env.FILTERS_JSON ? pushJSON(process.env.FILTERS_JSON, null) : null;

const set = (k, v) => {
  if (v === "" || v === undefined || v === null) return;
  out[k] = v;
};

set("platform", process.env.PLATFORM);
set("method", process.env.METHOD);
if (Array.isArray(keywords) && keywords.length > 0) out.keywords = keywords;
if (Array.isArray(links) && links.length > 0) out.links = links;
set("maxItems", process.env.MAX_ITEMS ? Number(process.env.MAX_ITEMS) : "");
set("feature", process.env.FEATURE);
set("mode", process.env.MODE);
set("interval", process.env.INTERVAL_VAL ? Number(process.env.INTERVAL_VAL) : "");
set("fetchDetail", process.env.FETCH_DETAIL === "" ? "" : process.env.FETCH_DETAIL === "true");
set("detailSpeed", process.env.DETAIL_SPEED);
set("detailDelay", process.env.DETAIL_DELAY ? Number(process.env.DETAIL_DELAY) : "");
set("replyLevel", process.env.REPLY_LEVEL ? Number(process.env.REPLY_LEVEL) : "");
set("autoExport", process.env.AUTO_EXPORT === "" ? "" : process.env.AUTO_EXPORT === "true");
set("exportMode", process.env.EXPORT_MODE);
set("tableName", process.env.TABLE_NAME);
if (fields !== null) out.fields = fields;
if (filters !== null) out.filters = filters;

process.stdout.write(JSON.stringify(out));
')"
}

collect_and_wait() {
  local attempts resp code task_id started_at now task status

  attempts=1
  task_id=""

  while (( attempts <= START_RETRIES )); do
    log "start collect attempt=$attempts"
    resp="$(api_post_json '/api/collect' "$PAYLOAD_JSON")"

    code="$(json_get "$resp" 'data?.code ?? ""')"
    if [[ "$code" == "TASK_RUNNING" ]]; then
      log "TASK_RUNNING returned, stopping current task then waiting idle"
      api_post_empty '/api/stop' >/dev/null || true
      wait_idle
      ((attempts++))
      continue
    fi

    task_id="$(json_get "$resp" 'data?.taskId ?? ""')"
    if [[ -z "$task_id" ]]; then
      die "collect response missing taskId: $resp"
    fi

    break
  done

  if [[ -z "$task_id" ]]; then
    die "failed to start task after $START_RETRIES retries"
  fi

  log "task started: $task_id"

  started_at="$(date +%s)"
  while :; do
    task="$(api_get "/api/tasks/$task_id")"
    status="$(json_get "$task" 'data?.status ?? ""')"

    case "$status" in
      running|exporting)
        ;;
      completed)
        if [[ "$EXPECT_BITABLE_EXPORT" == "true" ]]; then
          local export_status table_url
          export_status="$(json_get "$task" 'data?.export?.status ?? ""')"
          table_url="$(json_get "$task" 'data?.export?.tableUrl ?? ""')"
          if [[ "$export_status" != "completed" || -z "$table_url" ]]; then
            die "task completed but export not completed: $task"
          fi
        fi
        printf '%s\n' "$task"
        return 0
        ;;
      error)
        printf '%s\n' "$task"
        return 1
        ;;
      *)
        log "task status=$status"
        ;;
    esac

    now="$(date +%s)"
    if (( now - started_at >= TIMEOUT_SEC )); then
      if [[ "$status" == "exporting" ]]; then
        local export_status export_error record_count
        export_status="$(json_get "$task" 'data?.export?.status ?? ""')"
        export_error="$(json_get "$task" 'data?.export?.error ?? data?.error ?? ""')"
        record_count="$(json_get "$task" 'data?.export?.recordCount ?? data?.count ?? 0')"
        die "timeout waiting export result for task=$task_id (status=$status export.status=$export_status recordCount=$record_count error=${export_error:-none})"
      fi
      die "timeout waiting task=$task_id (last status=$status)"
    fi

    sleep "$POLL_SEC"
  done
}

# defaults
BASE_URL="http://127.0.0.1:19820"
POLL_SEC=3
TIMEOUT_SEC=1200
START_RETRIES=3
IDLE_TIMEOUT_SEC=180
ENSURE_BRIDGE="false"
BRIDGE_CMD=""
BRIDGE_READY_TIMEOUT_SEC=30
BRIDGE_LOG="/tmp/web-collection-bridge.log"
FORCE_STOP_BEFORE_START="false"
PAYLOAD_JSON=""
PAYLOAD_FILE=""

# payload flags
PLATFORM=""
METHOD=""
KEYWORDS=()
LINKS=()
MAX_ITEMS=""
FEATURE=""
MODE=""
INTERVAL_VAL=""
FETCH_DETAIL=""
DETAIL_SPEED=""
DETAIL_DELAY=""
REPLY_LEVEL=""
AUTO_EXPORT=""
EXPORT_MODE=""
TABLE_NAME=""
FIELDS_JSON=""
FILTERS_JSON=""

if [[ $# -eq 0 ]]; then
  usage
  exit 2
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payload) PAYLOAD_JSON="${2:-}"; shift 2 ;;
    --payload-file) PAYLOAD_FILE="${2:-}"; shift 2 ;;

    --platform) PLATFORM="${2:-}"; shift 2 ;;
    --method) METHOD="${2:-}"; shift 2 ;;
    --keyword) KEYWORDS+=("${2:-}"); shift 2 ;;
    --link) LINKS+=("${2:-}"); shift 2 ;;
    --max-items) MAX_ITEMS="${2:-}"; shift 2 ;;
    --feature) FEATURE="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    --interval) INTERVAL_VAL="${2:-}"; shift 2 ;;
    --fetch-detail) FETCH_DETAIL="$(normalize_bool "${2:-}")"; shift 2 ;;
    --detail-speed) DETAIL_SPEED="${2:-}"; shift 2 ;;
    --detail-delay) DETAIL_DELAY="${2:-}"; shift 2 ;;
    --reply-level) REPLY_LEVEL="${2:-}"; shift 2 ;;
    --auto-export) AUTO_EXPORT="$(normalize_bool "${2:-}")"; shift 2 ;;
    --export-mode) EXPORT_MODE="${2:-}"; shift 2 ;;
    --table-name) TABLE_NAME="${2:-}"; shift 2 ;;
    --fields-json) FIELDS_JSON="${2:-}"; shift 2 ;;
    --filters-json) FILTERS_JSON="${2:-}"; shift 2 ;;

    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    --poll-sec) POLL_SEC="${2:-}"; shift 2 ;;
    --timeout-sec) TIMEOUT_SEC="${2:-}"; shift 2 ;;
    --start-retries) START_RETRIES="${2:-}"; shift 2 ;;
    --idle-timeout-sec) IDLE_TIMEOUT_SEC="${2:-}"; shift 2 ;;
    --ensure-bridge) ENSURE_BRIDGE="true"; shift 1 ;;
    --bridge-cmd) BRIDGE_CMD="${2:-}"; shift 2 ;;
    --bridge-ready-timeout-sec) BRIDGE_READY_TIMEOUT_SEC="${2:-}"; shift 2 ;;
    --bridge-log) BRIDGE_LOG="${2:-}"; shift 2 ;;
    --force-stop-before-start) FORCE_STOP_BEFORE_START="true"; shift 1 ;;

    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

require_bin curl
require_bin node
build_auth_args

if ! is_int "$POLL_SEC"; then die "--poll-sec must be integer"; fi
if ! is_int "$TIMEOUT_SEC"; then die "--timeout-sec must be integer"; fi
if ! is_int "$START_RETRIES"; then die "--start-retries must be integer"; fi
if ! is_int "$IDLE_TIMEOUT_SEC"; then die "--idle-timeout-sec must be integer"; fi
if ! is_int "$BRIDGE_READY_TIMEOUT_SEC"; then die "--bridge-ready-timeout-sec must be integer"; fi
if [[ -n "$MAX_ITEMS" ]] && ! is_int "$MAX_ITEMS"; then die "--max-items must be integer"; fi
if [[ -n "$INTERVAL_VAL" ]] && ! is_int "$INTERVAL_VAL"; then die "--interval must be integer"; fi
if [[ -n "$DETAIL_DELAY" ]] && ! is_int "$DETAIL_DELAY"; then die "--detail-delay must be integer"; fi
if [[ -n "$REPLY_LEVEL" ]] && ! is_int "$REPLY_LEVEL"; then die "--reply-level must be integer"; fi

if [[ -n "$PAYLOAD_JSON" && -n "$PAYLOAD_FILE" ]]; then
  die "use only one of --payload or --payload-file"
fi

if [[ -n "$PAYLOAD_FILE" ]]; then
  if [[ ! -f "$PAYLOAD_FILE" ]]; then
    die "payload file not found: $PAYLOAD_FILE"
  fi
  PAYLOAD_JSON="$(cat "$PAYLOAD_FILE")"
fi

if [[ -z "$PAYLOAD_JSON" ]]; then
  if [[ -z "$PLATFORM" || -z "$METHOD" ]]; then
    die "--platform and --method are required when payload is not provided"
  fi

  if [[ -n "$FIELDS_JSON" ]]; then
    json_validate "$FIELDS_JSON" || die "invalid --fields-json"
  fi
  if [[ -n "$FILTERS_JSON" ]]; then
    json_validate "$FILTERS_JSON" || die "invalid --filters-json"
  fi

  KEYWORDS_JSON="[]"
  if (( ${#KEYWORDS[@]} > 0 )); then
    KEYWORDS_JSON="$(printf '%s\n' "${KEYWORDS[@]}" | node -e 'const fs=require("fs");const arr=fs.readFileSync(0,"utf8").split(/\n/).filter(Boolean);process.stdout.write(JSON.stringify(arr));')"
  fi

  LINKS_JSON="[]"
  if (( ${#LINKS[@]} > 0 )); then
    LINKS_JSON="$(printf '%s\n' "${LINKS[@]}" | node -e 'const fs=require("fs");const arr=fs.readFileSync(0,"utf8").split(/\n/).filter(Boolean);process.stdout.write(JSON.stringify(arr));')"
  fi

  export PLATFORM METHOD MAX_ITEMS FEATURE MODE INTERVAL_VAL FETCH_DETAIL DETAIL_SPEED DETAIL_DELAY REPLY_LEVEL AUTO_EXPORT EXPORT_MODE TABLE_NAME FIELDS_JSON FILTERS_JSON KEYWORDS_JSON LINKS_JSON
  build_payload_from_flags
fi

json_validate "$PAYLOAD_JSON" || die "invalid payload json"

EXPECT_EXPORT="$(json_get "$PAYLOAD_JSON" '
  Boolean(
    data?.export?.enabled === true ||
    data?.autoExport === true ||
    (typeof data?.export?.mode === "string" && data.export.mode.length > 0) ||
    (typeof data?.exportMode === "string" && data.exportMode.length > 0) ||
    (typeof data?.tableName === "string" && data.tableName.length > 0) ||
    (Array.isArray(data?.fields) && data.fields.length > 0) ||
    data?.export
  )
')"
EXPECT_BITABLE_EXPORT="$(json_get "$PAYLOAD_JSON" '
  Boolean(
    data?.export?.enabled === true &&
    ["personal", "bitable"].includes(data?.export?.mode)
  ) || Boolean(
    data?.autoExport === true &&
    ["personal", "bitable"].includes(data?.exportMode)
  )
')"

ensure_bridge

if [[ "$FORCE_STOP_BEFORE_START" == "true" ]]; then
  log "force stop before start"
  api_post_empty '/api/stop' >/dev/null || true
fi

log "waiting idle"
wait_idle
collect_and_wait
