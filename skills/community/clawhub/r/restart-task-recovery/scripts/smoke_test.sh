#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WS="$(cd "$ROOT/../.." && pwd)"
TMPDIR="${TMPDIR:-/tmp}"

mkdir -p "$WS/tmp"
cat > "$WS/tmp/session-snapshot.json" <<'JSON'
{
  "sessions": [
    {
      "sessionKey": "agent:engineer:main",
      "agentId": "engineer",
      "goal": "Regression verify",
      "lastDone": "401/idempotency/timezone passed",
      "nextStep": "Publish acceptance summary",
      "blockers": "none"
    },
    {
      "sessionKey": "agent:qa:main",
      "agentId": "qa",
      "goal": "Run retention checks",
      "lastDone": "Case set loaded",
      "nextStep": "Retry write results to report",
      "blockers": "none"
    }
  ]
}
JSON

STAMP_DATE="$(date +%F)"
STAMP_TIME="$(date +%H%M%S)"
CP="$WS/memory/restart-checkpoints/$STAMP_DATE/$STAMP_TIME.md"

cat "$WS/tmp/session-snapshot.json" | python3 "$ROOT/scripts/build_checkpoint.py" "$CP" >/dev/null
python3 "$ROOT/scripts/recover_from_latest_checkpoint.py" "$CP" > "$TMPDIR/recover-actions.json"
python3 "$ROOT/scripts/pre_resume_verify.py" "$TMPDIR/recover-actions.json" "$TMPDIR/recover-verified.json" >/dev/null
python3 "$ROOT/scripts/execute_verified_recovery.py" "$TMPDIR/recover-verified.json" > "$TMPDIR/recover-exec.json"

echo "=== Smoke Test Done ==="
echo "checkpoint: $CP"
echo "actions:    $TMPDIR/recover-actions.json"
echo "verified:   $TMPDIR/recover-verified.json"
echo "exec-plan:  $TMPDIR/recover-exec.json"

echo
echo "Summary:"
python3 - <<'PY'
import json, os
p=os.environ.get('TMPDIR','/tmp')
with open(f"{p}/recover-exec.json","r",encoding='utf-8') as f:
    d=json.load(f)
print(f"- sendActions: {len(d.get('sendActions',[]))}")
print(f"- holdForManualConfirm: {len(d.get('holdForManualConfirm',[]))}")
PY
