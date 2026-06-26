#!/usr/bin/env node

function usage() {
  console.error(`Usage: web-search.mjs "query" [options]

Options:
  -n <count>      Number of results (default: 10, max: 20)
  --lang <lang>   UI language hint (default: en)
  --json          Output JSON instead of plain text
  -h, --help      Show this help
`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

const query = args[0];
let n = 10;
let lang = 'en';
let json = false;
for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '-n') {
    n = Number.parseInt(args[i + 1] ?? '10', 10);
    i++;
    continue;
  }
  if (a === '--lang') {
    lang = args[i + 1] ?? 'en';
    i++;
    continue;
  }
  if (a === '--json') {
    json = true;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

if (!Number.isFinite(n) || n < 1) n = 10;
n = Math.max(1, Math.min(n, 20));

const apiKey = (process.env.SERPAPI_API_KEY || process.env.SEARCHAPI_API_KEY || '').trim();
if (!apiKey) {
  console.error('Missing SERPAPI_API_KEY or SEARCHAPI_API_KEY');
  console.error('Tip: export SERPAPI_API_KEY="..." before running this skill.');
  process.exit(1);
}

async function fetchJson(url, options = {}) {
  const resp = await fetch(url, options);
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    const detail = text.slice(0, 500).trim();
    throw new Error(`${resp.status} ${resp.statusText}${detail ? ` — ${detail}` : ''}`);
  }
  return resp.json();
}

const u = new URL('https://serpapi.com/search.json');
u.searchParams.set('engine', 'google');
u.searchParams.set('q', query);
u.searchParams.set('num', String(n));
u.searchParams.set('api_key', apiKey);
u.searchParams.set('hl', lang || 'en');

let data;
try {
  data = await fetchJson(u, { headers: { 'Accept': 'application/json' } });
} catch (error) {
  const msg = String(error?.message || error);
  if (msg.includes('401') || msg.includes('403')) {
    console.error(`Web search failed: ${msg}`);
    console.error('Check whether the API key is valid and has access to web search.');
    process.exit(1);
  }
  if (msg.includes('429')) {
    console.error(`Web search failed: ${msg}`);
    console.error('Rate limit hit. Reduce frequency or retry later.');
    process.exit(1);
  }
  console.error(`Web search failed: ${msg}`);
  process.exit(1);
}

const results = Array.isArray(data.organic_results) ? data.organic_results : [];
if (json) {
  console.log(JSON.stringify({
    query,
    count: results.slice(0, n).length,
    results: results.slice(0, n).map((r, idx) => ({
      rank: idx + 1,
      title: String(r.title || '').trim(),
      link: String(r.link || '').trim(),
      snippet: String(r.snippet || '').trim(),
      displayedLink: String(r.displayed_link || '').trim()
    }))
  }, null, 2));
  process.exit(0);
}

results.slice(0, n).forEach((r, idx) => {
  const title = String(r.title || '').trim();
  const link = String(r.link || '').trim();
  const snippet = String(r.snippet || '').trim();
  const displayedLink = String(r.displayed_link || '').trim();
  console.log(`[${idx + 1}] ${title}`);
  if (displayedLink) console.log(`Site: ${displayedLink}`);
  if (link) console.log(`Link: ${link}`);
  if (snippet) console.log(`Snippet: ${snippet}`);
  console.log('');
});
