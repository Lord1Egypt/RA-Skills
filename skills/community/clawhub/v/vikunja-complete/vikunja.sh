#!/usr/bin/env bash
set -euo pipefail

# Vikunja custom core CLI (single-user local-first, publishable generic core)
# Requires: curl, jq

VERSION="0.4.0"
API_RETRIES="${VIKUNJA_API_RETRIES:-3}"
API_RETRY_DELAY="${VIKUNJA_API_RETRY_DELAY:-1}"

err() { echo "ERROR: $*" >&2; }

die() {
  local code="${2:-1}"
  err "$1"
  exit "$code"
}

require_bin() {
  command -v "$1" >/dev/null 2>&1 || die "Missing required binary: $1" 127
}

require_env() {
  local key="$1"
  [[ -n "${!key:-}" ]] || die "Missing required environment variable: $key" 2
}

is_int() {
  [[ "${1:-}" =~ ^[0-9]+$ ]]
}

is_dateish() {
  # Accept YYYY-MM-DD or RFC3339-ish timestamp.
  [[ "${1:-}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}([Tt ][0-9]{2}:[0-9]{2}(:[0-9]{2})?([Zz]|[+-][0-9]{2}:[0-9]{2})?)?$ ]]
}

normalize_due() {
  local due="${1:-}"
  [[ -n "$due" ]] || { echo ""; return; }
  if [[ "$due" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "${due}T00:00:00Z"
  else
    echo "$due"
  fi
}

normalize_base_url() {
  local raw="${VIKUNJA_URL%/}"
  case "$raw" in
    */api/v1) echo "$raw" ;;
    */api/v1/*) echo "${raw%%/api/v1*}/api/v1" ;;
    *) echo "$raw/api/v1" ;;
  esac
}

parse_kv_flag() {
  local flag="$1"
  local val="${2:-}"
  [[ -n "$val" ]] || die "Missing value for ${flag}" 2
  echo "$val"
}

urlencode() {
  jq -rn --arg v "$1" '$v|@uri'
}

api_call() {
  local method="$1"; shift
  local path="$1"; shift
  local data="${1:-}"

  local url="${API_BASE}${path}"
  local tmp code attempt=1 curl_rc=0

  is_int "$API_RETRIES" || die "VIKUNJA_API_RETRIES must be an integer" 2
  is_int "$API_RETRY_DELAY" || die "VIKUNJA_API_RETRY_DELAY must be an integer" 2

  while (( attempt <= API_RETRIES )); do
    tmp="$(mktemp)"
    code="000"
    curl_rc=0

    if [[ -n "$data" ]]; then
      code="$(curl -sS -o "$tmp" -w "%{http_code}" -X "$method" "$url" \
        -H "Authorization: Bearer ${VIKUNJA_TOKEN}" \
        -H "Content-Type: application/json" \
        --connect-timeout 10 --max-time 30 \
        --data "$data")" || curl_rc=$?
    else
      code="$(curl -sS -o "$tmp" -w "%{http_code}" -X "$method" "$url" \
        -H "Authorization: Bearer ${VIKUNJA_TOKEN}" \
        --connect-timeout 10 --max-time 30)" || curl_rc=$?
    fi

    if [[ "$curl_rc" -eq 0 && "$code" -ge 200 && "$code" -lt 300 ]]; then
      cat "$tmp"
      rm -f "$tmp"
      return 0
    fi

    if [[ "$curl_rc" -ne 0 || "$code" == "429" || "$code" -ge 500 ]]; then
      if (( attempt < API_RETRIES )); then
        rm -f "$tmp"
        sleep "$API_RETRY_DELAY"
        ((attempt++))
        continue
      fi
    fi

    local body
    body="$(cat "$tmp" 2>/dev/null || true)"
    rm -f "$tmp"

    if [[ "$curl_rc" -ne 0 ]]; then
      err "Network error calling ${method} ${path} (curl exit ${curl_rc})"
      exit 12
    fi

    case "$code" in
      400) err "Validation error (HTTP 400) on ${method} ${path}"; [[ -n "$body" ]] && err "Response: $body"; exit 14 ;;
      401|403) err "Auth/permission error (HTTP ${code}) on ${method} ${path}"; [[ -n "$body" ]] && err "Response: $body"; exit 11 ;;
      404) err "Not found (HTTP 404) on ${method} ${path}"; [[ -n "$body" ]] && err "Response: $body"; exit 15 ;;
      *) err "HTTP $code from ${method} ${path}"; [[ -n "$body" ]] && err "Response: $body"; exit 10 ;;
    esac
  done
}

safe_task_update() {
  local id="$1"
  local patch="$2"
  local current merged
  current="$(api_call GET "/tasks/${id}")"
  merged="$(jq -n --argjson cur "$current" --argjson p "$patch" '$cur + $p')"
  api_call POST "/tasks/${id}" "$merged"
}

resolve_project_id() {
  local project_id="${1:-}"
  local project_name="${2:-}"

  if [[ -n "$project_id" && -n "$project_name" ]]; then
    die "Use either --project-id or --project (name), not both" 2
  fi

  if [[ -n "$project_id" ]]; then
    is_int "$project_id" || die "--project-id must be an integer" 2
    echo "$project_id"
    return
  fi

  if [[ -n "$project_name" ]]; then
    local projects matches count
    projects="$(api_call GET "/projects")"
    matches="$(echo "$projects" | jq -r --arg n "$project_name" '.[] | select(.title==$n) | .id')"
    count="$(echo "$matches" | sed '/^$/d' | wc -l | tr -d ' ')"

    if [[ "$count" == "0" ]]; then
      die "No project found with exact title: ${project_name}" 15
    elif [[ "$count" != "1" ]]; then
      die "Ambiguous project title '${project_name}' (${count} matches). Use --project-id." 2
    fi

    echo "$matches" | sed '/^$/d' | head -n1
    return
  fi

  echo ""
}

resolve_view_id() {
  local project_id="$1"
  local view_id="${2:-}"
  local view_name="${3:-}"

  if [[ -n "$view_id" && -n "$view_name" ]]; then
    die "Use either --view-id or --view (name), not both" 2
  fi

  if [[ -n "$view_id" ]]; then
    is_int "$view_id" || die "--view-id must be integer" 2
    echo "$view_id"
    return
  fi

  if [[ -n "$view_name" ]]; then
    local views matches count
    views="$(api_call GET "/projects/${project_id}/views")"
    matches="$(echo "$views" | jq -r --arg n "$view_name" '.[] | select(.title==$n) | .id')"
    count="$(echo "$matches" | sed '/^$/d' | wc -l | tr -d ' ')"
    if [[ "$count" == "0" ]]; then
      die "No view found with exact title '${view_name}' in project ${project_id}" 15
    elif [[ "$count" != "1" ]]; then
      die "Ambiguous view title '${view_name}' (${count} matches). Use --view-id." 2
    fi
    echo "$matches" | sed '/^$/d' | head -n1
    return
  fi

  echo ""
}

resolve_bucket_id() {
  local project_id="$1"
  local view_id="$2"
  local bucket_id="${3:-}"
  local bucket_name="${4:-}"

  if [[ -n "$bucket_id" && -n "$bucket_name" ]]; then
    die "Use either --bucket-id or --bucket (name), not both" 2
  fi

  if [[ -n "$bucket_id" ]]; then
    is_int "$bucket_id" || die "--bucket-id must be integer" 2
    echo "$bucket_id"
    return
  fi

  if [[ -n "$bucket_name" ]]; then
    local buckets matches count
    buckets="$(api_call GET "/projects/${project_id}/views/${view_id}/buckets")"
    matches="$(echo "$buckets" | jq -r --arg n "$bucket_name" '.[] | select(.title==$n) | .id')"
    count="$(echo "$matches" | sed '/^$/d' | wc -l | tr -d ' ')"
    if [[ "$count" == "0" ]]; then
      die "No bucket found with exact title '${bucket_name}' in view ${view_id}" 15
    elif [[ "$count" != "1" ]]; then
      die "Ambiguous bucket title '${bucket_name}' (${count} matches). Use --bucket-id." 2
    fi
    echo "$matches" | sed '/^$/d' | head -n1
    return
  fi

  echo ""
}

usage() {
  cat <<'EOF'
vikunja.sh (custom core)

Usage:
  vikunja.sh health
  vikunja.sh list [--project-id ID | --project NAME] [--overdue|--today] [--filter EXPR] [--limit N]
  vikunja.sh create (--project-id ID | --project NAME) --title TEXT [--description TEXT] [--due YYYY-MM-DD|RFC3339] [--priority 1..5]
  vikunja.sh complete --id TASK_ID
  vikunja.sh move --id TASK_ID (--project-id ID | --project NAME) [--view-id ID | --view NAME] [--bucket-id ID | --bucket NAME]
  vikunja.sh update --id TASK_ID [--title TEXT] [--description TEXT] [--due DATE] [--priority 1..5] [--done true|false] [--reminder DATE]
  vikunja.sh bulk-update --ids 1,2,3 [--priority 1..5] [--done true|false] [--due DATE]

  vikunja.sh comments list --task-id TASK_ID
  vikunja.sh comments add --task-id TASK_ID --comment TEXT
  vikunja.sh comments update --task-id TASK_ID --comment-id ID --comment TEXT
  vikunja.sh comments delete --task-id TASK_ID --comment-id ID

  vikunja.sh labels list [--task-id TASK_ID]
  vikunja.sh labels create --title TEXT [--color HEX]
  vikunja.sh labels add --task-id TASK_ID (--label-id ID | --label TITLE)
  vikunja.sh labels remove --task-id TASK_ID (--label-id ID | --label TITLE)

  vikunja.sh assignees list --task-id TASK_ID
  vikunja.sh assignees add --task-id TASK_ID --user-id USER_ID
  vikunja.sh assignees remove --task-id TASK_ID --user-id USER_ID

  vikunja.sh buckets list (--project-id ID | --project NAME) [--view-id ID | --view NAME]
  vikunja.sh buckets create (--project-id ID | --project NAME) (--view-id ID | --view NAME) --title TEXT

  vikunja.sh views list (--project-id ID | --project NAME)
  vikunja.sh views create (--project-id ID | --project NAME) --title TEXT [--kind list|kanban|table|gantt]

  vikunja.sh webhooks list (--project-id ID | --project NAME)
  vikunja.sh webhooks create (--project-id ID | --project NAME) --target-url URL --event EVENT [--event EVENT ...]
  vikunja.sh webhooks delete (--project-id ID | --project NAME) --webhook-id ID

  vikunja.sh attachments list --task-id TASK_ID
  vikunja.sh attachments upload --task-id TASK_ID --file /path/to/file [--filename NAME]
  vikunja.sh attachments download --task-id TASK_ID --attachment-id ID --output /path/to/file
  vikunja.sh attachments delete --task-id TASK_ID --attachment-id ID

  vikunja.sh relations add --task-id TASK_ID --other-task-id ID --kind KIND
  vikunja.sh relations remove --task-id TASK_ID --other-task-id ID --kind KIND

  vikunja.sh filters list
  vikunja.sh filters create --title TEXT --filter EXPR
  vikunja.sh filters get --id FILTER_ID
  vikunja.sh filters update --id FILTER_ID [--title TEXT] [--filter EXPR]
  vikunja.sh filters delete --id FILTER_ID

  vikunja.sh notifications list
  vikunja.sh notifications mark [--id NOTIFICATION_ID]

  vikunja.sh subscriptions subscribe --entity project|task --entity-id ID
  vikunja.sh subscriptions unsubscribe --entity project|task --entity-id ID

  vikunja.sh tokens list
  vikunja.sh tokens create --title TEXT --expires-at RFC3339 [--permissions-json '{"tasks":["read_all"]}']
  vikunja.sh tokens delete --token-id ID

Environment:
  VIKUNJA_URL              Base Vikunja URL (example: https://vikunja.example.com)
  VIKUNJA_TOKEN            API/JWT token
  VIKUNJA_API_RETRIES      Retry attempts for transient failures (default: 3)
  VIKUNJA_API_RETRY_DELAY  Seconds between retries (default: 1)

Notes:
  - URL is normalized to /api/v1 automatically.
  - Non-zero exit codes on validation/API failures.
  - Retries apply to network errors, HTTP 429, and HTTP 5xx.
EOF
}

cmd_health() {
  local info_json user_json
  info_json="$(api_call GET "/info")"
  user_json="$(api_call GET "/user")"

  jq -n \
    --argjson info "$info_json" \
    --argjson user "$user_json" \
    '{status:"ok", version:($info.version // "unknown"), user:($user.username // $user.name // "unknown")}'
}

cmd_list() {
  local project_id="" project_name="" overdue=false today=false filter="" limit=50

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --overdue) overdue=true; shift ;;
      --today) today=true; shift ;;
      --filter) filter="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --limit) limit="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for list: $1" 2 ;;
    esac
  done

  [[ "$overdue" == true && "$today" == true ]] && die "Use either --overdue or --today, not both" 2
  is_int "$limit" || die "--limit must be an integer" 2

  project_id="$(resolve_project_id "$project_id" "$project_name")"

  if [[ -z "$filter" ]]; then
    if [[ "$overdue" == true ]]; then
      filter='done = false && due_date < now'
    elif [[ "$today" == true ]]; then
      filter='done = false && due_date >= now/d && due_date < now/d + 1d'
    fi
  fi

  local path="/tasks?page=1&per_page=${limit}&sort_by[]=due_date&order_by[]=asc"
  if [[ -n "$project_id" ]]; then
    local pexpr="project_id = ${project_id}"
    [[ -n "$filter" ]] && pexpr="(${pexpr}) && (${filter})"
    path="/tasks?page=1&per_page=${limit}&sort_by[]=due_date&order_by[]=asc&filter=$(urlencode "$pexpr")"
  elif [[ -n "$filter" ]]; then
    path+="&filter=$(urlencode "$filter")"
  fi

  api_call GET "$path" | jq 'map({id,title,done,priority,due_date,project_id,bucket_id})'
}

cmd_create() {
  local project_id="" project_name="" title="" description="" due="" priority=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --description) description="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --due) due="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --priority) priority="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for create: $1" 2 ;;
    esac
  done

  project_id="$(resolve_project_id "$project_id" "$project_name")"
  [[ -n "$project_id" ]] || die "--project-id or --project is required" 2
  [[ -n "$title" ]] || die "--title is required" 2
  [[ ${#title} -ge 2 ]] || die "--title must be at least 2 chars" 2

  if [[ -n "$due" ]]; then
    is_dateish "$due" || die "--due must be YYYY-MM-DD or RFC3339" 2
    due="$(normalize_due "$due")"
  fi
  if [[ -n "$priority" ]]; then
    is_int "$priority" || die "--priority must be an integer 1..5" 2
    (( priority >= 1 && priority <= 5 )) || die "--priority must be 1..5" 2
  fi

  local payload
  payload="$(jq -n \
    --arg title "$title" \
    --arg description "$description" \
    --arg due "$due" \
    --argjson hasDue "$( [[ -n "$due" ]] && echo true || echo false )" \
    --arg priority "$priority" \
    --argjson hasPriority "$( [[ -n "$priority" ]] && echo true || echo false )" \
    '{title:$title}
      + (if ($description|length)>0 then {description:$description} else {} end)
      + (if $hasDue then {due_date:$due} else {} end)
      + (if $hasPriority then {priority:($priority|tonumber)} else {} end)')"

  api_call PUT "/projects/${project_id}/tasks" "$payload" | jq '{id,title,done,priority,due_date,project_id}'
}

cmd_complete() {
  local id=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for complete: $1" 2 ;;
    esac
  done

  [[ -n "$id" ]] || die "--id is required" 2
  is_int "$id" || die "--id must be an integer" 2

  safe_task_update "$id" '{"done":true}' | jq '{id,title,done,done_at,project_id,priority,due_date}'
}

cmd_move() {
  local id="" project_id="" project_name="" view_id="" view_name="" bucket_id="" bucket_name=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --view-id) view_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --view) view_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --bucket-id) bucket_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --bucket) bucket_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for move: $1" 2 ;;
    esac
  done

  [[ -n "$id" ]] || die "--id is required" 2
  is_int "$id" || die "--id must be integer" 2

  project_id="$(resolve_project_id "$project_id" "$project_name")"
  [[ -n "$project_id" ]] || die "--project-id or --project is required" 2

  view_id="$(resolve_view_id "$project_id" "$view_id" "$view_name")"

  if [[ -z "$view_id" && -z "$bucket_id" && -z "$bucket_name" ]]; then
    safe_task_update "$id" "$(jq -n --argjson p "$project_id" '{project_id:$p}')" | jq '{id,title,project_id,bucket_id,priority,due_date,done}'
    return
  fi

  [[ -n "$view_id" ]] || die "Bucket move requires --view-id or --view" 2
  bucket_id="$(resolve_bucket_id "$project_id" "$view_id" "$bucket_id" "$bucket_name")"
  [[ -n "$bucket_id" ]] || die "Bucket move requires --bucket-id or --bucket" 2

  local payload
  payload="$(jq -n --argjson task_id "$id" --argjson bucket_id "$bucket_id" --argjson project_view_id "$view_id" '{task_id:$task_id,bucket_id:$bucket_id,project_view_id:$project_view_id}')"
  api_call POST "/projects/${project_id}/views/${view_id}/buckets/${bucket_id}/tasks" "$payload" | jq '{task_id,bucket_id,project_view_id}'
}

cmd_update() {
  local id="" title="" description="" due="" priority="" done="" reminder=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --description) description="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --due) due="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --priority) priority="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --done) done="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --reminder) reminder="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for update: $1" 2 ;;
    esac
  done

  [[ -n "$id" ]] || die "--id is required" 2
  is_int "$id" || die "--id must be integer" 2
  [[ -n "$title$description$due$priority$done$reminder" ]] || die "No fields provided to update" 2

  if [[ -n "$due" ]]; then
    is_dateish "$due" || die "--due must be YYYY-MM-DD or RFC3339" 2
    due="$(normalize_due "$due")"
  fi
  if [[ -n "$priority" ]]; then
    is_int "$priority" || die "--priority must be integer 1..5" 2
    (( priority >= 1 && priority <= 5 )) || die "--priority must be 1..5" 2
  fi
  if [[ -n "$done" ]]; then
    [[ "$done" == "true" || "$done" == "false" ]] || die "--done must be true|false" 2
  fi
  if [[ -n "$reminder" ]]; then
    is_dateish "$reminder" || die "--reminder must be YYYY-MM-DD or RFC3339" 2
    reminder="$(normalize_due "$reminder")"
  fi

  local payload
  payload="$(jq -n \
    --arg title "$title" \
    --arg description "$description" \
    --arg due "$due" \
    --arg priority "$priority" \
    --arg done "$done" \
    --arg reminder "$reminder" \
    '{ }
    + (if ($title|length)>0 then {title:$title} else {} end)
    + (if ($description|length)>0 then {description:$description} else {} end)
    + (if ($due|length)>0 then {due_date:$due} else {} end)
    + (if ($priority|length)>0 then {priority:($priority|tonumber)} else {} end)
    + (if ($done|length)>0 then {done:($done=="true")} else {} end)
    + (if ($reminder|length)>0 then {reminders:[{reminder:$reminder}]} else {} end)
  ')"

  safe_task_update "$id" "$payload" | jq '{id,title,done,priority,due_date,reminders,project_id,bucket_id}'
}

cmd_bulk_update() {
  local ids_csv="" priority="" done="" due=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --ids) ids_csv="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --priority) priority="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --done) done="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --due) due="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for bulk-update: $1" 2 ;;
    esac
  done

  [[ -n "$ids_csv" ]] || die "--ids is required (comma-separated task IDs)" 2
  [[ -n "$priority$done$due" ]] || die "Provide at least one field (--priority, --done, --due)" 2

  if [[ -n "$priority" ]]; then
    is_int "$priority" || die "--priority must be integer 1..5" 2
    (( priority >= 1 && priority <= 5 )) || die "--priority must be 1..5" 2
  fi
  if [[ -n "$done" ]]; then
    [[ "$done" == "true" || "$done" == "false" ]] || die "--done must be true|false" 2
  fi
  if [[ -n "$due" ]]; then
    is_dateish "$due" || die "--due must be YYYY-MM-DD or RFC3339" 2
    due="$(normalize_due "$due")"
  fi

  local patch
  patch="$(jq -n --arg priority "$priority" --arg done "$done" --arg due "$due" '
    {}
    + (if ($priority|length)>0 then {priority:($priority|tonumber)} else {} end)
    + (if ($done|length)>0 then {done:($done=="true")} else {} end)
    + (if ($due|length)>0 then {due_date:$due} else {} end)
  ')"

  local ids_json
  ids_json="$(echo "$ids_csv" | jq -Rc 'split(",") | map(gsub("^ +| +$"; "")) | map(select(length>0) | tonumber?)')"
  [[ "$ids_json" != "[]" ]] || die "--ids must include at least one integer ID" 2

  local out='[]' id
  while IFS= read -r id; do
    [[ -n "$id" ]] || continue
    is_int "$id" || die "All IDs in --ids must be integers" 2
    out="$(jq -n --argjson arr "$out" --argjson row "$(safe_task_update "$id" "$patch" | jq '{id,title,done,priority,due_date,project_id}')" '$arr + [$row]')"
  done < <(echo "$ids_json" | jq -r '.[]')

  echo "$out"
}

cmd_comments() {
  local sub="${1:-}"; shift || true
  local task_id="" comment_id="" comment=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --comment-id) comment_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --comment) comment="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for comments ${sub}: $1" 2 ;;
    esac
  done

  [[ -n "$task_id" ]] || die "--task-id is required" 2
  is_int "$task_id" || die "--task-id must be integer" 2

  case "$sub" in
    list)
      api_call GET "/tasks/${task_id}/comments" | jq 'map({id,comment,created,updated,author:(.author.username // .author.name // null)})'
      ;;
    add)
      [[ -n "$comment" ]] || die "--comment is required" 2
      api_call PUT "/tasks/${task_id}/comments" "$(jq -n --arg c "$comment" '{comment:$c}')" | jq '{id,comment,created,updated}'
      ;;
    update)
      [[ -n "$comment_id" ]] || die "--comment-id is required" 2
      is_int "$comment_id" || die "--comment-id must be integer" 2
      [[ -n "$comment" ]] || die "--comment is required" 2
      api_call POST "/tasks/${task_id}/comments/${comment_id}" "$(jq -n --arg c "$comment" '{comment:$c}')" | jq '{id,comment,created,updated}'
      ;;
    delete)
      [[ -n "$comment_id" ]] || die "--comment-id is required" 2
      is_int "$comment_id" || die "--comment-id must be integer" 2
      api_call DELETE "/tasks/${task_id}/comments/${comment_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown comments subcommand: ${sub}" 2 ;;
  esac
}

resolve_label_id() {
  local label_id="${1:-}"
  local label_name="${2:-}"

  if [[ -n "$label_id" && -n "$label_name" ]]; then
    die "Use either --label-id or --label, not both" 2
  fi
  if [[ -n "$label_id" ]]; then
    is_int "$label_id" || die "--label-id must be integer" 2
    echo "$label_id"
    return
  fi
  if [[ -n "$label_name" ]]; then
    local labels matches count
    labels="$(api_call GET "/labels")"
    matches="$(echo "$labels" | jq -r --arg n "$label_name" '.[] | select(.title==$n) | .id')"
    count="$(echo "$matches" | sed '/^$/d' | wc -l | tr -d ' ')"
    if [[ "$count" == "0" ]]; then
      die "No label found with exact title: ${label_name}" 15
    elif [[ "$count" != "1" ]]; then
      die "Ambiguous label title '${label_name}' (${count} matches). Use --label-id." 2
    fi
    echo "$matches" | sed '/^$/d' | head -n1
    return
  fi
  echo ""
}

cmd_labels() {
  local sub="${1:-}"; shift || true
  local task_id="" label_id="" label="" title="" color=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --label-id) label_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --label) label="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --color) color="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for labels ${sub}: $1" 2 ;;
    esac
  done

  case "$sub" in
    list)
      if [[ -n "$task_id" ]]; then
        is_int "$task_id" || die "--task-id must be integer" 2
        api_call GET "/tasks/${task_id}/labels" | jq 'map({id,title,hex_color,created})'
      else
        api_call GET "/labels" | jq 'map({id,title,hex_color,created})'
      fi
      ;;
    create)
      [[ -n "$title" ]] || die "--title is required" 2
      if [[ -n "$color" ]]; then
        [[ "$color" =~ ^#?[0-9a-fA-F]{6}$ ]] || die "--color must be HEX like ff0000 or #ff0000" 2
        color="${color#\#}"
      fi
      api_call PUT "/labels" "$(jq -n --arg t "$title" --arg c "$color" '{title:$t} + (if ($c|length)>0 then {hex_color:$c} else {} end)')" | jq '{id,title,hex_color,created}'
      ;;
    add)
      [[ -n "$task_id" ]] || die "--task-id is required" 2
      is_int "$task_id" || die "--task-id must be integer" 2
      label_id="$(resolve_label_id "$label_id" "$label")"
      [[ -n "$label_id" ]] || die "--label-id or --label is required" 2
      api_call PUT "/tasks/${task_id}/labels" "$(jq -n --argjson id "$label_id" '{label_id:$id}')" | jq '{label_id,created}'
      ;;
    remove)
      [[ -n "$task_id" ]] || die "--task-id is required" 2
      is_int "$task_id" || die "--task-id must be integer" 2
      label_id="$(resolve_label_id "$label_id" "$label")"
      [[ -n "$label_id" ]] || die "--label-id or --label is required" 2
      api_call DELETE "/tasks/${task_id}/labels/${label_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown labels subcommand: ${sub}" 2 ;;
  esac
}

cmd_assignees() {
  local sub="${1:-}"; shift || true
  local task_id="" user_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --user-id) user_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for assignees ${sub}: $1" 2 ;;
    esac
  done

  [[ -n "$task_id" ]] || die "--task-id is required" 2
  is_int "$task_id" || die "--task-id must be integer" 2

  case "$sub" in
    list)
      # Some Vikunja versions return HTTP 500 on /tasks/{id}/assignees.
      if out="$(api_call GET "/tasks/${task_id}/assignees" 2>/dev/null)"; then
        echo "$out" | jq 'map({id,username,name})'
      else
        api_call GET "/tasks/${task_id}" | jq '(.assignees // .users // []) | map({id,username,name})'
      fi
      ;;
    add)
      [[ -n "$user_id" ]] || die "--user-id is required" 2
      is_int "$user_id" || die "--user-id must be integer" 2
      api_call PUT "/tasks/${task_id}/assignees" "$(jq -n --argjson uid "$user_id" '{user_id:$uid}')" | jq '{user_id:(.user_id // .id),created:(.Created // .created)}'
      ;;
    remove)
      [[ -n "$user_id" ]] || die "--user-id is required" 2
      is_int "$user_id" || die "--user-id must be integer" 2
      api_call DELETE "/tasks/${task_id}/assignees/${user_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown assignees subcommand: ${sub}" 2 ;;
  esac
}

cmd_views() {
  local sub="${1:-}"; shift || true
  local project_id="" project_name="" title="" kind="list"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --kind) kind="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for views ${sub}: $1" 2 ;;
    esac
  done

  project_id="$(resolve_project_id "$project_id" "$project_name")"
  [[ -n "$project_id" ]] || die "--project-id or --project is required" 2

  case "$sub" in
    list)
      api_call GET "/projects/${project_id}/views" | jq 'map({id,title,view_kind,project_id,position})'
      ;;
    create)
      [[ -n "$title" ]] || die "--title is required" 2
      [[ "$kind" =~ ^(list|kanban|table|gantt)$ ]] || die "--kind must be one of: list|kanban|table|gantt" 2
      api_call PUT "/projects/${project_id}/views" "$(jq -n --arg t "$title" --arg k "$kind" '{title:$t,view_kind:$k}')" | jq '{id,title,view_kind,project_id}'
      ;;
    *) die "Unknown views subcommand: ${sub}" 2 ;;
  esac
}

cmd_buckets() {
  local sub="${1:-}"; shift || true
  local project_id="" project_name="" view_id="" view_name="" title=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --view-id) view_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --view) view_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for buckets ${sub}: $1" 2 ;;
    esac
  done

  project_id="$(resolve_project_id "$project_id" "$project_name")"
  [[ -n "$project_id" ]] || die "--project-id or --project is required" 2

  if [[ "$sub" == "list" && -z "$view_id" && -z "$view_name" ]]; then
    local out='[]' vid
    while IFS= read -r vid; do
      local one
      one="$(api_call GET "/projects/${project_id}/views/${vid}/buckets" | jq --argjson v "$vid" 'map({id,title,project_view_id:$v,position,count,limit})')"
      out="$(jq -n --argjson a "$out" --argjson b "$one" '$a + $b')"
    done < <(api_call GET "/projects/${project_id}/views" | jq -r '.[].id')
    echo "$out"
    return
  fi

  view_id="$(resolve_view_id "$project_id" "$view_id" "$view_name")"
  [[ -n "$view_id" ]] || die "--view-id or --view is required" 2

  case "$sub" in
    list)
      api_call GET "/projects/${project_id}/views/${view_id}/buckets" | jq 'map({id,title,project_view_id,position,count,limit})'
      ;;
    create)
      [[ -n "$title" ]] || die "--title is required" 2
      api_call PUT "/projects/${project_id}/views/${view_id}/buckets" "$(jq -n --arg t "$title" '{title:$t}')" | jq '{id,title,project_view_id,position,count,limit}'
      ;;
    *) die "Unknown buckets subcommand: ${sub}" 2 ;;
  esac
}

cmd_webhooks() {
  local sub="${1:-}"; shift || true
  local project_id="" project_name="" webhook_id="" target_url=""
  local events=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) project_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --project) project_name="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --webhook-id) webhook_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --target-url) target_url="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --event) events+=("$(parse_kv_flag "$1" "${2:-}")"); shift 2 ;;
      *) die "Unknown flag for webhooks ${sub}: $1" 2 ;;
    esac
  done

  project_id="$(resolve_project_id "$project_id" "$project_name")"
  [[ -n "$project_id" ]] || die "--project-id or --project is required" 2

  case "$sub" in
    list)
      api_call GET "/projects/${project_id}/webhooks" | jq 'map({id,target_url,events,created,updated})'
      ;;
    create)
      [[ -n "$target_url" ]] || die "--target-url is required" 2
      [[ ${#events[@]} -gt 0 ]] || die "At least one --event is required" 2
      api_call PUT "/projects/${project_id}/webhooks" "$(jq -n --arg u "$target_url" --argjson e "$(printf '%s\n' "${events[@]}" | jq -R . | jq -s .)" '{target_url:$u,events:$e}')" | jq '{id,target_url,events,created,updated}'
      ;;
    delete)
      [[ -n "$webhook_id" ]] || die "--webhook-id is required" 2
      is_int "$webhook_id" || die "--webhook-id must be integer" 2
      api_call DELETE "/projects/${project_id}/webhooks/${webhook_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown webhooks subcommand: ${sub}" 2 ;;
  esac
}


cmd_attachments() {
  local sub="${1:-}"; shift || true
  local task_id="" attachment_id="" file="" filename="" output=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --attachment-id) attachment_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --file) file="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --filename) filename="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --output) output="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for attachments ${sub}: $1" 2 ;;
    esac
  done

  [[ -n "$task_id" ]] || die "--task-id is required" 2
  is_int "$task_id" || die "--task-id must be integer" 2

  case "$sub" in
    list)
      api_call GET "/tasks/${task_id}/attachments" | jq 'map({id,task_id,file_name:(.file.name // .file_name),file_size:(.file.size // .file_size),created_by:(.created_by.username // .created_by.name // null),created})'
      ;;
    upload)
      [[ -n "$file" ]] || die "--file is required" 2
      [[ -f "$file" ]] || die "--file path not found: ${file}" 2
      local file_arg response
      if [[ -n "$filename" ]]; then
        file_arg="files=@${file};filename=${filename}"
      else
        file_arg="files=@${file}"
      fi
      response="$(curl -sS -X PUT "${API_BASE}/tasks/${task_id}/attachments"         -H "Authorization: Bearer ${VIKUNJA_TOKEN}"         --connect-timeout 10 --max-time 60         -F "$file_arg")"
      echo "$response" | jq 'if ((.errors // []) | length) > 0 then error("attachment upload failed") else ((.success // []) | map({id,task_id,file_name:(.file.name // .file_name),file_size:(.file.size // .file_size),created}) | .[0]) end'
      ;;
    download)
      [[ -n "$attachment_id" ]] || die "--attachment-id is required" 2
      is_int "$attachment_id" || die "--attachment-id must be integer" 2
      [[ -n "$output" ]] || die "--output is required" 2
      local code
      code="$(curl -sS -o "$output" -w "%{http_code}" -X GET "${API_BASE}/tasks/${task_id}/attachments/${attachment_id}"         -H "Authorization: Bearer ${VIKUNJA_TOKEN}"         --connect-timeout 10 --max-time 60)"
      if [[ "$code" -lt 200 || "$code" -ge 300 ]]; then
        rm -f "$output"
        die "Attachment download failed (HTTP ${code})" 10
      fi
      jq -n --arg path "$output" '{message:"ok",output:$path}'
      ;;
    delete)
      [[ -n "$attachment_id" ]] || die "--attachment-id is required" 2
      is_int "$attachment_id" || die "--attachment-id must be integer" 2
      api_call DELETE "/tasks/${task_id}/attachments/${attachment_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown attachments subcommand: ${sub}" 2 ;;
  esac
}

cmd_relations() {
  local sub="${1:-}"; shift || true
  local task_id="" other_task_id="" kind=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --other-task-id) other_task_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --kind) kind="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for relations ${sub}: $1" 2 ;;
    esac
  done

  [[ -n "$task_id" ]] || die "--task-id is required" 2
  [[ -n "$other_task_id" ]] || die "--other-task-id is required" 2
  [[ -n "$kind" ]] || die "--kind is required" 2
  is_int "$task_id" || die "--task-id must be integer" 2
  is_int "$other_task_id" || die "--other-task-id must be integer" 2
  [[ "$kind" =~ ^(subtask|parenttask|related|duplicateof|duplicates|blocking|blocked|precedes|follows|copiedfrom|copiedto)$ ]] || die "--kind must be one of: subtask|parenttask|related|duplicateof|duplicates|blocking|blocked|precedes|follows|copiedfrom|copiedto" 2

  case "$sub" in
    add)
      api_call PUT "/tasks/${task_id}/relations" "$(jq -n --argjson other "$other_task_id" --arg kind "$kind" '{other_task_id:$other,relation_kind:$kind}')" | jq '{task_id,other_task_id,relation_kind,created}'
      ;;
    remove)
      api_call DELETE "/tasks/${task_id}/relations/${kind}/${other_task_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown relations subcommand: ${sub}" 2 ;;
  esac
}

cmd_filters() {
  local sub="${1:-}"; shift || true
  local id="" title="" filter=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --filter) filter="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for filters ${sub}: $1" 2 ;;
    esac
  done

  case "$sub" in
    list)
      api_call GET "/projects" | jq 'map(select(.id < 0) | {id:((.id * -1) - 1),title,created,updated})'
      ;;
    create)
      [[ -n "$title" ]] || die "--title is required" 2
      [[ -n "$filter" ]] || die "--filter is required" 2
      api_call PUT "/filters" "$(jq -n --arg t "$title" --arg f "$filter" '{title:$t,filters:{filter:$f}}')" | jq '{id,title,filter:(.filters.filter // null),created,updated}'
      ;;
    get)
      [[ -n "$id" ]] || die "--id is required" 2
      is_int "$id" || die "--id must be integer" 2
      api_call GET "/filters/${id}" | jq '{id,title,filter:(.filters.filter // null),created,updated}'
      ;;
    update)
      [[ -n "$id" ]] || die "--id is required" 2
      is_int "$id" || die "--id must be integer" 2
      [[ -n "$title$filter" ]] || die "Provide at least one field (--title, --filter)" 2
      local current_filter
      current_filter="$(api_call GET "/filters/${id}")"
      api_call POST "/filters/${id}" "$(jq -n --arg t "$title" --arg f "$filter" --argjson cur "$current_filter" '{filters:($cur.filters // {})} + (if ($t|length)>0 then {title:$t} else {} end) + (if ($f|length)>0 then {filters:(($cur.filters // {}) + {filter:$f})} else {} end)')" | jq '{id,title,filter:(.filters.filter // null),created,updated}'
      ;;
    delete)
      [[ -n "$id" ]] || die "--id is required" 2
      is_int "$id" || die "--id must be integer" 2
      api_call DELETE "/filters/${id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown filters subcommand: ${sub}" 2 ;;
  esac
}

cmd_notifications() {
  local sub="${1:-}"; shift || true
  local id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for notifications ${sub}: $1" 2 ;;
    esac
  done

  case "$sub" in
    list)
      api_call GET "/notifications" | jq 'map({id,name,subject,read_at,created})'
      ;;
    mark)
      if [[ -n "$id" ]]; then
        is_int "$id" || die "--id must be integer" 2
        api_call POST "/notifications/${id}" | jq '{id,read_at,message:(.message // empty)}'
      else
        api_call POST "/notifications" | jq '{message:(.message // "ok")}'
      fi
      ;;
    *) die "Unknown notifications subcommand: ${sub}" 2 ;;
  esac
}

cmd_subscriptions() {
  local sub="${1:-}"; shift || true
  local entity="" entity_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --entity) entity="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --entity-id) entity_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for subscriptions ${sub}: $1" 2 ;;
    esac
  done

  [[ -n "$entity" ]] || die "--entity is required" 2
  [[ "$entity" =~ ^(project|task)$ ]] || die "--entity must be project|task" 2
  [[ -n "$entity_id" ]] || die "--entity-id is required" 2
  is_int "$entity_id" || die "--entity-id must be integer" 2

  case "$sub" in
    subscribe)
      api_call PUT "/subscriptions/${entity}/${entity_id}" | jq --arg e "$entity" --argjson id "$entity_id" '{message:(.message // "ok"),entity:$e,entity_id:$id}'
      ;;
    unsubscribe)
      api_call DELETE "/subscriptions/${entity}/${entity_id}" | jq --arg e "$entity" --argjson id "$entity_id" '{message:(.message // "ok"),entity:$e,entity_id:$id}'
      ;;
    *) die "Unknown subscriptions subcommand: ${sub}" 2 ;;
  esac
}

cmd_tokens() {
  local sub="${1:-}"; shift || true
  local token_id="" title="" expires_at="" permissions_json='{"tasks":["read_all"]}'

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --token-id) token_id="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --title) title="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --expires-at) expires_at="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      --permissions-json) permissions_json="$(parse_kv_flag "$1" "${2:-}")"; shift 2 ;;
      *) die "Unknown flag for tokens ${sub}: $1" 2 ;;
    esac
  done

  case "$sub" in
    list)
      api_call GET "/tokens" | jq 'map({id,title,permissions,created,expires_at})'
      ;;
    create)
      [[ -n "$title" ]] || die "--title is required" 2
      [[ -n "$expires_at" ]] || die "--expires-at is required" 2
      is_dateish "$expires_at" || die "--expires-at must be YYYY-MM-DD or RFC3339" 2
      expires_at="$(normalize_due "$expires_at")"
      echo "$permissions_json" | jq -e 'type=="object" and length>0' >/dev/null || die "--permissions-json must be a non-empty JSON object" 2
      api_call PUT "/tokens" "$(jq -n --arg t "$title" --arg e "$expires_at" --argjson p "$permissions_json" '{title:$t,expires_at:$e,permissions:$p}')" | jq '{id,title,token,permissions,created,expires_at}'
      ;;
    delete)
      [[ -n "$token_id" ]] || die "--token-id is required" 2
      is_int "$token_id" || die "--token-id must be integer" 2
      api_call DELETE "/tokens/${token_id}" | jq '{message:(.message // "ok")}'
      ;;
    *) die "Unknown tokens subcommand: ${sub}" 2 ;;
  esac
}

main() {
  require_bin curl
  require_bin jq

  local cmd="${1:-}"
  [[ -n "$cmd" ]] || { usage; exit 0; }
  shift || true

  case "$cmd" in
    -h|--help|help) usage; exit 0 ;;
    --version|version) echo "$VERSION"; exit 0 ;;
  esac

  require_env VIKUNJA_URL
  require_env VIKUNJA_TOKEN
  API_BASE="$(normalize_base_url)"

  case "$cmd" in
    health) cmd_health "$@" ;;
    list) cmd_list "$@" ;;
    create) cmd_create "$@" ;;
    complete) cmd_complete "$@" ;;
    move) cmd_move "$@" ;;
    update) cmd_update "$@" ;;
    bulk-update) cmd_bulk_update "$@" ;;
    comments) cmd_comments "$@" ;;
    labels) cmd_labels "$@" ;;
    assignees) cmd_assignees "$@" ;;
    views) cmd_views "$@" ;;
    buckets) cmd_buckets "$@" ;;
    webhooks) cmd_webhooks "$@" ;;
    attachments) cmd_attachments "$@" ;;
    relations) cmd_relations "$@" ;;
    filters) cmd_filters "$@" ;;
    notifications) cmd_notifications "$@" ;;
    subscriptions) cmd_subscriptions "$@" ;;
    tokens) cmd_tokens "$@" ;;
    *) die "Unknown command: ${cmd}" 2 ;;
  esac
}

main "$@"
