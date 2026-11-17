// Presentación del reporte en texto (es/en) y JSON. Solo formatea datos que ya vienen sin contenido sensible.
import { STR } from './i18n.mjs';
import { BRAND } from './brand.mjs';
import { fmtInt, fmtUsd } from './util.mjs';
import { escapeInvisibleJson, safeDeep } from './safe.mjs';

const SEV_RANK = { high: 0, medium: 1, low: 2, info: 3 };
const PRIORITY = [
  'secret.exposed',
  'inject.critical',
  'config.secret_plaintext',
  'perm.secret_file_open',
  'heartbeat.full_history',
  'heartbeat.cache_expires',
  'schedule.frequent',
  'inject.override',
  'inject.hidden',
  'bootstrap.file_truncated',
  'memory.over_limit',
  'bootstrap.file_cut_by_total',
  'memory.bloat',
  'weight.heavy_file',
  'memory.near_full',
  'heartbeat.expensive_model',
  'heartbeat.no_active_hours',
  'heartbeat.bootstrap_each_run',
  'bootstrap.leftover',
  'bootstrap.near_cap',
];
const prio = (id) => {
  const i = PRIORITY.indexOf(id);
  return i === -1 ? PRIORITY.length : i;
};

export function renderJson(report) {
  return escapeInvisibleJson(JSON.stringify(report, null, 2));
}

function groupFindings(findings) {
  const map = new Map();
  for (const f of findings) {
    if (!map.has(f.id)) map.set(f.id, []);
    map.get(f.id).push(f);
  }
  return [...map.entries()]
    .map(([id, items]) => ({ id, items, severity: items.reduce((m, f) => (SEV_RANK[f.severity] < SEV_RANK[m] ? f.severity : m), 'info') }))
    .sort((a, b) => SEV_RANK[a.severity] - SEV_RANK[b.severity] || prio(a.id) - prio(b.id));
}

function pad(s, n) {
  s = String(s);
  return s.length >= n ? s : s + ' '.repeat(n - s.length);
}
function padL(s, n) {
  s = String(s);
  return s.length >= n ? s : ' '.repeat(n - s.length) + s;
}

function rowState(S, r, lang) {
  if (r.overFileCap) return S.stTrunc(fmtInt(r.chars - r.cap, lang));
  if (r.cutByTotal) return S.stCutTotal;
  if (r.nearCap) return S.stNear;
  if (r.fillPct !== null && r.fillPct !== undefined) return S.stFill(r.fillPct);
  if (r.injectedEveryTurn === false) return S.stNotEveryTurn;
  return S.stOk;
}

function bootTable(S, boot, lang) {
  const rows = boot.rows.filter((r) => r.present);
  if (!rows.length) return [`  (${S.noBootFiles})`];
  const head = [S.colFile, S.colChars, S.colTokens, S.colCap, S.colState];
  const body = rows.map((r) => [r.name, fmtInt(r.chars, lang), fmtInt(r.tokens, lang), r.cap ? fmtInt(r.cap, lang) : '—', rowState(S, r, lang)]);
  const widths = head.map((h, i) => Math.max(h.length, ...body.map((b) => String(b[i]).length)));
  const line = (cols) => '  ' + cols.map((c, i) => (i === 0 || i === 4 ? pad(c, widths[i]) : padL(c, widths[i]))).join('  ');
  return [line(head), ...body.map(line)];
}

function hbSection(S, a, lang) {
  const out = [];
  const { plan, economics: e } = a.heartbeat;
  if (!e.applicable) {
    out.push('  ' + (S.hbOff[e.reason] || S.hbOff['not-owner']));
    return out;
  }
  out.push('  ' + S.hbLine(plan, e));
  out.push('  ' + S.hbNow(e));

  const priced = e.priced;
  const head = S.hbTableHead(priced);
  const rows = e.rows.map((r) => {
    const label = r.sessionTokens ? S.hbTokens(r.sessionTokens) : lang === 'es' ? 'aislada' : 'isolated';
    if (priced) {
      const iso = r.isolateLight ? `${fmtRange(r.isolateLight.monthLow, r.isolateLight.monthHigh)}` : '—';
      const lon = r.cacheLong ? fmtUsd(r.cacheLong.month) : '—';
      return [label, `≈${fmtUsd(r.nowMonth)}`, iso, lon];
    }
    const [lo, hi] = [r.isolateLight?.promptLow ?? 2000, r.isolateLight?.promptHigh ?? 5000];
    return [label, fmtInt(r.promptTokens, lang), e.alreadyLean ? '—' : `${fmtInt(lo, lang)}–${fmtInt(hi, lang)}`, ''];
  });
  const cols = head.filter((h) => h !== '').length;
  const widths = head.slice(0, cols).map((h, i) => Math.max(h.length, ...rows.map((r) => String(r[i]).length)));
  const fmt = (cells) => '    ' + cells.slice(0, cols).map((c, i) => (i === 0 ? pad(c, widths[i]) : padL(c, widths[i]))).join('   ');
  out.push(fmt(head));
  for (const r of rows) out.push(fmt(r));

  if (e.billing === 'subscription') out.push('  ' + S.hbSubscription);
  else if (!priced) out.push('  ' + S.hbUnpriced(e.modelRef));
  if (priced && !e.alreadyLean) out.push('  ' + S.hbNoteLevers);
  if (!e.state.isolatedSession && e.rows.length > 1) out.push('  ' + S.hbNoteSession);
  return out;
}

function scheduleSection(S, a, install) {
  const out = [];
  if (install?.scheduleNote === 'sqlite') return ['  ' + S.scheduleSqlite];
  if (!a.schedules.length) return ['  ' + S.noSchedules];
  for (const s of a.schedules) out.push('  ' + S.scheduleLine(s));
  if (a.schedules.some((s) => s.active)) out.push('  ' + S.scheduleNote);
  return out;
}

function fmtRange(a, b) {
  return Math.round(a) === Math.round(b) ? `≈${fmtUsd(a)}` : `≈${fmtUsd(a)}–${fmtUsd(b)}`;
}

function usageSection(S, u) {
  const out = [];
  if (!u.recognized) return ['  ' + S.usageUnrecognized];
  out.push('  ' + S.usageLine(u));
  out.push('  ' + S.usageMix(u.shares));
  if (u.cacheWriteDominates) out.push('  ! ' + S.usageCacheWrite);
  else if (u.lowCacheHit) out.push('  ! ' + S.usageHit(u.cacheHitRate));
  if (u.missingCostEntries > 0) out.push('  ! ' + S.usageMissing(u.missingCostEntries));
  if (u.incompleteTotals) out.push('  ! ' + S.usageIncomplete(u.cacheStatus));
  return out;
}

/** Plega el texto a ASCII para terminales viejas (cmd/PowerShell con páginas de códigos antiguas). Solo es de presentación. */
export function toAscii(text) {
  return String(text)
    .replace(/≈/g, '~')
    .replace(/[—–]/g, '-')
    .replace(/·/g, '|')
    .replace(/→/g, '->')
    .replace(/×/g, 'x')
    .replace(/…/g, '...')
    .replace(/[¿¡]/g, '')
    .replace(/[“”«»]/g, '"')
    .replace(/[‘’]/g, "'")
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^\x09\x0a\x0d\x20-\x7e]/g, '?');
}

export function renderText(rawReport, { lang = 'es', cta = true, ascii = false } = {}) {
  // Todo texto que viene del disco o de la config (rutas, nombres, ids) se muestra en una línea y sin caracteres de control.
  const report = safeDeep(rawReport);
  const S = STR[lang] || STR.es;
  const L = [];
  L.push(S.header(report.tool.version));
  if (report.notFound) {
    L.push('');
    L.push(...S.notFound(report.notFound));
    L.push('');
    L.push(S.footerPrivacy);
    const early = L.join('\n') + '\n';
    return ascii ? toAscii(early) : early;
  }

  const allGroups = [];
  const installs = report.installs || [];
  const multiAgent = report.agents.length > 1;
  const multiPlatform = new Set(installs.map((i) => i.platform)).size > 1;
  const tag = (a) => (multiPlatform ? `${a.platformName} · ${a.id}` : a.id);
  for (const inst of installs) {
    L.push(S.installLine(inst, report.inputs.billing));
    L.push('');
    const agents = report.agents.filter((a) => a.platform === inst.platform && inst.agentIds.includes(a.id));
    for (const a of agents) {
      L.push(S.agentLine(a));
      L.push('');
      L.push(a.bootstrap.generic ? S.secBootGeneric : S.secBoot);
      L.push(...bootTable(S, a.bootstrap, lang));
      if (a.bootstrap.generic) L.push('  ' + S.bootTotalGeneric(a.bootstrap.rows.filter((r) => r.present).length));
      else L.push('  ' + S.bootTotal(fmtInt(a.bootstrap.injectedTokens, lang), fmtInt(a.bootstrap.injectedTotalChars, lang)));
      L.push('');
      if (a.platform === 'openclaw') {
        L.push(S.secHb);
        L.push(...hbSection(S, a, lang));
        L.push('');
      } else if (!a.bootstrap.generic) {
        L.push(S.secSchedules);
        L.push(...scheduleSection(S, a, inst));
        L.push('');
      }
      for (const g of groupFindings(a.findings)) allGroups.push({ ...g, agent: multiAgent ? tag(a) : null });
    }
  }

  for (const g of groupFindings(report.globalFindings)) allGroups.push({ ...g, agent: null });
  allGroups.sort((a, b) => SEV_RANK[a.severity] - SEV_RANK[b.severity] || prio(a.id) - prio(b.id));

  L.push(S.secFindings);
  let printed = 0;
  const firsts = [];
  const seenFix = new Set();
  for (const g of allGroups) {
    const render = S.f[g.id];
    if (!render) continue;
    const { head, fix } = render(g.items);
    if (!head) continue;
    printed++;
    const prefix = g.agent ? `[${g.agent}] ` : '';
    L.push(`  [${S.sev[g.severity]}] ${prefix}${head}`);
    if (fix) L.push(`         → ${fix}`);
    if (fix && g.severity !== 'info' && !seenFix.has(fix)) {
      seenFix.add(fix);
      firsts.push({ id: g.id, fix });
    }
  }
  if (!printed) L.push('  ' + S.noFindings);
  L.push('');

  if (firsts.length) {
    L.push(S.secFirst);
    firsts.slice(0, 3).forEach((f, i) => L.push(`  ${i + 1}. ${f.fix}`));
    L.push('');
  }

  if (report.usage) {
    L.push(S.secUsage);
    L.push(...usageSection(S, report.usage));
    L.push('');
  }

  L.push(S.footerEstimates(report.inputs.pricesAsOf));
  L.push(installs.some((i) => i.platform === 'openclaw') ? S.footerVerify : S.footerVerifyGeneric);
  L.push(S.footerPrivacy);
  if (cta && BRAND.url) {
    L.push('');
    L.push(S.cta(BRAND.name, BRAND.url, report.summary.fixable || 0));
  }
  const out = L.join('\n') + '\n';
  return ascii ? toAscii(out) : out;
}
