#!/usr/bin/env bash
# SUPAH Wallet X-Ray — Instant Wallet Intelligence
# Usage: wallet-xray.sh <address_or_ens> [chain]
#
# Payment: $0.05 USDC per scan via x402 on Base
# Your agent's HTTP client pays automatically. No API keys.
# Docs: https://www.x402.org | api.supah.ai

set -euo pipefail

INPUT="${1:?Usage: wallet-xray.sh <address_or_ens> [chain]}"
CHAIN="${2:-ethereum}"

CHAIN_LOWER=$(echo "$CHAIN" | tr '[:upper:]' '[:lower:]')
API_BASE="${SUPAH_API_BASE:-https://api.supah.ai}"

echo "🔍 SUPAH WALLET X-RAY — Scanning $INPUT on $CHAIN..."
echo ""

# ═══════════════════════════════════════════
# RESOLVE ENS (free, needed before API call)
# ═══════════════════════════════════════════

ADDRESS="$INPUT"
ENS_NAME=""

if [[ "$INPUT" == *.eth ]] || [[ "$INPUT" == *.xyz ]] || [[ ! "$INPUT" =~ ^0x ]]; then
  ENS_RESULT=$(curl -sf "https://api.ensideas.com/ens/resolve/$INPUT" 2>/dev/null || echo "{}")
  RESOLVED=$(echo "$ENS_RESULT" | node -pe "try{JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')).address||''}catch(e){''}" 2>/dev/null || echo "")
  if [ -n "$RESOLVED" ] && [ "$RESOLVED" != "null" ] && [ "$RESOLVED" != "" ]; then
    ADDRESS="$RESOLVED"
    ENS_NAME="$INPUT"
    echo "✅ Resolved $INPUT → $ADDRESS"
    echo ""
  else
    echo "❌ Could not resolve ENS name: $INPUT"
    exit 1
  fi
fi

ADDR_LOWER=$(echo "$ADDRESS" | tr '[:upper:]' '[:lower:]')

# ═══════════════════════════════════════════
# CALL SUPAH API (x402 payment)
# ═══════════════════════════════════════════

RESULT=$(curl -sf "${API_BASE}/agent/v1/wallet/${ADDR_LOWER}/stats?chain=${CHAIN_LOWER}" \
   \
  -H "Accept: application/json" \
  -w "\n%{http_code}" 2>/dev/null || echo -e "\n000")

HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | sed '$d')

# Handle x402 payment required
if [ "$HTTP_CODE" = "402" ]; then
  echo "💳 Payment required: \$0.05 USDC per wallet scan"
  echo ""
  echo "x402 micropayment on Base — your agent pays automatically."
  echo "Ensure your agent wallet has USDC on Base."
  echo ""
  echo "Works with: MCP, ACP, ClawHub, any x402-compatible agent"
  echo "Docs: x402.org | api.supah.ai"
  echo ""
  echo "Powered by SUPAH 🦸"
  
  echo '{"error":"payment_required","price":"0.05","currency":"USDC","network":"base","endpoint":"'${API_BASE}'/agent/v1/wallet","method":"x402","docs":"https://www.x402.org"}' > /tmp/wallet-xray-result.json
  echo "📄 JSON: /tmp/wallet-xray-result.json"
  exit 1
fi

if [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" = "500" ] || [ "$HTTP_CODE" = "503" ]; then
  echo "⚠️ SUPAH API temporarily unavailable. Try again shortly."
  exit 1
fi

if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
  echo "⚠️ Payment failed or insufficient USDC balance."
  exit 1
fi

# ═══════════════════════════════════════════
# PARSE & DISPLAY
# ═══════════════════════════════════════════

echo "$BODY" | node -e "
const fs = require('fs');
const raw = fs.readFileSync('/dev/stdin', 'utf8');
let d;
try { d = JSON.parse(raw); } catch(e) { console.log('⚠️ Unexpected response'); process.exit(1); }

if (d.status === 'error') {
  console.log('⚠️ Scan error: ' + (d.error?.message || 'Unknown'));
  process.exit(1);
}

const r = d.data || d;
const addr = '${ADDRESS}';
const ensName = '${ENS_NAME}';

// Extract
const trustScore = r.trustScore || r.score || 50;
const verdict = r.verdict || (trustScore >= 80 ? 'TRUSTED' : trustScore >= 55 ? 'NEUTRAL' : trustScore >= 35 ? 'SUSPICIOUS' : 'DANGEROUS');
const ve = verdict === 'TRUSTED' ? '🟢' : verdict === 'NEUTRAL' ? '🟡' : verdict === 'SUSPICIOUS' ? '🟠' : '🔴';
const labels = r.labels || [];
const scores = r.scores || {};
const risks = r.risks || [];
const positives = r.positives || [];
const profile = r.profile || {};

const bar = (s) => { const v = parseInt(s)||0; return '█'.repeat(Math.round(v/12.5)) + '░'.repeat(8 - Math.round(v/12.5)) + ' ' + v; };

console.log('');
console.log('🔍 SUPAH WALLET X-RAY');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');
console.log('Address: ' + addr.substring(0,6) + '...' + addr.substring(38));
if (ensName) console.log('ENS: ' + ensName);
console.log('Chain: ' + '${CHAIN}'.charAt(0).toUpperCase() + '${CHAIN}'.slice(1));
if (labels.length > 0) console.log('Labels: ' + labels.join(' | '));
console.log('');
console.log('TRUST SCORE: ' + trustScore + '/100 ' + ve + ' ' + verdict);

if (Object.keys(scores).length > 0) {
  console.log('');
  console.log('┌──────────────────────────────────────┐');
  const sLabels = { age: 'Wallet Age', activity: 'Activity Level', portfolio: 'Portfolio Health', trading: 'Trading Record', risk: 'Risk Flags', network: 'Network Quality' };
  for (const [k, v] of Object.entries(scores)) {
    console.log('│ ' + (sLabels[k]||k).padEnd(20) + bar(v) + ' │');
  }
  console.log('└──────────────────────────────────────┘');
}

if (profile.nativeBalance !== undefined) {
  console.log('');
  console.log('📊 PROFILE:');
  if (profile.ageDays) console.log('  • Age: ' + profile.ageDays + ' days');
  if (profile.nativeBalance !== undefined) console.log('  • Balance: ' + parseFloat(profile.nativeBalance).toFixed(4) + ' ' + (profile.nativeSymbol || 'ETH'));
  if (profile.tokensHeld) console.log('  • Tokens held: ' + profile.tokensHeld);
  if (profile.defiProtocols?.length) console.log('  • DeFi: ' + profile.defiProtocols.join(', '));
  if (profile.netWorth) console.log('  • Net worth: \$' + parseFloat(profile.netWorth).toLocaleString());
  if (profile.pnl) console.log('  • PnL: ' + (profile.pnl > 0 ? '+' : '') + '\$' + parseFloat(profile.pnl).toLocaleString());
}

if (risks.length > 0) { console.log(''); console.log('⚠️ RISKS:'); risks.forEach(r => console.log('  ' + (typeof r === 'string' ? r : r.message || JSON.stringify(r)))); }
if (positives.length > 0) { console.log(''); console.log('✅ POSITIVES:'); positives.forEach(p => console.log('  ' + (typeof p === 'string' ? p : p.message || JSON.stringify(p)))); }

console.log('');
console.log('NFA / DYOR — Powered by SUPAH 🦸');
console.log('api.supah.ai');

fs.writeFileSync('/tmp/wallet-xray-result.json', JSON.stringify(d, null, 2));
console.log('');
console.log('📄 JSON: /tmp/wallet-xray-result.json');
" 2>&1
