#!/usr/bin/env bash

set -euo pipefail

run_tasks_tests() {
  if skip "tasks"; then
    echo "==> tasks (skipped)"
    return 0
  fi

  run_required "tasks" "tasks lists list" gog tasks lists list --json --max 1 >/dev/null

  local created_list_json created_list_id list_json list_id
  echo "==> tasks lists create"
  created_list_json=$(gog tasks lists create "gogcli-smoke-$TS" --json)
  created_list_id=$(extract_id "$created_list_json")
  [ -n "$created_list_id" ] || { echo "Failed to parse task list id" >&2; exit 1; }
  list_id="$created_list_id"

  run_required "tasks" "tasks list" gog tasks list "$list_id" --json --max 1 >/dev/null

  local task_json task_id
  task_json=$(gog tasks add "$list_id" --title "gogcli-smoke-$TS" --due "$DAY1" --json)
  task_id=$(extract_id "$task_json")
  [ -n "$task_id" ] || { echo "Failed to parse task id" >&2; exit 1; }

  run_required "tasks" "tasks get" gog tasks get "$list_id" "$task_id" --json >/dev/null
  run_required "tasks" "tasks update" gog tasks update "$list_id" "$task_id" --title "gogcli-smoke-updated-$TS" --json >/dev/null
  run_required "tasks" "tasks done" gog tasks done "$list_id" "$task_id" --json >/dev/null
  run_required "tasks" "tasks undo" gog tasks undo "$list_id" "$task_id" --json >/dev/null
  run_required "tasks" "tasks delete" gog tasks delete "$list_id" "$task_id" --force >/dev/null

  local repeat_json repeat_ids
  repeat_json=$(gog tasks add "$list_id" --title "gogcli-smoke-repeat-$TS" --due "$DAY1" --repeat daily --repeat-count 2 --json)
  repeat_ids=$(extract_task_ids "$repeat_json")
  [ -n "$repeat_ids" ] || { echo "Failed to parse repeat task ids" >&2; exit 1; }
  while IFS= read -r tid; do
    [ -n "$tid" ] && run_required "tasks" "tasks delete repeat" gog tasks delete "$list_id" "$tid" --force >/dev/null
  done <<<"$repeat_ids"

  local done_json done_id
  done_json=$(gog tasks add "$list_id" --title "gogcli-smoke-done-$TS" --due "$DAY1" --json)
  done_id=$(extract_id "$done_json")
  [ -n "$done_id" ] || { echo "Failed to parse done task id" >&2; exit 1; }
  run_required "tasks" "tasks done (for clear)" gog tasks done "$list_id" "$done_id" --json >/dev/null
  run_required "tasks" "tasks clear" gog --force tasks clear "$list_id" --json >/dev/null
}
