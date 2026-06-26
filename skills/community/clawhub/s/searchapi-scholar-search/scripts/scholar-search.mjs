#!/usr/bin/env node

function usage() {
  console.error(`Usage: scholar-search.mjs "query" [options]

Options:
  -n <count>               Number of results (default: 10, max: 20)
  --year-from <year>       Filter results from this year onward
  --year-to <year>         Filter results up to this year
  --lang <lang>            UI language hint (default: en)
  --mode <mode>            Output mode: shortlist | review | verify (default: shortlist)
  --json                   Output JSON instead of plain text
  --no-enrich-doi          Skip DOI enrichment via Crossref
  -h, --help               Show this help
`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

const query = args[0];
let n = 10;
let yearFrom = '';
let yearTo = '';
let lang = 'en';
let mode = 'shortlist';
let json = false;
let enrichDoi = true;

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  if (a === '-n') {
    n = Number.parseInt(args[i + 1] ?? '10', 10);
    i++;
    continue;
  }
  if (a === '--year-from') {
    yearFrom = args[i + 1] ?? '';
    i++;
    continue;
  }
  if (a === '--year-to') {
    yearTo = args[i + 1] ?? '';
    i++;
    continue;
  }
  if (a === '--lang') {
    lang = args[i + 1] ?? 'en';
    i++;
    continue;
  }
  if (a === '--mode') {
    mode = (args[i + 1] ?? 'shortlist').trim().toLowerCase();
    i++;
    continue;
  }
  if (a === '--json') {
    json = true;
    continue;
  }
  if (a === '--no-enrich-doi') {
    enrichDoi = false;
    continue;
  }
  console.error(`Unknown arg: ${a}`);
  usage();
}

if (!Number.isFinite(n) || n < 1) n = 10;
n = Math.max(1, Math.min(n, 20));
if (!['shortlist', 'review', 'verify'].includes(mode)) mode = 'shortlist';

const apiKey = (process.env.SERPAPI_API_KEY || process.env.SEARCHAPI_API_KEY || '').trim();
if (!apiKey) {
  console.error('Missing SERPAPI_API_KEY or SEARCHAPI_API_KEY');
  console.error('Tip: export SERPAPI_API_KEY="..." before running this skill.');
  process.exit(1);
}

function normalizeText(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/<[^>]+>/g, ' ')
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function extractYear(text) {
  const match = String(text || '').match(/\b(19|20)\d{2}\b/);
  return match ? match[0] : '';
}

function extractDoi(text) {
  const match = String(text || '').match(/10\.\d{4,9}\/[!-;=?-~]+/i);
  return match ? match[0].replace(/[).,;]+$/, '') : '';
}

function safeArray(value) {
  return Array.isArray(value) ? value : [];
}

function pickScholarResults(data) {
  return safeArray(data.organic_results).length
    ? data.organic_results
    : safeArray(data.scholar_results).length
      ? data.scholar_results
      : safeArray(data.results).length
        ? data.results
        : [];
}

function detectPaperType(title, snippet = '') {
  const text = `${title} ${snippet}`.toLowerCase();
  if (/systematic review|meta-analysis/.test(text)) return 'systematic-review';
  if (/\breview\b|\bsurvey\b/.test(text)) return 'review';
  return 'primary-study';
}

function buildSignals({ paperType, year, citedBy, doi, link, crossrefUrl }) {
  const currentYear = new Date().getFullYear();
  const y = Number(year || 0);
  const signals = [];
  if (paperType === 'systematic-review') signals.push('systematic-review');
  else if (paperType === 'review') signals.push('review-like');
  if (Number.isFinite(citedBy) && citedBy >= 100) signals.push('highly-cited');
  if (y && currentYear - y <= 2) signals.push('recent');
  if (doi) signals.push('doi-found');
  if (link || crossrefUrl) signals.push('verification-ready');
  return signals;
}

function inferWhyRelevant({ title, paperType, citedBy, year, doi }) {
  const reasons = [];
  if (paperType === 'systematic-review') reasons.push('Likely a systematic review; useful for quickly mapping the topic.');
  else if (paperType === 'review') reasons.push('Likely a review/survey paper; useful for building an initial literature overview.');
  if (Number.isFinite(citedBy) && citedBy >= 100) reasons.push('High citation count suggests this may be an influential or widely discussed paper.');
  if (year && Number(new Date().getFullYear()) - Number(year) <= 2) reasons.push('Recent publication; useful for understanding current research directions.');
  if (doi) reasons.push('DOI detected or enriched; easier to verify and cite.');
  if (reasons.length === 0 && title) reasons.push('Potentially relevant title match for the query.');
  return reasons.join(' ');
}

function buildVerificationHints({ title, doi, link }) {
  const hints = [];
  if (title) hints.push(`Search exact title: "${title}"`);
  if (doi) hints.push(`Verify DOI landing page: ${doi}`);
  if (title) hints.push(`Search exact title with DOI: "${title}" DOI`);
  if (title) hints.push(`Search publisher page: "${title}" publisher`);
  if (!link) hints.push('Look for a publisher or repository landing page before citing.');
  return hints;
}

function buildQuerySuggestions(query, mode) {
  const q = query.trim();
  const base = [];
  if (!/review|survey|systematic review/i.test(q)) {
    base.push(`${q} review`);
    base.push(`${q} systematic review`);
  }
  if (!/trend|recent|latest/i.test(q)) {
    base.push(`${q} recent trends`);
  }
  base.push(`"${q}" DOI`);
  base.push(`"${q}" publisher`);
  if (mode === 'verify') base.push(`"${q}" site:doi.org`);
  if (mode === 'review') base.push(`${q} related work`);
  return [...new Set(base)].slice(0, 6);
}

function chooseBestLink({ link, doiUrl, crossrefUrl }) {
  return doiUrl || link || crossrefUrl || '';
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

async function enrichWithCrossref(title, year = '') {
  const normalizedTitle = normalizeText(title);
  if (!normalizedTitle) return null;

  const u = new URL('https://api.crossref.org/works');
  u.searchParams.set('query.title', title);
  u.searchParams.set('rows', '5');
  u.searchParams.set('select', 'DOI,title,URL,issued,container-title,score');

  const data = await fetchJson(u, {
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'OpenClaw-searchapi-scholar-search/1.1 (+https://clawhub.com)'
    }
  });

  const items = safeArray(data?.message?.items);
  let best = null;
  let bestScore = -1;

  for (const item of items) {
    const candidateTitle = safeArray(item.title)[0] || '';
    const candidateYear = item.issued?.['date-parts']?.[0]?.[0] ? String(item.issued['date-parts'][0][0]) : '';
    const normalizedCandidate = normalizeText(candidateTitle);

    let score = 0;
    if (normalizedCandidate && normalizedCandidate === normalizedTitle) score += 100;
    else if (normalizedCandidate && (normalizedCandidate.includes(normalizedTitle) || normalizedTitle.includes(normalizedCandidate))) score += 60;

    if (year && candidateYear && year === candidateYear) score += 20;
    score += Number(item.score || 0) / 10;

    if (score > bestScore) {
      bestScore = score;
      best = item;
    }
  }

  if (!best || bestScore < 20) return null;

  return {
    doi: String(best.DOI || '').trim(),
    doiUrl: best.DOI ? `https://doi.org/${best.DOI}` : '',
    crossrefUrl: String(best.URL || '').trim(),
    containerTitle: safeArray(best['container-title'])[0] || '',
    year: best.issued?.['date-parts']?.[0]?.[0] ? String(best.issued['date-parts'][0][0]) : ''
  };
}

const u = new URL('https://serpapi.com/search.json');
u.searchParams.set('engine', 'google_scholar');
u.searchParams.set('q', query);
u.searchParams.set('num', String(n));
u.searchParams.set('api_key', apiKey);
u.searchParams.set('hl', lang || 'en');
if (yearFrom) u.searchParams.set('as_ylo', yearFrom);
if (yearTo) u.searchParams.set('as_yhi', yearTo);

let data;
try {
  data = await fetchJson(u, { headers: { 'Accept': 'application/json' } });
} catch (error) {
  const msg = String(error?.message || error);
  if (msg.includes('401') || msg.includes('403')) {
    console.error(`Scholar search failed: ${msg}`);
    console.error('Check whether the API key is valid and has access to Scholar search.');
    process.exit(1);
  }
  if (msg.includes('429')) {
    console.error(`Scholar search failed: ${msg}`);
    console.error('Rate limit hit. Reduce frequency or retry later.');
    process.exit(1);
  }
  console.error(`Scholar search failed: ${msg}`);
  process.exit(1);
}

const results = pickScholarResults(data);
if (!Array.isArray(results) || results.length === 0) {
  const emptyPayload = { query, mode, count: 0, querySuggestions: buildQuerySuggestions(query, mode), results: [] };
  if (json) {
    console.log(JSON.stringify(emptyPayload, null, 2));
  } else {
    console.log('No Scholar results found.');
    console.log('Suggestions:');
    buildQuerySuggestions(query, mode).forEach((s) => console.log(`- ${s}`));
  }
  process.exit(0);
}

const normalized = [];
for (const [idx, r] of results.slice(0, n).entries()) {
  const title = String(r.title || '').trim();
  const publicationSummary = String(r.publication_info?.summary || r.publication || '').trim();
  const snippet = String(r.snippet || '').trim();
  const inlineLink = String(r.link || '').trim();
  const resourcesLink = safeArray(r.resources).map((x) => x?.link).find(Boolean) || '';
  const link = inlineLink || String(resourcesLink || '').trim();
  const citedByRaw = r.inline_links?.cited_by?.total ?? r.cited_by?.value ?? '';
  const citedBy = citedByRaw === '' ? null : Number(citedByRaw);
  const year = extractYear(publicationSummary) || extractYear(snippet);
  const authors = safeArray(r.publication_info?.authors).map((a) => a?.name).filter(Boolean);
  let doi = extractDoi(`${title} ${publicationSummary} ${snippet} ${link}`);
  let doiUrl = doi ? `https://doi.org/${doi}` : '';
  let crossref = null;

  if (!doi && enrichDoi && title) {
    try {
      crossref = await enrichWithCrossref(title, year);
      if (crossref?.doi) {
        doi = crossref.doi;
        doiUrl = crossref.doiUrl;
      }
    } catch {
      // Ignore Crossref enrichment failures to keep the primary search usable.
    }
  }

  const paperType = detectPaperType(title, snippet);
  const bestLink = chooseBestLink({ link, doiUrl, crossrefUrl: crossref?.crossrefUrl || '' });
  const signals = buildSignals({
    paperType,
    year: crossref?.year || year,
    citedBy,
    doi,
    link,
    crossrefUrl: crossref?.crossrefUrl || ''
  });

  normalized.push({
    rank: idx + 1,
    query,
    title,
    authors,
    publicationSummary,
    venue: crossref?.containerTitle || '',
    year: crossref?.year || year,
    link,
    officialOrBestLink: bestLink,
    citedBy,
    snippet,
    doi,
    doiUrl,
    crossrefUrl: crossref?.crossrefUrl || '',
    paperType,
    signals,
    whyRelevant: inferWhyRelevant({ title, paperType, citedBy, year: crossref?.year || year, doi }),
    verificationHints: buildVerificationHints({ title, doi, link })
  });
}

const payload = {
  query,
  mode,
  count: normalized.length,
  querySuggestions: buildQuerySuggestions(query, mode),
  results: normalized
};

if (json) {
  console.log(JSON.stringify(payload, null, 2));
  process.exit(0);
}

function printSignals(signals) {
  if (!signals.length) return;
  console.log(`Signals: ${signals.join(', ')}`);
}

function printSuggestions(querySuggestions) {
  if (!querySuggestions.length) return;
  console.log('Next search suggestions:');
  querySuggestions.forEach((s) => console.log(`- ${s}`));
}

if (mode === 'verify') {
  const top = normalized[0];
  console.log(`Verification candidate for query: ${query}`);
  console.log('');
  console.log(`[1] ${top.title}`);
  if (top.authors.length) console.log(`Authors: ${top.authors.join(', ')}`);
  if (top.publicationSummary) console.log(`Source: ${top.publicationSummary}`);
  if (top.year) console.log(`Year: ${top.year}`);
  if (top.doi) console.log(`DOI: ${top.doi}`);
  if (top.officialOrBestLink) console.log(`Best link: ${top.officialOrBestLink}`);
  printSignals(top.signals);
  console.log(`Why relevant: ${top.whyRelevant}`);
  console.log('Verification hints:');
  top.verificationHints.forEach((h) => console.log(`- ${h}`));
  console.log('');
  console.log('Other candidates:');
  normalized.slice(1, 5).forEach((item) => {
    console.log(`- ${item.title}${item.year ? ` (${item.year})` : ''}`);
  });
  console.log('');
  printSuggestions(payload.querySuggestions);
  process.exit(0);
}

if (mode === 'review') {
  const reviewLike = normalized.filter((item) => item.paperType !== 'primary-study');
  const primary = normalized.filter((item) => item.paperType === 'primary-study');
  console.log(`Review-oriented results for: ${query}`);
  console.log('');
  if (reviewLike.length) {
    console.log('Review / survey candidates:');
    reviewLike.slice(0, 5).forEach((item) => {
      console.log(`- ${item.title}${item.year ? ` (${item.year})` : ''}`);
      printSignals(item.signals);
      console.log(`  Why: ${item.whyRelevant}`);
    });
    console.log('');
  }
  if (primary.length) {
    console.log('Representative primary-study candidates:');
    primary.slice(0, 5).forEach((item) => {
      console.log(`- ${item.title}${item.year ? ` (${item.year})` : ''}`);
      printSignals(item.signals);
      console.log(`  Why: ${item.whyRelevant}`);
    });
    console.log('');
  }
  printSuggestions(payload.querySuggestions);
  process.exit(0);
}

console.log(`Shortlist for: ${query}`);
console.log('');
for (const item of normalized) {
  console.log(`[${item.rank}] ${item.title}`);
  if (item.authors.length) console.log(`Authors: ${item.authors.join(', ')}`);
  if (item.publicationSummary) console.log(`Source: ${item.publicationSummary}`);
  if (item.venue && (!item.publicationSummary || !item.publicationSummary.includes(item.venue))) console.log(`Venue: ${item.venue}`);
  if (item.year) console.log(`Year: ${item.year}`);
  if (item.officialOrBestLink) console.log(`Best link: ${item.officialOrBestLink}`);
  if (item.doi) console.log(`DOI: ${item.doi}`);
  if (item.citedBy !== null) console.log(`Cited by: ${item.citedBy}`);
  printSignals(item.signals);
  console.log(`Why relevant: ${item.whyRelevant}`);
  if (item.snippet) console.log(`Snippet: ${item.snippet}`);
  console.log('');
}
printSuggestions(payload.querySuggestions);
