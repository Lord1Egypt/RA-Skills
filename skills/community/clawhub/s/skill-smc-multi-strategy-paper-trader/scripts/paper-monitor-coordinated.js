#!/usr/bin/env node
/**
 * paper-monitor-coordinated.js — 8D/2S Coordinated Paper Trading Monitor
 * 
 * Runs both day trading (1h) and swing trading (4h) with shared capital.
 * Optimal split: 8 day slots + 2 swing slots = 10 total concurrent.
 * Orchestrator prevents same-symbol conflicts.
 * 
 * Day: SMC v4.0 — 1h BoS+FVG+TA≥5, 12h max hold
 * Swing: SMC — Daily BoS → 4h FVG+TA≥5, 72h max hold
 */
'use strict';
const https = require('https');
const fs    = require('fs');
const path  = require('path');

const PORTFOLIO_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/portfolio-coordinated.json');
const MAX_DAY = 8;
const MAX_SWING = 2;

const TOKENS = [
  'BTCUSDT','ETHUSDT','SOLUSDT','BNBUSDT','XRPUSDT','DOGEUSDT','AVAXUSDT','LINKUSDT',
  'ARBUSDT','OPUSDT','SUIUSDT','APTUSDT','INJUSDT','SEIUSDT','FETUSDT','RENDERUSDT',
  'TAOUSDT','NEARUSDT','WIFUSDT','JUPUSDT','TIAUSDT','DYMUSDT','STRKUSDT','TONUSDT',
  'NOTUSDT','EIGENUSDT','GRASSUSDT','VIRTUALUSDT','AKTUSDT',
];

function apiFetch(url) {
  return new Promise((res, rej) => {
    const r = https.get(url, resp => {
      let d = ''; resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    }); r.on('error', rej);
    r.setTimeout(15000, () => { r.destroy(); rej(new Error('timeout')); });
  });
}
function apiFetch2(url, token) {
  return new Promise((res, rej) => {
    const r = https.get(url, { headers: { Authorization: `token ${token}`, Accept: 'application/vnd.github.v3+json', 'User-Agent': 'Jarvis' } }, resp => {
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
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─── Math ─────────────────────────────────────────────────────────────────────
function calcEMA(v,p){const k=2/(p+1);let e=v[0];return v.map((x,i)=>{if(i>0)e=x*k+e*(1-k);return e;});}
function calcATR(cs,period=14){const t=cs.map((c,i)=>{if(i===0)return c.h-c.l;const p2=cs[i-1].c;return Math.max(c.h-c.l,Math.abs(c.h-p2),Math.abs(c.l-p2));});const a=[];for(let i=0;i<cs.length;i++){if(i<period-1){a.push(null);continue;}if(i===period-1){a.push(t.slice(0,period).reduce((s,v2)=>s+v2,0)/period);}else{a.push((a[i-1]*(period-1)+t[i])/period);}}return a;}
function calcRSI(c,p=14){const r=Array(c.length).fill(null);let ag=0,al=0;for(let i=1;i<=p;i++){const d=c[i]-c[i-1];if(d>0)ag+=d;else al-=d;}ag/=p;al/=p;r[p]=al===0?100:100-100/(1+ag/al);for(let i=p+1;i<c.length;i++){const d=c[i]-c[i-1];ag=(ag*(p-1)+(d>0?d:0))/p;al=(al*(p-1)+(d<0?-d:0))/p;r[i]=al===0?100:100-100/(1+ag/al);}return r;}
function calcMACD(c){const e12=calcEMA(c,12),e26=calcEMA(c,26);const ml=c.map((_,i)=>e12[i]-e26[i]);const sig=calcEMA(ml.slice(25),9);const h=[];for(let i=0;i<c.length;i++){if(i<33){h.push(null);continue;}h.push(ml[i]-(sig[i-25]||0));}return{macdLine:ml,histogram:h};}
function calcOBV(cs){const o=[0];for(let i=1;i<cs.length;i++){if(cs[i].c>cs[i-1].c)o.push(o[i-1]+cs[i].v);else if(cs[i].c<cs[i-1].c)o.push(o[i-1]-cs[i].v);else o.push(o[i-1]);}return o;}
function calcSMA(v,p){return v.map((_,i)=>{if(i<p-1)return null;return v.slice(i-p+1,i+1).reduce((s,x)=>s+x,0)/p;});}
function zScore(value, arr) {
  if (arr.length < 2) return 0;
  const mean = arr.reduce((s,v)=>s+v,0)/arr.length;
  const std = Math.sqrt(arr.reduce((s,v)=>s+(v-mean)**2,0)/arr.length);
  return std === 0 ? 0 : (value - mean) / std;
}

function taConfluenceScore(cs, idx) {
  const closes = cs.map(c => c.c);
  const rsi = calcRSI(closes); const macd = calcMACD(closes); const obv = calcOBV(cs);
  const ema9 = calcEMA(closes, 9); const ema21 = calcEMA(closes, 21); const bbSma = calcSMA(closes, 20);
  const i = idx, ZLB = 30;
  let score = 0;
  if (rsi[i] !== null) { const w = rsi.slice(Math.max(0,i-ZLB), i).filter(v=>v!==null); const z = zScore(rsi[i], w); if (z > 0.3 && rsi[i] < 78) score += 2; if (z > 1.0 && rsi[i] < 75) score += 1; }
  if (macd.histogram[i] !== null) { const w = macd.histogram.slice(Math.max(0,i-ZLB), i).filter(v=>v!==null); const z = zScore(macd.histogram[i], w); if (z > 0.3) score += 1; if (i > 0 && macd.histogram[i] > (macd.histogram[i-1]||0)) score += 1; }
  if (ema9[i] > ema21[i]) score += 2;
  if (bbSma[i] !== null && i >= 19) { const sl = closes.slice(i-19, i+1); const std = Math.sqrt(sl.reduce((s,v)=>s+(v-bbSma[i])**2,0)/20); const upper = bbSma[i]+2*std; const lower = bbSma[i]-2*std; const range = upper-lower; if(range>0){ const pB=(closes[i]-lower)/range; if(pB>0.5&&pB<0.85)score+=2; } }
  if (i > 10) { const od = obv[i]-obv[i-5]; const ods = []; for(let j=Math.max(6,i-ZLB);j<i;j++) ods.push(obv[j]-obv[j-5]); const z = zScore(od, ods); if(z>0.5)score+=1; if(z>1.0)score+=1; }
  return score;
}

// ─── Regime ───────────────────────────────────────────────────────────────────
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
    const pct = (e8[e8.length-1] - e21[e21.length-1]) / e21[e21.length-1] * 100;
    if (pct > 0.15) return { trend: 'bullish', spread: pct };
    if (pct < -0.15) return { trend: 'bearish', spread: pct };
    return { trend: 'neutral', spread: pct };
  } catch { return { trend: 'unknown', spread: 0 }; }
}
async function getBTCDailyRegime() {
  try {
    const r = await apiFetch('https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1d&limit=60');
    const closes = r.map(k => parseFloat(k[4]));
    const e20 = calcEMA(closes, 20), e50 = calcEMA(closes, 50);
    return e20[e20.length-1] > e50[e50.length-1] ? 'bullish' : 'bearish';
  } catch { return 'unknown'; }
}

// ─── Data ─────────────────────────────────────────────────────────────────────
async function getCandles1h(sym, limit=80) {
  await sleep(80);
  try {
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=1h&limit=${limit}`);
    return r.map(k => ({ ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4] }));
  } catch { return []; }
}
async function getCandles4h(sym, limit=100) {
  await sleep(80);
  try {
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=4h&limit=${limit}`);
    return r.map(k => ({ ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4] }));
  } catch { return []; }
}
async function getDailyCandles(sym, limit=60) {
  await sleep(80);
  try {
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=1d&limit=${limit}`);
    return r.map(k => ({ ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4] }));
  } catch { return []; }
}

// ─── Day Trading Signal (1h SMC) ──────────────────────────────────────────────
function detectDaySignal(cs) {
  const P = { swN:3, volZThreshold:1.0, fvgZThreshold:0.5, slAtrMult:1.5, tpAtrMult:3.0, taMinScore:5, volLookback:30, fvgLookback:50, atrPeriod:14 };
  const hi = Array(cs.length).fill(null);
  for (let i=P.swN; i<cs.length-P.swN; i++) {
    let isH=true;
    for (let j=1;j<=P.swN;j++) if(cs[i-j].h>=cs[i].h||cs[i+j].h>=cs[i].h) isH=false;
    if(isH) hi[i]=cs[i].h;
  }
  const atrs = calcATR(cs, P.atrPeriod);
  for (let i=cs.length-5; i<cs.length-1; i++) {
    if (i < P.swN+2) continue;
    let bosIdx = -1;
    for (let j=i-1; j>=Math.max(0,i-60); j--) { if (hi[j]!==null && cs[i].c>hi[j]) { bosIdx=j; break; } }
    if (bosIdx < 0) continue;
    for (let j=Math.max(2,i-3); j<=i; j++) {
      const gap = cs[j].l - cs[j-2].h;
      if (gap <= 0) continue;
      const gapPct = gap / cs[j].c;
      const recentGaps = [];
      for (let g=Math.max(2,j-P.fvgLookback); g<j; g++) { const pg=cs[g].l-cs[g-2].h; if(pg>0) recentGaps.push(pg/cs[g].c); }
      const fvgZ = zScore(gapPct, recentGaps);
      if (fvgZ < P.fvgZThreshold) continue;
      const fvgLo=cs[j-2].h, fvgHi=cs[j].l, fvgMid=(fvgLo+fvgHi)/2;
      const latest=cs[cs.length-1], lastIdx=cs.length-1;
      if (!(latest.l<=fvgHi && latest.h>=fvgLo)) continue;
      const volWindow = cs.slice(Math.max(0,lastIdx-P.volLookback),lastIdx).map(c=>c.v);
      if (zScore(latest.v, volWindow) < P.volZThreshold) continue;
      const atr = atrs[lastIdx]; if (!atr) continue;
      const ep = Math.min(latest.c, fvgMid);
      let obLo = ep - atr * P.slAtrMult;
      for (let k=bosIdx-1; k>=Math.max(0,bosIdx-15); k--) { if (cs[k].c<cs[k].o) { obLo=cs[k].l; break; } }
      const sl = Math.max(obLo*0.999, ep - atr * P.slAtrMult);
      const tp = ep + atr * P.tpAtrMult;
      if (sl >= ep) continue;
      const ta = taConfluenceScore(cs, lastIdx);
      if (ta < P.taMinScore) continue;
      return { ep, sl, tp, ta, atr };
    }
  }
  return null;
}

// ─── Swing Signal (Daily BoS → 4h FVG) ───────────────────────────────────────
function detectSwingSignal(k4h, kD) {
  if (kD.length < 15 || k4h.length < 60) return null;
  const SP = { swN:5, fvgAge:6, taMinScore:5, slAtrMult:2.5, tpAtrMult:5.0, atrPeriod:14 };
  // Daily BoS check
  const sh = Array(kD.length).fill(null);
  for (let i=SP.swN; i<kD.length-SP.swN; i++) {
    let ok=true;
    for (let j=1;j<=SP.swN;j++) if(kD[i-j].h>=kD[i].h||kD[i+j].h>=kD[i].h){ok=false;break;}
    if(ok) sh[i]=kD[i].h;
  }
  let hasBoS = false;
  for (let i=kD.length-5; i<kD.length; i++) {
    if (i<SP.swN+1) continue;
    for (let j=i-1; j>=Math.max(0,i-30); j--) { if(sh[j]!==null && kD[i].c>sh[j]){hasBoS=true;break;} }
    if (hasBoS) break;
  }
  if (!hasBoS) return null;
  // 4h FVG entry
  const atrs = calcATR(k4h, SP.atrPeriod);
  for (let j=k4h.length-1; j>=Math.max(2,k4h.length-SP.fvgAge); j--) {
    const gap = k4h[j].l - k4h[j-2].h;
    if (gap<=0 || gap/k4h[j].c<0.0005) continue;
    const fvgLo=k4h[j-2].h, fvgHi=k4h[j].l, fvgMid=(fvgLo+fvgHi)/2;
    const latest = k4h[k4h.length-1], lastIdx = k4h.length-1;
    if (!(latest.l<=fvgHi && latest.h>=fvgLo)) continue;
    const atr = atrs[lastIdx]; if (!atr) continue;
    const ep = Math.min(latest.c, fvgMid);
    let obLo = ep - atr * SP.slAtrMult;
    for (let k=j-1; k>=Math.max(0,j-15); k--) { if(k4h[k].c<k4h[k].o){obLo=k4h[k].l;break;} }
    const sl = Math.min(obLo*0.999, ep - atr * SP.slAtrMult);
    const tp = ep + atr * SP.tpAtrMult;
    if (sl>=ep) continue;
    const rr = (tp-ep)/(ep-sl); if (rr<1.5) continue;
    const ta = taConfluenceScore(k4h, lastIdx);
    if (ta < SP.taMinScore) continue;
    return { ep, sl, tp, ta, atr };
  }
  return null;
}

// ─── Portfolio ────────────────────────────────────────────────────────────────
function loadPortfolio() {
  try { return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8')); }
  catch {
    return {
      version: '1.0', last_updated: new Date().toISOString(),
      strategy: 'Coordinated 8D/2S — Day+Swing | Paper Trading',
      btc_regime: 'unknown', btc_fast_regime: 'unknown', btc_daily_regime: 'unknown',
      paper_portfolio: {
        starting_capital_usdc: 1000, current_capital_usdc: 1000, deployed_usdc: 0,
        open_positions: [], closed_trades: [],
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

// ─── Main ─────────────────────────────────────────────────────────────────────
async function run() {
  const uaeTime = new Date().toLocaleString('en-AE', { timeZone: 'Asia/Dubai', hour12: false });
  console.log(`\n[${uaeTime} UAE] Coordinated 8D/2S monitor running...`);

  const portfolio = loadPortfolio();
  const p = portfolio.paper_portfolio;

  // Regimes
  const btcRegime = await getBTCRegime();
  const btcFast = await getBTCFastRegime();
  const btcDaily = await getBTCDailyRegime();
  portfolio.btc_regime = btcRegime;
  portfolio.btc_fast_regime = btcFast.trend;
  portfolio.btc_fast_spread = parseFloat(btcFast.spread.toFixed(3));
  portfolio.btc_daily_regime = btcDaily;
  const btcBull = btcRegime === 'bullish';
  const sizeMultiplier = btcBull ? 1.0 : 0.5;
  const fastAllowEntry = btcFast.trend !== 'bearish';
  console.log(`BTC 4h: ${btcRegime} | Daily: ${btcDaily} | Fast 15m: ${btcFast.trend} (${btcFast.spread.toFixed(3)}%)${!fastAllowEntry ? ' ⛔ BLOCKED' : ' ✅'}`);

  // Count positions by strategy
  const dayPositions = p.open_positions.filter(pos => pos.strategy === 'day');
  const swingPositions = p.open_positions.filter(pos => pos.strategy === 'swing');
  console.log(`Positions: ${dayPositions.length}/${MAX_DAY} day, ${swingPositions.length}/${MAX_SWING} swing`);

  // ── Manage existing positions ──
  const now = Date.now();
  const stillOpen = [];

  for (const pos of p.open_positions) {
    const ageH = (now - new Date(pos.entry_time).getTime()) / 3600000;
    const maxH = pos.strategy === 'swing' ? 72 : 12;
    const trail = pos.strategy === 'swing' ? 0.05 : 0.03; // 5% swing, 3% day

    try {
      await sleep(80);
      const ticker = await apiFetch(`https://fapi.binance.com/fapi/v1/ticker/price?symbol=${pos.symbol}`);
      const price = parseFloat(ticker.price);
      pos.current_price = price;

      let closed = false, exitType = '', exitPrice = price, pnlPct = 0;

      if (price <= pos.sl_price) { exitType = 'SL'; exitPrice = pos.sl_price; closed = true; }
      else if (!pos.tp1_hit && price >= pos.tp_price) {
        pos.tp1_hit = true; pos.half_price = pos.tp_price; pos.trail_peak = price;
        stillOpen.push(pos);
        console.log(`  📈 ${pos.symbol} [${pos.strategy}] TP1 hit at $${price.toFixed(4)}`);
        continue;
      }
      else if (pos.tp1_hit) {
        if (price > (pos.trail_peak || pos.tp_price)) pos.trail_peak = price;
        const trailSL = (pos.trail_peak || price) * (1 - trail);
        if (price <= trailSL) {
          exitType = 'TRAIL'; exitPrice = trailSL; closed = true;
          pnlPct = ((pos.half_price - pos.entry_price)*0.5 + (exitPrice - pos.entry_price)*0.5) / pos.entry_price * 100;
        }
      }
      else if (ageH >= maxH) { exitType = 'TIME'; closed = true; }

      if (closed) {
        if (pnlPct === 0) pnlPct = (exitPrice - pos.entry_price) / pos.entry_price * 100;
        const pnlUSD = pos.size_usdc * pnlPct / 100;
        p.current_capital_usdc += pnlUSD;
        p.stats.total_trades++;
        if (pnlUSD > 0) p.stats.wins++; else p.stats.losses++;
        p.stats.total_pnl_usdc += pnlUSD;
        p.closed_trades.push({
          symbol: pos.symbol, entry_price: pos.entry_price, exit_price: exitPrice,
          entry_time: pos.entry_time, exit_time: new Date().toISOString(),
          held_hours: parseFloat(ageH.toFixed(1)), pnl_pct: parseFloat(pnlPct.toFixed(3)),
          pnl_usd: parseFloat(pnlUSD.toFixed(2)), exit_type: exitType,
          size_usdc: pos.size_usdc, btc_bull: pos.btc_bull_at_entry, strategy: pos.strategy,
        });
        console.log(`  ${pnlUSD > 0 ? '✅' : '❌'} ${pos.symbol} [${pos.strategy}] ${exitType} | ${pnlPct >= 0 ? '+' : ''}${pnlPct.toFixed(2)}% | $${pnlUSD >= 0 ? '+' : ''}${pnlUSD.toFixed(2)} | ${ageH.toFixed(0)}h`);
      } else {
        stillOpen.push(pos);
      }
    } catch { stillOpen.push(pos); }
  }
  p.open_positions = stillOpen;

  // ── Scan for new day trading signals (1h) ──
  const openDayCount = p.open_positions.filter(pos => pos.strategy === 'day').length;
  const openSymbols = new Set(p.open_positions.map(pos => pos.symbol));

  if (openDayCount < MAX_DAY && fastAllowEntry) {
    for (const sym of TOKENS) {
      if (p.open_positions.filter(pos => pos.strategy === 'day').length >= MAX_DAY) break;
      if (openSymbols.has(sym)) continue;

      const cs = await getCandles1h(sym);
      if (cs.length < 60) continue;

      const signal = detectDaySignal(cs);
      if (!signal) continue;

      const posSize = p.current_capital_usdc * 0.10 * sizeMultiplier;
      p.open_positions.push({
        symbol: sym, entry_price: signal.ep, sl_price: signal.sl, tp_price: signal.tp,
        size_usdc: posSize, entry_time: new Date().toISOString(),
        btc_bull_at_entry: btcBull, tp1_hit: false, trail_peak: null, half_price: null,
        current_price: signal.ep, strategy: 'day',
      });
      openSymbols.add(sym);
      console.log(`  🟢 DAY: ${sym} | $${signal.ep.toFixed(4)} | SL:$${signal.sl.toFixed(4)} | TP:$${signal.tp.toFixed(4)} | TA:${signal.ta}/11`);
    }
  }

  // ── Scan for new swing signals (4h + daily) ──
  const openSwingCount = p.open_positions.filter(pos => pos.strategy === 'swing').length;

  if (openSwingCount < MAX_SWING) {
    for (const sym of TOKENS) {
      if (p.open_positions.filter(pos => pos.strategy === 'swing').length >= MAX_SWING) break;
      if (openSymbols.has(sym)) continue;

      const [k4h, kD] = await Promise.all([getCandles4h(sym), getDailyCandles(sym)]);
      const signal = detectSwingSignal(k4h, kD);
      if (!signal) continue;

      const posSize = p.current_capital_usdc * 0.10 * sizeMultiplier;
      p.open_positions.push({
        symbol: sym, entry_price: signal.ep, sl_price: signal.sl, tp_price: signal.tp,
        size_usdc: posSize, entry_time: new Date().toISOString(),
        btc_bull_at_entry: btcBull, tp1_hit: false, trail_peak: null, half_price: null,
        current_price: signal.ep, atr_at_entry: signal.atr, strategy: 'swing',
      });
      openSymbols.add(sym);
      console.log(`  🔵 SWING: ${sym} | $${signal.ep.toFixed(4)} | SL:$${signal.sl.toFixed(4)} | TP:$${signal.tp.toFixed(4)} | TA:${signal.ta}/11`);
    }
  }

  // ── Save ──
  p.deployed_usdc = p.open_positions.reduce((s, pos) => s + pos.size_usdc, 0);
  savePortfolio(portfolio);

  // ── GitHub push ──
  try {
    const ghToken = fs.readFileSync(path.join(process.env.HOME, '.github_token'), 'utf8').trim();
    const content = Buffer.from(JSON.stringify(portfolio, null, 2)).toString('base64');
    const shaRes = await apiFetch2('https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-coordinated.json', ghToken);
    const sha = shaRes.sha || '';
    await apiFetch2Put('https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-coordinated.json', ghToken,
      JSON.stringify({ message: 'trading: coordinated portfolio update', content, sha: sha || undefined }));
    console.log('GitHub updated ✅');
  } catch(e) { console.log('GitHub push failed:', e.message); }

  // Summary
  const totalPnl = p.current_capital_usdc - p.starting_capital_usdc;
  const wr = p.stats.total_trades > 0 ? (p.stats.wins / p.stats.total_trades * 100).toFixed(1) : '—';
  const dc = p.open_positions.filter(pos => pos.strategy === 'day').length;
  const sc = p.open_positions.filter(pos => pos.strategy === 'swing').length;
  console.log(`\nCoordinated: $${p.current_capital_usdc.toFixed(2)} | PnL: ${totalPnl >= 0 ? '+' : ''}$${totalPnl.toFixed(2)} | WR: ${wr}% | Day: ${dc}/${MAX_DAY} | Swing: ${sc}/${MAX_SWING}`);
  console.log('Done ✅');
}

run().catch(e => { console.error('Error:', e.message); process.exit(1); });
