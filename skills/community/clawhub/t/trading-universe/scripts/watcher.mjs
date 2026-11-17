#!/usr/bin/env node
/**
 * watcher.mjs — persistent background price monitor for trading-universe
 * Polls Yahoo Finance live prices, builds rolling M15 candles, detects:
 *   - Double tops / double bottoms (EQH/EQL revisited)
 *   - Fair Value Gaps (FVGs) on M15 and H1
 * Sends Telegram alerts via OpenClaw message tool (spawned sub-agent)
 * 
 * Runs as Windows Scheduled Task (at logon, run whether user logged on or not)
 * State persisted to ~/.trading-universe/watcher-state.json
 */

import { readFileSync, writeFileSync, appendFileSync, renameSync, statSync, existsSync, mkdirSync, unlinkSync, openSync, closeSync } from "node:fs";
import { DEFAULT_ASSETS, normalizeAsset, roundPrice, symbolForAsset } from "./symbols.mjs";
import { homedir } from "node:os";
import { join } from "node:path";

const STATE_DIR = process.env.TRADE_DATA_DIR || join(homedir(), ".trading-universe");
mkdirSync(STATE_DIR, { recursive: true });
const STATE_FILE = join(STATE_DIR, "watcher-state.json");
const LOG_FILE = join(STATE_DIR, "watcher.log");
const LOG_MAX_BYTES = 5 * 1024 * 1024; // rotate (keep tail) past 5MB
const PID_FILE = join(STATE_DIR, "watcher.pid");
const QUEUE_LOCK_FILE = join(STATE_DIR, "alert-queue.lock");
const ALERT_STATE_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; // prune cooldown/dedupe entries older than this

// Watched pairs (same as dashboard default, extensible via env)
const WATCHED = (process.env.WATCH_PAIRS || DEFAULT_ASSETS.join(","))
  .split(",").map(normalizeAsset).filter((asset) => symbolForAsset(asset));

const POLL_INTERVAL_MS = 30000;      // 30s price poll
const STATE_SAVE_INTERVAL_MS = 60000; // 1min state flush
const ALERT_COOLDOWN_MS = 15 * 60 * 1000; // 15min per (asset, pattern) dedupe
const M15_SEC = 900;
const H1_SEC = 3600;
const MAX_CONCURRENT = 3;              // max parallel fetches to avoid rate limit
const STAGGER_MS = 2000;               // stagger between each asset in a batch

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  try {
    // Rotate (keep the tail) instead of growing forever; cheap statSync check
    // on every call, expensive read+trim only once the file is actually large.
    if (existsSync(LOG_FILE) && statSync(LOG_FILE).size > LOG_MAX_BYTES) {
      const tail = readFileSync(LOG_FILE, "utf8").split("\n").slice(-2000).join("\n");
      writeFileSync(LOG_FILE, tail);
    }
    appendFileSync(LOG_FILE, line + "\n");
  } catch {}
}

// Cross-process advisory lock (exclusive-create lockfile) so watcher.mjs and
// alert-sender.mjs never interleave a read-modify-write on alert-queue.json.
// Stale locks (owner crashed) are broken after LOCK_STALE_MS.
const LOCK_STALE_MS = 30000;
async function withQueueLock(fn) {
  const deadline = Date.now() + 20000;
  let acquired = false;
  for (;;) {
    try {
      closeSync(openSync(QUEUE_LOCK_FILE, "wx"));
      acquired = true;
      break;
    } catch (e) {
      if (e.code !== "EEXIST") throw e;
      try {
        if (Date.now() - statSync(QUEUE_LOCK_FILE).mtimeMs > LOCK_STALE_MS) {
          unlinkSync(QUEUE_LOCK_FILE); // previous holder died mid-lock — break it
          continue;
        }
      } catch {}
      if (Date.now() > deadline) throw new Error("alert-queue lock timed out");
      await new Promise((r) => setTimeout(r, 50 + Math.random() * 100));
    }
  }
  try {
    return await fn();
  } finally {
    if (acquired) try { unlinkSync(QUEUE_LOCK_FILE); } catch {}
  }
}

function loadState() {
  if (!existsSync(STATE_FILE)) return { prices: {}, candles: { M15: {}, H1: {} }, alerts: {} };
  try { return JSON.parse(readFileSync(STATE_FILE, "utf8")); } catch { return { prices: {}, candles: { M15: {}, H1: {} }, alerts: {} }; }
}

function saveState(state) {
  const tmp = `${STATE_FILE}.${process.pid}.tmp`;
  try { writeFileSync(tmp, JSON.stringify(state, null, 2)); renameSync(tmp, STATE_FILE); }
  catch (e) { try { unlinkSync(tmp); } catch {} log(`STATE SAVE FAILED: ${e.message}`); }
}

// Fetch live price from Yahoo v8 chart (1m interval, 1d range = last ~390 bars)
async function fetchLivePrice(symbol, attempt = 0) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1m&range=1d`;
  try {
    const res = await fetch(url, {
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" },
      signal: AbortSignal.timeout(20000),
    });
    if (!res.ok) {
      if (res.status === 429 && attempt < 2) {
        await new Promise(r => setTimeout(r, 3000 * (attempt + 1)));
        return fetchLivePrice(symbol, attempt + 1);
      }
      throw new Error(`HTTP ${res.status}`);
    }
    const j = await res.json();
    const r = j?.chart?.result?.[0];
    if (!r?.timestamp?.length) throw new Error("empty result");
    const meta = r.meta;
    const lastIdx = r.timestamp.length - 1;
    // Use regularMarketPrice if available, else last close
    const price = meta?.regularMarketPrice ?? r.indicators.quote[0].close[lastIdx];
    if (price == null) throw new Error("no price");
    return { price, timestamp: r.timestamp[lastIdx], high: r.indicators.quote[0].high[lastIdx], low: r.indicators.quote[0].low[lastIdx], open: r.indicators.quote[0].open[lastIdx] };
  } catch (e) {
    if (attempt < 2 && (e.name === "AbortError" || e.name === "TimeoutError")) {
      await new Promise(r => setTimeout(r, 2000 * (attempt + 1)));
      return fetchLivePrice(symbol, attempt + 1);
    }
    throw new Error(`${symbol}: ${e.message}`);
  }
}

// Build / roll M15 candle from 1m ticks
function rollM15(candles, tick) {
  const bucket = Math.floor(tick.timestamp / M15_SEC) * M15_SEC;
  let c = candles.find(x => x.t === bucket);
  if (!c) {
    c = { t: bucket, o: tick.open ?? tick.price, h: tick.high ?? tick.price, l: tick.low ?? tick.price, c: tick.price };
    candles.push(c);
  } else {
    c.h = Math.max(c.h, tick.high ?? tick.price);
    c.l = Math.min(c.l, tick.low ?? tick.price);
    c.c = tick.price;
  }
  // Keep last ~200 M15 candles (~50 hours)
  if (candles.length > 200) candles.splice(0, candles.length - 200);
  return c;
}

// Build / roll H1 candle from M15 closes
function rollH1(h1Candles, m15Candles) {
  if (!m15Candles.length) return;
  const lastM15 = m15Candles[m15Candles.length - 1];
  const bucket = Math.floor(lastM15.t / H1_SEC) * H1_SEC;
  let c = h1Candles.find(x => x.t === bucket);
  if (!c) {
    c = { t: bucket, o: lastM15.o, h: lastM15.h, l: lastM15.l, c: lastM15.c };
    h1Candles.push(c);
  } else {
    c.h = Math.max(c.h, lastM15.h);
    c.l = Math.min(c.l, lastM15.l);
    c.c = lastM15.c;
  }
  if (h1Candles.length > 200) h1Candles.splice(0, h1Candles.length - 200);
}

// Detect equal highs/lows (double top/bottom) on a timeframe
function detectEqualLevels(candles, lookback = 40, tolPct = 0.0015) {
  if (candles.length < 10) return { doubleTops: [], doubleBottoms: [] };
  const recent = candles.slice(-lookback);
  const highs = [], lows = [];
  for (let i = 2; i < recent.length - 2; i++) {
    const c = recent[i];
    const isHigh = c.h > recent[i-1].h && c.h > recent[i-2].h && c.h > recent[i+1].h && c.h > recent[i+2].h;
    const isLow  = c.l < recent[i-1].l && c.l < recent[i-2].l && c.l < recent[i+1].l && c.l < recent[i+2].l;
    if (isHigh) highs.push({ price: c.h, time: c.t, idx: i });
    if (isLow)  lows.push({ price: c.l, time: c.t, idx: i });
  }
  const doubleTops = [], doubleBottoms = [];
  // Pair highs within tolerance
  for (let i = 0; i < highs.length; i++) {
    for (let j = i + 1; j < highs.length; j++) {
      const diff = Math.abs(highs[i].price - highs[j].price) / highs[i].price;
      if (diff <= tolPct) {
        doubleTops.push({ level: (highs[i].price + highs[j].price) / 2, first: highs[i].time, second: highs[j].price, secondTime: highs[j].time, idx1: highs[i].idx, idx2: highs[j].idx });
      }
    }
  }
  for (let i = 0; i < lows.length; i++) {
    for (let j = i + 1; j < lows.length; j++) {
      const diff = Math.abs(lows[i].price - lows[j].price) / lows[i].price;
      if (diff <= tolPct) {
        doubleBottoms.push({ level: (lows[i].price + lows[j].price) / 2, first: lows[i].time, second: lows[j].price, secondTime: lows[j].time, idx1: lows[i].idx, idx2: lows[j].idx });
      }
    }
  }
  return { doubleTops, doubleBottoms };
}

// Detect FVGs (3-candle pattern) on closed candles only
function detectFVGs(candles) {
  if (candles.length < 5) return { bullish: [], bearish: [] };
  const closed = candles.slice(0, -1); // exclude forming
  const bullish = [], bearish = [];
  for (let i = 2; i < closed.length; i++) {
    const a = closed[i-2], c = closed[i];
    // Bullish FVG: candle i low > candle i-2 high
    if (c.l > a.h) {
      bullish.push({ top: c.l, bottom: a.h, ce: (c.l + a.h) / 2, time: c.t, idx: i });
    }
    // Bearish FVG: candle i high < candle i-2 low
    if (c.h < a.l) {
      bearish.push({ top: a.l, bottom: c.h, ce: (a.l + c.h) / 2, time: c.t, idx: i });
    }
  }
  return { bullish: bullish.slice(-10), bearish: bearish.slice(-10) };
}

// Check if price is near a level (within buffer)
function nearLevel(price, level, atrProxy) {
  const buffer = atrProxy * 0.15; // ~15% of daily ATR proxy
  return Math.abs(price - level) <= buffer;
}

// FX week: opens Sun 17:00 ET, closes Fri 17:00 ET — same rule ict-levels.mjs
// uses for meta.marketLikelyClosed. Covers the FX pairs, metals and index
// futures this watcher polls closely enough to avoid hammering Yahoo (and
// filling the log with fetch errors) all weekend.
function isMarketOpen() {
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
    timeZone: "America/New_York", weekday: "short", hour: "2-digit", hour12: false,
  }).formatToParts(new Date()).map((p) => [p.type, p.value]));
  const hour = parseInt(parts.hour, 10);
  return !(parts.weekday === "Sat" || (parts.weekday === "Fri" && hour >= 17) || (parts.weekday === "Sun" && hour < 17));
}

// Format time for alert
function fmtTime(ts) {
  return new Date(ts * 1000).toLocaleString("en-GB", { timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false });
}

// Send Telegram alert via OpenClaw message tool (spawned sub-agent approach)
async function sendAlert(message) {
  // We'll write a pending alert file that a tiny cron/agent picks up,
  // OR we can exec the openclaw CLI to send a message.
  // Simpler: use the gateway message tool via spawned sub-agent.
  // For now, write to alert queue file; we'll add the sender next.
  const alertFile = join(STATE_DIR, "alert-queue.json");
  await withQueueLock(() => {
    let queue = [];
    if (existsSync(alertFile)) {
      try { queue = JSON.parse(readFileSync(alertFile, "utf8")); } catch {}
    }
    queue.push({ ts: Date.now(), message });
    if (queue.length > 50) queue = queue.slice(-50);
    writeFileSync(alertFile, JSON.stringify(queue, null, 2));
  });
  log(`ALERT QUEUED: ${message.slice(0, 120)}...`);
}

// Check cooldown and send if fresh
function shouldAlert(state, asset, patternKey) {
  const key = `${asset}:${patternKey}`;
  const last = state.alerts[key] || 0;
  const now = Date.now();
  if (now - last < ALERT_COOLDOWN_MS) return false;
  state.alerts[key] = now;
  return true;
}

async function scanAsset(asset, state) {
  const symbol = symbolForAsset(asset);
  if (!symbol) { log(`${asset} ERROR: unsupported asset`); return; }
  try {
    const tick = await fetchLivePrice(symbol);
    const price = roundPrice(tick.price, asset);
    const prev = state.prices[asset] || { price };
    state.prices[asset] = { price, time: tick.timestamp, high: tick.high, low: tick.low, open: tick.open };
    
    // Initialize candle arrays
    if (!state.candles.M15[asset]) state.candles.M15[asset] = [];
    if (!state.candles.H1[asset]) state.candles.H1[asset] = [];
    
    // Roll candles
    const m15 = rollM15(state.candles.M15[asset], tick);
    rollH1(state.candles.H1[asset], state.candles.M15[asset]);
    
    // Need enough candles for patterns
    if (state.candles.M15[asset].length < 20) return;
    
    // ATR proxy from recent M15 range (rough daily ATR / sqrt(96))
    const recentM15 = state.candles.M15[asset].slice(-96);
    const ranges = recentM15.map(c => c.h - c.l).filter(r => r > 0);
    const atrProxy = ranges.length ? ranges.reduce((a,b)=>a+b,0)/ranges.length * Math.sqrt(96) : price * 0.008;
    
    // Detect patterns on M15
    const eq = detectEqualLevels(state.candles.M15[asset]);
    const fvg = detectFVGs(state.candles.M15[asset]);
    
    // Double top (EQH) revisited - price at/near the level again
    for (const dt of eq.doubleTops) {
      const eqKey = `${asset}:DT:${dt.level.toFixed(5)}`;
      if (nearLevel(price, dt.level, atrProxy) && dt.secondTime > (state.lastEqAlert?.[eqKey] || 0)) {
        if (shouldAlert(state, asset, `DT:${dt.level.toFixed(5)}`)) {
          await sendAlert(`🔴 **DOUBLE TOP** — ${asset}\nPrice ${price} revisiting EQH ${dt.level.toFixed(5)}\nFirst touch: ${fmtTime(dt.first)} | Second: ${fmtTime(dt.secondTime)}\nWatch for rejection / sell-side liquidity sweep`);
          state.lastEqAlert[eqKey] = dt.secondTime;
        }
      }
    }

    // Double bottom (EQL) revisited
    for (const db of eq.doubleBottoms) {
      const eqKey = `${asset}:DB:${db.level.toFixed(5)}`;
      if (nearLevel(price, db.level, atrProxy) && db.secondTime > (state.lastEqAlert?.[eqKey] || 0)) {
        if (shouldAlert(state, asset, `DB:${db.level.toFixed(5)}`)) {
          await sendAlert(`🟢 **DOUBLE BOTTOM** — ${asset}\nPrice ${price} revisiting EQL ${db.level.toFixed(5)}\nFirst touch: ${fmtTime(db.first)} | Second: ${fmtTime(db.secondTime)}\nWatch for rejection / buy-side liquidity sweep`);
          state.lastEqAlert[eqKey] = db.secondTime;
        }
      }
    }

    // Fresh FVG alerts (only the most recent unmitigated)
    for (const g of fvg.bullish.slice(-1)) {
      const key = `FVG_B:${asset}:${g.time}`;
      if (price >= g.bottom && price <= g.top && shouldAlert(state, asset, key)) {
        await sendAlert(`BULLISH FVG TOUCH — ${asset} (M15)\nPrice ${price} entered gap ${g.bottom.toFixed(5)} – ${g.top.toFixed(5)}\nCE: ${g.ce.toFixed(5)} | Formed: ${fmtTime(g.time)}\nContext alert only — review the validated dashboard ticket before acting.`);
      }
    }
    for (const g of fvg.bearish.slice(-1)) {
      const key = `FVG_S:${asset}:${g.time}`;
      if (price >= g.bottom && price <= g.top && shouldAlert(state, asset, key)) {
        await sendAlert(`BEARISH FVG TOUCH — ${asset} (M15)\nPrice ${price} entered gap ${g.bottom.toFixed(5)} – ${g.top.toFixed(5)}\nCE: ${g.ce.toFixed(5)} | Formed: ${fmtTime(g.time)}\nContext alert only — review the validated dashboard ticket before acting.`);
      }
    }
    
    // Log price movement for debugging
    const move = ((price - prev.price) / prev.price * 100).toFixed(3);
    if (Math.abs(move) > 0.05) log(`${asset} ${prev.price} -> ${price} (${move}%)`);
    
  } catch (e) {
    log(`${asset} ERROR: ${e.message}`);
  }
}

// Refuse to start a second instance against the same state dir — two
// watchers writing watcher-state.json / alert-queue.json independently would
// clobber each other's state and double up on alerts.
function claimSingleton() {
  if (existsSync(PID_FILE)) {
    const pid = parseInt(readFileSync(PID_FILE, "utf8").trim(), 10);
    if (pid && pid !== process.pid) {
      try {
        process.kill(pid, 0); // throws if no such process
        log(`Another watcher instance is already running (pid ${pid}) — exiting.`);
        process.exit(0);
      } catch { /* stale pidfile — previous instance died without cleaning up */ }
    }
  }
  writeFileSync(PID_FILE, String(process.pid));
}
function releaseSingleton() {
  try {
    if (existsSync(PID_FILE) && parseInt(readFileSync(PID_FILE, "utf8").trim(), 10) === process.pid) {
      unlinkSync(PID_FILE);
    }
  } catch {}
}

// Drop cooldown/dedupe entries older than ALERT_STATE_MAX_AGE_MS so state.alerts
// and state.lastEqAlert don't grow forever across a long-running/persistent process.
function pruneOldAlertState(state) {
  const cutoffMs = Date.now() - ALERT_STATE_MAX_AGE_MS;
  const cutoffSec = Math.floor(cutoffMs / 1000); // lastEqAlert stores Yahoo (seconds) timestamps
  for (const k of Object.keys(state.alerts)) if (state.alerts[k] < cutoffMs) delete state.alerts[k];
  for (const k of Object.keys(state.lastEqAlert)) if (state.lastEqAlert[k] < cutoffSec) delete state.lastEqAlert[k];
}

async function main() {
  log("=== WATCHER STARTED ===");
  log(`Watching: ${WATCHED.join(", ")}`);
  log(`Poll interval: ${POLL_INTERVAL_MS}ms`);
  log(`Max concurrent: ${MAX_CONCURRENT}, stagger: ${STAGGER_MS}ms`);

  if (!existsSync(STATE_DIR)) mkdirSync(STATE_DIR, { recursive: true });
  claimSingleton();

  let state = loadState();
  if (!state.lastEqAlert) state.lastEqAlert = {};
  if (!state.alerts) state.alerts = {};

  let lastSave = Date.now();
  let wasMarketOpen = null; // null = not yet logged either way

  async function loop() {
    const open = isMarketOpen();
    if (open !== wasMarketOpen) {
      log(open ? "Market open — resuming polling" : "Market closed (weekend) — pausing polling until reopen");
      wasMarketOpen = open;
    }
    if (!open) {
      if (Date.now() - lastSave > STATE_SAVE_INTERVAL_MS) { saveState(state); lastSave = Date.now(); }
      return;
    }

    // Staggered, limited concurrency
    const batches = [];
    for (let i = 0; i < WATCHED.length; i += MAX_CONCURRENT) {
      batches.push(WATCHED.slice(i, i + MAX_CONCURRENT));
    }

    for (const batch of batches) {
      await Promise.all(batch.map(a => scanAsset(a, state)));
      if (batches.indexOf(batch) < batches.length - 1) {
        await new Promise(r => setTimeout(r, STAGGER_MS));
      }
    }

    if (Date.now() - lastSave > STATE_SAVE_INTERVAL_MS) {
      pruneOldAlertState(state);
      saveState(state);
      lastSave = Date.now();
    }
  }

  // Initial run
  await loop();

  // Self-rescheduling timer (not setInterval) so a slow cycle — network
  // trouble, provider backoff — can never overlap with the next one and race
  // on the shared `state` object.
  let stopped = false;
  let busy = false;
  async function tick() {
    if (stopped) return;
    if (busy) { log("Previous cycle still running — skipping this tick"); }
    else {
      busy = true;
      try { await loop(); } catch (e) { log(`LOOP ERROR: ${e.message}`); } finally { busy = false; }
    }
    if (!stopped) setTimeout(tick, POLL_INTERVAL_MS);
  }
  setTimeout(tick, POLL_INTERVAL_MS);

  // Graceful shutdown
  const shutdown = () => {
    log("Shutting down...");
    stopped = true;
    saveState(state);
    releaseSingleton();
    process.exit(0);
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
}

main().catch(e => { log(`FATAL: ${e.message}`); releaseSingleton(); process.exit(1); });