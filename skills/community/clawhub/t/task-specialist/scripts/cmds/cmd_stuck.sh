cmd_stuck() {
  local stuck
  stuck=$(sql "SELECT id || ': ' || request_text 
    FROM tasks 
    WHERE status != 'done' 
    AND last_updated < datetime('now', '-7 days')
    ORDER BY last_updated ASC;")
  
  if [ -z "$stuck" ]; then
    ok "No stuck tasks found"
  else
    warn "Tasks not updated in 7+ days:"
    echo "$stuck" | while IFS= read -r line; do printf '  - %s\n' "$line"; done
  fi
}
