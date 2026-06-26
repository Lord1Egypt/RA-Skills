#!/usr/bin/env node
/**
 * regime-scorer.js — Multi-Factor BTC Regime Scoring System
 * 
 * Three timeframes: Fast (15m), Medium (4h), Macro (1d)
 * Each timeframe aggregates multiple z-scored indicators into a composite score (-10 to +10)
 * 
 * INDICATORS PER TIMEFRAME:
 *   Trend:      EMA cross, ADX, price vs MA200, higher highs/lows
 *   Momentum:   RSI, MACD histogram, rate of change
 *   Volatility: BB width, ATR percentile, Keltner squeeze
 *   Volume:     OBV trend, volume z-score, CVD
 *   Derivatives: Funding rate, long/short ratio, open interest delta
 *   Sentiment:   Fear & Greed Index (macro only)
 * 
 * OUTPUT: regime.json consumed by all monitors + dashboard
 */
'use strict';
const https = require('https');
const fs    = require('fs');
const path  = require('path');

const REGIME_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/regime.json');

function httpGet(url, timeout = 10000) {
  return new Promise((res, rej) => {
    const r = https.get(url, resp => {
      let d = ''; resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    });
    r.on('error', rej);
    r.setTimeout(timeout, () => { r.destroy(); rej(new Error('timeout')); });
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ═══════════════════════════════════════════════════════════════════════════════
// MATH HELPERS
// ═══════════════════════════════════════════════════════════════════════════════
function calcEMA(v, p) { const k = 2/(p+1); let e = v[0]; return v.map((x,i) => { if(i>0) e=x*k+e*(1-k); return e; }); }
function calcSMA(v, p) { return v.map((_,i) => i < p-1 ? null : v.slice(i-p+1,i+1).reduce((s,x)=>s+x,0)/p); }
function calcATR(cs, p=14) {
  const tr = cs.map((c,i) => i===0 ? c.h-c.l : Math.max(c.h-c.l, Math.abs(c.h-cs[i-1].c), Math.abs(c.l-cs[i-1].c)));
  const a = []; for (let i=0;i<cs.length;i++) { if(i<p-1){a.push(null);continue;} if(i===p-1){a.push(tr.slice(0,p).reduce((s,v)=>s+v,0)/p);} else{a.push((a[i-1]*(p-1)+tr[i])/p);} } return a;
}
function calcRSI(c, p=14) {
  const r = Array(c.length).fill(null); let ag=0,al=0;
  for(let i=1;i<=p;i++){const d=c[i]-c[i-1];if(d>0)ag+=d;else al-=d;} ag/=p;al/=p;
  r[p]=al===0?100:100-100/(1+ag/al);
  for(let i=p+1;i<c.length;i++){const d=c[i]-c[i-1];ag=(ag*(p-1)+(d>0?d:0))/p;al=(al*(p-1)+(d<0?-d:0))/p;r[i]=al===0?100:100-100/(1+ag/al);}
  return r;
}
function calcMACD(c) {
  const e12=calcEMA(c,12),e26=calcEMA(c,26);
  const ml=c.map((_,i)=>e12[i]-e26[i]);
  const sig=calcEMA(ml.slice(25),9);
  const hist=[];for(let i=0;i<c.length;i++){if(i<33){hist.push(null);continue;}hist.push(ml[i]-(sig[i-25]||0));}
  return { line: ml, signal: sig, histogram: hist };
}
function calcOBV(cs) {
  const o=[0];for(let i=1;i<cs.length;i++){if(cs[i].c>cs[i-1].c)o.push(o[i-1]+cs[i].v);else if(cs[i].c<cs[i-1].c)o.push(o[i-1]-cs[i].v);else o.push(o[i-1]);}return o;
}
function calcADX(cs, p=14) {
  if (cs.length < p * 3) return Array(cs.length).fill(null);
  const pdm=[0],ndm=[0],tr=[cs[0].h-cs[0].l];
  for(let i=1;i<cs.length;i++){
    const upMove=cs[i].h-cs[i-1].h, downMove=cs[i-1].l-cs[i].l;
    pdm.push(upMove>downMove&&upMove>0?upMove:0);
    ndm.push(downMove>upMove&&downMove>0?downMove:0);
    tr.push(Math.max(cs[i].h-cs[i].l,Math.abs(cs[i].h-cs[i-1].c),Math.abs(cs[i].l-cs[i-1].c)));
  }
  const atr=calcEMA(tr,p),spdm=calcEMA(pdm,p),sndm=calcEMA(ndm,p);
  const pdi=[],ndi=[],dx=[];
  for(let i=0;i<cs.length;i++){
    if(!atr[i]||atr[i]===0){pdi.push(null);ndi.push(null);dx.push(null);continue;}
    const pd=spdm[i]/atr[i]*100,nd=sndm[i]/atr[i]*100;
    pdi.push(pd);ndi.push(nd);
    const sum=pd+nd;dx.push(sum===0?0:Math.abs(pd-nd)/sum*100);
  }
  const adx=calcEMA(dx.map(v=>v||0),p);
  return adx.map((v,i)=>dx[i]!==null?v:null);
}
function calcBBWidth(closes, p=20) {
  return closes.map((_,i) => {
    if (i < p-1) return null;
    const sl = closes.slice(i-p+1,i+1);
    const m = sl.reduce((a,b)=>a+b,0)/p;
    const std = Math.sqrt(sl.reduce((a,b)=>a+(b-m)**2,0)/p);
    return m === 0 ? 0 : (4 * std) / m * 100; // BB width as % of price
  });
}
function calcROC(closes, p=10) {
  return closes.map((v,i) => i < p ? null : (v - closes[i-p]) / closes[i-p] * 100);
}
function zScore(value, arr) {
  const valid = arr.filter(v => v !== null && v !== undefined && !isNaN(v));
  if (valid.length < 5) return 0;
  const mean = valid.reduce((s,v)=>s+v,0)/valid.length;
  const std = Math.sqrt(valid.reduce((s,v)=>s+(v-mean)**2,0)/valid.length);
  return std === 0 ? 0 : (value - mean) / std;
}
function percentile(value, arr) {
  const valid = arr.filter(v => v !== null && !isNaN(v)).sort((a,b) => a - b);
  if (!valid.length) return 50;
  let below = 0; for (const v of valid) if (v < value) below++;
  return below / valid.length * 100;
}
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function sigmoid(x) { return 1 / (1 + Math.exp(-x)); }
function higherHighsLows(cs, lookback = 20) {
  if (cs.length < lookback * 2) return 0;
  const recent = cs.slice(-lookback), prior = cs.slice(-lookback*2, -lookback);
  const rHighs = recent.map(c=>c.h), rLows = recent.map(c=>c.l);
  const pHighs = prior.map(c=>c.h), pLows = prior.map(c=>c.l);
  const hh = Math.max(...rHighs) > Math.max(...pHighs) ? 1 : -1;
  const hl = Math.min(...rLows) > Math.min(...pLows) ? 1 : -1;
  return (hh + hl) / 2; // -1 to +1
}

// ═══════════════════════════════════════════════════════════════════════════════
// DATA FETCHERS
// ═══════════════════════════════════════════════════════════════════════════════
async function fetchCandles(sym, interval, limit) {
  await sleep(50);
  try {
    const r = await httpGet(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=${interval}&limit=${limit}`);
    return r.map(k => ({ ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4], tbv:+k[9]*+k[4] }));
  } catch { return []; }
}

async function fetchFundingRate(sym = 'BTCUSDT') {
  try {
    const r = await httpGet(`https://fapi.binance.com/fapi/v1/fundingRate?symbol=${sym}&limit=30`);
    return r.map(f => ({ ts: f.fundingTime, rate: parseFloat(f.fundingRate) }));
  } catch { return []; }
}

async function fetchLongShortRatio(sym = 'BTCUSDT', period = '4h') {
  try {
    const r = await httpGet(`https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=${sym}&period=${period}&limit=30`);
    return r.map(d => ({ ts: d.timestamp, ratio: parseFloat(d.longShortRatio) }));
  } catch { return []; }
}

async function fetchOpenInterest(sym = 'BTCUSDT', period = '4h') {
  try {
    const r = await httpGet(`https://fapi.binance.com/futures/data/openInterestHist?symbol=${sym}&period=${period}&limit=30`);
    return r.map(d => ({ ts: d.timestamp, oi: parseFloat(d.sumOpenInterest), oiVal: parseFloat(d.sumOpenInterestValue) }));
  } catch { return []; }
}

// ─── FRED Macro Data (no API key — CSV via curl for reliability) ───────────────
function fetchFRED(seriesId, startDate = '2023-01-01') {
  return new Promise((res) => {
    const url = `https://fred.stlouisfed.org/graph/fredgraph.csv?id=${seriesId}&cosd=${startDate}`;
    const { execSync } = require('child_process');
    try {
      const csv = execSync(`curl -sL --max-time 12 "${url}"`, { encoding: 'utf8', timeout: 15000 });
      const lines = csv.trim().split('\n').slice(1);
      const data = lines.map(l => {
        const [date, val] = l.split(',');
        const v = parseFloat(val);
        return { date, ts: new Date(date).getTime(), value: isNaN(v) ? null : v };
      }).filter(d => d.value !== null);
      res(data);
    } catch(e) { res([]); }
  });
}

async function fetchMacroLiquidity() {
  const [walcl, tga, rrp, m2, dxy, dgs10, t10yie, dff] = await Promise.all([
    fetchFRED('WALCL', '2024-01-01'),   // Fed Balance Sheet (weekly, millions)
    fetchFRED('WTREGEN', '2024-01-01'), // Treasury General Account (weekly, millions)
    fetchFRED('RRPONTSYD', '2024-01-01'), // Reverse Repo (daily, billions)
    fetchFRED('M2SL', '2023-01-01'),     // M2 Money Supply (monthly, billions)
    fetchFRED('DTWEXBGS', '2024-01-01'), // Trade-Weighted Dollar Index
    fetchFRED('DGS10', '2024-01-01'),    // 10Y Treasury Yield
    fetchFRED('T10YIE', '2024-01-01'),   // 10Y Breakeven Inflation
    fetchFRED('DFF', '2024-01-01'),      // Fed Funds Rate
  ]);
  return { walcl, tga, rrp, m2, dxy, dgs10, t10yie, dff };
}

function scoreMacroLiquidity(macro) {
  const scores = {};
  
  // 1. Net Liquidity = Fed Balance Sheet - TGA - RRP
  //    WALCL in millions, TGA in millions, RRP in billions (convert to millions)
  if (macro.walcl.length >= 4 && macro.tga.length >= 4 && macro.rrp.length >= 4) {
    const latestBS = macro.walcl[macro.walcl.length - 1].value; // millions
    const latestTGA = macro.tga[macro.tga.length - 1].value;    // millions
    const latestRRP = macro.rrp[macro.rrp.length - 1].value * 1000; // billions→millions
    const netLiq = latestBS - latestTGA - latestRRP;
    
    // Compare to 4 weeks ago
    const bs4w = macro.walcl.length >= 5 ? macro.walcl[macro.walcl.length - 5].value : latestBS;
    const tga4w = macro.tga.length >= 5 ? macro.tga[macro.tga.length - 5].value : latestTGA;
    const rrp4w = macro.rrp.length >= 5 ? macro.rrp[macro.rrp.length - 5].value * 1000 : latestRRP;
    const netLiq4w = bs4w - tga4w - rrp4w;
    
    const liqChange = (netLiq - netLiq4w) / netLiq4w * 100;
    // Expanding liquidity = bullish, contracting = bearish
    scores.net_liquidity = clamp(liqChange * 3, -2, 2); // 0.67% change = +2
    scores.net_liquidity_raw = parseFloat((netLiq / 1e6).toFixed(3)); // in trillions
    scores.net_liquidity_delta = parseFloat(liqChange.toFixed(3));
  } else { scores.net_liquidity = 0; }
  
  // 2. M2 Money Supply YoY growth rate
  if (macro.m2.length >= 13) {
    const latest = macro.m2[macro.m2.length - 1].value;
    const yoyAgo = macro.m2[macro.m2.length - 13].value; // ~12 months prior
    const yoyGrowth = (latest - yoyAgo) / yoyAgo * 100;
    // Positive M2 growth = bullish, negative = bearish
    // Historical: M2 growth 5-10% = normal, >10% = very bullish, <0% = bearish
    scores.m2_yoy = clamp((yoyGrowth - 3) / 4, -2, 2); // 3% = neutral, 7%+ = +1, 11%+ = +2
    scores.m2_yoy_raw = parseFloat(yoyGrowth.toFixed(2));
    
    // M2 momentum: 3-month change direction
    if (macro.m2.length >= 4) {
      const m3ago = macro.m2[macro.m2.length - 4].value;
      const m3delta = (latest - m3ago) / m3ago * 100;
      scores.m2_momentum = clamp(m3delta * 2, -1, 1); // 0.5% in 3mo = +1
    } else { scores.m2_momentum = 0; }
  } else { scores.m2_yoy = 0; scores.m2_momentum = 0; }
  
  // 3. DXY (Dollar Strength) — INVERSE correlation with BTC
  if (macro.dxy.length >= 20) {
    const latestDXY = macro.dxy[macro.dxy.length - 1].value;
    const dxy20ago = macro.dxy[Math.max(0, macro.dxy.length - 21)].value;
    const dxyChange = (latestDXY - dxy20ago) / dxy20ago * 100;
    // Rising dollar = bearish for BTC, falling = bullish
    scores.dxy = clamp(-dxyChange * 2, -2, 2); // 1% dollar rise = -2
    scores.dxy_raw = latestDXY;
    scores.dxy_delta = parseFloat(dxyChange.toFixed(3));
  } else { scores.dxy = 0; }
  
  // 4. Real Yields (10Y - breakeven inflation)
  //    High real yields = bad for BTC (money flows to bonds), low/negative = good
  if (macro.dgs10.length >= 5 && macro.t10yie.length >= 5) {
    const nominal = macro.dgs10[macro.dgs10.length - 1].value;
    const breakeven = macro.t10yie[macro.t10yie.length - 1].value;
    const realYield = nominal - breakeven;
    // Real yield > 2% = very bearish, < 0 = very bullish, 1% = neutral
    scores.real_yields = clamp(-(realYield - 1) * 1.5, -2, 2);
    scores.real_yields_raw = parseFloat(realYield.toFixed(3));
    
    // Direction matters too
    const nom5 = macro.dgs10[macro.dgs10.length - 6].value;
    const be5 = macro.t10yie[macro.t10yie.length - 6].value;
    const realYield5 = nom5 - be5;
    const ryDelta = realYield - realYield5;
    scores.real_yields_momentum = clamp(-ryDelta * 3, -1, 1); // rising real yields = bearish
  } else { scores.real_yields = 0; scores.real_yields_momentum = 0; }
  
  // 5. Fed Funds Rate trajectory
  if (macro.dff.length >= 30) {
    const latest = macro.dff[macro.dff.length - 1].value;
    const dff30 = macro.dff[Math.max(0, macro.dff.length - 31)].value;
    const rateChange = latest - dff30;
    // Cutting rates = bullish, hiking = bearish
    scores.fed_rate = clamp(-rateChange * 2, -2, 2); // 1% cut = +2
    scores.fed_rate_raw = latest;
    scores.fed_rate_delta = parseFloat(rateChange.toFixed(3));
  } else { scores.fed_rate = 0; }
  
  return scores;
}

async function fetchFearGreed() {
  try {
    const r = await httpGet('https://api.alternative.me/fng/?limit=30');
    if (r && r.data) return r.data.map(d => ({ ts: d.timestamp * 1000, value: parseInt(d.value), label: d.value_classification }));
  } catch {}
  return [];
}

// ═══════════════════════════════════════════════════════════════════════════════
// INDICATOR SCORING (each returns -2 to +2, z-scored where applicable)
// ═══════════════════════════════════════════════════════════════════════════════

function scoreTrend(cs, closes) {
  const scores = {};
  const n = cs.length - 1;
  
  // 1. EMA Cross (fast vs slow)
  const ema20 = calcEMA(closes, 20), ema50 = calcEMA(closes, 50);
  const emaDiff = (ema20[n] - ema50[n]) / closes[n] * 100;
  scores.ema_cross = clamp(emaDiff * 5, -2, 2); // scale: 0.4% diff = +2
  
  // 2. ADX (trend strength, direction-agnostic)
  const adx = calcADX(cs);
  const adxVal = adx[n] || 20;
  scores.adx = adxVal > 25 ? clamp((adxVal - 25) / 15, 0, 2) : clamp(-(25 - adxVal) / 15, -1, 0);
  // ADX only measures strength; combine with direction
  if (ema20[n] < ema50[n]) scores.adx *= -1; // strong downtrend = negative
  
  // 3. Price vs MA200
  const ema200 = calcEMA(closes, Math.min(200, closes.length - 1));
  const distMA200 = (closes[n] - ema200[n]) / ema200[n] * 100;
  scores.price_vs_ma200 = clamp(distMA200 / 5, -2, 2);
  
  // 4. Higher highs / higher lows
  const hhhl = higherHighsLows(cs, 20);
  scores.structure = hhhl * 2; // -2 to +2
  
  return scores;
}

function scoreMomentum(closes) {
  const scores = {};
  const n = closes.length - 1;
  
  // 1. RSI position + z-score
  const rsi = calcRSI(closes);
  if (rsi[n] !== null) {
    const rsiCentered = (rsi[n] - 50) / 25; // 50=neutral, 75=+1, 25=-1
    const rsiWindow = rsi.slice(Math.max(0, n-30), n).filter(v => v !== null);
    const rsiZ = zScore(rsi[n], rsiWindow);
    scores.rsi = clamp((rsiCentered + rsiZ * 0.3) * 1.5, -2, 2);
  } else { scores.rsi = 0; }
  
  // 2. MACD histogram z-score + direction
  const macd = calcMACD(closes);
  if (macd.histogram[n] !== null) {
    const macdWindow = macd.histogram.slice(Math.max(0, n-30), n).filter(v => v !== null);
    const macdZ = zScore(macd.histogram[n], macdWindow);
    const rising = n > 0 && macd.histogram[n] > (macd.histogram[n-1] || 0) ? 0.5 : -0.5;
    scores.macd = clamp((macdZ + rising) * 0.8, -2, 2);
  } else { scores.macd = 0; }
  
  // 3. Rate of Change (10-period)
  const roc = calcROC(closes, 10);
  if (roc[n] !== null) {
    const rocWindow = roc.slice(Math.max(0, n-30), n).filter(v => v !== null);
    const rocZ = zScore(roc[n], rocWindow);
    scores.roc = clamp(rocZ * 0.8, -2, 2);
  } else { scores.roc = 0; }
  
  return scores;
}

function scoreVolatility(cs, closes) {
  const scores = {};
  const n = cs.length - 1;
  
  // 1. BB Width percentile (high = trending, low = squeeze)
  const bbw = calcBBWidth(closes, 20);
  if (bbw[n] !== null) {
    const bbwWindow = bbw.slice(Math.max(0, n-60), n+1).filter(v => v !== null);
    const pct = percentile(bbw[n], bbwWindow);
    // Low BB width (squeeze) = mean reversion likely. High = trend following
    scores.bb_width = clamp((pct - 50) / 25, -2, 2); // >75th = trending, <25th = squeeze
  } else { scores.bb_width = 0; }
  
  // 2. ATR percentile
  const atrs = calcATR(cs, 14);
  if (atrs[n] !== null) {
    const atrPct = atrs[n] / closes[n] * 100; // ATR as % of price
    const atrWindow = atrs.slice(Math.max(0, n-60), n+1).filter(v => v !== null).map((v,i) => v / closes[Math.max(0, n-60)+i] * 100);
    const pct = percentile(atrPct, atrWindow);
    scores.atr_pctile = clamp((pct - 50) / 25, -2, 2);
  } else { scores.atr_pctile = 0; }
  
  // 3. Keltner squeeze detection (BB inside Keltner = compression)
  // Simplified: compare BB width to ATR ratio
  if (bbw[n] !== null && atrs[n] !== null) {
    const keltnerWidth = atrs[n] * 3 / closes[n] * 100; // ~3×ATR bands
    const squeeze = bbw[n] < keltnerWidth; // BB inside Keltner = squeeze
    scores.squeeze = squeeze ? -1 : 1; // squeeze = expect breakout (direction unknown)
  } else { scores.squeeze = 0; }
  
  return scores;
}

function scoreVolume(cs) {
  const scores = {};
  const n = cs.length - 1;
  
  // 1. OBV trend (z-scored 5-period OBV delta)
  const obv = calcOBV(cs);
  if (n > 10) {
    const obvDelta = obv[n] - obv[n-5];
    const obvDeltas = [];
    for (let j = Math.max(6, n-30); j < n; j++) obvDeltas.push(obv[j] - obv[j-5]);
    scores.obv = clamp(zScore(obvDelta, obvDeltas) * 0.8, -2, 2);
  } else { scores.obv = 0; }
  
  // 2. Volume z-score (current vs recent average)
  const vols = cs.map(c => c.v);
  const volWindow = vols.slice(Math.max(0, n-30), n);
  const volZ = zScore(vols[n], volWindow);
  scores.volume_z = clamp(volZ * 0.5, -2, 2); // high volume = confirms move
  
  // 3. CVD (taker buy pressure)
  const deltas = cs.map(c => { const buy = c.tbv || 0; return buy - (c.v - buy); });
  const deltaWindow = deltas.slice(Math.max(0, n-30), n);
  const cvdZ = zScore(deltas[n], deltaWindow);
  scores.cvd = clamp(cvdZ * 0.8, -2, 2);
  
  return scores;
}

function scoreDerivatives(funding, lsRatio, oiData) {
  const scores = {};
  
  // 1. Funding rate (positive = longs pay, crowded long = bearish contrarian)
  if (funding.length >= 3) {
    const recent = funding.slice(-3).map(f => f.rate);
    const avgFunding = recent.reduce((s,v) => s+v, 0) / recent.length;
    // Extreme positive funding = bearish (crowded long), extreme negative = bullish
    scores.funding = clamp(-avgFunding * 5000, -2, 2); // 0.01% = -0.5 (slightly bearish)
  } else { scores.funding = 0; }
  
  // 2. Long/Short ratio
  if (lsRatio.length >= 5) {
    const recent = lsRatio.slice(-5).map(d => d.ratio);
    const avgRatio = recent.reduce((s,v) => s+v, 0) / recent.length;
    // >1 = more longs (contrarian bearish), <1 = more shorts (contrarian bullish)
    scores.ls_ratio = clamp(-(avgRatio - 1) * 3, -2, 2);
  } else { scores.ls_ratio = 0; }
  
  // 3. Open Interest delta (rising OI + rising price = strong trend)
  if (oiData.length >= 5) {
    const oiVals = oiData.map(d => d.oiVal);
    const oiDelta = (oiVals[oiVals.length-1] - oiVals[0]) / oiVals[0] * 100;
    scores.oi_delta = clamp(oiDelta / 5, -2, 2); // 5% OI increase = +1
  } else { scores.oi_delta = 0; }
  
  return scores;
}

function scoreSentiment(fng) {
  const scores = {};
  
  if (fng.length >= 1) {
    const latest = fng[0].value; // 0-100
    // Contrarian: extreme fear = bullish, extreme greed = bearish
    // But also direct: moderate greed = healthy trend
    const centered = (latest - 50) / 50; // -1 to +1
    
    // Below 25 = extreme fear (contrarian bullish)
    // 25-45 = fear (mildly bullish)
    // 45-55 = neutral
    // 55-75 = greed (mildly bullish trend confirmation)
    // Above 75 = extreme greed (contrarian bearish)
    if (latest < 25) scores.fear_greed = 1.5; // extreme fear = buy
    else if (latest < 45) scores.fear_greed = 0.5;
    else if (latest <= 55) scores.fear_greed = 0;
    else if (latest <= 75) scores.fear_greed = 0.5; // greed confirms trend
    else scores.fear_greed = -1.5; // extreme greed = caution
    
    scores.fear_greed_raw = latest;
    scores.fear_greed_label = fng[0].label;
  } else { scores.fear_greed = 0; }
  
  return scores;
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSITE SCORING
// ═══════════════════════════════════════════════════════════════════════════════

function computeComposite(categories) {
  // Weights per category
  const weights = {
    trend: 2.0,
    momentum: 1.5,
    volatility: 1.0,
    volume: 1.5,
    derivatives: 1.5,
    sentiment: 1.0,
    liquidity: 3.0,  // Heaviest weight — "trade the tide, not the waves"
  };
  
  let totalScore = 0, totalWeight = 0;
  const breakdown = {};
  
  for (const [cat, scores] of Object.entries(categories)) {
    const vals = Object.values(scores).filter(v => typeof v === 'number');
    if (!vals.length) continue;
    const catAvg = vals.reduce((s,v) => s+v, 0) / vals.length;
    const w = weights[cat] || 1;
    totalScore += catAvg * w;
    totalWeight += w;
    breakdown[cat] = { avg: parseFloat(catAvg.toFixed(2)), weight: w, indicators: scores };
  }
  
  const composite = totalWeight > 0 ? totalScore / totalWeight : 0;
  // Scale to -10 to +10
  const scaled = clamp(composite * 5, -10, 10);
  
  return {
    score: parseFloat(scaled.toFixed(1)),
    signal: scaled > 3 ? 'BULLISH' : scaled > 1 ? 'LEAN_BULL' : scaled < -3 ? 'BEARISH' : scaled < -1 ? 'LEAN_BEAR' : 'NEUTRAL',
    breakdown,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// TIMEFRAME SCORERS
// ═══════════════════════════════════════════════════════════════════════════════

async function scoreFast() {
  const cs = await fetchCandles('BTCUSDT', '15m', 200);
  if (cs.length < 100) return { score: 0, signal: 'NO_DATA', breakdown: {} };
  const closes = cs.map(c => c.c);
  
  return computeComposite({
    trend: scoreTrend(cs, closes),
    momentum: scoreMomentum(closes),
    volatility: scoreVolatility(cs, closes),
    volume: scoreVolume(cs),
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// STPI — Short Term Probability Indicator (for day trading)
// 15m + 1h indicators + fast derivatives → 0-1 probability
// Updated hourly. Gates day trading entries at 0.5 threshold.
// ═══════════════════════════════════════════════════════════════════════════════
async function computeSTPI() {
  const [cs15m, cs1h] = await Promise.all([
    fetchCandles('BTCUSDT', '15m', 200),
    fetchCandles('BTCUSDT', '1h', 100),
  ]);
  if (cs15m.length < 100 || cs1h.length < 60) return { stpi: 0.5, rawScore: 0, breakdown: {} };
  
  const closes15 = cs15m.map(c => c.c);
  const closes1h = cs1h.map(c => c.c);
  const n15 = closes15.length - 1;
  const n1h = closes1h.length - 1;
  
  const categories = { trend_15m: [], momentum_15m: [], structure_1h: [], volatility: [], flow: [] };
  
  // ─── 15m TREND ───
  const ema8 = calcEMA(closes15, 8), ema21 = calcEMA(closes15, 21), ema50_15 = calcEMA(closes15, 50);
  
  // 1. EMA8 vs EMA21 spread
  const spread821 = (ema8[n15] - ema21[n15]) / closes15[n15] * 100;
  categories.trend_15m.push(clamp(spread821 * 10, -2, 2));
  
  // 2. EMA alignment (8 > 21 > 50)
  const aligned = ema8[n15] > ema21[n15] && ema21[n15] > ema50_15[n15];
  const inverted = ema8[n15] < ema21[n15] && ema21[n15] < ema50_15[n15];
  categories.trend_15m.push(aligned ? 2 : inverted ? -2 : 0);
  
  // 3. Price vs 50 EMA (short term trend)
  const dist50 = (closes15[n15] - ema50_15[n15]) / ema50_15[n15] * 100;
  categories.trend_15m.push(clamp(dist50 * 3, -2, 2));
  
  // ─── 15m MOMENTUM ───
  const rsi15 = calcRSI(closes15, 14);
  if (rsi15[n15] !== null) {
    const rsiCentered = (rsi15[n15] - 50) / 25;
    categories.momentum_15m.push(clamp(rsiCentered * 2, -2, 2));
  }
  
  const macd15 = calcMACD(closes15);
  if (macd15.histogram[n15] !== null) {
    const macdWindow = macd15.histogram.slice(Math.max(0, n15-30), n15).filter(v => v !== null);
    const mz = zScore(macd15.histogram[n15], macdWindow);
    categories.momentum_15m.push(clamp(mz * 0.8, -2, 2));
    // MACD rising/falling
    const rising = n15 > 0 && macd15.histogram[n15] > (macd15.histogram[n15-1] || 0);
    categories.momentum_15m.push(rising ? 1 : -1);
  }
  
  // ROC 5-period on 15m (~1.25 hours)
  if (n15 >= 5) {
    const roc5 = (closes15[n15] - closes15[n15-5]) / closes15[n15-5] * 100;
    categories.momentum_15m.push(clamp(roc5 * 5, -2, 2));
  }
  
  // ─── 1h STRUCTURE ───
  const ema9_1h = calcEMA(closes1h, 9), ema21_1h = calcEMA(closes1h, 21), ema50_1h = calcEMA(closes1h, 50);
  
  // 1h EMA alignment
  const aligned1h = ema9_1h[n1h] > ema21_1h[n1h] && ema21_1h[n1h] > ema50_1h[n1h];
  const inverted1h = ema9_1h[n1h] < ema21_1h[n1h] && ema21_1h[n1h] < ema50_1h[n1h];
  categories.structure_1h.push(aligned1h ? 2 : inverted1h ? -2 : 0);
  
  // 1h RSI
  const rsi1h = calcRSI(closes1h);
  if (rsi1h[n1h] !== null) {
    categories.structure_1h.push(clamp((rsi1h[n1h] - 50) / 25 * 1.5, -2, 2));
  }
  
  // 1h MACD direction
  const macd1h = calcMACD(closes1h);
  if (macd1h.histogram[n1h] !== null) {
    categories.structure_1h.push(macd1h.histogram[n1h] > 0 ? 1 : -1);
    const rising1h = n1h > 0 && macd1h.histogram[n1h] > (macd1h.histogram[n1h-1] || 0);
    categories.structure_1h.push(rising1h ? 0.5 : -0.5);
  }
  
  // ─── VOLATILITY (15m) ───
  const bbw = calcBBWidth(closes15, 20);
  if (bbw[n15] !== null) {
    const bbwWindow = bbw.slice(Math.max(0, n15-60), n15+1).filter(v => v !== null);
    const pct = percentile(bbw[n15], bbwWindow);
    categories.volatility.push(clamp((pct - 50) / 25, -2, 2));
  }
  
  // ATR percentile
  const atrs15 = calcATR(cs15m, 14);
  if (atrs15[n15] !== null) {
    const atrPct = atrs15[n15] / closes15[n15] * 100;
    categories.volatility.push(clamp((atrPct - 0.3) * 5, -2, 2)); // 0.3% = neutral for 15m
  }
  
  // ─── FLOW (volume + CVD on 15m) ───
  const vols15 = cs15m.map(c => c.v);
  const volWindow = vols15.slice(Math.max(0, n15-30), n15);
  const volZ = zScore(vols15[n15], volWindow);
  categories.flow.push(clamp(volZ * 0.5, -2, 2));
  
  // CVD
  const deltas = cs15m.map(c => { const buy = c.tbv || 0; return buy - (c.v - buy); });
  const deltaWindow = deltas.slice(Math.max(0, n15-30), n15);
  const cvdZ = zScore(deltas[n15], deltaWindow);
  categories.flow.push(clamp(cvdZ * 0.8, -2, 2));
  
  // OBV trend
  const obv = calcOBV(cs15m);
  if (n15 > 10) {
    const obvDelta = obv[n15] - obv[n15-5];
    const obvDs = [];
    for (let j = Math.max(6, n15-30); j < n15; j++) obvDs.push(obv[j] - obv[j-5]);
    categories.flow.push(clamp(zScore(obvDelta, obvDs) * 0.6, -2, 2));
  }
  
  // ── AGGREGATE ──
  const weights = { trend_15m: 2.5, momentum_15m: 2.0, structure_1h: 2.0, volatility: 1.0, flow: 1.5 };
  let totalScore = 0, totalWeight = 0;
  const breakdown = {};
  
  for (const [cat, vals] of Object.entries(categories)) {
    if (!vals.length) continue;
    const avg = vals.reduce((s,v) => s+v, 0) / vals.length;
    const w = weights[cat] || 1;
    totalScore += avg * w;
    totalWeight += w;
    breakdown[cat] = { avg: parseFloat(avg.toFixed(3)), weight: w, count: vals.length };
  }
  
  const rawScore = totalWeight > 0 ? totalScore / totalWeight : 0;
  const stpi = parseFloat(sigmoid(rawScore * 0.8).toFixed(4));
  
  return { stpi, rawScore: parseFloat(rawScore.toFixed(3)), signal: stpi >= 0.5 ? 'BULLISH' : 'BEARISH', breakdown };
}

async function scoreMedium() {
  const cs = await fetchCandles('BTCUSDT', '4h', 200);
  if (cs.length < 100) return { score: 0, signal: 'NO_DATA', breakdown: {} };
  const closes = cs.map(c => c.c);
  
  const [funding, lsRatio, oiData] = await Promise.all([
    fetchFundingRate(),
    fetchLongShortRatio('BTCUSDT', '4h'),
    fetchOpenInterest('BTCUSDT', '4h'),
  ]);
  
  return computeComposite({
    trend: scoreTrend(cs, closes),
    momentum: scoreMomentum(closes),
    volatility: scoreVolatility(cs, closes),
    volume: scoreVolume(cs),
    derivatives: scoreDerivatives(funding, lsRatio, oiData),
  });
}

async function scoreMacro() {
  const cs = await fetchCandles('BTCUSDT', '1d', 250);
  if (cs.length < 60) return { score: 0, signal: 'NO_DATA', breakdown: {} };
  const closes = cs.map(c => c.c);
  
  const [funding, lsRatio, oiData, fng, macroData] = await Promise.all([
    fetchFundingRate(),
    fetchLongShortRatio('BTCUSDT', '1d'),
    fetchOpenInterest('BTCUSDT', '1d'),
    fetchFearGreed(),
    fetchMacroLiquidity(),
  ]);
  
  return computeComposite({
    trend: scoreTrend(cs, closes),
    momentum: scoreMomentum(closes),
    volatility: scoreVolatility(cs, closes),
    volume: scoreVolume(cs),
    derivatives: scoreDerivatives(funding, lsRatio, oiData),
    sentiment: scoreSentiment(fng),
    liquidity: scoreMacroLiquidity(macroData),
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// REGIME CLASSIFICATION
// ═══════════════════════════════════════════════════════════════════════════════

function classifyRegime(fast, medium, macro) {
  // Determine overall market type
  const avgScore = (fast.score * 0.2 + medium.score * 0.4 + macro.score * 0.4);
  
  // Volatility regime from medium timeframe
  const medVol = medium.breakdown.volatility;
  const isSqueezing = medVol && medVol.indicators && medVol.indicators.squeeze < 0;
  const isHighVol = medVol && medVol.avg > 1;
  
  let marketType = 'MIXED';
  if (isSqueezing) marketType = 'COMPRESSION'; // expect breakout
  else if (isHighVol && Math.abs(avgScore) > 3) marketType = 'TRENDING';
  else if (!isHighVol && Math.abs(avgScore) < 2) marketType = 'RANGE_BOUND';
  else if (Math.abs(avgScore) > 5) marketType = 'STRONG_TREND';
  
  // Strategy recommendation
  let recommendation = 'NEUTRAL';
  if (marketType === 'TRENDING' || marketType === 'STRONG_TREND') {
    recommendation = avgScore > 0 ? 'TREND_FOLLOW_LONG' : 'TREND_FOLLOW_SHORT';
  } else if (marketType === 'RANGE_BOUND') {
    recommendation = 'MEAN_REVERSION';
  } else if (marketType === 'COMPRESSION') {
    recommendation = 'WAIT_BREAKOUT';
  }
  
  // Position sizing suggestion
  const confidence = Math.min(Math.abs(avgScore) / 7, 1); // 0-1
  const sizeMult = avgScore > 1 ? (0.5 + confidence * 0.5) : avgScore < -1 ? 0.5 * (1 - confidence * 0.3) : 0.5;
  
  return {
    composite_score: parseFloat(avgScore.toFixed(1)),
    composite_signal: avgScore > 3 ? 'BULLISH' : avgScore > 1 ? 'LEAN_BULL' : avgScore < -3 ? 'BEARISH' : avgScore < -1 ? 'LEAN_BEAR' : 'NEUTRAL',
    market_type: marketType,
    recommendation,
    confidence: parseFloat(confidence.toFixed(2)),
    size_multiplier: parseFloat(sizeMult.toFixed(2)),
    allow_new_longs: avgScore > -3, // block longs in strong downtrend
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function computeMTPIProbability() {
  // MTPI for swing trading — mirrors macro-rotation MTPI logic
  // but outputs as 0-1 probability for regime.json consumption
  const cs = await fetchCandles('BTCUSDT', '4h', 200);
  if (cs.length < 100) return { mtpi: 0.5, rawScore: 0, signal: 'NO_DATA', breakdown: {} };
  const closes = cs.map(c => c.c);
  const n = closes.length - 1;
  
  let funding = [], lsRatio = [], oiData = [];
  try { const r = await httpGet('https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=30'); funding = r.map(f => parseFloat(f.fundingRate)); } catch {}
  try { const r = await httpGet('https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=BTCUSDT&period=4h&limit=30'); lsRatio = r.map(d => parseFloat(d.longShortRatio)); } catch {}
  try { const r = await httpGet('https://fapi.binance.com/futures/data/openInterestHist?symbol=BTCUSDT&period=4h&limit=30'); oiData = r.map(d => parseFloat(d.sumOpenInterestValue)); } catch {}
  
  const categories = { momentum: [], structure: [], derivatives: [], flow: [] };
  
  // Momentum
  const rsi = calcRSI(closes);
  if (rsi[n] !== null) categories.momentum.push(clamp((rsi[n] - 50) / 20, -2, 2));
  const roc7 = n >= 42 ? (closes[n] - closes[n-42]) / closes[n-42] * 100 : 0; // 42×4h = 7 days
  categories.momentum.push(clamp(roc7 * 0.3, -2, 2));
  const macd = calcMACD(closes);
  if (macd.histogram[n] !== null) {
    categories.momentum.push(macd.histogram[n] > 0 ? 1 : -1);
    if (n > 0) categories.momentum.push(macd.histogram[n] > (macd.histogram[n-1]||0) ? 0.5 : -0.5);
  }
  
  // Structure
  const ema20 = calcEMA(closes, 20), ema50 = calcEMA(closes, 50);
  categories.structure.push(ema20[n] > ema50[n] ? 1.5 : -1.5);
  categories.structure.push(clamp((closes[n] - ema50[n]) / ema50[n] * 100 * 0.5, -2, 2));
  const hhhl = higherHighsLows(cs, 30);
  categories.structure.push(hhhl * 2);
  
  // Derivatives (data is already parsed to numbers)
  if (funding.length >= 3) {
    const valid = funding.slice(-3).filter(v => !isNaN(v));
    if (valid.length) { const avgF = valid.reduce((s,v)=>s+v,0)/valid.length; categories.derivatives.push(clamp(-avgF * 3000, -2, 2)); }
  }
  if (lsRatio.length >= 5) {
    const valid = lsRatio.slice(-5).filter(v => !isNaN(v));
    if (valid.length) { const avgLS = valid.reduce((s,v)=>s+v,0)/valid.length; categories.derivatives.push(clamp(-(avgLS - 1) * 3, -2, 2)); }
  }
  if (oiData.length >= 5) {
    const valid = oiData.filter(v => !isNaN(v));
    if (valid.length >= 2) { const oiDelta = (valid[valid.length-1] - valid[0]) / valid[0] * 100; categories.derivatives.push(clamp(oiDelta / 5, -2, 2)); }
  }
  
  // Flow
  const obv = calcOBV(cs);
  if (n > 10) {
    const obvDelta = obv[n] - obv[n-5];
    const obvDs = []; for (let j = Math.max(6,n-30); j < n; j++) obvDs.push(obv[j]-obv[j-5]);
    categories.flow.push(clamp(zScore(obvDelta, obvDs) * 0.8, -2, 2));
  }
  const deltas = cs.map(c => { const buy = c.tbv || 0; return buy - (c.v - buy); });
  const dw = deltas.slice(Math.max(0,n-30),n);
  categories.flow.push(clamp(zScore(deltas[n], dw) * 0.8, -2, 2));
  
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
  
  return { mtpi, rawScore: parseFloat(rawScore.toFixed(3)), signal: mtpi >= 0.5 ? 'BULLISH' : 'BEARISH', breakdown };
}

async function run() {
  const uaeTime = new Date().toLocaleString('en-AE', { timeZone: 'Asia/Dubai', hour12: false });
  console.log(`[${uaeTime} UAE] Regime scorer running...`);
  
  const [fast, medium, macro, stpiResult, mtpiResult] = await Promise.all([
    scoreFast(),
    scoreMedium(),
    scoreMacro(),
    computeSTPI(),
    computeMTPIProbability(),
  ]);
  
  const classification = classifyRegime(fast, medium, macro);
  
  const regime = {
    updated: new Date().toISOString(),
    fast: { timeframe: '15m', ...fast },
    medium: { timeframe: '4h', ...medium },
    macro: { timeframe: '1d', ...macro },
    stpi: stpiResult,   // for day trading v6
    mtpi: mtpiResult,   // for swing v2
    classification,
  };
  
  // Save
  fs.mkdirSync(path.dirname(REGIME_FILE), { recursive: true });
  fs.writeFileSync(REGIME_FILE, JSON.stringify(regime, null, 2));
  
  // Console summary
  const arrow = s => s > 3 ? '🟢↑' : s > 1 ? '🟡↗' : s < -3 ? '🔴↓' : s < -1 ? '🟠↘' : '⚪→';
  console.log(`\n  Fast (15m):  ${arrow(fast.score)} ${fast.score.toFixed(1).padStart(5)} | ${fast.signal}`);
  console.log(`  Medium (4h): ${arrow(medium.score)} ${medium.score.toFixed(1).padStart(5)} | ${medium.signal}`);
  console.log(`  Macro (1d):  ${arrow(macro.score)} ${macro.score.toFixed(1).padStart(5)} | ${macro.signal}`);
  console.log(`\n  STPI (day):  ${stpiResult.stpi >= 0.5 ? '🟢' : '🔴'} ${(stpiResult.stpi*100).toFixed(1).padStart(5)}% | ${stpiResult.signal} (raw: ${stpiResult.rawScore})`);
  console.log(`  MTPI (swing):${mtpiResult.mtpi >= 0.5 ? '🟢' : '🔴'} ${(mtpiResult.mtpi*100).toFixed(1).padStart(5)}% | ${mtpiResult.signal} (raw: ${mtpiResult.rawScore})`);
  console.log(`\n  Composite:   ${arrow(classification.composite_score)} ${classification.composite_score.toFixed(1).padStart(5)} | ${classification.composite_signal}`);
  console.log(`  Market:      ${classification.market_type} | Rec: ${classification.recommendation}`);
  console.log(`  Confidence:  ${(classification.confidence * 100).toFixed(0)}% | Size mult: ${classification.size_multiplier}x`);
  console.log(`  Longs OK:    ${classification.allow_new_longs ? '✅' : '⛔'}`);
  
  // Show breakdown
  for (const [tf, data] of [['Fast', fast], ['Medium', medium], ['Macro', macro]]) {
    console.log(`\n  ${tf} Breakdown:`);
    for (const [cat, info] of Object.entries(data.breakdown)) {
      const indicators = Object.entries(info.indicators || {}).map(([k,v]) => `${k}:${typeof v === 'number' ? v.toFixed(1) : v}`).join(' ');
      console.log(`    ${cat.padEnd(12)} avg:${info.avg.toFixed(1).padStart(5)} w:${info.weight} | ${indicators}`);
    }
  }
  
  console.log('\nDone ✅');
}

// Export for use as module
module.exports = { run, scoreFast, scoreMedium, scoreMacro, classifyRegime };

// Run if called directly
if (require.main === module) {
  run().catch(e => { console.error('Error:', e.message); process.exit(1); });
}
