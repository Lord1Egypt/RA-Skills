cmd_delete() {
  local id="${1:-}"
  local force=0
  if [ "$id" = "--force" ]; then
    id="${2:-}"
    force=1
  elif [ "${2:-}" = "--force" ]; then
    force=1
  fi

  [ -z "$id" ] && die "Usage: task delete ID [--force]"
  require_int "$id" "ID"

  local desc
  desc=$(sql "SELECT request_text FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$desc" ] && die "Task #$id not found"

  local sub_count
  sub_count=$(sql "SELECT count(*) FROM tasks WHERE parent_id = $id;")

  if [ "$sub_count" -gt 0 ] && [ "$force" -eq 0 ]; then
    die "Task #$id has $sub_count subtask(s). Use --force to delete."
  fi

  if [ "$sub_count" -gt 0 ]; then
    sql "DELETE FROM dependencies WHERE task_id IN (SELECT id FROM tasks WHERE parent_id = $id)
         OR depends_on_task_id IN (SELECT id FROM tasks WHERE parent_id = $id);"
    sql "DELETE FROM tasks WHERE parent_id = $id;"
    ok "Deleted $sub_count subtask(s)"
  fi

  sql "DELETE FROM dependencies WHERE task_id = $id OR depends_on_task_id = $id;"
  sql "DELETE FROM tasks WHERE id = $id;"
  ok "Deleted task #$id: $desc"
}
