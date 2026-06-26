#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/zqh2333/.openclaw/workspace"
TZ="Asia/Shanghai"
CRON_STORE="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/cron/jobs.json"
cd "$ROOT"

tmp_json="$(mktemp)"
cleanup() {
  rm -f "$tmp_json"
}
trap cleanup EXIT

list_jobs_json_file() {
  if [[ -f "$CRON_STORE" ]]; then
    cp "$CRON_STORE" "$tmp_json"
  else
    printf '{"version":1,"jobs":[]}\n' >"$tmp_json"
  fi
}

find_job_id() {
  local name="$1"
  list_jobs_json_file
  jq -r --arg name "$name" '.jobs[]? | select(.name == $name) | .id' "$tmp_json" | head -n1
}

upsert_job() {
  local name="$1"
  local description="$2"
  local expr="$3"
  local timeout_seconds="$4"
  local message="$5"

  local existing_id
  existing_id="$(find_job_id "$name")"

  if [[ -n "$existing_id" ]]; then
    openclaw cron edit "$existing_id" \
      --name "$name" \
      --description "$description" \
      --cron "$expr" \
      --tz "$TZ" \
      --session isolated \
      --message "$message" \
      --thinking low \
      --timeout-seconds "$timeout_seconds" \
      --tools exec,read \
      --no-deliver \
      --failure-alert \
      --failure-alert-after 1 \
      --failure-alert-cooldown 6h \
      --enable \
      --timeout 10000 </dev/null >/dev/null
    printf '{"action":"updated","id":"%s","name":"%s"}\n' "$existing_id" "$name"
  else
    : >"$tmp_json"
    openclaw cron add --json \
      --name "$name" \
      --description "$description" \
      --cron "$expr" \
      --tz "$TZ" \
      --session isolated \
      --message "$message" \
      --thinking low \
      --timeout-seconds "$timeout_seconds" \
      --tools exec,read \
      --no-deliver \
      --failure-alert \
      --failure-alert-after 1 \
      --failure-alert-cooldown 6h \
      --timeout 10000 </dev/null >"$tmp_json"
    jq -c '{action:"created", id:.id, name:.name}' "$tmp_json"
  fi
}

DAILY_MESSAGE=$(cat <<'EOF'
In /home/zqh2333/.openclaw/workspace, run the Shared Memory OS daily light maintenance. Execute these commands with exec and stop on real errors:
1) node skills/shared-memory-os/scripts/init-shared-memory-os.js
2) node skills/shared-memory-os/scripts/check-memory-health.js > reports/shared-memory/latest-health.json
3) node skills/shared-memory-os/scripts/rebuild-learnings-index.js
4) node skills/shared-memory-os/scripts/record-health-snapshot.js
Then read and briefly summarize latest-health.json and whether INDEX.md was refreshed. Keep the reply concise.
EOF
)

WEEKLY_MESSAGE=$(cat <<'EOF'
In /home/zqh2333/.openclaw/workspace, run the Shared Memory OS weekly maintenance. Execute this command with exec:
node skills/shared-memory-os/scripts/run-shared-memory-maintenance.js
After it completes, read reports/shared-memory/dashboard.md and reports/shared-memory/shared-memory-audit-report.md and provide a concise summary of health score, failed checks, duplicate groups, promotion candidates, and notable next actions.
EOF
)

MONTHLY_MESSAGE=$(cat <<'EOF'
In /home/zqh2333/.openclaw/workspace, run the Shared Memory OS monthly deep maintenance by executing:
node skills/shared-memory-os/scripts/run-shared-memory-maintenance.js
Then read these files if present and summarize the important findings only: reports/shared-memory/shared-memory-stale-durable-memory.json, reports/shared-memory/shared-memory-merge-suggestions.json, reports/shared-memory/shared-memory-skill-upgrade-candidates.json, reports/shared-memory/dashboard.md. Keep the report concise and action-oriented.
EOF
)

results=()
results+=("$(upsert_job 'shared-memory-os daily maintenance' 'Daily shared-memory health check, learnings index rebuild, and light maintenance.' '15 3 * * *' '300' "$DAILY_MESSAGE")")
results+=("$(upsert_job 'shared-memory-os weekly review' 'Weekly shared-memory review for duplicates, promotions, dashboard, and audit artifacts.' '30 3 * * 1' '600' "$WEEKLY_MESSAGE")")
results+=("$(upsert_job 'shared-memory-os monthly deep maintenance' 'Monthly deep shared-memory cleanup and review of stale entries, merge suggestions, and upgrade candidates.' '45 3 1 * *' '600' "$MONTHLY_MESSAGE")")

printf '{\n  "ok": true,\n  "timezone": "%s",\n  "results": [\n    %s\n  ]\n}\n' "$TZ" "$(printf '%s\n' "${results[@]}" | paste -sd ',\n    ' -)"
