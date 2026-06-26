#!/bin/bash
# spawn_worker.sh - helper to show sessions_spawn parameters (placeholder)
# Usage: ./spawn_worker.sh coding|testing <wf-id>
role="$1"
wf="$2"
if [ -z "$role" ] || [ -z "$wf" ]; then
  echo "Usage: $0 coding|testing <wf-id>"
  exit 1
fi
cat <<EOF
{
  "task": "worker-${role}",
  "label": "${wf}-${role}",
  "runtime": "subagent",
  "mode": "session",
  "thinking": "low",
  "thread": true,
  "runTimeoutSeconds": 3600
}
EOF
