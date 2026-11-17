// Lee la salida de `openclaw gateway usage-cost --json` (gasto REAL registrado por OpenClaw).
// El formato exacto puede variar entre versiones, así que el lector es tolerante:
// busca los totales (`totals`, `summary.totals`, o la raíz) y la lista diaria si existe.

import { parse } from './json5.mjs';
import { isPlainObject } from './util.mjs';

const NUM = (v) => (typeof v === 'number' && Number.isFinite(v) ? v : 0);
const FIELDS = ['input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'totalCost', 'inputCost', 'outputCost', 'cacheReadCost', 'cacheWriteCost', 'missingCostEntries'];

function looksLikeTotals(o) {
  return isPlainObject(o) && ('totalCost' in o || 'totalTokens' in o || 'cacheWriteCost' in o);
}

export function parseUsage(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    try {
      data = parse(text);
    } catch {
      return null;
    }
  }
  if (!isPlainObject(data)) return null;

  const candidates = [data.totals, data.summary?.totals, data.summary, data.result?.totals, data.result, data];
  const raw = candidates.find(looksLikeTotals);
  if (!raw) return null;

  const totals = {};
  for (const f of FIELDS) totals[f] = NUM(raw[f]);
  if (!totals.totalCost) totals.totalCost = totals.inputCost + totals.outputCost + totals.cacheReadCost + totals.cacheWriteCost;
  if (!totals.totalTokens) totals.totalTokens = totals.input + totals.output + totals.cacheRead + totals.cacheWrite;

  const dailyRaw = [data.daily, data.summary?.daily, data.result?.daily].find(Array.isArray);
  const daily = Array.isArray(dailyRaw) ? dailyRaw.filter((d) => isPlainObject(d)) : [];
  let days = NUM(data.days) || NUM(data.summary?.days) || NUM(data.range?.days) || daily.length;
  if (!days && daily.length === 0) days = 0;

  const cacheStatus = isPlainObject(data.cacheStatus) ? data.cacheStatus : isPlainObject(data.summary?.cacheStatus) ? data.summary.cacheStatus : null;

  return { totals, days, dailyCount: daily.length, cacheStatus };
}

/** Lectura de lo que significa el gasto real. Devuelve datos; el texto lo arma el reporte. */
export function analyzeUsage(u) {
  const t = u.totals;
  const cost = t.totalCost;
  const byType = {
    input: cost > 0 ? t.inputCost / cost : 0,
    output: cost > 0 ? t.outputCost / cost : 0,
    cacheRead: cost > 0 ? t.cacheReadCost / cost : 0,
    cacheWrite: cost > 0 ? t.cacheWriteCost / cost : 0,
  };
  const promptTokens = t.input + t.cacheRead + t.cacheWrite;
  const hitRate = promptTokens > 0 ? t.cacheRead / promptTokens : null;
  const monthly = u.days > 0 ? (cost / u.days) * 30 : null;
  const status = u.cacheStatus && typeof u.cacheStatus.status === 'string' ? u.cacheStatus.status : null;
  // Estados que la documentación de OpenClaw marca como "totales posiblemente incompletos".
  const incompleteTotals = status !== null && ['refreshing', 'partial', 'stale'].includes(status.toLowerCase());
  return {
    days: u.days,
    totalCost: cost,
    monthlyProjection: monthly,
    shares: byType,
    cacheHitRate: hitRate,
    cacheWriteDominates: byType.cacheWrite >= 0.5 && cost > 0,
    lowCacheHit: hitRate !== null && hitRate < 0.5 && promptTokens > 100000,
    missingCostEntries: t.missingCostEntries,
    incompleteTotals,
    cacheStatus: status,
  };
}
