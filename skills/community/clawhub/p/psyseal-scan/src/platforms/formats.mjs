// Lectores mínimos de YAML y TOML para sacar unas cuantas claves (modelo, topes, intervalos).
// No son parsers completos: ignoran lo que no entienden y nunca ejecutan nada. Para buscar credenciales
// se revisa el texto completo línea por línea, así que no dependen de esto.

function unquote(v) {
  const s = v.trim();
  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) return s.slice(1, -1);
  return s;
}

function stripComment(line) {
  // Quita "# comentario" fuera de comillas.
  let q = null;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (q) {
      if (c === q) q = null;
    } else if (c === '"' || c === "'") q = c;
    else if (c === '#' && (i === 0 || /\s/.test(line[i - 1]))) return line.slice(0, i);
  }
  return line;
}

/** Valor escalar de una ruta de claves en YAML de bloque (sin anclas, sin listas). null si no está. */
export function yamlGet(text, keys) {
  if (typeof text !== 'string') return null;
  const stack = []; // [{ indent, key }]
  let blockScalarIndent = -1;
  for (const rawLine of text.split(/\r?\n/)) {
    if (!rawLine.trim()) continue;
    const indent = rawLine.length - rawLine.trimStart().length;
    if (blockScalarIndent >= 0) {
      if (indent > blockScalarIndent) continue;
      blockScalarIndent = -1;
    }
    const line = stripComment(rawLine).trimEnd();
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('- ') || trimmed === '-' || trimmed.startsWith('---')) continue;
    const m = /^([A-Za-z0-9_.-]+|"[^"]+"|'[^']+')\s*:(?:\s+(.*))?$/.exec(trimmed);
    if (!m) continue;
    const key = unquote(m[1]);
    const value = m[2] === undefined ? '' : m[2].trim();
    while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
    const pathNow = [...stack.map((s) => s.key), key];
    if (value === '' || value === '|' || value === '>' || /^[|>][-+]?$/.test(value)) {
      if (value) blockScalarIndent = indent;
      stack.push({ indent, key });
      continue;
    }
    if (pathNow.length === keys.length && pathNow.every((k, i) => k === keys[i])) return unquote(value);
  }
  return null;
}

/** Valor de `key` en la tabla `[table]` de un TOML simple. table = '' para la raíz. */
export function tomlGet(text, table, key) {
  if (typeof text !== 'string') return null;
  let current = '';
  for (const raw of text.split(/\r?\n/)) {
    const line = stripComment(raw).trim();
    if (!line) continue;
    const t = /^\[\s*([^\][]+?)\s*\]$/.exec(line);
    if (t) {
      current = t[1].replace(/\s*\.\s*/g, '.');
      continue;
    }
    if (current !== table) continue;
    const m = /^([A-Za-z0-9_-]+|"[^"]+")\s*=\s*(.+)$/.exec(line);
    if (m && unquote(m[1]) === key) return unquote(m[2]);
  }
  return null;
}

/** Nombres de tablas TOML que empiezan con `prefix.` (p. ej. agents.<alias>). Devuelve el segmento siguiente. */
export function tomlSubtables(text, prefix) {
  if (typeof text !== 'string') return [];
  const out = new Set();
  for (const raw of text.split(/\r?\n/)) {
    const t = /^\s*\[\s*([^\][]+?)\s*\]\s*(?:#.*)?$/.exec(raw);
    if (!t) continue;
    const name = t[1].replace(/\s*\.\s*/g, '.');
    if (name.startsWith(prefix + '.')) {
      const seg = name.slice(prefix.length + 1).split('.')[0];
      if (seg) out.add(unquote(seg));
    }
  }
  return [...out];
}

export function toNumber(v) {
  if (v === null || v === undefined || v === '') return null;
  const n = Number(String(v).replace(/_/g, ''));
  return Number.isFinite(n) ? n : null;
}

export function toBool(v) {
  if (v === null || v === undefined) return null;
  const s = String(v).trim().toLowerCase();
  if (s === 'true' || s === 'yes' || s === 'on') return true;
  if (s === 'false' || s === 'no' || s === 'off') return false;
  return null;
}

/** "30m", "2h", "1d", "every 30m", "90" (minutos) → minutos. null si no se entiende. */
export function durationMinutes(s) {
  if (typeof s === 'number') return s > 0 ? s : null;
  if (typeof s !== 'string') return null;
  const m = /^(?:every\s+)?(\d+(?:\.\d+)?)\s*(m|min|mins|minutes?|h|hr|hrs|hours?|d|days?|s|sec|secs|seconds?)?$/i.exec(s.trim());
  if (!m) return null;
  const n = Number(m[1]);
  const u = (m[2] || 'm').toLowerCase();
  const mins = u.startsWith('s') ? n / 60 : u.startsWith('h') ? n * 60 : u.startsWith('d') ? n * 1440 : n;
  return mins > 0 ? mins : null;
}

function expandCronField(field, min, max) {
  const set = new Set();
  for (const part of field.split(',')) {
    const m = /^(\*|\d+(?:-\d+)?)(?:\/(\d+))?$/.exec(part.trim());
    if (!m) return null;
    let lo = min;
    let hi = max;
    if (m[1] !== '*') {
      const [a, b] = m[1].split('-').map(Number);
      lo = a;
      hi = b === undefined ? (m[2] ? max : a) : b;
    }
    const step = m[2] ? Number(m[2]) : 1;
    if (!(step > 0) || lo < min || hi > max || lo > hi) return null;
    for (let v = lo; v <= hi; v += step) set.add(v);
  }
  return set.size;
}

/** Corridas por día de una expresión cron de 5 campos (días activos; ignora día del mes y de la semana). */
export function cronRunsPerDay(expr) {
  if (typeof expr !== 'string') return null;
  const f = expr.trim().split(/\s+/);
  if (f.length !== 5) return null;
  const minutes = expandCronField(f[0], 0, 59);
  const hours = expandCronField(f[1], 0, 23);
  if (!minutes || !hours) return null;
  return minutes * hours;
}
