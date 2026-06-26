cmd_depend() {
  local id="${1:-}"
  local dep_id="${2:-}"
  [ -z "$id" ] && [ -z "$dep_id" ] && die "Usage: task depend ID DEPENDS_ON_ID"
  
  require_int "$id" "ID"
  require_int "$dep_id" "DEPENDS_ON_ID"
  
  [ "$id" -eq "$dep_id" ] && die "Task cannot depend on itself"

  local c1
  c1=$(sql "SELECT count(*) FROM tasks WHERE id = $id;")
  [ "$c1" -eq 0 ] && die "Task #$id not found"
  
  local c2
  c2=$(sql "SELECT count(*) FROM tasks WHERE id = $dep_id;")
  [ "$c2" -eq 0 ] && die "Dependency task #$dep_id not found"

  sql "INSERT OR IGNORE INTO dependencies (task_id, depends_on_task_id) VALUES ($id, $dep_id);"
  sql "UPDATE tasks SET last_updated = datetime('now') WHERE id = $id;"
  
  ok "Task #$id now depends on task #$dep_id"
}
