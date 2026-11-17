// Utilidades pequeñas y puras.

/** Duración tipo "30m", "1h", "90s", "45" (minutos por defecto) → minutos. null si no es válida. */
export function parseDurationMinutes(value) {
  if (typeof value === 'number' && Number.isFinite(value) && value >= 0) return value;
  if (typeof value !== 'string') return null;
  const m = /^\s*(\d+(?:\.\d+)?)\s*(ms|s|m|h|d)?\s*$/i.exec(value);
  if (!m) return null;
  const num = Number(m[1]);
  switch ((m[2] || 'm').toLowerCase()) {
    case 'ms': return num / 60000;
    case 's': return num / 60;
    case 'm': return num;
    case 'h': return num * 60;
    case 'd': return num * 1440;
    default: return null;
  }
}

/** Aproximación documentada por OpenClaw: ~4 caracteres por token. */
export const CHARS_PER_TOKEN = 4;
export function estimateTokens(chars) {
  return Math.ceil(chars / CHARS_PER_TOKEN);
}

export function isPlainObject(v) {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

/** Lectura segura con ruta tipo ["agents","defaults","heartbeat"]. */
export function dig(obj, path) {
  let cur = obj;
  for (const key of path) {
    if (!isPlainObject(cur) && !Array.isArray(cur)) return undefined;
    cur = cur[key];
    if (cur === undefined) return undefined;
  }
  return cur;
}

/** Fusión profunda (objetos); las listas y valores simples del segundo reemplazan. No muta. */
export function deepMerge(base, over) {
  if (!isPlainObject(base) || !isPlainObject(over)) return over === undefined ? base : over;
  const out = {};
  for (const k of Object.keys(base)) Object.defineProperty(out, k, { value: base[k], enumerable: true, writable: true, configurable: true });
  for (const k of Object.keys(over)) {
    const merged = k in out && isPlainObject(out[k]) && isPlainObject(over[k]) ? deepMerge(out[k], over[k]) : over[k];
    Object.defineProperty(out, k, { value: merged, enumerable: true, writable: true, configurable: true });
  }
  return out;
}

export function fmtInt(n, lang = 'es') {
  return Math.round(n).toLocaleString(lang === 'es' ? 'es-MX' : 'en-US');
}

export function fmtUsd(n, digits) {
  if (!Number.isFinite(n)) return '—';
  const d = digits ?? (Math.abs(n) >= 100 ? 0 : Math.abs(n) >= 1 ? 2 : 3);
  return `$${n.toLocaleString('en-US', { minimumFractionDigits: d === 0 ? 0 : Math.min(d, 2), maximumFractionDigits: d })}`;
}

export function clamp(n, lo, hi) {
  return Math.min(hi, Math.max(lo, n));
}

export function pct(part, whole) {
  return whole > 0 ? (part / whole) * 100 : 0;
}
