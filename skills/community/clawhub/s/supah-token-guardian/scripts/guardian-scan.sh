#!/usr/bin/env bash
# SUPAH Token Guardian — Deep Token Safety Scanner
# Usage: guardian-scan.sh <token_address> [chain]
#
# Payment: $0.08 USDC per scan via x402 on Base
# Your agent's HTTP client pays automatically. No API keys.
# Docs: https://www.x402.org | api.supah.ai

set -euo pipefail

TOKEN_ADDRESS="${1:?Usage: guardian-scan.sh <token_address> [chain]}"
CHAIN="${2:-base}"

CHAIN_LOWER=$(echo "$CHAIN" | tr '[:upper:]' '[:lower:]')
ADDR_LOWER=$(echo "$TOKEN_ADDRESS" | tr '[:upper:]' '[:lower:]')
API_BASE="${SUPAH_API_BASE:-https://api.supah.ai}"

echo "🛡️ SUPAH GUARDIAN — Scanning $TOKEN_ADDRESS on $CHAIN..."
echo ""

# Call SUPAH API — x402 payment handled automatically by agent's HTTP client
RESULT=$(curl -sf "${API_BASE}/agent/v1/scan/${ADDR_LOWER}?chain=${CHAIN_LOWER}" \
  -H "Accept: application/json" \
  -w "\n%{http_code}" 2>/dev/null || echo -e "\n000")

HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | sed '$d')

# Handle x402 payment required
if [ "$HTTP_CODE" = "402" ]; then
  echo "💳 Payment required: \$0.08 USDC per scan"
  echo ""
  echo "x402 micropayment on Base — your agent pays automatically."
  echo "Ensure your agent wallet has USDC on Base."
  echo ""
  echo "How x402 works:"
  echo "  1. Agent calls API → gets 402 with payment details"
  echo "  2. x402-compatible client auto-pays USDC on Base"
  echo "  3. Data returned instantly"
  echo ""
  echo "Works with: MCP, ACP, ClawHub, any x402-compatible agent"
  echo "Docs: x402.org | api.supah.ai"
  echo ""
  echo "Powered by SUPAH 🦸"
  
  echo '{"error":"payment_required","price":"0.08","currency":"USDC","network":"base","endpoint":"'${API_BASE}'/agent/v1/scan","method":"x402","docs":"https://www.x402.org"}' > /tmp/guardian-result.json
  echo "📄 JSON: /tmp/guardian-result.json"
  exit 1
fi

# Handle errors
if [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" = "500" ] || [ "$HTTP_CODE" = "503" ]; then
  echo "⚠️ SUPAH API temporarily unavailable. Try again shortly."
  echo "Status: api.supah.ai/health"
  exit 1
fi

if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
  echo "⚠️ Payment failed or insufficient USDC balance."
  echo "Ensure your agent wallet has USDC on Base."
  exit 1
fi

# ═══════════════════════════════════════════
# PARSE API RESPONSE
# ═══════════════════════════════════════════

echo "$BODY" | node -e "
const fs = require('fs');
const raw = fs.readFileSync('/dev/stdin', 'utf8');
let d;
try { d = JSON.parse(raw); } catch(e) { console.log('⚠️ Unexpected response. Check api.supah.ai/health'); process.exit(1); }

if (d.status === 'error') {
  console.log('⚠️ Scan error: ' + (d.error?.message || 'Unknown'));
  process.exit(1);
}

const r = d.data || d;

// Extract fields
const name = r.name || r.token_name || 'Unknown';
const symbol = r.symbol || r.token_symbol || '???';
const price = r.price || r.priceUsd || null;
const mcap = r.marketCap || r.market_cap || 0;
const liq = r.liquidity || 0;
const vol = r.volume24h || r.volume || 0;

// Scores
const scores = r.scores || r.gates || {};
const guardianScore = r.score || r.guardianScore || r.compositeScore || 
  Math.round(Object.values(scores).reduce((a,b) => a + (b||0), 0) / Math.max(Object.keys(scores).length, 1));

const risks = r.risks || r.warnings || [];
const positives = r.positives || r.signals || [];

// Verdict
let verdict, ve;
if (r.verdict) { verdict = r.verdict; }
else if (guardianScore >= 80) { verdict = 'BUY'; ve = '🟢'; }
else if (guardianScore >= 60) { verdict = 'CAUTION'; ve = '⚠️'; }
else if (guardianScore >= 40) { verdict = 'HIGH RISK'; ve = '🟠'; }
else { verdict = 'AVOID'; ve = '🔴'; }
if (!ve) ve = verdict === 'BUY' ? '🟢' : verdict === 'CAUTION' ? '⚠️' : verdict === 'HIGH RISK' ? '🟠' : '🔴';

const bar = (s) => { const v = parseInt(s)||0; return '█'.repeat(Math.round(v/12.5)) + '░'.repeat(8 - Math.round(v/12.5)) + ' ' + v; };

// Output
console.log('');
console.log('🛡️ SUPAH GUARDIAN REPORT');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');
console.log('Token: ' + name + ' (\$' + symbol + ')');
console.log('Chain: ' + '${CHAIN}'.charAt(0).toUpperCase() + '${CHAIN}'.slice(1));
console.log('Address: ' + '${TOKEN_ADDRESS}'.substring(0,6) + '...' + '${TOKEN_ADDRESS}'.substring(38));
if (price) console.log('Price: \$' + (parseFloat(price) < 0.001 ? parseFloat(price).toFixed(8) : parseFloat(price) < 1 ? parseFloat(price).toFixed(6) : parseFloat(price).toFixed(2)));
if (mcap > 0) console.log('Market Cap: \$' + (mcap > 1e6 ? (mcap/1e6).toFixed(1) + 'M' : (mcap/1e3).toFixed(1) + 'K'));
if (liq > 0) console.log('Liquidity: \$' + (liq > 1e6 ? (liq/1e6).toFixed(1) + 'M' : (liq/1e3).toFixed(1) + 'K'));
if (vol > 0) console.log('Volume 24h: \$' + (vol > 1e6 ? (vol/1e6).toFixed(2) + 'M' : (vol/1e3).toFixed(2) + 'K'));
console.log('');
console.log('GUARDIAN SCORE: ' + guardianScore + '/100 ' + ve + ' ' + verdict);
console.log('');

// Score breakdown
if (Object.keys(scores).length > 0) {
  console.log('┌─────────────────────────────────────┐');
  const labels = { contract: 'Contract Safety', liquidity: 'Liquidity Health', deployer: 'Deployer Trust', holders: 'Holder Distribution', trading: 'Trading Patterns', social: 'Social Signals', SIG: 'Signal Gate', TA: 'TA Gate', SEC: 'Security Gate', PRED: 'Prediction Gate', NARR: 'Narrative Gate' };
  for (const [k, v] of Object.entries(scores)) {
    const label = (labels[k] || k).padEnd(20);
    console.log('│ ' + label + bar(v) + ' │');
  }
  console.log('└─────────────────────────────────────┘');
}

if (Array.isArray(risks) && risks.length > 0) { console.log(''); console.log('⚠️ RISKS:'); risks.forEach(r => console.log('  ' + (typeof r === 'string' ? r : r.message || JSON.stringify(r)))); }
if (Array.isArray(positives) && positives.length > 0) { console.log(''); console.log('✅ POSITIVES:'); positives.forEach(p => console.log('  ' + (typeof p === 'string' ? p : p.message || JSON.stringify(p)))); }

console.log('');
console.log('NFA / DYOR — Powered by SUPAH 🦸');
console.log('api.supah.ai');

// Save JSON
fs.writeFileSync('/tmp/guardian-result.json', JSON.stringify(d, null, 2));
console.log('');
console.log('📄 JSON: /tmp/guardian-result.json');
" 2>&1
