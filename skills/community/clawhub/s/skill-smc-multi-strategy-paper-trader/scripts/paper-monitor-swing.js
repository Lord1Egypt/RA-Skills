#!/usr/bin/env node
/**
 * paper-monitor-swing.js — Swing Paper Trading Monitor
 * Best config from Phase 3 backtest: TA≥5, FVG6, srch4, SL2.5×ATR, TP5×ATR, trail3×ATR
 * Uses 4H candles + Daily BoS detection. Runs every 4h.
 * Separate portfolio from day trading for A/B comparison.
 * Reads orchestrator lock file to prevent conflicting positions.
 */
'use strict';
const https = require('https');
const fs    = require('fs');
const path  = require('path');

const PORTFOLIO_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/portfolio-swing.json');
const LOCK_FILE      = path.join(process.env.HOME, '.openclaw/workspace/trading/paper-dashboard/orchestrator-lock.json');

const TOKENS = [
  'BTCUSDT','ETHUSDT','SOLUSDT','BNBUSDT','XRPUSDT','DOGEUSDT','AVAXUSDT','LINKUSDT',
  'ARBUSDT','OPUSDT','SUIUSDT','APTUSDT','INJUSDT','SEIUSDT','FETUSDT','RENDERUSDT',
  'TAOUSDT','NEARUSDT','WIFUSDT','JUPUSDT','TIAUSDT','DYMUSDT','STRKUSDT','TONUSDT',
  'NOTUSDT','EIGENUSDT','GRASSUSDT','VIRTUALUSDT','AKTUSDT',
];

// Best swing config from Phase 3 backtest (row #9)
const P = {
  swN: 5,               // swing lookback for daily BoS
  fvgAge: 6,            // max FVG age in 4h candles (24h)
  fvgSearch: 4,         // candles to search for FVG after BoS
  maxHold: 72,          // max hold time in hours (3 days)
  maxConcurrent: 5,     // swing positions (orchestrator may override)
  posPct: 0.10,         // 10% position size
  // ATR-based SL/TP
  slAtrMult: 2.5,
  tpAtrMult: 5.0,
  trailAtrMult: 3.0,
  atrPeriod: 14,
  // TA z-score
  taMinScore: 5,
  taZLookback: 30,
  // Volume z-score
  volZThreshold: 0.0,   // best config had volZ=0 (no filter)
  volLookback: 30,
  // FVG z-score
  fvgZThreshold: 0.0,
};

function apiFetch(url) {
  return new Promise((res, rej) => {
    const r = https.get(url, resp => {
      let d = '';
      resp.on('data', c => d += c);
      resp.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
    });
    r.on('error', rej);
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

// ─── Math helpers ─────────────────────────────────────────────────────────────
function calcEMA(v,p){const k=2/(p+1);let e=v[0];return v.map((x,i)=>{if(i>0)e=x*k+e*(1-k);return e;});}
function calcATR(cs,period=14){const t=cs.map((c,i)=>{if(i===0)return c.h-c.l;const p2=cs[i-1].c;return Math.max(c.h-c.l,Math.abs(c.h-p2),Math.abs(c.l-p2));});const a=[];for(let i=0;i<cs.length;i++){if(i<period-1){a.push(null);continue;}if(i===period-1){a.push(t.slice(0,period).reduce((s,v2)=>s+v2,0)/period);}else{a.push((a[i-1]*(period-1)+t[i])/period);}}return a;}
function calcRSI(c,p=14){const r=Array(c.length).fill(null);let ag=0,al=0;for(let i=1;i<=p;i++){const d=c[i]-c[i-1];if(d>0)ag+=d;else al-=d;}ag/=p;al/=p;r[p]=al===0?100:100-100/(1+ag/al);for(let i=p+1;i<c.length;i++){const d=c[i]-c[i-1];ag=(ag*(p-1)+(d>0?d:0))/p;al=(al*(p-1)+(d<0?-d:0))/p;r[i]=al===0?100:100-100/(1+ag/al);}return r;}
function calcMACD(c){const e12=calcEMA(c,12),e26=calcEMA(c,26);const ml=c.map((_,i)=>e12[i]-e26[i]);const sig=calcEMA(ml.slice(25),9);const h=[];for(let i=0;i<c.length;i++){if(i<33){h.push(null);continue;}h.push(ml[i]-(sig[i-25]||0));}return{macdLine:ml,histogram:h};}
function calcOBV(cs){const o=[0];for(let i=1;i<cs.length;i++){if(cs[i].c>cs[i-1].c)o.push(o[i-1]+cs[i].v);else if(cs[i].c<cs[i-1].c)o.push(o[i-1]-cs[i].v);else o.push(o[i-1]);}return o;}
function calcBB(c,p=20){const s=[],u=[],l=[];for(let i=0;i<c.length;i++){if(i<p-1){s.push(null);u.push(null);l.push(null);continue;}const sl=c.slice(i-p+1,i+1);const m=sl.reduce((a,b)=>a+b,0)/p;const st=Math.sqrt(sl.reduce((a,b)=>a+(b-m)**2,0)/p);s.push(m);u.push(m+2*st);l.push(m-2*st);}return{sma:s,upper:u,lower:l};}
function zScore(value, arr) {
  if (arr.length < 2) return 0;
  const mean = arr.reduce((s,v)=>s+v,0)/arr.length;
  const std = Math.sqrt(arr.reduce((s,v)=>s+(v-mean)**2,0)/arr.length);
  return std === 0 ? 0 : (value - mean) / std;
}

// ─── TA Confluence ────────────────────────────────────────────────────────────
function taConfluenceScore(cs, idx) {
  const closes = cs.map(c => c.c);
  const rsi = calcRSI(closes);
  const macd = calcMACD(closes);
  const obv = calcOBV(cs);
  const ema9 = calcEMA(closes, 9);
  const ema21 = calcEMA(closes, 21);
  const bb = calcBB(closes);
  const i = idx;
  let score = 0;
  
  if (rsi[i] !== null) {
    const rsiW = rsi.slice(Math.max(0,i-P.taZLookback), i).filter(v=>v!==null);
    const rsiZ = zScore(rsi[i], rsiW);
    if (rsiZ > 0.3 && rsi[i] < 78) score += 2;
    if (rsiZ > 1.0 && rsi[i] < 75) score += 1;
  }
  if (macd.histogram[i] !== null) {
    const mW = macd.histogram.slice(Math.max(0,i-P.taZLookback), i).filter(v=>v!==null);
    const mZ = zScore(macd.histogram[i], mW);
    if (mZ > 0.3) score += 1;
    if (i > 0 && macd.histogram[i] > (macd.histogram[i-1]||0)) score += 1;
  }
  if (ema9[i] > ema21[i]) score += 2;
  if (bb.sma[i] !== null) {
    const range = bb.upper[i] - bb.lower[i];
    if (range > 0) {
      const pB = (closes[i] - bb.lower[i]) / range;
      if (pB > 0.5 && pB < 0.85) score += 2;
    }
  }
  if (i > 10) {
    const obvD = obv[i] - obv[i-5];
    const obvDs = [];
    for (let j = Math.max(6, i-P.taZLookback); j < i; j++) obvDs.push(obv[j] - obv[j-5]);
    const oZ = zScore(obvD, obvDs);
    if (oZ > 0.5) score += 1;
    if (oZ > 1.0) score += 1;
  }
  return score;
}

// ─── BTC Regime ───────────────────────────────────────────────────────────────
async function getBTCRegime() {
  try {
    const r = await apiFetch('https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1d&limit=60');
    const closes = r.map(k => parseFloat(k[4]));
    const e20 = calcEMA(closes, 20), e50 = calcEMA(closes, 50);
    return e20[e20.length-1] > e50[e50.length-1] ? 'bullish' : 'bearish';
  } catch { return 'unknown'; }
}

// ─── Data ─────────────────────────────────────────────────────────────────────
async function getCandles4h(sym, limit=200) {
  try {
    await sleep(80);
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=4h&limit=${limit}`);
    return r.map(k => ({
      ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4],
      v:+k[5]*+k[4], tbv:+k[9]*+k[4]
    }));
  } catch { return []; }
}

async function getDailyCandles(sym, limit=120) {
  try {
    await sleep(80);
    const r = await apiFetch(`https://fapi.binance.com/fapi/v1/klines?symbol=${sym}&interval=1d&limit=${limit}`);
    return r.map(k => ({
      ts:k[0], o:+k[1], h:+k[2], l:+k[3], c:+k[4], v:+k[5]*+k[4]
    }));
  } catch { return []; }
}

// ─── SMC on Daily → 4h Entry ─────────────────────────────────────────────────
function findDailySwingHighs(kD) {
  const sh = Array(kD.length).fill(null);
  const n = P.swN;
  for (let i = n; i < kD.length - n; i++) {
    let ok = true;
    for (let j = 1; j <= n; j++) {
      if (kD[i-j].h >= kD[i].h || kD[i+j].h >= kD[i].h) { ok = false; break; }
    }
    if (ok) sh[i] = kD[i].h;
  }
  return sh;
}

function hasDailyBoS(kD, sh) {
  // Check if any of the last 5 daily candles broke a swing high
  for (let i = kD.length - 5; i < kD.length; i++) {
    if (i < P.swN + 1) continue;
    for (let j = i - 1; j >= Math.max(0, i - 30); j--) {
      if (sh[j] !== null && kD[i].c > sh[j]) return true;
    }
  }
  return false;
}

function detect4hSignal(cs, hasBoS) {
  if (!hasBoS) return null;
  
  const atrs = calcATR(cs, P.atrPeriod);
  
  // Look for FVG in recent candles (within fvgAge)
  for (let j = cs.length - 1; j >= Math.max(2, cs.length - P.fvgAge); j--) {
    const gap = cs[j].l - cs[j-2].h;
    if (gap <= 0) continue;
    const gapPct = gap / cs[j].c;
    if (gapPct < 0.0005) continue;
    
    // FVG z-score
    if (P.fvgZThreshold > 0) {
      const recentGaps = [];
      for (let g = Math.max(2, j-50); g < j; g++) {
        const pg = cs[g].l - cs[g-2].h;
        if (pg > 0) recentGaps.push(pg / cs[g].c);
      }
      const fZ = zScore(gapPct, recentGaps);
      if (fZ < P.fvgZThreshold) continue;
    }
    
    // Check if latest candle is retesting FVG
    const fvgLo = cs[j-2].h, fvgHi = cs[j].l, fvgMid = (fvgLo + fvgHi) / 2;
    const latest = cs[cs.length - 1];
    const lastIdx = cs.length - 1;
    if (!(latest.l <= fvgHi && latest.h >= fvgLo)) continue;
    
    // Volume z-score
    if (P.volZThreshold > 0) {
      const vols = cs.slice(Math.max(0, lastIdx - P.volLookback), lastIdx).map(c => c.v);
      const vZ = zScore(latest.v, vols);
      if (vZ < P.volZThreshold) continue;
    }
    
    const atr = atrs[lastIdx];
    if (!atr) continue;
    
    const ep = Math.min(latest.c, fvgMid);
    
    // OB low for SL
    let obLo = ep - atr * P.slAtrMult;
    for (let k = j - 1; k >= Math.max(0, j - 15); k--) {
      if (cs[k].c < cs[k].o) { obLo = cs[k].l; break; }
    }
    const sl = Math.min(obLo * 0.999, ep - atr * P.slAtrMult);
    const tp = ep + atr * P.tpAtrMult;
    
    if (sl >= ep) continue;
    const rr = (tp - ep) / (ep - sl);
    if (rr < 1.5) continue;
    
    return { ep, sl, tp, fvgMid, gap: gapPct, atr };
  }
  return null;
}

// ─── Orchestrator Lock ────────────────────────────────────────────────────────
function getLockedSymbols() {
  try {
    const lock = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8'));
    return new Set(lock.day_trading_symbols || []);
  } catch { return new Set(); }
}

function updateOrchestratorLock(openSymbols) {
  try {
    let lock = {};
    try { lock = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8')); } catch {}
    lock.swing_symbols = [...openSymbols];
    lock.swing_updated = new Date().toISOString();
    fs.writeFileSync(LOCK_FILE, JSON.stringify(lock, null, 2));
  } catch {}
}

// ─── Portfolio ────────────────────────────────────────────────────────────────
function loadPortfolio() {
  try {
    return JSON.parse(fs.readFileSync(PORTFOLIO_FILE, 'utf8'));
  } catch {
    return {
      version: '1.0',
      last_updated: new Date().toISOString(),
      strategy: 'Swing SMC — Daily BoS → 4h FVG + TA ≥5 | Paper Trading',
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

// ─── Main ─────────────────────────────────────────────────────────────────────
async function run() {
  const uaeTime = new Date().toLocaleString('en-AE', { timeZone: 'Asia/Dubai', hour12: false });
  console.log(`\n[${uaeTime} UAE] Swing paper monitor running...`);

  const portfolio = loadPortfolio();
  const p = portfolio.paper_portfolio;

  // 1. BTC daily regime
  const btcRegime = await getBTCRegime();
  portfolio.btc_regime = btcRegime;
  const btcBull = btcRegime === 'bullish';
  const sizeMultiplier = btcBull ? 1.0 : 0.5;
  console.log(`BTC daily regime: ${btcRegime} → size: ${btcBull ? '10%' : '5%'}`);

  // 2. Check orchestrator lock for conflicting symbols
  const lockedSymbols = getLockedSymbols();
  if (lockedSymbols.size > 0) {
    console.log(`Orchestrator lock: ${lockedSymbols.size} symbols held by day trading: ${[...lockedSymbols].join(', ')}`);
  }

  // 3. Manage open positions
  const now = Date.now();
  const stillOpen = [];
  const atrs4h = {};

  for (const pos of p.open_positions) {
    const ageH = (now - new Date(pos.entry_time).getTime()) / 3600000;
    try {
      await sleep(80);
      const ticker = await apiFetch(`https://fapi.binance.com/fapi/v1/ticker/price?symbol=${pos.symbol}`);
      const price = parseFloat(ticker.price);
      pos.current_price = price;

      // Get current ATR for trailing
      let currentATR = pos.atr_at_entry || 0;
      if (!atrs4h[pos.symbol]) {
        const cs = await getCandles4h(pos.symbol, 20);
        if (cs.length >= 15) {
          const atrs = calcATR(cs, 14);
          currentATR = atrs[atrs.length - 1] || currentATR;
          atrs4h[pos.symbol] = currentATR;
        }
      } else {
        currentATR = atrs4h[pos.symbol];
      }

      let closed = false;
      let exitType = '', exitPrice = price, pnlPct = 0;

      // SL
      if (price <= pos.sl_price) {
        exitType = 'SL'; exitPrice = pos.sl_price; closed = true;
      }
      // TP1 (half position)
      else if (!pos.tp1_hit && price >= pos.tp_price) {
        pos.tp1_hit = true;
        pos.half_price = pos.tp_price;
        pos.trail_peak = price;
        stillOpen.push(pos);
        console.log(`  📈 ${pos.symbol} TP1 hit at $${price.toFixed(4)} — trailing stop active`);
        continue;
      }
      // Trailing stop after TP1
      else if (pos.tp1_hit) {
        if (price > (pos.trail_peak || pos.tp_price)) pos.trail_peak = price;
        const trailSL = (pos.trail_peak || price) - currentATR * P.trailAtrMult;
        if (price <= trailSL) {
          exitType = 'TRAIL'; exitPrice = trailSL; closed = true;
          pnlPct = ((pos.half_price - pos.entry_price)*0.5 + (exitPrice - pos.entry_price)*0.5) / pos.entry_price * 100;
        }
      }
      // Time exit (72h = 3 days)
      else if (ageH >= P.maxHold) {
        exitType = 'TIME'; closed = true;
      }

      if (closed) {
        if (pnlPct === 0) pnlPct = (exitPrice - pos.entry_price) / pos.entry_price * 100;
        const pnlUSD = pos.size_usdc * pnlPct / 100;
        p.current_capital_usdc += pnlUSD;
        p.stats.total_trades++;
        if (pnlUSD > 0) p.stats.wins++; else p.stats.losses++;
        p.stats.total_pnl_usdc += pnlUSD;

        p.closed_trades.push({
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
          strategy: 'swing',
        });
        console.log(`  ${pnlUSD > 0 ? '✅' : '❌'} ${pos.symbol} CLOSED | ${exitType} | ${pnlPct >= 0 ? '+' : ''}${pnlPct.toFixed(2)}% | $${pnlUSD >= 0 ? '+' : ''}${pnlUSD.toFixed(2)} | held ${ageH.toFixed(0)}h`);
      } else {
        stillOpen.push(pos);
      }
    } catch(e) {
      stillOpen.push(pos);
    }
  }
  p.open_positions = stillOpen;

  // 4. Scan for new swing signals
  if (p.open_positions.length < P.maxConcurrent) {
    const openSymbols = new Set(p.open_positions.map(pos => pos.symbol));
    
    for (const sym of TOKENS) {
      if (p.open_positions.length >= P.maxConcurrent) break;
      if (openSymbols.has(sym)) continue;
      if (lockedSymbols.has(sym)) {
        // Skip — day trading already has this symbol
        continue;
      }

      // Get daily candles for BoS detection
      const kD = await getDailyCandles(sym, 60);
      if (kD.length < 15) continue;
      
      const dailySH = findDailySwingHighs(kD);
      const hasBoS = hasDailyBoS(kD, dailySH);
      if (!hasBoS) continue;

      // Get 4h candles for entry
      const k4h = await getCandles4h(sym, 100);
      if (k4h.length < 60) continue;

      const signal = detect4hSignal(k4h, hasBoS);
      if (!signal) continue;

      // TA confluence gate
      const ta = taConfluenceScore(k4h, k4h.length - 1);
      if (ta < P.taMinScore) continue;

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
        atr_at_entry: signal.atr,
        strategy: 'swing',
      };
      p.open_positions.push(pos);
      openSymbols.add(sym);
      console.log(`  🟢 SWING SIGNAL: ${sym} | Entry: $${signal.ep.toFixed(4)} | SL: $${signal.sl.toFixed(4)} | TP: $${signal.tp.toFixed(4)} | Size: $${posSize.toFixed(2)} | TA:${ta}/11`);
    }
  }

  // 5. Update
  p.deployed_usdc = p.open_positions.reduce((s, pos) => s + pos.size_usdc, 0);
  savePortfolio(portfolio);
  
  // Update orchestrator lock
  const swingSymbols = new Set(p.open_positions.map(pos => pos.symbol));
  updateOrchestratorLock(swingSymbols);

  // 6. Push to GitHub
  try {
    const ghToken = fs.readFileSync(path.join(process.env.HOME, '.github_token'), 'utf8').trim();
    const content = Buffer.from(JSON.stringify(portfolio, null, 2)).toString('base64');
    const shaRes = await apiFetch2(`https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-swing.json`, ghToken);
    const sha = shaRes.sha || '';
    const body = JSON.stringify({ message: 'trading: swing portfolio update', content, sha: sha || undefined });
    await apiFetch2Put(`https://api.github.com/repos/Zero2Ai-hub/Jarvis-Ops/contents/trading/portfolio-swing.json`, ghToken, body);
    console.log('GitHub portfolio-swing.json updated ✅');
  } catch(e) {
    console.log('GitHub push failed (non-critical):', e.message);
  }

  // 7. Log observations
  try {
    const OBS_FILE = path.join(process.env.HOME, '.openclaw/workspace/trading/observations.md');
    const closedThisRun = p.closed_trades.filter(t => {
      return (now - new Date(t.exit_time).getTime()) / 60000 < 250; // within 4h window
    });
    if (closedThisRun.length > 0) {
      const ts = new Date().toISOString().replace('T',' ').slice(0,19) + ' UTC';
      let note = `\n## [${ts}] Swing Auto-Observation\n`;
      note += `**BTC daily regime:** ${btcRegime}\n`;
      note += `**Closed this cycle:**\n`;
      for (const t of closedThisRun) {
        note += `- ${t.symbol}: ${t.exit_type} | ${t.pnl_pct >= 0 ? '+' : ''}${t.pnl_pct}% ($${t.pnl_usd >= 0 ? '+' : ''}${t.pnl_usd}) | held ${t.held_hours}h\n`;
      }
      note += `---\n`;
      const existing = fs.existsSync(OBS_FILE) ? fs.readFileSync(OBS_FILE, 'utf8') : '# Trading Observations Log\n---\n';
      const headerEnd = existing.indexOf('---\n');
      if (headerEnd > -1) {
        fs.writeFileSync(OBS_FILE, existing.slice(0, headerEnd + 4) + note + existing.slice(headerEnd + 4));
      } else {
        fs.writeFileSync(OBS_FILE, existing + note);
      }
    }
  } catch {}

  const totalPnl = p.current_capital_usdc - p.starting_capital_usdc;
  const wr = p.stats.total_trades > 0 ? (p.stats.wins / p.stats.total_trades * 100).toFixed(1) : '—';
  console.log(`\nSwing Portfolio: $${p.current_capital_usdc.toFixed(2)} | PnL: ${totalPnl >= 0 ? '+' : ''}$${totalPnl.toFixed(2)} | WR: ${wr}% | Open: ${p.open_positions.length}/${P.maxConcurrent}`);
  console.log('Done ✅');
}

run().catch(e => { console.error('Swing monitor error:', e.message); process.exit(1); });
