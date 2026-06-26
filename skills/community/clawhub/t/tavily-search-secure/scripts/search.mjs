#!/usr/bin/env node

function usage() {
  console.error('Usage: search.mjs "query" [-n 5] [--deep] [--topic general|news] [--days 7] [--timeout 20000]');
  process.exit(2);
}

function fail(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function cleanText(input, maxLen = 1000) {
  return String(input ?? '')
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLen);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

const query = String(args[0] ?? '').trim();
if (!query) fail('Query boş olamaz.');
if (query.length > 500) fail('Query çok uzun (max 500 karakter).');

let n = 5;
let searchDepth = 'basic';
let topic = 'general';
let days = null;
let timeoutMs = 20000;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '-n') {
    n = Number.parseInt(args[i + 1] ?? '5', 10);
    i++;
    continue;
  }
  if (a === '--deep') {
    searchDepth = 'advanced';
    continue;
  }
  if (a === '--topic') {
    topic = String(args[i + 1] ?? 'general');
    i++;
    continue;
  }
  if (a === '--days') {
    days = Number.parseInt(args[i + 1] ?? '7', 10);
    i++;
    continue;
  }
  if (a === '--timeout') {
    timeoutMs = Number.parseInt(args[i + 1] ?? '20000', 10);
    i++;
    continue;
  }
  fail(`Unknown arg: ${a}`, 2);
}

n = Math.max(1, Math.min(Number.isFinite(n) ? n : 5, 10));
if (!['general', 'news'].includes(topic)) fail('topic sadece general veya news olabilir.');
if (days != null) {
  days = Math.max(1, Math.min(Number.isFinite(days) ? days : 7, 30));
}
timeoutMs = Math.max(3000, Math.min(Number.isFinite(timeoutMs) ? timeoutMs : 20000, 60000));

const apiKey = String(process.env.TAVILY_API_KEY ?? '').trim();
if (!apiKey) fail('Missing TAVILY_API_KEY');

const body = {
  api_key: apiKey,
  query,
  search_depth: searchDepth,
  topic,
  max_results: n,
  include_answer: true,
  include_raw_content: false,
};

if (topic === 'news' && days) {
  body.days = days;
}

const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), timeoutMs);

let resp;
try {
  resp = await fetch('https://api.tavily.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
    signal: controller.signal,
  });
} catch (err) {
  clearTimeout(timer);
  fail(`Tavily isteği başarısız: ${err?.name === 'AbortError' ? 'zaman aşımı' : 'ağ hatası'}`);
}
clearTimeout(timer);

if (!resp.ok) {
  const text = await resp.text().catch(() => '');
  fail(`Tavily Search failed (${resp.status}): ${cleanText(text, 240)}`);
}

const data = await resp.json();

const answer = cleanText(data?.answer ?? '', 4000);
if (answer) {
  console.log('## Answer\n');
  console.log(answer);
  console.log('\n---\n');
}

const results = Array.isArray(data?.results) ? data.results.slice(0, n) : [];
console.log('## Sources\n');

for (const r of results) {
  const title = cleanText(r?.title, 300);
  const url = cleanText(r?.url, 1200);
  const content = cleanText(r?.content, 400);
  const scoreNum = Number(r?.score);
  const score = Number.isFinite(scoreNum) ? ` (relevance: ${(scoreNum * 100).toFixed(0)}%)` : '';

  if (!title || !url) continue;
  console.log(`- **${title}**${score}`);
  console.log(`  ${url}`);
  if (content) console.log(`  ${content}`);
  console.log();
}
