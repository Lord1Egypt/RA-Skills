#!/usr/bin/env bash
# Setup script for Pura OpenClaw skill.
# Generates an API key and saves it for use.

set -euo pipefail

GATEWAY_URL="${PURA_GATEWAY_URL:-https://api.pura.xyz}"

if [[ -n "${PURA_API_KEY:-}" ]]; then
  echo "✓ PURA_API_KEY already set: ${PURA_API_KEY:0:13}..."
  echo ""
  echo "Testing connection..."
  STATUS=$(curl -s "${GATEWAY_URL}/api/health" 2>/dev/null || echo '{"status":"error"}')
  if echo "$STATUS" | grep -q '"ok"'; then
    echo "✓ Gateway is operational"
  else
    echo "⚠ Gateway returned: $STATUS"
  fi
  exit 0
fi

echo "Generating Pura API key..."
RESPONSE=$(curl -s -X POST "${GATEWAY_URL}/api/keys" \
  -H "Content-Type: application/json" \
  -d '{"label":"openclaw-agent"}')

KEY=$(echo "$RESPONSE" | grep -o '"key":"[^"]*"' | head -1 | cut -d'"' -f4)

if [[ -z "$KEY" ]]; then
  echo "✗ Failed to generate key. Response: $RESPONSE"
  exit 1
fi

echo "✓ Generated key: ${KEY:0:13}..."
echo ""
echo "Set this environment variable to use Pura:"
echo ""
echo "  export PURA_API_KEY=\"$KEY\""
echo ""
echo "Test it:"
echo "  curl -s -X POST ${GATEWAY_URL}/v1/chat/completions \\"
echo "    -H 'Authorization: Bearer $KEY' \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"stream\":false}'"
