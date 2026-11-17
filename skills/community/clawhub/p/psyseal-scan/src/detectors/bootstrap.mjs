// Cuánto del workspace entra al prompt en cada turno y qué se recorta por los topes de OpenClaw.
// Topes: agents.defaults.bootstrapMaxChars (20000 por archivo), bootstrapTotalMaxChars (60000 en total);
// USER.md tiene un tope fijo de 4,000 caracteres que la configuración solo puede bajar (docs: workspace-and-bootstrap).

import { BOOTSTRAP_FILES } from '../workspace.mjs';
import { DEFAULTS } from '../config.mjs';
import { estimateTokens } from '../util.mjs';

/**
 * @param {object} ws   resultado de readWorkspace
 * @param {{ bootstrapMaxChars:number, bootstrapTotalMaxChars:number }} caps
 */
export function analyzeBootstrap(ws, caps) {
  const rows = [];
  let remaining = caps.bootstrapTotalMaxChars;
  let rawTotal = 0;
  for (const name of BOOTSTRAP_FILES) {
    const f = ws.files[name] || { present: false, chars: 0 };
    const cap = name === 'USER.md' ? Math.min(caps.bootstrapMaxChars, DEFAULTS.userMdMaxChars) : caps.bootstrapMaxChars;
    const afterFileCap = Math.min(f.chars, cap);
    const injected = Math.min(afterFileCap, Math.max(0, remaining));
    remaining -= injected;
    rawTotal += f.chars;
    rows.push({
      name,
      present: !!f.present,
      chars: f.chars,
      cap,
      injectedChars: injected,
      tokens: estimateTokens(injected),
      overFileCap: f.chars > cap,
      cutByTotal: afterFileCap > injected,
      nearCap: f.present && f.chars > cap * 0.8 && f.chars <= cap,
    });
  }
  const injectedTotal = rows.reduce((a, r) => a + r.injectedChars, 0);
  return {
    rows,
    rawTotalChars: rawTotal,
    injectedTotalChars: injectedTotal,
    injectedTokens: estimateTokens(injectedTotal),
    totalCap: caps.bootstrapTotalMaxChars,
    overTotalCap: rows.reduce((a, r) => a + Math.min(r.chars, r.cap), 0) > caps.bootstrapTotalMaxChars,
  };
}
