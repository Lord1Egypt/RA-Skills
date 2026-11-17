export const REGISTRY_CONFIG = Object.freeze({
  minFvgSizeRatio: 0.60,
  minBaselineSamples: 20,
  swingStrengths: [3, 5],
  minIndependentConfluences: 2,
});

const clamp = (x) => Math.max(0, Math.min(1, x));
const iso = (t) => t == null ? null : new Date(t * 1000).toISOString();
const avg = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null;
const body = (c) => Math.abs(c.c - c.o);
const range = (c) => Math.max(0, c.h - c.l);

function killzoneAt(t) {
  if (t == null) return null;
  const parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", hour: "2-digit", hourCycle: "h23" }).formatToParts(new Date(t * 1000));
  const hour = Number(parts.find((p) => p.type === "hour")?.value);
  if (hour >= 2 && hour < 5) return "london";
  if (hour >= 7 && hour < 10) return "new-york-am";
  if (hour >= 10 && hour < 12) return "london-close";
  if (hour >= 20) return "asia";
  return "outside";
}

function atrAt(candles, index, period = 14) {
  const xs = [];
  for (let i = Math.max(1, index - period + 1); i <= index; i++) {
    const c = candles[i], p = candles[i - 1];
    xs.push(Math.max(c.h - c.l, Math.abs(c.h - p.c), Math.abs(c.l - p.c)));
  }
  return avg(xs) || Math.max(1e-9, range(candles[index]));
}

function candleExpansionAt(candles, index, direction) {
  const c = candles[index];
  const priorBody = avg(candles.slice(Math.max(0, index - 10), index).map(body)) || body(c);
  return {
    directional: direction === "bullish" ? c.c > c.o : c.c < c.o,
    bodyRangePct: Number((range(c) ? 100 * body(c) / range(c) : 0).toFixed(1)),
    bodyMultiple: Number((priorBody ? body(c) / priorBody : 0).toFixed(2)),
  };
}

export function detectSwings(candles, wing = 2) {
  const highs = [], lows = [], strength = wing * 2 + 1;
  for (let i = wing; i + wing < candles.length; i++) {
    const left = candles.slice(i - wing, i), right = candles.slice(i + 1, i + wing + 1);
    if (left.every((c) => candles[i].h > c.h) && right.every((c) => candles[i].h >= c.h))
      highs.push({ kind: "high", strength, level: candles[i].h, index: i, confirmedIndex: i + wing, t: candles[i].t });
    if (left.every((c) => candles[i].l < c.l) && right.every((c) => candles[i].l <= c.l))
      lows.push({ kind: "low", strength, level: candles[i].l, index: i, confirmedIndex: i + wing, t: candles[i].t });
  }
  return { highs, lows };
}

export function detectMultiScaleSwings(candles) {
  const merge = (kind) => {
    const map = new Map();
    for (const wing of [1, 2]) for (const s of detectSwings(candles, wing)[kind]) {
      const old = map.get(s.index);
      if (!old || s.strength > old.strength) map.set(s.index, s);
    }
    return [...map.values()].sort((a, b) => a.index - b.index);
  };
  return { highs: merge("highs"), lows: merge("lows") };
}

function resolveMssLifecycle(event, events, candles) {
  const legSize = Math.abs(event.mssExtreme - event.sweepExtreme);
  let wickIndex = null, acceptedIndex = null, chochIndex = null, brokenIndex = null, supersededIndex = null;
  let maxRetracement = 0;
  const nextEvent = events.find((x) => x.index > event.index);
  if (event.chochBrokenAtMss) chochIndex = event.index;
  for (let i = event.index + 1; i < candles.length && chochIndex == null && brokenIndex == null; i++) {
    const c = candles[i];
    const retracement = event.direction === "bullish"
      ? (event.mssExtreme - c.l) / legSize : (c.h - event.mssExtreme) / legSize;
    maxRetracement = Math.max(maxRetracement, clamp(retracement));
    if (wickIndex == null && (event.direction === "bullish" ? c.h > event.mssExtreme : c.l < event.mssExtreme)) wickIndex = i;
    if (acceptedIndex == null && (event.direction === "bullish" ? c.c > event.mssExtreme : c.c < event.mssExtreme)) acceptedIndex = i;
    if (event.chochTarget != null && (event.direction === "bullish" ? c.c > event.chochTarget : c.c < event.chochTarget)) {
      chochIndex = i; break;
    }
    if (event.direction === "bullish" ? c.c < event.sweepExtreme : c.c > event.sweepExtreme) {
      brokenIndex = i; break;
    }
    if (nextEvent && nextEvent.index === i && acceptedIndex == null) { supersededIndex = i; break; }
  }
  const status = chochIndex != null ? "choch-confirmed"
    : brokenIndex != null ? "failed-creation-leg"
    : supersededIndex != null ? "superseded"
    : acceptedIndex != null ? "mss-accepted-awaiting-choch"
    : wickIndex != null ? "wick-continuation-only" : "unresolved";
  const at = (i) => i == null ? null : candles[i].t;
  return {
    status,
    firstContinuationWickAt: at(wickIndex),
    firstContinuationCloseAt: at(acceptedIndex),
    chochConfirmedAt: at(chochIndex),
    creationLegBrokenAt: at(brokenIndex),
    supersededAt: at(supersededIndex),
    barsMssToFirstWick: wickIndex == null ? null : wickIndex - event.index,
    barsMssToFirstClose: acceptedIndex == null ? null : acceptedIndex - event.index,
    barsMssToChoch: chochIndex == null ? null : chochIndex - event.index,
    maxRetracementPct: Number((100 * maxRetracement).toFixed(1)),
    userBand60to70Touched: maxRetracement >= 0.60,
    oteBand62to79Touched: maxRetracement >= 0.62,
    extendedBeyond79: maxRetracement > 0.79,
    creationLegIntact: brokenIndex == null,
    firstWickKillzone: killzoneAt(at(wickIndex)),
    firstCloseKillzone: killzoneAt(at(acceptedIndex)),
    chochKillzone: killzoneAt(at(chochIndex)),
    legBreakKillzone: killzoneAt(at(brokenIndex)),
  };
}
export function detectMssEvents(candles) {
  const swings = detectMultiScaleSwings(candles), events = [];
  let sweptHigh = null, sweptLow = null;
  for (let i = 5; i < candles.length; i++) {
    const known = (xs) => xs.filter((s) => s.confirmedIndex < i).at(-1);
    const lastHigh = known(swings.highs), lastLow = known(swings.lows);
    if (lastHigh && candles[i].h > lastHigh.level)
      sweptHigh = { at: candles[i].t, index: i, level: lastHigh.level, extreme: candles[i].h, close: candles[i].c, swingStrength: lastHigh.strength };
    if (lastLow && candles[i].l < lastLow.level)
      sweptLow = { at: candles[i].t, index: i, level: lastLow.level, extreme: candles[i].l, close: candles[i].c, swingStrength: lastLow.strength };
    const expansionDown = candleExpansionAt(candles, i, "bearish");
    const expansionUp = candleExpansionAt(candles, i, "bullish");
    if (sweptHigh && lastLow && candles[i].c < lastLow.level && expansionDown.directional) {
      const external = swings.lows.filter((x) => x.strength === 5 && x.confirmedIndex < i && x.level < lastLow.level).at(-1);
      events.push({ direction: "bearish", at: candles[i].t, index: i, breakLevel: lastLow.level,
        breakSwingStrength: lastLow.strength, mssExtreme: candles[i].l,
        chochTarget: external?.level ?? null,
        chochBrokenAtMss: external ? candles[i].c < external.level : false,
        liquiditySweptAt: sweptHigh.at, liquiditySweptIndex: sweptHigh.index,
        liquidityLevel: sweptHigh.level, sweepExtreme: sweptHigh.extreme,
        sweepType: sweptHigh.close < sweptHigh.level ? "wick-sweep-rejection" : "close-through-sweep",
        sweepSwingStrength: sweptHigh.swingStrength, sweepKillzone: killzoneAt(sweptHigh.at),
        mssKillzone: killzoneAt(candles[i].t), barsSweepToMss: i - sweptHigh.index,
        candleExpansion: expansionDown });
      sweptHigh = null;
    }
    if (sweptLow && lastHigh && candles[i].c > lastHigh.level && expansionUp.directional) {
      const external = swings.highs.filter((x) => x.strength === 5 && x.confirmedIndex < i && x.level > lastHigh.level).at(-1);
      events.push({ direction: "bullish", at: candles[i].t, index: i, breakLevel: lastHigh.level,
        breakSwingStrength: lastHigh.strength, mssExtreme: candles[i].h,
        chochTarget: external?.level ?? null,
        chochBrokenAtMss: external ? candles[i].c > external.level : false,
        liquiditySweptAt: sweptLow.at, liquiditySweptIndex: sweptLow.index,
        liquidityLevel: sweptLow.level, sweepExtreme: sweptLow.extreme,
        sweepType: sweptLow.close > sweptLow.level ? "wick-sweep-rejection" : "close-through-sweep",
        sweepSwingStrength: sweptLow.swingStrength, sweepKillzone: killzoneAt(sweptLow.at),
        mssKillzone: killzoneAt(candles[i].t), barsSweepToMss: i - sweptLow.index,
        candleExpansion: expansionUp });
      sweptLow = null;
    }
  }
  for (const event of events) event.lifecycle = resolveMssLifecycle(event, events, candles);
  return events;
}

export function qualifyFvgSizes(zones, config = REGISTRY_CONFIG) {
  const baseline = [];
  for (const zone of zones) {
    const mean = avg(baseline);
    const ratio = mean ? zone.size / mean : null;
    const calibrated = baseline.length >= config.minBaselineSamples;
    const status = !calibrated ? "calibrating"
      : ratio < config.minFvgSizeRatio ? "invalid-size" : "valid-size";
    zone.sizeQualification = {
      status, mutable: true, ratioToPriorAverage: ratio == null ? null : Number(ratio.toFixed(3)),
      priorAverageSize: mean == null ? null : Number(mean.toFixed(6)),
      priorBaselineSamples: baseline.length,
      minValidRatio: config.minFvgSizeRatio,
    };
    zone.checklist = {
      status,
      validBySize: status === "valid-size",
      reason: status === "invalid-size" ? "FVG size is below 60% of causal prior-FVG average"
        : status === "calibrating" ? "fewer than 20 causal baseline FVGs" : null,
    };
    baseline.push(zone.size);
  }
  return zones;
}

export function detectFvgs(candles, maxAdjacentSpacingSeconds = 1800) {
  const out = [];
  for (let i = 2; i < candles.length; i++) {
    const a = candles[i - 2], b = candles[i - 1], c = candles[i];
    if (b.t - a.t > maxAdjacentSpacingSeconds || c.t - b.t > maxAdjacentSpacingSeconds) continue;
    let direction, lower, upper;
    if (c.l > a.h) { direction = "bullish"; lower = a.h; upper = c.l; }
    else if (c.h < a.l) { direction = "bearish"; lower = c.h; upper = a.l; }
    else continue;
    const atr = atrAt(candles, i);
    out.push({
      id: [direction, a.t, b.t, c.t, lower, upper].join("|"),
      direction, createdIndex: i, createdAt: c.t,
      candle1At: a.t, displacementAt: b.t, candle3At: c.t,
      lower, upper, ce: (lower + upper) / 2, size: upper - lower,
      sizeAtr: Number(((upper - lower) / atr).toFixed(3)), atrAtCreation: atr,
      candleExpansion: candleExpansionAt(candles, i - 1, direction),
    });
  }
  return qualifyFvgSizes(out);
}

function lifecycle(zone, candles) {
  let firstTouchIndex = null, touchCount = 0, maxRebalance = 0, ceIndex = null;
  let firstTouchRebalance = null;
  let fullIndex = null, closedThroughIndex = null, inverseConfirmedIndex = null, inverseFailedIndex = null;
  for (let i = zone.createdIndex + 1; i < candles.length; i++) {
    const c = candles[i], touched = c.l <= zone.upper && c.h >= zone.lower;
    if (touched) {
      touchCount++; firstTouchIndex ??= i;
      const p = zone.direction === "bullish" ? (zone.upper - Math.min(zone.upper, c.l)) / zone.size
        : (Math.max(zone.lower, c.h) - zone.lower) / zone.size;
      firstTouchRebalance ??= clamp(p);
      maxRebalance = Math.max(maxRebalance, clamp(p));
    }
    if (ceIndex == null && (zone.direction === "bullish" ? c.l <= zone.ce : c.h >= zone.ce)) ceIndex = i;
    if (fullIndex == null && (zone.direction === "bullish" ? c.l <= zone.lower : c.h >= zone.upper)) fullIndex = i;
    if (closedThroughIndex == null && (zone.direction === "bullish" ? c.c < zone.lower : c.c > zone.upper)) {
      closedThroughIndex = i; continue;
    }
    if (closedThroughIndex != null && i > closedThroughIndex && inverseConfirmedIndex == null) {
      const retested = zone.direction === "bullish" ? c.h >= zone.lower : c.l <= zone.upper;
      const respected = zone.direction === "bullish" ? c.c < zone.lower : c.c > zone.upper;
      if (retested && respected) inverseConfirmedIndex = i;
    }
    if (inverseConfirmedIndex != null && i > inverseConfirmedIndex && inverseFailedIndex == null)
      if (zone.direction === "bullish" ? c.c > zone.upper : c.c < zone.lower) inverseFailedIndex = i;
  }
  const at = (i) => i == null ? null : candles[i].t;
  return {
    firstTouchAt: at(firstTouchIndex), firstTouchIndex,
    firstTouchCandleNumber: firstTouchIndex == null ? null : 3 + firstTouchIndex - zone.createdIndex,
    firstTouchRebalancePct: firstTouchRebalance == null ? null : Number((100 * firstTouchRebalance).toFixed(1)),
    touchCount, maximumRebalancePct: Number((100 * maxRebalance).toFixed(1)),
    ceReachedAt: at(ceIndex), fullyRebalancedAt: at(fullIndex), closedThroughAt: at(closedThroughIndex),
    inversionConfirmedAt: at(inverseConfirmedIndex), inversionFailedAt: at(inverseFailedIndex),
    closedThroughIndex,
    geometryState: closedThroughIndex != null ? "closed-through" : fullIndex != null ? "fully-rebalanced"
      : ceIndex != null ? "ce-reached" : firstTouchIndex != null ? "partially-rebalanced" : "open",
    inversionState: inverseFailedIndex != null ? "inverse-failed" : inverseConfirmedIndex != null
      ? "inverse-confirmed" : closedThroughIndex != null ? "potential-inversion" : "none",
  };
}

function anyTouchActivation(zone, candles) {
  const i = zone.lifecycle.firstTouchIndex;
  const triggerBoundary = zone.direction === "bullish" ? zone.upper : zone.lower;
  if (i == null) return {
    rule: "any-fvg-touch", activated: false, ticketState: "not-activated",
    eligibleBySize: zone.sizeQualification.status === "valid-size",
    activatedAt: null, activatedAtIso: null, triggerBoundary,
    ceRequired: false, ceReachedAtActivation: false,
  };
  const candle = candles[i], eligibleBySize = zone.sizeQualification.status === "valid-size";
  return {
    rule: "any-fvg-touch",
    activated: true,
    ticketState: eligibleBySize ? "activated-size-valid" : "activated-observation-only",
    eligibleBySize,
    activatedAt: candle.t,
    activatedAtIso: iso(candle.t),
    activationCandleNumber: zone.lifecycle.firstTouchCandleNumber,
    triggerBoundary,
    firstTouchRebalancePct: zone.lifecycle.firstTouchRebalancePct,
    ceRequired: false,
    ceReachedAtActivation: zone.direction === "bullish" ? candle.l <= zone.ce : candle.h >= zone.ce,
    note: "Any overlap with the FVG activates the opportunity; CE remains lifecycle evidence only.",
  };
}

function surroundingMap(zone, zones) {
  const known = zones.filter((z) => z.createdIndex < zone.createdIndex
    && (z.lifecycle.closedThroughIndex == null || z.lifecycle.closedThroughIndex > zone.createdIndex));
  const describe = (z) => ({ id: z.id, direction: z.direction, ce: z.ce,
    distanceAtr: Number((Math.abs(z.ce - zone.ce) / zone.atrAtCreation).toFixed(2)) });
  const above = known.filter((z) => z.ce > zone.ce).sort((a, b) => a.ce - b.ce);
  const below = known.filter((z) => z.ce < zone.ce).sort((a, b) => b.ce - a.ce);
  const side = (xs) => ({ bullish: xs.filter((z) => z.direction === "bullish").length,
    bearish: xs.filter((z) => z.direction === "bearish").length, nearest: xs.slice(0, 3).map(describe) });
  return { above: side(above), below: side(below) };
}

function resample(candles, seconds) {
  const groups = new Map();
  for (const c of candles) {
    const t = Math.floor(c.t / seconds) * seconds;
    if (!groups.has(t)) groups.set(t, []);
    groups.get(t).push(c);
  }
  return [...groups.entries()].sort((a, b) => a[0] - b[0]).map(([t, xs]) => ({
    t, o: xs[0].o, h: Math.max(...xs.map((x) => x.h)), l: Math.min(...xs.map((x) => x.l)), c: xs.at(-1).c,
  }));
}

function weekStart(t) {
  const d = new Date(t * 1000), day = (d.getUTCDay() + 6) % 7;
  return Math.floor((Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()) / 1000 - day * 86400) / 604800) * 604800;
}

function addLiquiditySeries(levels, candles, prefix, toleranceAtr) {
  if (candles.length < 5) return;
  const swings = detectSwings(candles, 2), highs = swings.highs.slice(-20), lows = swings.lows.slice(-20);
  levels.push(...highs.map((s) => ({ type: prefix + "-swing-high", side: "above", level: s.level, formedAt: s.t })));
  levels.push(...lows.map((s) => ({ type: prefix + "-swing-low", side: "below", level: s.level, formedAt: s.t })));
  const equal = (xs, type, side) => {
    for (let i = xs.length - 1; i > 0; i--) for (let j = i - 1; j >= 0; j--) {
      if (Math.abs(xs[i].level - xs[j].level) <= toleranceAtr) {
        levels.push({ type, side, level: (xs[i].level + xs[j].level) / 2, formedAt: xs[i].t }); return;
      }
    }
  };
  equal(highs, prefix + "-equal-highs", "above");
  equal(lows, prefix + "-equal-lows", "below");
}

function structureBias(candles) {
  const swings = detectSwings(candles, 2), hs = swings.highs.slice(-2), ls = swings.lows.slice(-2);
  if (hs.length < 2 || ls.length < 2) return "unknown";
  if (hs[1].level > hs[0].level && ls[1].level > ls[0].level) return "bullish";
  if (hs[1].level < hs[0].level && ls[1].level < ls[0].level) return "bearish";
  return "range";
}
function liquidityAt(zone, h1, d1) {
  const knownH1 = h1.filter((c) => c.t + 3600 <= zone.createdAt);
  const knownH4 = resample(knownH1, 14400).filter((c) => c.t + 14400 <= zone.createdAt);
  const knownD = d1.filter((c) => c.t + 86400 <= zone.createdAt);
  const h1Atr = knownH1.length > 2 ? atrAt(knownH1, knownH1.length - 1) : zone.atrAtCreation;
  const levels = [];
  addLiquiditySeries(levels, knownH1, "h1", 0.1 * h1Atr);
  addLiquiditySeries(levels, knownH4, "h4", 0.2 * h1Atr);
  addLiquiditySeries(levels, knownD, "daily", 0.5 * h1Atr);
  const pd = knownD.at(-1);
  if (pd) {
    levels.push({ type: "previous-day-high", side: "above", level: pd.h, formedAt: pd.t });
    levels.push({ type: "previous-day-low", side: "below", level: pd.l, formedAt: pd.t });
  }
  const currentWeek = weekStart(zone.createdAt), previousWeek = knownD.filter((c) => weekStart(c.t) === currentWeek - 604800);
  if (previousWeek.length) {
    levels.push({ type: "previous-week-high", side: "above", level: Math.max(...previousWeek.map((c) => c.h)), formedAt: previousWeek.at(-1).t });
    levels.push({ type: "previous-week-low", side: "below", level: Math.min(...previousWeek.map((c) => c.l)), formedAt: previousWeek.at(-1).t });
  }
  const dedupe = (xs) => {
    const out = [];
    for (const x of xs) if (!out.some((y) => y.type === x.type && Math.abs(y.level - x.level) <= 0.01 * h1Atr)) out.push(x);
    return out.slice(0, 8).map((x) => ({ ...x,
      relativeSide: x.level > zone.ce ? "above" : "below",
      distanceAtr: Number((Math.abs(x.level - zone.ce) / h1Atr).toFixed(2)) }));
  };
  const structure = { h1: structureBias(knownH1), h4: structureBias(knownH4), daily: structureBias(knownD) };
  const alignedTimeframes = Object.entries(structure).filter(([, bias]) => bias === zone.direction).map(([tf]) => tf);
  const conflictingTimeframes = Object.entries(structure).filter(([, bias]) => bias !== "unknown" && bias !== "range" && bias !== zone.direction).map(([tf]) => tf);
  return {
    above: dedupe(levels.filter((x) => x.level > zone.ce).sort((a, b) => a.level - b.level)),
    below: dedupe(levels.filter((x) => x.level < zone.ce).sort((a, b) => b.level - a.level)),
    structure,
    alignment: { alignedTimeframes, conflictingTimeframes, alignedCount: alignedTimeframes.length,
      conflictCount: conflictingTimeframes.length, anyAligned: alignedTimeframes.length > 0 },
    note: "H1/H4/D liquidity and structure snapshot; no draw direction inferred",
  };
}

function liquidityPathSnapshot(zone, map, surrounding) {
  const side = zone.direction === "bullish" ? "above" : "below";
  const opposingDirection = zone.direction === "bullish" ? "bearish" : "bullish";
  const candidates = map[side].map((pool, index) => {
    const lo = Math.min(zone.ce, pool.level), hi = Math.max(zone.ce, pool.level);
    const obstructions = [...surrounding.above.nearest, ...surrounding.below.nearest]
      .filter((fvg) => fvg.direction === opposingDirection && fvg.ce > lo && fvg.ce < hi)
      .map((fvg) => ({ kind: "opposing-fvg", id: fvg.id, ce: fvg.ce }));
    const expectedReasonCodes = ["ACTIVE_LEG_DIRECTION", "KNOWN_AT_OBSERVATION"];
    if (/^(h4|daily|previous-day|previous-week)/.test(pool.type)) expectedReasonCodes.push("HTF_POOL");
    if (map.alignment.alignedTimeframes.length) expectedReasonCodes.push("STRUCTURE_ALIGNMENT");
    if (zone.candleExpansion.directional) expectedReasonCodes.push("DISPLACEMENT_TOWARD");
    if (index === 0 && !obstructions.length) expectedReasonCodes.push("NEAREST_UNOBSTRUCTED");
    return {
      poolId: [pool.type, pool.formedAt, Number(pool.level).toFixed(5)].join("|"),
      type: pool.type, level: pool.level, distanceAtr: pool.distanceAtr, rank: index + 1,
      expectedReasonCodes, structureSupport: map.alignment.alignedTimeframes,
      obstructions,
      contradictions: map.alignment.conflictingTimeframes.map((timeframe) => ({ kind: "structure-conflict", timeframe })),
      rankTrace: ["directional-side", "known-at-observation", "nearest-price-first"],
    };
  });
  const expected = candidates[0] || null;
  const contested = expected && (expected.obstructions.length || expected.contradictions.length);
  return {
    observedAt: zone.createdAt, observedAtIso: iso(zone.createdAt), direction: zone.direction,
    sourceLiquidity: [], destinationCandidates: candidates,
    expectedFirstPoolId: expected?.poolId ?? null,
    expectationState: !expected ? "unresolved" : contested ? "contested" : "supported",
    note: "Expected reasons are frozen at FVG creation and never rewritten by later price action.",
  };
}

function explainLiquidityDevelopment(zone, development, snapshot, mssEvents) {
  if (development.status !== "reached") return {
    ...development, actualFirstPoolId: null,
    expectationResult: "unresolved", actualMechanismCodes: [],
  };
  const firstLevel = development.levels?.[0];
  const actualFirstPoolId = firstLevel
    ? [firstLevel.type, firstLevel.formedAt, Number(firstLevel.level).toFixed(5)].join("|") : null;
  const reachedIndex = development.at == null ? null : development.at;
  const pathMss = mssEvents.filter((event) => event.at > zone.createdAt
    && reachedIndex != null && event.at <= reachedIndex);
  const opposing = zone.direction === "bullish" ? "bearish" : "bullish";
  const actualMechanismCodes = [];
  if (zone.lifecycle.firstTouchAt != null && zone.lifecycle.firstTouchAt <= development.at)
    actualMechanismCodes.push("FVG_ACTIVATED_BEFORE_REACH");
  else actualMechanismCodes.push("DESTINATION_REACHED_WITHOUT_FVG_ACTIVATION");
  if (pathMss.some((event) => event.direction === zone.direction)) actualMechanismCodes.push("ALIGNED_MSS_BEFORE_REACH");
  if (pathMss.some((event) => event.direction === opposing)) actualMechanismCodes.push("OPPOSING_MSS_BEFORE_REACH");
  if (zone.lifecycle.ceReachedAt != null && zone.lifecycle.ceReachedAt <= development.at)
    actualMechanismCodes.push("CE_REACHED_BEFORE_DESTINATION");
  if (zone.lifecycle.closedThroughAt != null && zone.lifecycle.closedThroughAt <= development.at)
    actualMechanismCodes.push("FVG_CLOSED_THROUGH_BEFORE_DESTINATION");
  const expectationResult = snapshot.expectedFirstPoolId == null ? "unresolved"
    : actualFirstPoolId === snapshot.expectedFirstPoolId ? "correct"
    : development.agreement === "aligned" ? "wrong-pool-same-side" : "wrong-side";
  return { ...development, reachedAtIso: iso(development.at), actualFirstPoolId,
    expectationResult, actualMechanismCodes };
}

function liquidityDevelopment(zone, candles, map) {
  let aboveHit = null, belowHit = null;
  for (let i = zone.createdIndex + 1; i < candles.length && (!aboveHit || !belowHit); i++) {
    const c = candles[i];
    if (!aboveHit) {
      const levels = map.above.filter((x) => c.h >= x.level);
      if (levels.length) aboveHit = { index: i, at: c.t, levels };
    }
    if (!belowHit) {
      const levels = map.below.filter((x) => c.l <= x.level);
      if (levels.length) belowHit = { index: i, at: c.t, levels };
    }
  }
  if (!aboveHit && !belowHit) return { status: "unreached", firstSide: null, agreement: null };
  if (aboveHit && belowHit && aboveHit.index === belowHit.index)
    return { status: "ambiguous-same-candle", firstSide: null, at: aboveHit.at, agreement: null };
  const first = !belowHit || (aboveHit && aboveHit.index < belowHit.index) ? { ...aboveHit, side: "above" } : { ...belowHit, side: "below" };
  const aligned = zone.direction === "bullish" ? first.side === "above" : first.side === "below";
  return { status: "reached", firstSide: first.side, at: first.at,
    levels: first.levels.map((x) => ({ type: x.type, level: x.level, formedAt: x.formedAt })),
    agreement: aligned ? "aligned" : "opposed" };
}

export function buildRegistry(asset, primary, h1 = [], d1 = [], nowSec = Date.now() / 1000, options = {}) {
  const timeframe = String(options.timeframe ?? "M15").toUpperCase();
  const primarySeconds = Number(options.primarySeconds ?? (timeframe === "H1" ? 3600 : 900));
  const candles = primary.filter((c) => c.t + primarySeconds <= nowSec), zones = detectFvgs(candles, primarySeconds * 2);
  for (const zone of zones) zone.lifecycle = lifecycle(zone, candles);
  const mssEvents = detectMssEvents(candles);
  for (const zone of zones) {
    zone.surroundingImbalances = surroundingMap(zone, zones);
    zone.entryActivation = anyTouchActivation(zone, candles);
    zone.htfLiquidity = liquidityAt(zone, h1, d1);
    zone.htfAlignment = zone.htfLiquidity.alignment;
    zone.sizeQualification.contextStatus = zone.sizeQualification.status === "invalid-size" && zone.htfAlignment.anyAligned
      ? "sub60-htf-aligned" : zone.sizeQualification.status;
    zone.liquidityPathSnapshot = liquidityPathSnapshot(zone, zone.htfLiquidity, zone.surroundingImbalances);
    zone.liquidityDevelopment = explainLiquidityDevelopment(zone,
      liquidityDevelopment(zone, candles, zone.htfLiquidity), zone.liquidityPathSnapshot, mssEvents);
    const opposite = zone.direction === "bullish" ? "bearish" : "bullish";
    const activeUntil = zone.lifecycle.closedThroughIndex ?? candles.length - 1;
    const find = (direction) => mssEvents.find((e) => e.direction === direction && e.index > zone.createdIndex
      && e.index <= activeUntil && e.liquiditySweptAt >= zone.createdAt);
    const opposing = find(opposite), aligned = find(zone.direction);
    const timing = (event) => !event ? null : zone.lifecycle.firstTouchIndex == null
      || event.index < zone.lifecycle.firstTouchIndex ? "before-first-touch" : "after-first-touch";
    zone.structureDevelopment = {
      opposingMss: opposing ? { ...opposing, timing: timing(opposing) } : null,
      alignedMss: aligned ? { ...aligned, timing: timing(aligned) } : null,
      reverseEntrySearch: opposing ? { direction: opposite, openedAt: opposing.at,
        timing: timing(opposing), mssLifecycle: opposing.lifecycle.status,
        state: "warning-only", reason: "liquidity sweep plus MSS while original FVG active" } : null,
    };
    zone.createdAtIso = iso(zone.createdAt);
    for (const key of ["firstTouchAt", "ceReachedAt", "fullyRebalancedAt", "closedThroughAt",
      "inversionConfirmedAt", "inversionFailedAt"]) zone.lifecycle[key + "Iso"] = iso(zone.lifecycle[key]);
  }
  return { schemaVersion: 1, engine: "TU-TDE", config: REGISTRY_CONFIG,
    generatedAt: new Date().toISOString(), asset: asset.toUpperCase(), timeframe,
    candles: candles.length, from: iso(candles[0]?.t), to: iso(candles.at(-1)?.t), mssEvents, zones };
}
