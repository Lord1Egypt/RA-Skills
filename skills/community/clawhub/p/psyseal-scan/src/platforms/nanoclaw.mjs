// NanoClaw. Se instala clonando su repositorio (la carpeta la elige la persona). Cada grupo de agente vive en
// groups/<carpeta>/ con su CLAUDE.md (instrucciones y memoria, entra completo al contexto) y sus skills;
// las credenciales están en .env en la raíz de la instalación.

import fs from 'node:fs';
import path from 'node:path';
import { expandHome, fileEntry, isDir, isFile, listMarkdown, readMany, secretStores } from './common.mjs';

export const ID = 'nanoclaw';
export const NAME = 'NanoClaw';

export function looksLikeNanoclaw(dir) {
  if (!isDir(path.join(dir, 'groups'))) return false;
  if (isFile(path.join(dir, 'nanoclaw.sh'))) return true;
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
    return typeof pkg?.name === 'string' && /nanoclaw/i.test(pkg.name);
  } catch {
    return false;
  }
}

export function detect({ home, env, cwd }) {
  const candidates = [env.NANOCLAW_DIR && path.resolve(expandHome(env.NANOCLAW_DIR, home)), path.join(home, 'nanoclaw'), path.join(home, 'NanoClaw'), cwd].filter(Boolean);
  const seen = new Set();
  const out = [];
  for (const c of candidates) {
    if (!looksLikeNanoclaw(path.resolve(c))) continue;
    // En Windows y macOS ~/nanoclaw y ~/NanoClaw pueden ser la misma carpeta: se compara la ruta real.
    let real;
    try {
      real = fs.realpathSync.native(c);
    } catch {
      continue;
    }
    const key = process.platform === 'win32' || process.platform === 'darwin' ? real.toLowerCase() : real;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ platform: ID, root: real });
  }
  return out;
}

export function read({ root }) {
  const groupsDir = path.join(root, 'groups');
  let names = [];
  try {
    names = fs.readdirSync(groupsDir, { withFileTypes: true }).filter((d) => d.isDirectory() && !d.name.startsWith('.')).map((d) => d.name);
  } catch {
    /* sin grupos */
  }
  const agents = [];
  for (const n of names.sort().slice(0, 50)) {
    const dir = path.join(groupsDir, n);
    const files = [fileEntry(path.join(dir, 'CLAUDE.md'), `groups/${n}/CLAUDE.md`, 'memory', { injected: true, agentWritten: true })];
    if (!files[0].present && !isDir(path.join(dir, 'skills'))) continue;
    const skillList = isDir(path.join(dir, 'skills')) ? listMarkdown(path.join(dir, 'skills'), { maxDepth: 4 }) : { files: [], symlinks: 0 };
    agents.push({
      id: n,
      label: null,
      root: dir,
      configPath: null,
      configFound: true,
      workspaceExists: true,
      model: null,
      files,
      skills: readMany(root, skillList.files, 'skill'),
      daily: null,
      schedules: [],
      symlinksSkipped: skillList.symlinks + files.filter((f) => f.symlink).length,
      stores: [],
      notes: [],
    });
  }
  const stores = secretStores(root, ['.env']);
  if (agents.length) agents[0].stores = stores;
  return { platform: ID, name: NAME, root, agents, stores: agents.length ? [] : stores, scheduleNote: 'sqlite' };
}
