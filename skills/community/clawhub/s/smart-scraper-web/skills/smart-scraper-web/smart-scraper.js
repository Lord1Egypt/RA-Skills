#!/usr/bin/env node
/**
 * Smart Web Scraping — Extract structured data from websites
 * 
 * Modes:
 *   --extract <url>                      → Extract structured data from page
 *   --extract --table <url>              → Extract tables from page
 *   --extract --list <url>               → Extract lists from page
 *   --extract --price <url>              → Extract prices from page
 *   --extract --article <url>            → Extract article content
 *   --extract --all <url>                → Extract everything
 *   --parse <html>                       → Parse raw HTML
 *   --status                             → Scraping status
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const WORKSPACE = (() => {
  if (process.env.SCRAPER_DIR) {
    // Validate: resolve to real path and ensure it's not traversing into dangerous areas
    const customDir = path.resolve(process.env.SCRAPER_DIR);
    // Block absolute paths that point to root, /etc, /proc, /sys, /dev etc.
    const blockedRoots = ['/', '/etc', '/proc', '/sys', '/dev', '/bin', '/sbin', '/boot', '/lib', '/usr', '/var', '/opt'];
    for (const root of blockedRoots) {
      if (customDir === root || customDir.startsWith(root + path.sep)) {
        return path.resolve(__dirname, '..', '..');
      }
    }
    return customDir;
  }
  let dir = __dirname;
  const root = path.parse(dir).root;
  for (let i = 0; i < 10; i++) {
    if (path.resolve(dir) === root) break;
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const CACHE_DIR = path.join(WORKSPACE, 'memory', 'scraper-cache');
const CACHE_FILE = path.join(CACHE_DIR, 'cache.json');
const DIFFS_DIR = path.join(CACHE_DIR, 'diffs');

// ── Cache limits ─────────────────────────────────────────────────────────────
const MAX_CACHE_ENTRIES = 50;
const MAX_CACHE_BYTES = 10 * 1024 * 1024; // 10MB
const CACHE_TTL = 300000; // 5 minutes

// ── CLI flags ────────────────────────────────────────────────────────────────
let useCache = false; // Cache disabled by default; --cache to enable
let watchUrl = null, watchInterval = null, watchAlert = false, watchDiffOnly = false;

// ── Redirect limits ──────────────────────────────────────────────────────────
const MAX_REDIRECTS = 5;
const REQUEST_TIMEOUT = 15000; // 15 seconds
const RATE_LIMIT_MS = 100; // minimum delay between requests

// ── SSRF blocklist ───────────────────────────────────────────────────────────
const BLOCKED_SCHEMES = ['file:', 'gopher:', 'data:', 'javascript:', 'ftp:'];
const PRIVATE_IP_RANGES = [
  /^127\./,          // localhost
  /^10\./,           // 10.0.0.0/8
  /^172\.(1[6-9]|2[0-9]|3[01])\./, // 172.16.0.0/12
  /^192\.168\./,     // 192.168.0.0/16
  /^169\.254\./,     // link-local
  /^0\./,            // 0.0.0.0/8
  /^::1$/,           // IPv6 localhost
  /^fc[0-9a-f]{2}:/, // IPv6 unique local
  /^fe[89ab][0-9a-f]:/, // IPv6 link-local
];
const CLOUD_METADATA_IPS = [
  '169.254.169.254',
  '169.254.170.2',
  '169.254.169.253',
];

// ── JSON parse limits ─────────────────────────────────────────────────────
const MAX_JSON_FILE_BYTES = 10 * 1024 * 1024; // 10MB before parse

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const stat = fs.statSync(file);
    if (stat.size > MAX_JSON_FILE_BYTES) {
      console.error(`[smart-scraper] Cache file too large (${formatBytes(stat.size)}), ignoring`);
      return fallback || {};
    }
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

// ─── URL VALIDATION ────────────────────────────────────────────────────────

function validateUrl(inputUrl) {
  let parsed;
  try {
    parsed = new URL(inputUrl);
  } catch {
    return { valid: false, error: `Invalid URL: ${inputUrl}` };
  }

  // Block dangerous schemes
  if (BLOCKED_SCHEMES.includes(parsed.protocol)) {
    return { valid: false, error: `Blocked scheme: ${parsed.protocol}` };
  }

  // Only allow http and https
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    return { valid: false, error: `Only http/https URLs allowed, got: ${parsed.protocol}` };
  }

  // Block cloud metadata endpoints
  if (CLOUD_METADATA_IPS.includes(parsed.hostname)) {
    return { valid: false, error: `Blocked cloud metadata endpoint: ${parsed.hostname}` };
  }

  // Block private/internal IPs
  const ip = parsed.hostname;
  for (const range of PRIVATE_IP_RANGES) {
    if (range.test(ip)) {
      return { valid: false, error: `Blocked private/internal IP: ${ip}` };
    }
  }

  // Block localhost variants
  if (['localhost', '0.0.0.0', '[::]', '::1'].includes(parsed.hostname)) {
    return { valid: false, error: `Blocked localhost: ${parsed.hostname}` };
  }

  return { valid: true, parsed };
}

// ─── HTTP FETCH (safe, with redirect limit and rate limiting) ────────────

let lastRequestTime = 0;

async function fetchPage(url, redirectCount = 0, originalUrl = null) {
  // Rate limiting
  const now = Date.now();
  const wait = RATE_LIMIT_MS - (now - lastRequestTime);
  if (wait > 0) await new Promise(r => setTimeout(r, wait));
  lastRequestTime = Date.now();

  // Max redirect limit
  if (redirectCount > MAX_REDIRECTS) {
    throw new Error(`Too many redirects (${MAX_REDIRECTS})`);
  }

  // Re-validate redirect target to prevent SSRF bypass
  if (redirectCount > 0) {
    const redirectValidation = validateUrl(url);
    if (!redirectValidation.valid) {
      throw new Error(`Redirect blocked: ${redirectValidation.error} (redirect target: ${url})`);
    }
    if (!originalUrl) {
      originalUrl = url;
    }
  }

  return new Promise((resolve, reject) => {
    const isHttps = url.startsWith('https');
    const client = isHttps ? https : http;

    const req = client.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; SmartScraper/1.0)' },
      timeout: REQUEST_TIMEOUT
    }, (res) => {
      // Handle redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        req.destroy();
        fetchPage(res.headers.location, redirectCount + 1, originalUrl || url)
          .then(resolve)
          .catch(reject);
        return;
      }

      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });

    req.on('error', reject);
    req.setTimeout(REQUEST_TIMEOUT, () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

// ─── HTML PARSING ──────────────────────────────────────────────────────────

function decodeHtmlEntities(text) {
  const entities = {
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
    '&#39;': "'",
    '&#x27;': "'",
    '&#x2F;': '/',
    '&#x60;': '`',
    '&#x3D;': '=',
    '&nbsp;': ' ',
    '&copy;': '©',
    '&reg;': '®',
    '&trade;': '™',
    '&mdash;': '—',
    '&ndash;': '–',
    '&hellip;': '…',
    '&lsquo;': "'",
    '&rsquo;': "'",
    '&ldquo;': '"',
    '&rdquo;': '"',
    '&bull;': '•',
    '&middot;': '·',
  };
  // Decode named entities first
  for (const [entity, char] of Object.entries(entities)) {
    text = text.split(entity).join(char);
  }
  // Decode numeric entities like &#123; and &#x1F;
  text = text.replace(/&#(\d{1,7});/g, (_, code) => String.fromCodePoint(parseInt(code, 10)));
  text = text.replace(/&#[xX]([0-9a-fA-F]{1,6});/g, (_, code) => String.fromCodePoint(parseInt(code, 16)));
  return text;
}

function stripHtml(html) {
  return decodeHtmlEntities(html
    .replace(/<script[^>]*>[\s\S]{0,50000}?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]{0,50000}?<\/style>/gi, '')
    .replace(/<[^>]{0,1024}>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim());
}

function parseHtml(html) {
  // Simple HTML parser for common patterns
  const result = {
    title: '',
    headings: [],
    paragraphs: [],
    links: [],
    tables: [],
    lists: [],
    prices: [],
    images: [],
    metadata: {}
  };
  
  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (titleMatch) result.title = decodeHtmlEntities(titleMatch[1].trim());
  
  // Extract headings
  const headingRegex = /<h([1-6])[^>]{0,1024}>([^<]{0,10000})<\/h\1>/gi;
  let match;
  while ((match = headingRegex.exec(html)) !== null) {
    result.headings.push({ level: parseInt(match[1]), text: decodeHtmlEntities(match[2].trim()) });
  }
  
  // Extract paragraphs
  const paraRegex = /<p[^>]{0,1024}>([\s\S]{0,100000})<\/p>/gi;
  while ((match = paraRegex.exec(html)) !== null) {
    const text = stripHtml(match[1]).trim();
    if (text.length > 20) result.paragraphs.push(text);
  }
  
  // Extract links
  const linkRegex = /<a[^>]{0,1024}href="([^"]{0,2048})"[^>]{0,1024}>([^<]{0,10000})<\/a>/gi;
  while ((match = linkRegex.exec(html)) !== null) {
    result.links.push({ url: match[1], text: decodeHtmlEntities(match[2].trim()) });
  }
  
  // Extract images
  const imgRegex = /<img[^>]{0,1024}src="([^"]{0,2048})"[^>]{0,1024}alt="([^"]{0,2048})"[^>]{0,1024}\/?>/gi;
  while ((match = imgRegex.exec(html)) !== null) {
    result.images.push({ src: match[1], alt: match[2] });
  }
  
  // Extract tables
  const tableRegex = /<table[\s\S]{0,500000}?<\/table>/gi;
  while ((match = tableRegex.exec(html)) !== null) {
    const tableHtml = match[0];
    const rows = [];
    const rowRegex = /<tr[\s\S]{0,500000}?<\/tr>/gi;
    let rowMatch;
    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      const cells = [];
      const cellRegex = /<(th|td)[^>]{0,1024}>([\s\S]{0,100000})<\/\1>/gi;
      let cellMatch;
      while ((cellMatch = cellRegex.exec(rowMatch[0])) !== null) {
        cells.push(stripHtml(cellMatch[2]).trim());
      }
      if (cells.length > 0) rows.push(cells);
    }
    if (rows.length > 0) result.tables.push(rows);
  }
  
  // Extract lists
  const listRegex = /<ul[\s\S]{0,500000}?<\/ul>|<ol[\s\S]{0,500000}?<\/ol>/gi;
  while ((match = listRegex.exec(html)) !== null) {
    const listHtml = match[0];
    const items = [];
    const itemRegex = /<li[^>]{0,1024}>([\s\S]{0,100000})<\/li>/gi;
    let itemMatch;
    while ((itemMatch = itemRegex.exec(listHtml)) !== null) {
      const text = stripHtml(itemMatch[1]).trim();
      if (text.length > 0) items.push(text);
    }
    if (items.length > 0) result.lists.push(items);
  }
  
  // Extract prices (common patterns)
  const priceRegex = /[\$€£¥]\s*\d+(?:,\d{3})*(?:\.\d{2})?/g;
  let priceMatch;
  while ((priceMatch = priceRegex.exec(html)) !== null) {
    result.prices.push(priceMatch[0]);
  }
  
  // Extract meta tags
  const metaRegex = /<meta[^>]*(?:name|property|itemprop)=["']([^"']+)["'][^>]*content=["']([^"']+)["'][^>]*\/?>/gi;
  while ((match = metaRegex.exec(html)) !== null) {
    result.metadata[match[1]] = decodeHtmlEntities(match[2]);
  }
  
  return result;
}

// ─── EXTRACT ───────────────────────────────────────────────────────────────

async function extractFromUrl(url, mode = 'all') {
  // Validate URL before fetching
  const validation = validateUrl(url);
  if (!validation.valid) {
    console.error(`[smart-scraper] Invalid URL: ${validation.error}`);
    console.error(`[smart-scraper] Only http/https URLs to public hosts are allowed.`);
    process.exit(1);
  }

  // Check cache
  const cache = loadJSON(CACHE_FILE, {});
  const cacheKey = url;
  let data = null;
  
  // Use cache only if enabled AND we have a valid cache entry
  const hasValidCache = cache[cacheKey] && (Date.now() - cache[cacheKey].timestamp < CACHE_TTL);
  
  if (useCache && hasValidCache) {
    console.log(`[smart-scraper] Cache hit: ${url}`);
    data = cache[cacheKey].data;
  } else {
    // Evict expired entries
    const now = Date.now();
    for (const [key, entry] of Object.entries(cache)) {
      if (now - entry.timestamp > CACHE_TTL) {
        delete cache[key];
      }
    }
    // Evict oldest if over limit
    while (Object.keys(cache).length >= MAX_CACHE_ENTRIES) {
      let oldestKey = null;
      let oldestTime = Infinity;
      for (const [key, entry] of Object.entries(cache)) {
        if (entry.timestamp < oldestTime) {
          oldestTime = entry.timestamp;
          oldestKey = key;
        }
      }
      if (oldestKey) delete cache[oldestKey];
    }

    // Fetch page
    const html = await fetchPage(url);

    // Parse
    data = parseHtml(html);
    data.url = url;
    data.fetchedAt = new Date().toISOString();
    data.contentLength = html.length;

    // Cache (only if --cache specified)
    if (useCache) {
      // SECURITY: Warn every time caching is active — privacy must be visible
      console.error(`⚠️  [smart-scraper] Caching scraped data to disk: ${CACHE_FILE}`);
      console.error(`    Stored: title, headings, paragraphs, links, tables, lists, prices, images, metadata`);
      console.error(`    To enable: add --cache to your command`);
      // Store full parsed data for cache hits to work correctly
      cache[cacheKey] = { timestamp: Date.now(), data };
      saveJSON(CACHE_FILE, cache);
    }
  }
  
  // Output based on mode
  switch (mode) {
    case 'table':
      console.log(`[smart-scraper] Tables found (${data.tables.length}):\n`);
      for (const table of data.tables.slice(0, 3)) {
        for (const row of table.slice(0, 5)) {
          console.log('  ' + row.join(' | '));
        }
        console.log('');
      }
      break;
    case 'list':
      console.log(`[smart-scraper] Lists found (${data.lists.length}):\n`);
      for (const list of data.lists.slice(0, 3)) {
        console.log(`  ${list.length} items:`);
        for (const item of list.slice(0, 10)) {
          console.log(`    • ${item.substring(0, 80)}`);
        }
        console.log('');
      }
      break;
    case 'price':
      console.log(`[smart-scraper] Prices found (${data.prices.length}):\n`);
      for (const price of data.prices.slice(0, 20)) {
        console.log(`  ${price}`);
      }
      break;
    case 'article':
      console.log(`[smart-scraper] Article content:\n`);
      console.log(`  Title: ${data.title}`);
      console.log(`  Headings: ${data.headings.length}`);
      console.log(`  Paragraphs: ${data.paragraphs.length}`);
      console.log('\n  First paragraphs:');
      for (const p of data.paragraphs.slice(0, 5)) {
        console.log(`    ${p.substring(0, 120)}...`);
      }
      break;
    default: // all
      console.log(`[smart-scraper] Extracted from ${url}:\n`);
      console.log(`  Title: ${data.title}`);
      console.log(`  Headings: ${data.headings.length}`);
      console.log(`  Paragraphs: ${data.paragraphs.length}`);
      console.log(`  Links: ${data.links.length}`);
      console.log(`  Tables: ${data.tables.length}`);
      console.log(`  Lists: ${data.lists.length}`);
      console.log(`  Prices: ${data.prices.length}`);
      console.log(`  Images: ${data.images.length}`);
      console.log(`  Metadata keys: ${Object.keys(data.metadata).length}`);
      console.log(`  Content length: ${data.contentLength.toLocaleString()} chars`);
      break;
  }
  
  return data;
}

// ─── CHANGE MONITORING ─────────────────────────────────────────────────────

function urlToHash(url) {
  let hash = 0;
  for (let i = 0; i < url.length; i++) {
    const char = url.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash).toString(16);
}

function loadSnapshot(url) {
  const hash = urlToHash(url);
  const file = path.join(DIFFS_DIR, `${hash}.json`);
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch { return null; }
}

function saveSnapshot(url, data) {
  const hash = urlToHash(url);
  ensureDir(DIFFS_DIR);
  const file = path.join(DIFFS_DIR, `${hash}.json`);
  fs.writeFileSync(file, JSON.stringify({ url, timestamp: new Date().toISOString(), data }, null, 2));
}

function diffSnapshots(oldData, newData) {
  const changes = [];
  
  // Compare prices
  const oldPrices = new Map(oldData.prices.map(p => [p.text.trim(), p]));
  for (const p of newData.prices) {
    const key = p.text.trim();
    if (!oldPrices.has(key)) {
      changes.push({ type: 'new', category: 'price', value: p.text });
    } else {
      const old = oldPrices.get(key);
      if (old.amount !== p.amount) {
        changes.push({ type: 'changed', category: 'price', from: old.amount, to: p.amount, text: key });
      }
    }
  }
  for (const [key, old] of oldPrices) {
    if (!newData.prices.find(p => p.text.trim() === key)) {
      changes.push({ type: 'removed', category: 'price', value: old.text });
    }
  }
  
  // Compare headings
  const oldHeadings = new Set(oldData.headings.map(h => h.text.trim()));
  for (const h of newData.headings) {
    const text = h.text.trim();
    if (!oldHeadings.has(text)) changes.push({ type: 'new', category: 'heading', value: text });
  }
  for (const text of oldHeadings) {
    if (!newData.headings.find(h => h.text.trim() === text)) changes.push({ type: 'removed', category: 'heading', value: text });
  }
  
  // Compare list items
  const oldLists = oldData.lists.map(l => l.items.map(i => i.trim()).join('\n')).join('\n');
  const newList = newData.lists.map(l => l.items.map(i => i.trim()).join('\n')).join('\n');
  if (oldLists !== newList) {
    changes.push({ type: 'changed', category: 'lists', from: `${oldData.lists.length} lists`, to: `${newData.lists.length} lists` });
  }
  
  // Compare links
  const oldLinks = new Set(oldData.links.map(l => l.href));
  for (const l of newData.links) {
    if (!oldLinks.has(l.href)) changes.push({ type: 'new', category: 'link', value: `${l.text} → ${l.href}` });
  }
  
  return changes;
}

async function watchMode(url, interval = null, alertOnChange = false, diffOnly = false) {
  ensureDir(DIFFS_DIR);
  const snapshot = loadSnapshot(url);
  
  console.log(`[smart-scraper] Watching: ${url}`);
  
  if (!snapshot) {
    // First run — capture baseline
    console.log('[smart-scraper] No baseline found. Capturing baseline...');
    const data = await extractFromUrl(url, 'all');
    saveSnapshot(url, data);
    console.log(`[smart-scraper] ✅ Baseline captured (${data.contentLength.toLocaleString()} chars)`);
    return 0;
  }
  
  // Re-scrape
  console.log('[smart-scraper] Re-scraping...');
  const newData = await extractFromUrl(url, 'all');
  
  // Compare
  const changes = diffSnapshots(snapshot.data, newData);
  
  if (changes.length === 0) {
    console.log('[smart-scraper] No changes detected.');
    return 0;
  }
  
  // Show changes
  console.log(`\n[smart-scraper] ${changes.length} change(s) detected:\n`);
  for (const c of changes) {
    switch (c.type) {
      case 'new':
        console.log(`  ➕ New ${c.category}: ${c.value}`);
        break;
      case 'removed':
        console.log(`  ➖ Removed ${c.category}: ${c.value}`);
        break;
      case 'changed':
        console.log(`  🔄 Changed ${c.category}: ${c.from || c.text} → ${c.to || 'N/A'}`);
        break;
    }
  }
  
  // Update snapshot
  saveSnapshot(url, newData);
  
  return alertOnChange ? 1 : 0;
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const cache = loadJSON(CACHE_FILE, {});
  let cacheSize = 0;
  for (const [, data] of Object.entries(cache)) {
    cacheSize += JSON.stringify(data.data).length;
  }
  
  console.log('[smart-scraper] Status:\n');
  console.log(`  Cached pages: ${Object.keys(cache).length}`);
  console.log(`  Cache size: ${formatBytes(cacheSize)}`);
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let cliMode = 'status';
let searchQuery = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--extract') cliMode = 'extract';
  if (args[i] === '--parse') cliMode = 'parse';
  if (args[i] === '--status') cliMode = 'status';
  if (args[i] === '--watch') {
    cliMode = 'watch';
    watchUrl = args[i + 1];
    watchInterval = args[i + 2];
    watchAlert = args.includes('--alert-on-change');
    watchDiffOnly = args.includes('--diff-only');
  }
  if (args[i] === '--table') searchQuery = 'table';
  if (args[i] === '--list') searchQuery = 'list';
  if (args[i] === '--price') searchQuery = 'price';
  if (args[i] === '--article') searchQuery = 'article';
  if (args[i] === '--all') searchQuery = 'all';
  if (args[i] === '--cache') useCache = true;
  if (args[i] === '--no-cache') useCache = false;
  if (args[i] === '--dir' && i + 1 < args.length) process.env.SCRAPER_DIR = args[i + 1];
}

// Find the first non-flag argument (URL or HTML)
function findArg() {
  for (const a of args) {
    if (!a.startsWith('--')) return a;
  }
  return null;
}

(async () => {
  switch (cliMode) {
    case 'extract': {
      const url = findArg();
      if (!url) {
        console.log('Usage: smart-scraper.js --extract <url>');
      } else {
        await extractFromUrl(url, searchQuery || 'all');
      }
      break;
    }
    case 'watch': {
      const url = watchUrl || findArg();
      if (!url) {
        console.log('Usage: smart-scraper.js --watch <url> [interval]');
        console.log('  Flags: --alert-on-change (exit 1 on change), --diff-only');
      } else {
        const exitCode = await watchMode(url, watchInterval, watchAlert, watchDiffOnly);
        process.exit(exitCode);
      }
      break;
    }
    case 'parse': {
      const html = findArg();
      if (!html) {
        console.log('Usage: smart-scraper.js --parse "<html content>"');
      } else {
        const data = parseHtml(html);
        console.log('[smart-scraper] Parsed HTML:\n');
        console.log(`  Title: ${data.title}`);
        console.log(`  Headings: ${data.headings.length}`);
        console.log(`  Paragraphs: ${data.paragraphs.length}`);
        console.log(`  Links: ${data.links.length}`);
        console.log(`  Tables: ${data.tables.length}`);
        console.log(`  Lists: ${data.lists.length}`);
        console.log(`  Prices: ${data.prices.length}`);
      }
      break;
    }
    default:
      showStatus();
      break;
  }
})();
