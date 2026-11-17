// Hermes Agent (Nous Research). Estructura tomada del código y la documentación del proyecto (octubre de 2026):
// ~/.hermes (o HERMES_HOME) con config.yaml, .env, auth.json, SOUL.md, memories/MEMORY.md y memories/USER.md
// (con tope de caracteres), skills/ (las escribe el propio agente), cron/jobs.json y perfiles en profiles/<nombre>.

import fs from 'node:fs';
import path from 'node:path';
import { parse as parseJson5 } from '../json5.mjs';
import { expandHome, fileEntry, isDir, listMarkdown, readConfigText, readMany, schedulePlan, secretStores } from './common.mjs';
import { cronRunsPerDay, toBool, toNumber, yamlGet } from './formats.mjs';

export const ID = 'hermes';
export const NAME = 'Hermes Agent';
const MEMORY_LIMIT = 2200;
const USER_LIMIT = 1375;

export function detect({ home, env }) {
  const root = env.HERMES_HOME ? path.resolve(expandHome(env.HERMES_HOME, home)) : path.join(home, '.hermes');
  if (!isDir(root)) return [];
  const looksLike = ['config.yaml', 'memories', 'SOUL.md', 'skills', 'state.db', '.env'].some((n) => fs.existsSync(path.join(root, n)));
  return looksLike ? [{ platform: ID, root }] : [];
}

function readJobs(text) {
  let data;
  try {
    data = parseJson5(text);
  } catch {
    return { jobs: [], error: true };
  }
  const list = Array.isArray(data) ? data : Array.isArray(data?.jobs) ? data.jobs : data && typeof data === 'object' ? Object.values(data.jobs || {}) : [];
  return { jobs: list.filter((j) => j && typeof j === 'object'), error: false };
}

function jobPlan(job, mainModel, cronModel) {
  const paused = String(job.state || '').trim() === 'paused' || !!job.paused_at;
  const enabled = job.enabled !== false && !paused && !job.no_agent;
  const sch = job.schedule && typeof job.schedule === 'object' ? job.schedule : {};
  let everyMin = null;
  let runsPerDay = null;
  if (sch.kind === 'interval') everyMin = toNumber(sch.minutes);
  else if (sch.kind === 'cron') runsPerDay = cronRunsPerDay(sch.expr);
  else return null; // "once" o desconocido: no es recurrente
  const name = String(job.name || job.id || 'cron').slice(0, 80);
  const model = (typeof job.model === 'string' && job.model) || cronModel || mainModel || null;
  if (runsPerDay !== null) {
    const p = schedulePlan({ name, kind: 'cron', everyMin: runsPerDay > 0 ? 1440 / runsPerDay : null, enabled, context: 'fresh', model });
    p.runsPerDay = enabled ? runsPerDay : 0;
    return p;
  }
  return schedulePlan({ name, kind: 'cron', everyMin, enabled, context: 'fresh', model });
}

function readAgent(id, h, isProfile) {
  const cfg = readConfigText(path.join(h, 'config.yaml'));
  const yaml = cfg.text;
  const model = yamlGet(yaml, ['model', 'default']) || yamlGet(yaml, ['model']) || null;
  const provider = yamlGet(yaml, ['model', 'provider']);
  const modelRef = model && provider && !model.includes('/') ? `${provider}/${model}` : model;
  const memOn = toBool(yamlGet(yaml, ['memory', 'memory_enabled'])) !== false;
  const memCap = toNumber(yamlGet(yaml, ['memory', 'memory_char_limit'])) || MEMORY_LIMIT;
  const userCap = toNumber(yamlGet(yaml, ['memory', 'user_char_limit'])) || USER_LIMIT;
  const cronModel = yamlGet(yaml, ['cron', 'model']);

  const files = [
    fileEntry(path.join(h, 'SOUL.md'), 'SOUL.md', 'boot', { injected: true }),
    fileEntry(path.join(h, 'memories', 'MEMORY.md'), 'memories/MEMORY.md', 'memory', { injected: memOn, cap: memCap, capKind: 'limit', agentWritten: true }),
    fileEntry(path.join(h, 'memories', 'USER.md'), 'memories/USER.md', 'memory', { injected: memOn, cap: userCap, capKind: 'limit', agentWritten: true }),
  ];

  const skillList = isDir(path.join(h, 'skills')) ? listMarkdown(path.join(h, 'skills'), { maxDepth: 4 }) : { files: [], symlinks: 0 };
  const skills = readMany(h, skillList.files, 'skill', { agentWritten: true });

  const schedules = [];
  const jobsText = readConfigText(path.join(h, 'cron', 'jobs.json')).text;
  let jobsError = false;
  if (jobsText) {
    const { jobs, error } = readJobs(jobsText);
    jobsError = error;
    for (const j of jobs) {
      const p = jobPlan(j, modelRef, cronModel);
      if (p && p.enabled) schedules.push(p);
    }
  }

  return {
    id,
    label: isProfile ? `perfil ${id}` : id,
    root: h,
    configPath: path.join(h, 'config.yaml'),
    configFound: !!yaml,
    model: modelRef,
    files,
    skills,
    daily: null,
    schedules,
    symlinksSkipped: skillList.symlinks + files.filter((f) => f.symlink).length,
    stores: secretStores(h, ['.env', 'auth.json', '.anthropic_oauth.json']),
    notes: jobsError ? [{ id: 'schedule.unreadable', data: { file: 'cron/jobs.json' } }] : [],
  };
}

export function read({ root }) {
  const agents = [readAgent('default', root, false)];
  const profilesDir = path.join(root, 'profiles');
  if (isDir(profilesDir)) {
    let names = [];
    try {
      names = fs.readdirSync(profilesDir, { withFileTypes: true }).filter((d) => d.isDirectory() && !d.name.startsWith('.')).map((d) => d.name);
    } catch {
      /* sin perfiles legibles */
    }
    for (const n of names.slice(0, 50)) agents.push(readAgent(n, path.join(profilesDir, n), true));
  }
  return { platform: ID, name: NAME, root, agents };
}
