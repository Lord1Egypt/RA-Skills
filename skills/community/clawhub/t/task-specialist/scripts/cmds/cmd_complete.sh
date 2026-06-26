cmd_complete() {
  local id="${1:-}"
  [ -z "$id" ] && die "Usage: task complete ID"
  require_int "$id" "ID"

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"
  [ "$status" = "done" ] && die "Task #$id is already complete"

  # Safety: Cannot complete parent if subtasks are pending
  local blocking_subs
  blocking_subs=$(sql "SELECT id || ': ' || request_text FROM tasks WHERE parent_id = $id AND status != 'done';")
  if [ -n "$blocking_subs" ]; then
    warn "Cannot complete task #$id — pending subtasks:"
    echo "$blocking_subs" | while IFS= read -r line; do
      printf '  → %s\n' "$line"
    done
    exit 1
  fi

  local verify_cmd
  verify_cmd=$(sql "SELECT verification_cmd FROM tasks WHERE id = $id;" 2>/dev/null) || true
  
  if [ -n "$verify_cmd" ]; then
    printf '\033[1;33mManual Checkpoint Required:\033[0m %s\n' "$verify_cmd"
    printf '\033[1;34mNote:\033[0m Auto-execution disabled for security (RCE prevention).\n'
  fi

  sql "UPDATE tasks SET status = 'done', completed_at = datetime('now'), last_updated = datetime('now'), started_at = COALESCE(started_at, datetime('now')) WHERE id = $id;"
  ok "Completed task #$id"

  # Auto-unblock dependents
  local dependents
  dependents=$(sql "SELECT DISTINCT d.task_id FROM dependencies d
    WHERE d.depends_on_task_id = $id;")
  
  if [ -n "$dependents" ]; then
    while IFS= read -r dep_id; do
      require_int "$dep_id" "dep_id"
      local unfinished
      unfinished=$(sql "SELECT count(*) FROM dependencies d
        JOIN tasks t ON t.id = d.depends_on_task_id
        WHERE d.task_id = $dep_id AND t.status != 'done';")
      
      if [ "$unfinished" -eq 0 ]; then
        local dep_status
        dep_status=$(sql "SELECT status FROM tasks WHERE id = $dep_id;")
        if [ "$dep_status" = "blocked" ]; then
          sql "UPDATE tasks SET status = 'pending', last_updated = datetime('now') WHERE id = $dep_id;"
          ok "Auto-unblocked task #$dep_id (all dependencies satisfied)"
        fi
      fi
    done <<< "$dependents"
  fi
}
