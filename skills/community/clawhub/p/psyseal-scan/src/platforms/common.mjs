// Utilidades compartidas por los lectores de plataformas. Solo lectura: no sigue enlaces simbólicos,
// limita tamaños y cantidad de archivos, y nunca escribe.

import fs from 'node:fs';
import path from 'node:path';
import { estimateTokens } from '../util.mjs';
import { scanSecrets } from '../detectors/secrets.mjs';

export const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_LISTED = 2000;
const MAX_SCANNED = 400;
const MAX_TOTAL_BYTES = 20 * 1024 * 1024;

export function expandHome(p, home) {
  if (typeof p !== 'string') return p;
  if (p === '~') return home;
  if (p.startsWith('~/') || p.startsWith('~\\')) return path.join(home, p.slice(2));
  return p;
}

export function isDir(p) {
  try {
    const st = fs.lstatSync(p);
    return st.isDirectory();
  } catch {
    return false;
  }
}

export function isFile(p) {
  try {
    return fs.lstatSync(p).isFile();
  } catch {
    return false;
  }
}

/** Lee un archivo regular (no enlace) de hasta 2 MB. */
export function readRegular(file) {
  let st;
  try {
    st = fs.lstatSync(file);
  } catch {
    return { missing: true };
  }
  if (st.isSymbolicLink()) return { symlink: true };
  if (!st.isFile()) return { missing: true };
  if (st.size > MAX_FILE_BYTES) return { tooLarge: true, bytes: st.size, mode: st.mode };
  try {
    let text = fs.readFileSync(file, 'utf8');
    if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
    return { text, bytes: st.size, mode: st.mode };
  } catch {
    return { missing: true };
  }
}

/** Lee texto de config (JSON, YAML, TOML) sin lanzar. */
export function readConfigText(file) {
  const r = readRegular(file);
  if (r.text !== undefined) return { text: r.text, error: null };
  if (r.missing) return { text: null, error: 'not-found' };
  if (r.symlink) return { text: null, error: 'symlink' };
  return { text: null, error: 'too-large' };
}

/**
 * Entrada de archivo normalizada.
 * kind: 'boot' (instrucciones del dueño) | 'memory' (memoria duradera) | 'daily' (notas por fecha) |
 *       'skill' | 'context' | 'task' (HEARTBEAT.md y similares)
 * injected: entra completo al prompt en cada turno. cap: tope de caracteres por archivo (null si no hay).
 */
export function fileEntry(abs, rel, kind, { injected = false, cap = null, capKind = 'truncate', agentWritten = false } = {}) {
  const r = readRegular(abs);
  const base = { abs, rel, kind, injected, cap, capKind, agentWritten, present: false, chars: 0, bytes: 0, text: '' };
  if (r.symlink) return { ...base, symlink: true };
  if (r.missing) return base;
  if (r.tooLarge) return { ...base, present: true, tooLarge: true, chars: r.bytes, bytes: r.bytes };
  return { ...base, present: true, chars: r.text.length, bytes: r.bytes, text: r.text };
}

/** Lista archivos .md bajo `dir` (sin seguir enlaces), hasta `maxDepth` niveles. Devuelve rutas absolutas. */
export function listMarkdown(dir, { maxDepth = 2, skipDirs = [] } = {}) {
  const out = [];
  const stats = { symlinks: 0, truncated: false };
  const skip = new Set(skipDirs);
  function walk(d, depth) {
    let names;
    try {
      names = fs.readdirSync(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of names) {
      if (out.length >= MAX_LISTED) {
        stats.truncated = true;
        return;
      }
      const full = path.join(d, e.name);
      if (e.isSymbolicLink()) {
        stats.symlinks++;
        continue;
      }
      if (e.isDirectory()) {
        if (depth < maxDepth && !skip.has(e.name) && !e.name.startsWith('.') && e.name !== 'node_modules') walk(full, depth + 1);
      } else if (e.isFile() && e.name.toLowerCase().endsWith('.md')) out.push(full);
    }
  }
  walk(dir, 0);
  return { files: out, ...stats };
}

/** Lee una lista de .md con límites de cantidad y bytes. */
export function readMany(root, absList, kind, opts = {}) {
  const sorted = [...absList].sort((a, b) => b.localeCompare(a)); // nombres con fecha: recientes primero
  const out = [];
  let bytes = 0;
  for (const abs of sorted.slice(0, MAX_SCANNED)) {
    const e = fileEntry(abs, path.relative(root, abs).split(path.sep).join('/'), kind, opts);
    if (!e.present) continue;
    bytes += e.bytes;
    if (bytes > MAX_TOTAL_BYTES) break;
    out.push(e);
  }
  return { entries: out, listed: absList.length, scanned: out.length };
}

/** ¿Un archivo con credenciales lo pueden leer otros usuarios de la máquina? (solo Unix) */
export function permissionInfo(abs) {
  if (process.platform === 'win32') return null;
  try {
    const st = fs.lstatSync(abs);
    if (!st.isFile()) return null;
    const mode = st.mode & 0o777;
    return { mode: mode.toString(8).padStart(3, '0'), groupOrOthers: (mode & 0o077) !== 0, othersRead: (mode & 0o004) !== 0 };
  } catch {
    return null;
  }
}

const ALWAYS_SECRET = /^(?:\.env(?:\..+)?|auth\.json|\.secret_key|\.anthropic_oauth\.json|\.security\.yml|credentials(?:\.json)?)$/i;

/**
 * Archivos de credenciales de la plataforma que existen, con sus permisos. Los archivos de credenciales (.env, auth.json…)
 * cuentan siempre; los de configuración (config.json, config.toml…) solo si de verdad contienen una credencial.
 */
export function secretStores(root, rels) {
  const out = [];
  for (const rel of rels) {
    const abs = path.join(root, rel);
    if (!isFile(abs)) continue;
    if (!ALWAYS_SECRET.test(path.basename(rel))) {
      const r = readRegular(abs);
      if (r.text === undefined || scanSecrets(r.text, { limit: 1 }).length === 0) continue;
    }
    out.push({ abs, rel, perm: permissionInfo(abs) });
  }
  return out;
}

/** Tokens que entran al prompt por archivo (aplicando el tope por archivo). */
export function injectedChars(f) {
  if (!f.present || !f.injected) return 0;
  return f.cap ? Math.min(f.chars, f.cap) : f.chars;
}

export function injectedTokens(files) {
  return estimateTokens(files.reduce((a, f) => a + injectedChars(f), 0));
}

/** Plan de una tarea programada a partir de minutos entre corridas y horas activas. */
export function schedulePlan({ name, kind, everyMin, hoursPerDay = 24, enabled = true, context = 'unknown', model = null, conditional = false }) {
  const ok = enabled && Number.isFinite(everyMin) && everyMin > 0 && hoursPerDay > 0;
  return {
    name,
    kind,
    enabled: ok,
    everyMin: Number.isFinite(everyMin) ? everyMin : null,
    hoursPerDay,
    runsPerDay: ok ? Math.floor((hoursPerDay * 60) / everyMin) : 0,
    context,
    model,
    conditional,
  };
}
