#!/usr/bin/env bash
# SUPAH Pulse — Real-time Crypto Market Intelligence
# Usage: market-pulse.sh [focus]
# focus: "full" (default) | "quick" | "defi" | "gas"
#
# Payment: $0.03 USDC per pulse via x402 on Base
# Your agent's HTTP client pays automatically. No API keys.
# Docs: https://www.x402.org | api.supah.ai

set -euo pipefail

FOCUS="${1:-full}"
API_BASE="${SUPAH_API_BASE:-https://api.supah.ai}"

echo "📡 SUPAH PULSE — Scanning markets..."
echo ""

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# ═══════════════════════════════════════════
# PARALLEL DATA FETCHING
# ═══════════════════════════════════════════

# SUPAH Market Regime (x402 paid — the core intelligence)
curl -sf "${API_BASE}/agent/v1/market/regime?focus=${FOCUS}" \
  -H "Accept: application/json" \
  -o "$TMPDIR/regime.json" 2>/dev/null &
P1=$!

# CoinGecko: Global market + prices (public, enriches the briefing)
curl -sf "https://api.coingecko.com/api/v3/global" \
  -o "$TMPDIR/global.json" 2>/dev/null &
P2=$!

curl -sf "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true" \
  -o "$TMPDIR/prices.json" 2>/dev/null &
P3=$!

# Fear & Greed
curl -sf "https://api.alternative.me/fng/?limit=7" \
  -o "$TMPDIR/fng.json" 2>/dev/null &
P4=$!

# DeFiLlama: Chain TVLs
curl -sf "https://api.llama.fi/v2/chains" \
  -o "$TMPDIR/chains_tvl.json" 2>/dev/null &
P5=$!

wait $P1 $P2 $P3 $P4 $P5 2>/dev/null || true

# ═══════════════════════════════════════════
# CHECK x402 PAYMENT
# ═══════════════════════════════════════════

# Check if regime came back as x402 paywall
REGIME_CHECK=$(cat "$TMPDIR/regime.json" 2>/dev/null | head -c 20)
if echo "$REGIME_CHECK" | grep -q "x402Version"; then
  echo "💳 Payment required: \$0.03 USDC per market pulse"
  echo ""
  echo "x402 micropayment on Base — your agent pays automatically."
  echo "Ensure your agent wallet has USDC on Base."
  echo ""
  echo "Works with: MCP, ACP, ClawHub, any x402-compatible agent"
  echo "Docs: x402.org | api.supah.ai"
  echo ""
  echo "Powered by SUPAH 🦸"
  echo '{"error":"payment_required","price":"0.03","currency":"USDC","network":"base","endpoint":"'${API_BASE}'/agent/v1/market/regime","method":"x402","docs":"https://www.x402.org"}' > /tmp/market-pulse-result.json
  echo "📄 JSON: /tmp/market-pulse-result.json"
  exit 1
fi

# ═══════════════════════════════════════════
# PARSE & DISPLAY
# ═══════════════════════════════════════════

node -e "
const fs = require('fs');
const load = (f) => { try { return JSON.parse(fs.readFileSync('$TMPDIR/' + f)); } catch(e) { return null; } };

const regime = load('regime.json');
const global = load('global.json');
const prices = load('prices.json');
const fng = load('fng.json');
const chainsTvl = load('chains_tvl.json');

const now = new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
const bar = (s) => { const v = Math.round(parseInt(s)||0); return '█'.repeat(Math.max(0,Math.round(v/12.5))) + '░'.repeat(Math.max(0,8 - Math.round(v/12.5))) + ' ' + v; };
const fmt = (n) => !n ? '?' : n > 1e12 ? (n/1e12).toFixed(2) + 'T' : n > 1e9 ? (n/1e9).toFixed(2) + 'B' : n > 1e6 ? (n/1e6).toFixed(1) + 'M' : n > 1e3 ? (n/1e3).toFixed(1) + 'K' : n.toFixed(0);
const pct = (n) => n == null ? '?' : (n > 0 ? '+' : '') + n.toFixed(1) + '%';

// ═══════════════════════════════
// SUPAH REGIME DATA (paid intelligence)
// ═══════════════════════════════
const r = regime || {};
const eth = r.eth || {};
const trend = r.trend || {};
const mom = r.momentumAnalysis || {};
const pred = r.prediction || {};
const macro = r.macro || {};
const levels = r.levels || {};
const mr = levels.meanReversion || {};
const vp = levels.volumeProfile || {};
const base = r.baseChainActivity || {};
const regimeSignals = r.signals || [];

// External data
const gd = global?.data || {};
const btc = prices?.bitcoin || {};
const ethCG = prices?.ethereum || {};
const sol = prices?.solana || {};
const fngData = fng?.data || [];
const fngCurrent = fngData[0] ? parseInt(fngData[0].value) : null;
const fngLabel = fngData[0]?.value_classification || '';
const fngYesterday = fngData[1] ? parseInt(fngData[1].value) : null;
const fngWeekAgo = fngData[6] ? parseInt(fngData[6].value) : null;
const fngTrend = fngCurrent && fngYesterday ? (fngCurrent > fngYesterday ? '↑' : fngCurrent < fngYesterday ? '↓' : '→') : '';

const totalMcap = gd.total_market_cap?.usd || 0;
const totalVol = gd.total_volume?.usd || 0;
const btcDom = gd.market_cap_percentage?.btc || 0;
const ethDom = gd.market_cap_percentage?.eth || 0;
const mcapChange = gd.market_cap_change_percentage_24h_usd || 0;

const chainTvl = Array.isArray(chainsTvl) ? chainsTvl : [];
const totalTvl = chainTvl.reduce((s, c) => s + (c.tvl || 0), 0);
const ethTvl = chainTvl.find(c => c.name === 'Ethereum')?.tvl || 0;
const baseTvl = chainTvl.find(c => c.name === 'Base')?.tvl || 0;
const arbTvl = chainTvl.find(c => c.name === 'Arbitrum')?.tvl || 0;
const solTvl = chainTvl.find(c => c.name === 'Solana')?.tvl || 0;

// ═══════════════════════════════
// SCORING ENGINE
// ═══════════════════════════════
let scores = {};

// 1. ETH MOMENTUM (from SUPAH regime)
const ethMom = mom.positionInRange != null ? Math.round(mom.positionInRange * 100) : 50;
scores.ethMomentum = ethMom;

// 2. TREND HEALTH
let trendScore = 50;
if (trend.allGreen) trendScore = 95;
else if (trend.recovering) trendScore = 70;
else if (trend.bottomForming) trendScore = 60;
else if (trend.accelerating && !trend.acceleratingDump) trendScore = 75;
else if (trend.decelerating) trendScore = 40;
else if (trend.acceleratingDump) trendScore = 15;
else if (trend.allRed) trendScore = 5;
else { trendScore = 35 + (trend.tfUp || 0) * 10; }
scores.trend = Math.max(0, Math.min(100, trendScore));

// 3. SENTIMENT
scores.sentiment = fngCurrent || 50;

// 4. MACRO HEALTH
let macroScore = 50;
const macroComposite = macro.compositeScore || 0;
macroScore = Math.max(0, Math.min(100, 50 + macroComposite * 5));
if (macro.liquidationRisk === 'HIGH') macroScore = Math.max(10, macroScore - 20);
if (macro.squeezeSetup === 'SHORT') macroScore = Math.min(90, macroScore + 15);
if (macro.squeezeSetup === 'LONG') macroScore = Math.max(10, macroScore - 15);
scores.macro = macroScore;

// 5. MEAN REVERSION
let revScore = 50;
const z = mr.zScore || 0;
if (z < -2) revScore = 20; // deeply oversold
else if (z < -1) revScore = 35;
else if (z > 2) revScore = 80; // overextended
else if (z > 1) revScore = 65;
else revScore = 50;
scores.meanReversion = revScore;

// 6. PREDICTION
let predScore = pred.direction === 'UP' ? 70 : pred.direction === 'DOWN' ? 30 : 50;
predScore = Math.round(predScore * (0.5 + (pred.confidence || 0) / 200));
scores.prediction = Math.max(0, Math.min(100, predScore));

// COMPOSITE
const w = { ethMomentum: 0.20, trend: 0.20, sentiment: 0.15, macro: 0.20, meanReversion: 0.10, prediction: 0.15 };
const pulseScore = Math.round(
  scores.ethMomentum*w.ethMomentum + scores.trend*w.trend + scores.sentiment*w.sentiment +
  scores.macro*w.macro + scores.meanReversion*w.meanReversion + scores.prediction*w.prediction
);

// Regime label
let regimeLabel = r.regime || 'UNKNOWN';
let regimeEmoji;
if (pulseScore >= 80) regimeEmoji = '🟢🟢';
else if (pulseScore >= 65) regimeEmoji = '🟢';
else if (pulseScore >= 50) regimeEmoji = '⚡';
else if (pulseScore >= 40) regimeEmoji = '🟡';
else if (pulseScore >= 25) regimeEmoji = '🟠';
else regimeEmoji = '🔴';

// ═══════════════════════════════
// OUTPUT
// ═══════════════════════════════
console.log('');
console.log('📡 SUPAH PULSE — Market Intelligence Briefing');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('');
console.log('🕐 ' + now);
console.log('');
console.log('MARKET PULSE: ' + pulseScore + '/100 ' + regimeEmoji + ' ' + regimeLabel);
console.log('CONFIDENCE: ' + (r.confidence ? r.confidence.toFixed(1) + '%' : '?'));
if (r.reason) console.log('REGIME NOTE: ' + r.reason);
if (fngCurrent) console.log('SENTIMENT: ' + fngLabel + ' (F&G: ' + fngCurrent + ' ' + fngTrend + ' from ' + fngYesterday + ', week ago: ' + fngWeekAgo + ')');
console.log('');

// Score breakdown
console.log('┌──────────────────────────────────────┐');
console.log('│ ETH Momentum       ' + bar(scores.ethMomentum) + ' │');
console.log('│ Trend Health        ' + bar(scores.trend) + ' │');
console.log('│ Sentiment           ' + bar(scores.sentiment) + ' │');
console.log('│ Macro Signals       ' + bar(scores.macro) + ' │');
console.log('│ Mean Reversion      ' + bar(scores.meanReversion) + ' │');
console.log('│ Prediction          ' + bar(scores.prediction) + ' │');
console.log('└──────────────────────────────────────┘');

// ═══════════════════════════════
// ETH MARKET SENTIMENT
// ═══════════════════════════════
console.log('');
console.log('📊 ETH MARKET SENTIMENT:');
if (eth.price) {
  console.log('  Price: \$' + eth.price.toLocaleString('en-US', {maximumFractionDigits: 2}));
  const pc = eth.priceChange || {};
  console.log('  Changes: 1h ' + pct(pc['1h']) + ' | 6h ' + pct(pc['6h']) + ' | 24h ' + pct(pc['24h']));
  console.log('  Weekly range: \$' + (eth.weeklyLow||0).toFixed(0) + ' — \$' + (eth.weeklyHigh||0).toFixed(0) + ' (position: ' + ((eth.pricePosition||0)*100).toFixed(0) + '%)');
}

// Momentum Analysis
console.log('');
console.log('⚡ MOMENTUM:');
if (mom.state) console.log('  State: ' + mom.state);
if (mom.delta10m != null) {
  console.log('  Speed: 10m ' + pct(mom.delta10m) + ' | 30m ' + pct(mom.delta30m) + ' | 1h ' + pct(mom.delta1h));
  console.log('  Trend: 3h ' + pct(mom.delta3h) + ' | 6h ' + pct(mom.delta6h));
  console.log('  Averages: 1h ' + pct(mom.avg1h) + ' | 3h ' + pct(mom.avg3h) + ' | 6h ' + pct(mom.avg6h));
  console.log('  24h range position: ' + ((mom.positionInRange||0)*100).toFixed(0) + '% (0%=low, 100%=high)');
}
if (mom.predictiveSignals?.length) {
  mom.predictiveSignals.forEach(s => console.log('  → ' + s));
}

// Trend Analysis
console.log('');
console.log('📈 TREND ANALYSIS:');
const trendFlags = [];
if (trend.allGreen) trendFlags.push('🟢 ALL GREEN — Strong uptrend across timeframes');
if (trend.allRed) trendFlags.push('🔴 ALL RED — Strong downtrend across timeframes');
if (trend.recovering) trendFlags.push('🔄 RECOVERING — Bouncing from lows');
if (trend.bottomForming) trendFlags.push('🔄 BOTTOM FORMING — Sell pressure easing');
if (trend.accelerating && !trend.acceleratingDump) trendFlags.push('🚀 ACCELERATING UP');
if (trend.acceleratingDump) trendFlags.push('💀 ACCELERATING DUMP');
if (trend.decelerating) trendFlags.push('⚠️ DECELERATING — Momentum fading');
if (trend.volSurge) trendFlags.push('📊 VOLUME SURGE — Big move incoming');
if (trend.volDecline) trendFlags.push('📉 VOLUME DECLINING — Low conviction');
if (trendFlags.length === 0) trendFlags.push('🟡 Mixed signals — no clear trend');
trendFlags.forEach(f => console.log('  ' + f));
console.log('  Timeframes: ' + (trend.tfUp||0) + ' up / ' + (trend.tfDown||0) + ' down');

// Support/Resistance
console.log('');
console.log('🎯 KEY LEVELS:');
if (levels.nearestSupport) console.log('  Support: \$' + levels.nearestSupport.toFixed(2) + ' (' + pct(-levels.distToSupport) + ' away)');
if (levels.nearestResistance) console.log('  Resistance: \$' + levels.nearestResistance.toFixed(2) + ' (' + pct(levels.distToResistance) + ' away)');
if (mr.ema20) console.log('  EMA20: \$' + mr.ema20.toFixed(2) + ' (' + pct(mr.distFromEma20) + ')');
if (mr.ema50) console.log('  EMA50: \$' + mr.ema50.toFixed(2) + ' (' + pct(mr.distFromEma50) + ')');
if (mr.zScore != null) {
  const zLabel = mr.zScore < -2 ? '🔴 DEEPLY OVERSOLD' : mr.zScore < -1 ? '🟠 OVERSOLD' : mr.zScore > 2 ? '🔴 DEEPLY OVERBOUGHT' : mr.zScore > 1 ? '🟠 OVERBOUGHT' : '🟢 NORMAL';
  console.log('  Z-Score: ' + mr.zScore.toFixed(2) + ' — ' + zLabel);
}
if (vp.poc) console.log('  Volume POC: \$' + vp.poc.toFixed(2) + ' (value area: \$' + (vp.valueLow||0).toFixed(0) + ' — \$' + (vp.valueHigh||0).toFixed(0) + ')');

// Macro Signals
console.log('');
console.log('🌍 MACRO:');
if (macro.btcPrice) console.log('  BTC: \$' + macro.btcPrice.toLocaleString() + ' (' + pct(macro.btc24h) + ')');
if (btc.usd) console.log('  ETH: \$' + (ethCG.usd||eth.price||0).toLocaleString() + ' | SOL: \$' + (sol.usd||0).toFixed(2));
if (btcDom) console.log('  BTC Dominance: ' + btcDom.toFixed(1) + '% | ETH: ' + ethDom.toFixed(1) + '%');
if (totalMcap) console.log('  Total MC: \$' + fmt(totalMcap) + ' (' + pct(mcapChange) + ') | Vol: \$' + fmt(totalVol));
if (macro.fundingRate != null) console.log('  Funding Rate: ' + (macro.fundingRate * 100).toFixed(4) + '% (' + (macro.fundingTrend||'') + ')');
if (macro.longShortRatio) console.log('  Long/Short Ratio: ' + macro.longShortRatio.toFixed(2) + ' | Taker B/S: ' + (macro.takerBuySell||0).toFixed(2));
if (macro.liquidationRisk && macro.liquidationRisk !== 'NONE') console.log('  ⚠️ Liquidation Risk: ' + macro.liquidationRisk);
if (macro.squeezeSetup && macro.squeezeSetup !== 'NONE') console.log('  ⚠️ Squeeze Setup: ' + macro.squeezeSetup);
if (macro.compositeSignal) console.log('  Macro Signal: ' + macro.compositeSignal + ' (score: ' + (macro.compositeScore||0) + ')');

// Prediction
console.log('');
console.log('🔮 PREDICTION:');
if (pred.direction) console.log('  Direction: ' + pred.direction + ' | Confidence: ' + (pred.confidence||0) + '%');
if (pred.predictedMove) console.log('  Expected Move: ' + pred.predictedMove);
if (pred.signals?.length) pred.signals.forEach(s => console.log('  → ' + s));

// DeFi
if (totalTvl > 0) {
  console.log('');
  console.log('🏦 DeFi TVL: \$' + fmt(totalTvl));
  if (ethTvl) console.log('  Ethereum: \$' + fmt(ethTvl) + ' | Base: \$' + fmt(baseTvl) + ' | Arbitrum: \$' + fmt(arbTvl));
  if (solTvl) console.log('  Solana: \$' + fmt(solTvl));
}

// Base Chain Activity
if (base.volume24h || base.wallets24h) {
  console.log('');
  console.log('🔵 BASE CHAIN:');
  if (base.volume1h) console.log('  Volume: 1h \$' + fmt(base.volume1h) + ' | 24h \$' + fmt(base.volume24h));
  if (base.wallets1h) console.log('  Wallets: 1h ' + fmt(base.wallets1h) + ' | 24h ' + fmt(base.wallets24h));
  if (base.txns24h) console.log('  Txns 24h: ' + fmt(base.txns24h));
}

// SUPAH Regime Signals
if (regimeSignals.length > 0) {
  console.log('');
  console.log('📡 SUPAH SIGNALS:');
  regimeSignals.forEach(s => console.log('  ' + s));
}

// Trading parameters
if (r.tradingParams) {
  console.log('');
  console.log('⚙️ TRADING PARAMETERS:');
  const tp = r.tradingParams;
  console.log('  ' + (tp.label || ''));
  console.log('  Min Score: ' + tp.minScore + ' | Min TA: ' + tp.minTA + ' | Stop Loss: ' + tp.stopLoss + '%');
  console.log('  Position Scale: ' + tp.positionScale + 'x | Entry: ' + tp.entryMode);
}

// Market Call
console.log('');
let marketCall;
if (pulseScore >= 70) marketCall = 'RISK-ON — Favor longs, increase size';
else if (pulseScore >= 55) marketCall = 'LEAN BULLISH — Moderate positions, buy dips';
else if (pulseScore >= 45) marketCall = 'NEUTRAL — Be selective, small positions';
else if (pulseScore >= 30) marketCall = 'LEAN BEARISH — Reduce exposure, hedge';
else marketCall = 'RISK-OFF — Capital preservation, stables';
console.log('💡 MARKET CALL: ' + marketCall);

// Tactical
console.log('');
console.log('🎯 TACTICAL:');
if (trend.bottomForming) console.log('  → Bottom forming — watch for confirmation before entries');
if (trend.allGreen) console.log('  → All timeframes green — trend following positions');
if (trend.allRed) console.log('  → All timeframes red — avoid longs, wait for reversal');
if (mr.zScore < -1.5) console.log('  → Oversold — mean reversion bounce likely');
if (mr.zScore > 1.5) console.log('  → Overbought — take profits, tighten stops');
if (macro.longShortRatio > 2) console.log('  → Heavy long bias — squeeze risk to downside');
if (macro.longShortRatio < 0.8) console.log('  → Heavy short bias — squeeze risk to upside');
if (mom.state === 'ACCELERATING_UP') console.log('  → Momentum accelerating up — ride the wave');
if (mom.state === 'DECELERATING_DOWN') console.log('  → Sell pressure easing — watch for reversal');
if (btcDom > 55) console.log('  → BTC dominance high — altcoins underperforming');
else if (btcDom < 45) console.log('  → BTC dominance low — altseason potential');
if (fngCurrent && fngCurrent < 25) console.log('  → Extreme Fear — historically good buying zone');
if (fngCurrent && fngCurrent > 75) console.log('  → Extreme Greed — historically good selling zone');

console.log('');
console.log('NFA / DYOR — Data: SUPAH Regime Engine + CoinGecko + Alternative.me + DeFiLlama');
console.log('Powered by SUPAH 🦸 | api.supah.ai');

// JSON
const json = {
  timestamp: new Date().toISOString(),
  pulseScore, regime: regimeLabel, confidence: r.confidence,
  scores,
  eth: { price: eth.price, changes: eth.priceChange, weeklyRange: { low: eth.weeklyLow, high: eth.weeklyHigh }, position: eth.pricePosition },
  momentum: { state: mom.state, deltas: { '10m': mom.delta10m, '30m': mom.delta30m, '1h': mom.delta1h, '3h': mom.delta3h, '6h': mom.delta6h }, averages: { '1h': mom.avg1h, '3h': mom.avg3h, '6h': mom.avg6h }, rangePosition: mom.positionInRange, predictiveSignals: mom.predictiveSignals },
  trend: { state: trend.allGreen ? 'ALL_GREEN' : trend.allRed ? 'ALL_RED' : trend.bottomForming ? 'BOTTOM_FORMING' : trend.recovering ? 'RECOVERING' : 'MIXED', tfUp: trend.tfUp, tfDown: trend.tfDown, flags: { volSurge: trend.volSurge, volDecline: trend.volDecline, accelerating: trend.accelerating, decelerating: trend.decelerating } },
  levels: { support: levels.nearestSupport, resistance: levels.nearestResistance, ema20: mr.ema20, ema50: mr.ema50, zScore: mr.zScore, volumePOC: vp.poc, valueArea: { low: vp.valueLow, high: vp.valueHigh } },
  prediction: pred,
  macro: { btcPrice: macro.btcPrice, btc24h: macro.btc24h, fundingRate: macro.fundingRate, longShortRatio: macro.longShortRatio, takerBuySell: macro.takerBuySell, liquidationRisk: macro.liquidationRisk, squeezeSetup: macro.squeezeSetup, signal: macro.compositeSignal, score: macro.compositeScore },
  sentiment: { fearGreed: fngCurrent, label: fngLabel, yesterday: fngYesterday, weekAgo: fngWeekAgo },
  dominance: { btc: btcDom, eth: ethDom },
  market: { totalMarketCap: totalMcap, totalVolume: totalVol, change24h: mcapChange },
  defi: { totalTvl, ethereum: ethTvl, base: baseTvl, arbitrum: arbTvl, solana: solTvl },
  baseChain: base,
  tradingParams: r.tradingParams,
  signals: regimeSignals,
  marketCall,
  meta: { source: 'supah-pulse', version: '2.0.0' }
};
fs.writeFileSync('/tmp/market-pulse-result.json', JSON.stringify(json, null, 2));
console.log('');
console.log('📄 JSON: /tmp/market-pulse-result.json');
" 2>&1
