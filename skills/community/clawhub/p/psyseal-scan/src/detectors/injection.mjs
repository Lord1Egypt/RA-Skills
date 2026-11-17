// Señales deterministas de "instrucciones colocadas desde fuera" en archivos de memoria.
// Son heurísticas: marcan para REVISAR, no acusan. Nunca devuelven el texto sospechoso
// (si lo hicieran, una memoria envenenada volvería a entrar al contexto del agente que corra el escaneo).

const L = '(?<![\\p{L}\\p{N}_])'; // límite de palabra con soporte de acentos

function rx(source) {
  return new RegExp(source, 'giu');
}

// class: 'critical' = patrón de exfiltración, ocultamiento o ejecución remota; 'override' = intento de reescribir reglas.
const PATTERNS = [
  {
    id: 'override-rules',
    cls: 'override',
    re: rx(`${L}(?:ignore|disregard|forget|override|bypass)\\s+(?:all\\s+|any\\s+|every\\s+|your\\s+|the\\s+|these\\s+|those\\s+)*(?:previous|prior|above|earlier|preceding|system|safety)\\s+(?:instructions?|rules?|prompts?|guidelines?|constraints?)`),
  },
  {
    id: 'override-rules',
    cls: 'override',
    re: rx(`${L}(?:ignora|olvida|descarta|omite|salt[aá]te)\\s+(?:todas?\\s+|tus\\s+|las\\s+|los\\s+)*(?:instrucciones|reglas|indicaciones|restricciones)\\s+(?:anteriores|previas|del\\s+sistema)`),
  },
  {
    id: 'override-persona',
    cls: 'override',
    re: rx(`${L}(?:you\\s+are\\s+now|from\\s+now\\s+on\\s+you\\s+(?:are|will|must)|a\\s+partir\\s+de\\s+ahora\\s+(?:eres|vas\\s+a|debes))\\s+(?:in\\s+)?(?:developer\\s+mode|dan\\b|jailbroken|unrestricted|sin\\s+restricciones)`),
  },
  {
    id: 'fake-system-block',
    cls: 'override',
    re: rx(`(?:<\\s*/?\\s*(?:system|instructions?)\\s*>|\\[\\s*(?:system|new\\s+instructions?)\\s*\\]|${L}new\\s+system\\s+(?:prompt|instructions?)\\s*:)`),
  },
  {
    id: 'exfiltrate-secrets',
    cls: 'critical',
    // Verbo de envío + credencial + destino ("to", "a", una URL, un correo o un webhook). Sin destino no cuenta:
    // así un formulario con campos "Email" y "Password" no parece una orden de exfiltración.
    re: rx(`${L}(?:send|post|upload|forward|email|e-mail|exfiltrate|leak|transmit|env[ií]a|manda|sube|reenv[ií]a|filtra)\\b[^\\n]{0,80}?(?:api[\\s_-]?keys?|tokens?|passwords?|secrets?|credentials?|private\\s+keys?|seed\\s+phrase|\\.env\\b|claves?|contrase[nñ]as?|credenciales)\\b[^\\n]{0,120}?(?:${L}(?:to|a|al|hacia|into|en)\\s|https?:\\/\\/|[\\w.+-]+@[\\w-]+\\.[\\w.]+|webhook)`),
  },
  {
    id: 'conceal-from-owner',
    cls: 'critical',
    re: rx(`${L}(?:do\\s+not|don'?t|never)\\s+(?:tell|inform|mention|reveal|show|notify)\\s+(?:this\\s+to\\s+)?(?:the\\s+)?(?:user|owner|human|operator)|${L}(?:no|nunca)\\s+(?:le\\s+)?(?:digas|menciones|informes|avises|muestres)\\s+(?:esto\\s+)?(?:al|a\\s+tu)\\s+(?:usuario|due[nñ]o|humano|operador)`),
  },
  {
    id: 'remote-exec',
    cls: 'critical',
    re: rx(`(?:curl|wget)\\s+[^|\\n]{0,200}\\|\\s*(?:sudo\\s+)?(?:ba|z)?sh\\b|base64\\s+(?:-d|--decode)\\b[^\\n]{0,80}\\|\\s*(?:ba|z)?sh\\b|powershell(?:\\.exe)?\\s+[^\\n]{0,40}-e(?:nc|ncodedcommand)\\b`),
  },
];

// Negaciones inmediatamente antes de la frase la vuelven legítima ("nunca envíes tus API keys", "never send ...").
const NEG_BEFORE = /(?:^|[^\p{L}\p{N}_])(?:never|do\s+not|don'?t|must\s+not|should\s+not|shouldn'?t|cannot|can'?t|nunca|jam[aá]s|no\s+debes|no|evita|avoid)\s+(?:ever\s+|to\s+|te\s+|se\s+)?$/iu;

function negatedBefore(line, index) {
  return NEG_BEFORE.test(line.slice(Math.max(0, index - 40), index));
}

// Caracteres invisibles usados para ocultar instrucciones ("ASCII smuggling") y controles bidireccionales.
const HIDDEN_RE = /[\u200b\u2060-\u2064\u202a-\u202e\u2066-\u2069\u{e0000}-\u{e007f}]/u;
const HIDDEN_ALL = /[\u200b\u2060-\u2064\u202a-\u202e\u2066-\u2069\u{e0000}-\u{e007f}]/gu;

/**
 * @param {string} text
 * @param {{ strict?: boolean }} opts strict=true para MEMORY.md, memory/*.md y USER.md (contenido que entra desde fuera);
 *        strict=false (AGENTS/SOUL/IDENTITY, escritos por el dueño) solo marca caracteres ocultos y patrones críticos.
 * @returns {{ id: string, cls: string, line: number }[]} sin texto.
 */
export function scanInjection(text, { strict = true, limit = 50 } = {}) {
  const out = [];
  if (!text) return out;
  const lines = text.split(/\r?\n/);
  for (let ln = 0; ln < lines.length && out.length < limit; ln++) {
    const line = lines[ln].length > 20000 ? lines[ln].slice(0, 20000) : lines[ln];
    if (line.length < 4) continue;

    if (HIDDEN_RE.test(line)) {
      const count = (line.match(HIDDEN_ALL) || []).length;
      out.push({ id: 'hidden-characters', cls: 'hidden', line: ln + 1, count });
    }
    for (const p of PATTERNS) {
      if (!strict && p.cls === 'override') continue;
      p.re.lastIndex = 0;
      let m;
      while ((m = p.re.exec(line)) !== null) {
        if (negatedBefore(line, m.index)) continue;
        out.push({ id: p.id, cls: p.cls, line: ln + 1 });
        break; // una señal de cada tipo por línea basta
      }
    }
  }
  return out.slice(0, limit);
}
