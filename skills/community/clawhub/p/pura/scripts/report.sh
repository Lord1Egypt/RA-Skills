#!/usr/bin/env bash
# Pura cost report — shows 24h spend breakdown and income.

set -euo pipefail

GATEWAY_URL="${PURA_GATEWAY_URL:-https://api.pura.xyz}"

if [[ -z "${PURA_API_KEY:-}" ]]; then
  echo "PURA_API_KEY not set. Run: bash scripts/setup.sh"
  exit 1
fi

echo "=== COST REPORT (24h) ==="
curl -s "${GATEWAY_URL}/api/report" \
  -H "Authorization: Bearer ${PURA_API_KEY}" | python3 -m json.tool 2>/dev/null || \
curl -s "${GATEWAY_URL}/api/report" \
  -H "Authorization: Bearer ${PURA_API_KEY}"

echo ""
echo "=== INCOME STATEMENT ==="
curl -s "${GATEWAY_URL}/api/income" \
  -H "Authorization: Bearer ${PURA_API_KEY}" | python3 -m json.tool 2>/dev/null || \
curl -s "${GATEWAY_URL}/api/income" \
  -H "Authorization: Bearer ${PURA_API_KEY}"
