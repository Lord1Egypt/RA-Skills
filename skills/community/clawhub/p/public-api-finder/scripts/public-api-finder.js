#!/usr/bin/env node
import { mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';

const SOURCE_URL = 'https://public-api-lists.github.io/public-api-lists/api/all.json';
const CACHE_PATH = join(homedir(), '.cache', 'public-api-finder', 'all.json');
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;

function usage() {
  console.log(`public-api-finder — find public APIs for agents and prototypes

Usage:
  public-api-finder <query> [options]

Options:
  --category <name>  Filter by category substring
  --no-auth          Only APIs with Auth = No
  --https            Only HTTPS APIs
  --cors <value>     Filter by CORS: Yes, No, Unknown
  --limit <n>        Max results (default: 8)
  --json             Emit JSON
  --refresh          Refresh cache
  -h, --help         Show help

Examples:
  public-api-finder "weather forecast" --no-auth --https
  public-api-finder "crypto prices" --category Cryptocurrency --limit 5
  public-api-finder "jobs" --json
`);
}

function parseArgs(argv) {
  const args = { query: '', limit: 8, json: false, refresh: false };
  const parts = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') args.help = true;
    else if (a === '--no-auth') args.noAuth = true;
    else if (a === '--https') args.https = true;
    else if (a === '--json') args.json = true;
    else if (a === '--refresh') args.refresh = true;
    else if (a === '--category') args.category = argv[++i] || '';
    else if (a === '--cors') args.cors = argv[++i] || '';
    else if (a === '--limit') args.limit = Number(argv[++i] || 8);
    else parts.push(a);
  }
  args.query = parts.join(' ').trim();
  return args;
}

function tokenSet(text) {
  return new Set(String(text).toLowerCase().match(/[a-z0-9]+/g)?.filter(t => t.length > 1) || []);
}

function intersectionCount(a, b) {
  let n = 0;
  for (const x of a) if (b.has(x)) n++;
  return n;
}

function score(entry, queryTokens) {
  const name = tokenSet(entry.name);
  const category = tokenSet(entry.category);
  const desc = tokenSet(entry.description);
  const all = new Set([...name, ...category, ...desc]);
  return 5 * intersectionCount(queryTokens, name)
    + 4 * intersectionCount(queryTokens, category)
    + 2 * intersectionCount(queryTokens, desc)
    + intersectionCount(queryTokens, all);
}

async function cacheIsFresh() {
  try {
    const s = await stat(CACHE_PATH);
    return Date.now() - s.mtimeMs < CACHE_TTL_MS;
  } catch {
    return false;
  }
}

async function loadData(refresh = false) {
  if (!refresh && await cacheIsFresh()) {
    return JSON.parse(await readFile(CACHE_PATH, 'utf8')).entries || [];
  }
  const res = await fetch(SOURCE_URL);
  if (!res.ok) throw new Error(`failed to fetch API list: HTTP ${res.status}`);
  const data = await res.json();
  await mkdir(dirname(CACHE_PATH), { recursive: true });
  await writeFile(CACHE_PATH, JSON.stringify(data, null, 2));
  return data.entries || [];
}

function filterEntries(entries, args) {
  const q = tokenSet(args.query);
  return entries.flatMap(e => {
    if (args.category && !String(e.category || '').toLowerCase().includes(args.category.toLowerCase())) return [];
    if (args.noAuth && String(e.auth || '').toLowerCase() !== 'no') return [];
    if (args.https && !e.https) return [];
    if (args.cors && String(e.cors || '').toLowerCase() !== args.cors.toLowerCase()) return [];
    const s = q.size ? score(e, q) : 1;
    if (q.size && s === 0) return [];
    return [{ ...e, score: s }];
  }).sort((a, b) => b.score - a.score || String(a.category).localeCompare(String(b.category)) || String(a.name).localeCompare(String(b.name))).slice(0, args.limit);
}

function printMarkdown(rows) {
  if (!rows.length) {
    console.log('No matching public APIs found. Try broader terms or remove filters.');
    return;
  }
  rows.forEach((e, i) => {
    console.log(`${i + 1}. **${e.name}** (${e.category}) — ${e.description}`);
    console.log(`   - URL: ${e.url}`);
    console.log(`   - Auth: \`${e.auth}\` · HTTPS: ${e.https ? 'yes' : 'no'} · CORS: ${e.cors} · score: ${e.score}`);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.query) {
    usage();
    return args.help ? 0 : 1;
  }
  const rows = filterEntries(await loadData(args.refresh), args);
  if (args.json) console.log(JSON.stringify(rows, null, 2));
  else printMarkdown(rows);
  return 0;
}

main().then(code => process.exitCode = code).catch(err => {
  console.error(`public-api-finder: ${err.message}`);
  process.exitCode = 1;
});
