#!/usr/bin/env node
/**
 * macro-rotation.js — Long-Term Macro Rotation Strategy
 * 
 * Inspired by institutional crypto macro rotation:
 * - LTPI (Long Term Probability Indicator): 0-1, macro liquidity + on-chain + global M2
 * - MTPI (Medium Term Probability Indicator): 0-1, market structure + derivatives + momentum
 * - Relative Strength Tournament: z-scored cross-pair strength, rotates into top 1-3
 * - Cash is a valid allocation when signals are weak
 * 
 * Runs DAILY at candle close. Rebalances portfolio allocation.
 * Starting capital: $10,000 (minimum for real gains)
 */
'use strict';
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const { execSync } = require('child_process');

const PORTFOLIO_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/portfolio-macro.json');

const TOKENS = [
  'BTCUSDT','ETHUSDT','SOLUSDT','BNBUSDT','XRPUSDT','DOGEUSDT','AVAXUSDT','LINKUSDT',
  'ARBUSDT','OPUSDT','SUIUSDT','APTUSDT','INJUSDT','SEIUSDT','FETUSDT','RENDERUSDT',
  'TAOUSDT','NEARUSDT','WIFUSDT','JUPUSDT','TIAUSDT','DYMUSDT','STRKUSDT','TONUSDT',
  'NOTUSDT','EIGENUSDT','GRASSUSDT','VIRTUALUSDT','AKTUSDT',
  'HYPEUSDT',    // Hyperliquid — prof's pick
  'PAXGUSDT',    // Gold (Paxos) — defensive allocation
];

// Token categories for allocation logic
const DEFENSIVE_TOKENS = new Set(['PAXGUSDT']);
const BTC_TOKEN = 'BTCUSDT';

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════
function httpGet(url, timeout = 10000) {
  return new Promise((res, rej) => {
    const r = https.get(url, resp => {
      let d = ''; resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    }); r.on('error', rej);
    r.setTimeout(timeout, () => { r.destroy(); rej(new Error('timeout')); });
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
function calcEMA(v,p){const k=2/(p+1);let e=v[0];return v.map((x,i)=>{if(i>0)e=x*k+e*(1-k);return e;});}
function calcRSI(c,p=14){const r=Array(c.length).fill(null);let ag=0,al=0;for(let i=1;i<=p;i++){const d=c[i]-c[i-1];if(d>0)ag+=d;else al-=d;}ag/=p;al/=p;r[p]=al===0?100:100-100/(1+ag/al);for(let i=p+1;i<c.length;i++){const d=c[i]-c[i-1];ag=(ag*(p-1)+(d>0?d:0))/p;al=(al*(p-1)+(d<0?-d:0))/p;r[i]=al===0?100:100-100/(1+ag/al);}return r;}
function clamp(v,min,max){return Math.max(min,Math.min(max,v));}

function zScoreArr(values) {
  const valid = values.filter(v => v !== null && !isNaN(v));
  if (valid.length < 3) return values.map(() => 0);
  const mean = valid.reduce((s,v)=>s+v,0)/valid.length;
  const std = Math.sqrt(valid.reduce((s,v)=>s+(v-mean)**2,0)/valid.length);
  if (std === 0) return values.map(() => 0);
  return values.map(v => v === null || isNaN(v) ? 0 : (v - mean) / std);
}

function sigmoid(x) { return 1 / (1 + Math.exp(-x)); } // maps any value to 0-1

// ═══════════════════════════════════════════════════════════════════════════════
// DATA FETCHERS
// ═══════════════════════════════════════════════════════════════════════════════
function fetchFRED(seriesId, startDate = '2024-01-01') {
  try {
    const csv = execSync(`curl -sL --max-time 12 "https://fred.stlouisfed.org/graph/fredgraph.csv?id=${seriesId}&cosd=${startDate}"`, { encoding: 'utf8', timeout: 15000 });
    const lines = csv.trim().split('\n').slice(1);
    return lines.map(l => { const [d,v] = l.split(','); const val = parseFloat(v); return { date: d, value: isNaN(val) ? null : val }; }).filter(d => d.value !== null);
  } catch { return []; }
}

async function fetchCandles(sym, interval, limit) {
  await sleep(60);
  try {
    const r = await httpGet(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=${interval}&limit=${limit}`);
    return r.map(k => ({ ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4], tbv:+k[9]*+k[4] }));
  } catch { return []; }
}

async function fetchFundingRate(sym = 'BTCUSDT') {
  try { const r = await httpGet(`https://fapi.binance.com/fapi/v1/fundingRate?symbol=${sym}&limit=30`); return r.map(f => parseFloat(f.fundingRate)); } catch { return []; }
}

async function fetchLSRatio(sym = 'BTCUSDT') {
  try { const r = await httpGet(`https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=${sym}&period=1d&limit=30`); return r.map(d => parseFloat(d.longShortRatio)); } catch { return []; }
}

async function fetchOI(sym = 'BTCUSDT') {
  try { const r = await httpGet(`https://fapi.binance.com/futures/data/openInterestHist?symbol=${sym}&period=1d&limit=30`); return r.map(d => parseFloat(d.sumOpenInterestValue)); } catch { return []; }
}

async function fetchFearGreed() {
  try { const r = await httpGet('https://api.alternative.me/fng/?limit=30'); return r.data ? r.data.map(d => parseInt(d.value)) : []; } catch { return []; }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LTPI — Long Term Probability Indicator
// 30+ inputs → classified → weighted → z-scored → sigmoid → 0-1
// ═══════════════════════════════════════════════════════════════════════════════
async function computeLTPI() {
  // ── Macro Liquidity (FRED) ──
  const [walcl, tga, rrp, m2, dxy, dgs10, t10yie, dff] = await Promise.all([
    fetchFRED('WALCL', '2024-01-01'),   // Fed Balance Sheet
    fetchFRED('WTREGEN', '2024-01-01'), // Treasury General Account
    fetchFRED('RRPONTSYD', '2024-06-01'), // Reverse Repo
    fetchFRED('M2SL', '2023-01-01'),     // M2
    fetchFRED('DTWEXBGS', '2024-06-01'), // Dollar Index
    fetchFRED('DGS10', '2024-06-01'),    // 10Y Yield
    fetchFRED('T10YIE', '2024-06-01'),   // Breakeven Inflation
    fetchFRED('DFF', '2024-06-01'),      // Fed Funds
  ]);
  
  // ── BTC Daily Candles (trend) ──
  const btcD = await fetchCandles('BTCUSDT', '1d', 250);
  const btcCloses = btcD.map(c => c.c);
  
  // ── Fear & Greed ──
  const fng = await fetchFearGreed();
  
  const inputs = {};
  const categories = { liquidity: [], trend: [], macro_momentum: [], risk_appetite: [] };
  
  // ─── LIQUIDITY INPUTS ───
  // 1. Net Liquidity 4-week delta
  if (walcl.length >= 5 && tga.length >= 5 && rrp.length >= 5) {
    const nl = walcl[walcl.length-1].value - tga[tga.length-1].value - rrp[rrp.length-1].value * 1000;
    const nl4 = walcl[walcl.length-5].value - tga[tga.length-5].value - (rrp.length >= 30 ? rrp[rrp.length-22].value : rrp[0].value) * 1000;
    inputs.net_liq_delta = (nl - nl4) / Math.abs(nl4) * 100;
    categories.liquidity.push(inputs.net_liq_delta * 2);
  }
  
  // 2. Net Liquidity 12-week delta (longer trend)
  if (walcl.length >= 13 && tga.length >= 13) {
    const nl = walcl[walcl.length-1].value - tga[tga.length-1].value;
    const nl12 = walcl[walcl.length-13].value - tga[tga.length-13].value;
    inputs.net_liq_12w = (nl - nl12) / Math.abs(nl12) * 100;
    categories.liquidity.push(inputs.net_liq_12w);
  }
  
  // 3. M2 YoY growth
  if (m2.length >= 13) {
    inputs.m2_yoy = (m2[m2.length-1].value - m2[m2.length-13].value) / m2[m2.length-13].value * 100;
    categories.liquidity.push((inputs.m2_yoy - 3) * 0.5); // 3% baseline
  }
  
  // 4. M2 3-month momentum
  if (m2.length >= 4) {
    inputs.m2_3m = (m2[m2.length-1].value - m2[m2.length-4].value) / m2[m2.length-4].value * 100;
    categories.liquidity.push(inputs.m2_3m * 3);
  }
  
  // 5. RRP trend (declining RRP = liquidity release)
  if (rrp.length >= 20) {
    const rrpNow = rrp[rrp.length-1].value;
    const rrp20 = rrp[rrp.length-20].value;
    inputs.rrp_delta = rrp20 !== 0 ? -(rrpNow - rrp20) / Math.max(rrp20, 1) * 100 : 0; // declining = positive
    categories.liquidity.push(inputs.rrp_delta * 0.5);
  }
  
  // ─── MACRO MOMENTUM ───
  // 6. DXY 20-day change (inverse)
  if (dxy.length >= 21) {
    inputs.dxy_20d = -(dxy[dxy.length-1].value - dxy[dxy.length-21].value) / dxy[dxy.length-21].value * 100;
    categories.macro_momentum.push(inputs.dxy_20d * 3);
  }
  
  // 7. DXY 60-day trend
  if (dxy.length >= 61) {
    inputs.dxy_60d = -(dxy[dxy.length-1].value - dxy[dxy.length-61].value) / dxy[dxy.length-61].value * 100;
    categories.macro_momentum.push(inputs.dxy_60d * 2);
  }
  
  // 8. Real yields level
  if (dgs10.length >= 1 && t10yie.length >= 1) {
    inputs.real_yield = dgs10[dgs10.length-1].value - t10yie[t10yie.length-1].value;
    categories.macro_momentum.push(-(inputs.real_yield - 1) * 1.5);
  }
  
  // 9. Real yields momentum (20d)
  if (dgs10.length >= 21 && t10yie.length >= 21) {
    const ryNow = dgs10[dgs10.length-1].value - t10yie[t10yie.length-1].value;
    const ry20 = dgs10[dgs10.length-21].value - t10yie[t10yie.length-21].value;
    inputs.real_yield_mom = -(ryNow - ry20) * 3;
    categories.macro_momentum.push(inputs.real_yield_mom);
  }
  
  // 10. Fed rate trajectory
  if (dff.length >= 30) {
    inputs.fed_rate_30d = -(dff[dff.length-1].value - dff[dff.length-30].value) * 2;
    categories.macro_momentum.push(inputs.fed_rate_30d);
  }
  
  // ─── BTC TREND ───
  if (btcCloses.length >= 200) {
    const n = btcCloses.length - 1;
    
    // 11. Price vs 200 EMA
    const ema200 = calcEMA(btcCloses, 200);
    inputs.btc_vs_200 = (btcCloses[n] - ema200[n]) / ema200[n] * 100;
    categories.trend.push(inputs.btc_vs_200 * 0.3);
    
    // 12. 50 vs 200 EMA (golden/death cross)
    const ema50 = calcEMA(btcCloses, 50);
    inputs.btc_50_200 = (ema50[n] - ema200[n]) / ema200[n] * 100;
    categories.trend.push(inputs.btc_50_200 * 0.5);
    
    // 13. 20 vs 50 EMA
    const ema20 = calcEMA(btcCloses, 20);
    inputs.btc_20_50 = (ema20[n] - ema50[n]) / ema50[n] * 100;
    categories.trend.push(inputs.btc_20_50);
    
    // 14. BTC 90-day ROC
    if (n >= 90) {
      inputs.btc_roc_90 = (btcCloses[n] - btcCloses[n-90]) / btcCloses[n-90] * 100;
      categories.trend.push(inputs.btc_roc_90 * 0.1);
    }
    
    // 15. BTC RSI 14 (daily)
    const rsi = calcRSI(btcCloses);
    if (rsi[n] !== null) {
      inputs.btc_rsi = rsi[n];
      categories.trend.push((rsi[n] - 50) * 0.05);
    }
    
    // 16. Higher highs count (last 60 days)
    let hh = 0;
    for (let i = n - 59; i <= n - 5; i++) {
      if (i < 5) continue;
      let isHigh = true;
      for (let j = 1; j <= 5; j++) if (btcD[i-j].h >= btcD[i].h || btcD[i+j].h >= btcD[i].h) isHigh = false;
      if (isHigh) hh++;
    }
    inputs.btc_hh_count = hh;
    categories.trend.push(hh * 0.3);
  }
  
  // ─── RISK APPETITE ───
  // 17. Fear & Greed (contrarian + confirmation)
  if (fng.length >= 1) {
    const fg = fng[0];
    inputs.fear_greed = fg;
    // Below 25: extreme fear → contrarian bullish
    // 25-45: fear → mild bullish
    // 45-55: neutral
    // 55-75: greed → confirms trend
    // 75+: extreme greed → contrarian bearish
    if (fg < 25) categories.risk_appetite.push(2);
    else if (fg < 40) categories.risk_appetite.push(0.5);
    else if (fg <= 60) categories.risk_appetite.push(0);
    else if (fg <= 75) categories.risk_appetite.push(0.5);
    else categories.risk_appetite.push(-2);
  }
  
  // 18. F&G 7-day average trend
  if (fng.length >= 7) {
    const avg7 = fng.slice(0,7).reduce((s,v)=>s+v,0)/7;
    const avg30 = fng.reduce((s,v)=>s+v,0)/fng.length;
    inputs.fng_momentum = avg7 - avg30;
    categories.risk_appetite.push(inputs.fng_momentum * 0.1);
  }
  
  // ── AGGREGATE ──
  // Weight each category, z-score within, then aggregate
  const weights = { liquidity: 3.0, macro_momentum: 2.0, trend: 2.0, risk_appetite: 1.0 };
  let totalScore = 0, totalWeight = 0;
  const breakdown = {};
  
  for (const [cat, vals] of Object.entries(categories)) {
    if (!vals.length) continue;
    const avg = vals.reduce((s,v)=>s+v,0)/vals.length;
    const w = weights[cat] || 1;
    totalScore += avg * w;
    totalWeight += w;
    breakdown[cat] = { avg: parseFloat(avg.toFixed(3)), weight: w, count: vals.length };
  }
  
  const rawScore = totalWeight > 0 ? totalScore / totalWeight : 0;
  
  // Sigmoid → 0-1 probability
  // Scale factor: adjust so ±3 raw → ~0.95/0.05 probability
  const ltpi = parseFloat(sigmoid(rawScore * 0.8).toFixed(4));
  
  return { ltpi, rawScore: parseFloat(rawScore.toFixed(3)), inputs, breakdown };
}

// ═══════════════════════════════════════════════════════════════════════════════
// MTPI — Medium Term Probability Indicator
// Market structure + derivatives + faster momentum
// ═══════════════════════════════════════════════════════════════════════════════
async function computeMTPI() {
  const btcD = await fetchCandles('BTCUSDT', '1d', 120);
  const btc4h = await fetchCandles('BTCUSDT', '4h', 200);
  if (btcD.length < 60 || btc4h.length < 100) return { mtpi: 0.5, rawScore: 0, inputs: {}, breakdown: {} };
  
  const closes = btcD.map(c => c.c);
  const closes4h = btc4h.map(c => c.c);
  const n = closes.length - 1;
  const n4 = closes4h.length - 1;
  
  const [funding, lsRatio, oiData, fng] = await Promise.all([
    fetchFundingRate(), fetchLSRatio(), fetchOI(), fetchFearGreed()
  ]);
  
  const inputs = {};
  const categories = { momentum: [], structure: [], derivatives: [], flow: [] };
  
  // ─── MOMENTUM ───
  // 1. Daily RSI
  const rsi = calcRSI(closes);
  if (rsi[n] !== null) {
    inputs.rsi_14 = rsi[n];
    categories.momentum.push((rsi[n] - 50) * 0.06);
  }
  
  // 2. 4h RSI (faster)
  const rsi4h = calcRSI(closes4h);
  if (rsi4h[n4] !== null) {
    inputs.rsi_4h = rsi4h[n4];
    categories.momentum.push((rsi4h[n4] - 50) * 0.04);
  }
  
  // 3. 7-day ROC
  if (n >= 7) {
    inputs.roc_7d = (closes[n] - closes[n-7]) / closes[n-7] * 100;
    categories.momentum.push(inputs.roc_7d * 0.3);
  }
  
  // 4. 21-day ROC
  if (n >= 21) {
    inputs.roc_21d = (closes[n] - closes[n-21]) / closes[n-21] * 100;
    categories.momentum.push(inputs.roc_21d * 0.15);
  }
  
  // 5. MACD histogram direction
  const e12 = calcEMA(closes, 12), e26 = calcEMA(closes, 26);
  const macdLine = closes.map((_,i) => e12[i] - e26[i]);
  const macdSig = calcEMA(macdLine.slice(25), 9);
  const hist = macdLine[n] - (macdSig[n-25] || 0);
  const histPrev = n > 1 ? macdLine[n-1] - (macdSig[n-26] || 0) : hist;
  inputs.macd_hist = hist;
  inputs.macd_rising = hist > histPrev;
  categories.momentum.push(hist > 0 ? 1 : -1);
  categories.momentum.push(hist > histPrev ? 0.5 : -0.5);
  
  // ─── STRUCTURE ───
  // 6. EMA alignment (8 > 21 > 50)
  const ema8 = calcEMA(closes, 8), ema21 = calcEMA(closes, 21), ema50 = calcEMA(closes, 50);
  const aligned = ema8[n] > ema21[n] && ema21[n] > ema50[n];
  const inverted = ema8[n] < ema21[n] && ema21[n] < ema50[n];
  inputs.ema_aligned = aligned ? 'bullish' : inverted ? 'bearish' : 'mixed';
  categories.structure.push(aligned ? 2 : inverted ? -2 : 0);
  
  // 7. Price vs 50 EMA distance
  inputs.dist_50ema = (closes[n] - ema50[n]) / ema50[n] * 100;
  categories.structure.push(clamp(inputs.dist_50ema * 0.3, -2, 2));
  
  // 8. 4h trend (20 vs 50 EMA)
  const ema20_4h = calcEMA(closes4h, 20), ema50_4h = calcEMA(closes4h, 50);
  inputs.trend_4h = (ema20_4h[n4] - ema50_4h[n4]) / ema50_4h[n4] * 100;
  categories.structure.push(clamp(inputs.trend_4h * 0.5, -2, 2));
  
  // ─── DERIVATIVES ───
  // 9. Funding rate (contrarian)
  if (funding.length >= 3) {
    const avgF = funding.slice(-3).reduce((s,v)=>s+v,0)/3;
    inputs.funding_avg = avgF;
    categories.derivatives.push(clamp(-avgF * 3000, -2, 2));
  }
  
  // 10. L/S Ratio (contrarian)
  if (lsRatio.length >= 5) {
    const avgLS = lsRatio.slice(-5).reduce((s,v)=>s+v,0)/5;
    inputs.ls_ratio = avgLS;
    categories.derivatives.push(clamp(-(avgLS - 1) * 3, -2, 2));
  }
  
  // 11. OI delta 7-day
  if (oiData.length >= 8) {
    const oiDelta = (oiData[oiData.length-1] - oiData[oiData.length-8]) / oiData[oiData.length-8] * 100;
    inputs.oi_7d_delta = oiDelta;
    categories.derivatives.push(clamp(oiDelta / 5, -2, 2));
  }
  
  // ─── FLOW (Volume + CVD) ───
  // 12. Daily volume trend
  const vols = btcD.map(c => c.v);
  if (n >= 20) {
    const volAvg5 = vols.slice(n-4,n+1).reduce((s,v)=>s+v,0)/5;
    const volAvg20 = vols.slice(n-19,n+1).reduce((s,v)=>s+v,0)/20;
    inputs.vol_ratio = volAvg5 / volAvg20;
    categories.flow.push(clamp((inputs.vol_ratio - 1) * 3, -2, 2));
  }
  
  // 13. CVD direction (daily)
  const deltas = btcD.map(c => (c.tbv||0) - (c.v - (c.tbv||0)));
  if (n >= 7) {
    const cvd7 = deltas.slice(n-6,n+1).reduce((s,v)=>s+v,0);
    const cvd14 = deltas.slice(Math.max(0,n-13),n+1).reduce((s,v)=>s+v,0);
    inputs.cvd_direction = cvd7 > 0 ? 'buying' : 'selling';
    categories.flow.push(cvd7 > 0 ? 1 : -1);
  }
  
  // ── AGGREGATE ──
  const weights = { momentum: 2.0, structure: 2.0, derivatives: 1.5, flow: 1.5 };
  let totalScore = 0, totalWeight = 0;
  const breakdown = {};
  
  for (const [cat, vals] of Object.entries(categories)) {
    if (!vals.length) continue;
    const avg = vals.reduce((s,v)=>s+v,0)/vals.length;
    const w = weights[cat] || 1;
    totalScore += avg * w;
    totalWeight += w;
    breakdown[cat] = { avg: parseFloat(avg.toFixed(3)), weight: w, count: vals.length };
  }
  
  const rawScore = totalWeight > 0 ? totalScore / totalWeight : 0;
  const mtpi = parseFloat(sigmoid(rawScore * 0.8).toFixed(4));
  
  return { mtpi, rawScore: parseFloat(rawScore.toFixed(3)), inputs, breakdown };
}

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIVE STRENGTH TOURNAMENT — v2 (Full Cross-Pair)
// 
// For each token: measure RS against EVERY other token in the pool.
//   SOL: SOL/BTC, SOL/ETH, SOL/BNB, SOL/XRP... (N-1 pairs)
//   Each pair: return ratio over 7d, 14d, 30d, 60d → average
//   Pool-wide RS = average of all pair RS scores
//   Then z-score pool-wide scores → true ranking
//
// A token wins only if it's beating the ENTIRE field, not just BTC.
// ═══════════════════════════════════════════════════════════════════════════════
async function runTournament() {
  // Fetch daily candles for all tokens
  const allCandles = {};
  const returns = {}; // { symbol: { 7: pct, 14: pct, 30: pct, 60: pct } }
  const PERIODS = [7, 14, 30, 60];
  
  for (const sym of TOKENS) {
    const cs = await fetchCandles(sym, '1d', 90);
    if (cs.length < 30) continue;
    allCandles[sym] = cs;
    const closes = cs.map(c => c.c);
    const n = closes.length - 1;
    
    returns[sym] = {};
    for (const p of PERIODS) {
      if (n >= p) {
        returns[sym][p] = (closes[n] - closes[n-p]) / closes[n-p] * 100;
      }
    }
  }
  
  const syms = Object.keys(returns);
  if (syms.length < 5) return [];
  
  // ── Cross-pair RS matrix ──
  // For each token, compute RS against every other token across all periods
  const poolRS = {}; // { symbol: average RS across all pairs and periods }
  
  for (const sym of syms) {
    const pairScores = [];
    
    for (const other of syms) {
      if (sym === other) continue;
      
      for (const p of PERIODS) {
        const symRet = returns[sym][p];
        const otherRet = returns[other][p];
        if (symRet === undefined || otherRet === undefined) continue;
        
        // RS ratio: how much sym outperforms other
        // Positive = sym winning, negative = sym losing
        // Use difference rather than ratio to handle negative returns cleanly
        pairScores.push(symRet - otherRet);
      }
    }
    
    poolRS[sym] = pairScores.length > 0
      ? pairScores.reduce((s,v) => s+v, 0) / pairScores.length
      : 0;
  }
  
  // ── Z-score the pool-wide RS ──
  const poolValues = syms.map(s => poolRS[s]);
  const poolZScores = zScoreArr(poolValues);
  
  // ── Build results with additional metrics ──
  const results = [];
  
  for (let i = 0; i < syms.length; i++) {
    const sym = syms[i];
    const cs = allCandles[sym];
    const closes = cs.map(c => c.c);
    const n = closes.length - 1;
    
    // Absolute momentum
    const mom7 = returns[sym][7] || 0;
    const mom30 = returns[sym][30] || 0;
    
    // Volume trend
    const vols = cs.map(c => c.v);
    const volRatio = n >= 14 ? (vols.slice(n-6,n+1).reduce((s,v)=>s+v,0)/7) / (vols.slice(n-13,n+1).reduce((s,v)=>s+v,0)/14) : 1;
    
    // RSI
    const rsi = calcRSI(closes);
    const rsiVal = rsi[n] || 50;
    
    // RS vs BTC specifically (for display)
    const btcRet7 = returns['BTCUSDT'] ? returns['BTCUSDT'][7] || 0 : 0;
    const btcRet30 = returns['BTCUSDT'] ? returns['BTCUSDT'][30] || 0 : 0;
    const rsVsBtc = ((mom7 - btcRet7) + (mom30 - btcRet30)) / 2;
    
    // Pool-wide RS z-score (the main ranking metric)
    const poolZ = poolZScores[i];
    
    // Final composite: pool RS z-score (60%) + volume (20%) + RSI momentum (20%)
    const volZ = zScoreArr(Object.values(allCandles).map(c => {
      const v = c.map(x=>x.v); const nn = v.length-1;
      return nn >= 14 ? (v.slice(nn-6,nn+1).reduce((s,x)=>s+x,0)/7)/(v.slice(nn-13,nn+1).reduce((s,x)=>s+x,0)/14) : 1;
    }))[i] || 0;
    
    const rsiZ = zScoreArr(syms.map(s => {
      const c = allCandles[s].map(x=>x.c);
      const r = calcRSI(c);
      return r[r.length-1] || 50;
    }))[i] || 0;
    
    const composite = poolZ * 0.6 + volZ * 0.2 + rsiZ * 0.2;
    
    results.push({
      symbol: sym,
      composite: parseFloat(composite.toFixed(4)),
      pool_rs: parseFloat(poolRS[sym].toFixed(3)),
      pool_z: parseFloat(poolZ.toFixed(3)),
      rs_vs_btc: parseFloat(rsVsBtc.toFixed(3)),
      mom_7d: parseFloat(mom7.toFixed(2)),
      mom_30d: parseFloat(mom30.toFixed(2)),
      vol_ratio: parseFloat(volRatio.toFixed(3)),
      rsi: parseFloat(rsiVal.toFixed(1)),
      price: closes[n],
      n_pairs: syms.length - 1,
    });
  }
  
  // Z-score the final composites
  const composites = results.map(r => r.composite);
  const finalZ = zScoreArr(composites);
  results.forEach((r, i) => { r.z_score = parseFloat(finalZ[i].toFixed(3)); });
  
  // Sort by z-score (best first)
  results.sort((a, b) => b.z_score - a.z_score);
  
  return results;
}

// ═══════════════════════════════════════════════════════════════════════════════
// ALLOCATION ENGINE — v2 (Prof-inspired LTPI×MTPI matrix)
//
// Key insight from prof:
//   - LTPI bearish ≠ go to cash. It means: avoid BTC leverage, reduce BTC exposure
//   - MTPI positive = deploy into RS winners REGARDLESS of LTPI
//   - LTPI controls: BTC allocation + leverage permission + defensive hedge %
//   - MTPI controls: overall deployment level + token count
//   - Gold (PAXG) is a valid defensive allocation
//   - Cash only when BOTH are deeply negative
// ═══════════════════════════════════════════════════════════════════════════════
function computeAllocation(ltpi, mtpi, tournament) {
  // Convert our 0-1 scale to prof's -1 to +1 for matrix logic
  const ltpiAdj = (ltpi - 0.5) * 2;  // 0→-1, 0.5→0, 1→+1
  const mtpiAdj = (mtpi - 0.5) * 2;
  
  // ── LTPI determines: BTC permission, defensive hedge %, leverage permission ──
  const btcAllowed = ltpiAdj > -0.2;          // BTC only when LTPI isn't bearish
  const btcLeverageAllowed = ltpiAdj > 0.3;   // Leverage only when LTPI clearly bullish
  const defensiveHedgePct = ltpiAdj < -0.3 ? 10 : ltpiAdj < 0 ? 5 : 0; // Gold allocation
  
  // ── MTPI determines: deployment level, token count ──
  let deployPct, maxTokens, riskLevel;
  
  if (mtpiAdj >= 0.5) {
    // MTPI strong positive — full deployment
    deployPct = 95; maxTokens = 3; riskLevel = 'AGGRESSIVE';
  } else if (mtpiAdj >= 0.2) {
    // MTPI moderate positive — high deployment
    deployPct = 80; maxTokens = 3; riskLevel = 'MODERATE';
  } else if (mtpiAdj >= -0.1) {
    // MTPI neutral — cautious deployment
    deployPct = 50; maxTokens = 2; riskLevel = 'CAUTIOUS';
  } else if (mtpiAdj >= -0.4) {
    // MTPI mildly negative — light deployment
    deployPct = 25; maxTokens = 1; riskLevel = 'DEFENSIVE';
  } else {
    // MTPI deeply negative — minimal to zero
    deployPct = 5; maxTokens = 1; riskLevel = 'RISK_OFF';
  }
  
  // ── Override: both deeply negative → full cash ──
  if (ltpiAdj < -0.5 && mtpiAdj < -0.3) {
    deployPct = 0; maxTokens = 0; riskLevel = 'CASH';
  }
  
  // ── Macro environment modifier ──
  // LTPI positive boosts deployment; LTPI negative reduces slightly but doesn't kill it
  if (ltpiAdj > 0.3) deployPct = Math.min(100, deployPct + 10);
  else if (ltpiAdj < -0.3) deployPct = Math.max(0, deployPct - 10);
  
  // ── Build allocation from RS tournament ──
  const allocations = [];
  let usedPct = 0;
  
  // Defensive hedge (gold) first — carved from total, not from deployment
  if (defensiveHedgePct > 0) {
    const goldToken = tournament.find(t => DEFENSIVE_TOKENS.has(t.symbol));
    if (goldToken) {
      allocations.push({
        symbol: goldToken.symbol, pct: defensiveHedgePct,
        z_score: goldToken.z_score, rs_vs_btc: goldToken.rs_vs_btc,
        price: goldToken.price, role: 'HEDGE',
      });
      usedPct += defensiveHedgePct;
    }
  }
  
  // RS winners (excluding defensive tokens and BTC if not allowed)
  const candidates = tournament.filter(t => {
    if (DEFENSIVE_TOKENS.has(t.symbol)) return false;
    if (t.symbol === BTC_TOKEN && !btcAllowed) return false;
    if (t.z_score < -0.5) return false; // skip weak tokens
    return true;
  });
  
  const remainingDeploy = Math.max(0, deployPct - usedPct);
  const selectedCount = Math.min(maxTokens, candidates.length);
  const selected = candidates.slice(0, selectedCount);
  
  if (selected.length > 0 && remainingDeploy > 0) {
    // Weight by z-score (stronger tokens get more)
    const totalZ = selected.reduce((s, t) => s + Math.max(t.z_score, 0.1), 0);
    for (const t of selected) {
      const weight = Math.max(t.z_score, 0.1) / totalZ;
      const pct = parseFloat((weight * remainingDeploy).toFixed(1));
      allocations.push({
        symbol: t.symbol, pct,
        z_score: t.z_score, rs_vs_btc: t.rs_vs_btc,
        price: t.price, role: t.symbol === BTC_TOKEN ? 'BTC' : 'RS_WINNER',
      });
      usedPct += pct;
    }
  }
  
  const cashPct = parseFloat((100 - usedPct).toFixed(1));
  
  return {
    risk_level: riskLevel,
    ltpi_adj: parseFloat(ltpiAdj.toFixed(3)),
    mtpi_adj: parseFloat(mtpiAdj.toFixed(3)),
    btc_allowed: btcAllowed,
    btc_leverage_allowed: btcLeverageAllowed,
    defensive_hedge_pct: defensiveHedgePct,
    deploy_pct: deployPct,
    max_tokens: maxTokens,
    allocations,
    cash_pct: cashPct,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// PORTFOLIO
// ═══════════════════════════════════════════════════════════════════════════════
function loadPortfolio() {
  try { return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8')); }
  catch {
    return {
      version: '1.0', last_updated: new Date().toISOString(),
      strategy: 'Macro Rotation — LTPI/MTPI + RS Tournament | Paper Trading',
      paper_portfolio: {
        starting_capital_usdc: 10000,
        current_capital_usdc: 10000,
        cash_usdc: 10000,
        positions: [],      // { symbol, entry_price, size_usdc, entry_time, pct }
        closed_trades: [],
        rebalance_log: [],
        stats: { total_rebalances: 0, total_trades: 0, wins: 0, losses: 0, total_pnl_usdc: 0 }
      }
    };
  }
}

function savePortfolio(data) {
  data.last_updated = new Date().toISOString();
  fs.mkdirSync(path.dirname(PORTFOLIO_FILE), { recursive: true });
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(data, null, 2));
}

async function rebalance(portfolio, allocation, tournament) {
  const p = portfolio.paper_portfolio;
  const now = new Date().toISOString();
  
  // Get current prices for all held positions
  for (const pos of p.positions) {
    try {
      await sleep(60);
      const ticker = await httpGet(`https://fapi.binance.com/fapi/v1/ticker/price?symbol=${pos.symbol}`);
      pos.current_price = parseFloat(ticker.price);
    } catch { pos.current_price = pos.entry_price; }
  }
  
  // Calculate current portfolio value
  let totalValue = p.cash_usdc;
  for (const pos of p.positions) {
    const pnl = (pos.current_price - pos.entry_price) / pos.entry_price * pos.size_usdc;
    totalValue += pos.size_usdc + pnl;
  }
  p.current_capital_usdc = parseFloat(totalValue.toFixed(2));
  
  // Target allocations
  const targetMap = {};
  for (const a of allocation.allocations) {
    targetMap[a.symbol] = { pct: a.pct, target_usdc: totalValue * a.pct / 100, price: a.price };
  }
  
  // Close positions not in target
  const newPositions = [];
  for (const pos of p.positions) {
    if (!targetMap[pos.symbol]) {
      // Close this position
      const pnlPct = (pos.current_price - pos.entry_price) / pos.entry_price * 100;
      const pnlUSD = pos.size_usdc * pnlPct / 100;
      p.cash_usdc += pos.size_usdc + pnlUSD;
      p.stats.total_trades++;
      if (pnlUSD > 0) p.stats.wins++; else p.stats.losses++;
      p.stats.total_pnl_usdc += pnlUSD;
      p.closed_trades.push({
        symbol: pos.symbol, entry_price: pos.entry_price, exit_price: pos.current_price,
        entry_time: pos.entry_time, exit_time: now,
        pnl_pct: parseFloat(pnlPct.toFixed(3)), pnl_usd: parseFloat(pnlUSD.toFixed(2)),
        size_usdc: pos.size_usdc, exit_reason: 'rotation',
      });
      console.log(`  🔄 CLOSE ${pos.symbol}: ${pnlPct >= 0 ? '+' : ''}${pnlPct.toFixed(2)}% ($${pnlUSD >= 0 ? '+' : ''}${pnlUSD.toFixed(2)})`);
    } else {
      // Keep, but adjust size if needed
      const target = targetMap[pos.symbol].target_usdc;
      const currentVal = pos.size_usdc * (1 + (pos.current_price - pos.entry_price) / pos.entry_price);
      const diff = target - currentVal;
      
      if (Math.abs(diff) / totalValue > 0.05) { // rebalance if >5% drift
        if (diff > 0) {
          // Add to position
          pos.size_usdc += diff;
          p.cash_usdc -= diff;
          console.log(`  📈 ADD ${pos.symbol}: +$${diff.toFixed(2)}`);
        } else {
          // Reduce position
          const reducePct = Math.abs(diff) / currentVal;
          const reduceUSD = pos.size_usdc * reducePct;
          const pnlPortion = reduceUSD * (pos.current_price - pos.entry_price) / pos.entry_price;
          pos.size_usdc -= reduceUSD;
          p.cash_usdc += reduceUSD + pnlPortion;
          console.log(`  📉 REDUCE ${pos.symbol}: -$${reduceUSD.toFixed(2)}`);
        }
      }
      pos.target_pct = targetMap[pos.symbol].pct;
      newPositions.push(pos);
      delete targetMap[pos.symbol];
    }
  }
  
  // Open new positions
  for (const [sym, target] of Object.entries(targetMap)) {
    if (target.target_usdc < 50) continue; // skip tiny positions
    if (p.cash_usdc < target.target_usdc) continue;
    
    const size = Math.min(target.target_usdc, p.cash_usdc);
    p.cash_usdc -= size;
    newPositions.push({
      symbol: sym, entry_price: target.price, current_price: target.price,
      size_usdc: parseFloat(size.toFixed(2)), entry_time: now, target_pct: target.pct,
    });
    console.log(`  🟢 OPEN ${sym}: $${size.toFixed(2)} (${target.pct}%) @ $${target.price.toFixed(4)}`);
  }
  
  p.positions = newPositions;
  p.stats.total_rebalances++;
  p.rebalance_log.push({
    time: now,
    capital: p.current_capital_usdc,
    positions: newPositions.map(pos => ({ symbol: pos.symbol, pct: pos.target_pct })),
    cash_pct: allocation.cash_pct,
  });
  
  // Trim log to last 90 entries
  if (p.rebalance_log.length > 90) p.rebalance_log = p.rebalance_log.slice(-90);
  
  return portfolio;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════
async function run() {
  const uaeTime = new Date().toLocaleString('en-AE', { timeZone: 'Asia/Dubai', hour12: false });
  console.log(`\n[${uaeTime} UAE] Macro Rotation — Daily Rebalance\n`);
  
  // 1. Compute LTPI
  console.log('📊 Computing LTPI...');
  const ltpiResult = await computeLTPI();
  console.log(`  LTPI: ${ltpiResult.ltpi.toFixed(4)} (raw: ${ltpiResult.rawScore}) ${ltpiResult.ltpi >= 0.5 ? '🟢 BULLISH' : '🔴 BEARISH'}`);
  
  // 2. Compute MTPI
  console.log('📊 Computing MTPI...');
  const mtpiResult = await computeMTPI();
  console.log(`  MTPI: ${mtpiResult.mtpi.toFixed(4)} (raw: ${mtpiResult.rawScore}) ${mtpiResult.mtpi >= 0.5 ? '🟢 BULLISH' : '🔴 BEARISH'}`);
  
  // 3. Run tournament
  console.log('🏆 Running RS Tournament...');
  const tournament = await runTournament();
  console.log(`  Top 5 (scored against ${tournament[0]?.n_pairs || '?'} peers):`);
  tournament.slice(0, 5).forEach((t, i) => {
    console.log(`    ${i+1}. ${t.symbol.padEnd(12)} z:${t.z_score.toFixed(2).padStart(6)} poolRS:${t.pool_rs.toFixed(1).padStart(6)} vsBTC:${t.rs_vs_btc.toFixed(1).padStart(6)} 7d:${t.mom_7d >= 0 ? '+' : ''}${t.mom_7d.toFixed(1)}% RSI:${t.rsi.toFixed(0)}`);
  });
  
  // 4. Compute allocation
  const allocation = computeAllocation(ltpiResult.ltpi, mtpiResult.mtpi, tournament);
  console.log(`\n  Risk Level: ${allocation.risk_level} | Deploy: ${allocation.deploy_pct}% | Cash: ${allocation.cash_pct}%`);
  console.log(`  BTC: ${allocation.btc_allowed ? '✅ allowed' : '❌ excluded'} | Leverage: ${allocation.btc_leverage_allowed ? '✅' : '❌'} | Hedge: ${allocation.defensive_hedge_pct}%`);
  console.log(`  Allocations:`);
  for (const a of allocation.allocations) {
    console.log(`    ${a.symbol.padEnd(12)} ${a.pct.toFixed(1)}% [${a.role}] (z:${a.z_score})`);
  }
  if (allocation.allocations.length === 0) console.log(`    100% CASH`);
  
  // 5. Rebalance portfolio
  console.log('\n🔄 Rebalancing...');
  let portfolio = loadPortfolio();
  
  // Store signals in portfolio for dashboard
  portfolio.ltpi = ltpiResult.ltpi;
  portfolio.ltpi_raw = ltpiResult.rawScore;
  portfolio.ltpi_breakdown = ltpiResult.breakdown;
  portfolio.mtpi = mtpiResult.mtpi;
  portfolio.mtpi_raw = mtpiResult.rawScore;
  portfolio.mtpi_breakdown = mtpiResult.breakdown;
  portfolio.allocation = allocation;
  portfolio.tournament_top10 = tournament.slice(0, 10);
  
  portfolio = await rebalance(portfolio, allocation, tournament);
  savePortfolio(portfolio);
  
  // 6. GitHub push
  try {
    const ghToken = fs.readFileSync(path.join(process.env.HOME, '.github_token'), 'utf8').trim();
    const content = Buffer.from(JSON.stringify(portfolio, null, 2)).toString('base64');
    const { execSync } = require('child_process');
    // Get SHA
    const shaResp = JSON.parse(execSync(`curl -sL -H "Authorization: token ${ghToken}" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-macro.json"`, { encoding: 'utf8', timeout: 10000 }).toString());
    const sha = shaResp.sha || '';
    const body = JSON.stringify({ message: 'trading: macro rotation update', content, sha: sha || undefined });
    execSync(`curl -sL -X PUT -H "Authorization: token ${ghToken}" -H "Accept: application/vnd.github.v3+json" -d '${body.replace(/'/g, "\\'")}' "https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-macro.json"`, { timeout: 15000 });
    console.log('GitHub updated ✅');
  } catch(e) { console.log('GitHub push failed:', e.message); }
  
  // Summary
  const p = portfolio.paper_portfolio;
  console.log(`\n${'═'.repeat(60)}`);
  console.log(`LTPI: ${ltpiResult.ltpi.toFixed(3)} (${allocation.ltpi_adj >= 0 ? '+' : ''}${allocation.ltpi_adj}) | MTPI: ${mtpiResult.mtpi.toFixed(3)} (${allocation.mtpi_adj >= 0 ? '+' : ''}${allocation.mtpi_adj}) | Risk: ${allocation.risk_level}`);
  console.log(`BTC: ${allocation.btc_allowed ? 'OK' : 'EXCLUDED'} | Deploy: ${allocation.deploy_pct}% | Cash: ${allocation.cash_pct}% | Hedge: ${allocation.defensive_hedge_pct}%`);
  console.log(`Portfolio: $${p.current_capital_usdc.toFixed(2)} | Cash: $${p.cash_usdc.toFixed(2)} | Positions: ${p.positions.length}`);
  console.log(`Trades: ${p.stats.total_trades} | WR: ${p.stats.total_trades > 0 ? (p.stats.wins/p.stats.total_trades*100).toFixed(0) : '—'}% | PnL: $${p.stats.total_pnl_usdc.toFixed(2)}`);
  console.log('Done ✅');
}

run().catch(e => { console.error('Fatal:', e.message, e.stack); process.exit(1); });
