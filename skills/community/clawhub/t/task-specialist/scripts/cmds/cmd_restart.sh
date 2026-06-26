#!/usr/bin/env bash

# Command: task restart <ID>
# Moves a completed or in_progress task back to pending

cmd_restart() {
  local id="${1:-}"
  [ -z "$id" ] && die "Usage: task restart ID"
  require_int "$id" "ID"

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"

  if [ "$status" != "done" ] && [ "$status" != "in_progress" ]; then
    die "Task #$id is currently '$status' (must be 'done' or 'in_progress' to restart)"
  fi

  sql "UPDATE tasks SET status = 'pending', completed_at = NULL, assignee = NULL, last_updated = datetime('now') WHERE id = $id;"
  ok "Task #$id restarted (now pending)"
}
