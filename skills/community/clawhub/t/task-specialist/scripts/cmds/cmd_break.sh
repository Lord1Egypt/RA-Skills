cmd_break() {
  local parent_id="${1:-}"
  [ -z "$parent_id" ] && die "Usage: task break PARENT_ID \"subtask 1\" \"subtask 2\" ..."
  require_int "$parent_id" "PARENT_ID"
  shift
  [ $# -eq 0 ] && die "Provide at least one subtask description"

  local pstatus
  pstatus=$(sql "SELECT status FROM tasks WHERE id = $parent_id;" 2>/dev/null) || true
  [ -z "$pstatus" ] && die "Parent task #$parent_id not found"

  local parent_priority parent_project
  parent_priority=$(sql "SELECT priority FROM tasks WHERE id = $parent_id;")
  parent_project=$(sql "SELECT project FROM tasks WHERE id = $parent_id;")
  require_int "$parent_priority" "parent_priority"

  local project_val="NULL"
  [ -n "$parent_project" ] && project_val="'$(printf '%s' "$parent_project" | sed "s/'/''/g")'"

  local prev_id=""
  local first_id=""
  local count=0

  for desc in "$@"; do
    local safe_desc
    safe_desc=$(printf '%s' "$desc" | sed "s/'/''/g")
    
    local sub_id
    sub_id=$(sql "INSERT INTO tasks (request_text, project, status, priority, parent_id, created_at, last_updated)
      VALUES ('$safe_desc', $project_val, 'pending', $parent_priority, $parent_id, datetime('now'), datetime('now'));
      SELECT last_insert_rowid();")
    
    require_int "$sub_id" "sub_id"
    [ -z "$first_id" ] && first_id="$sub_id"
    
    if [ -n "$prev_id" ]; then
      sql "INSERT INTO dependencies (task_id, depends_on_task_id) VALUES ($sub_id, $prev_id);"
    fi
    
    echo "  → Created subtask #$sub_id: $desc"
    prev_id="$sub_id"
    count=$((count + 1))
  done

  ok "Decomposed task #$parent_id into $count subtasks (#$first_id → #$prev_id)"
}
