#!/usr/bin/env node

import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const DEFAULT_CATALOG_URL = 'https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json';
const DEFAULT_SOUL_SOURCE = 'https://docs.openclaw.ai/reference/templates/SOUL.md';
const CHECKLIST_FILE = 'PRE-PUBLISH-CHECKLIST.md';
const USER_AGENT = 'openclaw-soul/0.1.0';
const FETCH_TIMEOUT_MS = 15000;

const workspaceDir = process.cwd();
const soulFile = path.join(workspaceDir, 'SOUL.md');
const dataDir = path.join(workspaceDir, 'soul-data');
const cacheDir = path.join(dataDir, 'cache');
const backupDir = path.join(dataDir, 'backups');
const stateFile = path.join(dataDir, 'state.json');
const cacheFile = path.join(cacheDir, 'agents.json');

const stateDefaults = {
  catalogUrl: DEFAULT_CATALOG_URL,
  lastFetchedAt: null,
  current: {
    id: 'openclaw-default',
    category: 'builtin',
    sourceUrl: DEFAULT_SOUL_SOURCE,
    appliedAt: null,
    checksum: null,
    custom: false
  }
};

function sha1(text) {
  return crypto.createHash('sha1').update(text, 'utf8').digest('hex');
}

function parseCatalogUrl(url, label) {
  if (typeof url !== 'string' || !url.trim()) {
    throw new Error(`Invalid ${label}: ${url}`);
  }
  try {
    return new URL(url);
  } catch {
    return null;
  }
}

function normalizeRelativeSoulPath(relPath) {
  if (typeof relPath !== 'string' || !relPath.trim()) {
    throw new Error('Catalog agent path must be a non-empty string.');
  }
  return relPath.trim();
}

function localWorkspacePath(input) {
  const resolved = path.resolve(workspaceDir, input);
  if (!resolved.startsWith(workspaceDir + path.sep) && resolved !== workspaceDir) {
    throw new Error(`Local path escapes workspace: ${input}`);
  }
  return resolved;
}

export async function ensureDirs() {
  await fs.mkdir(cacheDir, { recursive: true });
  await fs.mkdir(backupDir, { recursive: true });
}

export async function readJson(file, fallback) {
  try {
    return JSON.parse(await fs.readFile(file, 'utf8'));
  } catch {
    return fallback;
  }
}

export async function writeAtomic(file, content) {
  const dir = path.dirname(file);
  const base = path.basename(file);
  const temp = path.join(dir, `.${base}.${process.pid}.${Date.now()}.tmp`);
  await fs.writeFile(temp, content, 'utf8');
  await fs.rename(temp, file);
}

export async function writeJson(file, value) {
  await writeAtomic(file, JSON.stringify(value, null, 2) + '\n');
}

export function validateCatalog(catalog) {
  if (!catalog || typeof catalog !== 'object' || Array.isArray(catalog)) {
    throw new Error('Catalog must be a JSON object.');
  }
  if (!Array.isArray(catalog.agents)) {
    throw new Error('Catalog must contain an agents array.');
  }

  const ids = new Set();
  const agents = catalog.agents.map((agent, index) => {
    if (!agent || typeof agent !== 'object' || Array.isArray(agent)) {
      throw new Error(`Catalog agent at index ${index} must be an object.`);
    }
    const id = typeof agent.id === 'string' ? agent.id.trim() : '';
    const category = typeof agent.category === 'string' ? agent.category.trim() : '';
    const relPath = normalizeRelativeSoulPath(agent.path);
    if (!id) throw new Error(`Catalog agent at index ${index} is missing id.`);
    if (!category) throw new Error(`Catalog agent ${id} is missing category.`);
    const lowerId = id.toLowerCase();
    if (ids.has(lowerId)) throw new Error(`Duplicate catalog agent id: ${id}`);
    ids.add(lowerId);
    return {
      ...agent,
      id,
      category,
      path: relPath,
      name: typeof agent.name === 'string' ? agent.name.trim() : '',
      role: typeof agent.role === 'string' ? agent.role.trim() : ''
    };
  });

  return { ...catalog, agents };
}

export async function fetchRemoteText(url) {
  const parsed = parseCatalogUrl(url, 'URL');
  if (!parsed) {
    throw new Error(`Expected remote URL, got local path: ${url}`);
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(parsed.toString(), {
      headers: {
        'user-agent': USER_AGENT,
        'accept': 'application/json, text/plain;q=0.9, */*;q=0.8'
      },
      signal: controller.signal
    });
    if (!res.ok) throw new Error(`Fetch failed: ${res.status} ${res.statusText} for ${parsed}`);
    return await res.text();
  } catch (err) {
    if (err?.name === 'AbortError') {
      throw new Error(`Fetch timed out after ${FETCH_TIMEOUT_MS}ms for ${parsed}`);
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

export async function readLocalText(url) {
  const resolved = localWorkspacePath(url);
  return await fs.readFile(resolved, 'utf8');
}

export async function fetchText(url) {
  const parsed = parseCatalogUrl(url, 'URL');
  return parsed ? fetchRemoteText(url) : readLocalText(url);
}

export async function loadState() {
  const state = { ...stateDefaults, ...(await readJson(stateFile, stateDefaults)) };
  state.current = state.current && typeof state.current === 'object'
    ? { ...stateDefaults.current, ...state.current }
    : stateDefaults.current;
  return state;
}

export async function saveState(state) {
  await writeJson(stateFile, state);
}

export async function loadCatalog(force = false) {
  const state = await loadState();
  const cached = !force ? await readJson(cacheFile, null) : null;
  if (cached?.agents?.length) return { catalog: validateCatalog(cached), state, source: 'cache' };

  let parsed;
  try {
    parsed = JSON.parse(await fetchText(state.catalogUrl));
  } catch (err) {
    if (err instanceof SyntaxError) throw new Error('Catalog fetch succeeded, but JSON parsing failed.');
    throw err;
  }

  const catalog = validateCatalog(parsed);
  state.lastFetchedAt = new Date().toISOString();
  await Promise.all([writeJson(cacheFile, catalog), saveState(state)]);
  return { catalog, state, source: 'remote' };
}

export function byCategory({ agents = [] }) {
  const map = new Map();
  for (const agent of agents) {
    const category = agent.category || 'uncategorized';
    map.set(category, [...(map.get(category) || []), agent]);
  }
  return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

export function findAgent({ agents = [] }, id) {
  const needle = id.toLowerCase();
  return agents.find(a => [a.id, a.name].some(v => v?.toLowerCase() === needle));
}

export function searchAgents({ agents = [] }, text) {
  const needle = text.toLowerCase();
  return agents.filter(a => [a.id, a.name, a.category, a.role].some(v => v?.toLowerCase().includes(needle)));
}

export function buildRawSoulUrl(state, agent) {
  const relPath = normalizeRelativeSoulPath(agent.path || '');
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(relPath)) {
    return relPath;
  }
  if (/^(?:\.|\.|\/)/.test(relPath) || relPath.includes('/./') || relPath.includes('/../')) {
    return localWorkspacePath(relPath);
  }
  const parsed = parseCatalogUrl(state.catalogUrl, 'catalogUrl');
  const rawRoot = new URL('.', parsed);
  const resolved = new URL(relPath, rawRoot);
  return resolved.toString();
}

export function validateSoulContent(content, sourceUrl) {
  const text = typeof content === 'string' ? content.trim() : '';
  if (!text) throw new Error(`Fetched soul content is empty: ${sourceUrl}`);
  if (!(text.startsWith('#') || text.startsWith('---') || text.includes('\n# '))) {
    throw new Error(`Fetched content does not look like a SOUL.md file: ${sourceUrl}`);
  }
  return content;
}

export async function backupCurrentSoul() {
  try {
    const current = await fs.readFile(soulFile, 'utf8');
    const timestamp = new Date().toISOString().replaceAll(':', '-');
    const backupPath = path.join(backupDir, `SOUL-${timestamp}.md`);
    await writeAtomic(backupPath, current);
    return backupPath;
  } catch {
    return null;
  }
}

export async function listBackups() {
  try {
    const files = await fs.readdir(backupDir);
    return files.filter(name => name.startsWith('SOUL-') && name.endsWith('.md')).sort().reverse();
  } catch {
    return [];
  }
}

export async function currentSoul(state) {
  const current = state.current;
  if (!current?.custom && !current?.sourceUrl) {
    return {
      id: 'openclaw-default',
      category: 'builtin',
      sourceUrl: DEFAULT_SOUL_SOURCE,
      appliedAt: null,
      checksum: null,
      custom: false
    };
  }

  if (current?.custom) {
    return current;
  }

  if (!current?.checksum) {
    return current;
  }

  try {
    const live = await fs.readFile(soulFile, 'utf8');
    const checksum = sha1(live);
    if (checksum !== current.checksum) {
      return {
        ...current,
        id: 'custom',
        category: 'local',
        custom: true,
        note: `custom, from ${current.sourceUrl} (modified)`
      };
    }
  } catch {
    return {
      ...current,
      id: 'custom',
      category: 'local',
      custom: true,
      note: `custom, from ${current.sourceUrl} (modified)`
    };
  }

  return current;
}

export function print(text) {
  console.log(text);
}

export async function showHelp() {
  const state = await loadState();
  const active = await currentSoul(state);
  const label = active?.id ? `${active.id} (${active.category || 'unknown'})` : 'none recorded';
  print(`Current soul: ${label}\n\nCommands:\n  soul categories\n  soul list <category>\n  soul show <id>\n  soul apply <id>\n  soul current\n  soul restore\n  soul refresh\n  soul search <text>`);
}

export async function main() {
  const [subcommand = '', ...rest] = process.argv.slice(2).map(arg => arg.trim());
  await ensureDirs();

  if (!subcommand) return showHelp();

  if (subcommand === 'current') {
    const state = await loadState();
    const active = await currentSoul(state);
    if (active?.note) return print(active.note);
    return print(active
      ? `Current soul:\n- id: ${active.id}\n- category: ${active.category}\n- source: ${active.sourceUrl}\n- appliedAt: ${active.appliedAt ?? 'never'}`
      : 'No recorded applied soul yet.');
  }

  if (subcommand === 'restore') {
    const state = await loadState();
    const backups = await listBackups();
    const latest = backups[0];
    if (!latest) return print('No backup found in soul-data/backups/.');
    const backupPath = path.join(backupDir, latest);
    const content = validateSoulContent(await fs.readFile(backupPath, 'utf8'), backupPath);
    state.current = {
      id: 'custom',
      category: 'local',
      sourceUrl: backupPath,
      appliedAt: new Date().toISOString(),
      checksum: sha1(content),
      custom: true
    };
    await Promise.all([writeAtomic(soulFile, content), saveState(state)]);
    return print(`Restored SOUL.md from backup:\n- ${backupPath}\n\nStart a new session or use /new to fully apply the restored soul.`);
  }

  const { catalog, state, source } = await loadCatalog(subcommand === 'refresh');

  if (subcommand === 'refresh') {
    return print(`Catalog refreshed from ${source}:\n- url: ${state.catalogUrl}\n- agents: ${catalog.agents.length}\n- fetchedAt: ${state.lastFetchedAt}`);
  }

  if (subcommand === 'categories') {
    return print(byCategory(catalog).map(([category, list]) => `- ${category} (${list.length})`).join('\n'));
  }

  if (subcommand === 'list') {
    const category = (rest[0] || '').toLowerCase();
    if (!category) return print('Usage: soul list <category>\n\nTip: run `soul categories` first.');
    const matches = catalog.agents.filter(a => a.category.toLowerCase() === category);
    return print(matches.length
      ? matches.map(a => `- ${a.id} — ${a.role || a.name || a.id}`).join('\n')
      : `No souls found for category: ${category}`);
  }

  if (subcommand === 'search') {
    const text = rest.join(' ').trim();
    if (!text) return print('Usage: soul search <text>');
    const matches = searchAgents(catalog, text).slice(0, 40);
    return print(matches.length
      ? matches.map(a => `- ${a.id} [${a.category}]${a.role ? ` — ${a.role}` : ''}`).join('\n')
      : `No souls found matching: ${text}`);
  }

  if (subcommand === 'show') {
    const id = rest[0] || '';
    if (!id) return print('Usage: soul show <id>');
    const agent = findAgent(catalog, id);
    if (!agent) return print(`Soul not found: ${id}`);
    return print(`Soul:\n- id: ${agent.id}\n- category: ${agent.category}\n- name: ${agent.name || '(none)'}\n- role: ${agent.role || '(none)'}\n- source: ${buildRawSoulUrl(state, agent)}`);
  }

  if (subcommand === 'apply') {
    const id = rest[0] || '';
    if (!id) return print('Usage: soul apply <id>');
    const agent = findAgent(catalog, id);
    if (!agent) return print(`Soul not found: ${id}`);
    const sourceUrl = buildRawSoulUrl(state, agent);
    const content = validateSoulContent(await fetchText(sourceUrl), sourceUrl);
    const checksum = sha1(content);
    const backupPath = await backupCurrentSoul();
    state.current = {
      id: agent.id,
      category: agent.category,
      name: agent.name || null,
      role: agent.role || null,
      sourceUrl,
      appliedAt: new Date().toISOString(),
      checksum,
      custom: false,
      agentId: agent.id
    };
    await Promise.all([writeAtomic(soulFile, content), saveState(state)]);
    return print(`Applied soul:\n- id: ${agent.id}\n- category: ${agent.category}\n- source: ${sourceUrl}${backupPath ? `\n- backup: ${backupPath}` : ''}\n\nStart a new session or use /new to fully apply the new soul.`);
  }

  print(`Unknown subcommand: ${subcommand}\n\nRun: soul`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch((err) => {
    console.error(err?.message || String(err));
    process.exit(1);
  });
}
