/**
 * WALVIS list command — outputs a single message tool payload as JSON
 * Usage: node list.mjs [page] [spaceName]
 */

import { existsSync, readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const WALVIS_DIR = join(homedir(), '.walvis');
const PAGE_SIZE = 5;
const MANIFEST_PATH = join(WALVIS_DIR, 'manifest.json');

function printJson(payload) {
  console.log(JSON.stringify(payload));
}

function printError(message) {
  printJson({ error: message });
  process.exit(0);
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

function trimText(text, limit) {
  const normalized = String(text ?? '').replace(/\s+/g, ' ').trim();
  if (normalized.length <= limit) return normalized;
  return `${normalized.slice(0, limit - 1).trimEnd()}…`;
}

function sortItems(items) {
  return [...items].sort((left, right) => {
    const leftTime = new Date(left.updatedAt ?? left.createdAt).getTime();
    const rightTime = new Date(right.updatedAt ?? right.createdAt).getTime();
    return rightTime - leftTime;
  });
}

function formatItemBlock(item, index) {
  const tags = item.tags.length > 0
    ? item.tags.slice(0, 4).map((tag) => `#${tag}`).join(' ')
    : '(no tags)';
  const summary = trimText(item.summary || item.content || '(no summary)', 100);
  const meta = [
    item.url ? getDomain(item.url) : item.type,
    formatDate(item.updatedAt ?? item.createdAt),
    `id:${item.id}`,
  ].filter(Boolean).join(' • ');

  return [
    `${index}. ${item.title || '(untitled)'}`,
    summary,
    tags,
    meta,
  ].join('\n');
}

function buildButtons(items, start, pagination = []) {
  const rows = [];

  items.forEach((item, offset) => {
    const label = String(start + offset + 1);
    rows.push([
      { text: `🏷 ${label}`, callback_data: `w:tags:${item.id}` },
      { text: `📝 ${label}`, callback_data: `w:note:${item.id}` },
      { text: `🗑 ${label}`, callback_data: `w:del:${item.id}` },
    ]);

    if (item.screenshotBlobId || item.screenshotPath) {
      rows.push([{ text: `📸 ${label}`, callback_data: `w:ss:${item.id}` }]);
    }
  });

  if (pagination.length > 0) rows.push(pagination);
  rows.push([{ text: '🔄 Sync', callback_data: 'w:cron:sync' }]);
  return rows;
}

function buildPayload(space, items, page, totalPages) {
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * PAGE_SIZE;
  const pageItems = items.slice(start, start + PAGE_SIZE);
  const message = [
    `WALVIS List — ${space.name}`,
    `Page ${safePage}/${totalPages} • ${items.length} item(s)`,
    '',
    ...pageItems.flatMap((item, index) => [formatItemBlock(item, start + index + 1), '']),
  ].join('\n').trim();

  const pagination = [];
  if (safePage > 1) pagination.push({ text: '⬅️ Prev', callback_data: `w:page:${safePage - 2}` });
  if (safePage < totalPages) pagination.push({ text: '➡️ Next', callback_data: `w:page:${safePage}` });

  return {
    action: 'send',
    channel: 'telegram',
    message,
    buttons: buildButtons(pageItems, start, pagination),
  };
}

const args = process.argv.slice(2);
const requestedPage = parseInt(args[0] ?? '1', 10) || 1;
const spaceName = args[1] ?? null;

if (!existsSync(MANIFEST_PATH)) {
  printError('WALVIS not initialized. Run: npx walvis');
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST_PATH, 'utf8'));
} catch {
  printError('Failed to read ~/.walvis/manifest.json');
}

let spaceId = manifest.activeSpace;
if (spaceName) {
  const entry = Object.entries(manifest.spaces).find(([, value]) => value.name === spaceName);
  if (!entry) {
    printError(`Space "${spaceName}" not found.`);
  }
  spaceId = entry[0];
}

const spacePath = join(WALVIS_DIR, 'spaces', `${spaceId}.json`);
if (!existsSync(spacePath)) {
  printError(`Space "${spaceId}" not found.`);
}

let space;
try {
  space = JSON.parse(readFileSync(spacePath, 'utf8'));
} catch {
  printError(`Failed to read space file for "${spaceId}".`);
}

const items = sortItems(space.items ?? []);
if (items.length === 0) {
  printJson({ empty: true });
} else {
  const totalPages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(1, requestedPage), totalPages);
  printJson(buildPayload(space, items, safePage, totalPages));
}
