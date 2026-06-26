import { spawnSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { extname, join, dirname } from 'node:path';
import { cwd } from 'node:process';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const PAGE_SIZE = 5;
const EPOCHS = 5;
const LOCAL_DASHBOARD_URL = 'http://localhost:5173';
const TESTNET_RPC = 'https://fullnode.testnet.sui.io:443';
const MAINNET_RPC = 'https://fullnode.mainnet.sui.io:443';
const TESTNET_SEAL_PACKAGE_ID = '0x299d7d7592c84d08a25ec26c777933d6ab72e51b31a615027186a0a377fe75cb';
const URL_REGEX = /^https?:\/\/\S+$/i;
const TAG_STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how', 'in', 'into', 'is', 'it',
  'of', 'on', 'or', 'that', 'the', 'this', 'to', 'with', 'your', 'you', 'via', 'over', 'under',
]);
const fileDir = dirname(fileURLToPath(import.meta.url));

function getPaths() {
  const walvisDir = join(homedir(), '.walvis');
  return {
    walvisDir,
    manifestPath: join(walvisDir, 'manifest.json'),
    spacesDir: join(walvisDir, 'spaces'),
    mediaDir: join(walvisDir, 'media'),
    statePath: join(walvisDir, 'fastpath-state.json'),
  };
}

function ensureDirs() {
  const { walvisDir, spacesDir, mediaDir } = getPaths();
  if (!existsSync(walvisDir)) mkdirSync(walvisDir, { recursive: true });
  if (!existsSync(spacesDir)) mkdirSync(spacesDir, { recursive: true });
  if (!existsSync(mediaDir)) mkdirSync(mediaDir, { recursive: true });
}

function readJson(path, fallback = null) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function writeJson(path, payload) {
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}

function nowIso() {
  return new Date().toISOString();
}

function trimText(text, limit) {
  const normalized = String(text ?? '').replace(/\s+/g, ' ').trim();
  if (normalized.length <= limit) return normalized;
  return `${normalized.slice(0, limit - 1).trimEnd()}…`;
}

function tokenize(input) {
  const out = [];
  const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
  let match;
  while ((match = re.exec(input ?? '')) !== null) {
    out.push(match[1] ?? match[2] ?? match[3]);
  }
  return out;
}

function createId(length = 8) {
  const alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789';
  const bytes = randomBytes(length);
  let out = '';
  for (let i = 0; i < length; i += 1) {
    out += alphabet[bytes[i] % alphabet.length];
  }
  return out;
}

function applySealDefaults(manifest) {
  if (!manifest || manifest.network !== 'testnet' || manifest.sealPackageId) return false;
  manifest.sealPackageId = TESTNET_SEAL_PACKAGE_ID;
  return true;
}

function defaultManifest() {
  const timestamp = nowIso();
  return {
    agent: 'W.A.L.V.I.S.',
    activeSpace: 'default',
    fastPathEnabled: true,
    network: 'testnet',
    sealPackageId: TESTNET_SEAL_PACKAGE_ID,
    walrusPublisher: 'https://publisher.walrus-testnet.walrus.space',
    walrusAggregator: 'https://aggregator.walrus-testnet.walrus.space',
    spaces: {
      default: {
        name: 'Default Space',
        updatedAt: timestamp,
      },
    },
    items: {},
    llmEndpoint: '',
    llmModel: '',
    suiAddress: '',
  };
}

function defaultSpace() {
  const timestamp = nowIso();
  return {
    id: 'default',
    name: 'Default Space',
    description: 'Your main collection',
    items: [],
    createdAt: timestamp,
    updatedAt: timestamp,
  };
}

function ensureInitialized() {
  ensureDirs();
  const { manifestPath } = getPaths();
  let created = false;

  if (!existsSync(manifestPath)) {
    writeJson(manifestPath, defaultManifest());
    writeJson(spacePath('default'), defaultSpace());
    created = true;
  }

  const manifest = readManifest();
  if (applySealDefaults(manifest)) {
    writeManifest(manifest);
  }
  if (!spaceExists(manifest.activeSpace)) {
    writeSpace(defaultSpace());
  }

  return { manifest, created };
}

function readManifest() {
  const { manifestPath } = getPaths();
  const manifest = readJson(manifestPath);
  if (!manifest) {
    throw new Error('WALVIS is not initialized. Run: npx walvis');
  }
  if (!manifest.spaces || typeof manifest.spaces !== 'object') manifest.spaces = {};
  if (!manifest.items || typeof manifest.items !== 'object') manifest.items = {};
  return manifest;
}

function writeManifest(manifest) {
  const { manifestPath } = getPaths();
  writeJson(manifestPath, manifest);
}

function spacePath(spaceId) {
  const { spacesDir } = getPaths();
  return join(spacesDir, `${spaceId}.json`);
}

function spaceExists(spaceId) {
  return existsSync(spacePath(spaceId));
}

function readSpace(spaceId) {
  const path = spacePath(spaceId);
  if (!existsSync(path)) throw new Error(`Space not found: ${spaceId}`);
  const space = readJson(path);
  if (!space) throw new Error(`Space is invalid: ${spaceId}`);
  if (!Array.isArray(space.items)) space.items = [];
  return space;
}

function writeSpace(space) {
  writeJson(spacePath(space.id), space);
}

function listSpaceFiles() {
  ensureDirs();
  const { spacesDir } = getPaths();
  return readdirSync(spacesDir).filter((entry) => entry.endsWith('.json'));
}

function listSpaces() {
  const { spacesDir } = getPaths();
  return listSpaceFiles().map((entry) => readJson(join(spacesDir, entry))).filter(Boolean);
}

function readState() {
  const { statePath } = getPaths();
  const state = readJson(statePath, {});
  if (!state.pending || typeof state.pending !== 'object') state.pending = {};
  if (!state.ui || typeof state.ui !== 'object') state.ui = {};
  return state;
}

function writeState(state) {
  const { statePath } = getPaths();
  writeJson(statePath, state);
}

function buildParticipantKey(ctx) {
  const channel = ctx.channelId ?? ctx.channel ?? 'unknown';
  const account = ctx.accountId ?? 'default';
  const sender = ctx.senderId ?? ctx.from ?? 'unknown';
  return `${channel}:${account}:${sender}`;
}

function setPending(ctx, payload) {
  const state = readState();
  state.pending[buildParticipantKey(ctx)] = { ...payload, updatedAt: nowIso() };
  writeState(state);
}

function getPending(ctx) {
  const state = readState();
  return state.pending[buildParticipantKey(ctx)] ?? null;
}

function clearPending(ctx) {
  const state = readState();
  delete state.pending[buildParticipantKey(ctx)];
  writeState(state);
}

function setUiState(ctx, patch) {
  const state = readState();
  const key = buildParticipantKey(ctx);
  state.ui[key] = {
    ...(state.ui[key] ?? {}),
    ...patch,
    updatedAt: nowIso(),
  };
  writeState(state);
}

function getUiState(ctx) {
  const state = readState();
  return state.ui[buildParticipantKey(ctx)] ?? {};
}

function normalizeUrl(url) {
  try {
    const parsed = new URL(url);
    parsed.hash = '';
    if (parsed.pathname.endsWith('/') && parsed.pathname !== '/') {
      parsed.pathname = parsed.pathname.slice(0, -1);
    }
    return parsed.toString();
  } catch {
    return String(url ?? '').trim();
  }
}

function formatDate(iso) {
  if (!iso) return '-';
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function getDomain(url) {
  if (!url) return '';
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

function slugifyTag(value) {
  const slug = String(value ?? '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
  if (!slug || TAG_STOPWORDS.has(slug)) return '';
  return slug;
}

function normalizeTags(values) {
  const source = Array.isArray(values) ? values : tokenize(String(values ?? '').replace(/,/g, ' '));
  const seen = new Set();
  const output = [];
  for (const raw of source) {
    const tag = slugifyTag(raw);
    if (!tag || seen.has(tag)) continue;
    seen.add(tag);
    output.push(tag);
  }
  return output;
}

function pickTags(parts, fallback = []) {
  const pool = [];
  for (const part of parts) {
    const words = String(part ?? '')
      .toLowerCase()
      .replace(/https?:\/\//g, ' ')
      .replace(/[^a-z0-9]+/g, ' ')
      .split(/\s+/)
      .filter((word) => word.length >= 3 && !TAG_STOPWORDS.has(word));
    pool.push(...words);
  }
  const tags = normalizeTags(pool);
  for (const value of fallback) {
    const tag = slugifyTag(value);
    if (tag && !tags.includes(tag)) tags.push(tag);
  }
  return tags.slice(0, 5);
}

function updateManifestSpaceEntry(manifest, space) {
  const current = manifest.spaces?.[space.id] ?? {};
  manifest.spaces[space.id] = {
    ...current,
    name: space.name,
    updatedAt: space.updatedAt,
    ...(space.walrusBlobId ? { blobId: space.walrusBlobId } : {}),
    ...(space.syncedAt ? { syncedAt: space.syncedAt } : {}),
    ...(space.seal?.encrypted ? {
      encrypted: true,
      policyObjectId: space.seal.policyObjectId,
    } : {}),
  };
}

function updateManifestItemEntry(manifest, spaceId, item) {
  manifest.items[item.id] = {
    spaceId,
    ...(item.url ? { url: item.url } : {}),
    title: item.title,
    ...(item.screenshotBlobId ? { screenshotBlobId: item.screenshotBlobId } : {}),
    ...(item.localPath ? { screenshotPath: item.localPath } : {}),
    tags: [...(item.tags ?? [])],
    updatedAt: item.updatedAt ?? item.createdAt ?? nowIso(),
  };
}

function removeManifestItemEntry(manifest, itemId) {
  if (manifest.items && manifest.items[itemId]) {
    delete manifest.items[itemId];
  }
}

function resolveSpaceId(manifest, input) {
  if (!input) return manifest.activeSpace;
  if (manifest.spaces?.[input]) return input;
  const lower = String(input).toLowerCase();
  const found = Object.entries(manifest.spaces ?? {}).find(([id, entry]) => {
    return id.toLowerCase() === lower || String(entry?.name ?? '').toLowerCase() === lower;
  });
  return found?.[0] ?? null;
}

function findItemRecord(manifest, itemId) {
  if (!itemId) return null;
  const indexed = manifest.items?.[itemId];
  if (indexed?.spaceId && spaceExists(indexed.spaceId)) {
    const space = readSpace(indexed.spaceId);
    const index = space.items.findIndex((entry) => entry.id === itemId);
    if (index >= 0) {
      return {
        spaceId: indexed.spaceId,
        space,
        item: space.items[index],
        index,
      };
    }
  }

  for (const space of listSpaces()) {
    const index = (space.items ?? []).findIndex((entry) => entry.id === itemId);
    if (index >= 0) {
      return {
        spaceId: space.id,
        space,
        item: space.items[index],
        index,
      };
    }
  }

  return null;
}

function findMostRecentItem(space) {
  const items = [...(space.items ?? [])];
  items.sort((left, right) => {
    return new Date(right.updatedAt ?? right.createdAt ?? 0).getTime() - new Date(left.updatedAt ?? left.createdAt ?? 0).getTime();
  });
  return items[0] ?? null;
}

function formatItemBlock(item, index) {
  const tags = Array.isArray(item.tags) && item.tags.length > 0 ? item.tags.slice(0, 4).map((tag) => `#${tag}`).join(' ') : '(no tags)';
  const summary = trimText(item.summary || item.content || '(no summary)', 100);
  const meta = [item.url ? getDomain(item.url) : item.type, formatDate(item.updatedAt ?? item.createdAt), `id:${item.id}`]
    .filter(Boolean)
    .join(' • ');
  return [
    `${index}. ${item.title ?? '(untitled)'}`,
    summary,
    tags,
    meta,
  ].join('\n');
}

function buildReply(text, buttons) {
  const payload = { text };
  if (buttons && buttons.length > 0) {
    payload.channelData = {
      telegram: {
        buttons,
      },
    };
  }
  return payload;
}

function buildListButtons(items, pagination = []) {
  const rows = [];
  for (const item of items) {
    rows.push([
      { text: '🏷 Tags', callback_data: `/walvis-tags ${item.id}` },
      { text: '📝 Note', callback_data: `/walvis-note ${item.id}` },
      { text: '🗑 Delete', callback_data: `/walvis-delete ${item.id}` },
    ]);
    if (item.screenshotBlobId || item.localPath) {
      rows.push([{ text: '📸 Screenshot', callback_data: `/walvis-screenshot ${item.id}` }]);
    }
  }
  if (pagination.length > 0) rows.push(pagination);
  rows.push([{ text: '🔄 Sync', callback_data: '/walvis-sync' }]);
  return rows;
}

function inferContentType(path) {
  const ext = extname(path).toLowerCase();
  if (ext === '.png') return 'image/png';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.gif') return 'image/gif';
  if (ext === '.svg') return 'image/svg+xml';
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  return 'application/octet-stream';
}

async function uploadToWalrus(data, publisher, contentType = 'application/json') {
  const response = await fetch(`${publisher}/v1/blobs?epochs=${EPOCHS}`, {
    method: 'PUT',
    headers: { 'Content-Type': contentType },
    body: data,
  });

  if (!response.ok) {
    throw new Error(`Walrus upload failed (${response.status}): ${await response.text()}`);
  }

  const json = await response.json();
  const blobId = json?.newlyCreated?.blobObject?.blobId ?? json?.alreadyCertified?.blobId;
  if (!blobId) throw new Error('Walrus response missing blobId');
  return blobId;
}

async function fetchUrlMeta(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(url, {
      headers: { 'User-Agent': 'WALVIS Fast Path/0.2.0' },
      signal: controller.signal,
    });
    const html = await response.text();
    const title = decodeEntities(
      firstMatch(html, [
        /<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i,
        /<title[^>]*>([^<]+)<\/title>/i,
      ]),
    );
    const description = decodeEntities(
      firstMatch(html, [
        /<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i,
        /<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']+)["']/i,
      ]),
    );
    const domain = getDomain(url);
    return {
      title: trimText(title || domain || url, 80),
      summary: trimText(description || `Saved from ${domain || url} without AI analysis.`, 160),
      content: trimText(description || title || url, 500),
      tags: pickTags([domain, title, description], ['bookmark', domain.split('.').at(0)]),
    };
  } catch {
    const domain = getDomain(url);
    return {
      title: trimText(domain || url, 80),
      summary: 'Content could not be fetched — visit the link directly.',
      content: url,
      tags: pickTags([domain, url], ['bookmark', 'unread']),
    };
  } finally {
    clearTimeout(timeout);
  }
}

function firstMatch(text, patterns) {
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]) return match[1];
  }
  return '';
}

function decodeEntities(text) {
  return String(text ?? '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function describeTextEntry(text) {
  const normalized = String(text ?? '').trim();
  return {
    title: trimText(normalized, 80),
    summary: trimText(normalized, 160),
    content: trimText(normalized, 500),
    tags: pickTags([normalized], ['note']),
  };
}

function formatMist(mistValue) {
  const mist = BigInt(mistValue || '0');
  const whole = mist / 1_000_000_000n;
  const fraction = (mist % 1_000_000_000n).toString().padStart(9, '0').slice(0, 4);
  return `${whole}.${fraction} SUI`;
}

function isUnsynced(space, spaceEntry) {
  if (!spaceEntry?.syncedAt) return true;
  const updatedAt = new Date(space.updatedAt ?? 0).getTime();
  const syncedAt = new Date(spaceEntry.syncedAt).getTime();
  if (Number.isNaN(updatedAt) || Number.isNaN(syncedAt)) return true;
  return updatedAt > syncedAt;
}

function resolveWalvisScript(scriptName) {
  const candidates = [
    join(fileDir, '..', '..', 'skill', 'scripts', `${scriptName}.ts`),
    join(fileDir, '..', '..', 'scripts', `${scriptName}.ts`),
    join(homedir(), '.openclaw', 'skills', 'walvis', 'scripts', `${scriptName}.ts`),
  ];
  return candidates.find((candidate) => existsSync(candidate)) ?? null;
}

function resolveWalvisProjectRoot() {
  const candidates = [
    process.env.WALVIS_PROJECT_ROOT,
    join(fileDir, '..', '..'),
    join(fileDir, '..'),
    cwd(),
  ].filter(Boolean);

  return candidates.find((candidate) => {
    return existsSync(join(candidate, 'web', 'package.json'));
  }) ?? null;
}

function runTsxScript(scriptName, args) {
  const scriptPath = resolveWalvisScript(scriptName);
  if (!scriptPath) throw new Error(`Script not found: ${scriptName}`);
  const result = spawnSync(
    'npx',
    [
      '-y',
      '-p', 'tsx',
      '-p', '@mysten/seal',
      '-p', '@mysten/sui',
      '-p', '@mysten/bcs',
      'tsx',
      scriptPath,
      ...args,
    ],
    {
      encoding: 'utf8',
      timeout: 180_000,
    },
  );
  if (result.status !== 0) {
    const errorText = `${result.stderr ?? ''}${result.stdout ?? ''}`.trim();
    throw new Error(errorText || `Failed to run ${scriptName}`);
  }
  return `${result.stdout ?? ''}`.trim();
}

async function listCommand(ctx, rawArgs, options = {}) {
  const { manifest, created } = ensureInitialized();
  if (created && !rawArgs.trim() && !options.page) {
    return buildReply('🐋 Welcome to WALVIS!\nYour knowledge vault has been initialized.\nSend /walvis <url-or-text> to save your first bookmark.');
  }

  const tokens = tokenize(rawArgs);
  let page = options.page ?? 1;
  let requestedSpace = options.spaceId ?? null;

  if (!requestedSpace) {
    if (tokens[0] && /^\d+$/.test(tokens[0])) {
      page = Math.max(1, parseInt(tokens[0], 10));
      requestedSpace = tokens[1] ?? null;
    } else if (tokens[0]) {
      requestedSpace = tokens[0];
      if (tokens[1] && /^\d+$/.test(tokens[1])) {
        page = Math.max(1, parseInt(tokens[1], 10));
      }
    }
  }

  const spaceId = resolveSpaceId(manifest, requestedSpace) ?? manifest.activeSpace;
  const space = readSpace(spaceId);
  const items = [...(space.items ?? [])].sort((left, right) => {
    return new Date(right.updatedAt ?? right.createdAt ?? 0).getTime() - new Date(left.updatedAt ?? left.createdAt ?? 0).getTime();
  });

  setUiState(ctx, { list: { spaceId } });

  if (items.length === 0) {
    return buildReply(`WALVIS List — ${space.name}\n\nNo items yet. Send /walvis <url-or-text> to save one.`);
  }

  const totalPages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * PAGE_SIZE;
  const pageItems = items.slice(start, start + PAGE_SIZE);
  const text = [
    `WALVIS List — ${space.name}`,
    `Page ${safePage}/${totalPages} • ${items.length} item(s)`,
    '',
    ...pageItems.flatMap((item, index) => [formatItemBlock(item, start + index + 1), '']),
  ].join('\n').trim();

  const buttons = buildListButtons(
    pageItems.map((item, index) => ({
      id: item.id,
      shortLabel: String(start + index + 1),
      screenshotBlobId: item.screenshotBlobId,
      localPath: item.localPath,
    })),
    [
      ...(safePage > 1 ? [{ text: '⬅️ Prev', callback_data: `/walvis-list-page ${safePage - 1}` }] : []),
      ...(safePage < totalPages ? [{ text: '➡️ Next', callback_data: `/walvis-list-page ${safePage + 1}` }] : []),
    ],
  );

  return buildReply(text, buttons);
}

async function listPageCommand(ctx, rawArgs) {
  const page = Math.max(1, parseInt(tokenize(rawArgs)[0] ?? '1', 10) || 1);
  const ui = getUiState(ctx);
  return listCommand(ctx, '', { page, spaceId: ui.list?.spaceId ?? null });
}

async function searchCommand(ctx, rawArgs, options = {}) {
  const { manifest } = ensureInitialized();
  const tokens = tokenize(rawArgs);
  let page = options.page ?? 1;
  let query = options.query ?? '';

  if (!query) {
    if (tokens.length > 1 && /^\d+$/.test(tokens[tokens.length - 1])) {
      page = Math.max(1, parseInt(tokens.pop(), 10));
    }
    query = tokens.join(' ').trim();
  }

  if (!query) {
    return buildReply('Usage: /walvis search <query> [page]');
  }

  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  const allItems = [];
  for (const space of listSpaces()) {
    for (const item of space.items ?? []) {
      allItems.push({ item, spaceId: space.id });
    }
  }

  const results = allItems.filter(({ item }) => {
    const haystack = [item.title, item.summary, item.content, ...(item.tags ?? []), item.notes]
      .join(' ')
      .toLowerCase();
    return terms.every((term) => haystack.includes(term));
  }).sort((left, right) => {
    return new Date(right.item.updatedAt ?? right.item.createdAt ?? 0).getTime() - new Date(left.item.updatedAt ?? left.item.createdAt ?? 0).getTime();
  });

  setUiState(ctx, { search: { query } });

  if (results.length === 0) {
    return buildReply(`No results for "${query}".`);
  }

  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * PAGE_SIZE;
  const pageItems = results.slice(start, start + PAGE_SIZE);
  const text = [
    `WALVIS Search — "${query}"`,
    `Page ${safePage}/${totalPages} • ${results.length} match(es)`,
    '',
    ...pageItems.flatMap(({ item }, index) => [formatItemBlock(item, start + index + 1), '']),
  ].join('\n').trim();

  const buttons = buildListButtons(
    pageItems.map(({ item }, index) => ({
      id: item.id,
      shortLabel: String(start + index + 1),
      screenshotBlobId: item.screenshotBlobId,
      localPath: item.localPath,
    })),
    [
      ...(safePage > 1 ? [{ text: '⬅️ Prev', callback_data: `/walvis-search-page ${safePage - 1}` }] : []),
      ...(safePage < totalPages ? [{ text: '➡️ Next', callback_data: `/walvis-search-page ${safePage + 1}` }] : []),
    ],
  );

  return buildReply(text, buttons);
}

async function searchPageCommand(ctx, rawArgs) {
  const page = Math.max(1, parseInt(tokenize(rawArgs)[0] ?? '1', 10) || 1);
  const ui = getUiState(ctx);
  return searchCommand(ctx, '', { page, query: ui.search?.query ?? '' });
}

async function spacesCommand(ctx) {
  const { manifest } = ensureInitialized();
  const spaces = listSpaces().sort((left, right) => String(left.name).localeCompare(String(right.name)));
  if (spaces.length === 0) return buildReply('No spaces found.');
  const text = ['WALVIS Spaces', '', ...spaces.map((space) => {
    const active = space.id === manifest.activeSpace ? ' (active)' : '';
    return `- ${space.name} • ${(space.items ?? []).length} item(s)${active}`;
  })].join('\n');
  const buttons = spaces.map((space) => [{
    text: `${space.id === manifest.activeSpace ? '✅' : '📂'} ${trimText(space.name, 20)}`,
    callback_data: `/walvis-use ${space.id}`,
  }]);
  return buildReply(text, buttons);
}

async function newSpaceCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const name = String(rawArgs ?? '').trim();
  if (!name) return buildReply('Usage: /walvis new <name>');

  const exists = Object.entries(manifest.spaces ?? {}).find(([spaceId, entry]) => {
    return spaceId.toLowerCase() === name.toLowerCase() || String(entry?.name ?? '').toLowerCase() === name.toLowerCase();
  });
  if (exists) return buildReply(`Space "${name}" already exists.`);

  let id = createId();
  while (spaceExists(id)) id = createId();
  const timestamp = nowIso();
  const space = {
    id,
    name,
    description: '',
    items: [],
    createdAt: timestamp,
    updatedAt: timestamp,
  };
  writeSpace(space);
  manifest.activeSpace = id;
  updateManifestSpaceEntry(manifest, space);
  writeManifest(manifest);
  return buildReply(`Created space "${name}" and set it as active.`);
}

async function useSpaceCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const input = String(rawArgs ?? '').trim();
  if (!input) return buildReply('Usage: /walvis use <name>');
  const spaceId = resolveSpaceId(manifest, input);
  if (!spaceId) return buildReply(`Space "${input}" not found.`);
  manifest.activeSpace = spaceId;
  writeManifest(manifest);
  return buildReply(`Active space switched to "${manifest.spaces[spaceId]?.name ?? spaceId}".`);
}

async function fastPathControlCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const action = tokenize(rawArgs)[0]?.toLowerCase() ?? 'status';
  const onValues = new Set(['on', 'enable', 'enabled', '1', 'true']);
  const offValues = new Set(['off', 'disable', 'disabled', '0', 'false']);

  if (onValues.has(action)) {
    manifest.fastPathEnabled = true;
    writeManifest(manifest);
    return buildReply([
      'Fast path is ON.',
      'Deterministic commands now bypass the LLM for list/tag/note/sync/status/spaces/use/new/search/web/run/balance.',
      'Seal commands also route through fast path when their runtime dependencies are available.',
    ].join('\n'));
  }

  if (offValues.has(action)) {
    manifest.fastPathEnabled = false;
    writeManifest(manifest);
    return buildReply('Fast path is OFF. /walvis commands now use normal AI routing.');
  }

  return buildReply([
    `Fast path status: ${manifest.fastPathEnabled ? 'ON' : 'OFF'}`,
    'Covered commands: bare /walvis, list, search, spaces, new, use, tags, note, delete, screenshot, sync, status, balance, web, run.',
    'Seal commands: encrypt/share/unshare/seal-status (runtime-assisted).',
    'Usage: /walvis fastpath on|off|status',
  ].join('\n'));
}

async function statusCommand() {
  const { manifest } = ensureInitialized();
  const spaces = listSpaces();
  const unsynced = spaces.filter((space) => isUnsynced(space, manifest.spaces?.[space.id]));
  const lines = [
    'WALVIS Status',
    `Agent: ${manifest.agent ?? 'W.A.L.V.I.S.'}`,
    `Network: ${manifest.network ?? 'testnet'}`,
    `Active space: ${manifest.spaces?.[manifest.activeSpace]?.name ?? manifest.activeSpace ?? '-'}`,
    `Spaces: ${spaces.length}`,
    `Unsynced spaces: ${unsynced.length}`,
  ];
  if (manifest.suiAddress) lines.push(`Wallet: ${manifest.suiAddress}`);
  if (manifest.manifestBlobId) lines.push(`Manifest blob: ${manifest.manifestBlobId}`);
  return buildReply(lines.join('\n'));
}

async function balanceCommand() {
  const { manifest } = ensureInitialized();
  if (!manifest.suiAddress) return buildReply('No wallet configured in ~/.walvis/manifest.json.');
  const rpc = manifest.network === 'mainnet' ? MAINNET_RPC : TESTNET_RPC;
  const response = await fetch(rpc, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'suix_getBalance',
      params: [manifest.suiAddress, '0x2::sui::SUI'],
    }),
  });
  const json = await response.json();
  if (json.error) return buildReply(`Balance query failed: ${json.error.message}`);
  return buildReply(`Balance: ${formatMist(json?.result?.totalBalance ?? '0')}`);
}

async function webCommand() {
  const { manifest } = ensureInitialized();
  const active = manifest.spaces?.[manifest.activeSpace];
  if (!manifest.manifestBlobId && !active?.blobId) {
    return buildReply('No synced blob found yet. Run /walvis sync first.');
  }
  const lines = ['WALVIS Web'];
  if (manifest.manifestBlobId) lines.push(`Manifest blob: ${manifest.manifestBlobId}`);
  if (active?.blobId) lines.push(`Active space blob: ${active.blobId}`);
  lines.push('Open https://walvis.vercel.app and paste the manifest blob ID.');
  return buildReply(lines.join('\n'));
}

async function runCommand() {
  const projectRoot = resolveWalvisProjectRoot();
  const lines = [
    'WALVIS Local Preview',
    `Open ${LOCAL_DASHBOARD_URL} after starting the local dashboard.`,
    'The app loads ~/.walvis local files automatically.',
  ];

  if (projectRoot) {
    lines.push('', 'Run this on your computer:', `cd ${projectRoot}`, 'npm run dev:web');
  } else {
    lines.push('', 'Run this in your WALVIS repo:', 'npm run dev:web');
  }

  return buildReply(lines.join('\n'));
}

async function saveCommand(_ctx, rawArgs) {
  const input = String(rawArgs ?? '').trim();
  if (!input) return buildReply('Usage: /walvis <url-or-text>');

  const { manifest } = ensureInitialized();
  const space = readSpace(manifest.activeSpace);
  const timestamp = nowIso();
  const isUrl = URL_REGEX.test(input);
  const normalizedInputUrl = isUrl ? normalizeUrl(input) : null;
  const description = isUrl ? await fetchUrlMeta(input) : describeTextEntry(input);
  const existingIndex = isUrl
    ? space.items.findIndex((entry) => normalizeUrl(entry.url) === normalizedInputUrl)
    : -1;

  let item;
  let mode;
  if (existingIndex >= 0) {
    item = space.items[existingIndex];
    item.type = 'link';
    item.url = input;
    item.title = description.title;
    item.summary = description.summary;
    item.content = description.content;
    item.tags = normalizeTags([...(item.tags ?? []), ...(description.tags ?? [])]);
    item.updatedAt = timestamp;
    item.analyzedBy = 'walvis-fastpath';
    mode = 'updated';
  } else {
    item = {
      id: createId(),
      type: isUrl ? 'link' : 'text',
      ...(isUrl ? { url: input } : {}),
      title: description.title,
      summary: description.summary,
      tags: normalizeTags(description.tags),
      content: description.content,
      notes: '',
      createdAt: timestamp,
      updatedAt: timestamp,
      source: 'telegram',
      analyzedBy: 'walvis-fastpath',
    };
    space.items.push(item);
    mode = 'created';
  }

  space.updatedAt = timestamp;
  updateManifestSpaceEntry(manifest, space);
  updateManifestItemEntry(manifest, space.id, item);
  writeSpace(space);
  writeManifest(manifest);

  return buildReply([
    mode === 'updated' ? `🐋 Updated in ${space.name}` : `🐋 Saved to ${space.name}`,
    `📌 ${item.title}`,
    item.summary,
    item.tags.length > 0 ? `🏷 ${item.tags.map((tag) => `#${tag}`).join(' ')}` : '',
    isUrl ? '🔗 Link saved.' : '📝 Saved as text.',
  ].filter(Boolean).join('\n'));
}

function applyTagsToRecord(record, nextTags, mode = 'replace') {
  const tags = mode === 'append'
    ? normalizeTags([...(record.item.tags ?? []), ...nextTags])
    : normalizeTags(nextTags);
  record.item.tags = tags;
  record.item.updatedAt = nowIso();
  record.space.updatedAt = record.item.updatedAt;
}

function applyNoteToRecord(record, noteText, mode = 'replace') {
  const next = String(noteText ?? '').trim();
  const existing = String(record.item.notes ?? '').trim();
  record.item.notes = mode === 'append' && existing ? `${existing}\n${next}` : next;
  record.item.updatedAt = nowIso();
  record.space.updatedAt = record.item.updatedAt;
}

function persistRecord(manifest, record) {
  writeSpace(record.space);
  updateManifestSpaceEntry(manifest, record.space);
  updateManifestItemEntry(manifest, record.spaceId, record.item);
  writeManifest(manifest);
}

async function tagsCommand(ctx, rawArgs, mode = 'replace') {
  const { manifest } = ensureInitialized();
  const tokens = tokenize(rawArgs);
  if (tokens.length === 0) {
    return buildReply(mode === 'append' ? 'Usage: /walvis +tag [itemId] <tag1> <tag2>' : 'Usage: /walvis-tags <itemId> [tag1 tag2 ...]');
  }

  const maybeRecord = findItemRecord(manifest, tokens[0]);
  if (maybeRecord) {
    if (tokens.length === 1) {
      setPending(ctx, { type: 'tags', itemId: maybeRecord.item.id });
      return buildReply(`🏷 Current tags: ${(maybeRecord.item.tags ?? []).map((tag) => `#${tag}`).join(' ') || '(none)'}\nSend the new tags as your next message.`);
    }
    applyTagsToRecord(maybeRecord, tokens.slice(1), mode);
    persistRecord(manifest, maybeRecord);
    return buildReply(`🏷 Updated tags for ${maybeRecord.item.title}\n${maybeRecord.item.tags.map((tag) => `#${tag}`).join(' ')}`);
  }

  const space = readSpace(manifest.activeSpace);
  const item = findMostRecentItem(space);
  if (!item) return buildReply('No items available to tag.');
  const record = findItemRecord(manifest, item.id);
  applyTagsToRecord(record, tokens, 'append');
  persistRecord(manifest, record);
  return buildReply(`🏷 Added tags to ${record.item.title}\n${record.item.tags.map((tag) => `#${tag}`).join(' ')}`);
}

async function noteCommand(ctx, rawArgs, mode = 'replace') {
  const { manifest } = ensureInitialized();
  const tokens = tokenize(rawArgs);
  const input = String(rawArgs ?? '').trim();
  if (!input) {
    return buildReply(mode === 'append' ? 'Usage: /walvis +note [itemId] <text>' : 'Usage: /walvis-note <itemId> [text]');
  }

  const maybeRecord = tokens[0] ? findItemRecord(manifest, tokens[0]) : null;
  if (maybeRecord) {
    const noteText = input.slice(tokens[0].length).trim();
    if (!noteText) {
      setPending(ctx, { type: 'note', itemId: maybeRecord.item.id });
      return buildReply(`📝 Current note: ${maybeRecord.item.notes?.trim() || '(none)'}\nSend the new note as your next message.`);
    }
    applyNoteToRecord(maybeRecord, noteText, mode);
    persistRecord(manifest, maybeRecord);
    return buildReply(`📝 Updated note for ${maybeRecord.item.title}`);
  }

  const space = readSpace(manifest.activeSpace);
  const item = findMostRecentItem(space);
  if (!item) return buildReply('No items available to annotate.');
  const record = findItemRecord(manifest, item.id);
  applyNoteToRecord(record, input, 'append');
  persistRecord(manifest, record);
  return buildReply(`📝 Note added to ${record.item.title}`);
}

async function pendingCommand(ctx, rawArgs) {
  const pending = getPending(ctx);
  if (!pending) return buildReply('No pending WALVIS action.');
  const { manifest } = ensureInitialized();
  const record = findItemRecord(manifest, pending.itemId);
  if (!record) {
    clearPending(ctx);
    return buildReply('That item no longer exists.');
  }
  const input = String(rawArgs ?? '').trim();
  if (!input) return buildReply('Please send some text to finish the pending action.');

  if (pending.type === 'tags') {
    applyTagsToRecord(record, tokenize(input), 'replace');
    persistRecord(manifest, record);
    clearPending(ctx);
    return buildReply(`🏷 Updated tags for ${record.item.title}\n${record.item.tags.map((tag) => `#${tag}`).join(' ')}`);
  }

  if (pending.type === 'note') {
    applyNoteToRecord(record, input, 'replace');
    persistRecord(manifest, record);
    clearPending(ctx);
    return buildReply(`📝 Updated note for ${record.item.title}`);
  }

  clearPending(ctx);
  return buildReply('Unknown pending WALVIS action cleared.');
}

async function cancelPendingCommand(ctx) {
  if (!getPending(ctx)) return buildReply('No pending WALVIS action.');
  clearPending(ctx);
  return buildReply('Cancelled the pending WALVIS edit.');
}

async function deleteCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const itemId = tokenize(rawArgs)[0] ?? '';
  const record = findItemRecord(manifest, itemId);
  if (!record) return buildReply(`Item not found: ${itemId}`);
  const [removed] = record.space.items.splice(record.index, 1);
  record.space.updatedAt = nowIso();
  writeSpace(record.space);
  updateManifestSpaceEntry(manifest, record.space);
  removeManifestItemEntry(manifest, removed.id);
  writeManifest(manifest);
  return buildReply(`🗑 Deleted ${removed.title}`);
}

async function screenshotCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const itemId = tokenize(rawArgs)[0] ?? '';
  const record = findItemRecord(manifest, itemId);
  if (!record) return buildReply(`Item not found: ${itemId}`);
  if (record.item.screenshotBlobId) {
    return buildReply(`📸 Screenshot: ${manifest.walrusAggregator}/v1/blobs/${record.item.screenshotBlobId}`);
  }
  if (record.item.localPath) {
    return buildReply(`📸 Local screenshot path: ${record.item.localPath}`);
  }
  return buildReply(`📸 No screenshot available for ${record.item.title}.`);
}

async function syncCommand() {
  const { manifest } = ensureInitialized();
  if (!manifest.walrusPublisher || !manifest.walrusAggregator) {
    return buildReply('Walrus endpoints are missing in ~/.walvis/manifest.json.');
  }

  const spaces = listSpaces();
  if (spaces.length === 0) return buildReply('No spaces to sync.');

  let uploadedImages = 0;
  for (const space of spaces) {
    let changed = false;
    for (const item of space.items ?? []) {
      if (item.type !== 'image') continue;
      if (!item.localPath || item.screenshotBlobId) continue;
      if (!existsSync(item.localPath)) continue;
      const bytes = readFileSync(item.localPath);
      const blobId = await uploadToWalrus(bytes, manifest.walrusPublisher, inferContentType(item.localPath));
      item.screenshotBlobId = blobId;
      item.url = `${manifest.walrusAggregator}/v1/blobs/${blobId}`;
      item.updatedAt = nowIso();
      uploadedImages += 1;
      changed = true;
    }
    if (changed) {
      space.updatedAt = nowIso();
      writeSpace(space);
    }
  }

  const timestamp = nowIso();
  const spaceResults = [];
  for (const space of spaces) {
    const blobId = await uploadToWalrus(JSON.stringify(space), manifest.walrusPublisher, 'application/json');
    space.walrusBlobId = blobId;
    space.syncedAt = timestamp;
    writeSpace(space);

    updateManifestSpaceEntry(manifest, space);
    manifest.spaces[space.id].blobId = blobId;
    manifest.spaces[space.id].syncedAt = timestamp;

    for (const item of space.items ?? []) {
      updateManifestItemEntry(manifest, space.id, item);
    }

    spaceResults.push({ name: space.name, blobId });
  }

  const manifestBlobId = await uploadToWalrus(JSON.stringify(manifest), manifest.walrusPublisher, 'application/json');
  manifest.manifestBlobId = manifestBlobId;
  manifest.lastSyncAt = timestamp;
  writeManifest(manifest);

  return buildReply([
    'Synced to Walrus',
    ...spaceResults.map((entry) => `- ${entry.name}: ${entry.blobId}`),
    `- uploaded images: ${uploadedImages}`,
    `- manifest: ${manifestBlobId}`,
  ].join('\n'));
}

function activeSpace(manifest) {
  return readSpace(manifest.activeSpace);
}

async function encryptCommand() {
  const { manifest } = ensureInitialized();
  const space = activeSpace(manifest);
  if (space.seal?.encrypted) {
    return buildReply(`🔒 Space "${space.name}" is already encrypted.`);
  }
  if (applySealDefaults(manifest)) {
    writeManifest(manifest);
  }
  if (!manifest.sealPackageId) {
    return buildReply('⚠ Seal is not configured for this network yet.');
  }
  const output = runTsxScript('seal-crypto', ['enable', space.id]);
  const updated = readSpace(space.id);
  return buildReply([
    `🔒 Space "${updated.name}" is now Seal-encrypted!`,
    updated.seal?.policyObjectId ? `Policy Object: ${updated.seal.policyObjectId}` : output,
    'Only your wallet can decrypt this data.',
    'Use /walvis share <address> to grant access to others.',
    'Run /walvis sync to upload the encrypted version.',
  ].join('\n'));
}

function validSuiAddress(value) {
  return /^0x[a-f0-9]{64}$/i.test(String(value ?? '').trim());
}

async function shareCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const space = activeSpace(manifest);
  const address = tokenize(rawArgs)[0] ?? '';
  if (!space.seal?.encrypted) {
    return buildReply(`⚠ Space "${space.name}" is not encrypted. Use /walvis encrypt first.`);
  }
  if (!validSuiAddress(address)) {
    return buildReply('Usage: /walvis share <0x...64-hex-address>');
  }
  runTsxScript('seal-crypto', ['share', space.id, address]);
  const updated = readSpace(space.id);
  return buildReply([
    `🔓 Shared "${updated.name}" with ${address}`,
    'They can now decrypt this space in the web UI.',
    `Allowlist: ${updated.seal?.allowlist?.length ?? 0} address(es)`,
  ].join('\n'));
}

async function unshareCommand(_ctx, rawArgs) {
  const { manifest } = ensureInitialized();
  const space = activeSpace(manifest);
  const address = tokenize(rawArgs)[0] ?? '';
  if (!space.seal?.encrypted) {
    return buildReply(`⚠ Space "${space.name}" is not encrypted.`);
  }
  if (!validSuiAddress(address)) {
    return buildReply('Usage: /walvis unshare <0x...64-hex-address>');
  }
  runTsxScript('seal-crypto', ['unshare', space.id, address]);
  const updated = readSpace(space.id);
  return buildReply([
    `🔒 Revoked access for ${address} on "${updated.name}"`,
    `Allowlist: ${updated.seal?.allowlist?.length ?? 0} address(es)`,
  ].join('\n'));
}

async function sealStatusCommand() {
  const { manifest } = ensureInitialized();
  const space = activeSpace(manifest);
  if (!space.seal?.encrypted) {
    return buildReply(`🔓 Space "${space.name}" is NOT encrypted.\nUse /walvis encrypt to enable Seal encryption.`);
  }
  const allowlist = space.seal.allowlist?.length ? space.seal.allowlist.join('\n') : '(owner only)';
  return buildReply([
    `🔒 Space "${space.name}" — Seal Encrypted`,
    `Policy Object: ${space.seal.policyObjectId}`,
    `Allowlist: ${space.seal.allowlist?.length ?? 0} address(es)`,
    allowlist,
  ].join('\n'));
}

async function legacyCallbackCommand(ctx, rawArgs) {
  const value = String(rawArgs ?? '').trim();
  if (!value) return buildReply('Empty callback.');
  if (value.startsWith('w:page:')) {
    const pageIndex = parseInt(value.split(':')[2] ?? '0', 10) || 0;
    return listPageCommand(ctx, String(pageIndex + 1));
  }
  if (value.startsWith('w:sp:')) {
    const [, , pageIndexRaw, ...rest] = value.split(':');
    const pageIndex = parseInt(pageIndexRaw ?? '0', 10) || 0;
    const query = rest.join(':');
    return searchCommand(ctx, '', { page: pageIndex + 1, query });
  }
  if (value.startsWith('w:tags:')) return tagsCommand(ctx, value.split(':').slice(2).join(' '));
  if (value.startsWith('w:note:')) return noteCommand(ctx, value.split(':').slice(2).join(' '));
  if (value.startsWith('w:del:')) return deleteCommand(ctx, value.split(':').slice(2).join(' '));
  if (value.startsWith('w:ss:')) return screenshotCommand(ctx, value.split(':').slice(2).join(' '));
  if (value === 'w:cron:sync') return syncCommand(ctx, '');
  return buildReply(`Unsupported callback: ${value}`);
}

function wrap(handler) {
  return async (ctx) => {
    try {
      return await handler(ctx, ctx.args ?? '');
    } catch (error) {
      return buildReply(`walvis-fastpath error: ${(error && error.message) || String(error)}`);
    }
  };
}

function helpText() {
  return [
    'WALVIS commands',
    '- bare /walvis',
    '- /walvis list [page] [space]',
    '- /walvis search <query> [page]',
    '- /walvis +tag [itemId] <tags...>',
    '- /walvis +note [itemId] <text>',
    '- /walvis sync',
    '- /walvis encrypt | share | unshare | seal-status',
    '- /walvis spaces | new | use | status | balance | web | run',
    '- /walvis fastpath on|off|status',
  ].join('\n');
}

export default function register(api) {
  api.registerCommand({
    name: 'walvis-help',
    description: 'Show WALVIS command help.',
    handler: async () => buildReply(helpText()),
  });

  api.registerCommand({
    name: 'walvis-fastpath',
    description: 'Toggle WALVIS direct routing on/off without editing files.',
    acceptsArgs: true,
    handler: wrap(fastPathControlCommand),
  });

  api.registerCommand({
    name: 'walvis-list',
    description: 'List WALVIS items quickly (no model).',
    acceptsArgs: true,
    handler: wrap(listCommand),
  });

  api.registerCommand({
    name: 'walvis-list-page',
    description: 'Go to another WALVIS list page.',
    acceptsArgs: true,
    handler: wrap(listPageCommand),
  });

  api.registerCommand({
    name: 'walvis-search',
    description: 'Search WALVIS items quickly (no model).',
    acceptsArgs: true,
    handler: wrap(searchCommand),
  });

  api.registerCommand({
    name: 'walvis-search-page',
    description: 'Go to another WALVIS search page.',
    acceptsArgs: true,
    handler: wrap(searchPageCommand),
  });

  api.registerCommand({
    name: 'walvis-new',
    description: 'Create a WALVIS space quickly (no model).',
    acceptsArgs: true,
    handler: wrap(newSpaceCommand),
  });

  api.registerCommand({
    name: 'walvis-use',
    description: 'Switch active WALVIS space quickly (no model).',
    acceptsArgs: true,
    handler: wrap(useSpaceCommand),
  });

  api.registerCommand({
    name: 'walvis-spaces',
    description: 'List WALVIS spaces quickly (no model).',
    handler: wrap(spacesCommand),
  });

  api.registerCommand({
    name: 'walvis-status',
    description: 'Show WALVIS status quickly (no model).',
    handler: wrap(statusCommand),
  });

  api.registerCommand({
    name: 'walvis-balance',
    description: 'Check SUI balance quickly (no model).',
    handler: wrap(balanceCommand),
  });

  api.registerCommand({
    name: 'walvis-web',
    description: 'Show WALVIS web blob IDs quickly (no model).',
    handler: wrap(webCommand),
  });

  api.registerCommand({
    name: 'walvis-run',
    description: 'Show how to start the local WALVIS preview dashboard.',
    handler: wrap(runCommand),
  });

  api.registerCommand({
    name: 'walvis-sync',
    description: 'Sync WALVIS data to Walrus quickly (no model).',
    handler: wrap(syncCommand),
  });

  api.registerCommand({
    name: 'walvis-tags',
    description: 'Replace WALVIS item tags or open the tag editor.',
    acceptsArgs: true,
    handler: wrap((ctx, args) => tagsCommand(ctx, args, 'replace')),
  });

  api.registerCommand({
    name: 'walvis-tags-add',
    description: 'Append tags to a WALVIS item.',
    acceptsArgs: true,
    handler: wrap((ctx, args) => tagsCommand(ctx, args, 'append')),
  });

  api.registerCommand({
    name: 'walvis-note',
    description: 'Replace a WALVIS note or open the note editor.',
    acceptsArgs: true,
    handler: wrap((ctx, args) => noteCommand(ctx, args, 'replace')),
  });

  api.registerCommand({
    name: 'walvis-note-add',
    description: 'Append a note to a WALVIS item.',
    acceptsArgs: true,
    handler: wrap((ctx, args) => noteCommand(ctx, args, 'append')),
  });

  api.registerCommand({
    name: 'walvis-pending',
    description: 'Complete a pending WALVIS edit.',
    acceptsArgs: true,
    handler: wrap(pendingCommand),
  });

  api.registerCommand({
    name: 'walvis-cancel',
    description: 'Cancel a pending WALVIS edit.',
    handler: wrap(cancelPendingCommand),
  });

  api.registerCommand({
    name: 'walvis-delete',
    description: 'Delete a WALVIS item quickly.',
    acceptsArgs: true,
    handler: wrap(deleteCommand),
  });

  api.registerCommand({
    name: 'walvis-screenshot',
    description: 'Show a WALVIS screenshot quickly.',
    acceptsArgs: true,
    handler: wrap(screenshotCommand),
  });

  api.registerCommand({
    name: 'walvis-encrypt',
    description: 'Seal-encrypt the active WALVIS space.',
    handler: wrap(encryptCommand),
  });

  api.registerCommand({
    name: 'walvis-share',
    description: 'Share the active encrypted WALVIS space.',
    acceptsArgs: true,
    handler: wrap(shareCommand),
  });

  api.registerCommand({
    name: 'walvis-unshare',
    description: 'Revoke access to the active encrypted WALVIS space.',
    acceptsArgs: true,
    handler: wrap(unshareCommand),
  });

  api.registerCommand({
    name: 'walvis-seal-status',
    description: 'Show Seal status for the active WALVIS space.',
    handler: wrap(sealStatusCommand),
  });

  api.registerCommand({
    name: 'walvis-callback',
    description: 'Handle legacy WALVIS callback payloads.',
    acceptsArgs: true,
    handler: wrap(legacyCallbackCommand),
  });
}
