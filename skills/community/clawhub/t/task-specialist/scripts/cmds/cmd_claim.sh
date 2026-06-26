#!/bin/bash
# scripts/cmds/cmd_claim.sh
# Swarm Mechanics: Atomically fetches and locks the highest-priority, fully-unblocked task.

cmd_claim() {
  local agent=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --agent=*) agent="${1#*=}" ;;
      -*)        die "Unknown flag: $1" ;;
    esac
    shift
  done

  local safe_agent
  if [ -n "$agent" ]; then
    safe_agent=$(printf "%s" "$agent" | sed "s/'/''/g")
  else
    safe_agent="NULL"
  fi

  # Write the atomic UPDATE ... RETURNING query to a temporary SQL file to prevent injection
  # and allow for multi-line formatting without bash escaping hell.
  local sql_file
  sql_file=$(mktemp)
  
  local set_assignee_clause=""
  if [ "$safe_agent" != "NULL" ]; then
    set_assignee_clause=", assignee = '$safe_agent'"
  fi

  cat << EOF > "$sql_file"
-- Atomic Swarm Lock
UPDATE tasks
SET status = 'in_progress', started_at = datetime('now')$set_assignee_clause, last_updated = datetime('now')
WHERE id = (
    SELECT t.id FROM tasks t
    LEFT JOIN tasks parent ON t.parent_id = parent.id
    WHERE t.status = 'pending'
    AND (parent.id IS NULL OR parent.status NOT IN ('pending', 'blocked'))
    AND NOT EXISTS (
        SELECT 1 FROM dependencies d
        JOIN tasks dep_t on d.depends_on_task_id = dep_t.id
        WHERE d.task_id = t.id AND dep_t.status != 'done'
    )
    ORDER BY t.priority DESC, t.id ASC
    LIMIT 1
)
RETURNING id, request_text, project, priority, assignee;
EOF

  # Execute the atomic lock
  local result
  result=$(sqlite3 "$DB" < "$sql_file")
  rm -f "$sql_file"

  if [[ -z "$result" ]]; then
    printf "%b(No unblocked tasks available to claim)%b\n" "\033[33m" "\033[0m"
    exit 0
  fi

  # The RETURNING clause outputs the locked task natively as "ID|Text|Project|Priority|Assignee"
  IFS='|' read -r claimed_id request project priority assigned_agent <<< "$result"

  printf "%b[Swarm Lock Acquired]%b Successfully claimed Task %b#%s%b\n" "\033[1;32m" "\033[0m" "\033[1;36m" "$claimed_id" "\033[0m"
  printf "  Description : %s\n" "$request"
  printf "  Project     : %s\n" "${project:-(none)}"
  printf "  Priority    : %s\n" "$priority"
  if [ -n "$assigned_agent" ] && [ "$assigned_agent" != "NULL" ]; then
    printf "  Assignee    : %b%s%b\n" "\033[1;34m" "$assigned_agent" "\033[0m"
  fi
  printf "\n%bThis task is now marked 'in_progress'. Use 'task show %s' to read inherited context, and 'task complete %s' when finished.%b\n" "\033[0;90m" "$claimed_id" "$claimed_id" "\033[0m"
}
