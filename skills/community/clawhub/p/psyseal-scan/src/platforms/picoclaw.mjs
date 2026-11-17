// PicoClaw (Sipeed). Estructura tomada del código y la documentación del proyecto:
// ~/.picoclaw (o PICOCLAW_HOME), config en ~/.picoclaw/config.json (o PICOCLAW_CONFIG), workspace en
// agents.defaults.workspace (por defecto ~/.picoclaw/workspace) con AGENT.md/AGENTS.md, SOUL.md, USER.md,
// IDENTITY.md, memory/MEMORY.md y notas diarias memory/AAAAMM/AAAAMMDD.md (entran las de los últimos 3 días).
// Latido: heartbeat.enabled (por defecto true) cada heartbeat.interval minutos (por defecto 30, mínimo 5).

import path from 'node:path';
import { parse as parseJson5 } from '../json5.mjs';
import { expandHome, fileEntry, isDir, isFile, listMarkdown, readConfigText, readMany, schedulePlan, secretStores } from './common.mjs';
import { toBool, toNumber } from './formats.mjs';

export const ID = 'picoclaw';
export const NAME = 'PicoClaw';
const RECENT_DAYS_INJECTED = 3;

export function detect({ home, env }) {
  const root = env.PICOCLAW_HOME ? path.resolve(expandHome(env.PICOCLAW_HOME, home)) : path.join(home, '.picoclaw');
  const cfg = env.PICOCLAW_CONFIG ? path.resolve(expandHome(env.PICOCLAW_CONFIG, home)) : path.join(root, 'config.json');
  if (isFile(cfg) || isDir(path.join(root, 'workspace'))) return [{ platform: ID, root, configPath: cfg }];
  return [];
}

function resolveModel(cfg) {
  const d = cfg?.agents?.defaults || {};
  const name = (typeof d.model_name === 'string' && d.model_name) || (typeof d.model === 'string' && d.model) || null;
  if (!name) return null;
  const list = Array.isArray(cfg?.model_list) ? cfg.model_list : [];
  const hit = list.find((m) => m && m.model_name === name);
  if (hit && typeof hit.model === 'string') {
    if (hit.model.includes('/')) return hit.model;
    return typeof hit.provider === 'string' && hit.provider ? `${hit.provider}/${hit.model}` : hit.model;
  }
  return name;
}

export function read({ root, configPath }, { env = {} } = {}) {
  const home = path.dirname(root);
  const cfgText = readConfigText(configPath);
  let cfg = null;
  let configError = null;
  if (cfgText.text) {
    try {
      cfg = parseJson5(cfgText.text);
    } catch {
      configError = 'parse';
    }
  }
  const wsCfg = env.PICOCLAW_AGENTS_DEFAULTS_WORKSPACE || cfg?.agents?.defaults?.workspace;
  const ws = typeof wsCfg === 'string' && wsCfg ? path.resolve(expandHome(wsCfg, home)) : path.join(root, 'workspace');
  const model = resolveModel(cfg);

  const agentFile = isFile(path.join(ws, 'AGENT.md')) ? 'AGENT.md' : 'AGENTS.md';
  const files = [
    fileEntry(path.join(ws, agentFile), agentFile, 'boot', { injected: true }),
    fileEntry(path.join(ws, 'SOUL.md'), 'SOUL.md', 'boot', { injected: true }),
    fileEntry(path.join(ws, 'IDENTITY.md'), 'IDENTITY.md', 'boot', { injected: true }),
    fileEntry(path.join(ws, 'USER.md'), 'USER.md', 'memory', { injected: true, agentWritten: true }),
    fileEntry(path.join(ws, 'memory', 'MEMORY.md'), 'memory/MEMORY.md', 'memory', { injected: true, agentWritten: true }),
    fileEntry(path.join(ws, 'HEARTBEAT.md'), 'HEARTBEAT.md', 'task', { agentWritten: true }),
  ];

  // Notas diarias: memory/AAAAMM/AAAAMMDD.md. Las de los últimos días entran al prompt.
  const memDir = path.join(ws, 'memory');
  const dailyList = isDir(memDir) ? listMarkdown(memDir, { maxDepth: 1 }) : { files: [], symlinks: 0 };
  const dailyAbs = dailyList.files.filter((f) => /^\d{8}\.md$/.test(path.basename(f)));
  const daily = readMany(ws, dailyAbs, 'daily', { agentWritten: true });
  daily.entries.sort((a, b) => b.rel.localeCompare(a.rel));
  daily.entries.slice(0, RECENT_DAYS_INJECTED).forEach((e) => {
    e.injected = true;
  });

  const skillList = isDir(path.join(ws, 'skills')) ? listMarkdown(path.join(ws, 'skills'), { maxDepth: 4 }) : { files: [], symlinks: 0 };
  const skills = readMany(ws, skillList.files, 'skill', { agentWritten: true });

  const schedules = [];
  const hb = cfg?.heartbeat || {};
  const envEnabled = toBool(env.PICOCLAW_HEARTBEAT_ENABLED);
  const enabled = envEnabled !== null ? envEnabled : hb.enabled !== false;
  let every = toNumber(env.PICOCLAW_HEARTBEAT_INTERVAL) ?? toNumber(hb.interval) ?? 30;
  if (every < 5) every = 5;
  if (enabled) {
    const p = schedulePlan({ name: 'heartbeat', kind: 'heartbeat', everyMin: every, enabled: true, context: 'session', model });
    p.conditional = true;
    p.hasTasks = !!files.find((f) => f.rel === 'HEARTBEAT.md' && f.present && f.text.trim());
    schedules.push(p);
  }

  return {
    platform: ID,
    name: NAME,
    root,
    agents: [
      {
        id: 'main',
        label: null,
        root: ws,
        configPath,
        configFound: !!cfg,
        configError,
        workspaceExists: isDir(ws),
        model,
        files,
        skills,
        daily,
        schedules,
        symlinksSkipped: skillList.symlinks + dailyList.symlinks + files.filter((f) => f.symlink).length,
        stores: secretStores(root, [path.relative(root, configPath) || 'config.json', 'auth.json', '.security.yml']).filter((s) => !s.rel.startsWith('..')),
        notes: [],
      },
    ],
  };
}

export const _test = { resolveModel };
