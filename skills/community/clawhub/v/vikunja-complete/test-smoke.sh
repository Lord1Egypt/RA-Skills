#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI="$SCRIPT_DIR/vikunja.sh"

require_env() { [[ -n "${!1:-}" ]] || { echo "missing env: $1" >&2; exit 2; }; }
require_env VIKUNJA_URL
require_env VIKUNJA_TOKEN

health() { "$CLI" health >/dev/null; }

project_id_by_title() {
  local title="$1"
  curl -sS -H "Authorization: Bearer $VIKUNJA_TOKEN" "$VIKUNJA_URL/api/v1/projects" | jq -r --arg t "$title" '.[] | select(.title==$t) | .id' | head -n1
}

ensure_project() {
  local title="$1"
  local id
  id="$(project_id_by_title "$title")"
  if [[ -z "$id" ]]; then
    id="$(curl -sS -X PUT "$VIKUNJA_URL/api/v1/projects" -H "Authorization: Bearer $VIKUNJA_TOKEN" -H 'Content-Type: application/json' -d "{\"title\":\"$title\"}" | jq -r '.id')"
  fi
  echo "$id"
}

health
P1="$(ensure_project "Inbox")"
P2="$(ensure_project "Move Target")"

RUN_TAG="$(date +%s)-$RANDOM"
LABEL_TITLE="smoke-label-${RUN_TAG}"

CREATED="$($CLI create --project-id "$P1" --title "Smoke test ${RUN_TAG}" --due "2026-03-20" --priority 3)"
ID="$(echo "$CREATED" | jq -r '.id')"

"$CLI" update --id "$ID" --title "Smoke test updated" --priority 4 --reminder "2026-03-19" >/dev/null
"$CLI" comments add --task-id "$ID" --comment "smoke comment" >/dev/null
"$CLI" labels create --title "$LABEL_TITLE" --color "#22aa22" >/dev/null
"$CLI" labels add --task-id "$ID" --label "$LABEL_TITLE" >/dev/null
"$CLI" assignees add --task-id "$ID" --user-id 1 >/dev/null
"$CLI" move --id "$ID" --project-id "$P2" >/dev/null
"$CLI" complete --id "$ID" >/dev/null

"$CLI" list --project-id "$P2" --limit 20 | jq -e --argjson id "$ID" 'map(select(.id==$id and .done==true)) | length >= 1' >/dev/null
"$CLI" comments list --task-id "$ID" | jq -e 'length >= 1' >/dev/null
"$CLI" labels list --task-id "$ID" | jq -e --arg lbl "$LABEL_TITLE" 'map(.title) | any(.==$lbl)' >/dev/null

echo "smoke_test=pass task_id=$ID label=$LABEL_TITLE"
