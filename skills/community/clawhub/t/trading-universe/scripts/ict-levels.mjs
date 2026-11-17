#!/usr/bin/env node
// ict-levels.mjs — deterministic ICT primitives from Yahoo Finance v8 chart API.
// Usage: node ict-levels.mjs XAUUSD   → full JSON for one asset (ends with `candidate`)
//        node ict-levels.mjs scan     → whole watchlist: who has a valid entry right now
// Prints one JSON object. On failure prints {"error": "..."} and exits 0 so the
// calling model reports the problem instead of inventing numbers.


// Format a candle timestamp in the user's own timezone (e.g. "Wed 07:45") so
// every level (FVG, OB, dealing-range edge) tells you which candle on YOUR
// chart printed it — price feeds drift by a small offset, time doesn't.
const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
const fmtLT = (t) => t ? new Intl.DateTimeFormat("en-GB", { timeZone: localTz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(t * 1000)).replace(",", "") : null;

// Saved fundamentals leaderboard (written by the assistant after each run):
// technical tickets that fight a high-conviction macro verdict get demoted,
// aligned ones promoted. Fail-soft: missing or stale (>36h) board = no effect.
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { filterForwardDraws, findFvgs, findOrderBlocks, zoneFreshnessLabel } from "./zone-lifecycle.mjs";
import { DEFAULT_ASSETS, FUTURES_SYMBOLS, normalizeAsset, symbolForAsset } from "./symbols.mjs";
import { adaptDiscoveredTicket, buildTicketDiscoveryEngine, selectActionableTickets } from "./tde-entry-engine.mjs";
const DATA_DIR = process.env.TRADE_DATA_DIR || join(homedir(), ".trading-universe");
const TRADES_FILE = process.env.TRADES_FILE || join(DATA_DIR, "live-trades.json");

function loadFundamentals() {
  try {
    const j = JSON.parse(readFileSync(join(DATA_DIR, "fundamentals.json"), "utf8"));
    if (!j?.items?.length || !j.asOf) return null;
    const ageH = (Date.now() - new Date(j.asOf).getTime()) / 36e5;
    if (!(ageH >= 0) || ageH > 36) return null; // a stale macro board is worse than none
    const map = {};
    for (const it of j.items) map[normalizeAsset(it.asset)] = { direction: it.direction, score: it.score, asOf: j.asOf };
    return map;
  } catch { return null; }
}
const FUNDAMENTALS = loadFundamentals();

// Lessons from the user's own tracked trades (dashboard trade log): per-setup
// outcome stats + recent situation→result lines. Deep-read models consult
// this so the system learns from its track record. Fail-soft: null when the
// log is missing or has no closed trades.
function loadLessons() {
  try {
    const j = JSON.parse(readFileSync(TRADES_FILE, "utf8"));
    const closed = (j.trades || []).filter((t) => t.status === "closed" && t.rMultiple != null);
    if (!closed.length) return null;
    const fam = (s) => String(s || "").split("@")[0].replace(/\(.*?\)/g, "").trim() || "unknown";
    const bySetup = {};
    for (const t of closed) {
      const a = (bySetup[fam(t.setup)] ||= { trades: 0, wins: 0, losses: 0, totalR: 0 });
      a.trades++;
      if (t.rMultiple > 0) a.wins++; else if (t.rMultiple < 0) a.losses++;
      a.totalR = Number((a.totalR + t.rMultiple).toFixed(2));
    }
    const recent = closed.slice(-8).map((t) => t.lesson ||
      `${t.asset} ${t.direction} ${fam(t.setup)}${t.fundamentals ? ` · macro ${t.fundamentals.direction} ${t.fundamentals.score}/5` : ""} · ${t.killzone || "kz?"} → ${t.outcome} (${t.rMultiple > 0 ? "+" : ""}${t.rMultiple}R)`);
    return { closedTrades: closed.length, bySetup, recent };
  } catch { return null; }
}
const LESSONS = loadLessons();

function fail(msg) {
  console.log(JSON.stringify({ error: msg }));
  process.exit(0);
}

// Zones and structure must come from CLOSED candles only — a forming candle
// can print an FVG or a BOS that no longer exists at candle close.
function closedOnly(candles, intervalSec) {
  const last = candles[candles.length - 1];
  if (last && (last.complete === false || Date.now() / 1000 - last.t < intervalSec)) {
    return candles.slice(0, -1);
  }
  return candles;
}

async function fetchCandles(sym, interval, range) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sym)}?interval=${interval}&range=${range}`;
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(url, {
        headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" },
        signal: AbortSignal.timeout(15000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const j = await res.json();
      const r = j?.chart?.result?.[0];
      if (!r?.timestamp?.length) throw new Error(j?.chart?.error?.description || "empty result");
      const q = r.indicators.quote[0];
      const candles = [];
      for (let i = 0; i < r.timestamp.length; i++) {
        const o = q.open[i], h = q.high[i], l = q.low[i], cc = q.close[i];
        if (o == null || h == null || l == null || cc == null) continue;
        // impossible bars (feed glitches) would print false swings and pools
        if (h < l || h < o || h < cc || l > o || l > cc) continue;
        candles.push({ t: r.timestamp[i], o, h, l, c: cc, v: q.volume?.[i] ?? null });
      }
      if (candles.length < 20) throw new Error("too few candles");
      return { candles, livePrice: r.meta?.regularMarketPrice ?? candles[candles.length - 1].c };
    } catch (e) {
      if (attempt === 1) throw new Error(`${sym} ${interval}: ${e.message}`);
      await new Promise((r2) => setTimeout(r2, 1500));
    }
  }
}

function resample(candles, hours) {
  const out = [];
  const size = hours * 3600;
  let cur = null;
  for (const c of candles) {
    const bucket = Math.floor(c.t / size) * size;
    if (!cur || cur.t !== bucket) {
      if (cur) out.push(cur);
      cur = { t: bucket, o: c.o, h: c.h, l: c.l, c: c.c };
    } else {
      cur.h = Math.max(cur.h, c.h);
      cur.l = Math.min(cur.l, c.l);
      cur.c = c.c;
    }
  }
  if (cur) out.push(cur);
  return out;
}

function atr(candles, period = 14) {
  const trs = [];
  for (let i = 1; i < candles.length; i++) {
    const p = candles[i - 1], c = candles[i];
    trs.push(Math.max(c.h - c.l, Math.abs(c.h - p.c), Math.abs(c.l - p.c)));
  }
  const last = trs.slice(-period);
  return last.reduce((a, b) => a + b, 0) / last.length;
}

// ---- classic indicator pack (RSI / EMA / MACD / Bollinger / Stochastic) ----
// Standard-settings, closes-only math for the dashboard's deep-detail Raw tab.
// Context only: NONE of these feed the deterministic setup engine, the debate
// scoring or the ticket math — ICT levels stay the single source of decisions.
function emaLast(closes, period) {
  if (closes.length < period) return null;
  const k = 2 / (period + 1);
  let e = closes.slice(0, period).reduce((a, b) => a + b, 0) / period;
  for (let i = period; i < closes.length; i++) e = closes[i] * k + e * (1 - k);
  return e;
}
function rsiLast(closes, period = 14) {
  if (closes.length < period + 1) return null;
  let gain = 0, loss = 0;
  for (let i = 1; i <= period; i++) { const d = closes[i] - closes[i - 1]; if (d >= 0) gain += d; else loss -= d; }
  gain /= period; loss /= period;
  for (let i = period + 1; i < closes.length; i++) {
    const d = closes[i] - closes[i - 1];
    gain = (gain * (period - 1) + Math.max(d, 0)) / period;
    loss = (loss * (period - 1) + Math.max(-d, 0)) / period;
  }
  if (loss === 0) return 100;
  return 100 - 100 / (1 + gain / loss);
}
function macdLast(closes, fast = 12, slow = 26, sig = 9) {
  if (closes.length < slow + sig) return null;
  const emaSeries = (p) => {
    const k = 2 / (p + 1), out = [];
    let e = closes.slice(0, p).reduce((a, b) => a + b, 0) / p;
    out[p - 1] = e;
    for (let i = p; i < closes.length; i++) { e = closes[i] * k + e * (1 - k); out[i] = e; }
    return out;
  };
  const ef = emaSeries(fast), es = emaSeries(slow);
  const line = [];
  for (let i = slow - 1; i < closes.length; i++) line.push(ef[i] - es[i]);
  const k = 2 / (sig + 1);
  let s = line.slice(0, sig).reduce((a, b) => a + b, 0) / sig;
  for (let i = sig; i < line.length; i++) s = line[i] * k + s * (1 - k);
  const l = line[line.length - 1];
  return { line: l, signal: s, hist: l - s };
}
function bollingerLast(closes, period = 20, mult = 2) {
  if (closes.length < period) return null;
  const w = closes.slice(-period);
  const mid = w.reduce((a, b) => a + b, 0) / period;
  const sd = Math.sqrt(w.reduce((a, b) => a + (b - mid) * (b - mid), 0) / period);
  const upper = mid + mult * sd, lower = mid - mult * sd;
  const px = closes[closes.length - 1];
  return {
    upper, mid, lower,
    pctB: upper === lower ? null : ((px - lower) / (upper - lower)) * 100,
    widthPct: mid ? ((upper - lower) / mid) * 100 : null,
  };
}
function stochLast(candles, kP = 14, smooth = 3, dP = 3) {
  if (candles.length < kP + smooth + dP) return null;
  const rawK = [];
  for (let i = kP - 1; i < candles.length; i++) {
    let hi = -Infinity, lo = Infinity;
    for (let j = i - kP + 1; j <= i; j++) { if (candles[j].h > hi) hi = candles[j].h; if (candles[j].l < lo) lo = candles[j].l; }
    rawK.push(hi === lo ? 50 : ((candles[i].c - lo) / (hi - lo)) * 100);
  }
  const sma = (arr, p, end) => arr.slice(end - p + 1, end + 1).reduce((a, b) => a + b, 0) / p;
  const kS = [];
  for (let i = smooth - 1; i < rawK.length; i++) kS.push(sma(rawK, smooth, i));
  return { k: kS[kS.length - 1], d: sma(kS, dP, kS.length - 1) };
}

// Fractal swing points, k candles each side.
function swings(candles, k = 2) {
  const highs = [], lows = [];
  for (let i = k; i < candles.length - k; i++) {
    let isH = true, isL = true;
    for (let j = 1; j <= k; j++) {
      if (candles[i].h <= candles[i - j].h || candles[i].h <= candles[i + j].h) isH = false;
      if (candles[i].l >= candles[i - j].l || candles[i].l >= candles[i + j].l) isL = false;
    }
    if (isH) highs.push({ t: candles[i].t, p: candles[i].h });
    if (isL) lows.push({ t: candles[i].t, p: candles[i].l });
  }
  return { highs, lows };
}

// Structure from the alternating swing sequence: merge swing highs/lows
// chronologically, collapse consecutive same-side swings to their extreme,
// then read HH/HL vs LH/LL off the last two legs. CHoCH = the bias of the
// previous leg pair differs from the current one.
function structure(candles) {
  const { highs, lows } = swings(candles);
  // Too few fractal swings for a directional (HH/HL vs LH/LL) read. This is a
  // data-window limitation, not a claim the market has "no structure" — so
  // still surface whatever high/low we DO have; scoreStructure() turns that
  // into a real "ranging between X and Y" readout instead of a dead end.
  if (highs.length < 2 || lows.length < 2) {
    const hi = highs.length ? highs.reduce((a, b) => (b.p > a.p ? b : a)) : null;
    const lo = lows.length ? lows.reduce((a, b) => (b.p < a.p ? b : a)) : null;
    return {
      bias: "range",
      lastSwingHigh: hi?.p ?? null, lastSwingLow: lo?.p ?? null,
      lastSwingHighAt: hi?.t ?? null, lastSwingHighAtLocal: fmtLT(hi?.t),
      lastSwingLowAt: lo?.t ?? null, lastSwingLowAtLocal: fmtLT(lo?.t),
      lastClose: candles[candles.length - 1]?.c ?? null,
      note: "too few swings in this window for a directional read",
    };
  }
  const merged = [
    ...highs.map((h) => ({ ...h, side: "H" })),
    ...lows.map((l) => ({ ...l, side: "L" })),
  ].sort((a, b) => a.t - b.t);
  const seq = [];
  for (const s of merged) {
    const last = seq[seq.length - 1];
    if (last && last.side === s.side) {
      if ((s.side === "H" && s.p > last.p) || (s.side === "L" && s.p < last.p)) seq[seq.length - 1] = s;
    } else seq.push(s);
  }
  const hs = seq.filter((s) => s.side === "H"), ls = seq.filter((s) => s.side === "L");
  if (hs.length < 2 || ls.length < 2) {
    const hi = hs[hs.length - 1], lo = ls[ls.length - 1];
    return {
      bias: "range",
      lastSwingHigh: hi?.p ?? null, lastSwingLow: lo?.p ?? null,
      lastSwingHighAt: hi?.t ?? null, lastSwingHighAtLocal: fmtLT(hi?.t),
      lastSwingLowAt: lo?.t ?? null, lastSwingLowAtLocal: fmtLT(lo?.t),
      lastClose: candles[candles.length - 1]?.c ?? null,
      note: "not enough alternating swings in this window for a directional read",
    };
  }
  const biasOf = (hPair, lPair) => {
    const hh = hPair[1].p > hPair[0].p, hl = lPair[1].p > lPair[0].p;
    const lh = hPair[1].p < hPair[0].p, ll = lPair[1].p < lPair[0].p;
    return hh && hl ? "bullish" : lh && ll ? "bearish" : "range";
  };
  const [h1, h2] = hs.slice(-2), [l1, l2] = ls.slice(-2);
  const bias = biasOf([h1, h2], [l1, l2]);
  let choch = false, chochLevel = null;
  if (hs.length >= 3 && ls.length >= 3) {
    const prevBias = biasOf(hs.slice(-3, -1), ls.slice(-3, -1));
    if (prevBias !== "range" && bias !== "range" && prevBias !== bias) {
      choch = true;
      // The swing whose break flipped the bias.
      chochLevel = bias === "bullish" ? h1.p : l1.p;
    }
  }
  const lastClose = candles[candles.length - 1].c;
  const bosUp = lastClose > h2.p, bosDown = lastClose < l2.p;
  // When did the break actually CONFIRM? The first close beyond the swing
  // after the swing printed — so a ticket born from this BOS can say "valid
  // since <that candle>", not just "since the scan that noticed it".
  let bosUpAt = null, bosDownAt = null;
  if (bosUp) { const bc = candles.find((c) => c.t > h2.t && c.c > h2.p); bosUpAt = bc ? bc.t : null; }
  if (bosDown) { const bc = candles.find((c) => c.t > l2.t && c.c < l2.p); bosDownAt = bc ? bc.t : null; }
  return {
    bias,
    lastSwingHigh: h2.p,
    lastSwingLow: l2.p,
    lastSwingHighAt: h2.t, lastSwingHighAtLocal: fmtLT(h2.t),
    lastSwingLowAt: l2.t, lastSwingLowAtLocal: fmtLT(l2.t),
    bosUp,
    bosDown,
    bosUpAt, bosUpAtLocal: fmtLT(bosUpAt),
    bosDownAt, bosDownAtLocal: fmtLT(bosDownAt),
    lastClose,
    choch,
    chochLevel,
    note: "alternating swing-sequence read",
  };
}

// Swing high+low pair bracketing current price = dealing range. Starts from
// the nearest bracketing levels and widens (nearer side first) until the
// range spans at least 0.6×daily-ATR — a micro-range gives meaningless
// premium/discount zoning.
function dealingRange(candles, price, atrD) {
  const { highs, lows } = swings(candles);
  const ups = highs.filter((h) => h.p > price).sort((a, b) => a.p - b.p);
  const dns = lows.filter((l) => l.p < price).sort((a, b) => b.p - a.p);
  if (!ups.length || !dns.length) return null;
  let ui = 0, di = 0;
  while (ups[ui].p - dns[di].p < 0.6 * atrD) {
    const canUp = ui + 1 < ups.length, canDn = di + 1 < dns.length;
    if (!canUp && !canDn) break;
    if (canUp && (!canDn || ups[ui].p - price <= price - dns[di].p)) ui++;
    else di++;
  }
  const hiP = ups[ui].p, loP = dns[di].p;
  const hiT = ups[ui].t, loT = dns[di].t;
  const eq = (hiP + loP) / 2;
  const pos = ((price - loP) / (hiP - loP)) * 100;
  return {
    high: hiP,
    low: loP,
    // The exact candles that set each edge — so the same box (and its 50%
    // equilibrium line) can be redrawn on the user's own TradingView chart
    // by time, independent of any price-feed offset.
    highAt: hiT, lowAt: loT,
    highAtLocal: fmtLT(hiT), lowAtLocal: fmtLT(loT),
    equilibrium: eq,
    positionPct: Math.round(pos),
    zone: pos > 60 ? "premium" : pos < 40 ? "discount" : "equilibrium",
  };
}

// 3-candle fair value gaps, kept if unmitigated (<50% filled), near price,
// fresh (younger than maxAgeSec — a weeks-old gap is not an intraday anchor),
// and at least minSize tall — sub-noise gaps produce untradeable 1-pip stops.
function fvgs(candles, atrD, price, minSize, maxAgeSec) {
  const bull = [], bear = [];
  for (let i = 2; i < candles.length; i++) {
    const a = candles[i - 2], c = candles[i];
    if (c.l > a.h) {
      // bullish FVG between a.h (floor) and c.l (top)
      let minLow = Infinity;
      for (let j = i + 1; j < candles.length; j++) minLow = Math.min(minLow, candles[j].l);
      const size = c.l - a.h;
      const filled = minLow === Infinity ? 0 : Math.max(0, Math.min(1, (c.l - minLow) / size));
      if (size >= minSize && filled < 0.5) bull.push({ top: c.l, bottom: a.h, ce: (c.l + a.h) / 2, t: c.t, atLocal: fmtLT(c.t) });
    }
    if (c.h < a.l) {
      let maxHigh = -Infinity;
      for (let j = i + 1; j < candles.length; j++) maxHigh = Math.max(maxHigh, candles[j].h);
      const size = a.l - c.h;
      const filled = maxHigh === -Infinity ? 0 : Math.max(0, Math.min(1, (maxHigh - c.h) / size));
      if (size >= minSize && filled < 0.5) bear.push({ top: a.l, bottom: c.h, ce: (a.l + c.h) / 2, t: c.t, atLocal: fmtLT(c.t) });
    }
  }
  const nowSec = Date.now() / 1000;
  const near = (g) => Math.abs(g.ce - price) < 1.5 * atrD && nowSec - g.t <= maxAgeSec;
  return { bullish: bull.filter(near).slice(-4), bearish: bear.filter(near).slice(-4) };
}

// Order blocks: the last opposite-close candle immediately before a
// displacement that creates an FVG (the OB candle is bar 1 of the 3-bar gap
// pattern). Kept while unviolated (no close through the far edge), near
// price, fresh, and at least minSize tall.
function orderBlocks(candles, atrD, price, minSize, maxAgeSec) {
  const bull = [], bear = [];
  for (let i = 0; i + 2 < candles.length; i++) {
    const a = candles[i], c = candles[i + 2];
    if (a.c < a.o && c.l > a.h) {
      // down-close candle followed by a bullish FVG displacement
      let violated = false;
      for (let j = i + 3; j < candles.length; j++) if (candles[j].c < a.l) { violated = true; break; }
      if (!violated && a.h - a.l >= minSize) bull.push({ top: a.h, bottom: a.l, mid: (a.h + a.l) / 2, t: a.t, atLocal: fmtLT(a.t) });
    }
    if (a.c > a.o && c.h < a.l) {
      let violated = false;
      for (let j = i + 3; j < candles.length; j++) if (candles[j].c > a.h) { violated = true; break; }
      if (!violated && a.h - a.l >= minSize) bear.push({ top: a.h, bottom: a.l, mid: (a.h + a.l) / 2, t: a.t, atLocal: fmtLT(a.t) });
    }
  }
  const nowSec = Date.now() / 1000;
  const near = (g) => Math.abs(g.mid - price) < 1.5 * atrD && nowSec - g.t <= maxAgeSec;
  return { bullish: bull.filter(near).slice(-3), bearish: bear.filter(near).slice(-3) };
}

// Equal highs/lows: clusters of >=2 swing points within tolerance. The pool
// sits at the extreme of the cluster (where the stops actually rest); we also
// return how many swings formed it and WHEN the most recent one printed, so the
// card/dashboard can tell the user which candle to look at on the chart.
function eqClusters(points, tol, side) {
  const sorted = points.slice().sort((a, b) => a.p - b.p);
  const groups = [];
  let group = [];
  for (const s of sorted) {
    if (!group.length || s.p - group[0].p <= tol) group.push(s);
    else { if (group.length >= 2) groups.push(group); group = [s]; }
  }
  if (group.length >= 2) groups.push(group);
  return groups.map((g) => {
    const ext = g.reduce((a, c) => (side === "high" ? (c.p > a.p ? c : a) : (c.p < a.p ? c : a)));
    const last = g.reduce((a, c) => (c.t > a.t ? c : a)); // freshest touch of the level
    return { level: ext.p, at: last.t, count: g.length };
  });
}

// Session + prior-period liquidity levels from intraday candles (UTC windows).
// Buy-side liquidity = stops resting above HIGHS; sell-side = below LOWS.
// So `above` only ever contains highs and `below` only lows — an old session
// low sitting above price is NOT a target pool.
function liquidity(daily, m15, h1, price, atrD) {
  const levels = [];
  // Format a candle timestamp in the user's own timezone (e.g. "Wed 07:45") so
  // each pool tells you which candle on your chart printed it.
  const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  const fmtLT = (t) => t ? new Intl.DateTimeFormat("en-GB", { timeZone: localTz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(t * 1000)).replace(",", "") : null;
  const days = {};
  const nyDate = (t, shiftHours = 0) => {
    const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/New_York", year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(new Date((t + shiftHours * 3600) * 1000)).map((p) => [p.type, p.value]));
    return `${parts.year}-${parts.month}-${parts.day}`;
  };
  for (const c of m15) {
    const np = tzParts(new Date(c.t * 1000), "America/New_York");
    const hour = parseInt(np.hour, 10);
    const sess = hour >= 19 ? "asia" : hour >= 2 && hour < 5 ? "london" : hour >= 8 && hour < 11 ? "newyork" : null;
    if (!sess) continue;
    // The Asia evening belongs to the following New York trading day.
    const d = nyDate(c.t, sess === "asia" ? 5 : 0);
    days[d] ||= {};
    const bucket = (days[d][sess] ||= { h: -Infinity, l: Infinity, hT: null, lT: null });
    if (c.h > bucket.h) { bucket.h = c.h; bucket.hT = c.t; }
    if (c.l < bucket.l) { bucket.l = c.l; bucket.lT = c.t; }
  }
  const dayKeys = Object.keys(days).sort();
  const today = dayKeys[dayKeys.length - 1];
  for (const dk of dayKeys.slice(-2)) {
    for (const [sess, v] of Object.entries(days[dk])) {
      const tag = dk === today ? "today" : "prev";
      levels.push({ level: v.h, label: `${sess} high (${tag})`, side: "high", tf: "M15", at: v.hT, atLocal: fmtLT(v.hT) });
      levels.push({ level: v.l, label: `${sess} low (${tag})`, side: "low", tf: "M15", at: v.lT, atLocal: fmtLT(v.lT) });
    }
  }
  // Previous day from dailies — but spot/CFD brokers anchor the daily candle
  // at 17:00 New York while Yahoo anchors near midnight UTC. When the m15
  // series covers the previous NY-anchored trading day, rebuild PDH/PDL from
  // it so the levels match what the user's chart calls "yesterday".
  let pdPushed = false;
  {
    const nyFmt = new Intl.DateTimeFormat("en-CA", { timeZone: "America/New_York" });
    const tradingDay = (t) => nyFmt.format(new Date((t + 7 * 3600) * 1000));
    const byDay = {};
    for (const c of m15) {
      const k = tradingDay(c.t);
      const d = (byDay[k] ||= { h: -Infinity, l: Infinity, n: 0, hT: null, lT: null });
      if (c.h > d.h) { d.h = c.h; d.hT = c.t; }
      if (c.l < d.l) { d.l = c.l; d.lT = c.t; }
      d.n++;
    }
    const keys = Object.keys(byDay).sort();
    const prev = keys[keys.length - 2];
    if (prev && byDay[prev].n >= 50) { // reasonably complete day
      levels.push({ level: byDay[prev].h, label: "PDH", side: "high", tf: "D", at: byDay[prev].hT, atLocal: fmtLT(byDay[prev].hT) },
                  { level: byDay[prev].l, label: "PDL", side: "low", tf: "D", at: byDay[prev].lT, atLocal: fmtLT(byDay[prev].lT) });
      pdPushed = true;
    }
  }
  if (!pdPushed && daily.length >= 2) {
    const pd = daily[daily.length - 2];
    levels.push({ level: pd.h, label: "PDH", side: "high", tf: "D", at: pd.t, atLocal: fmtLT(pd.t) },
                { level: pd.l, label: "PDL", side: "low", tf: "D", at: pd.t, atLocal: fmtLT(pd.t) });
  }
  const weekAgo = daily.slice(-6, -1);
  if (weekAgo.length) {
    const wh = weekAgo.reduce((a, c) => (c.h > a.h ? c : a));
    const wl = weekAgo.reduce((a, c) => (c.l < a.l ? c : a));
    levels.push({ level: wh.h, label: "prev-week high", side: "high", tf: "D", at: wh.t, atLocal: fmtLT(wh.t) });
    levels.push({ level: wl.l, label: "prev-week low", side: "low", tf: "D", at: wl.t, atLocal: fmtLT(wl.t) });
  }
  // Equal highs/lows on H1 (last 20 swings, 0.1×ATR_D tolerance) — resting
  // stop clusters, classic draw targets. Count = how many swings formed the pool.
  const h1sw = swings(h1);
  for (const cl of eqClusters(h1sw.highs.slice(-20), 0.1 * atrD, "high")) {
    levels.push({ level: cl.level, label: `equal highs (EQH ×${cl.count})`, side: "high", tf: "H1", at: cl.at, atLocal: fmtLT(cl.at) });
  }
  for (const cl of eqClusters(h1sw.lows.slice(-20), 0.1 * atrD, "low")) {
    levels.push({ level: cl.level, label: `equal lows (EQL ×${cl.count})`, side: "low", tf: "H1", at: cl.at, atLocal: fmtLT(cl.at) });
  }
  // Swept flag: within the last ~24h of bars price wicked beyond the level
  // AND some candle CLOSED back inside afterwards (the stop-run signature) AND
  // price still trades inside now. A wick that never closed back is a
  // breakout, not a sweep — that distinction is what makes sweep-reversal
  // entries reliable.
  const recent = m15.slice(-96);
  // Returns the wick time of the LAST confirmed sweep (wick beyond + a later
  // close back inside), or null. The timestamp lets setups demand that the
  // displacement came AFTER the raid — the 2022-model sequence.
  const sweptInfo = (lvl, side) => {
    let wickT = null, confirmed = false;
    for (const c of recent) {
      if (side === "high" ? c.h > lvl : c.l < lvl) { wickT = c.t; confirmed = false; }
      if (wickT != null && (side === "high" ? c.c < lvl : c.c > lvl)) confirmed = true;
    }
    return confirmed ? wickT : null;
  };
  // "Touched" (but not confirmed-swept): price reached the level at least once
  // in the recent window without the close-back-inside that sweptInfo demands.
  // A pool price has already delivered to is a spent magnet — DOL skips it.
  const touchedInfo = (lvl, side) => {
    let t = null;
    for (const c of recent) if (side === "high" ? c.h >= lvl : c.l <= lvl) t = c.t;
    return t;
  };
  for (const lv of levels) {
    const t0 = sweptInfo(lv.level, lv.side);
    lv.swept = t0 != null && (lv.side === "high" ? price < lv.level : price > lv.level);
    if (lv.swept) lv.sweptAt = t0;
    lv.touchedAt = touchedInfo(lv.level, lv.side);
    lv.touched = !lv.swept && lv.touchedAt != null;
  }
  const inRange = (lv) => Math.abs(lv.level - price) < 2 * atrD;
  const above = levels.filter((l) => l.side === "high" && l.level > price && inRange(l)).sort((a, b) => a.level - b.level);
  const below = levels.filter((l) => l.side === "low" && l.level < price && inRange(l)).sort((a, b) => b.level - a.level);
  return { above: above.slice(0, 6), below: below.slice(0, 6) };
}

const DOW = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
// Parts of `date` in a given IANA timezone.
function tzParts(date, tz) {
  return Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
    timeZone: tz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false,
  }).formatToParts(date).map((p) => [p.type, p.value]));
}
// Next Date at which it is `targetDow` `targetHour`:00 in New York time, on or
// after `from`. Steps hour-by-hour (ET is a whole-hour offset from UTC, so
// flooring local minutes to :00 lands on :00 ET too).
function nextNyTime(from, targetDow, targetHour) {
  for (let i = 0; i < 8 * 24; i++) {
    const d = new Date(from.getTime() + i * 3600 * 1000);
    const p = tzParts(d, "America/New_York");
    if (DOW[p.weekday] === targetDow && parseInt(p.hour, 10) === targetHour) {
      return new Date(d.getTime() - d.getMinutes() * 60000 - d.getSeconds() * 1000 - d.getMilliseconds());
    }
  }
  return null;
}
// Which major market center is actually open right now — distinct from
// "killzone" (ICT's narrow high-probability windows). Standard retail-forex
// session hours in ET: Tokyo 19:00–04:00, London 03:00–12:00, New York
// 08:00–17:00 (overlaps are the highest-liquidity stretches; the 17:00–19:00
// gap between NY close and Tokyo open is the thinnest part of the day).
function activeSession(nyHour) {
  const tokyo = nyHour >= 19 || nyHour < 4;
  const london = nyHour >= 3 && nyHour < 12;
  const newyork = nyHour >= 8 && nyHour < 17;
  if (london && newyork) return "London/New York overlap";
  if (tokyo && london) return "Tokyo/London overlap";
  if (tokyo) return "Tokyo session";
  if (london) return "London session";
  if (newyork) return "New York session";
  return "between sessions — thin liquidity";
}
// The clock the USER sees is their own machine timezone. The FX week and ICT
// killzones are anchored in New York time (open Sun 17:00 ET, close Fri 17:00 ET;
// London KZ 02:00–05:00 ET, NY AM KZ 08:00–11:00 ET) so they are correct wherever
// the user runs this.
function sessionClock() {
  const now = new Date();
  const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  const lp = tzParts(now, localTz);
  const ny = tzParts(now, "America/New_York");
  const nyHour = parseInt(ny.hour, 10);
  const marketOpen = !(ny.weekday === "Sat" || (ny.weekday === "Fri" && nyHour >= 17) || (ny.weekday === "Sun" && nyHour < 17));
  let killzone;
  if (!marketOpen) killzone = "weekend — market closed";
  else if (nyHour >= 2 && nyHour < 5) killzone = "London KZ (active)";
  else if (nyHour >= 8 && nyHour < 11) killzone = "NY AM KZ (active)";
  else killzone = "outside killzones";
  const session = marketOpen ? activeSession(nyHour) : null;
  const openAt = marketOpen ? null : nextNyTime(now, 0, 17);   // Sunday 17:00 ET
  const closeAt = marketOpen ? nextNyTime(now, 5, 17) : null;  // Friday 17:00 ET
  const fmtLocal = (d) => d == null ? null : new Intl.DateTimeFormat("en-GB", {
    timeZone: localTz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false,
  }).format(d).replace(",", "");
  return {
    local: `${lp.weekday} ${lp.hour}:${lp.minute}`,
    tz: localTz,
    killzone,
    session,
    marketOpen,
    reopenLocal: fmtLocal(openAt),
    reopenInMin: openAt ? Math.round((openAt - now) / 60000) : null,
    closeLocal: fmtLocal(closeAt),
    closeInMin: closeAt ? Math.round((closeAt - now) / 60000) : null,
  };
}

function round(x, price) {
  const dp = price > 500 ? 1 : price > 5 ? 3 : 5;
  return Number(x.toFixed(dp));
}

// High-impact news awareness (ForexFactory weekly calendar, keyless).
// Fail-soft: any problem returns null and the analysis proceeds without it.
function newsCurrencies(symbol) {
  if (FUTURES_SYMBOLS.has(symbol)) return ["USD"];
  const m = symbol.match(/^([A-Z]{3})([A-Z]{3})=X$/);
  return m ? [m[1], m[2]] : [];
}

async function fetchCalendar() {
  const url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json";
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(url, {
        headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" },
        signal: AbortSignal.timeout(15000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const j = await res.json();
      if (!Array.isArray(j)) throw new Error("unexpected calendar format");
      return j;
    } catch {
      if (attempt === 1) return null;
      await new Promise((r) => setTimeout(r, 1500));
    }
  }
  return null;
}

// Events for this asset's currencies: High impact within 12h ahead (Medium
// only within 2h), plus anything that started in the last 30 min. Titles are
// untrusted external text — sanitized hard.
function newsRisk(calendar, symbol) {
  if (!calendar) return null;
  const ccys = new Set(newsCurrencies(symbol));
  if (!ccys.size) return null;
  const now = Date.now();
  const out = [];
  for (const ev of calendar) {
    const ccy = String(ev?.country || "").toUpperCase();
    if (!ccys.has(ccy)) continue;
    const impact = String(ev?.impact || "");
    const t = Date.parse(ev?.date);
    if (!Number.isFinite(t)) continue;
    const inMin = Math.round((t - now) / 60000);
    if (inMin < -30 || inMin > 720) continue;
    if (impact !== "High" && !(impact === "Medium" && inMin <= 120)) continue;
    const event = String(ev?.title || "").replace(/[^A-Za-z0-9 .%-]/g, "").slice(0, 40);
    out.push({ ccy, event, inMin, impact });
  }
  out.sort((a, b) => a.inMin - b.inMin);
  return out.slice(0, 4);
}

// Applies the playbook to the analyzed JSON and returns ALL qualifying order
// tickets, best first. Rules the model also follows: RR ≥ 1.5, ticket ordering
// sanity, confluence stars; rank = stars, then proximity to current price,
// then tighter stop. entryType "limit" = resting retracement order (may never
// fill); "market" = actionable at the current price right now. Every ticket
// carries whyEntry/whySL anchors so the user can verify levels on their chart.
function pickSetup(o) {
  if (o.meta.marketLikelyClosed) return [];
  const price = o.meta.price;
  const atrD = o.meta.atrDaily;
  const buf = o.meta.slBuffer, minStop = o.meta.minStopDistance;
  const rd = (x) => round(x, price);
  const dr = o.dealingRange4H;
  const s = o.structure;
  const kzActive = /active/i.test(o.meta.killzone);
  const above = o.liquidity.above, below = o.liquidity.below;
  const fd = o.meta.fundamentals;
  const regime = o.meta.regime || {};
  const opposesMacro = (dir) => fd && fd.score >= 3
    && ((dir === "LONG" && fd.direction === "Bearish") || (dir === "SHORT" && fd.direction === "Bullish"));
  const alignsMacro = (dir) => fd && fd.score >= 3
    && ((dir === "LONG" && fd.direction === "Bullish") || (dir === "SHORT" && fd.direction === "Bearish"));
  const countersTrendDay = (dir) => regime.trendDay
    && ((regime.direction === "up" && dir === "SHORT") || (regime.direction === "down" && dir === "LONG"));
  // TP2 must sit meaningfully beyond TP1 or it's not a runner target.
  const minTpSep = 0.25 * atrD;
  const nextAbove = (from) => above.find((l) => l.level > from + minTpSep);
  const nextBelow = (from) => below.find((l) => l.level < from - minTpSep);
  const cands = [];
  const fvgList = (side) => [
    ...o.fvgs.H1[side].map((g) => ({ ...g, tf: "H1", kind: "FVG" })),
    ...o.fvgs.M15[side].map((g) => ({ ...g, tf: "M15", kind: "FVG" })),
  ];
  // Entry anchors = FVGs plus order blocks; both carry entry/sl/top/bottom.
  const anchors = (side) => [
    ...fvgList(side),
    ...(o.obs?.H1?.[side] || []).map((g) => ({ ...g, tf: "H1", kind: "OB" })),
    ...(o.obs?.M15?.[side] || []).map((g) => ({ ...g, tf: "M15", kind: "OB" })),
  ];
  const zoneDesc = (g, side) => (g.kind === "OB"
    ? `${OB_LABEL} of ${zoneFreshnessLabel(g)} ${g.tf} ${side} OB ${g.bottom}–${g.top}`
    : `${CE_LABEL} of ${zoneFreshnessLabel(g)} ${g.tf} ${side} FVG ${g.bottom}–${g.top}`)
    + (g.atLocal ? ` (${g.tf} candle ${g.atLocal})` : "");
  // Ticket validity lineage: validSince = the candle at which the setup was
  // COMPLETE on the chart (zone print / post-raid FVG / BOS confirm close) —
  // the ticket existed from that moment even if no scan was running.
  // formingSince = the earlier event it grew from (the raid, the watched
  // swing), i.e. "you could see it forming since then". Both are real candle
  // times from the data, never the scan clock.
  const vs = (t, note, forming) => ({ validSince: t ?? null, validSinceNote: note || null, formingSince: forming ?? null });
  const slZoneDesc = (g, long) => g.kind === "OB"
    ? `${buf} beyond OB ${long ? `low ${g.bottom}` : `high ${g.top}`}, min-stop ${minStop} enforced`
    : `${buf} beyond FVG ${long ? `floor ${g.bottom}` : `ceiling ${g.top}`}, min-stop ${minStop} enforced`;
  const consider = (c) => {
    if (c.entry == null || c.sl == null || c.tp1 == null) return;
    const long = c.direction === "LONG";
    // The draw on liquidity is the natural runner target when no laddered
    // pool was found beyond TP1.
    const dol = o.drawOnLiquidity;
    if (c.tp2 == null && dol && ((long && dol.side === "above") || (!long && dol.side === "below"))
      && (long ? dol.level > c.tp1 + minTpSep : dol.level < c.tp1 - minTpSep)) {
      c.tp2 = dol.level; c.tp2Label = `${dol.label} (the draw)`;
    }
    const ordered = long
      ? c.sl < c.entry && c.entry < c.tp1 && (c.tp2 == null || c.tp1 < c.tp2)
      : c.sl > c.entry && c.entry > c.tp1 && (c.tp2 == null || c.tp1 > c.tp2);
    const rr = long ? (c.tp1 - c.entry) / (c.entry - c.sl) : (c.entry - c.tp1) / (c.sl - c.entry);
    if (!ordered || !(rr >= 1.5)) return;
    // Entries farther than 0.75×daily-ATR from price are unlikely to fill
    // today — not an intraday ticket, discard.
    if (Math.abs(c.entry - price) > 0.75 * atrD) return;
    // A confirmed one-way trend day is not the day to fade — no counter tickets.
    if (countersTrendDay(c.direction)) return;
    let stars = c.aPlus ? 2 : 1; // A+ sequence setups start a star ahead
    if (kzActive) stars++;
    if (s.H4.bias === (long ? "bullish" : "bearish")) stars++;
    if (c.swept) stars++;
    if (rr >= 2) stars++;
    if (alignsMacro(c.direction)) {
      stars = Math.min(5, stars + 1);
      c.macroNote = `macro-aligned: fundamentals ${fd.direction} ${fd.score}/5`;
    } else if (opposesMacro(c.direction)) {
      stars = Math.max(1, stars - 2);
      c.macroNote = `⚠️ counter-macro: fundamentals say ${fd.direction} ${fd.score}/5 — reduced size or skip`;
    }
    // Provider-agnostic entry AREA label — the named zone the entry sits in, so it
    // maps to the user's chart regardless of small feed price differences. Market
    // entries read "at market"; limits take the POI named after the setup's " @ ".
    let entryLabel = c.entryLabel;
    if (!entryLabel) {
      if (c.entryType === "market") entryLabel = "at market";
      else {
        const at = (c.setup.split(" @ ")[1] || "").replace(/\b(bullish|bearish)\s/i, "").replace(/\s*\(price in zone NOW\)/i, "").trim();
        if (at) entryLabel = /^Discount/i.test(c.setup) ? `${at} · discount` : /^Premium/i.test(c.setup) ? `${at} · premium` : at;
      }
    }
    // "Equilibrium" alone isn't reproducible on the user's own chart — a raw
    // 50% level with no anchor. Name the two candles that set the 4H range
    // (its high and low) so the same box, and the same midpoint, can be
    // redrawn by time regardless of any price-feed offset.
    if (c.tp1Label === "equilibrium" && dr && dr.lowAtLocal && dr.highAtLocal) {
      c.tp1Label = `equilibrium — 4H range ${dr.low}–${dr.high} set ${dr.lowAtLocal}–${dr.highAtLocal}`;
    }
    cands.push({
      ...c, entryLabel, rr: Number(rr.toFixed(1)), stars,
      validSinceLocal: c.validSince ? fmtLT(c.validSince) : null,
      formingSinceLocal: c.formingSince ? fmtLT(c.formingSince) : null,
      fromPricePctAtr: Math.round((Math.abs(c.entry - price) / atrD) * 100),
      stopDist: Math.abs(c.entry - c.sl),
    });
  };

  // Setup 0 — the 2022 model (A+): liquidity raid → displacement AFTER the
  // raid (a fresh M15 FVG born later than the sweep wick) → limit back at the
  // displacement origin. The full ICT sequence, not just a swept flag.
  for (const lv of below.filter((l) => l.swept && l.sweptAt)) {
    if (!(s.M15.bias === "bullish" || s.M15.bosUp)) break;
    for (const g of o.fvgs.M15.bullish.filter((g) => g.t > lv.sweptAt && g.entry < price)) {
      const sl = Math.min(g.sl, lv.slBeyond);
      const tp1 = dr && dr.equilibrium > g.entry ? dr.equilibrium : above[0]?.level ?? null;
      const tp1Label = dr && dr.equilibrium > g.entry ? "equilibrium" : above[0]?.label;
      const t2 = tp1 != null ? nextAbove(tp1) : null;
      consider({ setup: `2022 model (${lv.label} raid → displacement) @ M15 FVG`, direction: "LONG", entryType: "limit",
        entry: g.entry, sl, tp1, tp1Label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the post-raid displacement FVG printed — the ${lv.label} raid that started the sequence hit ${fmtLT(lv.sweptAt)}`, lv.sweptAt),
        swept: true, sweepLevel: lv.level, sweepLabel: lv.label, aPlus: true,
        whyEntry: `${CE_LABEL} of the M15 bullish FVG the displacement left AFTER raiding ${lv.label} ${lv.level}${lv.atLocal ? ` (${lv.tf} candle ${lv.atLocal})` : ""} — the 2022-model origin`,
        whySL: sl === lv.slBeyond ? `beyond the raid extreme ${lv.level} − ${buf} buffer` : `beyond FVG floor ${g.bottom} (farther than the raid extreme)` });
    }
  }
  for (const lv of above.filter((l) => l.swept && l.sweptAt)) {
    if (!(s.M15.bias === "bearish" || s.M15.bosDown)) break;
    for (const g of o.fvgs.M15.bearish.filter((g) => g.t > lv.sweptAt && g.entry > price)) {
      const sl = Math.max(g.sl, lv.slBeyond);
      const tp1 = dr && dr.equilibrium < g.entry ? dr.equilibrium : below[0]?.level ?? null;
      const tp1Label = dr && dr.equilibrium < g.entry ? "equilibrium" : below[0]?.label;
      const t2 = tp1 != null ? nextBelow(tp1) : null;
      consider({ setup: `2022 model (${lv.label} raid → displacement) @ M15 FVG`, direction: "SHORT", entryType: "limit",
        entry: g.entry, sl, tp1, tp1Label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the post-raid displacement FVG printed — the ${lv.label} raid that started the sequence hit ${fmtLT(lv.sweptAt)}`, lv.sweptAt),
        swept: true, sweepLevel: lv.level, sweepLabel: lv.label, aPlus: true,
        whyEntry: `${CE_LABEL} of the M15 bearish FVG the displacement left AFTER raiding ${lv.label} ${lv.level}${lv.atLocal ? ` (${lv.tf} candle ${lv.atLocal})` : ""} — the 2022-model origin`,
        whySL: sl === lv.slBeyond ? `beyond the raid extreme ${lv.level} + ${buf} buffer` : `beyond FVG ceiling ${g.top} (farther than the raid extreme)` });
    }
  }

  // Setup 1 — discount reversal (LONG, resting limit, FVG or OB anchor)
  if (dr && dr.zone === "discount" && (s.H4.bias === "bullish" || s.H1.bias === "bullish")) {
    for (const g of anchors("bullish").filter((g) => g.entry < price)) {
      const t2 = nextAbove(dr.equilibrium);
      consider({ setup: `Discount reversal @ ${g.tf} bullish ${g.kind}`, direction: "LONG", entryType: "limit",
        entry: g.entry, sl: g.sl, tp1: dr.equilibrium, tp1Label: "equilibrium",
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the ${g.tf} ${g.kind} zone printed; lifecycle is ${zoneFreshnessLabel(g)}`),
        whyEntry: `${zoneDesc(g, "bullish")}, in 4H discount`,
        whySL: slZoneDesc(g, true) });
    }
  }
  // Setup 2 — premium rejection (SHORT, resting limit, FVG or OB anchor)
  if (dr && dr.zone === "premium" && (s.H4.bias === "bearish" || s.H1.bias === "bearish")) {
    for (const g of anchors("bearish").filter((g) => g.entry > price)) {
      const t2 = nextBelow(dr.equilibrium);
      consider({ setup: `Premium rejection @ ${g.tf} bearish ${g.kind}`, direction: "SHORT", entryType: "limit",
        entry: g.entry, sl: g.sl, tp1: dr.equilibrium, tp1Label: "equilibrium",
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the ${g.tf} ${g.kind} zone printed; lifecycle is ${zoneFreshnessLabel(g)}`),
        whyEntry: `${zoneDesc(g, "bearish")}, in 4H premium`,
        whySL: slZoneDesc(g, false) });
    }
  }
  // Setup 3 — liquidity-sweep reversal (both directions, resting limit)
  // Sweep reversals must have the H1 on their side too — an M15 flip alone
  // inside an H1 uptrend is a pullback, not a reversal (the July-2 lesson).
  const sweptAbove = above.filter((l) => l.swept);
  if (sweptAbove.length && (s.M15.bias === "bearish" || s.M15.bosDown)
    && (s.H1.bias === "bearish" || s.H1.bosDown)) {
    for (const g of o.fvgs.M15.bearish.filter((g) => g.entry > price)) {
      const lv = sweptAbove.find((l) => l.level >= g.entry) || sweptAbove[sweptAbove.length - 1];
      const sl = Math.max(g.sl, lv.slBeyond);
      const tp1 = dr && dr.equilibrium < g.entry ? dr.equilibrium : below[0]?.level ?? null;
      const tp1Label = dr && dr.equilibrium < g.entry ? "equilibrium" : below[0]?.label;
      const t2 = tp1 != null ? nextBelow(tp1) : null;
      consider({ setup: `Sweep reversal (${lv.label} swept) @ M15 FVG`, direction: "SHORT", entryType: "limit",
        entry: g.entry, sl, tp1, tp1Label,
        tp2: t2?.level ?? null, tp2Label: t2?.label, swept: true, sweepLevel: lv.level, sweepLabel: lv.label,
        ...vs(g.t, `the M15 FVG behind the entry printed${lv.sweptAt ? ` — the ${lv.label} sweep it trades off hit ${fmtLT(lv.sweptAt)}` : ""}`, lv.sweptAt || null),
        whyEntry: `${CE_LABEL} of M15 bearish FVG ${g.bottom}–${g.top}${g.atLocal ? ` (M15 candle ${g.atLocal})` : ""} left after the ${lv.label} ${lv.level}${lv.atLocal ? ` (${lv.tf} candle ${lv.atLocal})` : ""} sweep`,
        whySL: sl === lv.slBeyond ? `beyond sweep extreme ${lv.level} + ${buf} buffer` : `beyond FVG ceiling ${g.top} (farther than the sweep extreme)` });
    }
  }
  const sweptBelow = below.filter((l) => l.swept);
  if (sweptBelow.length && (s.M15.bias === "bullish" || s.M15.bosUp)
    && (s.H1.bias === "bullish" || s.H1.bosUp)) {
    for (const g of o.fvgs.M15.bullish.filter((g) => g.entry < price)) {
      const lv = sweptBelow.find((l) => l.level <= g.entry) || sweptBelow[sweptBelow.length - 1];
      const sl = Math.min(g.sl, lv.slBeyond);
      const tp1 = dr && dr.equilibrium > g.entry ? dr.equilibrium : above[0]?.level ?? null;
      const tp1Label = dr && dr.equilibrium > g.entry ? "equilibrium" : above[0]?.label;
      const t2 = tp1 != null ? nextAbove(tp1) : null;
      consider({ setup: `Sweep reversal (${lv.label} swept) @ M15 FVG`, direction: "LONG", entryType: "limit",
        entry: g.entry, sl, tp1, tp1Label,
        tp2: t2?.level ?? null, tp2Label: t2?.label, swept: true, sweepLevel: lv.level, sweepLabel: lv.label,
        ...vs(g.t, `the M15 FVG behind the entry printed${lv.sweptAt ? ` — the ${lv.label} sweep it trades off hit ${fmtLT(lv.sweptAt)}` : ""}`, lv.sweptAt || null),
        whyEntry: `${CE_LABEL} of M15 bullish FVG ${g.bottom}–${g.top}${g.atLocal ? ` (M15 candle ${g.atLocal})` : ""} left after the ${lv.label} ${lv.level}${lv.atLocal ? ` (${lv.tf} candle ${lv.atLocal})` : ""} sweep`,
        whySL: sl === lv.slBeyond ? `beyond sweep extreme ${lv.level} − ${buf} buffer` : `beyond FVG floor ${g.bottom} (farther than the sweep extreme)` });
    }
  }
  // Setup 4 — trend continuation pullback (resting limit, H1 FVG or OB anchor)
  if (s.H4.bias === "bullish" && s.H1.bias === "bullish") {
    for (const g of anchors("bullish").filter((g) => g.tf === "H1" && g.entry < price)) {
      const sl = s.H1.slIfLong != null ? Math.min(g.sl, s.H1.slIfLong) : g.sl;
      const t1 = above.find((l) => l.level > g.entry);
      const t2 = t1 ? nextAbove(t1.level) : null;
      consider({ setup: `Continuation pullback @ H1 bullish ${g.kind}`, direction: "LONG", entryType: "limit",
        entry: g.entry, sl, tp1: t1?.level ?? null, tp1Label: t1?.label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the H1 ${g.kind} pullback zone printed; lifecycle is ${zoneFreshnessLabel(g)}`),
        whyEntry: `${zoneDesc(g, "bullish")} — pullback in aligned H4+H1 uptrend`,
        whySL: sl === s.H1.slIfLong ? `below H1 swing low ${s.H1.lastSwingLow} − ${buf} buffer` : `below ${g.kind} lower edge ${g.bottom} (farther than the swing)` });
    }
  }
  if (s.H4.bias === "bearish" && s.H1.bias === "bearish") {
    for (const g of anchors("bearish").filter((g) => g.tf === "H1" && g.entry > price)) {
      const sl = s.H1.slIfShort != null ? Math.max(g.sl, s.H1.slIfShort) : g.sl;
      const t1 = below.find((l) => l.level < g.entry);
      const t2 = t1 ? nextBelow(t1.level) : null;
      consider({ setup: `Continuation pullback @ H1 bearish ${g.kind}`, direction: "SHORT", entryType: "limit",
        entry: g.entry, sl, tp1: t1?.level ?? null, tp1Label: t1?.label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the H1 ${g.kind} pullback zone printed; lifecycle is ${zoneFreshnessLabel(g)}`),
        whyEntry: `${zoneDesc(g, "bearish")} — pullback in aligned H4+H1 downtrend`,
        whySL: sl === s.H1.slIfShort ? `above H1 swing high ${s.H1.lastSwingHigh} + ${buf} buffer` : `above ${g.kind} upper edge ${g.top} (farther than the swing)` });
    }
  }
  // Setup 5 — in-gap bounce (MARKET: price is inside the FVG right now)
  if ((s.H4.bias === "bullish" || s.H1.bias === "bullish") && (!dr || dr.zone !== "premium")) {
    for (const g of fvgList("bullish").filter((g) => g.bottom <= price && price <= g.top)) {
      const poolT1 = above.find((l) => l.level > price);
      const useEq = dr && dr.equilibrium > price;
      const tp1 = useEq ? dr.equilibrium : poolT1?.level ?? null;
      const t2 = tp1 != null ? nextAbove(tp1) : null;
      consider({ setup: `In-gap bounce @ ${g.tf} bullish FVG (price in zone NOW)`, direction: "LONG", entryType: "market",
        entry: price, sl: g.sl, tp1, tp1Label: useEq ? "equilibrium" : poolT1?.label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the ${g.tf} FVG price is trading inside right now printed then`),
        whyEntry: `price ${price} is trading INSIDE ${zoneFreshnessLabel(g)} ${g.tf} bullish FVG ${g.bottom}–${g.top}${g.atLocal ? ` (${g.tf} candle ${g.atLocal})` : ""} right now — enter at market, no waiting`,
        whySL: `${buf} beyond FVG floor ${g.bottom}, min-stop ${minStop} enforced` });
    }
  }
  if ((s.H4.bias === "bearish" || s.H1.bias === "bearish") && (!dr || dr.zone !== "discount")) {
    for (const g of fvgList("bearish").filter((g) => g.bottom <= price && price <= g.top)) {
      const poolT1 = below.find((l) => l.level < price);
      const useEq = dr && dr.equilibrium < price;
      const tp1 = useEq ? dr.equilibrium : poolT1?.level ?? null;
      const t2 = tp1 != null ? nextBelow(tp1) : null;
      consider({ setup: `In-gap bounce @ ${g.tf} bearish FVG (price in zone NOW)`, direction: "SHORT", entryType: "market",
        entry: price, sl: g.sl, tp1, tp1Label: useEq ? "equilibrium" : poolT1?.label,
        tp2: t2?.level ?? null, tp2Label: t2?.label,
        ...vs(g.t, `the ${g.tf} FVG price is trading inside right now printed then`),
        whyEntry: `price ${price} is trading INSIDE ${zoneFreshnessLabel(g)} ${g.tf} bearish FVG ${g.bottom}–${g.top}${g.atLocal ? ` (${g.tf} candle ${g.atLocal})` : ""} right now — enter at market, no waiting`,
        whySL: `${buf} beyond FVG ceiling ${g.top}, min-stop ${minStop} enforced` });
    }
  }
  // Setup 6 — momentum BOS continuation (MARKET: fresh M15 displacement)
  if (s.M15.bosUp && (s.H4.bias === "bullish" || s.H1.bias === "bullish") && s.M15.lastSwingLow != null) {
    const sl = rd(Math.min(s.M15.lastSwingLow - buf, price - minStop));
    const poolT1 = above.find((l) => l.level > price);
    const t2 = poolT1 ? nextAbove(poolT1.level) : null;
    consider({ setup: "Momentum BOS continuation (M15 displacement up)", direction: "LONG", entryType: "market",
      entry: price, sl, tp1: poolT1?.level ?? null, tp1Label: poolT1?.label,
      tp2: t2?.level ?? null, tp2Label: t2?.label,
      ...vs(s.M15.bosUpAt, `the M15 close that broke the swing high confirmed the BOS — the swing it broke printed ${s.M15.lastSwingHighAtLocal || "earlier"}`, s.M15.lastSwingHighAt),
      whyEntry: `M15 closed ABOVE swing high ${s.M15.lastSwingHigh}${s.M15.lastSwingHighAtLocal ? ` (M15 candle ${s.M15.lastSwingHighAtLocal})` : ""} (BOS up) with HTF alignment — ride the displacement from ${price}`,
      whySL: `below M15 BOS-origin swing low ${s.M15.lastSwingLow} − ${buf} buffer, min-stop enforced` });
  }
  if (s.M15.bosDown && (s.H4.bias === "bearish" || s.H1.bias === "bearish") && s.M15.lastSwingHigh != null) {
    const sl = rd(Math.max(s.M15.lastSwingHigh + buf, price + minStop));
    const poolT1 = below.find((l) => l.level < price);
    const t2 = poolT1 ? nextBelow(poolT1.level) : null;
    consider({ setup: "Momentum BOS continuation (M15 displacement down)", direction: "SHORT", entryType: "market",
      entry: price, sl, tp1: poolT1?.level ?? null, tp1Label: poolT1?.label,
      tp2: t2?.level ?? null, tp2Label: t2?.label,
      ...vs(s.M15.bosDownAt, `the M15 close that broke the swing low confirmed the BOS — the swing it broke printed ${s.M15.lastSwingLowAtLocal || "earlier"}`, s.M15.lastSwingLowAt),
      whyEntry: `M15 closed BELOW swing low ${s.M15.lastSwingLow}${s.M15.lastSwingLowAtLocal ? ` (M15 candle ${s.M15.lastSwingLowAtLocal})` : ""} (BOS down) with HTF alignment — ride the displacement from ${price}`,
      whySL: `above M15 BOS-origin swing high ${s.M15.lastSwingHigh} + ${buf} buffer, min-stop enforced` });
  }

  cands.sort((a, b) => b.stars - a.stars || a.fromPricePctAtr - b.fromPricePctAtr || a.stopDist - b.stopDist || b.rr - a.rr);
  // Different setup paths can anchor on the same FVG/OB — same direction with
  // entry AND SL within 0.05×ATR is one trade idea, keep only the best-ranked.
  const dupTol = 0.05 * atrD;
  const deduped = [];
  for (const c of cands) {
    if (deduped.some((k) => k.direction === c.direction
      && Math.abs(k.entry - c.entry) <= dupTol && Math.abs(k.sl - c.sl) <= dupTol)) continue;
    deduped.push(c);
  }
  deduped.forEach((c) => delete c.stopDist);
  return deduped;
}

// FVG entry depth, measured from the TOUCH edge of the gap (env-tunable, like
// ICT_ASSUME_OPEN). 0 = enter the moment price touches the gap (near edge),
// 50 = classic CE / midpoint (default), 100 = full fill (far edge). The dashboard
// threads this in per scan via ICT_CE_PCT so a saved setting changes where resting
// limits (and therefore tracked fills) sit.
const CE_PCT = (() => { const v = Number(process.env.ICT_CE_PCT); return Number.isFinite(v) ? Math.max(0, Math.min(100, Math.round(v))) : 50; })();
const CE_LABEL = CE_PCT === 50 ? "CE (midpoint)" : CE_PCT === 0 ? "near edge (immediate touch)" : CE_PCT === 100 ? "far edge (full fill)" : `${CE_PCT}% gap depth`;
// Order-block entry depth (ICT_OB_PCT), independent of the FVG CE% above. An OB is
// the last candle before the move, so the base default is an IMMEDIATE TOUCH of its
// proximal edge: 0 = near edge (immediate touch, default), 50 = the block's 50% mid,
// 100 = far edge (full fill). Threaded in per scan via ICT_OB_PCT.
const OB_PCT = (() => { const v = Number(process.env.ICT_OB_PCT); return Number.isFinite(v) ? Math.max(0, Math.min(100, Math.round(v))) : 0; })();
const OB_LABEL = OB_PCT === 0 ? "near edge (immediate touch)" : OB_PCT === 50 ? "50% (mid)" : OB_PCT === 100 ? "far edge (full fill)" : `${OB_PCT}% OB depth`;

// `calendar` is the shared news calendar in scan mode (fetched once); when
// undefined (single-asset run) it is fetched here. null = fetch failed, skip.
async function analyze(key, calendar, opts = {}) {
  const canon = normalizeAsset(key);
  // Any 6-letter FX pair resolves to Yahoo's <PAIR>=X automatically, so all
  // major crosses work without being listed individually. Exotics still resolve
  // but are intentionally kept out of the watchlist / selector.
  const symbol = symbolForAsset(canon);
  if (!symbol) throw new Error(`unsupported asset: ${key}`);
  const calP = calendar !== undefined ? Promise.resolve(calendar) : fetchCalendar();
  const [d1, h1raw, m15] = await Promise.all([
    fetchCandles(symbol, "1d", "1y"),
    fetchCandles(symbol, "1h", "3mo"),
    fetchCandles(symbol, "15m", "5d"),
  ]);
  const cal = await calP;
  const dailyRaw = d1.candles;
  const daily = closedOnly(dailyRaw, 86400);
  // Structure and zone creation read CLOSED candles only; zone lifecycle also
  // consumes later raw/forming candles because a live wick can mitigate a zone.
  // liquidity extremes and data-age use the raw series (a forming candle's
  // high/low are real prints already).
  const h1 = closedOnly(h1raw.candles, 3600);
  const m15c = closedOnly(m15.candles, 900);
  const h4 = closedOnly(resample(h1, 4), 14400);
  const price = m15.livePrice;
  const atrD = atr(daily), atrH1 = atr(h1);
  const todayUtc = new Date().toISOString().slice(0, 10);
  const todayCandle = dailyRaw[dailyRaw.length - 1];
  const atrUsedPct = Math.round(((todayCandle.h - todayCandle.l) / atrD) * 100);
  // Trend-day regime: a full-ATR day closing hard at one extreme is one-way
  // flow (NFP-style). Fading it is how counter-trend tickets die — pickSetup
  // drops counter-direction candidates entirely on these days.
  const dayRange = todayCandle.h - todayCandle.l;
  const closePos = dayRange > 0 ? (todayCandle.c - todayCandle.l) / dayRange : 0.5;
  const trendDay = atrUsedPct >= 90 && (closePos >= 0.75 || closePos <= 0.25);
  const regime = {
    trendDay,
    direction: trendDay ? (closePos >= 0.75 ? "up" : "down") : null,
    closePosPct: Math.round(closePos * 100),
  };
  const lastTs = m15.candles[m15.candles.length - 1].t;
  const dataAgeMin = Math.round((Date.now() / 1000 - lastTs) / 60);
  const clock = sessionClock();

  const r = (x) => round(x, price);
  const rr = (obj, keys) => { for (const k of keys) if (obj && obj[k] != null) obj[k] = r(obj[k]); return obj; };

  const dr = dealingRange(h4, price, atrD);

  // Stop-loss engineering: SL never sits ON the level (buffer) and never
  // closer than minStop to entry — kills the 1-pip-stop / RR-28 tickets.
  const buffer = 0.1 * atrD;
  const minStop = 0.2 * atrD;

  // Pre-compute the order ticket per FVG so the model copies, never calculates.
  // Freshness: H1 anchors ≤14 calendar days (~10 trading), M15 ≤3 days.
  const fvgAll = {
    H1: findFvgs(h1, h1raw.candles, atrD, price, 0.1 * atrD, 14 * 86400, fmtLT),
    M15: findFvgs(m15c, m15.candles, atrD, price, 0.05 * atrD, 3 * 86400, fmtLT),
  };
  for (const tf of Object.values(fvgAll)) {
    for (const g of tf.bullish) {
      // Price falls INTO a bullish gap from above → the touch edge is the top.
      g.entry = g.top - (CE_PCT / 100) * (g.top - g.bottom);
      g.sl = Math.min(g.bottom - buffer, g.entry - minStop);
      if (dr && dr.equilibrium > g.entry) g.rrToEq = Number(((dr.equilibrium - g.entry) / (g.entry - g.sl)).toFixed(1));
    }
    for (const g of tf.bearish) {
      // Price rises INTO a bearish gap from below → the touch edge is the bottom.
      g.entry = g.bottom + (CE_PCT / 100) * (g.top - g.bottom);
      g.sl = Math.max(g.top + buffer, g.entry + minStop);
      if (dr && dr.equilibrium < g.entry) g.rrToEq = Number(((g.entry - dr.equilibrium) / (g.sl - g.entry)).toFixed(1));
    }
  }

  // Order blocks get the same ticket treatment (entry at the configured OB depth,
  // engineered SL). g.mid stays available for alerts / proximity checks.
  const obAll = {
    H1: findOrderBlocks(h1, h1raw.candles, atrD, price, 0.05 * atrD, 14 * 86400, fmtLT),
    M15: findOrderBlocks(m15c, m15.candles, atrD, price, 0.03 * atrD, 3 * 86400, fmtLT),
  };
  for (const tf of Object.values(obAll)) {
    for (const g of tf.bullish) {
      // Price falls INTO a bullish (demand) OB from above → proximal edge is the top.
      g.entry = g.top - (OB_PCT / 100) * (g.top - g.bottom);
      g.sl = Math.min(g.bottom - buffer, g.entry - minStop);
    }
    for (const g of tf.bearish) {
      // Price rises INTO a bearish (supply) OB from below → proximal edge is the bottom.
      g.entry = g.bottom + (OB_PCT / 100) * (g.top - g.bottom);
      g.sl = Math.max(g.top + buffer, g.entry + minStop);
    }
  }

  const sH1 = structure(h1);
  if (sH1.lastSwingLow != null) sH1.slIfLong = sH1.lastSwingLow - buffer;
  if (sH1.lastSwingHigh != null) sH1.slIfShort = sH1.lastSwingHigh + buffer;

  const out = {
    meta: {
      asset: key.toUpperCase(), yahooSymbol: symbol,
      dataSource: "yahoo",
      isFutures: FUTURES_SYMBOLS.has(symbol),
      priceNote: FUTURES_SYMBOLS.has(symbol)
        ? "futures quote — sits at a small constant offset vs spot; on TradingView, align each level by the reference it names (FVG, OB, EQH/EQL or POI), not the raw price"
        : "spot quote — matches typical broker/spot prices closely",
      price: r(price), dateUtc: todayUtc,
      clock: clock.local, tz: clock.tz, killzone: clock.killzone, session: clock.session,
      marketOpen: clock.marketOpen,
      // Override for the reasoning-vs-deterministic debate default. Unset → the
      // model self-identifies; set TRADING_MODEL_CLASS=reasoning|deterministic to force.
      modeOverride: ["reasoning", "deterministic"].includes((process.env.TRADING_MODEL_CLASS || "").toLowerCase())
        ? process.env.TRADING_MODEL_CLASS.toLowerCase() : null,
      reopenLocal: clock.reopenLocal, reopenInMin: clock.reopenInMin,
      closeLocal: clock.closeLocal, closeInMin: clock.closeInMin,
      // Market-open is session-based (FX week: Sun 17:00 ET → Fri 17:00 ET), NOT
      // a data-age guess — the old dataAge>120 test misfired right at the Sunday
      // reopen while Yahoo was still catching up. Stale data on a weekday is
      // surfaced via dataAgeMin/staleData, not by hiding the card.
      // ICT_ASSUME_OPEN=1 forces open for weekend testing.
      dataAgeMin, staleData: dataAgeMin > 120,
      marketLikelyClosed: process.env.ICT_ASSUME_OPEN ? false : !clock.marketOpen,
      atrDaily: r(atrD), atrH1: r(atrH1), atrUsedTodayPct: atrUsedPct,
      slBuffer: r(buffer), minStopDistance: r(minStop),
      newsRisk: newsRisk(cal, symbol),
      regime,
      fundamentals: FUNDAMENTALS?.[normalizeAsset(key)] ?? null,
      lessons: LESSONS,
    },
    structure: {
      D: rr(structure(daily), ["lastSwingHigh", "lastSwingLow", "chochLevel"]),
      H4: rr(structure(h4), ["lastSwingHigh", "lastSwingLow", "chochLevel"]),
      H1: rr(sH1, ["lastSwingHigh", "lastSwingLow", "slIfLong", "slIfShort", "chochLevel"]),
      M15: rr(structure(m15c), ["lastSwingHigh", "lastSwingLow", "chochLevel"]),
    },
    dealingRange4H: dr ? rr(dr, ["high", "low", "equilibrium"]) : null,
    liquidity: (() => {
      const lq = liquidity(daily, m15.candles, h1, price, atrD);
      lq.above.forEach((l) => { l.slBeyond = r(l.level + buffer); l.level = r(l.level); });
      lq.below.forEach((l) => { l.slBeyond = r(l.level - buffer); l.level = r(l.level); });
      return lq;
    })(),
    fvgs: (() => {
      for (const tf of Object.values(fvgAll)) for (const side of Object.values(tf)) side.forEach((g) => rr(g, ["top", "bottom", "ce", "entry", "sl"]));
      return fvgAll;
    })(),
    obs: (() => {
      for (const tf of Object.values(obAll)) for (const side of Object.values(tf)) side.forEach((g) => rr(g, ["top", "bottom", "mid", "entry", "sl"]));
      return obAll;
    })(),
  };
  // Rate each timeframe's structure for continuation probability.
  for (const [tfName, higherName] of [["M15", "H1"], ["H1", "H4"], ["H4", "D"], ["D", null]]) {
    scoreStructure(tfName, out.structure[tfName], higherName ? out.structure[higherName] : null, higherName, out.dealingRange4H, out.meta.atrUsedTodayPct);
  }
  out.structureRead = readStructureBoard(out.structure);
  out.drawOnLiquidity = pickDOL(out.liquidity, out.structure, price, atrD);
  buildSlRails(out, price, buffer, r);
  out.wyckoff = wyckoff(h1, out.structure, out.dealingRange4H, out.liquidity, price, atrD, r);

  // Trading-Universe TDE owns ticket discovery. The surrounding structure,
  // liquidity, fundamentals, magnet and Wyckoff reads remain presentation
  // context and do not create or veto orders.
  const engineData = { m15: m15.candles, h1: h1raw.candles, d1: dailyRaw };
  const engineRuns = out.meta.marketLikelyClosed ? [] : ["M15", "H1"].map((timeframe) =>
    buildTicketDiscoveryEngine(out.meta.asset, engineData, Date.now() / 1000, {
      timeframe,
      currentPrice: price,
    }));
  const actionableTickets = selectActionableTickets(
    engineRuns.flatMap((engine) => engine.tickets),
    { price },
  );
  const discovered = actionableTickets.map((ticket) => {
    const candidate = adaptDiscoveredTicket(ticket, { price, atrDaily: atrD, round: r });
    candidate.validSinceLocal = candidate.validSince ? fmtLT(candidate.validSince) : null;
    candidate.formingSinceLocal = candidate.formingSince ? fmtLT(candidate.formingSince) : null;
    candidate.debate = debateTicket(out, candidate);
    return candidate;
  });
  out.meta.ticketDiscovery = {
    engine: "Trading-Universe TDE",
    timeframes: engineRuns.map((engine) => engine.timeframe),
    actionableTickets: discovered.length,
  };
  out.candidate = discovered[0] ?? null;
  if (discovered.length > 1) out.altCandidates = discovered.slice(1, 3);

  // If the chosen ticket is a confirmed sweep-reversal, that raid remains the
  // Wyckoff spring/upthrust label. Display only: StageV qualification is final.
  if (out.candidate && out.candidate.swept && out.candidate.sweepLabel && (!out.wyckoff || out.wyckoff.bias === "neutral")) {
    const long = out.candidate.direction === "LONG";
    const ev = long ? "spring" : "upthrust", sch = long ? "accumulation" : "distribution";
    out.wyckoff = {
      schematic: sch, phase: `Phase C — ${ev} (the ticket's raid)`, event: ev, bias: long ? "bullish" : "bearish",
      range: out.wyckoff?.range ?? null, events: out.wyckoff?.events ?? [], effortResult: out.wyckoff?.effortResult ?? null, fromTicket: true,
      location: `the entry sits on a confirmed ${long ? "sell-side" : "buy-side"} raid of ${out.candidate.sweepLabel} that reversed — Wyckoff Phase C ${ev}, the ${long ? "markup" : "markdown"} trigger.`,
      nextTell: long ? `hold above the raid low; an H1 BOS up = Phase D markup confirmation.` : `hold below the raid high; an H1 BOS down = Phase D markdown confirmation.`,
      suggestedAction: long
        ? `this ticket IS the Phase C long: enter at the ${out.candidate.sweepLabel} reclaim (the FVG/OB it left), trigger = H1 BOS up, invalid on an H1 close back below the raid low.`
        : `this ticket IS the Phase C short: enter at the ${out.candidate.sweepLabel} retest (the FVG/OB it left), trigger = H1 BOS down, invalid on an H1 close back above the raid high.`,
      note: `the ${out.candidate.sweepLabel} raid behind this entry is a Wyckoff ${ev} — ${sch}, bias ${long ? "UP" : "DOWN"}: the sweep-and-reverse that starts the ${long ? "markup" : "markdown"}.`,
    };
  }

  // Keep an immediately actionable alternative visible when the leading plan is
  // a distant resting order. This is display only, not another qualification.
  if (out.candidate && out.candidate.entryType !== "market" && out.candidate.fromPricePctAtr > 25) {
    const now = discovered.find((candidate) => candidate !== out.candidate
      && (candidate.entryType === "market" || candidate.fromPricePctAtr <= 10));
    if (now) out.candidateNow = now;
  }

  const generatedAt = Date.now();
  const generatedAtLocal = out.meta.clock;
  if (out.candidate) Object.assign(out.candidate, { generatedAt, generatedAtLocal });
  if (out.candidateNow) Object.assign(out.candidateNow, { generatedAt, generatedAtLocal });
  if (!out.candidate) {
    out.candidateNote = out.meta.marketLikelyClosed
      ? "market likely closed — no card"
      : "no current unresolved order passes Trading-Universe TDE qualification — stand down";
  }  // Lightweight closes-only price trails for the dashboard grid's sparklines —
  // unconditional (unlike the full ohlc block below): ~170 numbers vs. ~450+ rows,
  // cheap enough that every card can have one, not just single-asset runs.
  out.spark = m15c.slice(-20).map((c) => r(c.c)); // kept for back-compat; superseded by out.sparks
  // Per-timeframe trails — HALVED windows (user call: the longer trails read
  // as an over-stretched flat line at ~220px). 15–24 points ≈ 9–15px per
  // segment, so the shape actually shows. Note: daily is the raw series
  // (today's forming candle included) — real prints, fine for a trail.
  out.sparks = {
    m15: m15c.slice(-24).map((c) => r(c.c)), // 24 × 15m ≈ 6h
    h1: h1.slice(-24).map((c) => r(c.c)),    // 24 × 1h  ≈ 1 trading day
    h4: h4.slice(-21).map((c) => r(c.c)),    // 21 × 4h  ≈ 3.5 days
    d: dailyRaw.slice(-15).map((c) => r(c.c)),  // 15 × 1d  ≈ 3 weeks
  };
  // Parallel candle-open timestamps (epoch seconds) for the sparkline hover
  // tooltip — real candle times, so the dashboard never guesses across
  // weekends/session gaps.
  out.sparkTs = {
    m15: m15c.slice(-24).map((c) => c.t),
    h1: h1.slice(-24).map((c) => c.t),
    h4: h4.slice(-21).map((c) => c.t),
    d: dailyRaw.slice(-15).map((c) => c.t),
  };
  // Classic indicator pack per timeframe — surfaces on the dashboard's
  // deep-detail Raw tab ONLY (deliberately kept OFF the main cards/board
  // until explicitly promoted). Context only: the setup engine, debate and
  // ticket math never read these.
  const rz = (x) => (x == null || !isFinite(x) ? null : r(x));
  const n1 = (x) => (x == null || !isFinite(x) ? null : Number(x.toFixed(1)));
  const indiTf = (candles) => {
    const closes = candles.map((c) => c.c);
    const macd = macdLast(closes), bb = bollingerLast(closes), sto = stochLast(candles);
    return {
      rsi14: n1(rsiLast(closes)),
      ema20: rz(emaLast(closes, 20)), ema50: rz(emaLast(closes, 50)), ema200: rz(emaLast(closes, 200)),
      macd: macd && { line: rz(macd.line), signal: rz(macd.signal), hist: rz(macd.hist) },
      bb: bb && { upper: rz(bb.upper), mid: rz(bb.mid), lower: rz(bb.lower), pctB: n1(bb.pctB), widthPct: n1(bb.widthPct) },
      stoch: sto && { k: n1(sto.k), d: n1(sto.d) },
      atr14: rz(candles.length > 14 ? atr(candles) : null),
    };
  };
  out.indicators = {
    note: "standard closes-only pack (RSI14 · EMA20/50/200 · MACD 12-26-9 · Bollinger 20,2 · Stoch 14-3-3 · ATR14) — context only, the ICT engine does not trade off these",
    M15: indiTf(m15c), H1: indiTf(h1), H4: indiTf(h4), D: indiTf(daily),
  };
  // Raw OHLC window for the reasoning re-check — single-asset runs only (opts.ohlc);
  // the scan uses summarize() and the universe dump must stay lean, so neither sets it.
  // Array rows keep it compact; sized to actually support the full tape checklist:
  // M15 ~16h (all sessions), H1 ~3 days, H4 ~1 week, D ~1 month. The last m15/h1 row
  // may be a still-forming candle (its high/low are real prints, its close provisional).
  if (opts.ohlc) {
    const rows = (arr, n) => arr.slice(-n).map((c) => [c.t, r(c.o), r(c.h), r(c.l), r(c.c), c.v ?? null]);
    out.ohlc = {
      tz: out.meta.tz,
      asOf: new Date().toISOString(),
      note: "recent candles for tape verification; last m15/h1 row may be forming. OHLC rounded to the instrument tick; v is null on FX spot.",
      cols: ["t", "o", "h", "l", "c", "v"],
      m15: rows(m15.candles, 64),
      h1: rows(h1raw.candles, 72),
      h4: rows(h4, 30),
      d: rows(dailyRaw, 20),
    };
  }
  return out;
}

// Wyckoff read — the same mechanics ICT tracks, in Wyckoff's language, reusing
// what the engine already computes. A bounded trading range = accumulation /
// distribution; a swept sell-side pool at the range low that reclaims = a SPRING
// (Phase C, bullish); a swept buy-side pool at the range high that fails = an
// UPTHRUST (bearish); a BOS out of the range = a Sign of Strength / Weakness;
// a clean trend = markup / markdown (Phase E). Volume (where the feed gives it —
// indices/metals) grades effort vs result. Advisory confluence only; never a
// source of prices.
function wyckoff(h1, struct, dr, liq, price, atrD, r) {
  if (!h1 || h1.length < 30) return null;
  const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  const fmtLT = (t) => t ? new Intl.DateTimeFormat("en-GB", { timeZone: localTz, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(t * 1000)).replace(",", "") : null;
  const sw = swings(h1, 2);
  const hi = sw.highs.slice(-8), lo = sw.lows.slice(-8);
  if (hi.length < 2 || lo.length < 2) return null;
  const resistance = Math.max(...hi.map((s) => s.p));
  const support = Math.min(...lo.map((s) => s.p));
  const width = resistance - support;
  if (width <= 0) return null;
  const posPct = Math.round(((price - support) / width) * 100);
  const widthAtr = width / atrD;
  const h1b = struct.H1?.bias, h4b = struct.H4?.bias;
  const ranging = widthAtr < 1.4 && posPct >= -12 && posPct <= 112 && !(struct.H1?.bosUp || struct.H1?.bosDown);
  const now = Date.now() / 1000;
  const fresh = (t) => t && now - t < 36 * 3600;
  // A swept sell-side pool at the range low that reclaimed = spring; a swept
  // buy-side pool at the range high that failed = upthrust. Gate each by
  // structure so a swept high inside a MARKUP reads as strength (SOS), not a
  // failed upthrust — Wyckoff must agree with trend, not fight it.
  const upTrend = struct.H1?.bias === "bullish" || struct.H1?.bosUp;
  const downTrend = struct.H1?.bias === "bearish" || struct.H1?.bosDown;
  const springRaw = (liq.below || []).find((l) => l.swept && fresh(l.sweptAt) && Math.abs(l.level - support) <= 0.5 * atrD);
  const upthrustRaw = (liq.above || []).find((l) => l.swept && fresh(l.sweptAt) && Math.abs(l.level - resistance) <= 0.5 * atrD);
  // A spring is only a LIVE Phase-C trigger while price is still low in the range
  // (it just reclaimed the low); once price has rallied to the upper half the
  // spring has matured into markup, so it stays in the event map as history but is
  // no longer the active read. Mirror for the upthrust at the top.
  const spring = springRaw && !downTrend && posPct <= 55 ? springRaw : null;
  const upthrust = upthrustRaw && !upTrend && posPct >= 45 ? upthrustRaw : null;
  const vols = h1.slice(-60).map((b) => b.v).filter((v) => v != null && v > 0);
  const avgV = vols.length >= 20 ? vols.reduce((a, b) => a + b, 0) / vols.length : null;
  const nearBar = (t) => { if (!t) return null; let best = null; for (const c of h1) if (best === null || Math.abs(c.t - t) < Math.abs(best.t - t)) best = c; return best; };
  const eventBarVol = (t) => nearBar(t)?.v ?? null;
  const volTag = (t) => { if (!avgV || !t) return null; const b = nearBar(t); if (!b || b.v == null) return null; const rel = b.v / avgV; return rel >= 1.6 ? "climactic vol" : rel >= 1.1 ? "strong vol" : "light vol"; };

  // A spring/upthrust is read FIRST — it is the same event as an ICT sweep-and-
  // reverse, and stays meaningful even once price has displaced out of the range.
  let schematic = null, phase = null, event = null, bias = "neutral";
  if (spring && !upthrust) {
    schematic = "accumulation"; event = "spring"; bias = "bullish";
    phase = "Phase C — spring (the test)"; // price still low in the range = live trigger; markup handoff is the markup branch
  } else if (upthrust && !spring) {
    schematic = "distribution"; event = "upthrust"; bias = "bearish";
    phase = "Phase C — upthrust (the test)"; // price still high in the range = live trigger; markdown handoff is the markdown branch
  } else if (ranging) {
    if (posPct <= 38) { schematic = "accumulation"; phase = "Phase B — building cause (lower range)"; }
    else if (posPct >= 62) { schematic = "distribution"; phase = "Phase B — building cause (upper range)"; }
    else { schematic = "range"; phase = "Phase B — mid-range (low conviction)"; }
  } else if (h1b === "bullish" && h4b !== "bearish") {
    // Phase E (free markup) only once price has BROKEN OUT of the top; while it is
    // still inside the band a bullish bias is demand in control — Phase D.
    schematic = "markup"; bias = "bullish"; if (struct.H1?.bosUp) event = "SOS";
    phase = (struct.H1?.bosUp || posPct >= 85)
      ? (event === "SOS" ? "Phase D->E — SOS, markup out of the range" : "Phase E — markup")
      : "Phase D — demand in control, marking up inside the range";
  } else if (h1b === "bearish" && h4b !== "bullish") {
    schematic = "markdown"; bias = "bearish"; if (struct.H1?.bosDown) event = "SOW";
    phase = (struct.H1?.bosDown || posPct <= 15)
      ? (event === "SOW" ? "Phase D->E — SOW, markdown out of the range" : "Phase E — markdown")
      : "Phase D — supply in control, marking down inside the range";
  } else { schematic = "transition"; phase = "transition — no clean Wyckoff structure"; bias = "neutral"; }

  // Event map — the canonical Wyckoff landmarks, read off the swing sequence in
  // time order, so the read pinpoints WHICH stage the asset is in, not just AMD.
  // SC/BC = the climax that set the band; AR = the automatic move that set the
  // opposite edge; ST = the (higher/lower) retest; Spring/Upthrust = the Phase-C
  // test; SOS/SOW = the Phase-D break out of the range.
  const climaxLow = lo.reduce((m, s) => (s.p < m.p ? s : m), lo[0]);
  const climaxHigh = hi.reduce((m, s) => (s.p > m.p ? s : m), hi[0]);
  const highsAfter = (t) => sw.highs.filter((s) => s.t > t);
  const lowsAfter = (t) => sw.lows.filter((s) => s.t > t);
  const lastHigh = sw.highs[sw.highs.length - 1], lastLow = sw.lows[sw.lows.length - 1];
  const events = [];
  const add = (name, p, t, desc) => { if (p == null || !t) return; events.push({ name, price: r(p), at: fmtLT(t), _t: t, desc }); };
  const accumSide = schematic === "accumulation" || (schematic === "markup" && !ranging);
  const distSide = schematic === "distribution" || (schematic === "markdown" && !ranging);
  if (accumSide) {
    add("SC", climaxLow.p, climaxLow.t, `selling climax — set support${volTag(climaxLow.t) ? ", " + volTag(climaxLow.t) : ""}`);
    const ar = highsAfter(climaxLow.t)[0];
    if (ar) add("AR", ar.p, ar.t, "automatic rally — set the range top");
    if (ar) { const sts = lowsAfter(ar.t).filter((s) => s.p >= climaxLow.p - 0.1 * atrD); const st = sts[sts.length - 1]; if (st && st.t !== climaxLow.t) add("ST", st.p, st.t, "secondary test — higher low, supply drying up"); }
    if (springRaw) add("Spring", springRaw.level, springRaw.sweptAt, `swept ${r(springRaw.level)} & reclaimed${volTag(springRaw.sweptAt) ? ", " + volTag(springRaw.sweptAt) : ""}`);
    if (struct.H1?.bosUp && lastHigh) add("SOS", resistance, lastHigh.t, "sign of strength — closed above the range top");
  } else if (distSide) {
    add("BC", climaxHigh.p, climaxHigh.t, `buying climax — set resistance${volTag(climaxHigh.t) ? ", " + volTag(climaxHigh.t) : ""}`);
    const ar = lowsAfter(climaxHigh.t)[0];
    if (ar) add("AR", ar.p, ar.t, "automatic reaction — set the range low");
    if (ar) { const sts = highsAfter(ar.t).filter((s) => s.p <= climaxHigh.p + 0.1 * atrD); const st = sts[sts.length - 1]; if (st && st.t !== climaxHigh.t) add("ST", st.p, st.t, "secondary test — lower high, demand drying up"); }
    if (upthrustRaw) add("Upthrust", upthrustRaw.level, upthrustRaw.sweptAt, `swept ${r(upthrustRaw.level)} & failed${volTag(upthrustRaw.sweptAt) ? ", " + volTag(upthrustRaw.sweptAt) : ""}`);
    if (struct.H1?.bosDown && lastLow) add("SOW", support, lastLow.t, "sign of weakness — closed below the range low");
  }
  events.sort((a, b) => a._t - b._t);
  const eventMap = events.map(({ _t, ...e }) => e);

  // Where price sits right now, and what confirms the next phase — the pinpoint.
  const rngS = `${r(support)}–${r(resistance)}`;
  let location, nextTell;
  if (event === "spring") {
    location = struct.H1?.bosUp
      ? `spring confirmed and price broke the range top — Phase D, markup starting; buy the LPS pullback into old resistance ${r(resistance)}.`
      : `in the spring reclaim — price swept ${r(springRaw.level)} and is back inside at ${posPct}% of the range (Phase C); the long trigger is live.`;
    nextTell = struct.H1?.bosUp ? `a higher-low holding above ${r(resistance)} = LPS, the with-trend add.` : `an H1 close above the range top ${r(resistance)} = SOS -> Phase D markup.`;
  } else if (event === "upthrust") {
    location = struct.H1?.bosDown
      ? `upthrust confirmed and price broke the range low — Phase D, markdown starting; sell the LPSY pullback into old support ${r(support)}.`
      : `in the upthrust rejection — price swept ${r(upthrustRaw.level)} and failed back inside at ${posPct}% of the range (Phase C); the short trigger is live.`;
    nextTell = struct.H1?.bosDown ? `a lower-high staying under ${r(support)} = LPSY, the with-trend add.` : `an H1 close below the range low ${r(support)} = SOW -> Phase D markdown.`;
  } else if (schematic === "markup") {
    location = (struct.H1?.bosUp || posPct >= 85)
      ? `markup out of the ${rngS} range — trending up, price at ${posPct}%; buy pullbacks into demand, do not chase.`
      : `demand in control inside the ${rngS} range, price at ${posPct}% and marking up toward the top ${r(resistance)}; buy pullbacks, not the highs.`;
    nextTell = `an H1 close above ${r(resistance)} = SOS/breakout (Phase E); loss of the last higher-low warns of an upthrust/distribution.`;
  } else if (schematic === "markdown") {
    location = (struct.H1?.bosDown || posPct <= 15)
      ? `markdown out of the ${rngS} range — trending down, price at ${posPct}%; sell rallies into supply, do not chase.`
      : `supply in control inside the ${rngS} range, price at ${posPct}% and rolling down from the top toward ${r(support)}; sell rallies, not the lows.`;
    nextTell = `an H1 close below ${r(support)} = SOW/breakdown (Phase E); reclaim of the last lower-high warns of a spring/accumulation.`;
  } else if (schematic === "accumulation") {
    location = `Phase B accumulation — basing at ${posPct}% of the ${rngS} range, low in the band after the AR; cause still building.`;
    nextTell = `a dip under support ${r(support)} that reclaims = spring (Phase C long trigger); an H1 close above ${r(resistance)} = SOS.`;
  } else if (schematic === "distribution") {
    location = `Phase B distribution — topping at ${posPct}% of the ${rngS} range, high in the band after the AR; cause still building.`;
    nextTell = `a poke above resistance ${r(resistance)} that fails = upthrust (Phase C short trigger); an H1 close below ${r(support)} = SOW.`;
  } else if (schematic === "range") {
    location = `mid-range (${posPct}%) of ${rngS} — Phase B equilibrium, the lowest-conviction zone; wait for the edges.`;
    nextTell = `a test of ${r(support)} (spring) or ${r(resistance)} (upthrust) shows the Composite Man's hand.`;
  } else {
    location = `no clean Wyckoff range on H1 — price is between structures.`;
    nextTell = `wait for a range to form or a decisive trend leg to print.`;
  }

  let effortResult = null;
  if (avgV && (spring || upthrust)) {
    const ev = spring || upthrust; const bv = eventBarVol(ev.sweptAt);
    if (bv != null) effortResult = bv >= 1.6 * avgV
      ? `high-volume ${event || "test"} — strong absorption, effort backs the turn`
      : `muted volume on the ${event || "test"} — wants confirmation`;
  }
  const rng = `${r(support)}–${r(resistance)}`;
  let note;
  if (event === "spring") note = `H1 spring — swept the range low ${r(support)} and reclaimed (${phase}); accumulation, bias UP toward the range high ${r(resistance)}.`;
  else if (event === "upthrust") note = `H1 upthrust — swept the range high ${r(resistance)} and failed (${phase}); distribution, bias DOWN toward the range low ${r(support)}.`;
  else if (schematic === "markup") note = `H1 markup (Phase E)${event === "SOS" ? " — SOS: closed above the range, a sign of strength" : ""}; trend leg in progress, favour buying pullbacks.`;
  else if (schematic === "markdown") note = `H1 markdown (Phase E)${event === "SOW" ? " — SOW: closed below the range, a sign of weakness" : ""}; trend leg in progress, favour selling rallies.`;
  else if (schematic === "accumulation") note = `H1 accumulation range ${rng}, price low in the band (${posPct}%) — Phase B building cause; watch for a spring.`;
  else if (schematic === "distribution") note = `H1 distribution range ${rng}, price high in the band (${posPct}%) — Phase B building cause; watch for an upthrust.`;
  else if (schematic === "range") note = `H1 balanced range ${rng} (${posPct}%) — Phase B; wait for a spring/upthrust or a decisive break.`;
  else note = `no clean Wyckoff structure on H1 right now.`;
  if (effortResult) note += ` ${effortResult.charAt(0).toUpperCase()}${effortResult.slice(1)}.`;

  // Concrete, deterministic entry action off the schematic — the "so what do I
  // do" the next-tell implies, spelled out: direction, trigger, invalidation.
  const suggestedAction = wyckoffAction(schematic, event, r(support), r(resistance));

  return { schematic, phase, event, bias, range: { support: r(support), resistance: r(resistance), posPct, widthAtr: +widthAtr.toFixed(2) }, events: eventMap, location, nextTell, suggestedAction, note };
}

// Turn a Wyckoff read into a copy-ready action line: what to do, what confirms
// it, what voids it. Null for schematics with no actionable edge yet.
function wyckoffAction(schematic, event, support, resistance) {
  if (event === "spring") return `long the reclaim/LPS back toward ${resistance}; trigger = H1 BOS up (Phase D markup); invalid on an H1 close back below the spring low ${support}.`;
  if (event === "upthrust") return `short the retest/LPSY back toward ${support}; trigger = H1 BOS down (Phase D markdown); invalid on an H1 close back above the upthrust high ${resistance}.`;
  if (schematic === "markup") return `buy pullbacks into demand toward ${support}; do not chase the highs; invalid on loss of the last higher-low.`;
  if (schematic === "markdown") return `sell rallies into supply toward ${resistance}; do not chase the lows; invalid on reclaim of the last lower-high.`;
  if (schematic === "accumulation") return `wait for a spring at support ${support} to reclaim, then go long; no trade mid-range.`;
  if (schematic === "distribution") return `wait for an upthrust at resistance ${resistance} to fail, then go short; no trade mid-range.`;
  return null; // range / transition — no edge yet
}

// Up to 3 stop-loss rails per side, nearest-first — the swing (primary), then
// the demand/supply zones and dealing-range edge, plus a MEMORY of already-swept
// pools that can still act as inversion S/R (an old iFVG where a personal stop
// keeps structural backing even though the pool reads "used"). Additive-only:
// slIfLong/slIfShort stay as the single primary rail.
function buildSlRails(out, price, buffer, r) {
  const H1 = out.structure.H1, dr = out.dealingRange4H, fvgs = out.fvgs || {}, obs = out.obs || {};
  const mk = (level, label, why, swept) => ({ level: r(level), label, why, swept: !!swept });
  const longC = [], shortC = [];
  if (H1.slIfLong != null) longC.push(mk(H1.slIfLong, "H1 swing low", "under the swing that anchors the intraday trend — a break flips H1 structure", false));
  if (H1.slIfShort != null) shortC.push(mk(H1.slIfShort, "H1 swing high", "above the swing that anchors the intraday trend — a break flips H1 structure", false));
  for (const tf of ["H1", "M15"]) {
    for (const g of ((fvgs[tf] || {}).bullish) || []) if (g.bottom < price) longC.push(mk(g.bottom - buffer, `${tf} bullish FVG floor`, "under the unmitigated demand FVG — a true break invalidates the imbalance", false));
    for (const g of ((obs[tf] || {}).bullish) || []) if (g.bottom < price) longC.push(mk(g.bottom - buffer, `${tf} bullish OB base`, "under the demand order block — the last down-close before the up-move", false));
    for (const g of ((fvgs[tf] || {}).bearish) || []) if (g.top > price) shortC.push(mk(g.top + buffer, `${tf} bearish FVG ceiling`, "over the unmitigated supply FVG — a true break invalidates the imbalance", false));
    for (const g of ((obs[tf] || {}).bearish) || []) if (g.top > price) shortC.push(mk(g.top + buffer, `${tf} bearish OB top`, "over the supply order block — the last up-close before the down-move", false));
  }
  if (dr) {
    if (dr.low < price) longC.push(mk(dr.low - buffer, "4H range low", "under the 4H dealing-range low — loses the discount leg", false));
    if (dr.high > price) shortC.push(mk(dr.high + buffer, "4H range high", "over the 4H dealing-range high — loses the premium leg", false));
  }
  for (const l of (out.liquidity?.below) || []) if ((l.swept || l.touched) && l.level < price) longC.push(mk(l.level - buffer, `swept ${l.label}`, "price already raided this level — it can still act as inversion support (iFVG-style); a personal stop parked here keeps structural backing even though the pool reads 'used'", true));
  for (const l of (out.liquidity?.above) || []) if ((l.swept || l.touched) && l.level > price) shortC.push(mk(l.level + buffer, `swept ${l.label}`, "price already raided this level — it can still act as inversion resistance; a personal stop parked here keeps structural backing even though the pool reads 'used'", true));
  const finish = (arr, longSide) => {
    const seen = new Set(), keep = [];
    arr.sort((a, b) => longSide ? b.level - a.level : a.level - b.level); // nearest to price first
    for (const c of arr) { const k = c.level.toFixed(6); if (seen.has(k)) continue; seen.add(k); keep.push(c); if (keep.length >= 3) break; }
    return keep;
  };
  out.structure.H1.slRails = { long: finish(longC, true), short: finish(shortC, false) };
}

// Draw on liquidity: the single pool price is most likely being pulled toward
// right now — the first question of any ICT read. Weighted by pool class
// (weekly/daily levels and engineered EQH/EQL over session extremes),
// alignment with H4/D structure, and proximity. Unswept pools only: a raided
// pool no longer pulls.
function pickDOL(lq, s, price, atrD) {
  const classW = (lb) => /prev-week/.test(lb) ? 3 : /PD[HL]/.test(lb) ? 3 : /EQ[HL]/.test(lb) ? 2.5 : /prev/.test(lb) ? 2 : 1.5;
  const cands = [];
  for (const side of ["above", "below"]) {
    const dirBias = side === "above" ? "bullish" : "bearish";
    for (const lv of lq[side]) {
      if (lv.swept) continue;
      let sc = classW(lv.label);
      if (s.H4.bias === dirBias) sc += 2;
      if (s.D.bias === dirBias) sc += 1;
      const dist = Math.abs(lv.level - price);
      sc -= (dist / atrD) * 0.5;
      cands.push({ side, level: lv.level, label: lv.label, tf: lv.tf, atLocal: lv.atLocal, score: Number(sc.toFixed(2)), dist, touched: !!lv.touched });
    }
  }
  if (!cands.length) return null;
  cands.sort((a, b) => b.score - a.score);
  // Pools that are already visited or effectively at price are not useful
  // forward draws. Skip them entirely; if none remain, return no DOL instead
  // of presenting an irrelevant historical area as the primary target.
  const eligible = filterForwardDraws(cands, atrD);
  if (!eligible.length) return null;
  const primary = eligible[0];
  const nxt = eligible[1] || null;
  const best = { side: primary.side, level: primary.level, label: primary.label, tf: primary.tf, atLocal: primary.atLocal, score: primary.score };
  if (nxt) best.next = { side: nxt.side, level: nxt.level, label: nxt.label, tf: nxt.tf, atLocal: nxt.atLocal };
  best.note = `price is most likely being drawn ${best.side === "above" ? "UP" : "DOWN"} to ${best.label} ${best.level}${best.atLocal ? ` (${best.tf}, seen ${best.atLocal})` : ""}`
    + (best.next ? ` · next draw: ${best.next.label} ${best.next.level}` : "");
  return best;
}

// Deterministic bull/bear debate per ticket: every argument comes from script
// facts, weighed into a verdict. Rejected tickets never reach the card;
// borderline ones print with their strongest objection. This is the
// TradingAgents debate idea made deterministic so any model can carry it.
function debateTicket(o, c) {
  const long = c.direction === "LONG";
  const s = o.structure, dr = o.dealingRange4H, m = o.meta;
  const forArgs = [], against = [];
  let score = 0;
  const pro = (txt) => { forArgs.push(txt); score += 1; };
  const con = (txt, w = 1) => { against.push(txt); score -= w; };

  if (/active/i.test(m.killzone)) pro(`killzone active (${m.killzone})`);
  else con("outside killzones — thin participation");
  if (s.H4.bias === (long ? "bullish" : "bearish")) pro("H4 structure aligned");
  else if (s.H4.bias !== "range") con(`fighting H4 ${s.H4.bias}`);
  if (s.D.bias === (long ? "bullish" : "bearish")) pro("daily structure aligned");
  else if (s.D.bias !== "range") con(`fighting daily ${s.D.bias}`);
  if (c.swept) pro(`confirmed liquidity ${c.sweepLabel ? `raid on ${c.sweepLabel}` : "sweep"} behind the entry`);
  if (c.rr >= 2) pro(`RR ${c.rr} pays for the risk`);
  const dol = o.drawOnLiquidity;
  if (dol) {
    const toward = (long && dol.side === "above") || (!long && dol.side === "below");
    if (toward) pro(`trades toward the draw on liquidity (${dol.label} ${dol.level})`);
    else con(`trades INTO the draw — price is being pulled toward ${dol.label} ${dol.level}`, 2);
  }
  // Entry location within the reversal leg (raid extreme → TP1): the deeper
  // the entry sits, the better the location.
  if (c.sweepLevel != null && c.tp1 != null) {
    // Signed position: only meaningful when the entry actually sits inside
    // the raid-extreme → TP1 leg (the fallback pool pick can put the swept
    // level on the far side of the entry — no location claim then).
    const denom = c.tp1 - c.sweepLevel;
    const posF = denom !== 0 ? (c.entry - c.sweepLevel) / denom : -1;
    if (posF >= 0 && posF <= 1) {
      const pos = Math.round(posF * 100);
      if (pos <= 38) pro(`entry deep in the reversal leg (${pos}% off the raid extreme)`);
      else if (pos >= 62) con(`entry chases the reversal leg (${pos}% up the move)`);
    }
  }
  if (c.macroNote) {
    if (c.macroNote.startsWith("macro-aligned")) pro(c.macroNote);
    else con(c.macroNote, 2);
  }
  // Wyckoff confluence: a spring/markup backing a long (or upthrust/markdown a
  // short) is textbook; a distribution structure under a long is a real warning.
  const wy = o.wyckoff;
  if (wy && wy.bias !== "neutral") {
    if ((wy.bias === "bullish") === long) pro(`Wyckoff aligned — ${wy.event || wy.schematic} (${wy.phase})`);
    else con(`Wyckoff opposes — ${wy.schematic} structure biased ${wy.bias}`, 2);
  }
  const h1 = s.H1;
  if (h1.bias === (long ? "bullish" : "bearish") && (h1.continuation || 0) >= 4) {
    pro(`H1 structure strong (continuation ${h1.continuation}/5)`);
  }
  if (dr) {
    if (long && dr.zone === "discount") pro(`buying discount (${dr.positionPct}%)`);
    if (!long && dr.zone === "premium") pro(`selling premium (${dr.positionPct}%)`);
    if (long && dr.positionPct > 75) con(`buying deep premium (${dr.positionPct}% of the 4H range)`);
    if (!long && dr.positionPct < 25) con(`selling deep discount (${dr.positionPct}% of the 4H range)`);
  }
  if (m.regime?.trendDay) {
    if ((m.regime.direction === "up") === long) pro(`with the trend day (${m.regime.direction})`);
    // counter-trend-day tickets were already dropped by the hard gate
  }
  if (c.entryType === "market" && m.atrUsedTodayPct >= 110) {
    con(`day's range already spent (${m.atrUsedTodayPct}% ATR) — chasing late`);
  }
  const soon = (m.newsRisk || []).find((e) => e.inMin <= 180);
  if (soon) con(`${soon.ccy} ${soon.event} in ${soon.inMin}m — resting orders can gap through stops`);
  // Target obstruction: an unswept pool sitting between entry and TP1 is
  // where the move stalls before paying.
  if (c.tp1 != null) {
    const pools = long ? o.liquidity.above : o.liquidity.below;
    const eps = 0.05 * m.atrDaily;
    const blocker = pools.find((l) => !l.swept
      && (long ? l.level > c.entry + eps && l.level < c.tp1 - eps
               : l.level < c.entry - eps && l.level > c.tp1 + eps));
    if (blocker) con(`unswept ${blocker.label} ${blocker.level} sits before TP1 — likely stall`);
  }
  const verdict = score >= 2 ? "valid" : score >= 0 ? "borderline" : "rejected";
  return { for: forArgs, against, score, verdict };
}

// Continuation scoring per timeframe: how likely is this structure to HOLD?
// Deterministic factors: alignment with the higher timeframe, freshness
// (CHoCH), momentum (BOS with the bias), room inside the 4H range, and the
// day's ATR budget. Score 1-5; `factors` strings are copy-ready for the card.
function scoreStructure(tfName, s, higher, higherName, dr, atrUsedPct) {
  if (!s || s.bias == null) return;
  if (s.bias === "range") {
    // A range IS structure — report the bounds and where price sits, not "no edge".
    s.continuation = 2;
    s.verdict = "ranging";
    const hi = s.lastSwingHigh, lo = s.lastSwingLow, c = s.lastClose;
    if (hi != null && lo != null && hi > lo) {
      const pos = c != null ? Math.round(((c - lo) / (hi - lo)) * 100) : null;
      const lean = pos == null ? "" : pos >= 70 ? ` — near the top (${pos}%), watch for a fade or a break up`
        : pos <= 30 ? ` — near the bottom (${pos}%), watch for a bounce or a break down`
        : ` — mid-range (${pos}%), the low-conviction zone`;
      s.factors = [`ranging between ${lo} and ${hi}${lean}`, "no clean trend — trade the edges, not the middle"];
    } else {
      s.factors = ["ranging — not enough swings yet for a trend read"];
    }
    return;
  }
  let score = 2;
  const factors = [];
  if (higher && higher.bias === s.bias) { score++; factors.push(`aligned with ${higherName} ${higher.bias}`); }
  else if (higher && higher.bias !== "range" && higher.bias !== s.bias) { score--; factors.push(`fighting ${higherName} ${higher.bias} — likely counter-trend`); }
  if (s.choch) { score++; factors.push(`fresh CHoCH${s.chochLevel != null ? ` through ${s.chochLevel}` : ""} — young structure, early in its life`); }
  if ((s.bias === "bullish" && s.bosUp) || (s.bias === "bearish" && s.bosDown)) { score++; factors.push("BOS with the trend — momentum confirmed"); }
  if ((s.bias === "bullish" && s.bosDown) || (s.bias === "bearish" && s.bosUp)) { score -= 2; factors.push("just broke AGAINST its own bias — failing"); }
  if (dr) {
    if (s.bias === "bullish" && dr.positionPct < 60) { score++; factors.push(`room to run — price at ${dr.positionPct}% of the 4H range`); }
    else if (s.bias === "bullish" && dr.positionPct > 75) { score--; factors.push(`deep premium (${dr.positionPct}%) — little room left up`); }
    else if (s.bias === "bearish" && dr.positionPct > 40) { score++; factors.push(`room to run — price at ${dr.positionPct}% of the 4H range`); }
    else if (s.bias === "bearish" && dr.positionPct < 25) { score--; factors.push(`deep discount (${dr.positionPct}%) — little room left down`); }
  }
  if ((tfName === "H1" || tfName === "M15") && atrUsedPct >= 150) { score--; factors.push(`daily range exhausted (${atrUsedPct}% ATR used)`); }
  s.continuation = Math.max(1, Math.min(5, score));
  s.verdict = s.continuation >= 5 ? "very likely to hold" : s.continuation === 4 ? "likely to hold" : s.continuation === 3 ? "usable with care" : s.continuation === 2 ? "weak" : "likely to fail";
  s.factors = factors.length ? factors : ["plain trend, no extra confluence"];
}

// Whole-board verdict: alignment count, the strongest timeframe, and a
// deterministic one-liner for the classic combinations (copy-ready).
function readStructureBoard(st) {
  const tfs = ["D", "H4", "H1", "M15"];
  const biases = tfs.map((t) => st[t]?.bias);
  const bull = biases.filter((b) => b === "bullish").length;
  const bear = biases.filter((b) => b === "bearish").length;
  let strongest = null;
  for (const t of tfs) {
    const s = st[t];
    if (s?.continuation != null && s.bias !== "range" && (!strongest || s.continuation > st[strongest].continuation)) strongest = t;
  }
  const h4 = st.H4, h1 = st.H1, d = st.D;
  let note;
  if (bull === 4) note = "full bullish alignment — highest-probability continuation up";
  else if (bear === 4) note = "full bearish alignment — highest-probability continuation down";
  else if (h4?.bias === "bearish" && h1?.bias === "bullish") note = h4.bosUp
    ? `H4 bearish is BREAKING — price closed above its swing high ${h4.lastSwingHigh}; bias flip in progress, H1 bullish is leading`
    : `H1/M15 strength is counter-trend inside H4 bearish — treat rallies as pullbacks to sell unless H4 reclaims ${h4.lastSwingHigh}`;
  else if (h4?.bias === "bullish" && h1?.bias === "bearish") note = h4.bosDown
    ? `H4 bullish is BREAKING — price closed below its swing low ${h4.lastSwingLow}; bias flip in progress, H1 bearish is leading`
    : `H1/M15 weakness is counter-trend inside H4 bullish — treat dips as pullbacks to buy unless H4 loses ${h4.lastSwingLow}`;
  else if (h4?.bias !== "range" && d?.bias !== "range" && h4?.bias !== d?.bias) note = `H4 ${h4.bias} is a counter-trend bounce inside the bigger D ${d.bias} trend — fine to trade intraday, but exit within the session; don't hold it like a swing position`;
  else if (h4?.bias === "range") note = "H4 undecided — H1/M15 structure carries less weight until H4 picks a side";
  else {
    // Fallback for boards that match no classic combination: state the actual
    // majority (and name the exception timeframes with their real states)
    // instead of always phrasing it as "N of 4 bullish".
    const state = (t) => `${t} (${st[t]?.bias || "?"})`;
    const bullTfs = tfs.filter((t) => st[t]?.bias === "bullish");
    const bearTfs = tfs.filter((t) => st[t]?.bias === "bearish");
    const rangeN = 4 - bull - bear;
    if (bear > bull) {
      const exc = tfs.filter((t) => st[t]?.bias !== "bearish").map(state).join(" and ");
      note = `${bear} of 4 timeframes bearish — mostly bearish board except ${exc}; trade only where timeframes agree`;
    } else if (bull > bear) {
      const exc = tfs.filter((t) => st[t]?.bias !== "bullish").map(state).join(" and ");
      note = `${bull} of 4 timeframes bullish — mostly bullish board except ${exc}; trade only where timeframes agree`;
    } else {
      note = `mixed board — ${bull} bullish (${bullTfs.join(", ") || "none"}) vs ${bear} bearish (${bearTfs.join(", ") || "none"})${rangeN ? ` with ${rangeN} in range` : ""}; trade only where timeframes agree`;
    }
  }
  return { alignment: `${bull} bullish / ${bear} bearish / ${4 - bull - bear} range`, strongest, note };
}

// One-line summary per asset for scan mode.
function summarize(o) {
  const s = {
    asset: o.meta.asset,
    price: o.meta.price,
    biasH4: o.structure.H4.bias,
    zone: o.dealingRange4H ? `${o.dealingRange4H.zone} ${o.dealingRange4H.positionPct}%` : null,
    dataAgeMin: o.meta.dataAgeMin,
  };
  if (o.meta.isFutures) s.futures = true;
  if (o.meta.newsRisk?.length) s.newsRisk = o.meta.newsRisk;
  if (o.candidate) {
    s.candidate = o.candidate;
    if (o.candidateNow) s.alsoNow = o.candidateNow;
  } else {
    s.reason = o.meta.marketLikelyClosed ? "market likely closed" : "no setup ≥ RR 1.5";
  }
  return s;
}

const rawArgs = process.argv.slice(2).map((a) => (a || "").toLowerCase().replace(/[^a-z0-9=.-]/g, ""));
const structureMode = rawArgs.includes("structure");
const arg = rawArgs.find((a) => a && a !== "structure") || "";
if (!arg) fail("no asset given. Usage: node ict-levels.mjs XAUUSD | scan | structure XAUUSD");
// Optional custom watchlist for scan/universe (the dashboard's pair selector),
// passed via UNIVERSE_ASSETS env (comma-separated). Empty → the default 15.
const CUSTOM = (process.env.UNIVERSE_ASSETS || "").split(",").map((s) => s.trim().toLowerCase().replace(/[^a-z0-9]/g, "")).filter(Boolean);
const LIST = CUSTOM.length ? CUSTOM : DEFAULT_ASSETS;

if (arg === "universe") {
  // FULL analyze() output for every asset — machine consumption only (the
  // browser dashboard). ~150 KB of JSON; models must keep using `scan`.
  const sharedCalendar = await fetchCalendar();
  const results = new Array(LIST.length);
  let next = 0;
  async function worker() {
    while (next < LIST.length) {
      const idx = next++;
      try { results[idx] = await analyze(LIST[idx], sharedCalendar); }
      catch (e) { results[idx] = { meta: { asset: LIST[idx].toUpperCase() }, error: e.message }; }
    }
  }
  await Promise.all([worker(), worker(), worker()]);
  const clock = sessionClock();
  console.log(JSON.stringify({ universe: {
    clock: clock.local, tz: clock.tz, killzone: clock.killzone, session: clock.session, marketOpen: clock.marketOpen,
    reopenLocal: clock.reopenLocal, reopenInMin: clock.reopenInMin,
    closeLocal: clock.closeLocal, closeInMin: clock.closeInMin,
    generatedAtMs: Date.now(), assets: results } }));
} else if (arg === "scan" || arg === "all" || arg === "watchlist") {
  const sharedCalendar = await fetchCalendar(); // once for all assets
  const results = new Array(LIST.length);
  let next = 0;
  async function worker() {
    while (next < LIST.length) {
      const idx = next++;
      try { results[idx] = summarize(await analyze(LIST[idx], sharedCalendar)); }
      catch (e) { results[idx] = { asset: LIST[idx].toUpperCase(), error: e.message }; }
    }
  }
  await Promise.all([worker(), worker(), worker()]);
  const clock = sessionClock();
  console.log(JSON.stringify({
    scan: {
      clock: clock.local, tz: clock.tz, killzone: clock.killzone, session: clock.session, marketOpen: clock.marketOpen,
      reopenLocal: clock.reopenLocal, closeLocal: clock.closeLocal, closeInMin: clock.closeInMin,
      validEntries: results.filter((x) => x.candidate),
      standDown: results.filter((x) => !x.candidate && !x.error).map((x) => x.asset),
      errors: results.filter((x) => x.error),
    },
  }, null, 1));
} else {
  try {
    const out = await analyze(arg, undefined, { ohlc: !structureMode });
    if (structureMode) {
      // Compact structure-only report: per-TF bias + continuation score +
      // factors, plus the whole-board read. No tickets, no level maps.
      const m = out.meta;
      console.log(JSON.stringify({
        meta: {
          asset: m.asset, price: m.price, clock: m.clock, killzone: m.killzone, session: m.session,
          dataAgeMin: m.dataAgeMin, marketLikelyClosed: m.marketLikelyClosed,
          atrUsedTodayPct: m.atrUsedTodayPct, priceNote: m.priceNote, newsRisk: m.newsRisk,
        },
        structure: out.structure,
        dealingRange4H: out.dealingRange4H,
        structureRead: out.structureRead,
      }, null, 1));
    } else {
      console.log(JSON.stringify(out, null, 1));
    }
  } catch (e) {
    fail(e.message);
  }
}
