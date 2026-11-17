// Economía del latido (heartbeat) y del arranque. Todo son ESTIMACIONES con supuestos declarados:
// el reporte las muestra como rangos y nunca como promesa. Para cifras reales usa --usage.

import { ANTHROPIC_PRICES, costOf, isDirectAnthropic, resolvePricing } from './pricing.mjs';
import { resolveCacheRetention } from './config.mjs';

export const ASSUMPTIONS = Object.freeze({
  // Latido normal: casi siempre responde NO_REPLY (unos pocos tokens).
  heartbeatOutputTokens: 100,
  // Documentación de OpenClaw (gateway/heartbeat, "Cost awareness"): ~100K → ~2–5K tokens por ejecución
  // con isolatedSession (+ lightContext).
  isolatedLightTokens: [2000, 5000],
  // Supuesto propio: prompt del sistema + herramientas cuando solo hay isolatedSession (sin lightContext).
  isolatedOverheadTokens: 3000,
  // Tamaños de sesión principal que se muestran cuando la persona no pasa --session-tokens.
  sessionTokenScenarios: [20000, 50000, 100000],
  daysPerMonth: 30,
});

const TTL_SHORT_MIN = 5;
const TTL_LONG_MIN = 60;

/** Costo de una ejecución de latido con prompt de P tokens, según caché y cadencia. null si no se puede valorar. */
export function perRunCost(pricing, P, retention, everyMin, outputTokens = ASSUMPTIONS.heartbeatOutputTokens) {
  switch (retention) {
    case 'none':
      return { cost: costOf(pricing, { input: P, output: outputTokens }), mode: 'sin-cache' };
    case 'short':
      return everyMin <= TTL_SHORT_MIN
        ? { cost: costOf(pricing, { cacheRead: P, output: outputTokens }), mode: 'lectura' }
        : { cost: costOf(pricing, { cacheWrite5m: P, output: outputTokens }), mode: 'escritura-5m' };
    case 'long':
      return everyMin <= TTL_LONG_MIN
        ? { cost: costOf(pricing, { cacheRead: P, output: outputTokens }), mode: 'lectura' }
        : { cost: costOf(pricing, { cacheWrite1h: P, output: outputTokens }), mode: 'escritura-1h' };
    default:
      return null;
  }
}

/**
 * @param {object} ctx { agent, plan (resolveHeartbeat), config, billing, bootstrapTokens, sessionTokens?, priceOverride?, env? }
 */
export function heartbeatEconomics(ctx) {
  const { agent, plan, config, billing, bootstrapTokens, sessionTokens, priceOverride, env } = ctx;
  if (!plan.enabled) return { applicable: false, reason: plan.reason };

  const modelRef = plan.model || agent.model || null;
  const direct = isDirectAnthropic(modelRef);
  const pricing = resolvePricing(modelRef, { config, override: priceOverride });
  const retention = resolveCacheRetention(config, agent, modelRef, { directAnthropic: direct, env });
  const subscription = billing.mode === 'subscription';
  const canPrice = !!pricing && !!retention.value && !subscription;

  const runsPerMonth = plan.runsPerDay * ASSUMPTIONS.daysPerMonth;
  const [isoLo, isoHi] = ASSUMPTIONS.isolatedLightTokens;

  // Tamaño del prompt de cada ejecución HOY.
  const alreadyLean = plan.isolatedSession && plan.lightContext;
  const scenarios = [];
  if (plan.isolatedSession) {
    const P = plan.lightContext ? Math.round((isoLo + isoHi) / 2) : bootstrapTokens + ASSUMPTIONS.isolatedOverheadTokens;
    scenarios.push({ sessionTokens: null, promptTokens: P });
  } else {
    const list = Number.isFinite(sessionTokens) && sessionTokens > 0 ? [sessionTokens] : ASSUMPTIONS.sessionTokenScenarios;
    for (const S of list) scenarios.push({ sessionTokens: S, promptTokens: S });
  }

  const rows = scenarios.map((sc) => {
    const row = { ...sc, nowPerRun: null, nowMonth: null, isolateLight: null, cacheLong: null };
    if (!canPrice) return row;
    const now = perRunCost(pricing, sc.promptTokens, retention.value, plan.everyMin);
    row.nowPerRun = now.cost;
    row.nowMode = now.mode;
    row.nowMonth = now.cost * runsPerMonth;

    if (!alreadyLean) {
      const lo = perRunCost(pricing, isoLo, retention.value, plan.everyMin).cost;
      const hi = perRunCost(pricing, isoHi, retention.value, plan.everyMin).cost;
      const monthLo = lo * runsPerMonth;
      const monthHi = hi * runsPerMonth;
      row.isolateLight = {
        promptLow: isoLo,
        promptHigh: isoHi,
        monthLow: monthLo,
        monthHigh: monthHi,
        savingLow: Math.max(0, row.nowMonth - monthHi),
        savingHigh: Math.max(0, row.nowMonth - monthLo),
      };
    }

    if (!plan.isolatedSession && retention.value !== 'long' && plan.everyMin <= TTL_LONG_MIN) {
      const long = perRunCost(pricing, sc.promptTokens, 'long', plan.everyMin).cost * runsPerMonth;
      row.cacheLong = { month: long, saving: Math.max(0, row.nowMonth - long) };
    }
    return row;
  });

  // Mayor palanca por escenario (las palancas se solapan: nunca se suman).
  for (const r of rows) {
    const lows = [r.isolateLight?.savingLow ?? 0, r.cacheLong?.saving ?? 0];
    const highs = [r.isolateLight?.savingHigh ?? 0, r.cacheLong?.saving ?? 0];
    r.bestSavingLow = Math.max(...lows);
    r.bestSavingHigh = Math.max(...highs);
  }

  const headline = canPrice
    ? {
        nowLow: Math.min(...rows.map((r) => r.nowMonth)),
        nowHigh: Math.max(...rows.map((r) => r.nowMonth)),
        savingLow: Math.min(...rows.map((r) => r.bestSavingLow)),
        savingHigh: Math.max(...rows.map((r) => r.bestSavingHigh)),
      }
    : null;

  // Modelo más barato para el latido (solo la razón de precios; que sirva depende de la tarea).
  let cheaperModel = null;
  if (pricing && !plan.model) {
    const ref = ANTHROPIC_PRICES['haiku-5.5'];
    const ratio = pricing.base.in / ref.in;
    if (ratio >= 3) cheaperModel = { name: ref.name, ratio };
  }

  return {
    applicable: true,
    modelRef,
    directAnthropic: direct,
    pricing: pricing ? { name: pricing.name, source: pricing.source, exact: pricing.exact } : null,
    priced: canPrice,
    billing: billing.mode,
    retention,
    everyMin: plan.everyMin,
    runsPerDay: plan.runsPerDay,
    runsPerMonth,
    state: { isolatedSession: plan.isolatedSession, lightContext: plan.lightContext },
    alreadyLean,
    rows,
    headline,
    cheaperModel,
  };
}

/** Valor de quitar `tokens` del arranque: por cada 1,000 llamadas, si todas aciertan el caché o todas lo reescriben. */
export function trimValue(pricing, tokens) {
  if (!pricing || !(tokens > 0)) return null;
  const r = pricing.base;
  return {
    per1000Hit: (tokens * r.read * 1000) / 1e6,
    per1000Miss: (tokens * r.w5 * 1000) / 1e6,
  };
}
