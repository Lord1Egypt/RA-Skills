#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
STATE_DIR="${UNRAID_STATE_DIR:-${REPO_DIR}/.state}"
LOG_DIR="${STATE_DIR}/logs"

require_base_url() {
  if [[ -z "${UNRAID_BASE_URL:-}" ]]; then
    echo "FAIL: Unraid base URL is not configured. Set UNRAID_BASE_URL and retry."
    exit 2
  fi
  if [[ ! "${UNRAID_BASE_URL}" =~ ^https?:// ]]; then
    echo "FAIL: UNRAID_BASE_URL must begin with http:// or https://."
    exit 2
  fi
}

require_api_key() {
  if [[ -z "${UNRAID_API_KEY:-}" ]]; then
    echo "FAIL: Unraid API key is not configured. Set UNRAID_API_KEY and retry."
    exit 2
  fi
}

require_timeout() {
  local timeout="${UNRAID_TIMEOUT_SECONDS:-10}"
  if ! [[ "${timeout}" =~ ^[0-9]+$ ]]; then
    echo "FAIL: UNRAID_TIMEOUT_SECONDS must be an integer."
    exit 2
  fi
}

require_command() {
  local cmd="$1"
  local why="$2"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "FAIL: Missing dependency '${cmd}' (${why})."
    exit 7
  fi
}

endpoint() {
  echo "${UNRAID_BASE_URL%/}/graphql"
}

ensure_state_dirs() {
  mkdir -p "${STATE_DIR}" "${LOG_DIR}" "${STATE_DIR}/snapshots"
}

latest_snapshot_path() {
  echo "${STATE_DIR}/latest_snapshot.json"
}

timestamped_snapshot_path() {
  local ts
  ts="$(date -u +"%Y%m%dT%H%M%SZ")"
  echo "${STATE_DIR}/snapshots/snapshot_${ts}.json"
}

sanitize_error_file() {
  local err_file="$1"
  tr '\n' ' ' < "$err_file" | sed 's/[[:space:]]\+/ /g' | cut -c1-300
}

graphql_post() {
  local query_json="$1"
  local body_file="$2"
  local err_file="$3"
  local timeout="${UNRAID_TIMEOUT_SECONDS:-10}"
  local csrf_token="${UNRAID_CSRF_TOKEN:-}"
  local session_cookie="${UNRAID_SESSION_COOKIE:-}"
  local ep
  local -a curl_args
  local config_file
  ep="$(endpoint)"

  # Create secure temporary config file for curl (keeps API key out of process list)
  config_file=$(mktemp) || { echo "Failed to create temp config file for curl" >&2; return 1; }
  chmod 600 "$config_file" || { rm -f "$config_file"; return 1; }
  trap "rm -f '$config_file'" RETURN

  # Write headers to config file (more secure than command-line arguments)
  {
    echo "header = \"Content-Type: application/json\""
    printf "header = \"x-api-key: %s\"\n" "$UNRAID_API_KEY"
    echo "header = \"X-Requested-With: XMLHttpRequest\""
    if [[ -n "$csrf_token" ]]; then
      printf "header = \"X-CSRF-TOKEN: %s\"\n" "$csrf_token"
    fi
    if [[ -n "$session_cookie" ]]; then
      printf "header = \"Cookie: %s\"\n" "$session_cookie"
    fi
  } > "$config_file"

  curl_args=(
    -sS
    --config "$config_file"
    --connect-timeout "$timeout"
    --max-time "$timeout"
    -o "$body_file"
    -w "%{http_code}"
    -X POST "$ep"
  )

  curl "${curl_args[@]}" --data "$query_json" 2>"$err_file"
}

compute_health_status_from_snapshot() {
  local snapshot_file="$1"
  local cpu_warn="${UNRAID_CPU_WARN_PERCENT:-85}"
  local cpu_crit="${UNRAID_CPU_CRIT_PERCENT:-95}"
  local mem_warn="${UNRAID_MEM_WARN_PERCENT:-85}"
  local mem_crit="${UNRAID_MEM_CRIT_PERCENT:-95}"
  local stopped_warn="${UNRAID_STOPPED_WARN_COUNT:-1}"
  local stopped_crit="${UNRAID_STOPPED_CRIT_COUNT:-3}"

  jq -r \
    --argjson cpu_warn "$cpu_warn" \
    --argjson cpu_crit "$cpu_crit" \
    --argjson mem_warn "$mem_warn" \
    --argjson mem_crit "$mem_crit" \
    --argjson stopped_warn "$stopped_warn" \
    --argjson stopped_crit "$stopped_crit" '
      def to_num($v):
        if $v == null then 0
        elif ($v|type) == "number" then $v
        elif ($v|type) == "string" then (($v|gsub("[^0-9.]"; "")|tonumber?) // 0)
        else 0 end;

      def normsmart($v): ($v // "" | ascii_downcase);

      . as $root
      | ($root.data.info.cpu.usage // 0 | to_num(.)) as $cpu
      | ($root.data.info.memory.usage // 0 | to_num(.)) as $mem
      | ($root.data.array.errors // 0 | to_num(.)) as $array_errors
      | ($root.data.array.parity.errors // 0 | to_num(.)) as $parity_errors
      | ($root.data.array.state // "unknown") as $array_state
      | ($root.data.array.syncAction // "") as $sync_action
      | ($root.data.array.syncProgress // "") as $sync_progress
      | ($root.data.docker.containers // []) as $containers
      | ($containers | map(select((.state // "")|ascii_downcase != "running"))) as $stopped
      | ($root.data.array.disks // []
          | map(select((normsmart(.smartStatus)) as $s | ($s != "" and $s != "ok" and $s != "disk_ok" and $s != "passed" and $s != "healthy" and $s != "unknown")))) as $disk_warnings
      | ($root.graphql_errors // []) as $graphql_errors
      | [] as $alerts
        | (if ($graphql_errors | length) > 0 then $alerts + ["GraphQL returned errors; snapshot may be partial."] else $alerts end) as $alerts
      | (if $array_errors > 0 then $alerts + ["Array reports " + ($array_errors|tostring) + " errors."] else $alerts end) as $alerts
      | (if $parity_errors > 0 then $alerts + ["Parity reports " + ($parity_errors|tostring) + " errors."] else $alerts end) as $alerts
      | (if ($disk_warnings | length) > 0 then $alerts + ["Disk SMART warnings: " + (($disk_warnings|map(.name // "unknown")|join(", ")))] else $alerts end) as $alerts
      | (if $cpu >= $cpu_crit then $alerts + ["CPU usage critical at " + ($cpu|tostring) + "%."]
         elif $cpu >= $cpu_warn then $alerts + ["CPU usage high at " + ($cpu|tostring) + "%."]
         else $alerts end) as $alerts
      | (if $mem >= $mem_crit then $alerts + ["Memory usage critical at " + ($mem|tostring) + "%."]
         elif $mem >= $mem_warn then $alerts + ["Memory usage high at " + ($mem|tostring) + "%."]
         else $alerts end) as $alerts
      | (if ($stopped | length) >= $stopped_crit then $alerts + ["Many containers are stopped: " + (($stopped|length)|tostring)]
         elif ($stopped | length) >= $stopped_warn then $alerts + ["Some containers are stopped: " + (($stopped|length)|tostring)]
         else $alerts end) as $alerts
      | (if (($array_state|ascii_downcase) != "started" and ($array_state|ascii_downcase) != "unknown") then $alerts + ["Array state is " + $array_state + "."] else $alerts end) as $alerts
      | (if ($sync_action|length) > 0 and ($sync_action|ascii_downcase) != "none" then
           $alerts + ["Array sync action active: " + $sync_action + (if ($sync_progress|length) > 0 then " (" + $sync_progress + ")" else "" end)]
         else $alerts end) as $alerts
      | {
          overall:
            (if $array_errors > 0 or $parity_errors > 0 or ($disk_warnings|length) > 0 or $cpu >= $cpu_crit or $mem >= $mem_crit or (($stopped|length) >= $stopped_crit)
             then "critical"
             elif ($alerts|length) > 0
             then "warning"
             else "healthy" end),
          alerts: $alerts,
          metrics: {
            cpu_usage_percent: $cpu,
            memory_usage_percent: $mem,
            array_errors: $array_errors,
            parity_errors: $parity_errors,
            stopped_containers: ($stopped|length),
            disk_smart_warning_count: ($disk_warnings|length)
          }
        }
    ' "$snapshot_file"
}