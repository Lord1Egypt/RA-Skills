// ZeroClaw. Estructura tomada del código y la documentación del proyecto (octubre de 2026):
// ~/.zeroclaw (o ZEROCLAW_CONFIG_DIR) con config.toml y .secret_key; cada agente en agents/<alias>/workspace
// con AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md y USER.md (entran al prompt, tope de 20,000 caracteres por archivo)
// y MEMORY.md/BOOTSTRAP.md (entran solo en algunos turnos). La memoria larga vive en SQLite (data/memory/brain.db),
// con una copia legible en data/memory/MEMORY_SNAPSHOT.md. Latido: [heartbeat] enabled (por defecto false),
// interval_minutes (por defecto 30).

import fs from 'node:fs';
import path from 'node:path';
import { expandHome, fileEntry, isDir, isFile, listMarkdown, readConfigText, readMany, schedulePlan, secretStores } from './common.mjs';
import { toBool, toNumber, tomlGet, tomlSubtables } from './formats.mjs';

export const ID = 'zeroclaw';
export const NAME = 'ZeroClaw';
const FILE_CAP = 20000;
const BOOT = ['AGENTS.md', 'SOUL.md', 'TOOLS.md', 'IDENTITY.md', 'USER.md'];
const CONDITIONAL = ['BOOTSTRAP.md', 'MEMORY.md'];

export function detect({ home, env }) {
  const root = env.ZEROCLAW_CONFIG_DIR ? path.resolve(expandHome(env.ZEROCLAW_CONFIG_DIR, home)) : path.join(home, '.zeroclaw');
  if (isFile(path.join(root, 'config.toml')) || isDir(path.join(root, 'agents')) || isDir(path.join(root, 'data'))) return [{ platform: ID, root }];
  return [];
}

function agentFiles(ws) {
  return [
    ...BOOT.map((n) => fileEntry(path.join(ws, n), n, n === 'USER.md' ? 'memory' : 'boot', { injected: true, cap: FILE_CAP })),
    ...CONDITIONAL.map((n) => fileEntry(path.join(ws, n), n, n === 'MEMORY.md' ? 'memory' : 'boot', { injected: false, cap: FILE_CAP, agentWritten: n === 'MEMORY.md' })),
    fileEntry(path.join(ws, 'HEARTBEAT.md'), 'HEARTBEAT.md', 'task'),
  ];
}

export function read({ root }, { env = {} } = {}) {
  const cfgPath = path.join(root, 'config.toml');
  const toml = readConfigText(cfgPath).text;
  const dataDir = env.ZEROCLAW_WORKSPACE
    ? path.resolve(expandHome(env.ZEROCLAW_WORKSPACE, path.dirname(root)))
    : isDir(path.join(root, 'data'))
      ? path.join(root, 'data')
      : path.join(root, 'workspace');

  const aliases = new Set(tomlSubtables(toml, 'agents'));
  const agentsDir = path.join(root, 'agents');
  if (isDir(agentsDir)) {
    try {
      for (const d of fs.readdirSync(agentsDir, { withFileTypes: true })) if (d.isDirectory() && !d.name.startsWith('.')) aliases.add(d.name);
    } catch {
      /* ilegible */
    }
  }
  const defaultModel = tomlGet(toml, '', 'default_model');
  const hbEnabled = toBool(tomlGet(toml, 'heartbeat', 'enabled')) === true;
  const hbAgent = tomlGet(toml, 'heartbeat', 'agent');
  const hbEvery = toNumber(tomlGet(toml, 'heartbeat', 'interval_minutes')) || 30;

  const agents = [];
  const list = [...aliases].sort().slice(0, 50);
  // Instalaciones antiguas: archivos de personalidad en la carpeta de datos (antes "workspace").
  if (!list.length && BOOT.some((n) => isFile(path.join(dataDir, n)))) list.push(null);

  for (const alias of list) {
    const ws = alias ? path.join(agentsDir, alias, 'workspace') : dataDir;
    const model = (alias && (tomlGet(toml, `agents.${alias}`, 'model') || tomlGet(toml, `agents.${alias}`, 'default_model'))) || defaultModel || null;
    const files = agentFiles(ws);
    const skillRoots = [path.join(ws, 'skills')].filter(isDir);
    const skillLists = skillRoots.map((d) => listMarkdown(d, { maxDepth: 4 }));
    const skills = readMany(ws, skillLists.flatMap((s) => s.files), 'skill');
    const schedules = [];
    if (hbEnabled && (!hbAgent || hbAgent === alias || (!alias && list.length === 1))) {
      const p = schedulePlan({ name: 'heartbeat', kind: 'heartbeat', everyMin: hbEvery, enabled: true, context: 'session', model });
      p.conditional = toBool(tomlGet(toml, 'heartbeat', 'two_phase')) !== false;
      schedules.push(p);
    }
    agents.push({
      id: alias || 'default',
      label: null,
      root: ws,
      configPath: cfgPath,
      configFound: !!toml,
      workspaceExists: isDir(ws),
      model,
      files,
      skills,
      daily: null,
      schedules,
      symlinksSkipped: skillLists.reduce((a, s) => a + s.symlinks, 0) + files.filter((f) => f.symlink).length,
      stores: [],
      notes: [],
    });
  }

  // Copia legible de la memoria compartida (la base SQLite no se abre: no hace falta y evita bloqueos).
  const snapshot = fileEntry(path.join(dataDir, 'memory', 'MEMORY_SNAPSHOT.md'), 'data/memory/MEMORY_SNAPSHOT.md', 'memory', { agentWritten: true });
  if (snapshot.present && agents.length) agents[0].files.push(snapshot);

  const stores = secretStores(root, ['config.toml', '.secret_key', '.env']);
  if (agents.length) agents[0].stores = stores;
  return { platform: ID, name: NAME, root, agents, stores: agents.length ? [] : stores };
}
