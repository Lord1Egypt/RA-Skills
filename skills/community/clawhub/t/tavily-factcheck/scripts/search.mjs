#!/usr/bin/env node
/**
 * Enhanced Tavily Search — aligned with official API (2026-03).
 * https://docs.tavily.com/documentation/api-reference/endpoint/search
 *
 * Improvements over upstream:
 * - Fixed const/require bugs
 * - Added: time_range, start_date, end_date, include_domains, exclude_domains,
 *   exact_match, country, finance topic, include_images
 * - Removed deprecated `days` param (use --time-range instead)
 * - Outputs response_time and request_id for debugging
 */

import { readFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';

function usage() {
  console.error(`Usage: search.mjs "query" [options]

Options:
  -n <count>              Max results (1-20, default: 5)
  --deep                  Advanced search depth (2 credits, more relevant)
  --topic <t>             general (default) | news | finance
  --time-range <r>        day | week | month | year
  --start-date <d>        YYYY-MM-DD (results after this date)
  --end-date <d>          YYYY-MM-DD (results before this date)
  --include-domains <d>   Comma-separated domains to include
  --exclude-domains <d>   Comma-separated domains to exclude
  --exact                 Only return results containing exact quoted phrases
  --country <name>        Boost results from country (full name: china, united states, japan)
  --images                Include images in results
  --raw                   Include raw markdown content from pages
  --json                  Output raw JSON instead of formatted markdown`);
  process.exit(2);
}

// ── Parse args ─────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '-h' || args[0] === '--help') usage();

const query = args[0];
const opts = {
  maxResults: 5,
  searchDepth: 'basic',
  topic: 'general',
  timeRange: null,
  startDate: null,
  endDate: null,
  includeDomains: null,
  excludeDomains: null,
  exactMatch: false,
  country: null,
  includeImages: false,
  includeRawContent: false,
  jsonOutput: false,
};

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  const next = () => { i++; return args[i]; };
  switch (a) {
    case '-n': opts.maxResults = Math.max(1, Math.min(Number.parseInt(next() ?? '5', 10), 20)); break;
    case '--deep': opts.searchDepth = 'advanced'; break;
    case '--topic': opts.topic = next() ?? 'general'; break;
    case '--time-range': opts.timeRange = next(); break;
    case '--start-date': opts.startDate = next(); break;
    case '--end-date': opts.endDate = next(); break;
    case '--include-domains': opts.includeDomains = (next() ?? '').split(',').map(d => d.trim()).filter(Boolean); break;
    case '--exclude-domains': opts.excludeDomains = (next() ?? '').split(',').map(d => d.trim()).filter(Boolean); break;
    case '--exact': opts.exactMatch = true; break;
    case '--country': opts.country = next(); break;
    case '--images': opts.includeImages = true; break;
    case '--raw': opts.includeRawContent = true; break;
    case '--json': opts.jsonOutput = true; break;
    default: console.error(`Unknown arg: ${a}`); usage();
  }
}

if (!['general', 'news', 'finance'].includes(opts.topic)) {
  console.error(`Invalid topic: ${opts.topic}. Must be general, news, or finance.`);
  process.exit(2);
}

// ── Resolve API key ────────────────────────────────────────────────────

let apiKey = (process.env.TAVILY_API_KEY ?? '').trim();

if (!apiKey) {
  // Fallback: read from ~/.openclaw/.env or ~/.env
  for (const envPath of [
    path.join(homedir(), '.openclaw', '.env'),
    path.join(homedir(), '.env'),
  ]) {
    try {
      const content = await readFile(envPath, 'utf-8');
      const match = content.match(/TAVILY_API_KEY\s*=\s*(\S+)/);
      if (match?.[1]) {
        apiKey = match[1].trim();
        break;
      }
    } catch { /* file not found, continue */ }
  }
}

if (!apiKey) {
  console.error('Missing TAVILY_API_KEY. Set env var or add to ~/.openclaw/.env');
  process.exit(1);
}

// ── Build request ──────────────────────────────────────────────────────

const body = {
  api_key: apiKey,
  query,
  search_depth: opts.searchDepth,
  topic: opts.topic,
  max_results: opts.maxResults,
  include_answer: true,
  include_raw_content: opts.includeRawContent ? 'markdown' : false,
  include_images: opts.includeImages,
};

if (opts.timeRange) body.time_range = opts.timeRange;
if (opts.startDate) body.start_date = opts.startDate;
if (opts.endDate) body.end_date = opts.endDate;
if (opts.includeDomains?.length) body.include_domains = opts.includeDomains;
if (opts.excludeDomains?.length) body.exclude_domains = opts.excludeDomains;
if (opts.exactMatch) body.exact_match = true;
if (opts.country) body.country = opts.country;

// ── Execute search ─────────────────────────────────────────────────────

const resp = await fetch('https://api.tavily.com/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => '');
  console.error(`Tavily Search failed (${resp.status}): ${text.slice(0, 500)}`);
  process.exit(1);
}

const data = await resp.json();

// ── Output ─────────────────────────────────────────────────────────────

if (opts.jsonOutput) {
  process.stdout.write(JSON.stringify(data, null, 2) + '\n');
  process.exit(0);
}

// Formatted markdown output
if (data.answer) {
  console.log('## Answer\n');
  console.log(data.answer);
  console.log('\n---\n');
}

const results = (data.results ?? []).slice(0, opts.maxResults);
if (results.length > 0) {
  console.log('## Sources\n');
  for (const r of results) {
    const title = String(r?.title ?? '').trim();
    const url = String(r?.url ?? '').trim();
    const content = String(r?.content ?? '').trim();
    const score = r?.score ? ` (relevance: ${(r.score * 100).toFixed(0)}%)` : '';
    if (!title || !url) continue;
    console.log(`- **${title}**${score}`);
    console.log(`  ${url}`);
    if (content) {
      console.log(`  ${content.slice(0, 400)}${content.length > 400 ? '...' : ''}`);
    }
    console.log();
  }
}

if (data.images?.length && opts.includeImages) {
  console.log('## Images\n');
  for (const img of data.images.slice(0, 5)) {
    const imgUrl = typeof img === 'string' ? img : img?.url;
    const desc = typeof img === 'object' ? img?.description : '';
    if (imgUrl) console.log(`- ${imgUrl}${desc ? ` — ${desc}` : ''}`);
  }
  console.log();
}

// Footer: timing and debug info
const timing = data.response_time ? `${data.response_time.toFixed(2)}s` : 'N/A';
console.log(`---\n_Search: "${query}" | depth: ${opts.searchDepth} | topic: ${opts.topic} | results: ${results.length} | time: ${timing}_`);
