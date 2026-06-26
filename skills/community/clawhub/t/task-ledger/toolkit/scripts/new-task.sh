#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <slug> <title> [goal] [executionMode] [stagesCsv] [priority] [owner]" >&2
  echo "Example: $0 deploy-api '部署 API 服务' '拉代码、重启并做健康检查' background-process 'pull_code,install_deps,build,restart_service,healthcheck,report' high main" >&2
  exit 1
fi

slug="$1"
title="$2"
goal="${3:-}"
execution_mode="${4:-background-process}"
stages_csv="${5:-prepare,execute,verify}"
priority="${6:-normal}"
owner="${7:-main}"

case "$priority" in
  low|normal|high|urgent) ;;
  *)
    echo "invalid priority: $priority" >&2
    exit 1
    ;;
esac

IFS=',' read -r -a raw_stages <<< "$stages_csv"
stages=()
for s in "${raw_stages[@]}"; do
  trimmed="$(printf '%s' "$s" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
  if [[ -n "$trimmed" ]]; then
    stages+=("$trimmed")
  fi
done

if [[ ${#stages[@]} -eq 0 ]]; then
  echo "stagesCsv must contain at least one non-empty stage" >&2
  exit 1
fi

first_stage="${stages[0]}"
timestamp="$(date +%Y%m%d-%H%M)"
iso_time="$(date +%Y-%m-%dT%H:%M:%S%z | sed 's/\([0-9][0-9]\)$/:\1/')"
task_id="${slug}-${timestamp}"

mkdir -p tasks logs outputs "outputs/${task_id}"
: > "logs/${task_id}.log"

stages_json=""
for stage_id in "${stages[@]}"; do
  if [[ -n "$stages_json" ]]; then
    stages_json+=$'\n    , '
  else
    stages_json+="    "
  fi
  stages_json+="{ \"id\": \"${stage_id}\", \"status\": \"todo\" }"
done

cat > "tasks/${task_id}.json" <<EOF
{
  "taskId": "${task_id}",
  "title": "${title}",
  "goal": "${goal}",
  "status": "pending",
  "priority": "${priority}",
  "createdAt": "${iso_time}",
  "startedAt": null,
  "updatedAt": "${iso_time}",
  "completedAt": null,
  "lastVerifiedAt": null,
  "ownerSession": "main",
  "owner": "${owner}",
  "assignedAgent": null,
  "executionMode": "${execution_mode}",
  "idempotent": true,
  "canResume": true,
  "retryCount": 0,
  "maxRetries": 2,
  "stage": "${first_stage}",
  "stages": [
${stages_json}
  ],
  "dependsOn": [],
  "blockedBy": [],
  "blockedReason": null,
  "nextAction": "Start ${first_stage}",
  "resumeHint": "Verify real state before resuming; do not blindly rerun side effects.",
  "decisionNotes": "",
  "workingSummary": "",
  "artifacts": {
    "logPath": "logs/${task_id}.log",
    "outputDir": "outputs/${task_id}",
    "files": []
  },
  "process": {
    "sessionId": null,
    "pid": null
  },
  "subtask": {
    "sessionKey": null,
    "agentId": null
  },
  "cron": {
    "jobId": null,
    "schedule": null,
    "nextRunAt": null
  },
  "rollback": {
    "available": false,
    "strategy": null,
    "status": "not-applicable",
    "artifacts": []
  },
  "notifications": {
    "notifiedStart": false,
    "notifiedCompletion": false,
    "notifiedRecovery": false
  },
  "events": [
    {
      "ts": "${iso_time}",
      "type": "task.created",
      "message": "Task skeleton created",
      "details": {
        "status": "pending",
        "stage": "${first_stage}",
        "executionMode": "${execution_mode}",
        "stages": "${stages_csv}",
        "priority": "${priority}",
        "owner": "${owner}"
      }
    }
  ],
  "result": null,
  "error": null
}
EOF

echo "Created task skeleton: ${task_id}"
echo "- task: tasks/${task_id}.json"
echo "- log: logs/${task_id}.log"
echo "- output: outputs/${task_id}/"
echo "- stages: ${stages[*]}"
