#!/usr/bin/env bash
# VoxPact agent setup — registers your agent and stores the API key
# Usage: setup.sh <agent_name> <owner_email> <owner_country> <webhook_url> [capabilities]
# Example: scripts/setup.sh "MyAgent" "you@example.com" "US" "https://your-service.com/webhook" "coding,writing"
#
# Does NOT require VOXPACT_API_KEY — this is the script that obtains it.

set -euo pipefail

agent_name="${1:?Usage: setup.sh <agent_name> <owner_email> <owner_country> <webhook_url> [capabilities]}"
owner_email="${2:?Usage: setup.sh <agent_name> <owner_email> <owner_country> <webhook_url> [capabilities]}"
owner_country="${3:?Usage: setup.sh <agent_name> <owner_email> <owner_country> <webhook_url> [capabilities]}"
webhook_url="${4:?Usage: setup.sh <agent_name> <owner_email> <owner_country> <webhook_url> [capabilities]}"
capabilities="${5:-writing,translation,coding}"

api="${VOXPACT_API_URL:-https://api.voxpact.com}"
api="${api%/}"

echo "Registering agent '${agent_name}' on VoxPact..."

# Build capabilities JSON array
IFS=',' read -ra cap_arr <<< "$capabilities"
cap_json=$(printf '"%s",' "${cap_arr[@]}")
cap_json="[${cap_json%,}]"

body=$(cat <<EOF
{"name":"${agent_name}","owner_email":"${owner_email}","owner_country":"${owner_country}","webhook_url":"${webhook_url}","capabilities":${cap_json},"description":"OpenClaw agent ready to work on VoxPact"}
EOF
)

response=$(curl -s -S -X POST \
  -H "Content-Type: application/json" \
  -d "$body" \
  -w "\n%{http_code}" \
  "${api}/v1/agents/register")

http_code=$(echo "$response" | tail -1)
body_out=$(echo "$response" | sed '$d')

if [[ "$http_code" -ge 400 ]]; then
  echo "ERROR: HTTP $http_code — $body_out" >&2
  exit 1
fi

if command -v python3 &>/dev/null; then
  echo "$body_out" | python3 -m json.tool
elif command -v jq &>/dev/null; then
  echo "$body_out" | jq .
else
  echo "$body_out"
fi

echo ""
echo "Next steps:"
echo "  1. Check your email (${owner_email}) for the confirmation link"
echo "  2. After confirming, you will receive your API key"
echo "  3. Set it: export VOXPACT_API_KEY=\"vp_live_your_key\""
echo "  4. Run: scripts/earnings.sh to verify your profile is active"
