// Orquestador: encuentra los agentes de las plataformas conocidas, los lee (solo lectura), corre los detectores
// y arma el reporte (objeto plano). El reporte NO contiene texto de los archivos ni valores de credenciales:
// solo conteos, rutas, líneas y tipos.

import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { detectBilling, loadConfig, resolveAgents, resolveHeartbeat, resolvePaths } from './config.mjs';
import { readWorkspace } from './workspace.mjs';
import { analyzeBootstrap } from './detectors/bootstrap.mjs';
import { analyzeBloat } from './detectors/memory.mjs';
import { scanConfigSecrets, scanSecrets } from './detectors/secrets.mjs';
import { scanInjection } from './detectors/injection.mjs';
import { ASSUMPTIONS, heartbeatEconomics, trimValue } from './cost.mjs';
import { costOf, resolvePricing, PRICES_AS_OF, PRICES_SOURCE } from './pricing.mjs';
import { analyzeUsage, parseUsage } from './usage.mjs';
import { estimateTokens } from './util.mjs';
import { ADAPTERS, PLATFORM_NAMES, generic, nanoclaw } from './platforms/index.mjs';
import { injectedChars, isDir, isFile, listMarkdown, readMany } from './platforms/common.mjs';
import { countFixable } from './fixable.mjs';

/** Huella del estado de un agente: cambia si cambia cualquier archivo que se revisó. No revela su contenido. */
function fingerprint(items) {
  const lines = items
    .filter((x) => x && typeof x.text === 'string' && x.rel)
    .map((x) => `${x.rel}\u0000${crypto.createHash('sha256').update(x.text).digest('hex')}`)
    .sort();
  return crypto.createHash('sha256').update('psyseal-state-v1\n' + lines.join('\n')).digest('hex');
}

export const VERSION = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8')).version;

const SEVERITY_RANK = { high: 0, medium: 1, low: 2, info: 3 };
const EXTERNAL_CONTENT_FILES = new Set(['MEMORY.md', 'USER.md']); // contenido que entra desde conversaciones y herramientas
const OWNER_FILES = new Set(['AGENTS.md', 'SOUL.md', 'IDENTITY.md', 'BOOTSTRAP.md']);
const HEAVY_FILE_CHARS = 20000; // archivo sin tope que entra completo en cada mensaje
const FREQUENT_RUNS_PER_DAY = 48; // cada 30 minutos o más seguido

function detectHarness(config, agent) {
  const vals = [config?.agents?.defaults?.agentRuntime, config?.agents?.defaults?.runtime?.type, agent?.raw?.agentRuntime, agent?.raw?.runtime?.type];
  return vals.some((v) => typeof v === 'string' && /codex/i.test(v)) ? 'codex' : 'standard';
}

function sortFindings(list) {
  return list.sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity]);
}

/* ------------------------------------------------------------------ OpenClaw */

function scanOpenClaw(opts, env, home) {
  const paths = resolvePaths({ configPath: opts.config, workspace: opts.workspace, env, home });
  const loaded = loadConfig(paths.configPath, env);
  const config = loaded.config;

  const billing =
    opts.billing && opts.billing !== 'auto' ? { mode: opts.billing, oauthLike: opts.billing === 'subscription' } : detectBilling(config);

  let agents = resolveAgents(config, paths);
  const allAgentIds = agents.map((a) => a.id);
  if (opts.agent) agents = agents.filter((a) => a.id === opts.agent);
  if (paths.workspaceOverride) {
    const first = agents[0] || resolveAgents(null, paths)[0];
    agents = [{ ...first, workspace: paths.workspaceOverride }];
  }

  // Sin config, sin carpeta de estado y sin workspace: no hay OpenClaw aquí.
  const absent =
    loaded.error === 'not-found' && !paths.workspaceOverride && !fs.existsSync(paths.stateDir) && !agents.some((a) => fs.existsSync(a.workspace));
  if (absent) return { absent: true, paths };

  const priceOverride = opts.price || null;
  const globalFindings = [];
  if (opts.agent && !paths.workspaceOverride && agents.length === 0) {
    globalFindings.push({ id: 'agent.not_found', severity: 'medium', data: { id: opts.agent, available: allAgentIds.slice(0, 20) } });
  }
  if (loaded.error === 'not-found') globalFindings.push({ id: 'config.missing', severity: 'info', data: { path: paths.configPath } });
  else if (loaded.error) globalFindings.push({ id: 'config.error', severity: 'medium', data: { path: paths.configPath, error: String(loaded.error).slice(0, 300) } });
  if (loaded.warnings.length) globalFindings.push({ id: 'config.include_warnings', severity: 'info', data: { warnings: loaded.warnings.slice(0, 10) } });

  if (config) {
    for (const s of scanConfigSecrets(config)) {
      globalFindings.push({ id: 'config.secret_plaintext', severity: 'medium', data: { path: s.path, type: s.label, length: s.length } });
    }
  }

  const agentReports = agents.map((agent) => scanOpenClawAgent({ agent, config, billing, opts, priceOverride, env, stateDir: paths.stateDir }));
  return {
    absent: false,
    paths,
    loaded,
    billing,
    install: { platform: 'openclaw', name: PLATFORM_NAMES.openclaw, root: paths.stateDir, configPath: paths.configPath, configFound: !loaded.error },
    globalFindings,
    agents: agentReports,
  };
}

function scanOpenClawAgent({ agent, config, billing, opts, priceOverride, env, stateDir }) {
  const findings = [];
  const ws = readWorkspace(agent.workspace);
  const model = agent.model;
  const pricing = resolvePricing(model, { config, override: priceOverride });
  const harness = detectHarness(config, agent);

  if (!ws.exists) findings.push({ id: 'workspace.missing', severity: 'medium', data: { path: agent.workspace } });

  // 1) Peso del arranque
  const boot = analyzeBootstrap(ws, { bootstrapMaxChars: agent.bootstrapMaxChars, bootstrapTotalMaxChars: agent.bootstrapTotalMaxChars });
  for (const r of boot.rows) {
    if (r.overFileCap) {
      findings.push({ id: 'bootstrap.file_truncated', severity: 'medium', data: { file: r.name, chars: r.chars, cap: r.cap, lostChars: r.chars - r.cap } });
    } else if (r.cutByTotal) {
      findings.push({ id: 'bootstrap.file_cut_by_total', severity: 'medium', data: { file: r.name, chars: r.chars } });
    } else if (r.nearCap) {
      findings.push({ id: 'bootstrap.near_cap', severity: 'low', data: { file: r.name, chars: r.chars, cap: r.cap } });
    }
  }
  const boots = ws.files['BOOTSTRAP.md'];
  if (boots?.present && boots.chars > 0) {
    findings.push({ id: 'bootstrap.leftover', severity: 'low', data: { abs: path.join(agent.workspace, 'BOOTSTRAP.md'), chars: boots.chars, tokens: estimateTokens(Math.min(boots.chars, agent.bootstrapMaxChars)) } });
  }
  if (ws.legacy.length) findings.push({ id: 'bootstrap.legacy_files', severity: 'low', data: { files: ws.legacy } });
  if (ws.symlinksSkipped) findings.push({ id: 'workspace.symlinks_skipped', severity: 'info', data: { count: ws.symlinksSkipped } });

  // 2) Memoria inflada (MEMORY.md)
  const mem = ws.files['MEMORY.md'];
  if (mem?.present && mem.text) bloatFinding(findings, 'MEMORY.md', mem.text, pricing, path.join(agent.workspace, 'MEMORY.md'));

  // 3) Credenciales en texto plano + 4) instrucciones sospechosas
  const textSources = [];
  for (const [name, f] of Object.entries(ws.files)) if (f.present && f.text) textSources.push({ file: name, text: f.text, kind: EXTERNAL_CONTENT_FILES.has(name) ? 'memory' : 'boot' });
  for (const n of ws.daily.notes) textSources.push({ file: n.rel, text: n.text, daily: true, kind: 'daily' });
  for (const src of textSources) {
    const abs = path.join(agent.workspace, ...src.file.split('/'));
    secretFindings(findings, src.file, src.text, abs, src.kind);
    const strict = src.daily || EXTERNAL_CONTENT_FILES.has(src.file);
    if (!strict && !OWNER_FILES.has(src.file)) continue;
    injectionFindings(findings, src.file, src.text, strict, { abs, fileKind: src.kind });
  }

  // Skills del workspace y las compartidas de la instalación
  const skillDirs = [path.join(agent.workspace, 'skills'), stateDir && path.join(stateDir, 'skills')].filter((d) => d && isDir(d));
  const seenSkill = new Set();
  const skillTexts = [];
  for (const d of skillDirs) {
    const listed = listMarkdown(d, { maxDepth: 4 });
    const read = readMany(path.dirname(d), listed.files.filter((f) => !seenSkill.has(f)), 'skill');
    listed.files.forEach((f) => seenSkill.add(f));
    skillFindings(findings, read.entries);
    for (const e of read.entries) if (e.present && e.text) skillTexts.push({ rel: `${path.dirname(d) === agent.workspace ? '' : 'shared/'}${e.rel}`, text: e.text });
  }

  // 5) Latido
  const plan = resolveHeartbeat(config, agent, billing);
  const bootstrapTokens = boot.injectedTokens;
  const econ = heartbeatEconomics({ agent, plan, config, billing, bootstrapTokens, sessionTokens: opts.sessionTokens, priceOverride, env });

  if (!plan.enabled) {
    findings.push({ id: 'heartbeat.disabled', severity: 'info', data: { reason: plan.reason } });
  } else {
    if (plan.invalidEvery) findings.push({ id: 'heartbeat.invalid_every', severity: 'low', data: {} });
    if (!plan.isolatedSession) {
      findings.push({
        id: 'heartbeat.full_history',
        severity: econ.headline && econ.headline.savingHigh >= 50 ? 'high' : 'medium',
        data: { everyMin: plan.everyMin, runsPerDay: plan.runsPerDay, savingLow: econ.headline?.savingLow ?? null, savingHigh: econ.headline?.savingHigh ?? null, priced: econ.priced },
      });
    } else if (!plan.lightContext && bootstrapTokens >= 3000) {
      findings.push({ id: 'heartbeat.bootstrap_each_run', severity: 'low', data: { tokens: bootstrapTokens } });
    }
    const shortGap = econ.retention.value === 'short' && plan.everyMin > 5 && econ.directAnthropic;
    if (shortGap && !plan.isolatedSession) {
      findings.push({ id: 'heartbeat.cache_expires', severity: 'medium', data: { everyMin: plan.everyMin, explicit: econ.retention.explicit, canFix: plan.everyMin <= 60 } });
    }
    if (econ.cheaperModel) {
      findings.push({ id: 'heartbeat.expensive_model', severity: 'low', data: { model: econ.modelRef, cheaper: econ.cheaperModel.name, ratio: Math.round(econ.cheaperModel.ratio) } });
    }
    if (!plan.activeHoursSet && plan.runsPerDay >= 24) findings.push({ id: 'heartbeat.no_active_hours', severity: 'low', data: { runsPerDay: plan.runsPerDay } });
    if (!econ.pricing) findings.push({ id: 'heartbeat.price_unknown', severity: 'info', data: { model: econ.modelRef } });
  }
  if (harness === 'codex') findings.push({ id: 'harness.codex', severity: 'info', data: {} });

  return {
    id: agent.id,
    platform: 'openclaw',
    platformName: PLATFORM_NAMES.openclaw,
    workspace: agent.workspace,
    workspaceExists: ws.exists,
    model,
    pricing: pricing ? { name: pricing.name, source: pricing.source, exact: pricing.exact } : null,
    harness,
    bootstrap: boot,
    dailyNotes: { count: ws.daily.count, scanned: ws.daily.scannedCount, truncatedList: ws.daily.truncatedList },
    heartbeat: { plan: { ...plan }, economics: econ },
    root: agent.workspace,
    fingerprint: fingerprint([...textSources.map((t) => ({ rel: t.file, text: t.text })), ...skillTexts]),
    findings: sortFindings(findings),
  };
}

/* ------------------------------------------------------------------ detectores comunes */

function bloatFinding(findings, file, text, pricing, abs) {
  const bloat = analyzeBloat(text);
  if (bloat.reclaimableChars >= 1000) {
    findings.push({
      id: 'memory.bloat',
      severity: 'low',
      data: {
        file,
        abs,
        dupLines: bloat.dupLines,
        blobLines: bloat.blobLines,
        bigFences: bloat.bigFences,
        reclaimableChars: bloat.reclaimableChars,
        reclaimableTokens: bloat.reclaimableTokens,
        perThousandCalls: trimValue(pricing, bloat.reclaimableTokens),
      },
    });
  }
}

function secretFindings(findings, file, text, abs, fileKind) {
  for (const s of scanSecrets(text)) {
    findings.push({ id: 'secret.exposed', severity: 'high', data: { file, abs, fileKind, line: s.line, type: s.label, kind: s.id, length: s.length } });
  }
}

function injectionFindings(findings, file, text, strict, { skill = false, abs = null, fileKind = null } = {}) {
  for (const s of scanInjection(text, { strict })) {
    // En skills son comunes las instrucciones de instalación (curl … | sh): se marcan para revisar, no como alarma.
    const severity = s.cls === 'critical' && !skill ? 'high' : 'medium';
    findings.push({ id: `inject.${s.cls}`, severity, data: { file, abs, fileKind: skill ? 'skill' : fileKind, strict, line: s.line, signal: s.id, count: s.count } });
  }
}

/** Skills instaladas (por ejemplo desde un registro público): credenciales y órdenes peligrosas. */
function skillFindings(findings, entries) {
  for (const f of entries) {
    if (!f.present || !f.text) continue;
    secretFindings(findings, f.rel, f.text, f.abs, 'skill');
    injectionFindings(findings, f.rel, f.text, false, { skill: true, abs: f.abs });
  }
}

/* ------------------------------------------------------------------ otras plataformas */

function weightRows(files) {
  return files
    .filter((f) => f.kind !== 'task' && f.kind !== 'skill')
    .map((f) => {
      const injected = injectedChars(f);
      const truncating = f.cap && f.capKind === 'truncate';
      return {
        name: f.rel,
        present: !!f.present,
        injectedEveryTurn: !!f.injected,
        chars: f.chars,
        cap: f.cap,
        capKind: f.cap ? f.capKind : null,
        injectedChars: injected,
        tokens: estimateTokens(injected),
        overFileCap: !!(truncating && f.chars > f.cap),
        cutByTotal: false,
        nearCap: !!(truncating && f.present && f.chars > f.cap * 0.8 && f.chars <= f.cap),
        fillPct: f.cap && f.capKind === 'limit' ? Math.round((f.chars / f.cap) * 100) : null,
      };
    });
}

function scheduleCost(plan, injectedTok, pricing) {
  const perRunTokens = injectedTok + ASSUMPTIONS.isolatedOverheadTokens;
  const runsPerMonth = plan.runsPerDay * ASSUMPTIONS.daysPerMonth;
  const out = { perRunTokens, runsPerMonth, monthTokens: perRunTokens * runsPerMonth, perRunUsd: null, monthUsd: null };
  if (pricing && runsPerMonth > 0) {
    out.perRunUsd = costOf(pricing, { input: perRunTokens, output: ASSUMPTIONS.heartbeatOutputTokens });
    out.monthUsd = out.perRunUsd * runsPerMonth;
  }
  return out;
}

function analyzeAgent(install, agent, opts) {
  const findings = [];
  const pricing = resolvePricing(agent.model, { config: null, override: opts.price || null });
  if (agent.workspaceExists === false) findings.push({ id: 'workspace.missing', severity: 'medium', data: { path: agent.root } });
  if (agent.generic) findings.push({ id: 'platform.generic', severity: 'info', data: {} });

  const injectedDaily = (agent.daily?.entries || []).filter((e) => e.injected);
  const rows = weightRows([...agent.files, ...injectedDaily]);
  const injectedTotalChars = rows.reduce((a, r) => a + r.injectedChars, 0);
  const injectedTok = estimateTokens(injectedTotalChars);

  for (const f of agent.files) {
    if (!f.present) continue;
    if (f.cap && f.capKind === 'truncate') {
      if (f.chars > f.cap) findings.push({ id: 'bootstrap.file_truncated', severity: 'medium', data: { file: f.rel, chars: f.chars, cap: f.cap, lostChars: f.chars - f.cap } });
      else if (f.chars > f.cap * 0.8) findings.push({ id: 'bootstrap.near_cap', severity: 'low', data: { file: f.rel, chars: f.chars, cap: f.cap } });
    } else if (f.cap && f.capKind === 'limit') {
      if (f.chars > f.cap) findings.push({ id: 'memory.over_limit', severity: 'medium', data: { file: f.rel, chars: f.chars, cap: f.cap } });
      else if (f.chars >= f.cap * 0.9) findings.push({ id: 'memory.near_full', severity: 'low', data: { file: f.rel, chars: f.chars, cap: f.cap, pct: Math.round((f.chars / f.cap) * 100) } });
    } else if (f.injected && f.chars > HEAVY_FILE_CHARS) {
      findings.push({ id: 'weight.heavy_file', severity: 'low', data: { file: f.rel, chars: f.chars, tokens: estimateTokens(f.chars) } });
    }
    if (f.kind === 'memory' && f.text) bloatFinding(findings, f.rel, f.text, pricing, f.abs);
  }

  // Credenciales e instrucciones sospechosas en todo lo que se lee.
  const sources = [...agent.files, ...(agent.daily?.entries || []), ...(agent.skills?.entries || [])].filter((f) => f.present && f.text);
  for (const f of sources) {
    if (f.kind === 'skill') continue;
    secretFindings(findings, f.rel, f.text, f.abs, f.kind);
    const strict = (f.kind === 'memory' || f.kind === 'daily') && f.agentWritten;
    if (f.kind === 'context' && !agent.generic) continue;
    injectionFindings(findings, f.rel, f.text, strict, { abs: f.abs, fileKind: f.kind });
  }
  skillFindings(findings, agent.skills?.entries || []);

  for (const s of agent.stores || []) {
    if (s.perm?.groupOrOthers) findings.push({ id: 'perm.secret_file_open', severity: 'medium', data: { file: s.rel, abs: s.abs, mode: s.perm.mode, othersRead: s.perm.othersRead } });
  }
  if (agent.symlinksSkipped) findings.push({ id: 'workspace.symlinks_skipped', severity: 'info', data: { count: agent.symlinksSkipped } });
  for (const n of agent.notes || []) findings.push({ id: n.id, severity: 'info', data: n.data });

  const schedules = agent.schedules.map((p) => {
    const active = !p.conditional || p.hasTasks !== false;
    const cost = active ? scheduleCost(p, injectedTok, resolvePricing(p.model || agent.model, { config: null, override: opts.price || null })) : null;
    if (active && p.runsPerDay >= FREQUENT_RUNS_PER_DAY) {
      findings.push({
        id: 'schedule.frequent',
        severity: 'low',
        data: { platform: install.platform, configPath: agent.configPath || null, name: p.name, kind: p.kind, everyMin: p.everyMin, runsPerDay: p.runsPerDay, perRunTokens: cost.perRunTokens, monthUsd: cost.monthUsd },
      });
    }
    return { ...p, active, cost };
  });

  return {
    id: agent.id,
    platform: install.platform,
    platformName: install.name,
    workspace: agent.root,
    workspaceExists: agent.workspaceExists !== false,
    model: agent.model,
    pricing: pricing ? { name: pricing.name, source: pricing.source, exact: pricing.exact } : null,
    bootstrap: { rows, injectedTotalChars, injectedTokens: injectedTok, generic: !!agent.generic },
    schedules,
    skills: { count: agent.skills?.entries?.length || 0 },
    root: agent.root,
    fingerprint: fingerprint(sources),
    findings: sortFindings(findings),
  };
}

/** Qué plataforma es una carpeta que la persona señala con --path. */
function adapterForPath(dir) {
  if (isFile(path.join(dir, 'openclaw.json'))) return { openclaw: true };
  if (nanoclaw.looksLikeNanoclaw(dir)) return { adapter: nanoclaw, ref: { platform: 'nanoclaw', root: dir } };
  // Las demás plataformas se reconocen por su carpeta de instalación (~/.hermes, ~/.nanobot, ~/.picoclaw, ~/.zeroclaw).
  for (const a of ADAPTERS) {
    if (a.ID === 'nanoclaw') continue;
    const found = a.detect({ home: path.dirname(dir), env: {}, cwd: dir }).find((r) => path.resolve(r.root) === dir);
    if (found) return { adapter: a, ref: found };
  }
  if (isDir(path.join(dir, 'memories')) && isFile(path.join(dir, 'SOUL.md'))) {
    return { adapter: ADAPTERS.find((a) => a.ID === 'hermes'), ref: { platform: 'hermes', root: dir } };
  }
  return { adapter: generic, ref: { platform: 'generic', root: dir } };
}

/**
 * @param {object} opts { config, workspace, agent, lang, billing, sessionTokens, price, usageText, env, home, cwd, platform, path }
 */
export function runScan(opts = {}) {
  const env = opts.env ?? process.env;
  const home = opts.home ?? os.homedir();
  const cwd = opts.cwd ?? process.cwd();
  const want = opts.platform && opts.platform !== 'auto' ? opts.platform : null;

  const installs = [];
  const agents = [];
  const globalFindings = [];
  let oc = null;

  let pathTarget = null;
  if (opts.path) pathTarget = adapterForPath(path.resolve(opts.path));

  // OpenClaw
  const ocEnv = pathTarget?.openclaw ? { ...env, OPENCLAW_STATE_DIR: path.resolve(opts.path) } : env;
  if ((pathTarget ? pathTarget.openclaw : !want || want === 'openclaw')) {
    oc = scanOpenClaw(opts, ocEnv, home);
    if (!oc.absent) {
      installs.push({ ...oc.install, agentIds: oc.agents.map((a) => a.id) });
      agents.push(...oc.agents);
      globalFindings.push(...oc.globalFindings);
    }
  }

  // Otras plataformas
  const refs = [];
  if (pathTarget && !pathTarget.openclaw) refs.push({ adapter: pathTarget.adapter, ref: pathTarget.ref });
  else if (!pathTarget) {
    for (const a of ADAPTERS) {
      if (want && want !== a.ID) continue;
      for (const ref of a.detect({ home, env, cwd })) refs.push({ adapter: a, ref });
    }
  }
  for (const { adapter, ref } of refs) {
    let inst;
    try {
      inst = adapter.read(ref, { env });
    } catch (e) {
      globalFindings.push({ id: 'platform.read_error', severity: 'medium', data: { platform: adapter.ID, root: ref.root, error: String(e?.message || e).slice(0, 200) } });
      continue;
    }
    let list = inst.agents;
    if (opts.agent) list = list.filter((a) => a.id === opts.agent);
    const reports = list.map((a) => analyzeAgent(inst, a, opts));
    for (const s of inst.stores || []) {
      if (s.perm?.groupOrOthers) globalFindings.push({ id: 'perm.secret_file_open', severity: 'medium', data: { file: s.rel, abs: s.abs, mode: s.perm.mode, othersRead: s.perm.othersRead, platform: inst.platform } });
    }
    if (!inst.agents.length) globalFindings.push({ id: 'platform.no_agents', severity: 'info', data: { platform: inst.platform, root: inst.root } });
    installs.push({ platform: inst.platform, name: inst.name, root: inst.root, agentIds: reports.map((r) => r.id), scheduleNote: inst.scheduleNote || null });
    agents.push(...reports);
  }

  const notFound = installs.length === 0 ? { platform: process.platform, configPath: oc?.paths?.configPath ?? null, stateDir: oc?.paths?.stateDir ?? null, searched: want ? [want] : ['openclaw', ...ADAPTERS.map((a) => a.ID)] } : null;

  let usage = null;
  if (opts.usageText) {
    const parsed = parseUsage(opts.usageText);
    usage = parsed ? { ...analyzeUsage(parsed), recognized: true } : { recognized: false };
  }

  const all = [...globalFindings, ...agents.flatMap((a) => a.findings.map((f) => ({ ...f, agent: a.id })))];
  const counts = { high: 0, medium: 0, low: 0, info: 0 };
  for (const f of all) counts[f.severity]++;

  const report = {
    tool: { name: 'psyseal-scan', version: VERSION },
    inputs: {
      configPath: oc && !oc.absent ? oc.paths.configPath : null,
      configFound: !!(oc && !oc.absent && !oc.loaded.error),
      configError: oc && !oc.absent && oc.loaded.error && oc.loaded.error !== 'not-found' ? oc.loaded.error : null,
      billing: oc && !oc.absent ? oc.billing.mode : 'unknown',
      usageProvided: !!opts.usageText,
      pricesAsOf: PRICES_AS_OF,
      pricesSource: PRICES_SOURCE,
    },
    notFound,
    installs,
    globalFindings,
    agents,
    usage,
    summary: { counts, total: all.length, fixable: 0 },
  };
  report.summary.fixable = countFixable(report);
  return report;
}
