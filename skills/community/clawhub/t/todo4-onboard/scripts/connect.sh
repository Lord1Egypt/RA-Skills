#!/usr/bin/env bash
set -euo pipefail

# Todo4 Onboarding — Step 3: Connect agent and write MCP config
# Calls POST /auth/agent-connect with the user's access token.
# Writes MCP config to ~/.openclaw/mcp_config.json and stores agent token in ~/.openclaw/.env.
# Exit codes: 0 = success, 1 = server/network error, 2 = validation/client error

if [ $# -lt 1 ]; then
  echo '{"error":"missing_argument","message":"Usage: connect.sh <access_token> [agent_name]"}' >&2
  exit 2
fi

if [ -z "${HOME:-}" ]; then
  echo '{"error":"env_missing","message":"HOME is not set"}' >&2
  exit 2
fi

ACCESS_TOKEN="$1"
AGENT_NAME="${2:-OpenClaw}"
API_URL="https://todo4.io/api/v1"

JSON_BODY=$(jq -n --arg name "$AGENT_NAME" '{"agentName": $name, "agentPlatform": "openclaw"}')

RESPONSE=$(curl -s -w "\n%{http_code}" --fail-with-body \
  -X POST "${API_URL}/auth/agent-connect" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d "$JSON_BODY" 2>&1) || true

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  200|201)
    ;;
  401)
    echo "$BODY" | jq . >&2 2>/dev/null || echo "$BODY" >&2
    exit 2
    ;;
  422)
    echo "$BODY" | jq . >&2 2>/dev/null || echo "$BODY" >&2
    exit 2
    ;;
  429)
    echo "$BODY" | jq . >&2
    exit 2
    ;;
  *)
    echo "$BODY" | jq . >&2 2>/dev/null || echo "$BODY" >&2
    exit 1
    ;;
esac

# ── Extract tokens and config from response ──────────────────────────────────

AGENT_TOKEN=$(echo "$BODY" | jq -r '.data.agentAccessToken')
MCP_SNIPPET=$(echo "$BODY" | jq -c '.data.mcpConfigSnippet')

if [ -z "$AGENT_TOKEN" ] || [ "$AGENT_TOKEN" = "null" ]; then
  echo '{"error":"parse_error","message":"Could not extract agentAccessToken from response"}' >&2
  exit 1
fi

if [ -z "$MCP_SNIPPET" ] || [ "$MCP_SNIPPET" = "null" ]; then
  echo '{"error":"parse_error","message":"Could not extract mcpConfigSnippet from response"}' >&2
  exit 1
fi

# ── Write/merge MCP config ───────────────────────────────────────────────────

MCP_CONFIG="${HOME}/.openclaw/mcp_config.json"

if [ -f "$MCP_CONFIG" ]; then
  # Deep-merge: add/replace mcpServers.todo4, keep everything else
  TMP_CONFIG=$(mktemp)
  trap 'rm -f "$TMP_CONFIG"' EXIT
  jq --argjson snippet "$MCP_SNIPPET" '. * $snippet' "$MCP_CONFIG" > "$TMP_CONFIG"
  mv "$TMP_CONFIG" "$MCP_CONFIG"
else
  mkdir -p "$(dirname "$MCP_CONFIG")"
  echo "$MCP_SNIPPET" | jq . > "$MCP_CONFIG"
fi

# ── Store agent token in ~/.openclaw/.env ────────────────────────────────────

ENV_FILE="${HOME}/.openclaw/.env"
mkdir -p "$(dirname "$ENV_FILE")"

if [ -f "$ENV_FILE" ]; then
  # Remove existing TODO4_AGENT_TOKEN line (portable: no sed -i differences)
  TMP_ENV=$(mktemp)
  grep -v "^TODO4_AGENT_TOKEN=" "$ENV_FILE" > "$TMP_ENV" || true
  mv "$TMP_ENV" "$ENV_FILE"
fi

echo "TODO4_AGENT_TOKEN=${AGENT_TOKEN}" >> "$ENV_FILE"

# ── Output success ───────────────────────────────────────────────────────────
#
# Emit the one-time web login URL (if the API included it) so the skill can
# offer the user a click-through link that lands in the authenticated web app.
# The URL is a 5-minute, single-use auth code — safe to display in chat once.
# Full response body is intentionally NOT echoed (would leak the agent token).

WEB_LOGIN_URL=$(echo "$BODY" | jq -r '.data.webLoginUrl // empty')
if [ -n "$WEB_LOGIN_URL" ]; then
  echo "WEB_LOGIN_URL=${WEB_LOGIN_URL}"
fi

exit 0
