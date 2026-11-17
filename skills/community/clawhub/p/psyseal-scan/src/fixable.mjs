// Qué hallazgos sabe arreglar la limpieza y con qué operación. Lo usan el escáner (para decir cuántos se pueden
// arreglar) y la limpieza (para armar el plan), así los dos cuentan igual.

const FILE_KINDS_REDACT = new Set(['boot', 'memory', 'daily', 'skill', 'context']);
const FILE_KINDS_QUARANTINE = new Set(['memory', 'daily']);

/**
 * @param {object} f hallazgo del reporte
 * @param {string} platform plataforma del agente (openclaw, hermes, …, generic)
 * @returns {Array<{ op: string, target?: string, args?: object, risk: 'safe'|'behavior' }>}
 */
export function opsFor(f, platform, { winNative = process.platform === 'win32' } = {}) {
  const d = f.data || {};
  switch (f.id) {
    case 'secret.exposed':
      return d.abs && FILE_KINDS_REDACT.has(d.fileKind) ? [{ op: 'redact', target: d.abs, risk: 'safe' }] : [];
    case 'inject.critical':
    case 'inject.override':
    case 'inject.hidden':
      return d.abs && FILE_KINDS_QUARANTINE.has(d.fileKind) ? [{ op: 'quarantine', target: d.abs, args: { strict: d.strict !== false }, risk: 'safe' }] : [];
    case 'memory.bloat': {
      if (!d.abs) return [];
      const ops = [];
      if (d.dupLines > 0) ops.push({ op: 'dedupe', target: d.abs, risk: 'safe' });
      if (d.blobLines + d.bigFences > 0 && platform !== 'generic') ops.push({ op: 'archive', target: d.abs, args: { platform }, risk: 'safe' });
      return ops;
    }
    case 'perm.secret_file_open':
      return d.abs && !winNative ? [{ op: 'chmod600', target: d.abs, risk: 'safe' }] : [];
    case 'bootstrap.leftover':
      return d.abs ? [{ op: 'remove-file', target: d.abs, risk: 'behavior' }] : [];
    case 'heartbeat.full_history':
      return platform === 'openclaw' ? [{ op: 'openclaw-isolate', risk: 'behavior' }] : [];
    case 'heartbeat.no_active_hours':
      return platform === 'openclaw' ? [{ op: 'openclaw-active-hours', risk: 'behavior' }] : [];
    case 'schedule.frequent': {
      if (d.kind !== 'heartbeat' || !d.configPath) return [];
      if (d.platform === 'nanobot') return [{ op: 'json-set', target: d.configPath, args: { keys: ['gateway', 'heartbeat', 'intervalS'], value: 3600 }, risk: 'behavior' }];
      if (d.platform === 'picoclaw') return [{ op: 'json-set', target: d.configPath, args: { keys: ['heartbeat', 'interval'], value: 60 }, risk: 'behavior' }];
      if (d.platform === 'zeroclaw') return [{ op: 'toml-set', target: d.configPath, args: { table: 'heartbeat', key: 'interval_minutes', value: 60 }, risk: 'behavior' }];
      return [];
    }
    default:
      return [];
  }
}

/** Cuántos hallazgos (no informativos) tienen al menos una operación de limpieza. */
export function countFixable(report) {
  let n = 0;
  for (const a of report.agents || []) for (const f of a.findings) if (f.severity !== 'info' && opsFor(f, a.platform).length) n++;
  for (const f of report.globalFindings || []) if (f.severity !== 'info' && opsFor(f, f.data?.platform || 'openclaw').length) n++;
  return n;
}
