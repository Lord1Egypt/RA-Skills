#!/usr/bin/env bash

# Command: task board
# Renders tasks in a 4-column ASCII Kanban board

cmd_board() {
  local data
  data=$(sqlite3 -separator '|' "$DB" "SELECT status, id, request_text, IFNULL(assignee, ''), IFNULL(due_date, ''), IFNULL(tags, '') FROM tasks WHERE status IN ('pending', 'in_progress', 'done', 'blocked') ORDER BY id ASC;")
  
  printf "\n"
  printf " %b%-29s%b| %b%-29s%b| %b%-29s%b| %b%-29s%b\n" "\033[1;33m" "PENDING" "\033[0m" "\033[1;36m" "IN PROGRESS" "\033[0m" "\033[1;32m" "DONE" "\033[0m" "\033[1;31m" "BLOCKED" "\033[0m"
  printf "%s\n" "-------------------------------+------------------------------+------------------------------+------------------------------"
  
  if [ -z "$data" ]; then
    printf " (No tasks on the board)\n\n"
    return 0
  fi

  echo "$data" | awk -F'|' '
    BEGIN {
      col[1] = "pending"
      col[2] = "in_progress"
      col[3] = "done"
      col[4] = "blocked"
    }
    {
      status = $1
      id = $2
      text = $3
      assignee = $4
      due = $5
      tags = $6

      if (assignee != "") {
        text = text " (@" assignee ")"
      }
      if (due != "") {
        text = text " (Due: " due ")"
      }
      if (tags != "") {
        text = text " (" tags ")"
      }

      if (length(text) > 23) {
        text = substr(text, 1, 20) "..."
      }
      
      idx = ++count[status]
      cell[status, idx] = sprintf("[%s] %s", id, text)
    }
    END {
      max_rows = 0
      for (i=1; i<=4; i++) {
        if (count[col[i]] > max_rows) max_rows = count[col[i]]
      }
      
      for (r = 1; r <= max_rows; r++) {
        printf(" ")
        for (i = 1; i <= 4; i++) {
          val = cell[col[i], r]
          if (val == "") {
            printf "%-29s", ""
          } else {
            printf "%-29s", val
          }
          if (i < 4) printf "| "
        }
        printf "\n"
      }
      printf("\n")
    }
  '
}
