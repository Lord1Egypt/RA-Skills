cmd_edit() {
  local id="${1:-}"
  local desc="" priority="" project="" verify="" assignee="" assignee_set=0 due_date="" tags=""
  shift

  [ -z "$id" ] && die "Usage: task edit ID [--desc=\"new text\"] [--priority=N] [--project=NAME] [--verify=\"cmd\"] [--assignee=\"NAME\"|--unassign] [--due=\"YYYY-MM-DD\"] [--tags=\"a,b\"]"
  require_int "$id" "ID"

  while [ $# -gt 0 ]; do
    case "$1" in
      --desc=*)     desc="${1#*=}" ;;
      --priority=*) priority="${1#*=}" ;;
      --project=*)  project="${1#*=}" ;;
      --verify=*)   verify="${1#*=}" ;;
      --assignee=*) assignee="${1#*=}"; assignee_set=1 ;;
      --unassign)   assignee=""; assignee_set=1 ;;
      --due=*)      due_date="${1#*=}" ;;
      --tags=*)     tags="${1#*=}" ;;
      -*)           die "Unknown flag: $1" ;;
    esac
    shift
  done

  [ -z "$desc" ] && [ -z "$priority" ] && [ -z "$project" ] && [ -z "$verify" ] && [ "$assignee_set" -eq 0 ] && [ -z "$due_date" ] && [ -z "$tags" ] && die "Nothing to edit. Provide --desc, --priority, --project, --verify, --assignee/--unassign, --due, or --tags."

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"

  local updates=""

  if [ -n "$desc" ]; then
    local safe_desc
    safe_desc=$(printf '%s' "$desc" | sed "s/'/''/g")
    updates="request_text = '$safe_desc'"
  fi

  if [ -n "$priority" ]; then
    require_int "$priority" "--priority"
    if [ "$priority" -lt 1 ] || [ "$priority" -gt 10 ]; then
      die "Priority must be 1-10"
    fi
    [ -n "$updates" ] && updates="$updates, "
    updates="${updates}priority = $priority"
  fi

  if [ -n "$project" ]; then
    local safe_proj
    safe_proj=$(printf '%s' "$project" | sed "s/'/''/g")
    [ -n "$updates" ] && updates="$updates, "
    if [ "$project" = "none" ] || [ "$project" = "null" ] || [ "$project" = "NULL" ]; then
        updates="${updates}project = NULL"
    else
        updates="${updates}project = '$safe_proj'"
    fi
  fi

  if [ -n "$verify" ]; then
    local safe_verify
    safe_verify=$(printf '%s' "$verify" | sed "s/'/''/g")
    [ -n "$updates" ] && updates="$updates, "
    if [ "$verify" = "none" ] || [ "$verify" = "null" ] || [ "$verify" = "NULL" ]; then
        updates="${updates}verification_cmd = NULL"
    else
        updates="${updates}verification_cmd = '$safe_verify'"
    fi
  fi
  
  if [ "$assignee_set" -eq 1 ]; then
    [ -n "$updates" ] && updates="$updates, "
    if [ -z "$assignee" ] || [ "$assignee" = "none" ] || [ "$assignee" = "null" ] || [ "$assignee" = "NULL" ]; then
        updates="${updates}assignee = NULL"
    else
        local safe_assignee
        safe_assignee=$(printf '%s' "$assignee" | sed "s/'/''/g")
        updates="${updates}assignee = '$safe_assignee'"
    fi
  fi
  
  if [ -n "$due_date" ]; then
    [ -n "$updates" ] && updates="$updates, "
    if [ "$due_date" = "none" ] || [ "$due_date" = "null" ] || [ "$due_date" = "NULL" ]; then
        updates="${updates}due_date = NULL"
    else
        [[ "$due_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "--due must be in YYYY-MM-DD format"
        local safe_due
        safe_due=$(printf '%s' "$due_date" | sed "s/'/''/g")
        updates="${updates}due_date = '$safe_due'"
    fi
  fi
  
  if [ -n "$tags" ]; then
    [ -n "$updates" ] && updates="$updates, "
    if [ "$tags" = "none" ] || [ "$tags" = "null" ] || [ "$tags" = "NULL" ]; then
        updates="${updates}tags = NULL"
    else
        local safe_tags
        safe_tags=$(printf '%s' "$tags" | sed "s/'/''/g")
        updates="${updates}tags = '$safe_tags'"
    fi
  fi

  sql "UPDATE tasks SET $updates, last_updated = datetime('now') WHERE id = $id;"
  ok "Updated task #$id"
}
