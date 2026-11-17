// Precios por millón de tokens (USD). Fuente: página oficial de precios de Anthropic,
// consultada el 2026-10-14. Verifica siempre en la fuente: los precios cambian.
// Escritura de caché a 1 h = 2× la entrada; a 5 min = 1.25× la entrada (columnas explícitas).

export const PRICES_SOURCE = 'https://platform.claude.com/docs/en/about-claude/pricing';
export const PRICES_AS_OF = '2026-10-14';

// key: familia-versión. in/out/w5/w1h/read en USD por millón de tokens.
const T = (name, input, w5, w1h, read, out, extra = {}) => ({ name, in: input, w5, w1h, read, out, ...extra });

export const ANTHROPIC_PRICES = {
  'fable-5.1': T('Claude Fable 5.1', 10, 12.5, 20, 0.25, 50),
  'mythos-5.1': T('Claude Mythos 5.1', 10, 12.5, 20, 0.25, 50),
  'fable-5': T('Claude Fable 5', 10, 12.5, 20, 1, 50),
  'mythos-5': T('Claude Mythos 5', 10, 12.5, 20, 1, 50),
  'opus-5.5': T('Claude Opus 5.5', 4, 5, 8, 0.2, 20),
  'opus-5': T('Claude Opus 5', 5, 6.25, 10, 0.5, 25),
  'opus-4.8': T('Claude Opus 4.8', 5, 6.25, 10, 0.5, 25),
  'opus-4.7': T('Claude Opus 4.7', 5, 6.25, 10, 0.5, 25),
  'opus-4.6': T('Claude Opus 4.6', 5, 6.25, 10, 0.5, 25),
  'opus-4.5': T('Claude Opus 4.5', 5, 6.25, 10, 0.5, 25),
  'opus-4.1': T('Claude Opus 4.1', 15, 18.75, 30, 1.5, 75),
  'opus-4': T('Claude Opus 4', 15, 18.75, 30, 1.5, 75),
  'sonnet-5.5': T('Claude Sonnet 5.5', 2, 2.5, 4, 0.1, 10),
  'sonnet-5': T('Claude Sonnet 5', 2, 2.5, 4, 0.2, 10),
  'sonnet-4.6': T('Claude Sonnet 4.6', 3, 3.75, 6, 0.3, 15),
  'sonnet-4.5': T('Claude Sonnet 4.5', 3, 3.75, 6, 0.3, 15),
  'sonnet-4': T('Claude Sonnet 4', 3, 3.75, 6, 0.3, 15),
  // Haiku 5.5 cambia de tarifa cuando el prompt (entrada + lecturas + escrituras de caché) supera 100K tokens.
  'haiku-5.5': T('Claude Haiku 5.5', 0.1, 0.125, 0.2, 0.01, 0.5, {
    tierAbove: { tokens: 100000, in: 0.5, w5: 0.625, w1h: 1, read: 0.05, out: 2.5 },
  }),
  'haiku-4.5': T('Claude Haiku 4.5', 1, 1.25, 2, 0.1, 5),
  'haiku-3.5': T('Claude Haiku 3.5', 0.8, 1, 1.6, 0.08, 4),
};

const FAMILY_RE = /claude-(opus|sonnet|haiku|fable|mythos)-(\d+)(?:[-.](\d{1,2})(?!\d))?/;
const LEGACY_RE = /claude-(\d)(?:[-.](\d{1,2})(?!\d))?-(opus|sonnet|haiku)/;

/** "anthropic/claude-opus-4-6" | "anthropic/claude-opus-4.6" | "claude-sonnet-4-5-20250929" | "us.anthropic.claude-haiku-4-5-v1:0" → "opus-4.6" etc. */
export function anthropicKeyFromRef(ref) {
  if (typeof ref !== 'string') return null;
  const s = ref.toLowerCase();
  let m = FAMILY_RE.exec(s);
  if (m) return m[3] !== undefined ? `${m[1]}-${m[2]}.${m[3]}` : `${m[1]}-${m[2]}`;
  m = LEGACY_RE.exec(s);
  if (m) return m[2] !== undefined ? `${m[3]}-${m[1]}.${m[2]}` : `${m[3]}-${m[1]}`;
  return null;
}

/** Proveedor de un ref "provider/modelo" (null si no trae). */
export function providerOf(ref) {
  if (typeof ref !== 'string') return null;
  const i = ref.indexOf('/');
  return i > 0 ? ref.slice(0, i).toLowerCase() : null;
}

/** ¿Este proveedor factura exactamente como la API directa de Anthropic? */
export function isDirectAnthropic(ref) {
  const p = providerOf(ref);
  return p === 'anthropic' || p === 'anthropic-vertex' || p === 'claude-cli';
}

/**
 * Resuelve las tarifas de un modelo.
 * Orden: --price (override) → precios de tu openclaw.json (models.providers.*.models[].cost) → tabla de Anthropic.
 * Devuelve { rates, name, source, exact } o null si no se conoce el precio.
 */
export function resolvePricing(ref, { config, override } = {}) {
  if (override) return { name: ref || 'override', source: 'override', exact: true, base: override };
  if (typeof ref !== 'string' || !ref) return null;

  const provider = providerOf(ref);
  const id = provider ? ref.slice(provider.length + 1) : ref;
  const cfgModels = config?.models?.providers?.[provider]?.models;
  if (Array.isArray(cfgModels)) {
    const hit = cfgModels.find((m) => m && (m.id === id || m.id === ref));
    const c = hit?.cost;
    if (c && Number.isFinite(c.input) && Number.isFinite(c.output)) {
      const input = c.input;
      return {
        name: hit.name || ref,
        source: 'config',
        exact: true,
        base: {
          in: input,
          out: c.output,
          read: Number.isFinite(c.cacheRead) ? c.cacheRead : input,
          w5: Number.isFinite(c.cacheWrite) ? c.cacheWrite : input,
          w1h: input * 2, // así lo calcula OpenClaw para escrituras de 1 h
        },
      };
    }
  }

  const key = anthropicKeyFromRef(ref);
  const row = key && ANTHROPIC_PRICES[key];
  if (!row) return null;
  return {
    name: row.name,
    source: 'anthropic-table',
    exact: isDirectAnthropic(ref),
    base: { in: row.in, out: row.out, read: row.read, w5: row.w5, w1h: row.w1h },
    tierAbove: row.tierAbove,
  };
}

/** Tarifas aplicables a una petición según el tamaño del prompt. */
export function ratesFor(pricing, promptTokens) {
  const t = pricing.tierAbove;
  if (t && promptTokens > t.tokens) return { in: t.in, out: t.out, read: t.read, w5: t.w5, w1h: t.w1h };
  return pricing.base;
}

/** Costo en USD de una petición. u = { input, output, cacheRead, cacheWrite5m, cacheWrite1h } en tokens. */
export function costOf(pricing, u) {
  const input = u.input || 0;
  const cacheRead = u.cacheRead || 0;
  const w5 = u.cacheWrite5m || 0;
  const w1h = u.cacheWrite1h || 0;
  const r = ratesFor(pricing, input + cacheRead + w5 + w1h);
  return (input * r.in + (u.output || 0) * r.out + cacheRead * r.read + w5 * r.w5 + w1h * r.w1h) / 1e6;
}
