#!/usr/bin/env bash
# PostToolUse — scrub toolResponse before it's returned to the agent.
# Primary defense against malicious Clawhub skills that craft tool responses
# containing prompt injection or agent hijack payloads.
#
# Reads OpenClaw hook envelope from stdin.
# Exits 0 (optionally with modified JSON) to allow; exits 1 to block.
set -euo pipefail

SENTINEL_API_URL="${SENTINEL_API_URL:-https://sentinel.ircnet.us}"
SENTINEL_KEY="${SENTINEL_KEY:-}"
SENTINEL_TIER="${SENTINEL_TIER:-standard}"

input=$(cat)

if [[ -z "$SENTINEL_KEY" ]]; then
  exit 0
fi

tool_name=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('toolName','unknown'))" 2>/dev/null || echo "unknown")
content=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tool_response = d.get('toolResponse')
if tool_response is None:
    print('')
elif isinstance(tool_response, str):
    print(tool_response)
else:
    print(json.dumps(tool_response))
" 2>/dev/null)

if [[ -z "$content" ]]; then
  exit 0
fi

payload=$(python3 -c "
import json, sys
print(json.dumps({'content': sys.argv[1], 'tier': sys.argv[2]}))
" "$content" "$SENTINEL_TIER")

response=$(curl -sf \
  -X POST "${SENTINEL_API_URL}/v1/scrub" \
  -H "X-Sentinel-Key: ${SENTINEL_KEY}" \
  -H "Content-Type: application/json" \
  -d "$payload" 2>/dev/null) || exit 0

action=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['security']['action_taken'])" 2>/dev/null || echo "clean")
safe_payload=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['safe_payload'])" 2>/dev/null || echo "$content")
threat_score=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['security']['threat_score'])" 2>/dev/null || echo "0")

case "$action" in
  blocked)
    echo "[sentinel] BLOCKED tool response from '${tool_name}' — malicious content detected (threat_score=${threat_score})" >&2
    exit 1
    ;;
  neutralized)
    echo "[sentinel] Neutralized tool response from '${tool_name}' (threat_score=${threat_score})" >&2
    echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
d['toolResponse'] = sys.argv[1]
print(json.dumps(d))
" "$safe_payload"
    ;;
  flagged)
    echo "[sentinel] Flagged tool response from '${tool_name}' (threat_score=${threat_score}) — passing through" >&2
    ;;
esac
