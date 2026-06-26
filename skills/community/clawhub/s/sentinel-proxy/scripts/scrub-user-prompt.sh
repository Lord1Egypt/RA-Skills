#!/usr/bin/env bash
# UserPromptSubmit — scrub inbound user messages before the agent processes them.
#
# Reads OpenClaw hook envelope from stdin.
# Exits 0 (optionally with modified JSON) to allow; exits 1 to block.
set -euo pipefail

SENTINEL_API_URL="${SENTINEL_API_URL:-https://sentinel.ircnet.us}"
SENTINEL_KEY="${SENTINEL_KEY:-}"
SENTINEL_TIER="${SENTINEL_TIER:-standard}"

input=$(cat)

# Pass through if Sentinel not configured
if [[ -z "$SENTINEL_KEY" ]]; then
  exit 0
fi

content=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('metadata', {}).get('userPrompt') or '')
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
  -d "$payload" 2>/dev/null) || exit 0  # unreachable → pass through

action=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['security']['action_taken'])" 2>/dev/null || echo "clean")
safe_payload=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['safe_payload'])" 2>/dev/null || echo "$content")
threat_score=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['security']['threat_score'])" 2>/dev/null || echo "0")

case "$action" in
  blocked)
    echo "[sentinel] BLOCKED user prompt (threat_score=${threat_score})" >&2
    exit 1
    ;;
  neutralized)
    echo "[sentinel] Neutralized user prompt (threat_score=${threat_score})" >&2
    # Return modified envelope with safe prompt
    echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
d.setdefault('metadata', {})['userPrompt'] = sys.argv[1]
print(json.dumps(d))
" "$safe_payload"
    ;;
  flagged)
    echo "[sentinel] Flagged user prompt (threat_score=${threat_score}) — passing through" >&2
    ;;
esac
