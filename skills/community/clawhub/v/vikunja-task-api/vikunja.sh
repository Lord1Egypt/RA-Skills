#!/usr/bin/env bash
set -euo pipefail

: "${VIKUNJA_URL:?Set VIKUNJA_URL (base URL or include /api/v1)}"

# Normalize VIKUNJA_URL to include /api/v1
VIKUNJA_URL=${VIKUNJA_URL%/}
case "$VIKUNJA_URL" in
  */api/v1) : ;;
  */api/v1/*) VIKUNJA_URL=${VIKUNJA_URL%%/api/v1*}/api/v1 ;;
  *) VIKUNJA_URL="$VIKUNJA_URL/api/v1" ;;
esac

# Auth:
# - Preferred: set VIKUNJA_TOKEN (JWT or API token starting with tk_)
# - Fallback: set VIKUNJA_USERNAME + VIKUNJA_PASSWORD and we'll request a JWT
: "${VIKUNJA_TOKEN:=}"
: "${VIKUNJA_USERNAME:=}"
: "${VIKUNJA_PASSWORD:=}"

usage() {
  cat <<'EOF'
vikunja.sh - Vikunja CLI helper

Usage:
  vikunja.sh projects              List all projects
  vikunja.sh list --filter '<expr>'  List tasks (default: done=false)
  vikunja.sh overdue              Overdue tasks
  vikunja.sh due-today            Due today
  vikunja.sh show <taskId>        Show task details
  vikunja.sh done <taskId>         Mark task done
  vikunja.sh create <projectId> "<title>"   Create task in project
  vikunja.sh delete <taskId>       Delete task

Environment:
  VIKUNJA_URL      e.g. http://192.168.8.11:3456
  VIKUNJA_TOKEN    JWT or API token (tk_...)
  VIKUNJA_USERNAME Username (fallback)
  VIKUNJA_PASSWORD Password (fallback)

Filter syntax: https://vikunja.io/docs/filters/
EOF
}

ensure_token() {
  if [[ -n "$VIKUNJA_TOKEN" ]]; then
    return 0
  fi

  if [[ -z "$VIKUNJA_USERNAME" || -z "$VIKUNJA_PASSWORD" ]]; then
    echo "Missing auth: set VIKUNJA_TOKEN, or set VIKUNJA_USERNAME + VIKUNJA_PASSWORD" >&2
    exit 2
  fi

  VIKUNJA_TOKEN=$(curl -fsS -X POST "$VIKUNJA_URL/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$VIKUNJA_USERNAME\",\"password\":\"$VIKUNJA_PASSWORD\",\"long_token\":true}" \
    | jq -r '.token // empty')

  if [[ -z "$VIKUNJA_TOKEN" || "$VIKUNJA_TOKEN" == "null" ]]; then
    echo "Login failed: no token returned" >&2
    exit 1
  fi
}

api_get() {
  local path=$1
  ensure_token
  curl -fsS "$VIKUNJA_URL$path" -H "Authorization: Bearer $VIKUNJA_TOKEN"
}

api_put() {
  local path=$1
  local json=${2:-}
  ensure_token
  curl -fsS -X PUT "$VIKUNJA_URL$path" \
    -H "Authorization: Bearer $VIKUNJA_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$json"
}

api_post_json() {
  local path=$1
  local json=${2:-}
  ensure_token

  if [[ "$json" == "@-" ]]; then
    curl -fsS -X POST "$VIKUNJA_URL$path" \
      -H "Authorization: Bearer $VIKUNJA_TOKEN" \
      -H "Content-Type: application/json" \
      -d @-
    return 0
  fi

  curl -fsS -X POST "$VIKUNJA_URL$path" \
    -H "Authorization: Bearer $VIKUNJA_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$json"
}

api_delete() {
  local path=$1
  ensure_token
  curl -fsS -X DELETE "$VIKUNJA_URL$path" -H "Authorization: Bearer $VIKUNJA_TOKEN"
}

urlencode() {
  jq -sRr @uri
}

project_map_json() {
  api_get "/projects" | jq 'map({key:(.id|tostring), value:.title}) | from_entries'
}

format_tasks() {
  local projects_json=$1
  jq -r --argjson projects "$projects_json" '
    def project_icon($name):
      ($name // "") as $n
      | ($n | split(" ")[0]) as $first
      | if ($first | test("^[A-Za-z0-9]")) then "" else $first end;

    def fmt_due($iso):
      if ($iso == null or $iso == "0001-01-01T00:00:00Z") then "(no due)"
      else ($iso | fromdateiso8601 | strftime("%b/%e") | gsub(" "; ""))
      end;

    .[]
    | ($projects[(.project_id|tostring)] // "") as $pname
    | project_icon($pname) as $icon
    | ($icon | if length>0 then . else "🔨" end) as $glyph
    | "\($glyph) \(fmt_due(.due_date)) - #\(.id) \(.title)"
  '
}

list_tasks() {
  local filter=${1:-'done = false'}
  local encoded_filter
  encoded_filter=$(printf %s "$filter" | urlencode)

  local projects
  projects=$(project_map_json)

  # Use GET /tasks (v2 API, not /tasks/all)
  api_get "/tasks?filter=$encoded_filter&sort_by=due_date&order_by=asc" | format_tasks "$projects"
}

cmd=${1:-}
shift || true

case "$cmd" in
  -h|--help|help|"")
    usage
    exit 0
    ;;

  projects)
    ensure_token
    curl -fsS "$VIKUNJA_URL/projects" -H "Authorization: Bearer $VIKUNJA_TOKEN" \
      | jq -r '.[] | "\(.id)\t\(.title)"'
    ;;

  overdue)
    list_tasks 'done = false && due_date < now'
    ;;

  due-today)
    list_tasks 'done = false && due_date >= now/d && due_date < now/d + 1d'
    ;;

  list)
    filter="done = false"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --filter)
          filter=${2:-}
          shift 2
          ;;
        *)
          shift
          ;;
      esac
    done
    list_tasks "$filter"
    ;;

  show)
    task_id=${1:-}
    if [[ -z "$task_id" ]]; then
      echo "Missing task id" >&2
      exit 2
    fi
    api_get "/tasks/$task_id" | jq '{id,title,description,done,done_at,due_date,project_id,repeat_after,priority,created,updated}'
    ;;

  done)
    task_id=${1:-}
    if [[ -z "$task_id" ]]; then
      echo "Missing task id" >&2
      exit 2
    fi
    # Mark done via POST /tasks/{id}
    api_post_json "/tasks/$task_id" '{"done": true}' | jq '{id,title,done,done_at}'
    ;;

  create)
    project_id=${1:-}
    title=${2:-}
    if [[ -z "$project_id" || -z "$title" ]]; then
      echo "Usage: vikunja.sh create <projectId> \"<title>\"" >&2
      exit 2
    fi
    # Create task via PUT /projects/{id}/tasks
    api_put "/projects/$project_id/tasks" "{\"title\":\"$title\",\"description\":\"\",\"due_date\":\"0001-01-01T00:00:00Z\"}" \
      | jq '{id,title,project_id,done,due_date}'
    ;;

  delete)
    task_id=${1:-}
    if [[ -z "$task_id" ]]; then
      echo "Missing task id" >&2
      exit 2
    fi
    api_delete "/tasks/$task_id" | jq
    ;;

  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
