// nanobot (HKUDS). Estructura tomada del código y la documentación del proyecto (octubre de 2026):
// ~/.nanobot/config.json (también otras instancias ~/.nanobot-*), workspace con AGENTS.md, SOUL.md y USER.md
// (entran al prompt), memory/MEMORY.md (entra al prompt), HEARTBEAT.md, skills/ y cron/jobs.json.
// Latido: gateway.heartbeat.enabled (por defecto true) cada gateway.heartbeat.intervalS (por defecto 1800 s).

import fs from 'node:fs';
import path from 'node:path';
import { parse as parseJson5 } from '../json5.mjs';
import { expandHome, fileEntry, isDir, isFile, listMarkdown, readConfigText, readMany, schedulePlan, secretStores } from './common.mjs';
import { cronRunsPerDay, toNumber } from './formats.mjs';

export const ID = 'nanobot';
export const NAME = 'nanobot';
const DEFAULT_INTERVAL_S = 1800;
const DEFAULT_MODEL = 'anthropic/claude-opus-4-5';

export function detect({ home }) {
  const out = [];
  let names = [];
  try {
    names = fs.readdirSync(home, { withFileTypes: true }).filter((d) => d.isDirectory() && /^\.nanobot(?:-[A-Za-z0-9_.-]+)?$/.test(d.name)).map((d) => d.name);
  } catch {
    return out;
  }
  for (const n of names.sort()) {
    const root = path.join(home, n);
    if (isFile(path.join(root, 'config.json')) || isDir(path.join(root, 'workspace'))) out.push({ platform: ID, root });
  }
  return out;
}

/** ¿HEARTBEAT.md tiene tareas activas? Solo entonces el latido despierta al agente. */
export function heartbeatHasTasks(text) {
  if (!text) return false;
  const lines = text.split(/\r?\n/);
  let inActive = false;
  for (const l of lines) {
    if (/^#{1,6}\s/.test(l)) {
      inActive = /^#{1,6}\s+active\s+tasks\b/i.test(l);
      continue;
    }
    if (inActive && /^\s*(?:[-*+]|\d+[.)])\s+\S/.test(l) && !/<!--/.test(l)) return true;
  }
  return false;
}

function jobPlan(job, model) {
  const s = job.schedule && typeof job.schedule === 'object' ? job.schedule : {};
  const enabled = job.enabled !== false;
  const name = String(job.name || job.id || 'cron').slice(0, 80);
  if (s.kind === 'every') return schedulePlan({ name, kind: 'cron', everyMin: toNumber(s.everyMs ?? s.every_ms) / 60000, enabled, context: 'session', model });
  if (s.kind === 'cron') {
    const rpd = cronRunsPerDay(s.expr);
    if (!rpd) return null;
    const p = schedulePlan({ name, kind: 'cron', everyMin: 1440 / rpd, enabled, context: 'session', model });
    p.runsPerDay = enabled ? rpd : 0;
    return p;
  }
  return null;
}

export function read({ root }) {
  const home = path.dirname(root);
  const cfgPath = path.join(root, 'config.json');
  const cfgText = readConfigText(cfgPath);
  let cfg = null;
  let configError = null;
  if (cfgText.text) {
    try {
      cfg = parseJson5(cfgText.text);
    } catch {
      configError = 'parse';
    }
  }
  const defaults = cfg?.agents?.defaults || {};
  const ws = typeof defaults.workspace === 'string' ? path.resolve(expandHome(defaults.workspace, home)) : path.join(root, 'workspace');
  const model = (typeof defaults.model === 'string' && defaults.model) || (cfg ? DEFAULT_MODEL : null);

  const files = [
    fileEntry(path.join(ws, 'AGENTS.md'), 'AGENTS.md', 'boot', { injected: true }),
    fileEntry(path.join(ws, 'SOUL.md'), 'SOUL.md', 'boot', { injected: true }),
    fileEntry(path.join(ws, 'USER.md'), 'USER.md', 'memory', { injected: true, agentWritten: true }),
    fileEntry(path.join(ws, 'memory', 'MEMORY.md'), 'memory/MEMORY.md', 'memory', { injected: true, agentWritten: true }),
    fileEntry(path.join(ws, 'HEARTBEAT.md'), 'HEARTBEAT.md', 'task', { agentWritten: true }),
  ];

  const skillList = isDir(path.join(ws, 'skills')) ? listMarkdown(path.join(ws, 'skills'), { maxDepth: 4 }) : { files: [], symlinks: 0 };
  const skills = readMany(ws, skillList.files, 'skill', { agentWritten: true });

  const schedules = [];
  const hb = cfg?.gateway?.heartbeat || {};
  const hbEnabled = hb.enabled !== false;
  const intervalS = toNumber(hb.intervalS ?? hb.interval_s) || DEFAULT_INTERVAL_S;
  const hbFile = files.find((f) => f.rel === 'HEARTBEAT.md');
  if (hbEnabled) {
    const p = schedulePlan({ name: 'heartbeat', kind: 'heartbeat', everyMin: intervalS / 60, enabled: true, context: 'session', model });
    p.conditional = true;
    p.hasTasks = heartbeatHasTasks(hbFile?.text);
    schedules.push(p);
  }
  const jobsText = readConfigText(path.join(ws, 'cron', 'jobs.json')).text;
  if (jobsText) {
    try {
      const data = parseJson5(jobsText);
      const list = Array.isArray(data) ? data : Array.isArray(data?.jobs) ? data.jobs : [];
      for (const j of list) {
        if (!j || typeof j !== 'object' || /heartbeat/i.test(String(j.name || j.id || ''))) continue;
        const p = jobPlan(j, model);
        if (p && p.enabled) schedules.push(p);
      }
    } catch {
      /* jobs.json ilegible: se ignora */
    }
  }

  const agent = {
    id: path.basename(root) === '.nanobot' ? 'main' : path.basename(root).replace(/^\.nanobot-/, ''),
    label: null,
    root: ws,
    configPath: cfgPath,
    configFound: !!cfg,
    configError,
    workspaceExists: isDir(ws),
    model,
    files,
    skills,
    daily: null,
    schedules,
    symlinksSkipped: skillList.symlinks + files.filter((f) => f.symlink).length,
    stores: secretStores(root, ['config.json', '.env']),
    notes: [],
  };
  return { platform: ID, name: NAME, root, agents: [agent] };
}
