#!/usr/bin/env bash
# Example: Daily health + treasury summary
# Usage: bash examples/daily-summary.sh
# Requires: ZK_BANKIR_HOST (default: http://localhost:3000)

ZK_BANKIR_HOST="${ZK_BANKIR_HOST:-http://localhost:3000}"

echo "=== ZK-Bankir Daily Summary ==="
echo "Time: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo ""

# 1. Health check
echo "--- Health ---"
HEALTH=$(curl -s "$ZK_BANKIR_HOST/health" -H "Accept: application/json" 2>/dev/null)
if echo "$HEALTH" | jq -e '.status == "ok"' > /dev/null 2>&1; then
  echo "✅ Server: ONLINE"
else
  echo "❌ Server: OFFLINE or unreachable"
  exit 1
fi

# 2. Treasury balances
echo ""
echo "--- Treasury Balances ---"
BALANCES=$(curl -s "$ZK_BANKIR_HOST/api/v1/treasury/balances" -H "Accept: application/json" 2>/dev/null)
if [ -n "$BALANCES" ] && echo "$BALANCES" | jq -e '.btc' > /dev/null 2>&1; then
  echo "$BALANCES" | jq -r '
    "BTC:   \(.btc.balance) [\(.btc.vault // "watch-only")]",
    "PUSD:  \(.pusd.balance) [\(.pusd.chain // "Payy")]",
    "Total: $\(.total_usd.total) USD (BTC @ $\(.total_usd.btc_price_usd))"
  '
  # Kraken status
  KRAKEN_ERR=$(echo "$BALANCES" | jq -r '.kraken.error // ""')
  if [ -n "$KRAKEN_ERR" ]; then
    echo "⚠️  Kraken: unavailable ($(echo "$BALANCES" | jq -r '.kraken.error' | head -c 60))"
  fi
else
  echo "⚠️  Could not fetch balances"
fi

# 3. Recent decisions
echo ""
echo "--- Recent Decisions (last 5) ---"
DECISIONS=$(curl -s "$ZK_BANKIR_HOST/api/v1/decisions" -H "Accept: application/json" 2>/dev/null)
if [ -n "$DECISIONS" ] && echo "$DECISIONS" | jq -e 'type == "array"' > /dev/null 2>&1; then
  echo "$DECISIONS" | jq -r '.[-5:] | .[] | "#\(.id) \(.action) $\(.amount) [\(.status)]"'
else
  echo "⚠️  No decisions or API unavailable"
fi

# 4. Hash chain (requires local access)
echo ""
echo "--- Hash Chain ---"
ZK_PATH="${ZK_BANKIR_PATH:-/home/cwn/App/domains/finance/zk-bankir}"
if [ -d "$ZK_PATH" ]; then
  cd "$ZK_PATH" && \
    bin/rails runner "puts Decision.verify_chain ? '✅ Chain intact' : '❌ Chain BROKEN'" 2>/dev/null || \
    echo "⚠️  Could not verify (Rails not available locally)"
else
  echo "⚠️  ZK_BANKIR_PATH not accessible"
fi

echo ""
echo "=== Summary Complete ==="
