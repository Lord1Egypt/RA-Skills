#!/usr/bin/env bash
# End-to-end verification for the Pura OpenClaw skill.
# Generates a key if needed, sends a real inference request, prints the result.

set -euo pipefail

GATEWAY_URL="${PURA_GATEWAY_URL:-https://api.pura.xyz}"

# 1. Ensure we have an API key
if [[ -z "${PURA_API_KEY:-}" ]]; then
  echo "No PURA_API_KEY set. Generating one..."
  RESPONSE=$(curl -s -X POST "${GATEWAY_URL}/api/keys" \
    -H "Content-Type: application/json" \
    -d '{"label":"openclaw-verify"}')

  PURA_API_KEY=$(echo "$RESPONSE" | grep -o '"key":"[^"]*"' | head -1 | cut -d'"' -f4)

  if [[ -z "$PURA_API_KEY" ]]; then
    echo "✗ Failed to generate key. Response: $RESPONSE"
    exit 1
  fi
  echo "✓ Generated key: ${PURA_API_KEY:0:13}..."
  echo ""
  echo "  export PURA_API_KEY=\"$PURA_API_KEY\""
  echo ""
fi

# 2. Health check
echo "Checking gateway health..."
HEALTH=$(curl -s "${GATEWAY_URL}/api/health" 2>/dev/null || echo '{"status":"error"}')
if echo "$HEALTH" | grep -q '"ok"'; then
  echo "✓ Gateway is operational"
else
  echo "✗ Gateway health check failed: $HEALTH"
  exit 1
fi

# 3. Send a real inference request
echo ""
echo "Sending inference request..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
  -H "Authorization: Bearer $PURA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Reply with exactly: pong"}],"stream":false}')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "✓ Inference succeeded (HTTP $HTTP_CODE)"
else
  echo "✗ Inference failed (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi

# 4. Extract and display key fields
CONTENT=$(echo "$BODY" | grep -o '"content":"[^"]*"' | head -1 | cut -d'"' -f4)
MODEL=$(echo "$BODY" | grep -o '"model":"[^"]*"' | head -1 | cut -d'"' -f4)

echo ""
echo "Response: $CONTENT"
echo "Model:    $MODEL"

echo ""
echo "✓ Pura skill is working. Your agent can route LLM calls through ${GATEWAY_URL}/v1"
