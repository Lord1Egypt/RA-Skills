// Modo general: cualquier carpeta de agente que no sea de una plataforma conocida (--path <carpeta>).
// Revisa los archivos Markdown (instrucciones y memoria) en busca de credenciales, instrucciones colocadas
// desde fuera y memoria inflada. No estima costos: sin conocer la plataforma no se sabe qué entra al prompt.

import path from 'node:path';
import { isDir, listMarkdown, readMany, secretStores } from './common.mjs';

export const ID = 'generic';
export const NAME = 'Agent folder'; // el reporte de texto lo traduce (i18n.mjs)

const BOOT_RE = /^(?:agents?|soul|identity|claude|gemini|tools|bootstrap|system|instructions?|persona|rules?)(?:\.[a-z]+)?\.md$/i;
const MEMORY_RE = /^(?:memory|memories|user|history|notes?|context|knowledge)(?:[._-].*)?\.md$/i;

function classify(rel) {
  const base = path.basename(rel);
  const parts = rel.split('/');
  if (parts.some((p) => /^skills?$/i.test(p))) return 'skill';
  if (/^\d{4}-?\d{2}-?\d{2}\.md$/.test(base) || /^\d{8}\.md$/.test(base)) return 'daily';
  if (parts.some((p) => /^(?:memory|memories)$/i.test(p)) || MEMORY_RE.test(base)) return 'memory';
  if (BOOT_RE.test(base)) return 'boot';
  return 'context';
}

export function read({ root }) {
  const list = isDir(root) ? listMarkdown(root, { maxDepth: 3, skipDirs: ['node_modules', '.git', 'dist', 'build', 'vendor'] }) : { files: [], symlinks: 0 };
  const all = readMany(root, list.files, 'context');
  for (const e of all.entries) {
    e.kind = classify(e.rel);
    e.agentWritten = e.kind === 'memory' || e.kind === 'daily';
  }
  const files = all.entries.filter((e) => e.kind !== 'skill' && e.kind !== 'daily');
  const skills = { entries: all.entries.filter((e) => e.kind === 'skill'), listed: 0, scanned: 0 };
  const daily = { entries: all.entries.filter((e) => e.kind === 'daily'), listed: 0, scanned: 0 };
  return {
    platform: ID,
    name: NAME,
    root,
    agents: [
      {
        id: path.basename(root) || root,
        label: null,
        root,
        configPath: null,
        configFound: true,
        workspaceExists: isDir(root),
        model: null,
        files,
        skills,
        daily,
        schedules: [],
        symlinksSkipped: list.symlinks,
        stores: secretStores(root, ['.env', '.env.local']),
        notes: [],
        generic: true,
        listedTruncated: list.truncated,
      },
    ],
  };
}
