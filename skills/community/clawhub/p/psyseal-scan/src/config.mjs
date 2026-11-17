// Lectura (solo lectura) de openclaw.json y resolución de agentes, heartbeat, topes y caché.
// Claves y valores por defecto: documentación oficial de OpenClaw v2026.9.x
// (gateway/heartbeat, gateway/config-agents/*, reference/prompt-caching, concepts/agent-workspace).

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { parse } from './json5.mjs';
import { deepMerge, dig, isPlainObject, parseDurationMinutes } from './util.mjs';

export const DEFAULTS = Object.freeze({
  bootstrapMaxChars: 20000,
  bootstrapTotalMaxChars: 60000,
  userMdMaxChars: 4000,
  heartbeatEveryMin: 30,
  heartbeatEveryMinOauth: 60,
});

const MAX_FILE_BYTES = 2 * 1024 * 1024;
const MAX_INCLUDE_DEPTH = 10;

export function expandHome(p, home) {
  if (typeof p !== 'string') return p;
  if (p === '~') return home;
  if (p.startsWith('~/') || p.startsWith('~\\')) return path.join(home, p.slice(2));
  return p;
}

/** Rutas por defecto de OpenClaw (estado, config, workspace). */
export function resolvePaths({ configPath, workspace, env = process.env, home = os.homedir() } = {}) {
  const profile = env.OPENCLAW_PROFILE && env.OPENCLAW_PROFILE !== 'default' ? env.OPENCLAW_PROFILE : null;
  const stateDir = env.OPENCLAW_STATE_DIR
    ? path.resolve(expandHome(env.OPENCLAW_STATE_DIR, home))
    : path.join(home, profile ? `.openclaw-${profile}` : '.openclaw');
  const cfg = configPath
    ? path.resolve(expandHome(configPath, home))
    : env.OPENCLAW_CONFIG_PATH
      ? path.resolve(expandHome(env.OPENCLAW_CONFIG_PATH, home))
      : path.join(stateDir, 'openclaw.json');
  const defaultWorkspace = env.OPENCLAW_WORKSPACE_DIR
    ? path.resolve(expandHome(env.OPENCLAW_WORKSPACE_DIR, home))
    : path.join(stateDir, 'workspace');
  return {
    home,
    stateDir,
    configPath: cfg,
    defaultWorkspace,
    workspaceOverride: workspace ? path.resolve(expandHome(workspace, home)) : null,
  };
}

function readTextCapped(file) {
  const st = fs.statSync(file);
  if (!st.isFile()) throw new Error('no es un archivo regular');
  if (st.size > MAX_FILE_BYTES) throw new Error('archivo mayor a 2 MB');
  return fs.readFileSync(file, 'utf8');
}

function insideRoots(file, roots) {
  const real = fs.realpathSync(file);
  return roots.some((r) => real === r || real.startsWith(r + path.sep));
}

function resolveIncludes(node, baseDir, roots, depth, seen, warnings) {
  if (Array.isArray(node)) return node.map((x) => resolveIncludes(x, baseDir, roots, depth, seen, warnings));
  if (!isPlainObject(node)) return node;
  const { $include: inc, ...rest } = node;
  const out = {};
  for (const k of Object.keys(rest)) {
    Object.defineProperty(out, k, {
      value: resolveIncludes(rest[k], baseDir, roots, depth, seen, warnings),
      enumerable: true,
      writable: true,
      configurable: true,
    });
  }
  if (inc === undefined) return out;
  if (depth >= MAX_INCLUDE_DEPTH) {
    warnings.push('include-depth');
    return out;
  }
  const list = Array.isArray(inc) ? inc : [inc];
  let merged;
  for (const rel of list) {
    if (typeof rel !== 'string' || rel.includes('\0') || rel.length >= 4096) {
      warnings.push('include-invalid');
      continue;
    }
    const file = path.resolve(baseDir, rel);
    try {
      if (!insideRoots(file, roots)) {
        warnings.push(`include-outside:${rel}`);
        continue;
      }
      const real = fs.realpathSync(file);
      if (seen.has(real)) {
        warnings.push(`include-cycle:${rel}`);
        continue;
      }
      const sub = parse(readTextCapped(file));
      const resolved = resolveIncludes(sub, path.dirname(file), roots, depth + 1, new Set([...seen, real]), warnings);
      merged = merged === undefined ? resolved : deepMerge(merged, resolved);
    } catch (e) {
      warnings.push(`include-error:${rel}:${e.message}`);
    }
  }
  if (merged === undefined) return out;
  // Los archivos incluidos van primero; las claves hermanas los sobrescriben (regla documentada de $include).
  return deepMerge(merged, out);
}

/** Carga openclaw.json. Devuelve { config, warnings, error }. Nunca lanza. */
export function loadConfig(configPath, env = process.env) {
  const warnings = [];
  let text;
  try {
    text = readTextCapped(configPath);
  } catch (e) {
    if (e.code === 'ENOENT') return { config: null, warnings, error: 'not-found' };
    return { config: null, warnings, error: `read:${e.message}` };
  }
  let raw;
  try {
    raw = parse(text);
  } catch (e) {
    return { config: null, warnings, error: `parse:${e.message}` };
  }
  if (!isPlainObject(raw)) return { config: null, warnings, error: 'parse:la raíz no es un objeto' };

  const baseDir = path.dirname(configPath);
  const roots = [fs.realpathSync(baseDir)];
  for (const r of String(env.OPENCLAW_INCLUDE_ROOTS || '').split(path.delimiter)) {
    if (r && path.isAbsolute(r)) {
      try {
        roots.push(fs.realpathSync(r));
      } catch {
        /* ignora raíces inexistentes */
      }
    }
  }
  let config = raw;
  if (JSON.stringify(raw).includes('"$include"')) {
    config = resolveIncludes(raw, baseDir, roots, 0, new Set([fs.realpathSync(configPath)]), warnings);
  }
  return { config, warnings, error: null };
}

/** Texto del modelo: "provider/model" a partir de string u objeto {primary}. */
export function primaryOf(modelField) {
  if (typeof modelField === 'string' && modelField.trim()) return modelField.trim();
  if (isPlainObject(modelField) && typeof modelField.primary === 'string' && modelField.primary.trim()) {
    return modelField.primary.trim();
  }
  return null;
}

/** Cómo se factura Anthropic según auth.profiles de la config: 'api' | 'subscription' | 'mixed' | 'unknown'. */
export function detectBilling(config) {
  const profiles = dig(config, ['auth', 'profiles']);
  if (!isPlainObject(profiles)) return { mode: 'unknown', oauthLike: false };
  let api = false;
  let sub = false;
  for (const [id, p] of Object.entries(profiles)) {
    if (!isPlainObject(p)) continue;
    const provider = String(p.provider || id.split(':')[0] || '').toLowerCase();
    if (provider !== 'anthropic') continue;
    const mode = String(p.mode || '').toLowerCase().replace(/[-_]/g, '');
    if (mode === 'oauth' || mode === 'token') sub = true;
    else if (mode === 'apikey') api = true;
  }
  const mode = api && sub ? 'mixed' : sub ? 'subscription' : api ? 'api' : 'unknown';
  return { mode, oauthLike: sub };
}

function entriesOf(config) {
  const agents = config?.agents;
  if (isPlainObject(agents?.entries)) {
    return Object.entries(agents.entries).map(([id, cfg]) => ({ id, cfg: isPlainObject(cfg) ? cfg : {} }));
  }
  if (Array.isArray(agents?.list)) {
    // Formato anterior de OpenClaw: lista de agentes con id.
    return agents.list
      .filter((a) => isPlainObject(a) && typeof a.id === 'string')
      .map((a) => ({ id: a.id, cfg: a }));
  }
  return [];
}

/**
 * Lista de agentes con workspace, modelo, topes de bootstrap y heartbeat fusionado.
 * Reglas de workspace (docs/concepts/agent-workspace): un solo agente hereda el workspace por defecto;
 * con varios, `<agents.defaults.workspace>/<id>` o `<state>/workspace-<id>`.
 */
export function resolveAgents(config, paths) {
  const cfg = config || {};
  const defaults = isPlainObject(cfg.agents?.defaults) ? cfg.agents.defaults : {};
  let list = entriesOf(cfg);
  const implicit = list.length === 0;
  if (implicit) list = [{ id: 'main', cfg: {} }];
  const multi = list.length > 1;
  const anyHeartbeatBlock = list.some((a) => isPlainObject(a.cfg.heartbeat));

  const ownerId =
    (typeof defaults.heartbeat?.agentId === 'string' && defaults.heartbeat.agentId) ||
    (typeof defaults.systemAgent?.agentId === 'string' && defaults.systemAgent.agentId) ||
    (!multi ? list[0].id : null);

  const defaultsWorkspace = typeof defaults.workspace === 'string' ? path.resolve(expandHome(defaults.workspace, paths.home)) : null;

  return list.map(({ id, cfg: a }) => {
    let workspace;
    if (paths.workspaceOverride && list.length === 1) workspace = paths.workspaceOverride;
    else if (typeof a.workspace === 'string') workspace = path.resolve(expandHome(a.workspace, paths.home));
    else if (!multi) workspace = defaultsWorkspace || paths.defaultWorkspace;
    else if (defaultsWorkspace) workspace = path.join(defaultsWorkspace, id);
    else workspace = path.join(paths.stateDir, `workspace-${id}`);

    const model = primaryOf(a.model) || primaryOf(defaults.model);
    const hasHeartbeatBlock = isPlainObject(a.heartbeat);
    const heartbeat = deepMerge(isPlainObject(defaults.heartbeat) ? defaults.heartbeat : {}, hasHeartbeatBlock ? a.heartbeat : {});
    const runsHeartbeat = anyHeartbeatBlock ? hasHeartbeatBlock : ownerId === id;

    return {
      id,
      implicit,
      workspace,
      model,
      heartbeat,
      hasHeartbeatBlock,
      runsHeartbeat,
      bootstrapMaxChars: Number(a.bootstrapMaxChars ?? defaults.bootstrapMaxChars) || DEFAULTS.bootstrapMaxChars,
      bootstrapTotalMaxChars: Number(a.bootstrapTotalMaxChars ?? defaults.bootstrapTotalMaxChars) || DEFAULTS.bootstrapTotalMaxChars,
      contextInjection: a.contextInjection ?? defaults.contextInjection ?? 'always',
      raw: a,
    };
  });
}

/**
 * cacheRetention efectivo para un agente y modelo. Orden (gana el último), según reference/prompt-caching:
 * defaults.params → defaults.models[m].params → entries.<id>.models[m].params → entries.<id>.params.
 * Sin valor explícito, OpenClaw usa "short" para Anthropic directo; para otros proveedores es desconocido.
 */
export function resolveCacheRetention(config, agent, modelRef, { directAnthropic, env = {} }) {
  const defaults = config?.agents?.defaults || {};
  const layers = [
    dig(defaults, ['params', 'cacheRetention']),
    modelRef ? dig(defaults, ['models', modelRef, 'params', 'cacheRetention']) : undefined,
    modelRef ? dig(agent.raw, ['models', modelRef, 'params', 'cacheRetention']) : undefined,
    dig(agent.raw, ['params', 'cacheRetention']),
  ];
  let value;
  for (const v of layers) if (v === 'none' || v === 'short' || v === 'long') value = v;
  if (value) return { value, explicit: true };
  // Documentado (reference/prompt-caching): OPENCLAW_CACHE_RETENTION=long sin valor explícito sube a 1 h solo en api.anthropic.com / Vertex.
  const fromEnv = String(dig(config, ['env', 'vars', 'OPENCLAW_CACHE_RETENTION']) ?? env.OPENCLAW_CACHE_RETENTION ?? '').toLowerCase();
  if (directAnthropic && fromEnv === 'long') return { value: 'long', explicit: false, viaEnv: true };
  return { value: directAnthropic ? 'short' : null, explicit: false };
}

/** Plan de heartbeat de un agente: cadencia, ventana activa y banderas que afectan el costo. */
export function resolveHeartbeat(config, agent, billing) {
  const hb = agent.heartbeat || {};
  const cronOff = config?.cron?.enabled === false;
  const everyRaw = hb.every;
  const unset = everyRaw === undefined || everyRaw === null;
  let everyMin = unset ? null : parseDurationMinutes(everyRaw);
  if (unset) everyMin = billing.oauthLike ? DEFAULTS.heartbeatEveryMinOauth : DEFAULTS.heartbeatEveryMin;
  const invalidEvery = !unset && everyMin === null;
  if (invalidEvery) everyMin = DEFAULTS.heartbeatEveryMin;

  const hours = activeHoursPerDay(hb.activeHours);
  let enabled = agent.runsHeartbeat && !cronOff && everyMin > 0 && hours > 0;
  let reason = null;
  if (!agent.runsHeartbeat) reason = 'not-owner';
  else if (cronOff) reason = 'cron-disabled';
  else if (everyMin <= 0) reason = 'every-zero';
  else if (hours <= 0) reason = 'zero-width-window';

  const runsPerDay = enabled ? Math.floor((hours * 60) / everyMin) : 0;
  return {
    enabled,
    reason,
    everyMin,
    everyExplicit: !unset,
    invalidEvery,
    hoursPerDay: hours,
    activeHoursSet: isPlainObject(hb.activeHours),
    runsPerDay,
    isolatedSession: hb.isolatedSession === true,
    lightContext: hb.lightContext === true,
    model: typeof hb.model === 'string' && hb.model.trim() ? hb.model.trim() : null,
    target: hb.target ?? 'owner',
  };
}

function toMinutes(hhmm) {
  const m = /^\s*(\d{1,2}):(\d{2})\s*$/.exec(String(hhmm));
  if (!m) return null;
  return Number(m[1]) * 60 + Number(m[2]);
}

/** Horas activas por día (24 si no hay ventana). */
export function activeHoursPerDay(activeHours) {
  if (!isPlainObject(activeHours)) return 24;
  const s = toMinutes(activeHours.start);
  const e = toMinutes(activeHours.end);
  if (s === null || e === null) return 24;
  if (s === e) return 0;
  const span = e > s ? e - s : 1440 - s + e;
  return span / 60;
}
