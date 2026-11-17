import { buildRegistry, detectMssEvents, detectMultiScaleSwings } from "./tde-registry.mjs";
import { simulateTicket, DEFAULT_RISK_POLICY } from "./tde-lifecycle.mjs";
import { deriveModelStop } from "./tde-risk.mjs";

export const ENGINE_CONFIG = Object.freeze({
  minRR: 2,
  minIndependentConfluences: 2,
  atrPeriod: 14,
  minDisplacementBodyPct: 50,
  minDisplacementBodyMultiple: 0.8,
  volumeExpansionRatio: 1.5,
  relativeVolumeLookback: 20,
  minRelativeVolumeSamples: 10,
  turtleMinCloseInsideRangePct: 10,
  turtleMinCloseAwayFromExtremePct: 50,
  oteEntryPct: 0.62,
  oteBand: Object.freeze([0.62, 0.79]),
  maxBarsSweepToMss: 4,
  equalPoolToleranceAtr: 0.1,
  pendingOrderLifetimeMarketHours: 36,
  riskPolicy: DEFAULT_RISK_POLICY,
  excludedModels: ["breaker", "bpr", "inducement", "crt", "po3", "smt",
    "volume-profile", "poc-hvn-lvn", "order-flow-delta"],
});

const avg = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null;
const iso = (t) => t == null ? null : new Date(t * 1000).toISOString();
const finite = (x) => typeof x === "number" && Number.isFinite(x);
const clamp = (x) => Math.max(0, Math.min(1, x));
const body = (c) => Math.abs(c.c - c.o);
const candleRange = (c) => Math.max(0, c.h - c.l);

export function resolveMarketEntry(candles, signalIndex, currentPrice, fallback) {
  return candles[signalIndex + 1]?.o ?? currentPrice ?? fallback;
}

function atrAt(candles, index, period = ENGINE_CONFIG.atrPeriod) {
  const xs = [];
  for (let i = Math.max(1, index - period + 1); i <= index; i++) {
    const c = candles[i], p = candles[i - 1];
    xs.push(Math.max(c.h - c.l, Math.abs(c.h - p.c), Math.abs(c.l - p.c)));
  }
  return avg(xs) || Math.max(1e-9, candleRange(candles[index]));
}

function resample(candles, seconds) {
  const groups = new Map();
  for (const c of candles) {
    const t = Math.floor(c.t / seconds) * seconds;
    if (!groups.has(t)) groups.set(t, []);
    groups.get(t).push(c);
  }
  return [...groups.entries()].sort((a, b) => a[0] - b[0]).map(([t, xs]) => ({
    t, o: xs[0].o, h: Math.max(...xs.map((x) => x.h)),
    l: Math.min(...xs.map((x) => x.l)), c: xs.at(-1).c,
    v: xs.some((x) => finite(x.v)) ? xs.reduce((s, x) => s + (finite(x.v) ? x.v : 0), 0) : null,
  }));
}

function buildBiasTimeline(candles) {
  const swings = detectMultiScaleSwings(candles);
  const highsByConfirm = [...swings.highs].sort((a, b) => a.confirmedIndex - b.confirmedIndex);
  const lowsByConfirm = [...swings.lows].sort((a, b) => a.confirmedIndex - b.confirmedIndex);
  const knownH = [], knownL = [], timeline = [];
  let hi = 0, li = 0;
  for (let i = 0; i < candles.length; i++) {
    while (hi < highsByConfirm.length && highsByConfirm[hi].confirmedIndex <= i) knownH.push(highsByConfirm[hi++]);
    while (li < lowsByConfirm.length && lowsByConfirm[li].confirmedIndex <= i) knownL.push(lowsByConfirm[li++]);
    const hs = knownH.slice(-2), ls = knownL.slice(-2);
    let bias = "unknown";
    if (hs.length === 2 && ls.length === 2) {
      if (hs[1].level > hs[0].level && ls[1].level > ls[0].level) bias = "bullish";
      else if (hs[1].level < hs[0].level && ls[1].level < ls[0].level) bias = "bearish";
      else bias = "range";
    }
    timeline.push(bias);
  }
  return { timeline, swings };
}

function lastClosedIndex(candles, seconds, t) {
  let lo = 0, hi = candles.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (candles[mid].t + seconds <= t) lo = mid + 1;
    else hi = mid;
  }
  return lo - 1;
}

const nyHourFormatter = new Intl.DateTimeFormat("en-US", {
  timeZone: "America/New_York", hour: "2-digit", hourCycle: "h23",
});
function killzoneAt(t) {
  const parts = nyHourFormatter.formatToParts(new Date(t * 1000));
  const hour = Number(parts.find((x) => x.type === "hour")?.value);
  if (hour >= 2 && hour < 5) return "london";
  if (hour >= 7 && hour < 10) return "new-york-am";
  if (hour >= 10 && hour < 12) return "london-close";
  return "outside";
}

function detectBosEvents(candles, swings) {
  const events = [];
  for (let i = 2; i < candles.length; i++) {
    const high = swings.highs.filter((x) => x.confirmedIndex < i).at(-1);
    const low = swings.lows.filter((x) => x.confirmedIndex < i).at(-1);
    if (high && candles[i - 1].c <= high.level && candles[i].c > high.level)
      events.push({ id: "bos-up|" + candles[i].t + "|" + high.index, direction: "bullish",
        index: i, at: candles[i].t, level: high.level, swingId: high.index });
    if (low && candles[i - 1].c >= low.level && candles[i].c < low.level)
      events.push({ id: "bos-down|" + candles[i].t + "|" + low.index, direction: "bearish",
        index: i, at: candles[i].t, level: low.level, swingId: low.index });
  }
  return events;
}

function detectSweepEvents(candles, swings, equalPools = []) {
  const events = [];
  for (let i = 2; i < candles.length; i++) {
    const high = swings.highs.filter((x) => x.confirmedIndex < i).at(-1);
    const low = swings.lows.filter((x) => x.confirmedIndex < i).at(-1);
    const c = candles[i], sweptHigh = Boolean(high && c.h > high.level && c.c < high.level);
    const sweptLow = Boolean(low && c.l < low.level && c.c > low.level);
    if (sweptHigh && sweptLow) continue;
    const add = (swing, direction, side, extreme, poolSide) => {
      const range = candleRange(c), atr = atrAt(candles, i);
      const equalPool = equalPools.find((p) => p.side === poolSide && p.knownIndex < i
        && Math.abs(p.level - swing.level) <= ENGINE_CONFIG.equalPoolToleranceAtr * atr);
      const closeInside = direction === "bearish" ? swing.level - c.c : c.c - swing.level;
      const closeAway = direction === "bearish" ? c.h - c.c : c.c - c.l;
      const closeInsideRangePct = range ? 100 * closeInside / range : 0;
      const closeAwayFromExtremePct = range ? 100 * closeAway / range : 0;
      const directionalClose = direction === "bearish" ? c.c < c.o : c.c > c.o;
      const decisiveClose = closeInsideRangePct >= ENGINE_CONFIG.turtleMinCloseInsideRangePct
        && closeAwayFromExtremePct >= ENGINE_CONFIG.turtleMinCloseAwayFromExtremePct;
      events.push({ id: "sweep-" + (side === "buy-side" ? "high" : "low") + "|" + c.t + "|" + swing.index,
        direction, side, index: i, at: c.t, level: swing.level, extreme,
        poolKind: equalPool ? (poolSide === "highs" ? "equal-highs" : "equal-lows")
          : swing.strength === 5 ? "external-swing" : "internal-swing",
        poolId: equalPool?.id ?? "swing|" + swing.kind + "|" + swing.index,
        swingStrength: swing.strength, equalPoolId: equalPool?.id ?? null,
        penetrationAtr: Number((Math.abs(extreme - swing.level) / atr).toFixed(3)),
        closeInsideRangePct: Number(closeInsideRangePct.toFixed(1)),
        closeAwayFromExtremePct: Number(closeAwayFromExtremePct.toFixed(1)),
        rejectionBodyPct: range ? Number((100 * body(c) / range).toFixed(1)) : 0,
        decisiveClose, directionalClose, decisiveRejection: decisiveClose && directionalClose });
    };
    if (sweptHigh) add(high, "bearish", "buy-side", c.h, "highs");
    if (sweptLow) add(low, "bullish", "sell-side", c.l, "lows");
  }
  return events;
}
function detectEqualPools(candles, swings) {
  const pools = [];
  const scan = (xs, side) => {
    for (let i = 1; i < xs.length; i++) {
      const a = xs[i - 1], b = xs[i], tol = ENGINE_CONFIG.equalPoolToleranceAtr * atrAt(candles, b.index);
      if (Math.abs(a.level - b.level) <= tol)
        pools.push({ id: "equal-" + side + "|" + a.index + "|" + b.index,
          side, level: (a.level + b.level) / 2, firstIndex: a.index,
          secondIndex: b.index, knownIndex: b.confirmedIndex, at: candles[b.index].t });
    }
  };
  scan(swings.highs, "highs");
  scan(swings.lows, "lows");
  return pools;
}

function volumeRatioAt(candles, index) {
  const current = candles[index]?.v;
  if (!finite(current) || current <= 0) return null;
  const prior = candles.slice(Math.max(0, index - ENGINE_CONFIG.relativeVolumeLookback), index)
    .map((c) => c.v).filter((v) => finite(v) && v > 0);
  if (prior.length < ENGINE_CONFIG.minRelativeVolumeSamples) return null;
  const mean = avg(prior);
  return mean ? current / mean : null;
}
function displacementAt(candles, index, direction) {
  const c = candles[index], prior = avg(candles.slice(Math.max(0, index - 10), index).map(body)) || body(c);
  const bodyPct = candleRange(c) ? 100 * body(c) / candleRange(c) : 0;
  const multiple = prior ? body(c) / prior : 0;
  const directional = direction === "bullish" ? c.c > c.o : c.c < c.o;
  return { directional, bodyPct, bodyMultiple: multiple,
    valid: directional && bodyPct >= ENGINE_CONFIG.minDisplacementBodyPct
      && multiple >= ENGINE_CONFIG.minDisplacementBodyMultiple };
}

function externalRangeAt(swings, index) {
  const high = swings.highs.filter((x) => x.strength === 5 && x.confirmedIndex < index).at(-1);
  const low = swings.lows.filter((x) => x.strength === 5 && x.confirmedIndex < index).at(-1);
  if (!high || !low || high.level <= low.level) return null;
  return { high: high.level, low: low.level, equilibrium: (high.level + low.level) / 2,
    highId: high.index, lowId: low.index };
}

function rangeLocation(range, price) {
  if (!range) return "unknown";
  const p = clamp((price - range.low) / (range.high - range.low));
  return p < 0.5 ? "discount" : p > 0.5 ? "premium" : "equilibrium";
}

export function isZoneOpenAt(zone, signalIndex) {
  const closedThroughIndex = zone?.lifecycle?.closedThroughIndex;
  return closedThroughIndex == null || closedThroughIndex > signalIndex;
}

export function qualifiesMssDisplacement(event, config = ENGINE_CONFIG) {
  const expansion = event?.candleExpansion;
  return Boolean(expansion?.directional)
    && finite(expansion.bodyRangePct)
    && expansion.bodyRangePct >= config.minDisplacementBodyPct
    && finite(expansion.bodyMultiple)
    && expansion.bodyMultiple >= config.minDisplacementBodyMultiple
    && Number.isInteger(event?.barsSweepToMss)
    && event.barsSweepToMss >= 0
    && event.barsSweepToMss <= config.maxBarsSweepToMss;
}

export function qualifiesMomentumContinuation({ htfAligned, displacement } = {}) {
  return Boolean(htfAligned && displacement?.valid);
}

export function isMeaningfulLiquidityRaid(sweep) {
  return ["equal-highs", "equal-lows", "external-swing"].includes(sweep?.poolKind);
}

const M15_ENABLED_MODELS = new Set([
  "fvg-mitigation",
  "premium-discount",
  "trend-continuation",
  "order-block",
  "mss-fvg",
  "ict-2022",
  "ote",
  "turtle-soup-confirmed",
  "fvg-fourth-candle-confirmed",
  "in-gap-bounce",
]);
const H1_ENABLED_MODELS = new Set([
  "fvg-mitigation",
  "premium-discount",
  "trend-continuation",
  "order-block",
]);

export function isModelEnabledForTimeframe(model, timeframe) {
  const enabled = String(timeframe).toUpperCase() === "H1"
    ? H1_ENABLED_MODELS
    : String(timeframe).toUpperCase() === "M15"
      ? M15_ENABLED_MODELS
      : null;
  return Boolean(enabled?.has(model));
}

const cleanPrice = (value) => Number(value.toFixed(12));

export function selectOteOverlap(event, zones = [], orderBlocks = [], config = ENGINE_CONFIG) {
  if (!event || !["bullish", "bearish"].includes(event.direction)) return null;
  if (![event.sweepExtreme, event.mssExtreme].every(finite)) return null;
  const leg = Math.abs(event.mssExtreme - event.sweepExtreme);
  if (!(leg > 0) || !Number.isInteger(event.index)) return null;
  const [nearPct, deepPct] = config.oteBand;
  const retracementPrice = (pct) => event.direction === "bullish"
    ? event.mssExtreme - pct * leg
    : event.mssExtreme + pct * leg;
  const near = retracementPrice(nearPct), deep = retracementPrice(deepPct);
  const oteBand = [Math.min(near, deep), Math.max(near, deep)];
  const sameLeg = (feature) => feature?.direction === event.direction
    && Number.isInteger(feature.createdIndex)
    && feature.createdIndex >= event.index
    && feature.createdIndex <= event.index + 4
    && finite(feature.lower)
    && finite(feature.upper)
    && feature.upper > feature.lower;
  const candidates = [];
  for (const zone of zones) {
    if (!sameLeg(zone) || zone.sizeQualification?.status !== "valid-size") continue;
    candidates.push({ featureType: "fvg", featureId: zone.id, createdIndex: zone.createdIndex,
      lower: zone.lower, upper: zone.upper });
  }
  for (const orderBlock of orderBlocks) {
    if (!sameLeg(orderBlock)) continue;
    candidates.push({ featureType: "order-block", featureId: orderBlock.id,
      createdIndex: orderBlock.createdIndex, lower: orderBlock.lower, upper: orderBlock.upper });
  }
  const overlaps = candidates.map((candidate) => {
    const lower = Math.max(oteBand[0], candidate.lower);
    const upper = Math.min(oteBand[1], candidate.upper);
    return upper > lower ? { ...candidate, overlap: [lower, upper], width: upper - lower } : null;
  }).filter(Boolean).sort((a, b) => {
    const priorityA = a.featureType === "order-block" ? 0 : 1;
    const priorityB = b.featureType === "order-block" ? 0 : 1;
    return priorityA - priorityB || b.width - a.width || String(a.featureId).localeCompare(String(b.featureId));
  });
  const selected = overlaps[0];
  if (!selected) return null;
  const entry = (selected.overlap[0] + selected.overlap[1]) / 2;
  const retracementPct = event.direction === "bullish"
    ? (event.mssExtreme - entry) / leg
    : (entry - event.mssExtreme) / leg;
  return {
    featureType: selected.featureType,
    featureId: selected.featureId,
    createdIndex: selected.createdIndex,
    oteBand: oteBand.map(cleanPrice),
    overlap: selected.overlap.map(cleanPrice),
    entry: cleanPrice(entry),
    retracementPct: cleanPrice(retracementPct),
  };
}

export function buildEntryChecklist(ticket) {
  const evidence = ticket?.evidence ?? {};
  const directionBias = ticket?.direction === "LONG" ? "bullish"
    : ticket?.direction === "SHORT" ? "bearish" : null;
  const alignedTimeframes = directionBias
    ? Object.entries(ticket?.htf ?? {})
      .filter(([, bias]) => bias === directionBias)
      .map(([timeframe]) => timeframe)
    : [];
  const primaryStructureAligned = directionBias != null && ticket?.primaryBias === directionBias;
  const confirmedStructureShift = finite(evidence.mssAt) || finite(evidence.mssId);
  const htfAccepted = alignedTimeframes.length > 0
    || primaryStructureAligned
    || confirmedStructureShift;
  const htfAcceptanceBasis = alignedTimeframes.length > 0 ? "higher-timeframe-trend"
    : primaryStructureAligned ? "primary-structure"
      : confirmedStructureShift ? "confirmed-structure-shift"
        : null;
  const fvgId = evidence.fvgId ?? evidence.zoneId ?? evidence.retracementFvgId
    ?? (evidence.overlapFeatureType === "fvg" ? evidence.overlapFeatureId : null);
  const orderBlockId = evidence.ob?.id
    ?? (evidence.overlapFeatureType === "order-block" ? evidence.overlapFeatureId : null);
  const structureId = evidence.bos?.id ?? evidence.sweep?.id ?? evidence.mssId
    ?? (finite(evidence.mssAt) ? String(evidence.mssAt) : null);
  const hasMappedEntryPoi = Boolean(
    fvgId || orderBlockId || structureId
    || evidence.bounds?.every(finite)
    || evidence.creationLeg?.every(finite),
  );
  const oteApplicable = ticket?.model === "ote";
  const retracementPct = evidence.retracementPct;
  const otePassed = oteApplicable
    ? finite(retracementPct)
      && retracementPct >= ENGINE_CONFIG.oteBand[0]
      && retracementPct <= ENGINE_CONFIG.oteBand[1]
      && evidence.overlap?.every(finite)
      && Boolean(evidence.overlapFeatureId)
    : null;
  const invalidationLevel = ticket?.stopEvidence?.invalidationLevel
    ?? ticket?.stopEvidence?.structuralAnchor;
  const invalidationType = ticket?.stopEvidence?.anchorType ?? null;
  const targetLevel = ticket?.targetPool?.level;
  const items = {
    htfTrendAlignment: {
      question: "Is the position aligned with the higher-timeframe trend?",
      passed: alignedTimeframes.length > 0,
      alignedTimeframes,
      accepted: htfAccepted,
      acceptanceBasis: htfAcceptanceBasis,
    },
    pointsOfInterest: {
      question: "Are the relevant POIs, order blocks, and FVGs mapped?",
      passed: hasMappedEntryPoi,
      mapped: { fvgId: fvgId ?? null, orderBlockId: orderBlockId ?? null, structureId: structureId ?? null },
    },
    oteConfluence: {
      question: "Does the entry have OTE plus model-specific confluence?",
      applicable: oteApplicable,
      passed: otePassed,
      retracementPct: finite(retracementPct) ? retracementPct : null,
      overlapFeatureId: evidence.overlapFeatureId ?? null,
    },
    liquidityObjective: {
      question: "What objective is price being drawn toward?",
      passed: finite(targetLevel),
      level: finite(targetLevel) ? targetLevel : null,
      poolId: ticket?.targetPool?.id ?? null,
      kind: ticket?.targetPool?.kind ?? null,
    },
    protectedLevel: {
      question: "Which level is unlikely to be retested while the thesis remains valid?",
      passed: finite(invalidationLevel) && Boolean(invalidationType),
      level: finite(invalidationLevel) ? invalidationLevel : null,
      type: invalidationType,
      thesis: "structural invalidation",
    },
  };
  const required = [
    items.htfTrendAlignment.accepted,
    items.pointsOfInterest.passed,
    items.liquidityObjective.passed,
    items.protectedLevel.passed,
    !oteApplicable || items.oteConfluence.passed,
  ];

  return { passed: required.every(Boolean), items };
}

export function scoreTicketQuality(ticket) {
  const evidence = ticket?.evidence ?? {};
  const tags = new Set(ticket?.tags ?? []);
  const directionBias = ticket?.direction === "LONG" ? "bullish" : "bearish";
  const alignedFromEvidence = Array.isArray(evidence.htfAligned) ? evidence.htfAligned.length : 0;
  const alignedFromTicket = Object.values(ticket?.htf ?? {}).filter((bias) => bias === directionBias).length;
  const alignedTimeframes = Math.max(alignedFromEvidence, alignedFromTicket);
  const hasSweep = finite(evidence.sweepLevel) || Boolean(evidence.sweep)
    || finite(evidence.ob?.sweepExtreme);
  const hasMss = finite(evidence.mssAt) || finite(evidence.mssId);
  const hasDelivery = Boolean(evidence.fvgId || evidence.zoneId || evidence.retracementFvgId
    || evidence.ob || evidence.creationLeg || evidence.overlapFeatureId);
  const hasStructureBreak = finite(evidence.breakLevel) || finite(evidence.mssBreakLevel)
    || Boolean(evidence.bos) || Boolean(evidence.ob?.bosId);
  const location = evidence.location ?? ticket?.rangeLocation;
  const locationAligned = ticket?.direction === "LONG" ? location === "discount" : location === "premium";
  const displacement = evidence.displacement ?? evidence.ob?.displacement;
  const targetKind = String(ticket?.targetPool?.kind ?? "");
  const targetClarity = targetKind === "htf-liquidity" ? 1.5
    : targetKind === "external-swing" ? 1
      : ticket?.targetPool ? 0.5 : 0;
  const stopInvalidation = finite(ticket?.stopEvidence?.structuralAnchor)
    && Boolean(ticket?.stopEvidence?.anchorType)
    ? 1.25 : 0;
  const freshness = tags.has("fresh") ? 0.75 : tags.has("later-touch") ? -0.25 : 0;
  const session = ["london", "new-york-am", "london-close"].includes(ticket?.killzone) ? 0.75 : 0;
  const components = {
    sequence: 0.75 * [hasSweep, hasMss, hasDelivery, hasStructureBreak].filter(Boolean).length,
    htfAlignment: 0.75 * Math.min(2, alignedTimeframes),
    location: locationAligned ? 1 : 0,
    liquidityTarget: targetClarity,
    displacement: displacement?.valid ? 1 : 0,
    freshness,
    stopInvalidation,
    session,
  };
  const score = Object.values(components).reduce((sum, value) => sum + value, 0);
  return { score: Number(score.toFixed(3)), components };
}

function activeTarget(candles, swings, direction, entry, index) {
  const source = direction === "LONG" ? swings.highs : swings.lows;
  const known = source.filter((s) => s.confirmedIndex < index
    && (direction === "LONG" ? s.level > entry : s.level < entry));
  const active = known.filter((s) => {
    for (let i = s.confirmedIndex + 1; i <= index; i++) {
      if (direction === "LONG" ? candles[i].h >= s.level : candles[i].l <= s.level) return false;
    }
    return true;
  }).sort((a, b) => direction === "LONG" ? a.level - b.level : b.level - a.level);
  const s = active[0];
  return s ? { id: "swing|" + s.kind + "|" + s.index, level: s.level,
    kind: s.strength === 5 ? "external-swing" : "internal-swing", strength: s.strength } : null;
}

function firstTouchIndex(zone, candles, start = zone.createdIndex + 1) {
  for (let i = start; i < candles.length; i++)
    if (candles[i].l <= zone.upper && candles[i].h >= zone.lower) return i;
  return null;
}


function detectOrderBlocks(candles, zones, bosEvents, sweepEvents) {
  const out = [], seen = new Set();
  for (const zone of zones) {
    if (zone.sizeQualification.status !== "valid-size") continue;
    const direction = zone.direction, disp = displacementAt(candles, zone.createdIndex - 1, direction);
    if (!disp.valid) continue;
    const bos = bosEvents.find((e) => e.direction === direction
      && e.index >= zone.createdIndex - 1 && e.index <= zone.createdIndex);
    const sweep = [...sweepEvents].reverse().find((e) => e.direction === direction
      && e.index <= zone.createdIndex && zone.createdIndex - e.index <= 96);
    if (!bos || !sweep) continue;
    let origin = null;
    for (let j = zone.createdIndex - 2; j >= Math.max(0, zone.createdIndex - 8); j--) {
      const opposite = direction === "bullish" ? candles[j].c < candles[j].o : candles[j].c > candles[j].o;
      if (opposite) { origin = j; break; }
    }
    if (origin == null) continue;
    const key = direction + "|" + origin;
    if (seen.has(key)) continue;
    seen.add(key);
    const c = candles[origin];
    out.push({ id: "ob|" + key, direction, originIndex: origin, createdIndex: zone.createdIndex,
      createdAt: zone.createdAt, lower: c.l, upper: c.h, midpoint: (c.l + c.h) / 2,
      fvgId: zone.id, bosId: bos.id, sweepId: sweep.id, sweepExtreme: sweep.extreme,
      displacement: disp });
  }
  return out;
}

function summarizeRows(rows) {
  const count = (name) => rows.filter((r) => r.outcome === name).length;
  const resolved = rows.filter((r) => finite(r.rMultiple));
  const totalR = resolved.reduce((s, r) => s + r.rMultiple, 0);
  return {
    episodes: rows.length,
    filled: rows.filter((r) => r.filledAt != null).length,
    target: count("target"), stop: count("stop"), breakeven: count("breakeven"),
    ambiguous: count("ambiguous"), invalidatedBeforeFill: count("invalidated-before-fill"),
    pending: count("pending-at-data-end"), open: count("open-at-data-end"),
    totalR: Number(totalR.toFixed(3)),
    expectancyResolved: resolved.length ? Number((totalR / resolved.length).toFixed(3)) : null,
  };
}

function grouped(rows, fn) {
  const map = new Map();
  for (const row of rows) {
    const key = fn(row) ?? "unknown";
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(row);
  }
  return Object.fromEntries([...map.entries()].sort((a, b) => a[0].localeCompare(b[0]))
    .map(([k, v]) => [k, summarizeRows(v)]));
}


const physicalTicketKey = (row) => [
  row.direction,
  row.entryType,
  row.placedIndex,
  Number(row.actualEntry ?? row.entry).toFixed(5),
  Number(row.sl).toFixed(5),
  Number(row.target).toFixed(5),
].join("|");

export function dedupePhysicalTickets(rows) {
  const map = new Map();
  for (const row of rows) {
    const key = physicalTicketKey(row);
    const existing = map.get(key);
    if (!existing) {
      const quality = finite(row.qualityScore) ? { score: row.qualityScore, components: row.qualityComponents }
        : scoreTicketQuality(row);
      map.set(key, {
        ...row,
        qualityScore: quality.score, qualityComponents: quality.components,
        physicalKey: key,
        modelAliases: [row.model],
        confluenceFamilies: [...new Set(row.confluenceFamilies ?? [])],
        tags: [...new Set(row.tags ?? [])],
      });
      continue;
    }
    if (!existing.modelAliases.includes(row.model)) existing.modelAliases.push(row.model);
    existing.confluenceFamilies = [...new Set([
      ...existing.confluenceFamilies,
      ...(row.confluenceFamilies ?? []),
    ])];
    existing.tags = [...new Set([...existing.tags, ...(row.tags ?? [])])];
    const incoming = finite(row.qualityScore) ? { score: row.qualityScore, components: row.qualityComponents }
      : scoreTicketQuality(row);
    if (incoming.score > existing.qualityScore) {
      existing.qualityScore = incoming.score;
      existing.qualityComponents = incoming.components;
    }
  }
  return [...map.values()];
}

export function buildTicketDiscoveryEngine(asset, data, nowSec = Date.now() / 1000, options = {}) {
  const timeframe = String(options.timeframe ?? "M15").toUpperCase();
  if (!["M15", "H1"].includes(timeframe)) throw new Error("timeframe must be M15 or H1");
  const primarySeconds = timeframe === "H1" ? 3600 : 900;
  const primarySource = timeframe === "H1" ? data.h1 : data.m15;
  const candles = primarySource.filter((c) => c.t + primarySeconds <= nowSec);
  const h1 = data.h1.filter((c) => c.t + 3600 <= nowSec);
  const d1 = data.d1.filter((c) => c.t + 86400 <= nowSec);
  const h4 = resample(h1, 14400).filter((c) => c.t + 14400 <= nowSec);
  const m15State = buildBiasTimeline(candles);
  const h1State = buildBiasTimeline(h1), h4State = buildBiasTimeline(h4), d1State = buildBiasTimeline(d1);
  const swings = m15State.swings;
  const registry = buildRegistry(asset, candles, h1, d1, nowSec, { timeframe, primarySeconds });
  const eligibleHtfKeys = timeframe === "H1" ? ["h4", "daily"] : ["h1", "h4", "daily"];
  const zones = registry.zones, zoneById = new Map(zones.map((z) => [z.id, z]));
  const mssEvents = registry.mssEvents;
  const bosEvents = detectBosEvents(candles, swings);
  const equalPools = detectEqualPools(candles, swings);
  const sweepEvents = detectSweepEvents(candles, swings, equalPools);
  const orderBlocks = detectOrderBlocks(candles, zones, bosEvents, sweepEvents);
  const tickets = [], ticketIds = new Set();
  const riskFor = (args) => {
    try {
      return deriveModelStop(args);
    } catch {
      return null;
    }
  };

  const htfAt = (t) => {
    const read = (state, xs, sec) => {
      const i = lastClosedIndex(xs, sec, t);
      return i < 0 ? "unknown" : state.timeline[i];
    };
    return { h1: read(h1State, h1, 3600), h4: read(h4State, h4, 14400), daily: read(d1State, d1, 86400) };
  };

  const activeMssAt = (direction, index) => {
    const t = candles[index]?.t;
    return [...mssEvents].reverse().find((e) => e.direction === direction && e.index <= index
      && qualifiesMssDisplacement(e)
      && (e.lifecycle.creationLegBrokenAt == null || e.lifecycle.creationLegBrokenAt > t)
      && (e.lifecycle.supersededAt == null || e.lifecycle.supersededAt > t)) ?? null;
  };

  const fvgContext = (zone, index, price) => {
    const direction = zone.direction, htf = htfAt(candles[index].t);
    const alignedTf = Object.entries(htf).filter(([tf, bias]) => eligibleHtfKeys.includes(tf) && bias === direction).map(([tf]) => tf);
    const primaryAligned = m15State.timeline[index] === direction;
    const m15Aligned = timeframe === "M15" ? primaryAligned : null;
    const mss = activeMssAt(direction, index);
    const range = externalRangeAt(swings, index), location = rangeLocation(range, price);
    const locationOk = direction === "bullish" ? location === "discount" : location === "premium";
    const path = zone.liquidityPathSnapshot;
    return { htf, alignedTf, primaryAligned, m15Aligned, mss, range, location, locationOk, path,
      structureOk: alignedTf.length > 0 || primaryAligned || Boolean(mss),
      liquidityOk: Boolean(path?.destinationCandidates?.length) };
  };

  const pathTarget = (zone, direction, entry, sl) => {
    const long = direction === "LONG", risk = long ? entry - sl : sl - entry;
    if (!(risk > 0)) return null;
    const selected = (zone?.liquidityPathSnapshot?.destinationCandidates ?? [])
      .filter((p) => timeframe !== "H1" || !p.type.startsWith("h1-")).find((p) => {
      const reward = long ? p.level - entry : entry - p.level;
      return reward > 0 && reward / risk >= ENGINE_CONFIG.minRR;
    });
    return selected ? { id: selected.poolId, level: selected.level, kind: "htf-liquidity",
      type: selected.type, rank: selected.rank, distanceAtr: selected.distanceAtr,
      expectationState: zone.liquidityPathSnapshot.expectationState,
      expectedReasonCodes: selected.expectedReasonCodes,
      contradictions: selected.contradictions, obstructions: selected.obstructions } : null;
  };
  const addTicket = ({ model, sourceId, direction, signalIndex, entryType = "limit",
    entry, sl, stopEvidence, targetOverride = null, evidence = {}, confluences = [], tags = [] }) => {
    if (!isModelEnabledForTimeframe(model, timeframe)) return null;
    if (signalIndex < 0 || signalIndex >= candles.length) return null;
    const actualEntry = entryType === "market"
      ? resolveMarketEntry(candles, signalIndex, options.currentPrice, entry)
      : entry;
    if (![actualEntry, sl].every(finite)) return null;
    const long = direction === "LONG";
    if (long ? sl >= actualEntry : sl <= actualEntry) return null;
    const target = targetOverride ?? activeTarget(candles, swings, direction, actualEntry, signalIndex);
    if (!target) return null;
    const risk = long ? actualEntry - sl : sl - actualEntry;
    const reward = long ? target.level - actualEntry : actualEntry - target.level;
    const rr = reward / risk;
    if (!(rr >= ENGINE_CONFIG.minRR)) return null;
    const families = [...new Set([...confluences, "liquidity"])];
    if (families.length < ENGINE_CONFIG.minIndependentConfluences) return null;
    const id = model + "|" + sourceId + "|" + direction + "|" + signalIndex + "|" + actualEntry.toFixed(5);
    if (ticketIds.has(id)) return null;
    const t = candles[signalIndex].t, htf = htfAt(t), range = externalRangeAt(swings, signalIndex);
    const ticket = { id, asset: asset.toUpperCase(), timeframe, model, sourceId, direction, entryType,
      placedIndex: signalIndex, barsSincePlacement: candles.length - 1 - signalIndex,
      placedAt: t, placedAtIso: iso(t), entry: actualEntry, sl, stopEvidence,
      target: target.level, targetPool: target, rr: Number(rr.toFixed(3)),
      evidence, confluenceFamilies: families, tags, killzone: killzoneAt(t),
      primaryBias: m15State.timeline[signalIndex],
      m15Bias: timeframe === "M15" ? m15State.timeline[signalIndex] : null, htf, dealingRange: range,
      rangeLocation: rangeLocation(range, actualEntry) };
    const entryChecklist = buildEntryChecklist(ticket);
    if (!entryChecklist.passed) return null;
    ticket.entryChecklist = entryChecklist;
    ticketIds.add(id);
    const quality = scoreTicketQuality(ticket);
    ticket.qualityScore = quality.score;
    ticket.qualityComponents = quality.components;
    tickets.push(ticket);
    return ticket;
  };
  for (const zone of zones) {
    if (zone.sizeQualification.status !== "valid-size") continue;
    const i = zone.createdIndex, direction = zone.direction === "bullish" ? "LONG" : "SHORT";
    const disp = displacementAt(candles, i - 1, zone.direction);
    if (!disp.valid) continue;
    const touch = firstTouchIndex(zone, candles);
    if (touch === i + 1) continue;
    const entry = zone.direction === "bullish" ? zone.upper : zone.lower;
    const context = fvgContext(zone, i, zone.ce);
    if (!context.structureOk || !context.liquidityOk) continue;
    const stopEvidence = riskFor({ model: "fvg-mitigation", direction, entry,
      zone, event: context.mss });
    if (!stopEvidence) continue;
    const sl = stopEvidence.price;
    const targetOverride = pathTarget(zone, direction, entry, sl);
    if (!targetOverride) continue;
    const base = { zoneId: zone.id, bounds: [zone.lower, zone.upper],
      sizeRatio: zone.sizeQualification.ratioToPriorAverage, displacement: disp,
      htfAligned: context.alignedTf, m15Aligned: context.m15Aligned,
      mssId: context.mss?.at ?? null, liquidityPathSnapshot: context.path,
      selectedLiquidityTarget: targetOverride };
    const tags = ["any-touch-after-candle-4"];
    if (touch != null) tags.push("later-touch");
    addTicket({ model: "fvg-mitigation", sourceId: zone.id, direction, signalIndex: i,
      entry, sl, stopEvidence, targetOverride, evidence: base, confluences: ["delivery", "structure"], tags });
    if (context.locationOk)
      addTicket({ model: "premium-discount", sourceId: zone.id, direction, signalIndex: i,
        entry, sl, stopEvidence, targetOverride, evidence: { ...base, location: context.location },
        confluences: ["delivery", "structure", "location"], tags });
    if (context.alignedTf.includes("h1") || context.alignedTf.includes("h4"))
      addTicket({ model: "trend-continuation", sourceId: zone.id, direction, signalIndex: i,
        entry, sl, stopEvidence, targetOverride, evidence: base, confluences: ["delivery", "structure"], tags });
  }
  for (const ob of orderBlocks) {
    const i = ob.createdIndex, direction = ob.direction === "bullish" ? "LONG" : "SHORT";
    const zone = zoneById.get(ob.fvgId);
    if (!zone) continue;
    const context = fvgContext(zone, i, ob.midpoint);
    if (!context.structureOk || !context.locationOk || !context.liquidityOk) continue;
    const stopEvidence = riskFor({ model: "order-block", direction, entry: ob.midpoint,
      orderBlock: ob, sweep: { extreme: ob.sweepExtreme } });
    if (!stopEvidence) continue;
    const sl = stopEvidence.price;
    const targetOverride = pathTarget(zone, direction, ob.midpoint, sl);
    if (!targetOverride) continue;
    addTicket({ model: "order-block", sourceId: ob.id, direction, signalIndex: i,
      entry: ob.midpoint, sl, stopEvidence, targetOverride,
      evidence: { ob, location: context.location, htfAligned: context.alignedTf,
        m15Aligned: context.m15Aligned, mssId: context.mss?.at ?? null,
        liquidityPathSnapshot: context.path, selectedLiquidityTarget: targetOverride },
      confluences: ["delivery", "structure", "location"],
      tags: ["fresh", "sweep-before-ob", "bos-caused", "htf-liquidity-target"] });
  }
  for (const event of mssEvents) {
    if (!qualifiesMssDisplacement(event)) continue;
    const direction = event.direction === "bullish" ? "LONG" : "SHORT";
    const associated = zones.find((z) => z.direction === event.direction
      && z.sizeQualification.status === "valid-size"
      && z.createdIndex >= event.index && z.createdIndex <= event.index + 4);
    if (associated) {
      const entry = event.direction === "bullish" ? associated.upper : associated.lower;
      const stopEvidence = riskFor({ model: "mss-fvg", direction, entry, event });
      if (!stopEvidence) continue;
      const sl = stopEvidence.price;
      const evidence = { mssAt: event.at, sweepAt: event.liquiditySweptAt,
        sweepLevel: event.liquidityLevel, fvgId: associated.id, breakLevel: event.breakLevel };
      addTicket({ model: "mss-fvg", sourceId: event.at + "|" + associated.id, direction,
        signalIndex: associated.createdIndex, entry, sl, stopEvidence, evidence,
        confluences: ["liquidity", "structure", "delivery"], tags: ["any-touch"] });
      addTicket({ model: "ict-2022", sourceId: event.at + "|" + associated.id, direction,
        signalIndex: associated.createdIndex, entry, sl, stopEvidence, evidence,
        confluences: ["liquidity", "structure", "delivery"], tags: ["raid-displacement-retracement"] });
    }
    const ote = selectOteOverlap(event, zones, orderBlocks);
    if (ote) {
      const entry = ote.entry;
      const stopEvidence = riskFor({ model: "ote", direction, entry, event });
      if (!stopEvidence) continue;
      const sl = stopEvidence.price;
      addTicket({ model: "ote", sourceId: `${event.at}|${ote.featureId}`, direction,
        signalIndex: ote.createdIndex,
        entry, sl, stopEvidence, evidence: { mssAt: event.at, creationLeg: [event.sweepExtreme, event.mssExtreme],
          retracementPct: ote.retracementPct, oteBand: ote.oteBand, overlap: ote.overlap,
          overlapFeatureType: ote.featureType, overlapFeatureId: ote.featureId },
        confluences: ["liquidity", "structure", "location", "delivery"],
        tags: ["mss-creation-leg", `${ote.featureType}-overlap`] });
    }
  }

  for (const sweep of sweepEvents) {
    const direction = sweep.direction === "bullish" ? "LONG" : "SHORT";
    const mss = mssEvents.find((e) => e.direction === sweep.direction
      && e.liquiditySweptAt === sweep.at && e.index >= sweep.index);
    const acceptedBeyond = mss && candles.slice(sweep.index + 1, mss.index + 1).some((c) =>
      sweep.direction === "bearish" ? c.c > sweep.extreme : c.c < sweep.extreme);
    if (!isMeaningfulLiquidityRaid(sweep) || !sweep.decisiveClose
      || !mss || !qualifiesMssDisplacement(mss) || acceptedBeyond) continue;
    const associated = zones.find((z) => z.direction === sweep.direction
      && z.sizeQualification.status === "valid-size"
      && z.createdIndex >= mss.index && z.createdIndex <= mss.index + 4);
    if (!associated) continue;
    const entry = sweep.direction === "bullish" ? associated.upper : associated.lower;
    const stopEvidence = riskFor({ model: "turtle-soup-confirmed", direction, entry, event: { sweepExtreme: sweep.extreme } });
    if (!stopEvidence) continue;
    const sl = stopEvidence.price;
    const context = fvgContext(associated, associated.createdIndex, associated.ce);
    const targetOverride = pathTarget(associated, direction, entry, sl);
    if (!context.structureOk || !context.liquidityOk || !targetOverride) continue;
    addTicket({ model: "turtle-soup-confirmed", sourceId: sweep.id + "|" + associated.id,
      direction, signalIndex: associated.createdIndex, entry, sl, stopEvidence, targetOverride,
      evidence: { sweep, mssAt: mss.at, mssBreakLevel: mss.breakLevel,
        retracementFvgId: associated.id, htfAligned: context.alignedTf,
        liquidityPathSnapshot: context.path, selectedLiquidityTarget: targetOverride,
        execution: "mss-displacement-then-fvg-retracement" },
      confluences: ["liquidity", "structure", "delivery"],
      tags: ["meaningful-liquidity-raid", "close-back-inside", "mss-confirmed", "retracement-entry"] });
  }
  for (const bos of bosEvents) {
    const direction = bos.direction === "bullish" ? "LONG" : "SHORT";
    const knownOpposite = (bos.direction === "bullish" ? swings.lows : swings.highs)
      .filter((s) => s.confirmedIndex < bos.index).at(-1);
    if (!knownOpposite) continue;
    const marketEntry = resolveMarketEntry(candles, bos.index, options.currentPrice, candles[bos.index].c);
    const stopEvidence = riskFor({ model: "momentum-bos", direction, entry: marketEntry, opposingSwing: knownOpposite });
    if (!stopEvidence) continue;
    const sl = stopEvidence.price;
    const disp = displacementAt(candles, bos.index, bos.direction);
    const htf = htfAt(bos.at), aligned = eligibleHtfKeys.some((tf) => htf[tf] === bos.direction);
    const vr = volumeRatioAt(candles, bos.index);
    if (qualifiesMomentumContinuation({ htfAligned: aligned, displacement: disp })
      && finite(vr) && vr >= ENGINE_CONFIG.volumeExpansionRatio)
      addTicket({ model: "volume-continuation", sourceId: bos.id, direction, signalIndex: bos.index,
        entryType: "market", entry: marketEntry, sl, stopEvidence,
        evidence: { bos, htf, volumeRatio: Number(vr.toFixed(2)), displacement: disp },
        confluences: ["structure", "delivery", "participation"], tags: ["relative-volume-only"] });
  }


  for (const zone of zones.filter((z) => z.sizeQualification.status === "valid-size")) {
    const i = firstTouchIndex(zone, candles);
    if (i == null || !isZoneOpenAt(zone, i)) continue;
    const c = candles[i], closesInside = c.c >= zone.lower && c.c <= zone.upper;
    if (!closesInside) continue;
    const direction = zone.direction === "bullish" ? "LONG" : "SHORT";
    const context = fvgContext(zone, i, zone.ce);
    if (!context.structureOk || !context.liquidityOk) continue;
    const actualEntry = resolveMarketEntry(candles, i, options.currentPrice, c.c);
    const fourth = i === zone.createdIndex + 1;
    const model = fourth ? "fvg-fourth-candle-confirmed" : "in-gap-bounce";
    const stopEvidence = riskFor({ model, direction, entry: actualEntry, zone, event: context.mss });
    if (!stopEvidence) continue;
    const sl = stopEvidence.price;
    const targetOverride = pathTarget(zone, direction, actualEntry, sl);
    if (!targetOverride) continue;
    addTicket({ model,
      sourceId: zone.id, direction, signalIndex: i, entryType: "market", entry: actualEntry, sl, stopEvidence,
      targetOverride, evidence: { fvgId: zone.id, touchAt: c.t, closeInside: true,
        htfAligned: context.alignedTf, m15Aligned: context.m15Aligned,
        mssId: context.mss?.at ?? null, liquidityPathSnapshot: context.path,
        selectedLiquidityTarget: targetOverride },
      confluences: ["delivery", "structure"], tags: fourth
        ? ["fourth-candle-close-inside", "entry-next-open", "htf-liquidity-target"]
        : ["later-touch", "close-inside", "entry-next-open", "htf-liquidity-target"] });
  }
  const managed = tickets.map((t) => simulateTicket(t, candles, ENGINE_CONFIG.riskPolicy));
  const baseline = tickets.map((t) => simulateTicket(t, candles,
    { moveStopToBreakevenAtR: null, breakevenEffective: "disabled" }));
  const uniqueManaged = dedupePhysicalTickets(managed), uniqueBaseline = dedupePhysicalTickets(baseline);
  const baselineByPhysicalKey = new Map(uniqueBaseline.map((r) => [r.physicalKey, r]));
  const beComparison = {
    managed: summarizeRows(uniqueManaged),
    unmanaged: summarizeRows(uniqueBaseline),
    stoppedToBreakeven: uniqueManaged.filter((r) => r.outcome === "breakeven"
      && baselineByPhysicalKey.get(r.physicalKey)?.outcome === "stop").length,
    laterTargetsCutToBreakeven: uniqueManaged.filter((r) => r.outcome === "breakeven"
      && baselineByPhysicalKey.get(r.physicalKey)?.outcome === "target").length,
    unchangedStops: uniqueManaged.filter((r) => r.outcome === "stop"
      && baselineByPhysicalKey.get(r.physicalKey)?.outcome === "stop").length,
  };
  const fourthCandle = uniqueManaged.filter((r) => r.tags.includes("fourth-candle-close-inside"));
  const volumeBars = candles.filter((c) => finite(c.v) && c.v > 0).length;
  const volumeAvailability = { available: volumeBars >= ENGINE_CONFIG.minRelativeVolumeSamples,
    barsWithVolume: volumeBars, totalBars: candles.length,
    coveragePct: candles.length ? Number((100 * volumeBars / candles.length).toFixed(1)) : 0,
    definition: "current positive candle volume divided by mean positive volume of the prior 20 " + timeframe + " candles",
    deltaAvailable: false };

  return {
    schemaVersion: 1,
    engine: "TU-TDE",
    generatedAt: new Date().toISOString(),
    asset: asset.toUpperCase(), timeframe, primarySeconds,
    coverage: { from: iso(candles[0]?.t), to: iso(candles.at(-1)?.t), candles: candles.length },
    config: ENGINE_CONFIG,
    detectors: {
      fvgs: zones.length,
      validFvgs: zones.filter((z) => z.sizeQualification.status === "valid-size").length,
      orderBlocks: orderBlocks.length,
      swingHighs: swings.highs.length, swingLows: swings.lows.length,
      equalPools: equalPools.length, sweeps: sweepEvents.length, bos: bosEvents.length,
      mss: mssEvents.length,
      volumeBars, volumeCoveragePct: volumeAvailability.coveragePct,
      relativeVolumeExpandedBos: managed.filter((r) => r.model === "volume-continuation").length,
      chochConfirmed: mssEvents.filter((e) => e.lifecycle.status === "choch-confirmed").length,
    },
    modelCohortEpisodes: managed.length,
    uniquePhysicalEpisodes: uniqueManaged.length,
    totals: summarizeRows(uniqueManaged),
    byModel: grouped(managed, (r) => r.model),
    byKillzone: grouped(managed, (r) => r.killzone),
    fourthCandlePolicy: "candle-4-close-inside-then-candle-5-open",
    fourthCandle: summarizeRows(fourthCandle),
    volumeAvailability,
    breakevenComparison: beComparison,
    tickets: uniqueManaged,
  };
}



const MODEL_LABELS = Object.freeze({
  "fvg-mitigation": "FVG mitigation",
  "premium-discount": "Premium/discount reversal",
  "trend-continuation": "Trend continuation",
  "order-block": "Order block",
  "mss-fvg": "MSS + FVG",
  "ict-2022": "ICT 2022 model",
  ote: "OTE retracement",
  "choch-continuation": "CHOCH continuation",
  "turtle-soup-confirmed": "Confirmed Turtle Soup",
  "momentum-bos": "Momentum BOS",
  "volume-continuation": "Relative-volume continuation",
  "fvg-fourth-candle-confirmed": "Fourth-candle FVG confirmation",
  "in-gap-bounce": "In-gap bounce",
});

const modelLabel = (model) => MODEL_LABELS[model] ?? String(model || "Deterministic setup");
const displayType = (value) => String(value || "liquidity").split("-").map((word) => /^(h1|h4|d1|fvg|mss|bos|ote)$/i.test(word) ? word.toUpperCase() : word.toLowerCase()).join(" ");

export function selectActionableTickets(tickets, { price = null } = {}) {
  const distance = (ticket) => finite(price) ? Math.abs(ticket.entry - price) : 0;
  const quality = (ticket) => finite(ticket.qualityScore)
    ? ticket.qualityScore : scoreTicketQuality(ticket).score;
  return tickets.filter((ticket) => {
    if (ticket.outcome !== "pending-at-data-end") return false;
    if (!Number.isInteger(ticket.barsSincePlacement)) return true;
    const barsPerHour = ticket.timeframe === "H1" ? 1 : 4;
    return ticket.barsSincePlacement <= ENGINE_CONFIG.pendingOrderLifetimeMarketHours * barsPerHour;
  }).sort((a, b) => quality(b) - quality(a)
      || b.placedAt - a.placedAt
      || distance(a) - distance(b)
      || b.rr - a.rr
      || a.id.localeCompare(b.id));
}

export function adaptDiscoveredTicket(ticket, { price, atrDaily, round = (value) => value } = {}) {
  const families = [...new Set(ticket.confluenceFamilies ?? [])];
  const evidence = ticket.evidence ?? {};
  const bounds = evidence.bounds ?? (evidence.ob ? [evidence.ob.lower, evidence.ob.upper] : null);
  const fvgId = evidence.fvgId ?? evidence.zoneId ?? evidence.retracementFvgId ?? null;
  const sourceParts = [];
  if (fvgId) sourceParts.push("FVG delivery");
  if (bounds?.every(finite)) sourceParts.push(`zone ${round(bounds[0])}-${round(bounds[1])}`);
  if (finite(evidence.sweepLevel)) sourceParts.push(`liquidity raid ${round(evidence.sweepLevel)}`);
  if (finite(evidence.mssAt)) sourceParts.push(`MSS ${iso(evidence.mssAt)}`);
  if (evidence.ob) sourceParts.push("order block");
  if (evidence.creationLeg?.every(finite)) sourceParts.push(`creation leg ${round(evidence.creationLeg[0])}-${round(evidence.creationLeg[1])}`);
  const basis = sourceParts.length ? sourceParts.join("; ") : "deterministic chart evidence";
  const targetLabel = ticket.targetPool?.type
    ? displayType(ticket.targetPool.type)
    : ticket.targetPool?.kind?.endsWith("swing")
      ? `${displayType(ticket.targetPool.kind)} ${ticket.direction === "LONG" ? "high" : "low"}`
      : "evidence-backed liquidity target";
  const entryLabel = ticket.entryType === "market"
    ? "at market"
    : bounds?.every(finite)
      ? `${modelLabel(ticket.model)} zone ${round(bounds[0])}-${round(bounds[1])}`
      : `${modelLabel(ticket.model)} entry`;
  const directionWord = ticket.direction === "LONG" ? "below" : "above";
  const stopEvidence = ticket.stopEvidence;
  const anchorLabel = String(stopEvidence?.anchorType ?? "structural-evidence-anchor").replaceAll("-", " ");
  const stopReason = finite(stopEvidence?.structuralAnchor)
    ? `stop is the ${anchorLabel} invalidation at ${round(stopEvidence.structuralAnchor)}`
    : "stop is beyond the structural evidence anchor";
  const stars = Math.max(1, Math.min(5, 1 + families.length));
  const fromPricePctAtr = finite(price) && finite(atrDaily) && atrDaily > 0
    ? Math.round((Math.abs(ticket.entry - price) / atrDaily) * 100)
    : 0;

  return {
    engineTicketId: ticket.id,
    setup: modelLabel(ticket.model),
    model: ticket.model,
    direction: ticket.direction,
    entryType: ticket.entryType,
    entry: round(ticket.entry),
    sl: round(ticket.sl),
    tp1: round(ticket.target),
    tp2: null,
    entryLabel,
    tp1Label: targetLabel,
    tp2Label: null,
    rr: Number(ticket.rr.toFixed(1)),
    stars,
    validSince: ticket.placedAt,
    validSinceNote: `${modelLabel(ticket.model)} completed on the ${ticket.timeframe ?? "primary"} close`,
    validSinceLocal: null,
    formingSince: evidence.sweepAt ?? evidence.sweep?.at ?? null,
    formingSinceLocal: null,
    fromPricePctAtr,
    swept: finite(evidence.sweepLevel) || Boolean(evidence.sweep),
    sweepLevel: evidence.sweepLevel ?? evidence.sweep?.level ?? null,
    sweepLabel: evidence.sweep ? "liquidity raid" : null,
    confluenceFamilies: families,
    whyEntry: `${modelLabel(ticket.model)} qualified from ${basis}; independent evidence: ${families.join(", ")}; target: ${targetLabel} ${round(ticket.target)}.`,
    whySL: `structurally invalidated ${directionWord} entry at ${round(ticket.sl)}; ${stopReason}.`,
  };
}
