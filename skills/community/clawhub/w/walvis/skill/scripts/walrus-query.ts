#!/usr/bin/env node
/**
 * WALVIS query script
 * Search bookmarks in local spaces
 *
 * Usage:
 *   walrus-query search <query>          - full-text search across all spaces
 *   walrus-query tags                    - list all tags with counts
 *   walrus-query list [spaceId]          - list items in a space
 *   walrus-query tag <tagName>           - filter by tag
 */

import { readManifest, listSpaceFiles, SPACES_DIR } from './storage.js';
import type { BookmarkItem, Space } from './types.js';
import { readFileSync } from 'fs';
import { join } from 'path';

function loadAllSpaces(): Space[] {
  return listSpaceFiles().map(f =>
    JSON.parse(readFileSync(join(SPACES_DIR, f), 'utf-8')) as Space
  );
}

function scoreItem(item: BookmarkItem, query: string): number {
  const q = query.toLowerCase();
  const terms = q.split(/\s+/);
  let score = 0;

  const titleLower = item.title.toLowerCase();
  const summaryLower = item.summary.toLowerCase();
  const tagsLower = item.tags.join(' ').toLowerCase();
  const contentLower = item.content.toLowerCase();

  for (const term of terms) {
    if (titleLower.includes(term)) score += 10;
    if (tagsLower.includes(term)) score += 8;
    if (summaryLower.includes(term)) score += 5;
    if (contentLower.includes(term)) score += 2;
  }

  // Exact phrase bonus
  if (titleLower.includes(q)) score += 5;
  if (summaryLower.includes(q)) score += 3;

  return score;
}

export interface SearchResult {
  item: BookmarkItem;
  spaceName: string;
  spaceId: string;
  score: number;
}

export function searchAll(query: string, limit = 10): SearchResult[] {
  const spaces = loadAllSpaces();
  const results: SearchResult[] = [];

  for (const space of spaces) {
    for (const item of space.items) {
      const score = scoreItem(item, query);
      if (score > 0) {
        results.push({ item, spaceName: space.name, spaceId: space.id, score });
      }
    }
  }

  return results.sort((a, b) => b.score - a.score).slice(0, limit);
}

export function listAllTags(): Array<{ tag: string; count: number }> {
  const spaces = loadAllSpaces();
  const tagCounts = new Map<string, number>();

  for (const space of spaces) {
    for (const item of space.items) {
      for (const tag of item.tags) {
        tagCounts.set(tag, (tagCounts.get(tag) ?? 0) + 1);
      }
    }
  }

  return Array.from(tagCounts.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count);
}

export function filterByTag(tagName: string): SearchResult[] {
  const spaces = loadAllSpaces();
  const results: SearchResult[] = [];
  const tag = tagName.toLowerCase();

  for (const space of spaces) {
    for (const item of space.items) {
      if (item.tags.some(t => t.toLowerCase() === tag)) {
        results.push({ item, spaceName: space.name, spaceId: space.id, score: 1 });
      }
    }
  }

  return results.sort((a, b) => b.item.createdAt.localeCompare(a.item.createdAt));
}

export function formatResultsForTelegram(results: SearchResult[], query?: string): string {
  if (results.length === 0) {
    return query ? `No results found for "${query}"` : 'No items found.';
  }

  const lines = results.map((r, i) => {
    const tags = r.item.tags.map(t => `#${t}`).join(' ');
    const url = r.item.url ? `\n   🔗 ${r.item.url}` : '';
    return `${i + 1}. **${r.item.title}**${url}\n   ${r.item.summary.slice(0, 100)}...\n   ${tags} [${r.spaceName}]`;
  });

  const header = query ? `Search results for "${query}":\n\n` : '';
  return header + lines.join('\n\n');
}

// CLI entry point
const [,, cmd, ...args] = process.argv;

if (cmd === 'search') {
  const query = args.join(' ');
  if (!query) { console.error('Usage: walrus-query search <query>'); process.exit(1); }
  const results = searchAll(query);
  console.log(formatResultsForTelegram(results, query));

} else if (cmd === 'tags') {
  const tags = listAllTags();
  if (tags.length === 0) { console.log('No tags found.'); }
  else tags.forEach(({ tag, count }) => console.log(`  #${tag}: ${count}`));

} else if (cmd === 'tag') {
  const tagName = args[0];
  if (!tagName) { console.error('Usage: walrus-query tag <tagName>'); process.exit(1); }
  const results = filterByTag(tagName);
  console.log(formatResultsForTelegram(results));

} else if (cmd === 'list') {
  const spaces = loadAllSpaces();
  for (const space of spaces) {
    console.log(`\n[${space.name}] (${space.items.length} items)`);
    for (const item of space.items.slice(0, 20)) {
      const tags = item.tags.map(t => `#${t}`).join(' ');
      console.log(`  • ${item.title} ${tags}`);
    }
  }
} else {
  console.error('Usage: walrus-query search|tags|tag|list [args]');
  process.exit(1);
}
