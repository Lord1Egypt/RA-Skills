// Detección determinista de credenciales expuestas. NUNCA devuelve el valor encontrado:
// solo tipo, línea y longitud. Así el reporte no puede filtrar el secreto (ni a la pantalla,
// ni al contexto del agente que ejecute esta skill).

const PATTERNS = [
  { id: 'anthropic-key', label: 'Anthropic', re: /(?<![A-Za-z0-9_-])sk-ant-[A-Za-z0-9]{2,12}-[A-Za-z0-9_-]{20,}/g },
  { id: 'openrouter-key', label: 'OpenRouter', re: /(?<![A-Za-z0-9_-])sk-or-v1-[A-Za-z0-9]{32,}/g },
  { id: 'openai-key', label: 'OpenAI', re: /(?<![A-Za-z0-9_-])sk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{32,}/g },
  { id: 'github-token', label: 'GitHub', re: /(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})/g },
  { id: 'aws-access-key', label: 'AWS', re: /(?<![A-Z0-9])(?:AKIA|ASIA)[0-9A-Z]{16}(?![A-Z0-9])/g },
  { id: 'google-api-key', label: 'Google', re: /(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{35}(?![A-Za-z0-9_-])/g },
  { id: 'slack-token', label: 'Slack', re: /(?<![A-Za-z0-9])xox[abprs]-[A-Za-z0-9-]{10,}/g },
  { id: 'telegram-bot-token', label: 'Telegram', re: /(?<![0-9])\d{8,10}:[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])/g },
  { id: 'discord-bot-token', label: 'Discord', re: /(?<![A-Za-z0-9_-])[MNO][A-Za-z0-9_-]{23,25}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}/g },
  { id: 'stripe-key', label: 'Stripe', re: /(?<![A-Za-z0-9_])(?:sk|rk)_live_[A-Za-z0-9]{20,}/g },
  { id: 'private-key-block', label: 'Llave privada (PEM)', re: /-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----/g, noBodyCheck: true },
  { id: 'jwt', label: 'JWT', re: /(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g },
  { id: 'url-credentials', label: 'URL con usuario y contraseña', re: /(?<![A-Za-z0-9+.-])[a-z][a-z0-9+.-]{1,15}:\/\/[^\s:@/]{1,64}:[^\s@/]{4,128}@[^\s/]{3,}/gi, noBodyCheck: true },
];

// Variables tipo api_key=..., "password": "...", token: ... (solo si el valor parece un secreto real).
const ASSIGNED = /(?<![A-Za-z0-9])(?:[A-Za-z0-9_-]{0,40}(?:api[_-]?key|secret|token|passw(?:or)?d|passwd|pwd|private[_-]?key|access[_-]?key|credential)[A-Za-z0-9_-]{0,40})["']?\s*[:=]\s*["'`]?([^\s"'`,;)}\]]{12,})/gi;
const HEX64_CONTEXT = /priv(?:ate)?[ _-]?key|secret|seed|mnemonic|wallet/i;
const HEX64 = /(?<![A-Za-z0-9])(?:0x)?[a-fA-F0-9]{64}(?![A-Za-z0-9])/g;

const PLACEHOLDER_WORDS = /^(?:your|tu|mi|my|xxx|<|\$\{|\$[A-Z_]|\{\{|%[A-Z_]|example|ejemplo|changeme|cambia|placeholder|redacted|todo|none|null|undefined|true|false|env:|process\.env|secret:|\*+|\.\.\.)/i;

function distinctChars(s) {
  return new Set(s).size;
}

function looksLikeSecretValue(v) {
  if (v.length < 12) return false;
  if (PLACEHOLDER_WORDS.test(v)) return false;
  if (/[([{<>|\\]/.test(v)) return false; // llamadas, objetos y plantillas: código, no un valor pegado
  if (!/\d/.test(v) && /^[A-Za-z_.$-]+$/.test(v)) return false; // palabras, identificadores y rutas de propiedades (a.b.c)
  if (/^(?:\/|\.\/|~\/|[a-z]:\\|https?:\/\/[^:@]*$)/i.test(v)) return false; // rutas y URL sin credenciales
  if (distinctChars(v) < 6) return false; // "xxxxxxxxxxxx", "************"
  const hasDigit = /\d/.test(v);
  const hasLetter = /[A-Za-z]/.test(v);
  const classes = [/[a-z]/, /[A-Z]/, /\d/, /[^A-Za-z0-9]/].filter((r) => r.test(v)).length;
  return (hasDigit && hasLetter && v.length >= 16) || (v.length >= 32 && classes >= 2);
}

function isPlaceholderUrlCredential(url) {
  const m = /:\/\/([^:@/]*):([^@/]*)@/.exec(url);
  if (!m) return true;
  return /^(?:pass(?:word)?|contrase\w*|secret|\*+|<[^>]*>|\{[^}]*\}|\$\{[^}]*\}|x{3,}|changeme|example|tu_?password)$/i.test(m[2]);
}

function isPlaceholderToken(token) {
  // Ejemplos de documentación: sk-ant-xxxxxxxx..., sk-...AAAAAAAA
  const body = token.replace(/^[A-Za-z]{2,}[_-]/, '');
  return distinctChars(body) < 6 || /xxxx|your|example|ejemplo|1234567890/i.test(token);
}

/**
 * Escanea un texto y devuelve hallazgos sin valores: [{ id, label, line, length }].
 * Máx. `limit` hallazgos por texto. Con `withSpans` agrega `start`/`end` (columnas dentro de la línea): solo lo usa
 * la limpieza para tapar el valor; el reporte nunca lo muestra.
 */
export function scanSecrets(text, { limit = 50, withSpans = false } = {}) {
  const out = [];
  if (!text) return out;
  const lines = text.split(/\r?\n/);
  for (let ln = 0; ln < lines.length && out.length < limit; ln++) {
    // Líneas enormes (volcados base64/JSON) se revisan solo en su primera parte: evita costo cuadrático.
    const line = lines[ln].length > 20000 ? lines[ln].slice(0, 20000) : lines[ln];
    if (line.length < 12) continue;
    const spans = [];
    const overlaps = (a, b) => spans.some(([s, e]) => a < e && b > s);

    for (const p of PATTERNS) {
      p.re.lastIndex = 0;
      let m;
      while ((m = p.re.exec(line)) !== null) {
        const start = m.index;
        const end = start + m[0].length;
        if (!p.noBodyCheck && isPlaceholderToken(m[0])) continue;
        if (p.id === 'url-credentials' && isPlaceholderUrlCredential(m[0])) continue;
        if (overlaps(start, end)) continue;
        spans.push([start, end]);
        out.push({ id: p.id, label: p.label, line: ln + 1, length: m[0].length, ...(withSpans ? { start, end } : {}) });
        if (out.length >= limit) break;
      }
    }
    if (out.length >= limit) break;

    if (HEX64_CONTEXT.test(line)) {
      HEX64.lastIndex = 0;
      let h;
      while ((h = HEX64.exec(line)) !== null) {
        const start = h.index;
        const end = start + h[0].length;
        if (overlaps(start, end)) continue;
        if (distinctChars(h[0].replace(/^0x/, '')) < 8) continue;
        spans.push([start, end]);
        out.push({ id: 'hex-private-key', label: 'Posible llave privada (64 hex)', line: ln + 1, length: h[0].length, ...(withSpans ? { start, end } : {}) });
        if (out.length >= limit) break;
      }
    }

    ASSIGNED.lastIndex = 0;
    let a;
    while ((a = ASSIGNED.exec(line)) !== null) {
      const value = a[1];
      const start = a.index + a[0].length - value.length;
      const end = start + value.length;
      if (overlaps(start, end)) continue;
      if (!looksLikeSecretValue(value)) continue;
      spans.push([start, end]);
      out.push({ id: 'assigned-secret', label: 'Credencial asignada', line: ln + 1, length: value.length, ...(withSpans ? { start, end } : {}) });
      if (out.length >= limit) break;
    }

  }
  return out;
}

/** Recorre el árbol de la config buscando credenciales en texto plano. Devuelve rutas, nunca valores. */
export function scanConfigSecrets(config, { limit = 50 } = {}) {
  const out = [];
  const seen = new Set();
  function walk(node, pathParts, depth) {
    if (out.length >= limit || depth > 24) return;
    if (typeof node === 'string') {
      const keyName = pathParts[pathParts.length - 1] || '';
      let hit = null;
      // 1) patrones de proveedores
      const found = scanSecrets(node, { limit: 1 });
      if (found.length) hit = found[0];
      // 2) clave con nombre sensible y valor plausible (no ${VAR}, no SecretRef)
      if (!hit && /key|token|secret|passw|credential/i.test(keyName) && looksLikeSecretValue(node)) {
        hit = { id: 'assigned-secret', label: 'Credencial asignada', length: node.length };
      }
      if (hit) {
        const p = pathParts.join('.');
        if (!seen.has(p)) {
          seen.add(p);
          out.push({ id: hit.id, label: hit.label, path: p, length: hit.length ?? node.length });
        }
      }
      return;
    }
    if (Array.isArray(node)) {
      node.forEach((v, i) => walk(v, [...pathParts, String(i)], depth + 1));
      return;
    }
    if (node && typeof node === 'object') {
      for (const k of Object.keys(node)) walk(node[k], [...pathParts, k], depth + 1);
    }
  }
  walk(config, [], 0);
  return out;
}
