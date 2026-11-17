export const DEFAULT_RISK_POLICY = Object.freeze({
  moveStopToBreakevenAtR: 0.5,
  breakevenEffective: "next-candle",
});

const finite = (x) => typeof x === "number" && Number.isFinite(x);
const iso = (t) => t == null ? null : new Date(t * 1000).toISOString();

export function simulateTicket(ticket, candles, policy = DEFAULT_RISK_POLICY) {
  const long = ticket.direction === "LONG";
  const placedIndex = ticket.placedIndex;
  if (!Number.isInteger(placedIndex) || placedIndex < 0 || placedIndex >= candles.length)
    throw new Error("ticket.placedIndex is outside the candle archive");
  const market = ticket.entryType === "market";
  const marketFillIndex = placedIndex + 1;
  if (market && marketFillIndex >= candles.length)
    return { ...ticket, outcome: "pending-at-data-end", rMultiple: null, filledAt: null };

  let entry = market ? candles[marketFillIndex].o : ticket.entry;
  const sl = ticket.sl, target = ticket.target;
  if (![entry, sl, target].every(finite)) throw new Error("ticket entry/sl/target must be finite");
  const risk = long ? entry - sl : sl - entry;
  const reward = long ? target - entry : entry - target;
  if (!(risk > 0) || !(reward > 0)) throw new Error("ticket direction ordering is invalid");
  const targetR = reward / risk;
  const beAtR = policy.moveStopToBreakevenAtR;
  const beTrigger = finite(beAtR) ? (long ? entry + beAtR * risk : entry - beAtR * risk) : null;

  let fillIndex = null, beTriggeredIndex = null, beEffectiveIndex = null;
  let max = entry, min = entry, outcome = null, terminalIndex = null;
  const events = [];

  const touched = (c, level) => c.l <= level && c.h >= level;
  const stopHit = (c, stop) => long ? c.l <= stop : c.h >= stop;
  const targetHit = (c) => long ? c.h >= target : c.l <= target;
  const triggerHit = (c) => beTrigger != null && (long ? c.h >= beTrigger : c.l <= beTrigger);

  for (let i = placedIndex + 1; i < candles.length; i++) {
    const c = candles[i];
    if (fillIndex == null) {
      if (market) {
        if (i !== marketFillIndex) continue;
        fillIndex = i;
      } else {
        if (!touched(c, entry)) {
          const invalidatedWithoutTouch = long ? c.h < entry && c.l <= sl : c.l > entry && c.h >= sl;
          if (invalidatedWithoutTouch) {
            outcome = "invalidated-before-fill"; terminalIndex = i;
            events.push({ type: outcome, at: c.t });
            break;
          }
          continue;
        }
        fillIndex = i;
      }
      events.push({ type: "filled", at: c.t, price: entry });
    }

    max = Math.max(max, c.h);
    min = Math.min(min, c.l);
    const activeStop = beEffectiveIndex != null && i >= beEffectiveIndex ? entry : sl;
    const hitStop = stopHit(c, activeStop), hitTarget = targetHit(c);

    if (hitStop && hitTarget) {
      outcome = "ambiguous"; terminalIndex = i;
      events.push({ type: "ambiguous-stop-target", at: c.t, activeStop });
      break;
    }
    if (hitTarget) {
      outcome = "target"; terminalIndex = i;
      events.push({ type: "target", at: c.t, price: target });
      break;
    }
    if (hitStop) {
      outcome = activeStop === entry ? "breakeven" : "stop";
      terminalIndex = i;
      events.push({ type: outcome, at: c.t, price: activeStop });
      break;
    }
    if (beTriggeredIndex == null && triggerHit(c)) {
      beTriggeredIndex = i;
      beEffectiveIndex = i + 1;
      events.push({ type: "breakeven-armed", at: c.t, trigger: beTrigger,
        effectiveAt: candles[i + 1]?.t ?? null });
    }
  }

  if (outcome == null) outcome = fillIndex == null ? "pending-at-data-end" : "open-at-data-end";
  const mfeR = fillIndex == null ? null : (long ? max - entry : entry - min) / risk;
  const maeR = fillIndex == null ? null : (long ? entry - min : max - entry) / risk;
  const rMultiple = outcome === "target" ? targetR : outcome === "stop" ? -1
    : outcome === "breakeven" ? 0 : null;
  return {
    ...ticket,
    actualEntry: entry,
    initialRisk: risk,
    targetR: Number(targetR.toFixed(3)),
    riskPolicy: policy,
    outcome,
    rMultiple: rMultiple == null ? null : Number(rMultiple.toFixed(3)),
    filledAt: fillIndex == null ? null : candles[fillIndex].t,
    filledAtIso: fillIndex == null ? null : iso(candles[fillIndex].t),
    terminalAt: terminalIndex == null ? null : candles[terminalIndex].t,
    terminalAtIso: terminalIndex == null ? null : iso(candles[terminalIndex].t),
    breakevenTriggeredAt: beTriggeredIndex == null ? null : candles[beTriggeredIndex].t,
    breakevenEffectiveAt: beEffectiveIndex == null ? null : candles[beEffectiveIndex]?.t ?? null,
    mfeR: mfeR == null ? null : Number(mfeR.toFixed(3)),
    maeR: maeR == null ? null : Number(maeR.toFixed(3)),
    events,
  };
}