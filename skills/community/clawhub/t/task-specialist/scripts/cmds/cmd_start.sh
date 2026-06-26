cmd_start() {
  local id="${1:-}"
  [ -z "$id" ] && die "Usage: task start ID"
  require_int "$id" "ID"

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"
  [ "$status" = "done" ] && die "Task #$id is already done"
  [ "$status" = "in_progress" ] && die "Task #$id is already in progress"

  local blocking
  blocking=$(sql "SELECT d.depends_on_task_id || ': ' || t.request_text
    FROM dependencies d
    JOIN tasks t ON t.id = d.depends_on_task_id
    WHERE d.task_id = $id AND t.status != 'done';")

  if [ -n "$blocking" ]; then
    warn "Cannot start task #$id — blocked by unfinished dependencies:"
    echo "$blocking" | while IFS= read -r line; do
      printf '  → %s\n' "$line"
    done
    exit 1
  fi

  sql "UPDATE tasks SET status = 'in_progress', started_at = datetime('now'), last_updated = datetime('now') WHERE id = $id;"
  ok "Started task #$id"
}
