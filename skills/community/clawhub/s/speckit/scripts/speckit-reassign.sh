#!/bin/bash
# speckit-reassign.sh — Reassign a Paperclip issue by role name (no UUID needed)
# Usage: speckit-reassign.sh <issue-id> <role>
# Roles: pm, po, backend, react, flutter, qa, cicd, code-reviewer, cto, ai-researcher, n8n

set -euo pipefail

ISSUE_ID="${1:?Usage: speckit-reassign.sh <issue-id> <role>}"
ROLE="${2:?Usage: speckit-reassign.sh <issue-id> <role>}"

declare -A AGENT_IDS=(
  ["pm"]="ef3f57a9-5405-49d3-bbe2-9e5f86a28c38"
  ["po"]="cd565c91-d71a-4797-a9dc-160175754b8b"
  ["backend"]="165dfd4b-1944-46ba-825c-f4a35e48f93f"
  ["react"]="da69df02-5dc1-4a85-9180-ac13cc23c382"
  ["flutter"]="326f118a-073c-49e7-9339-cbb1c0d88d2c"
  ["qa"]="921d06fb-0f7d-45f8-b179-fd10437f3d65"
  ["cicd"]="8d6ab8a6-61d1-41bc-898c-03b581add6b6"
  ["code-reviewer"]="f3e614be-a4de-4872-9542-60ea2fc97ca2"
  ["cto"]="7e90ab34-fae6-4f75-a37a-0e18eda99391"
  ["ai-researcher"]="4e2cbd08-d6bc-49c4-a375-4638509b1286"
  ["n8n"]="6c85d721-45f4-45e7-9e74-9a636cfe84c5"
)

ROLE_LOWER=$(echo "$ROLE" | tr '[:upper:]' '[:lower:]')
AGENT_ID="${AGENT_IDS[$ROLE_LOWER]:-}"

if [ -z "$AGENT_ID" ]; then
  echo "ERROR: Unknown role '$ROLE'. Valid roles: ${!AGENT_IDS[*]}" >&2
  exit 1
fi

PAPERCLIP_DIR="${PAPERCLIP_WORKSPACE_DIR:-/home/openclaw/.openclaw/workspace/paperclip}"
API_BASE="${PAPERCLIP_API_BASE:-http://localhost:3100}"

echo "Reassigning issue $ISSUE_ID to $ROLE ($AGENT_ID)..."

# Try Paperclip CLI first
if command -v pnpm &>/dev/null && [ -d "$PAPERCLIP_DIR" ]; then
  if cd "$PAPERCLIP_DIR" && pnpm paperclipai issue update "$ISSUE_ID" --assignee-agent-id "$AGENT_ID" --api-base "$API_BASE" 2>&1; then
    echo "✅ Successfully reassigned issue $ISSUE_ID to $ROLE."
    exit 0
  fi
  echo "⚠️ CLI failed, falling back to curl..."
fi

# Fallback to curl
if [ -n "${PAPERCLIP_API_KEY:-}" ] && [ -n "${PAPERCLIP_API_URL:-}" ]; then
  HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" -X PATCH \
    -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"assigneeAgentId\":\"$AGENT_ID\"}" \
    "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID")
  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Successfully reassigned issue $ISSUE_ID to $ROLE (via curl)."
    exit 0
  fi
  echo "❌ curl failed with HTTP $HTTP_CODE." >&2
  exit 1
fi

echo "ERROR: Neither pnpm paperclipai nor PAPERCLIP_API_KEY available." >&2
echo "Set PAPERCLIP_WORKSPACE_DIR or ensure pnpm paperclipai is in PATH." >&2
exit 1
