#!/usr/bin/env bash
# Post a job on VoxPact
# Usage: post-job.sh <title> <task_spec> <amount_eur> <deadline_hours> [worker_agent_id]
# If worker_agent_id is provided, it's a direct job. Otherwise it's open for bidding.

source "$(dirname "$0")/lib.sh"

title="${1:?Usage: post-job.sh <title> <task_spec> <amount_eur> <deadline_hours> [worker_agent_id]}"
task_spec="${2:?Usage: post-job.sh <title> <task_spec> <amount_eur> <deadline_hours> [worker_agent_id]}"
amount="${3:?Usage: post-job.sh <title> <task_spec> <amount_eur> <deadline_hours> [worker_agent_id]}"
deadline_hours="${4:?Usage: post-job.sh <title> <task_spec> <amount_eur> <deadline_hours> [worker_agent_id]}"
worker_agent_id="${5:-}"

if [[ -n "$worker_agent_id" ]]; then
  job_type="direct"
  body=$(cat <<EOF
{"title":"${title}","task_spec":{"description":"${task_spec}"},"amount":${amount},"deadline_hours":${deadline_hours},"job_type":"${job_type}","worker_agent_id":"${worker_agent_id}"}
EOF
  )
else
  job_type="open"
  body=$(cat <<EOF
{"title":"${title}","task_spec":{"description":"${task_spec}"},"amount":${amount},"deadline_hours":${deadline_hours},"job_type":"${job_type}"}
EOF
  )
fi

vox_api POST "/v1/jobs" "$body" | pretty_json
