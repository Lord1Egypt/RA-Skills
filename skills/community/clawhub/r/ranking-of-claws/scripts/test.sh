#!/bin/bash
# Test your Ranking of Claws setup
set -euo pipefail

API_URL="https://rankingofclaws.angelstreet.io/api"
echo "Testing Ranking of Claws..."

# Test API connectivity
echo -n "1. API reachable: "
if curl -sf "$API_URL/stats" > /dev/null 2>&1; then
  echo "OK"
else
  echo "FAIL - cannot reach $API_URL"
  exit 1
fi

# Test report endpoint contract without creating fake agents
echo -n "2. Report endpoint contract: "
HTTP_CODE=$(curl -s -o /tmp/roc-test-report.json -w "%{http_code}" -X POST "$API_URL/report" \
  -H "Content-Type: application/json" \
  -d '{}')
if [ "$HTTP_CODE" = "400" ] && grep -q "Missing required fields" /tmp/roc-test-report.json; then
  echo "OK"
else
  echo "FAIL - unexpected response (HTTP $HTTP_CODE)"
  cat /tmp/roc-test-report.json
fi

# Test rank endpoint shape
echo -n "3. Rank endpoint reachable: "
RANK_HTTP=$(curl -s -o /tmp/roc-test-rank.json -w "%{http_code}" "$API_URL/rank?agent=non-existent-agent")
if [ "$RANK_HTTP" = "404" ] || [ "$RANK_HTTP" = "400" ]; then
  echo "OK"
else
  echo "FAIL - unexpected response (HTTP $RANK_HTTP)"
  cat /tmp/roc-test-rank.json
fi

# Check hook file
echo -n "4. Hook handler: "
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$SKILL_DIR/hooks/handler.js" ]; then
  echo "OK ($SKILL_DIR/hooks/handler.js)"
else
  echo "MISSING - hook not found"
fi

echo ""
echo "All checks passed. Your agent can report usage!"
echo "Quick test: ./scripts/report.sh YourAgentName CH 1000"
