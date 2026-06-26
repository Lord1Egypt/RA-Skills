cmd_block() {
  local id="${1:-}"
  local reason="${2:-}"
  [ -z "$id" ] && die "Usage: task block ID \"reason\""
  require_int "$id" "ID"

  local status
  status=$(sql "SELECT status FROM tasks WHERE id = $id;" 2>/dev/null) || true
  [ -z "$status" ] && die "Task #$id not found"
  [ "$status" = "done" ] && die "Task #$id is already done"

  local safe_reason
  safe_reason=$(printf '%s' "$reason" | sed "s/'/''/g")

  sql "UPDATE tasks SET status = 'blocked',
    notes = CASE WHEN notes IS NULL OR notes = '' THEN 'BLOCKED: $safe_reason'
            ELSE notes || char(10) || 'BLOCKED: $safe_reason' END,
    last_updated = datetime('now')
    WHERE id = $id;"
  ok "Blocked task #$id: $reason"
}
