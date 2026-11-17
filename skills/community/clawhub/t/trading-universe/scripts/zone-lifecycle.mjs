const clamp = (x) => Math.max(0, Math.min(1, x));

// Forward liquidity draws must still be ahead of price discovery. A pool that
// was already touched or sits effectively at the current price is context, not
// a target. Kept pure/exported so the no-fallback rule has regression coverage.
export function filterForwardDraws(candidates, atrD, tooCloseAtr = 0.25) {
  const minDistance = Number.isFinite(atrD) && atrD > 0 ? tooCloseAtr * atrD : 0;
  return (Array.isArray(candidates) ? candidates : []).filter((c) =>
    c && !c.touched && Number.isFinite(c.dist) && c.dist >= minDistance);
}

function stateFromFill(fillPct, invalidated) {
  if (invalidated) return "invalidated";
  if (!(fillPct > 0)) return "fresh";
  if (fillPct < 0.5) return "partial";
  if (fillPct < 1) return "ce_tested";
  return "mitigated";
}

// Create zones only from closed signal candles, then evaluate their lifecycle
// against every later raw candle, including the current forming candle.
export function findFvgs(signalCandles, lifecycleCandles, atrD, price, minSize, maxAgeSec, fmtTime) {
  const bull = [], bear = [];
  for (let i = 2; i < signalCandles.length; i++) {
    const a = signalCandles[i - 2], c = signalCandles[i];
    if (c.l > a.h) {
      const top = c.l, bottom = a.h, size = top - bottom;
      if (size >= minSize) bull.push({ top, bottom, ce: (top + bottom) / 2, t: c.t, atLocal: fmtTime(c.t) });
    }
    if (c.h < a.l) {
      const top = a.l, bottom = c.h, size = top - bottom;
      if (size >= minSize) bear.push({ top, bottom, ce: (top + bottom) / 2, t: c.t, atLocal: fmtTime(c.t) });
    }
  }
  const evaluate = (g, side) => {
    const later = lifecycleCandles.filter((c) => c.t > g.t);
    const size = g.top - g.bottom;
    let fillPct = 0, firstTouchAt = null, touchCount = 0, invalidated = false;
    for (const c of later) {
      const touched = side === "bullish" ? c.l < g.top : c.h > g.bottom;
      if (touched) { touchCount++; firstTouchAt ||= c.t; }
      const f = side === "bullish" ? (g.top - c.l) / size : (c.h - g.bottom) / size;
      fillPct = Math.max(fillPct, clamp(f));
      if (side === "bullish" ? c.c < g.bottom : c.c > g.top) invalidated = true;
    }
    return { ...g, fillPct: Number((fillPct * 100).toFixed(1)), firstTouchAt, firstTouchAtLocal: fmtTime(firstTouchAt), touchCount,
      zoneState: stateFromFill(fillPct, invalidated), invalidated };
  };
  const now = Date.now() / 1000;
  const usable = (g) => !g.invalidated && g.fillPct < 50 && Math.abs(g.ce - price) < 1.5 * atrD && now - g.t <= maxAgeSec;
  return {
    bullish: bull.map((g) => evaluate(g, "bullish")).filter(usable).slice(-4),
    bearish: bear.map((g) => evaluate(g, "bearish")).filter(usable).slice(-4),
  };
}

export function findOrderBlocks(signalCandles, lifecycleCandles, atrD, price, minSize, maxAgeSec, fmtTime) {
  const bull = [], bear = [];
  for (let i = 0; i + 2 < signalCandles.length; i++) {
    const a = signalCandles[i], c = signalCandles[i + 2];
    if (a.c < a.o && c.l > a.h && a.h - a.l >= minSize) {
      bull.push({ top: a.h, bottom: a.l, mid: (a.h + a.l) / 2, t: a.t, confirmedAt: c.t, atLocal: fmtTime(a.t) });
    }
    if (a.c > a.o && c.h < a.l && a.h - a.l >= minSize) {
      bear.push({ top: a.h, bottom: a.l, mid: (a.h + a.l) / 2, t: a.t, confirmedAt: c.t, atLocal: fmtTime(a.t) });
    }
  }
  const evaluate = (g, side) => {
    const later = lifecycleCandles.filter((c) => c.t > g.confirmedAt);
    const size = g.top - g.bottom;
    let fillPct = 0, firstTouchAt = null, touchCount = 0, invalidated = false;
    for (const c of later) {
      const touched = side === "bullish" ? c.l <= g.top : c.h >= g.bottom;
      if (touched) { touchCount++; firstTouchAt ||= c.t; }
      const f = side === "bullish" ? (g.top - c.l) / size : (c.h - g.bottom) / size;
      fillPct = Math.max(fillPct, clamp(f));
      if (side === "bullish" ? c.c < g.bottom : c.c > g.top) invalidated = true;
    }
    return { ...g, fillPct: Number((fillPct * 100).toFixed(1)), firstTouchAt, firstTouchAtLocal: fmtTime(firstTouchAt), touchCount,
      zoneState: stateFromFill(fillPct, invalidated), invalidated };
  };
  const now = Date.now() / 1000;
  const usable = (g) => !g.invalidated && g.fillPct < 50 && Math.abs(g.mid - price) < 1.5 * atrD && now - g.t <= maxAgeSec;
  return {
    bullish: bull.map((g) => evaluate(g, "bullish")).filter(usable).slice(-3),
    bearish: bear.map((g) => evaluate(g, "bearish")).filter(usable).slice(-3),
  };
}

export function zoneFreshnessLabel(g) {
  if (!g || g.zoneState === "fresh") return "fresh/unmitigated";
  return `${g.zoneState} (${g.fillPct}% rebalanced)`;
}
