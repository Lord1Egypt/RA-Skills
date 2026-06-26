#!/usr/bin/env bash

# Command: task unblock <ID>
# Moves a blocked task back to pending

cmd_unblock() {
  local id="${1:-}"
  [ -z "$id" ] && die "Usage: task unblock ID"
  require_int "$id" "ID"

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"

  if [ "$status" != "blocked" ]; then
    die "Task #$id is not blocked (status: $status)"
  fi

  sql "UPDATE tasks SET status = 'pending', last_updated = datetime('now') WHERE id = $id;"
  ok "Task #$id unblocked (now pending)"
}
