cmd_show() {
  local id="${1:-}"
  [ -z "$id" ] && die "Usage: task show ID"
  require_int "$id" "ID"

  local exists
  exists=$(sql "SELECT count(*) FROM tasks WHERE id = $id;")
  [ "$exists" -eq 0 ] && die "Task #$id not found"

  echo "── Task #$id ───────────────────────────────────"
  sqlite3 -batch "$DB" "SELECT
      'Task:        ' || '[\033[1;36m' || id || '\033[0m] ' || request_text || char(10) ||
      'Status:      ' || status || char(10) ||
      'Project:     ' || IFNULL(project, 'none') || char(10) ||
      'Assignee:    ' || IFNULL(assignee, 'none') || char(10) ||
      'Due Date:    ' || IFNULL(due_date, 'none') || char(10) ||
      'Tags:        ' || IFNULL(tags, 'none') || char(10) ||
      'Verify Cmd:  ' || IFNULL(verification_cmd, 'none') || char(10) ||
      'Priority:    ' || priority || char(10) ||
      'Parent ID:   ' || IFNULL(parent_id, 'none') || char(10) ||
      'Created:     ' || created_at || char(10) ||
      'Started:     ' || IFNULL(started_at, '-') || char(10) ||
      'Completed:   ' || IFNULL(completed_at, '-') || char(10) ||
      'Updated:     ' || last_updated
      FROM tasks WHERE id = $id;"

  local notes
  notes=$(sql "SELECT notes FROM tasks WHERE id = $id;")
  if [ -n "$notes" ]; then
    echo ""
    echo "── Notes ────────────────────────────────────────"
    echo "$notes"
  fi

  local deps
  deps=$(sql "SELECT d.depends_on_task_id || ' (' || t.status || '): ' || substr(t.request_text, 1, 40)
    FROM dependencies d
    JOIN tasks t ON t.id = d.depends_on_task_id
    WHERE d.task_id = $id;")
  if [ -n "$deps" ]; then
    echo ""
    echo "── Depends On ───────────────────────────────────"
    echo "$deps" | while IFS= read -r line; do printf '  - %s\n' "$line"; done
  fi

  local subs
  subs=$(sql "SELECT id || ' (' || status || '): ' || substr(request_text, 1, 40) FROM tasks WHERE parent_id = $id;")
  if [ -n "$subs" ]; then
    echo ""
    echo "── Subtasks ─────────────────────────────────────"
    echo "$subs" | while IFS= read -r line; do printf '  - %s\n' "$line"; done
  fi
}
