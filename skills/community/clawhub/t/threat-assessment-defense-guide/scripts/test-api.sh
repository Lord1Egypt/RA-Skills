#!/bin/bash
# threat-assessment-defense-guide - Quick test script
# Usage: ./test-api.sh
# Requires: TOOLWEB_API_KEY environment variable

set -euo pipefail

API_URL="https://hub.toolweb.in/security/threat-assessment-defense/"

if [ -z "${TOOLWEB_API_KEY:-}" ]; then
  echo "❌ Error: TOOLWEB_API_KEY is not set."
  echo ""
  echo "Get your API key from: https://portal.toolweb.in"
  echo "Then run: export TOOLWEB_API_KEY='your-key-here'"
  exit 1
fi

echo "🛡️ Threat Assessment & Defense Guide — Test Run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "threatOptions": {
      "threat_type": ["Ransomware", "Phishing"],
      "industry": ["Technology"],
      "assets": ["Cloud Infrastructure", "Endpoints"]
    },
    "sessionId": "test-'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "✅ API call successful (HTTP $HTTP_CODE)"
  echo ""
  echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
elif [ "$HTTP_CODE" -eq 401 ]; then
  echo "❌ Authentication failed (HTTP 401). Check your TOOLWEB_API_KEY."
elif [ "$HTTP_CODE" -eq 429 ]; then
  echo "⚠️  Rate limit exceeded (HTTP 429). Wait 60 seconds and retry."
else
  echo "❌ API error (HTTP $HTTP_CODE)"
  echo "$BODY"
fi
