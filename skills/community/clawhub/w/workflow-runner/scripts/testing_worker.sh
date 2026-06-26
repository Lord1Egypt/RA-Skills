#!/bin/bash
# testing_worker.sh - template for testing subagent
# Inputs: WF_ID, ARTIFACT_PATH
WF_ID="$1"
ARTIFACT_PATH="$2"
WORKDIR="/tmp/${WF_ID}-testing"
mkdir -p "$WORKDIR"
cd "$WORKDIR"
# unpack artifact if provided
if [ -f "$ARTIFACT_PATH" ]; then
  tar -xzf "$ARTIFACT_PATH"
fi
# Run test: execute scripts/hello.sh and check output
OUT=$(./code/scripts/hello.sh 2>&1 || true)
EXPECTED="hello world"
STATUS="pass"
if [ "$OUT" != "$EXPECTED" ]; then
  STATUS="fail"
fi
cat > ../${WF_ID}-test-report.json <<EOF
{ "wfId":"${WF_ID}", "role":"testing", "status":"${STATUS}", "output": $(printf '%s' "${OUT}" | jq -R -s '.' ) }
EOF
echo "Testing finished: ${STATUS}"
