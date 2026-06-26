#!/usr/bin/env bash
# PreToolUse — scan toolInput before the agent sends it to an external tool.
# Primary defense against data exfiltration: catches the agent trying to send
# sensitive data outbound to a malicious skill before it leaves the session.
#
# Reads OpenClaw hook envelope from stdin.
# Exits 0 to allow the tool call; exits 1 to block it.
set -euo pipefail

SENTINEL_API_URL="${SENTINEL_API_URL:-https://sentinel.ircnet.us}"
SENTINEL_KEY="${SENTINEL_KEY:-}"
SENTINEL_TIER="${SENTINEL_TIER:-standard}"

input=$(cat)

if [[ -z "$SENTINEL_KEY" ]]; then
  exit 0
fi

# Serialize toolInput as JSON string for scrubbing
tool_name=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('toolName','unknown'))" 2>/dev/null || echo "unknown")
content=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tool_input = d.get('toolInput', {})
# Serialize the full toolInput so Sentinel sees all parameters
print(json.dumps(tool_input))
" 2>/dev/null)

if [[ -z "$content" || "$content" == "{}" ]]; then
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
threat_score=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['security']['threat_score'])" 2>/dev/null || echo "0")

case "$action" in
  blocked|neutralized)
    # For outbound tool calls, block on both blocked AND neutralized —
    # we can't safely reconstruct a modified toolInput from a neutralized string.
    echo "[sentinel] BLOCKED outbound tool call '${tool_name}' — possible data exfiltration (action=${action}, threat_score=${threat_score})" >&2
    exit 1
    ;;
  flagged)
    echo "[sentinel] Flagged outbound tool call '${tool_name}' (threat_score=${threat_score}) — passing through" >&2
    ;;
esac
