#!/usr/bin/env node
/**
 * paper-monitor-v5.js — Live Paper Trading Monitor
 * SMC v5.0 — Hybrid SMC + TA + CVD Confirmation
 * Runs every 1h (XX:01 UTC). Scans all 29 tokens.
 * SMC structural signal + z-scored TA (≥5) + strict CVD delta (z≥0.5).
 * Separate portfolio from v4.0 for A/B comparison.
 */
'use strict';
const https = require('https');
const fs    = require('fs');
const path  = require('path');

const PORTFOLIO_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/portfolio-v5.json');
const JOURNAL_FILE   = path.join(process.env.HOME, '.openclaw/workspace/trading/journal-v5.json');
const LOCK_FILE      = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/orchestrator-lock.json');

const TOKENS = [
  'BTCUSDT','ETHUSDT','SOLUSDT','BNBUSDT','XRPUSDT','DOGEUSDT','AVAXUSDT','LINKUSDT',
  'ARBUSDT','OPUSDT','SUIUSDT','APTUSDT','INJUSDT','SEIUSDT','FETUSDT','RENDERUSDT',
  'TAOUSDT','NEARUSDT','WIFUSDT','JUPUSDT','TIAUSDT','DYMUSDT','STRKUSDT','TONUSDT',
  'NOTUSDT','EIGENUSDT','GRASSUSDT','VIRTUALUSDT','AKTUSDT',
];

const P = { swN:3, fvgAge:8, tr:0.03, maxH:12, maxConcurrent:10, posPct:0.10,
  // v5.0 z-score params (Config H: SMC+TA≥5+CVD z≥0.5)
  volZThreshold: 1.0, volLookback: 30,
  fvgZThreshold: 0.5, fvgLookback: 50,
  slAtrMult: 1.5, tpAtrMult: 3.0, atrPeriod: 14,
  taMinScore: 5, taZLookback: 30,
  cvdZThreshold: 0.5, cvdLookback: 30,
};

function apiFetch2(url, token) {
  return new Promise((res, rej) => {
    const r = require('https').get(url, { headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github.v3+json', 'User-Agent': 'Jarvis' } }, resp => {
      let d = ''; resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    }); r.on('error', rej); r.setTimeout(10000, () => { r.destroy(); rej(new Error('timeout')); });
  });
}
function apiFetch2Put(url, token, body) {
  return new Promise((res, rej) => {
    const opts = require('url').parse(url);
    opts.method = 'PUT';
    opts.headers = { Authorization: `token ${token}`, Accept: 'application/vnd.github.v3+json', 'Content-Type': 'application/json', 'User-Agent': 'Jarvis', 'Content-Length': Buffer.byteLength(body) };
    const r = require('https').request(opts, resp => {
      let d = ''; resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    }); r.on('error', rej); r.write(body); r.end();
  });
}
function apiFetch(url) {
  return new Promise((res, rej) => {
    const r = https.get(url, resp => {
      let d = '';
      resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    });
    r.on('error', rej);
    r.setTimeout(10000, () => { r.destroy(); rej(new Error('timeout')); });
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

function calcEMA(v, p) {
  const k = 2/(p+1); let e = v[0];
  return v.map((x,i) => { if(i>0) e=x*k+e*(1-k); return e; });
}

function zScore(value, arr) {
  if (arr.length < 2) return 0;
  const mean = arr.reduce((s,v)=>s+v,0)/arr.length;
  const std = Math.sqrt(arr.reduce((s,v)=>s+(v-mean)**2,0)/arr.length);
  if (std === 0) return 0;
  return (value - mean) / std;
}

function calcATR(cs, period=14) {
  const trs = cs.map((c,i) => {
    if (i===0) return c.h - c.l;
    const prev = cs[i-1].c;
    return Math.max(c.h - c.l, Math.abs(c.h - prev), Math.abs(c.l - prev));
  });
  const atrs = [];
  for (let i=0; i<cs.length; i++) {
    if (i < period-1) { atrs.push(null); continue; }
    if (i === period-1) {
      atrs.push(trs.slice(0, period).reduce((s,v)=>s+v,0)/period);
    } else {
      atrs.push((atrs[i-1]*(period-1)+trs[i])/period);
    }
  }
  return atrs;
}

function calcSMA(v, p) {
  return v.map((_, i) => {
    if (i < p-1) return null;
    return v.slice(i-p+1, i+1).reduce((s,x)=>s+x,0)/p;
  });
}

function calcRSI(closes, period=14) {
  const rsi = new Array(closes.length).fill(null);
  let avgGain = 0, avgLoss = 0;
  for (let i = 1; i <= period; i++) {
    const d = closes[i] - closes[i-1];
    if (d > 0) avgGain += d; else avgLoss += Math.abs(d);
  }
  avgGain /= period; avgLoss /= period;
  rsi[period] = avgLoss === 0 ? 100 : 100 - 100/(1+avgGain/avgLoss);
  for (let i = period+1; i < closes.length; i++) {
    const d = closes[i] - closes[i-1];
    avgGain = (avgGain*(period-1) + (d>0?d:0)) / period;
    avgLoss = (avgLoss*(period-1) + (d<0?Math.abs(d):0)) / period;
    rsi[i] = avgLoss === 0 ? 100 : 100 - 100/(1+avgGain/avgLoss);
  }
  return rsi;
}

function calcMACD(closes) {
  const e12 = calcEMA(closes, 12), e26 = calcEMA(closes, 26);
  const macdLine = closes.map((_, i) => e12[i] - e26[i]);
  const signal = calcEMA(macdLine.slice(25), 9);
  const histogram = [];
  for (let i = 0; i < closes.length; i++) {
    if (i < 33) { histogram.push(null); continue; }
    histogram.push(macdLine[i] - (signal[i-25] || 0));
  }
  return { macdLine, histogram };
}

function calcOBV(cs) {
  const obv = [0];
  for (let i = 1; i < cs.length; i++) {
    if (cs[i].c > cs[i-1].c) obv.push(obv[i-1] + cs[i].v);
    else if (cs[i].c < cs[i-1].c) obv.push(obv[i-1] - cs[i].v);
    else obv.push(obv[i-1]);
  }
  return obv;
}

function taConfluenceScore(cs, idx) {
  const closes = cs.map(c => c.c);
  const rsi = calcRSI(closes, 14);
  const macd = calcMACD(closes);
  const obv = calcOBV(cs);
  const ema9 = calcEMA(closes, 9);
  const ema21 = calcEMA(closes, 21);
  const bbSma = calcSMA(closes, 20);
  
  const i = idx;
  const ZLB = P.taZLookback;
  let score = 0;
  
  // Z-scored RSI
  if (rsi[i] !== null) {
    const rsiWindow = rsi.slice(Math.max(0,i-ZLB), i).filter(v=>v!==null);
    const rsiZ = zScore(rsi[i], rsiWindow);
    if (rsiZ > 0.3 && rsi[i] < 78) score += 2;
    if (rsiZ > 1.0 && rsi[i] < 75) score += 1;
  }
  
  // Z-scored MACD histogram
  if (macd.histogram[i] !== null) {
    const macdWindow = macd.histogram.slice(Math.max(0,i-ZLB), i).filter(v=>v!==null);
    const macdZ = zScore(macd.histogram[i], macdWindow);
    if (macdZ > 0.3) score += 1;
    if (i > 0 && macd.histogram[i] !== null && macd.histogram[i-1] !== null && macd.histogram[i] > macd.histogram[i-1]) score += 1;
  }
  
  // EMA alignment (9 > 21)
  if (ema9[i] > ema21[i]) score += 2;
  
  // BB position (sweet spot)
  if (bbSma[i] !== null && i >= 19) {
    const slice = closes.slice(i-19, i+1);
    const std = Math.sqrt(slice.reduce((s,v)=>s+(v-bbSma[i])**2,0)/20);
    const upper = bbSma[i] + 2*std;
    const lower = bbSma[i] - 2*std;
    const range = upper - lower;
    if (range > 0) {
      const bbPct = (closes[i] - lower) / range;
      if (bbPct > 0.5 && bbPct < 0.85) score += 2;
    }
  }
  
  // Z-scored OBV
  if (i > 10) {
    const obvDelta = obv[i] - obv[i-5];
    const obvDeltas = [];
    for (let j = Math.max(6, i-ZLB); j < i; j++) {
      obvDeltas.push(obv[j] - obv[j-5]);
    }
    const obvZ = zScore(obvDelta, obvDeltas);
    if (obvZ > 0.5) score += 1;
    if (obvZ > 1.0) score += 1;
  }
  
  return score; // max ~11
}

async function getBTCRegime() {
  try {
    const r = await apiFetch('https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h&limit=60');
    const closes = r.map(k => parseFloat(k[4]));
    const e20 = calcEMA(closes, 20), e50 = calcEMA(closes, 50);
    return e20[e20.length-1] > e50[e50.length-1] ? 'bullish' : 'bearish';
  } catch { return 'unknown'; }
}

async function getBTCFastRegime() {
  try {
    const r = await apiFetch('https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m&limit=30');
    const closes = r.map(k => parseFloat(k[4]));
    const e8 = calcEMA(closes, 8), e21 = calcEMA(closes, 21);
    const fast = e8[e8.length-1], slow = e21[e21.length-1];
    // Also check momentum: is price accelerating down?
    const pctFromSlow = (fast - slow) / slow * 100;
    // bullish: fast > slow, neutral: within 0.15%, bearish: fast < slow
    if (pctFromSlow > 0.15) return { trend: 'bullish', spread: pctFromSlow };
    if (pctFromSlow < -0.15) return { trend: 'bearish', spread: pctFromSlow };
    return { trend: 'neutral', spread: pctFromSlow };
  } catch { return { trend: 'unknown', spread: 0 }; }
}

async function getCandles(sym, limit=100) {
  try {
    await sleep(80);
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=1h&limit=${limit}`);
    return r.map(k => ({
      ts:k[0], o:parseFloat(k[1]), h:parseFloat(k[2]), l:parseFloat(k[3]), c:parseFloat(k[4]),
      v:parseFloat(k[5])*parseFloat(k[4]),
      tbv:parseFloat(k[9])*parseFloat(k[4])  // taker buy quote volume
    }));
  } catch { return []; }
}

function calcCVDDelta(cs) {
  // Delta per candle = taker buy - taker sell (taker sell = total - taker buy)
  return cs.map(c => {
    const buyVol = c.tbv || 0;
    const sellVol = (c.v || 0) - buyVol;
    return buyVol - sellVol;
  });
}

function detectSignal(cs) {
  // Find swing highs
  const hi = new Array(cs.length).fill(null);
  const n = P.swN;
  for (let i=n; i<cs.length-n; i++) {
    let isH=true;
    for (let j=1;j<=n;j++) if(cs[i-j].h>=cs[i].h||cs[i+j].h>=cs[i].h) isH=false;
    if(isH) hi[i]=cs[i].h;
  }
  
  // Precompute ATR for SL/TP
  const atrs = calcATR(cs, P.atrPeriod);
  
  // Check last 5 candles for BoS + FVG
  for (let i=cs.length-5; i<cs.length-1; i++) {
    if (i < n+2) continue;
    // BoS: close breaks prior swing high
    let bosIdx = -1;
    for (let j=i-1; j>=Math.max(0,i-60); j--) {
      if (hi[j]!==null && cs[i].c>hi[j]) { bosIdx=j; break; }
    }
    if (bosIdx < 0) continue;
    // FVG within 3 candles after BoS
    for (let j=Math.max(2,i-3); j<=i; j++) {
      const gap = cs[j].l - cs[j-2].h;
      if (gap <= 0) continue;
      const gapPct = gap / cs[j].c;
      
      // v3.2: Z-scored FVG size (must be 0.5σ above recent average)
      const recentGaps = [];
      for (let g=Math.max(2, j-P.fvgLookback); g<j; g++) {
        const pg = cs[g].l - cs[g-2].h;
        if (pg > 0) recentGaps.push(pg / cs[g].c);
      }
      const fvgZ = zScore(gapPct, recentGaps);
      if (fvgZ < P.fvgZThreshold) continue;

      // Check if price is retesting the FVG right now (latest candle)
      const fvgLo=cs[j-2].h, fvgHi=cs[j].l, fvgMid=(fvgLo+fvgHi)/2;
      const latest=cs[cs.length-1];
      const lastIdx = cs.length - 1;
      if (!(latest.l<=fvgHi && latest.h>=fvgLo)) continue;

      // v3.2: Z-scored volume (must be 1.0σ above recent average)
      const volWindow = cs.slice(Math.max(0, lastIdx-P.volLookback), lastIdx).map(c=>c.v);
      const volZ = zScore(latest.v, volWindow);
      if (volZ < P.volZThreshold) continue;

      // v3.2: ATR-based SL/TP
      const atr = atrs[lastIdx];
      if (!atr) continue;
      
      const ep = Math.min(latest.c, fvgMid);
      
      // SL: max of (OB low, entry - 1.5×ATR)
      let obLo = ep - atr * P.slAtrMult;
      for (let k=bosIdx-1; k>=Math.max(0,bosIdx-15); k--) {
        if (cs[k].c<cs[k].o) { obLo=cs[k].l; break; }
      }
      const sl = Math.max(obLo*0.999, ep - atr * P.slAtrMult);
      const tp = ep + atr * P.tpAtrMult;
      
      if (sl >= ep) continue;
      return { ep, sl, tp, fvgMid, gap: gapPct, volZ: volZ.toFixed(1), fvgZ: fvgZ.toFixed(1), atr };
    }
  }
  return null;
}

function loadPortfolio() {
  try {
    return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
  } catch {
    return {
      version: '1.0',
      last_updated: new Date().toISOString(),
      strategy: 'SMC v5.0 — Hybrid SMC+TA+CVD | Paper Trading',
      btc_regime: 'unknown',
      paper_portfolio: {
        starting_capital_usdc: 1000,
        current_capital_usdc: 1000,
        deployed_usdc: 0,
        open_positions: [],
        closed_trades: [],
        stats: { total_trades:0, wins:0, losses:0, total_pnl_usdc:0 }
      }
    };
  }
}

function savePortfolio(data) {
  data.last_updated = new Date().toISOString();
  fs.mkdirSync(path.dirname(PORTFOLIO_FILE), { recursive: true });
  fs.writeFileSync(PORTFOLIO_FILE, JSON.stringify(data, null, 2));
}

async function run() {
  const uaeTime = new Date().toLocaleString('en-AE', { timeZone: 'Asia/Dubai', hour12: false });
  console.log(`\n[${uaeTime} UAE] Paper monitor running...`);

  const portfolio = loadPortfolio();
  const p = portfolio.paper_portfolio;

  // 1. Check BTC regime (macro + fast)
  const btcRegime = await getBTCRegime();
  const btcFast = await getBTCFastRegime();
  portfolio.btc_regime = btcRegime;
  portfolio.btc_fast_regime = btcFast.trend;
  portfolio.btc_fast_spread = parseFloat(btcFast.spread.toFixed(3));
  const btcBull = btcRegime === 'bullish';
  const sizeMultiplier = btcBull ? 1.0 : 0.5;
  // Fast regime gates new entries — if bearish on 15m, skip new longs
  const fastAllowEntry = btcFast.trend !== 'bearish';
  console.log(`BTC regime: ${btcRegime} → position size: ${btcBull ? '10%' : '5%'}`);
  console.log(`BTC fast (15m): ${btcFast.trend} (spread: ${btcFast.spread.toFixed(3)}%)${!fastAllowEntry ? ' ⛔ NEW ENTRIES BLOCKED' : ' ✅'}`);

  // 2. Close expired positions
  const now = Date.now();
  const stillOpen = [];
  for (const pos of p.open_positions) {
    const ageH = (now - new Date(pos.entry_time).getTime()) / 3600000;
    // Get current price
    try {
      await sleep(80);
      const ticker = await apiFetch(`https://fapi.binance.com/fapi/v1/ticker/price?symbol=${pos.symbol}`);
      const price = parseFloat(ticker.price);
      pos.current_price = price;

      let closed = false;
      let exitType = '', exitPrice = price, pnlPct = 0;

      // Check SL
      if (price <= pos.sl_price) {
        exitType = 'SL'; exitPrice = pos.sl_price; closed = true;
      }
      // Check TP1 (if not yet hit)
      else if (!pos.tp1_hit && price >= pos.tp_price) {
        pos.tp1_hit = true;
        pos.half_price = pos.tp_price;
        pos.trail_peak = price;
        stillOpen.push(pos);
        console.log(`  📈 ${pos.symbol} TP1 hit at $${price.toFixed(4)} — trailing stop active`);
        continue;
      }
      // Check trailing stop after TP1
      else if (pos.tp1_hit) {
        if (price > (pos.trail_peak || pos.tp_price)) pos.trail_peak = price;
        const trailSL = (pos.trail_peak || price) * (1 - P.tr);
        if (price <= trailSL) {
          exitType = 'TRAIL'; exitPrice = trailSL; closed = true;
          pnlPct = ((pos.half_price - pos.entry_price)*0.5 + (exitPrice - pos.entry_price)*0.5) / pos.entry_price * 100;
        }
      }
      // Time exit
      else if (ageH >= P.maxH) {
        exitType = 'TIME'; exitPrice = price; closed = true;
      }

      if (closed) {
        if (pnlPct === 0) pnlPct = (exitPrice - pos.entry_price) / pos.entry_price * 100;
        const pnlUSD = pos.size_usdc * pnlPct / 100;
        p.current_capital_usdc += pnlUSD;
        p.stats.total_trades++;
        if (pnlUSD > 0) p.stats.wins++; else p.stats.losses++;
        p.stats.total_pnl_usdc += pnlUSD;

        const trade = {
          symbol: pos.symbol,
          entry_price: pos.entry_price,
          exit_price: exitPrice,
          entry_time: pos.entry_time,
          exit_time: new Date().toISOString(),
          held_hours: parseFloat(ageH.toFixed(1)),
          pnl_pct: parseFloat(pnlPct.toFixed(3)),
          pnl_usd: parseFloat(pnlUSD.toFixed(2)),
          exit_type: exitType,
          size_usdc: pos.size_usdc,
          btc_bull: pos.btc_bull_at_entry,
        };
        p.closed_trades.push(trade);
        console.log(`  ${pnlUSD > 0 ? '✅' : '❌'} ${pos.symbol} CLOSED | ${exitType} | ${pnlPct >= 0 ? '+' : ''}${pnlPct.toFixed(2)}% | $${pnlUSD >= 0 ? '+' : ''}${pnlUSD.toFixed(2)}`);
      } else {
        stillOpen.push(pos);
      }
    } catch(e) {
      stillOpen.push(pos); // keep open on error
    }
  }
  p.open_positions = stillOpen;

  // 3. Scan for new signals (gated by fast regime + orchestrator lock)
  let swingLockedSymbols = new Set();
  try {
    const lock = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8'));
    swingLockedSymbols = new Set(lock.swing_symbols || []);
    if (swingLockedSymbols.size > 0) console.log(`Orchestrator: ${swingLockedSymbols.size} symbols locked by swing: ${[...swingLockedSymbols].join(', ')}`);
  } catch {}
  
  if (p.open_positions.length < P.maxConcurrent && fastAllowEntry) {
    const openSymbols = new Set(p.open_positions.map(pos => pos.symbol));
    for (const sym of TOKENS) {
      if (p.open_positions.length >= P.maxConcurrent) break;
      if (openSymbols.has(sym)) continue; // already in position
      if (swingLockedSymbols.has(sym)) continue; // swing holds this

      const cs = await getCandles(sym, 80);
      if (cs.length < 60) continue;

      const signal = detectSignal(cs);
      if (!signal) continue;

      // v4.0: TA confluence confirmation
      const ta = taConfluenceScore(cs, cs.length - 1);
      if (ta < P.taMinScore) continue;

      // v5.0: CVD delta confirmation (z ≥ 0.5 = strong buying aggression)
      const deltas = calcCVDDelta(cs);
      const lastIdx = cs.length - 1;
      const deltaWindow = deltas.slice(Math.max(0, lastIdx - P.cvdLookback), lastIdx);
      const cvdZ = zScore(deltas[lastIdx], deltaWindow);
      if (cvdZ < P.cvdZThreshold) continue;

      const posSize = p.current_capital_usdc * P.posPct * sizeMultiplier;
      const pos = {
        symbol: sym,
        entry_price: signal.ep,
        sl_price: signal.sl,
        tp_price: signal.tp,
        size_usdc: posSize,
        entry_time: new Date().toISOString(),
        btc_bull_at_entry: btcBull,
        tp1_hit: false,
        trail_peak: null,
        half_price: null,
        current_price: signal.ep,
      };
      p.open_positions.push(pos);
      console.log(`  🟢 NEW SIGNAL: ${sym} | Entry: $${signal.ep.toFixed(4)} | SL: $${signal.sl.toFixed(4)} | TP: $${signal.tp.toFixed(4)} | Size: $${posSize.toFixed(2)} | volZ:${signal.volZ} fvgZ:${signal.fvgZ} TA:${ta}/11 CVD:${cvdZ.toFixed(1)}`);
    }
  }

  // 4. Update deployed
  p.deployed_usdc = p.open_positions.reduce((s, pos) => s + pos.size_usdc, 0);

  // 5. Save locally + update orchestrator lock
  savePortfolio(portfolio);
  try {
    let lock = {};
    try { lock = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8')); } catch {}
    lock.day_trading_symbols = p.open_positions.map(pos => pos.symbol);
    lock.day_trading_updated = new Date().toISOString();
    fs.writeFileSync(LOCK_FILE, JSON.stringify(lock, null, 2));
  } catch {}

  // 6. Push to GitHub (feeds Vercel dashboard)
  try {
    const fs2 = require('fs'), path2 = require('path');
    const ghToken = fs2.readFileSync(path2.join(process.env.HOME, '.github_token'), 'utf8').trim();
    const content = Buffer.from(JSON.stringify(portfolio, null, 2)).toString('base64');

    // Get current SHA
    const shaRes = await apiFetch2(`https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-v5.json`, ghToken);
    const sha = shaRes.sha || '';

    const body = JSON.stringify({ message: 'trading: v5 portfolio update', content, sha: sha || undefined });
    await apiFetch2Put(`https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-v5.json`, ghToken, body);
    console.log('GitHub portfolio.json updated ✅');
  } catch(e) {
    console.log('GitHub push failed (non-critical):', e.message);
  }

  const totalPnl = p.current_capital_usdc - p.starting_capital_usdc;
  const wr = p.stats.total_trades > 0 ? (p.stats.wins / p.stats.total_trades * 100).toFixed(1) : '—';
  console.log(`Portfolio: $${p.current_capital_usdc.toFixed(2)} | PnL: ${totalPnl >= 0 ? '+' : ''}$${totalPnl.toFixed(2)} | WR: ${wr}% | Open: ${p.open_positions.length}/10`);

  // 7. Log observations (append to trading/observations.md for any notable events)
  try {
    const OBS_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/observations.md');
    const closedThisRun = p.closed_trades.filter(t => {
      const exitAge = (now - new Date(t.exit_time).getTime()) / 60000;
      return exitAge < 35; // closed in last 35 min (within this cycle)
    });
    if (closedThisRun.length > 0 || !fastAllowEntry) {
      const ts = new Date().toISOString().replace('T',' ').slice(0,19) + ' UTC';
      let note = `\n## [${ts}] Auto-Observation\n`;
      note += `**Macro regime:** ${btcRegime} | **Fast regime (15m):** ${btcFast.trend} (${btcFast.spread.toFixed(3)}%)\n`;
      if (!fastAllowEntry) note += `**⛔ Fast filter blocked new entries** — BTC 15m trend bearish\n`;
      if (closedThisRun.length > 0) {
        note += `**Closed this cycle:**\n`;
        for (const t of closedThisRun) {
          note += `- ${t.symbol}: ${t.exit_type} | ${t.pnl_pct >= 0 ? '+' : ''}${t.pnl_pct}% ($${t.pnl_usd >= 0 ? '+' : ''}${t.pnl_usd}) | held ${t.held_hours}h | BTC bull at entry: ${t.btc_bull}\n`;
        }
      }
      note += `**Portfolio:** $${p.current_capital_usdc.toFixed(2)} | WR: ${wr}% | Open: ${p.open_positions.length}/10\n---\n`;
      const existing = fs.existsSync(OBS_FILE) ? fs.readFileSync(OBS_FILE, 'utf8') : '# Trading Observations Log\n---\n';
      // Insert after the header (after first ---)
      const headerEnd = existing.indexOf('---\n');
      if (headerEnd > -1) {
        const before = existing.slice(0, headerEnd + 4);
        const after = existing.slice(headerEnd + 4);
        fs.writeFileSync(OBS_FILE, before + note + after);
      } else {
        fs.writeFileSync(OBS_FILE, existing + note);
      }
    }
  } catch(e) {
    console.log('Observation log failed (non-critical):', e.message);
  }

  console.log('Done ✅');
}

run().catch(e => { console.error('Monitor error:', e.message); process.exit(1); });
