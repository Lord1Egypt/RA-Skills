#!/bin/bash
# scripts/cmds/cmd_note.sh
# Swarm Mechanics: Appends an agent's context log to a downstream task permanently.

cmd_note() {
  if [[ $# -lt 2 ]]; then
    die "Usage: task note <ID> \"<context string>\""
  fi

  local id="$1"
  shift
  local raw_note="$*"

  require_int "$id" "Task ID"

  # Sanitize the input note string to prevent SQLite injection
  local safe_note
  safe_note=$(printf "%s" "$raw_note" | sed "s/'/''/g")

  # Write the UPDATE statement to safely append the note with a localized timestamp.
  # COALESCE ensures that if notes is NULL, we don't end up appending to nothing.
  local sql_file
  sql_file=$(mktemp)
  
  cat << EOF > "$sql_file"
UPDATE tasks
SET notes = ltrim(COALESCE(notes, '') || char(10) || '[' || datetime('now', 'localtime') || '] Agent Note: ' || '$safe_note', char(10)),
    last_updated = datetime('now')
WHERE id = $id;
EOF

  sql "$(cat "$sql_file")" || die "Failed to append context note to task $id"
  rm -f "$sql_file"

  ok "Context note persistently attached to Task #$id."
}
