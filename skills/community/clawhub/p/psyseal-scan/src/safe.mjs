// Texto apto para mostrar en una terminal o en el contexto de un agente.
// Los nombres de archivo, ids de agente, modelos y rutas vienen de la config y del disco: alguien con acceso al
// workspace podría poner en ellos secuencias de escape de terminal, saltos de línea (para falsificar líneas del
// reporte) o caracteres invisibles y bidireccionales (para disfrazar texto). Aquí se neutralizan.

// Rangos de puntos de código que nunca se muestran tal cual: controles C0/C1, guion suave, marcas y controles
// bidireccionales, anchos cero, separadores de línea, rellenos invisibles, selectores de variación y "tags" de Unicode.
const RANGES = [
  [0x0000, 0x001f], [0x007f, 0x009f], [0x00ad, 0x00ad], [0x061c, 0x061c], [0x115f, 0x1160], [0x17b4, 0x17b5],
  [0x180e, 0x180e], [0x200b, 0x200f], [0x2028, 0x202e], [0x2060, 0x206f], [0x3164, 0x3164], [0xfe00, 0xfe0f],
  [0xfeff, 0xfeff], [0xffa0, 0xffa0], [0xfff0, 0xfffb], [0xe0000, 0xe0fff],
];
const hex = (n) => n.toString(16);
const CLASS = RANGES.map(([a, b]) => (a === b ? `\\u{${hex(a)}}` : `\\u{${hex(a)}}-\\u{${hex(b)}}`)).join('');
const UNSAFE = new RegExp(`[${CLASS}]`, 'gu');

/** Una sola línea, sin caracteres peligrosos, con un largo máximo (se recorta por el centro para conservar inicio y final). */
export function safeText(value, max = 160) {
  const cps = Array.from(String(value).replace(UNSAFE, '?'));
  if (cps.length <= max) return cps.join('');
  const half = Math.floor((max - 1) / 2);
  return cps.slice(0, half).join('') + '…' + cps.slice(cps.length - half).join('');
}

/** Copia del reporte con todos los textos pasados por safeText. No cambia números, booleanos ni la estructura. */
export function safeDeep(value, max = 160, depth = 0) {
  if (typeof value === 'string') return safeText(value, max);
  if (depth > 32 || value === null || typeof value !== 'object') return value;
  if (Array.isArray(value)) return value.map((v) => safeDeep(v, max, depth + 1));
  const out = {};
  for (const k of Object.keys(value)) {
    Object.defineProperty(out, safeText(k, max), { value: safeDeep(value[k], max, depth + 1), enumerable: true, writable: true, configurable: true });
  }
  return out;
}

// En JSON, los controles C0 ya salen escapados por JSON.stringify; el resto de la lista se escapa aquí.
const JSON_UNSAFE = new RegExp(`[${RANGES.filter(([a]) => a > 0x1f).map(([a, b]) => (a === b ? `\\u{${hex(a)}}` : `\\u{${hex(a)}}-\\u{${hex(b)}}`)).join('')}]`, 'gu');

/** En la salida JSON, los caracteres invisibles o bidireccionales se escriben como escapes (JSON válido y visible). */
export function escapeInvisibleJson(json) {
  return json.replace(JSON_UNSAFE, (c) => Array.from({ length: c.length }, (_, i) => '\\u' + c.charCodeAt(i).toString(16).padStart(4, '0')).join(''));
}
