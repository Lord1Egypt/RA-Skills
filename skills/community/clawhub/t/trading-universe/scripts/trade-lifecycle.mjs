import { pipSize, normalizeAsset, symbolForAsset } from "./symbols.mjs";
import { ENGINE_CONFIG } from "./tde-entry-engine.mjs";

export const TRADE_SCHEMA_VERSION = 2;
export const ACTIVE_STATUSES = new Set(["pending", "open", "ambiguous"]);
export const TERMINAL_STATUSES = new Set(["closed", "cancelled", "expired", "invalid_before_fill"]);

const finite = (x) => typeof x === "number" && Number.isFinite(x);
const iso = (x) => {
  const d = new Date(x);
  return Number.isFinite(d.getTime()) ? d.toISOString() : null;
};
const rnd2 = (x) => Number.isFinite(x) ? Number(x.toFixed(2)) : null;
const rnd1 = (x) => Number.isFinite(x) ? Number(x.toFixed(1)) : null;

// Seconds per bar, by the interval reconcileTrades tags onto the candle array.
// Used to measure MARKET-hours elapsed (candle count × interval) for the
// unfilled-order expiry — weekend/holiday gaps print no candles, so they
// correctly don't count toward the 36-market-hour limit.
const INTERVAL_SEC = { "1m": 60, "5m": 300, "15m": 900, "1h": 3600 };
const EXPIRE_MARKET_SEC = 36 * 3600;

export function setupId(setup) {
  const s = String(setup || "").toLowerCase();
  const models = [
    ["fvg mitigation", "fvg-mitigation"],
    ["premium/discount reversal", "premium-discount"],
    ["trend continuation", "trend-continuation"],
    ["order block", "order-block"],
    ["mss + fvg", "mss-fvg"],
    ["ict 2022 model", "ict-2022"],
    ["2022 model", "ict-2022"],
    ["ote retracement", "ote"],
    ["choch continuation", "choch-continuation"],
    ["confirmed turtle soup", "turtle-soup-confirmed"],
    ["momentum bos", "momentum-bos"],
    ["relative-volume continuation", "volume-continuation"],
    ["fourth-candle fvg confirmation", "fvg-fourth-candle-confirmed"],
    ["in-gap bounce", "in-gap-bounce"],
  ];
  return models.find(([prefix]) => s.startsWith(prefix))?.[1] ?? "unknown";
}

// Immutable activation snapshot used by the trade-detail and saved-review UI.
// New records capture this before any manual edit can mutate the live ticket.
// Migrated records are explicitly labelled because an older ledger cannot
// reconstruct levels that may have been edited before this field existed.
export function snapshotTicket(ticket, source = "activation") {
  return {
    source,
    capturedAt: iso(ticket?.activatedAt || ticket?.orderPlacedAt) || new Date().toISOString(),
    asset: normalizeAsset(ticket?.asset),
    direction: String(ticket?.direction || "").toUpperCase(),
    setup: ticket?.setup || "",
    setupId: ticket?.setupId || setupId(ticket?.setup),
    engineVersion: ticket?.engineVersion || null,
    entryType: ticket?.entryType || "limit",
    entry: ticket?.entry ?? null,
    sl: ticket?.sl ?? null,
    tp1: ticket?.tp1 ?? null,
    tp1Label: ticket?.tp1Label || null,
    tp2: ticket?.tp2 ?? null,
    tp2Label: ticket?.tp2Label || null,
    rr: ticket?.rr ?? null,
    r1: ticket?.r1 ?? null,
    r2: ticket?.r2 ?? null,
    stars: ticket?.stars ?? null,
    whyEntry: ticket?.whyEntry || "",
    whySL: ticket?.whySL || "",
    priceAtActivation: ticket?.priceAtActivation ?? null,
    killzone: ticket?.killzone || null,
    structureNote: ticket?.structureNote || null,
    originAt: ticket?.originAt || null,
    originAtLocal: ticket?.originAtLocal || null,
  };
}

export function validateTicket(ticket, opts = {}) {
  const errors = [];
  const direction = String(ticket?.direction || "").toUpperCase();
  if (!/^(LONG|SHORT)$/.test(direction)) errors.push("direction must be LONG or SHORT");
  for (const key of ["entry", "sl", "tp1"]) if (!finite(ticket?.[key])) errors.push(`${key} must be finite`);
  if (ticket?.tp2 != null && !finite(ticket.tp2)) errors.push("tp2 must be finite or null");
  if (!errors.length) {
    const { entry, sl, tp1, tp2 } = ticket;
    const ordered = direction === "LONG"
      ? sl < entry && entry < tp1 && (tp2 == null || tp1 < tp2)
      : sl > entry && entry > tp1 && (tp2 == null || tp1 > tp2);
    if (!ordered) errors.push("ticket levels are not ordered for direction");
    // RR band is an entry-QUALITY gate — it belongs only to /api/trades/add.
    // Manual edits (skipRR) and the replayer must not be blocked by it, or an
    // edited RR-out-of-band trade would flip to "ambiguous" on the next pass.
    if (!opts.skipRR) {
      const risk = Math.abs(entry - sl);
      const rr = risk ? (direction === "LONG" ? tp1 - entry : entry - tp1) / risk : NaN;
      if (!(rr >= ENGINE_CONFIG.minRR)) errors.push(`RR ${Number.isFinite(rr) ? rr.toFixed(2) : "invalid"} below engine qualification`);
    }
  }
  return { ok: errors.length === 0, errors };
}

function event(trade, type, eventAt, detail, source = "system") {
  trade.events ||= [];
  const at = iso(eventAt) || new Date().toISOString();
  const key = `${type}:${at}`;
  if (trade.events.some((e) => `${e.type}:${e.eventAt}` === key)) return false;
  const recordedAt = new Date().toISOString(), line = String(detail || "");
  trade.events.push({ type, eventAt: at, recordedAt, source, detail: line });
  trade.history ||= [];
  trade.history.push({ at, recordedAt, event: type, detail: line, source });
  return true;
}

export function migrateTradeDocument(input) {
  const raw = Array.isArray(input?.trades) ? input.trades : [];
  let changed = input?.schemaVersion !== TRADE_SCHEMA_VERSION;
  const trades = raw.map((old) => {
    const t = { ...old };
    t.asset = normalizeAsset(t.asset);
    t.schemaVersion = TRADE_SCHEMA_VERSION;
    t.setupId ||= setupId(t.setup);
    t.orderPlacedAt ||= t.activatedAt || new Date().toISOString();
    t.dataQuality ||= { status: "provisional", excludedFromStats: false, reason: "migrated v1 record" };
    t.events ||= (t.history || []).map((h) => ({
      type: h.event || "legacy", eventAt: iso(h.at), recordedAt: iso(h.at), source: "legacy", detail: h.detail || "",
    })).filter((e) => e.eventAt);
    if (!t.originalTicket) {
      t.originalTicket = snapshotTicket(t, "migration-current-state");
      changed = true;
    }
    if (t.status === "open" && t.entryType === "limit" && !t.filledAt) t.status = "pending";
    if (t.status === "open" && t.entryType === "market" && !t.filledAt) {
      t.filledAt = t.activatedAt; t.fillPrice = t.entry;
    }
    if (t.outcome === "cancelled") t.status = "cancelled";
    if (t.status === "closed" && t.invalidated) { t.invalidated = false; t.invalidatedAt = null; }
    if (t.status !== old.status || !old.schemaVersion || !old.setupId || !old.events || !old.dataQuality || !old.originalTicket) changed = true;
    return t;
  });
  return { document: { schemaVersion: TRADE_SCHEMA_VERSION, updatedAt: input?.updatedAt || new Date().toISOString(), trades }, changed };
}

export function performanceStats(trades) {
  const scored = trades.filter((t) => t.status === "closed" && finite(t.rMultiple) && !t.dataQuality?.excludedFromStats);
  const wins = scored.filter((t) => t.rMultiple > 0);
  const losses = scored.filter((t) => t.rMultiple < 0);
  const totalR = scored.reduce((a, t) => a + t.rMultiple, 0);
  const grossWin = wins.reduce((a, t) => a + t.rMultiple, 0);
  const grossLoss = -losses.reduce((a, t) => a + t.rMultiple, 0);
  return {
    n: scored.length, wins: wins.length, losses: losses.length,
    totalR: rnd2(totalR), expectancyR: scored.length ? rnd2(totalR / scored.length) : null,
    profitFactor: grossLoss > 0 ? rnd2(grossWin / grossLoss) : grossWin > 0 ? null : 0,
  };
}

export async function fetchLifecycleCandles(asset, startMs, endMs = Date.now(), fetchImpl = fetch) {
  const symbol = symbolForAsset(asset);
  if (!symbol) throw new Error(`unsupported asset ${asset}`);
  const ageDays = Math.max(0, (endMs - startMs) / 864e5);
  const intervals = ageDays <= 7 ? ["1m", "5m", "15m"] : ageDays <= 30 ? ["5m", "15m", "1h"] : ["15m", "1h"];
  let lastError;
  for (const interval of intervals) {
    const p1 = Math.floor((startMs - 3600e3) / 1000), p2 = Math.ceil((endMs + 60e3) / 1000);
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?period1=${p1}&period2=${p2}&interval=${interval}&events=history`;
    try {
      const res = await fetchImpl(url, { headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }, signal: AbortSignal.timeout(15000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const j = await res.json(); const r = j?.chart?.result?.[0]; const q = r?.indicators?.quote?.[0];
      if (!r?.timestamp?.length || !q) throw new Error("empty candle result");
      const candles = r.timestamp.map((t, i) => ({ t: t * 1000, o: q.open[i], h: q.high[i], l: q.low[i], c: q.close[i] }))
        .filter((c) => c.t >= startMs && finite(c.o) && finite(c.h) && finite(c.l) && finite(c.c));
      if (candles.length) return { symbol, interval, candles };
      throw new Error("no candles in lifecycle window");
    } catch (e) { lastError = e; }
  }
  throw new Error(`${asset} lifecycle candles unavailable: ${lastError?.message || "unknown"}`);
}

// Replay the documented management plan: 50% at TP1, remaining stop to BE,
// runner to TP2; no TP2 means full exit at TP1. Same-bar conflicts are marked
// ambiguous rather than guessed.
export function reconcileTrade(trade, candles, now = Date.now()) {
  const t = trade;
  if (!ACTIVE_STATUSES.has(t.status)) return { changed: false, trade: t };
  const valid = validateTicket(t, { skipRR: true });
  if (!valid.ok) {
    t.status = "ambiguous"; t.lifecycleError = valid.errors.join("; ");
    return { changed: true, trade: t };
  }
  const long = t.direction === "LONG";
  const risk = Math.abs(t.entry - t.sl);
  let changed = false;
  let fillIndex = -1;
  if (t.filledAt) fillIndex = candles.findIndex((c) => c.t >= new Date(t.filledAt).getTime());
  if (fillIndex < 0 && t.entryType === "market") {
    fillIndex = 0; t.filledAt = iso(t.orderPlacedAt); t.fillPrice = t.entry; t.status = "open";
    changed = event(t, "filled", t.filledAt, `market entry ${t.entry}`, "replay") || changed;
  }
  if (fillIndex < 0) {
    const marketable = finite(t.priceAtActivation) && (long ? t.priceAtActivation <= t.entry : t.priceAtActivation >= t.entry);
    if (marketable) fillIndex = 0;
    else fillIndex = candles.findIndex((c) => long ? c.l <= t.entry : c.h >= t.entry);
    if (fillIndex >= 0) {
      const c = candles[fillIndex]; t.filledAt = iso(marketable ? t.orderPlacedAt : c.t); t.fillPrice = t.entry; t.status = "open";
      changed = event(t, "filled", t.filledAt, `${t.direction} limit filled @ ${t.entry}`, "replay") || changed;
    }
  }
  if (fillIndex < 0) {
    // Auto-expire a resting order that never filled within 36 MARKET-hours.
    // Market-hours = number of candles since the order was placed × the bar
    // interval; the reconcile feed is already sliced to c.t >= orderPlacedAt,
    // so weekend gaps simply contribute no candles. sec === 0 (a caller that
    // passed a plain array with no .interval, e.g. a unit test) never expires.
    const sec = INTERVAL_SEC[candles.interval] || 0;
    if (!t.expireExempt && sec > 0 && candles.length * sec >= EXPIRE_MARKET_SEC) {
      const idx = Math.min(candles.length - 1, Math.ceil(EXPIRE_MARKET_SEC / sec) - 1);
      const at = iso(candles[idx].t);
      t.status = "expired"; t.outcome = "not_filled";
      t.closedAt = at; t.eventClosedAt = at; t.recordedClosedAt = new Date().toISOString();
      t.lastCheckedAt = new Date(now).toISOString();
      changed = event(t, "expired", candles[idx].t, "limit not filled within 36 market-hours — order expired", "replay") || changed;
      return { changed: true, trade: t };
    }
    t.status = "pending"; t.lastCheckedAt = new Date(now).toISOString();
    return { changed, trade: t };
  }

  let min = Infinity, max = -Infinity, tp1Hit = !!t.tp1HitAt;
  for (let i = Math.max(0, fillIndex); i < candles.length; i++) {
    const c = candles[i]; min = Math.min(min, c.l); max = Math.max(max, c.h);
    const slLevel = tp1Hit ? t.entry : t.sl;
    const hitSl = long ? c.l <= slLevel : c.h >= slLevel;
    const hitTp1 = !tp1Hit && (long ? c.h >= t.tp1 : c.l <= t.tp1);
    const hitTp2 = t.tp2 != null && (long ? c.h >= t.tp2 : c.l <= t.tp2);
    if ((hitSl && hitTp1) || (hitSl && hitTp2)) {
      t.status = "ambiguous"; t.ambiguousAt = iso(c.t);
      t.lifecycleError = `same ${candles.interval || "candle"} touched stop and target; lower timeframe/manual confirmation required`;
      changed = event(t, "ambiguous", c.t, t.lifecycleError, "replay") || changed;
      break;
    }
    if (hitSl) {
      t.status = "closed"; t.outcome = tp1Hit ? "tp1be" : "sl"; t.exitPrice = slLevel; t.eventClosedAt = iso(c.t);
      t.recordedClosedAt = new Date().toISOString(); t.closedAt = t.eventClosedAt;
      t.rMultiple = tp1Hit ? rnd2(0.5 * t.r1) : -1;
      changed = event(t, "closed", c.t, `${t.outcome} automatically reconciled @ ${slLevel}`, "replay") || changed;
      break;
    }
    if (hitTp2 && tp1Hit) {
      t.status = "closed"; t.outcome = "tp2"; t.exitPrice = t.tp2; t.eventClosedAt = iso(c.t);
      t.recordedClosedAt = new Date().toISOString(); t.closedAt = t.eventClosedAt;
      t.rMultiple = t.r1 == null ? null : t.r2 != null ? rnd2(0.5 * t.r1 + 0.5 * t.r2) : t.r1;
      changed = event(t, "closed", c.t, `TP2 automatically reconciled @ ${t.tp2}`, "replay") || changed;
      break;
    }
    if (hitTp1) {
      t.tp1HitAt = iso(c.t); tp1Hit = true;
      changed = event(t, "tp1", c.t, `TP1 touched @ ${t.tp1}; simulated runner stop moved to breakeven`, "replay") || changed;
      if (t.tp2 == null) {
        t.status = "closed"; t.outcome = "tp1full"; t.exitPrice = t.tp1; t.eventClosedAt = iso(c.t);
        t.recordedClosedAt = new Date().toISOString(); t.closedAt = t.eventClosedAt; t.rMultiple = t.r1;
        changed = event(t, "closed", c.t, `full exit at TP1 automatically reconciled`, "replay") || changed;
        break;
      }
    }
  }
  if (min < Infinity) {
    const mfe = rnd2((long ? max - t.entry : t.entry - min) / risk);
    const mae = rnd2((long ? t.entry - min : max - t.entry) / risk);
    if (mfe !== t.mfeR || mae !== t.maeR) changed = true;
    t.mfeR = mfe; t.maeR = mae;
  }
  t.lastCheckedAt = new Date(now).toISOString();
  if (t.status === "closed") {
    t.invalidated = false; t.invalidatedAt = null;
    t.pips = finite(t.rMultiple) ? rnd1(t.rMultiple * risk / pipSize(t.asset)) : null;
    t.dataQuality ||= { status: "replayed", excludedFromStats: false, reason: "" };
    if (t.dataQuality.status === "provisional") t.dataQuality.status = "replayed";
    const family = t.setupId || setupId(t.setup);
    t.lesson = `${t.asset} ${t.direction} ${family}` +
      (t.fundamentals ? ` | macro ${t.fundamentals.direction} ${t.fundamentals.score}/5` : "") +
      ` | ${t.killzone || "kz?"} -> ${t.outcome}` + (finite(t.rMultiple) ? ` (${t.rMultiple > 0 ? "+" : ""}${t.rMultiple}R)` : "");
  }
  return { changed, trade: t };
}
