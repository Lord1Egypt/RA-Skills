/**
 * WALVIS search command — outputs a single message tool payload as JSON
 *
 * Usage:
 *   node --import tsx/esm search.ts <query> [page]
 *
 * Output: JSON object for one `message` tool call.
 */

import { existsSync, readFileSync, readdirSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';
import type { Space, BookmarkItem } from './types.js';

const WALVIS_DIR = join(homedir(), '.walvis');
const SPACES_DIR = join(WALVIS_DIR, 'spaces');
const PAGE_SIZE = 5;

type Button = {
  text: string;
  callback_data: string;
};

type SearchEntry = {
  item: BookmarkItem;
  spaceName: string;
};

type MessagePayload = {
  action: 'send';
  channel: 'telegram';
  message: string;
  buttons: Button[][];
};

function formatDate(iso?: string): string {
  if (!iso) return '-';
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function getDomain(url?: string): string {
  if (!url) return '';
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

function trimText(text: string | undefined, limit: number): string {
  const normalized = String(text ?? '').replace(/\s+/g, ' ').trim();
  if (normalized.length <= limit) return normalized;
  return `${normalized.slice(0, limit - 1).trimEnd()}…`;
}

function loadAllEntries(): SearchEntry[] {
  const files = readdirSync(SPACES_DIR).filter((file) => file.endsWith('.json'));
  const entries: SearchEntry[] = [];

  files.forEach((file) => {
    const space: Space = JSON.parse(readFileSync(join(SPACES_DIR, file), 'utf8'));
    (space.items ?? []).forEach((item) => {
      entries.push({ item, spaceName: space.name });
    });
  });

  return entries;
}

function matchesQuery(item: BookmarkItem, terms: string[]): boolean {
  const haystack = [item.title, item.summary, item.content, ...item.tags, item.notes]
    .join(' ')
    .toLowerCase();
  return terms.every((term) => haystack.includes(term));
}

function sortEntries(entries: SearchEntry[]): SearchEntry[] {
  return [...entries].sort((left, right) => {
    const leftTime = new Date(left.item.updatedAt ?? left.item.createdAt).getTime();
    const rightTime = new Date(right.item.updatedAt ?? right.item.createdAt).getTime();
    return rightTime - leftTime;
  });
}

function formatItemBlock(entry: SearchEntry, index: number): string {
  const { item, spaceName } = entry;
  const tags = item.tags.length > 0
    ? item.tags.slice(0, 4).map((tag) => `#${tag}`).join(' ')
    : '(no tags)';
  const summary = trimText(item.summary || item.content || '(no summary)', 100);
  const meta = [
    item.url ? getDomain(item.url) : item.type,
    spaceName,
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

function buildButtons(entries: SearchEntry[], start: number, query: string, pagination: Button[] = []): Button[][] {
  const rows: Button[][] = [];

  entries.forEach(({ item }, offset) => {
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
  rows.push([{ text: `🔎 ${trimText(query, 18)}`, callback_data: `w:sp:0:${query}` }]);
  return rows;
}

function buildPayload(query: string, entries: SearchEntry[], page: number, totalPages: number): MessagePayload {
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * PAGE_SIZE;
  const pageEntries = entries.slice(start, start + PAGE_SIZE);
  const message = [
    `WALVIS Search — "${query}"`,
    `Page ${safePage}/${totalPages} • ${entries.length} match(es)`,
    '',
    ...pageEntries.flatMap((entry, index) => [formatItemBlock(entry, start + index + 1), '']),
  ].join('\n').trim();

  const pagination: Button[] = [];
  if (safePage > 1) pagination.push({ text: '⬅️ Prev', callback_data: `w:sp:${safePage - 2}:${query}` });
  if (safePage < totalPages) pagination.push({ text: '➡️ Next', callback_data: `w:sp:${safePage}:${query}` });

  return {
    action: 'send',
    channel: 'telegram',
    message,
    buttons: buildButtons(pageEntries, start, query, pagination),
  };
}

function printJson(payload: unknown): void {
  console.log(JSON.stringify(payload));
}

function printError(message: string): never {
  printJson({ error: message });
  process.exit(0);
}

function main(): void {
  const args = process.argv.slice(2);
  if (!args[0]) {
    printJson({ error: 'Usage: search.ts <query> [page]' });
    process.exit(1);
  }

  const query = args[0];
  const requestedPage = parseInt(args[1] ?? '1', 10) || 1;
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);

  if (!existsSync(SPACES_DIR)) {
    printError('WALVIS not initialized. Run: npx walvis');
  }

  let entries: SearchEntry[];
  try {
    entries = loadAllEntries();
  } catch {
    printError('Failed to read ~/.walvis/spaces');
  }

  const results = sortEntries(entries.filter(({ item }) => matchesQuery(item, terms)));
  if (results.length === 0) {
    printJson({ empty: true, query });
    return;
  }

  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE));
  const safePage = Math.min(Math.max(1, requestedPage), totalPages);
  printJson(buildPayload(query, results, safePage, totalPages));
}

main();
