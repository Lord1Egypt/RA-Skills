// Lectura de solo lectura del workspace de un agente OpenClaw.
// No sigue enlaces simbólicos, limita tamaños y cantidad de archivos, y nunca escribe.

import fs from 'node:fs';
import path from 'node:path';

/** Archivos que OpenClaw inyecta en el prompt (docs/concepts/system-prompt, "Workspace bootstrap injection"). */
export const BOOTSTRAP_FILES = ['AGENTS.md', 'SOUL.md', 'IDENTITY.md', 'USER.md', 'BOOTSTRAP.md', 'MEMORY.md'];
/** Archivos de versiones anteriores: se avisan, pero no cuentan como inyectados. */
export const LEGACY_FILES = ['TOOLS.md', 'HEARTBEAT.md', 'memory.md'];

const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_DAILY_LISTED = 2000;
const MAX_DAILY_SCANNED = 400;
const MAX_DAILY_TOTAL_BYTES = 20 * 1024 * 1024;
const MAX_DAILY_DEPTH = 2;

function readRegular(file) {
  let st;
  try {
    st = fs.lstatSync(file);
  } catch {
    return { missing: true };
  }
  if (st.isSymbolicLink()) return { symlink: true };
  if (!st.isFile()) return { missing: true };
  if (st.size > MAX_FILE_BYTES) return { tooLarge: true, bytes: st.size };
  try {
    let text = fs.readFileSync(file, 'utf8');
    if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
    return { text, bytes: st.size };
  } catch {
    return { missing: true };
  }
}

function listDaily(dir, depth, out, stats) {
  let names;
  try {
    names = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const d of names) {
    if (out.length >= MAX_DAILY_LISTED) {
      stats.truncatedList = true;
      return;
    }
    const full = path.join(dir, d.name);
    if (d.isSymbolicLink()) {
      stats.symlinks++;
      continue;
    }
    if (d.isDirectory()) {
      if (depth < MAX_DAILY_DEPTH) listDaily(full, depth + 1, out, stats);
    } else if (d.isFile() && d.name.toLowerCase().endsWith('.md')) {
      out.push(full);
    }
  }
}

export function readWorkspace(dir) {
  const result = {
    dir,
    exists: false,
    files: {},
    legacy: [],
    daily: { count: 0, scannedCount: 0, scannedChars: 0, notes: [], truncatedList: false },
    symlinksSkipped: 0,
  };
  let rootNames;
  try {
    const st = fs.statSync(dir);
    if (!st.isDirectory()) return result;
    rootNames = new Set(fs.readdirSync(dir));
  } catch {
    return result;
  }
  result.exists = true;

  for (const name of BOOTSTRAP_FILES) {
    if (!rootNames.has(name)) {
      result.files[name] = { present: false, chars: 0, bytes: 0, text: '' };
      continue;
    }
    const r = readRegular(path.join(dir, name));
    if (r.symlink) {
      result.symlinksSkipped++;
      result.files[name] = { present: false, symlink: true, chars: 0, bytes: 0, text: '' };
    } else if (r.missing) {
      result.files[name] = { present: false, chars: 0, bytes: 0, text: '' };
    } else if (r.tooLarge) {
      // No se lee completo; para topes cuenta como mayor a cualquier límite razonable.
      result.files[name] = { present: true, tooLarge: true, chars: r.bytes, bytes: r.bytes, text: '' };
    } else {
      result.files[name] = { present: true, chars: r.text.length, bytes: r.bytes, text: r.text };
    }
  }
  for (const name of LEGACY_FILES) if (rootNames.has(name)) result.legacy.push(name);

  // Notas diarias (memory/*.md): no se inyectan, pero pueden contener secretos o instrucciones colocadas desde fuera.
  const memDir = path.join(dir, 'memory');
  const listed = [];
  const stats = { symlinks: 0, truncatedList: false };
  try {
    if (fs.lstatSync(memDir).isDirectory()) listDaily(memDir, 0, listed, stats);
  } catch {
    /* sin carpeta memory */
  }
  result.symlinksSkipped += stats.symlinks;
  result.daily.count = listed.length;
  result.daily.truncatedList = stats.truncatedList;
  listed.sort((a, b) => b.localeCompare(a)); // las más recientes primero (nombres YYYY-MM-DD)
  let bytes = 0;
  for (const file of listed.slice(0, MAX_DAILY_SCANNED)) {
    const r = readRegular(file);
    if (r.text === undefined) continue;
    bytes += r.bytes;
    if (bytes > MAX_DAILY_TOTAL_BYTES) break;
    result.daily.notes.push({ rel: path.relative(dir, file).split(path.sep).join('/'), chars: r.text.length, text: r.text });
    result.daily.scannedChars += r.text.length;
  }
  result.daily.scannedCount = result.daily.notes.length;
  return result;
}
