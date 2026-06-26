cmd_create() {
  local desc="" priority="" parent="" project="" verify="" due_date="" tags=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --priority=*) priority="${1#*=}" ;;
      --parent=*)   parent="${1#*=}" ;;
      --project=*)  project="${1#*=}" ;;
      --verify=*)   verify="${1#*=}" ;;
      --due=*)      due_date="${1#*=}" ;;
      --tags=*)     tags="${1#*=}" ;;
      -*)           die "Unknown flag: $1" ;;
      *)            desc="$1" ;;
    esac
    shift
  done

  [ -z "$desc" ] && die "Usage: task create \"description\" [--priority=N] [--parent=ID] [--project=NAME] [--verify=\"cmd\"] [--due=\"YYYY-MM-DD\"] [--tags=\"a,b\"]"

  if [ -n "$parent" ]; then
    require_int "$parent" "--parent"
  fi

  if [ -n "$parent" ] && [ -z "$priority" ]; then
    priority=$(sql "SELECT priority FROM tasks WHERE id = $parent;")
  elif [ -z "$priority" ]; then
    priority=5
  fi

  require_int "$priority" "--priority"
  if [ "$priority" -lt 1 ] || [ "$priority" -gt 10 ]; then
    die "Priority must be 1-10"
  fi

  if [ -n "$parent" ]; then
    local pcount
    pcount=$(sql "SELECT count(*) FROM tasks WHERE id = $parent;")
    [ "$pcount" -eq 0 ] && die "Parent task $parent does not exist"
  fi

  local parent_val="NULL"
  [ -n "$parent" ] && parent_val="$parent"
  
  local project_val="NULL"
  [ -n "$project" ] && project_val="'$(printf '%s' "$project" | sed "s/'/''/g")'"

  local safe_desc
  safe_desc=$(printf '%s' "$desc" | sed "s/'/''/g")

  local verify_val="NULL"
  [ -n "$verify" ] && verify_val="'$(printf '%s' "$verify" | sed "s/'/''/g")'"
  
  local due_val="NULL"
  if [ -n "$due_date" ]; then
    [[ "$due_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "--due must be in YYYY-MM-DD format"
    due_val="'$(printf '%s' "$due_date" | sed "s/'/''/g")'"
  fi
  
  local tags_val="NULL"
  [ -n "$tags" ] && tags_val="'$(printf '%s' "$tags" | sed "s/'/''/g")'"

  local task_id
  task_id=$(sql "INSERT INTO tasks (request_text, project, status, priority, parent_id, verification_cmd, due_date, tags, created_at, last_updated)
    VALUES ('$safe_desc', $project_val, 'pending', $priority, $parent_val, $verify_val, $due_val, $tags_val, datetime('now'), datetime('now'));
    SELECT last_insert_rowid();")

  ok "Created task #$task_id: $desc (priority=$priority${project:+, project=$project}${due_date:+, due=$due_date}${tags:+, tags=$tags})"
  echo "$task_id"
}
