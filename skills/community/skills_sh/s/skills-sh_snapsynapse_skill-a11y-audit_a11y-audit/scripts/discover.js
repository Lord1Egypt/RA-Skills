#!/usr/bin/env node
/*
skill_bundle: a11y-audit
file_role: script
version: 3
version_date: 2026-05-31
previous_version: 2
change_summary: >
  Added bounded fetches, same-origin discovery defaults, explicit
  cross-origin sitemap opt-in, and origin disclosure.
*/

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const DEFAULT_MAX_BYTES = 2 * 1024 * 1024;
const DEFAULT_MAX_REDIRECTS = 5;

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) { args[key] = true; continue; }
    args[key] = next;
    i += 1;
  }
  return args;
}

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

function fetchResource(url, opts = {}, state = {}) {
  return new Promise((resolve) => {
    const requestUrl = new URL(url);
    const redirects = state.redirects || 0;
    const maxRedirects = Number.isFinite(opts.maxRedirects) ? opts.maxRedirects : DEFAULT_MAX_REDIRECTS;
    const maxBytes = Number.isFinite(opts.maxBytes) ? opts.maxBytes : DEFAULT_MAX_BYTES;
    const allowedOrigins = opts.allowedOrigins || null;

    if (allowedOrigins && !allowedOrigins.has(requestUrl.origin)) {
      return resolve({
        blocked: true,
        reason: 'cross-origin',
        url: requestUrl.href,
        origin: requestUrl.origin,
      });
    }

    const mod = requestUrl.protocol === 'https:' ? https : http;
    const req = mod.get(requestUrl, { timeout: 10000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const redirectUrl = new URL(res.headers.location, requestUrl).href;
        res.resume();
        if (redirects >= maxRedirects) {
          return resolve({
            blocked: true,
            reason: 'redirect-limit',
            url: redirectUrl,
            origin: new URL(redirectUrl).origin,
          });
        }
        return resolve(fetchResource(redirectUrl, opts, { redirects: redirects + 1 }));
      }
      if (res.statusCode !== 200) {
        res.resume();
        return resolve(null);
      }
      const chunks = [];
      let totalBytes = 0;
      let tooLarge = false;
      res.on('data', (c) => {
        totalBytes += c.length;
        if (totalBytes > maxBytes) {
          tooLarge = true;
          res.resume();
          req.destroy();
          return;
        }
        chunks.push(c);
      });
      res.on('end', () => resolve({
        body: tooLarge ? null : Buffer.concat(chunks).toString('utf8'),
        url: requestUrl.href,
        blocked: tooLarge,
        reason: tooLarge ? 'max-bytes' : null,
        origin: requestUrl.origin,
      }));
    });
    req.on('timeout', () => {
      req.destroy();
      resolve(null);
    });
    req.on('error', () => resolve(null));
  });
}

async function httpFetch(url, opts = {}) {
  const resource = await fetchResource(url, opts);
  return resource && !resource.blocked ? resource.body : null;
}

function resolvePublishedUrl(value, baseUrl) {
  return new URL(value, baseUrl).href;
}

// ---------------------------------------------------------------------------
// Sitemap parsing (simple XML — no dependency needed)
// ---------------------------------------------------------------------------

function parseSitemap(xml) {
  const urls = [];
  const re = /<loc>(.*?)<\/loc>/g;
  let m;
  while ((m = re.exec(xml)) !== null) urls.push(m[1].trim());
  return urls;
}

// ---------------------------------------------------------------------------
// HTML link extraction (fallback when no sitemap)
// ---------------------------------------------------------------------------

function extractLinks(html, baseUrl) {
  const links = new Set();
  const re = /<a\s[^>]*href="([^"#?]+)"/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    let href = m[1];
    if (href.startsWith('mailto:') || href.startsWith('javascript:')) continue;
    if (!href.startsWith('http')) href = new URL(href, baseUrl).href;
    try {
      const u = new URL(href);
      const base = new URL(baseUrl);
      if (u.origin === base.origin) links.add(href);
    } catch { /* skip malformed */ }
  }
  return [...links];
}

// ---------------------------------------------------------------------------
// URL pattern classification
// ---------------------------------------------------------------------------

function classifyUrl(urlStr) {
  const u = new URL(urlStr);
  let pathname = u.pathname;
  pathname = pathname.replace(/\/index\.html$/, '/');
  if (pathname === '/') return { pattern: '/', segments: [] };

  const parts = pathname.split('/').filter(Boolean);
  if (parts.length > 0) parts[parts.length - 1] = parts[parts.length - 1].replace(/\.html$/, '');

  if (parts.length === 1) return { pattern: parts[0], segments: parts };

  const patternParts = [parts[0], ...parts.slice(1).map(() => '*')];
  return { pattern: patternParts.join('/'), segments: parts };
}

// ---------------------------------------------------------------------------
// DOM fingerprinting (lightweight — loads HTML, counts structural elements)
// ---------------------------------------------------------------------------

function computeFingerprint(html) {
  if (!html) return { score: 0, elements: {} };

  // Count elements inside <main> if present, else whole body
  let region = html;
  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  if (mainMatch) region = mainMatch[1];

  const counts = {};
  const tags = ['table', 'details', 'form', 'input', 'select', 'button', 'ul', 'ol', 'dl', 'h1', 'h2', 'h3', 'h4', 'img', 'canvas', 'svg', 'iframe', 'video', 'audio'];
  for (const tag of tags) {
    const re = new RegExp(`<${tag}[\\s>]`, 'gi');
    const matches = region.match(re);
    if (matches) counts[tag] = matches.length;
  }

  // Count data attributes that imply interactivity
  const sortable = (region.match(/data-sortable/gi) || []).length;
  const filterable = (region.match(/data-filterable/gi) || []).length;
  if (sortable) counts['[data-sortable]'] = sortable;
  if (filterable) counts['[data-filterable]'] = filterable;

  // Complexity score: weighted sum
  const weights = { table: 3, details: 2, form: 3, input: 2, select: 2, button: 1, dl: 2, iframe: 4, video: 4, canvas: 3, svg: 1, '[data-sortable]': 2, '[data-filterable]': 2 };
  let score = 0;
  for (const [tag, count] of Object.entries(counts)) {
    score += count * (weights[tag] || 1);
  }

  return { score, elements: counts };
}

async function fingerprintCandidates(urls, fetchOpts = {}) {
  // Load HTML for each candidate and compute fingerprint
  const results = [];
  for (const url of urls) {
    const html = await httpFetch(url, fetchOpts);
    const fp = computeFingerprint(html);
    results.push({ url, ...fp });
  }
  return results.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return a.url.localeCompare(b.url);
  });
}

// ---------------------------------------------------------------------------
// Representative selection (with optional fingerprinting)
// ---------------------------------------------------------------------------

function buildCandidateIndexes(total, limit = 8) {
  if (total <= 0) return [];
  if (total === 1) return [0];

  const candidateCount = Math.min(limit, total);
  const indexes = new Set();
  for (let i = 0; i < candidateCount; i += 1) {
    indexes.add(Math.floor((i * (total - 1)) / (candidateCount - 1)));
  }
  return [...indexes].sort((a, b) => a - b);
}

async function selectRepresentatives(group, maxPerGroup, useFingerprint, fetchOpts = {}) {
  const urls = group.urls.sort();
  if (urls.length <= Math.max(maxPerGroup, 3)) {
    return { selected: urls, reason: `all ${urls.length} — small group` };
  }

  if (useFingerprint) {
    const candidateIdxs = buildCandidateIndexes(urls.length);
    const candidates = candidateIdxs.map((i) => urls[i]);

    const fingerprinted = await fingerprintCandidates(candidates, fetchOpts);
    if (fingerprinted.length > 0 && fingerprinted[0].score > 0) {
      // Pick most complex and least complex
      const selected = [fingerprinted[0].url];
      const least = fingerprinted[fingerprinted.length - 1];
      if (least.url !== selected[0]) selected.push(least.url);
      if (maxPerGroup >= 3 && fingerprinted.length > 2) {
        const mid = fingerprinted[Math.floor(fingerprinted.length / 2)];
        if (!selected.includes(mid.url)) selected.push(mid.url);
      }
      return {
        selected: selected.slice(0, maxPerGroup),
        reason: `${selected.length} of ${urls.length} — by DOM complexity (scores: ${fingerprinted[0].score}→${least.score})`,
        fingerprints: fingerprinted,
      };
    }
  }

  // Fallback: alphabetic spread
  const selected = [urls[0], urls[urls.length - 1]];
  if (maxPerGroup >= 3 && urls.length > 4) {
    selected.splice(1, 0, urls[Math.floor(urls.length / 2)]);
  }
  return {
    selected: selected.slice(0, maxPerGroup),
    reason: `${selected.length} of ${urls.length} — alphabetic spread`,
  };
}

// ---------------------------------------------------------------------------
// API entity enrichment
// ---------------------------------------------------------------------------

function enrichGroupLabel(pattern, apiManifest) {
  if (!apiManifest) return null;
  // Support both "endpoints" and "files" keys (common API index patterns)
  const catalog = apiManifest.endpoints || apiManifest.files;
  if (!catalog) return null;

  // Map URL patterns to API endpoint names
  const patternToEndpoint = {
    'regulation/*': 'regulations',
    'obligation/*': 'obligations',
    'authority/*': 'authorities',
    'applies-to/*': 'jurisdictions',
    'standard/*': 'standards',
    'requires/*/*': 'provisions',
  };

  const endpointKey = patternToEndpoint[pattern];
  if (!endpointKey) return null;

  const endpoint = catalog[endpointKey];
  if (!endpoint) return null;

  return {
    entityType: endpointKey,
    description: endpoint.description || null,
    count: endpoint.count || null,
  };
}

// ---------------------------------------------------------------------------
// Main discovery
// ---------------------------------------------------------------------------

async function discover(runtimeUrl, opts = {}) {
  const maxPerGroup = parseInt(opts.maxPerGroup, 10) || 2;
  const useFingerprint = opts.fingerprint !== false;
  const baseOrigin = new URL(runtimeUrl).origin;
  const allowCrossOriginSitemaps = opts.allowCrossOriginSitemaps === true;
  const fetchOpts = {
    allowedOrigins: allowCrossOriginSitemaps ? null : new Set([baseOrigin]),
    maxBytes: Number.isFinite(opts.maxBytes) ? opts.maxBytes : DEFAULT_MAX_BYTES,
    maxRedirects: Number.isFinite(opts.maxRedirects) ? opts.maxRedirects : DEFAULT_MAX_REDIRECTS,
  };

  let allUrls = [];
  let source = 'unknown';
  const blockedFetches = [];

  const recordBlocked = (resource) => {
    if (resource && resource.blocked) {
      blockedFetches.push({
        url: resource.url,
        origin: resource.origin,
        reason: resource.reason,
      });
      return true;
    }
    return false;
  };

  // 1. Try sitemap via well-known paths
  if (!opts.noSitemap) {
    const sitemapUrls = [
      `${baseOrigin}/sitemap.xml`,
      `${baseOrigin}/sitemap_index.xml`,
    ];

    const robotsResource = await fetchResource(`${baseOrigin}/robots.txt`, fetchOpts);
    if (recordBlocked(robotsResource)) {
      // Continue with default same-origin sitemap paths.
    } else if (robotsResource) {
      const sitemapMatch = robotsResource.body.match(/Sitemap:\s*(\S+)/i);
      if (sitemapMatch) {
        try {
          sitemapUrls.unshift(resolvePublishedUrl(sitemapMatch[1], robotsResource.url));
        } catch { /* use defaults */ }
      }
    }

    for (const sitemapUrl of [...new Set(sitemapUrls)]) {
      const xmlResource = await fetchResource(sitemapUrl, fetchOpts);
      if (recordBlocked(xmlResource)) continue;
      const xml = xmlResource && xmlResource.body;
      if (xml && (xml.includes('<urlset') || xml.includes('<sitemapindex'))) {
        let discoveredUrls = parseSitemap(xml).map((entry) => {
          try {
            return resolvePublishedUrl(entry, xmlResource.url);
          } catch {
            return entry;
          }
        });

        if (xml.includes('<sitemapindex')) {
          const subSitemaps = discoveredUrls;
          discoveredUrls = [];
          for (const sub of subSitemaps) {
            const subXmlResource = await fetchResource(sub, fetchOpts);
            if (recordBlocked(subXmlResource)) continue;
            if (!subXmlResource) continue;
            discoveredUrls.push(...parseSitemap(subXmlResource.body).map((entry) => {
              try {
                return resolvePublishedUrl(entry, subXmlResource.url);
              } catch {
                return entry;
              }
            }));
          }
        }

        allUrls = [...new Set(discoveredUrls)];
        source = `sitemap (${sitemapUrl})`;
        break;
      }
    }
  }

  // 2. Fallback: crawl navigation links
  if (allUrls.length === 0) {
    const html = await httpFetch(runtimeUrl, fetchOpts);
    if (html) {
      allUrls = extractLinks(html, runtimeUrl);
      source = 'html-crawl (depth 1)';

      const hubUrls = [...allUrls];
      for (const hubUrl of hubUrls.slice(0, 20)) {
        const hubHtml = await httpFetch(hubUrl, fetchOpts);
        if (hubHtml) {
          const deeper = extractLinks(hubHtml, hubUrl);
          for (const d of deeper) {
            if (!allUrls.includes(d)) allUrls.push(d);
          }
        }
      }
      source = `html-crawl (depth 2, ${allUrls.length} links)`;
    }
  }

  if (allUrls.length === 0) {
    return { error: 'No pages discovered. Check the URL and try --no-sitemap for crawl mode.' };
  }

  // 3. Classify into groups
  const groupMap = new Map();
  for (const url of allUrls) {
    const { pattern } = classifyUrl(url);
    if (!groupMap.has(pattern)) groupMap.set(pattern, { pattern, urls: [] });
    groupMap.get(pattern).urls.push(url);
  }

  // 4. Fetch API manifest for enrichment
  let apiManifest = null;
  for (const apiPath of ['/api/v1/index.json', '/api/index.json']) {
    const apiJson = await httpFetch(`${baseOrigin}${apiPath}`, fetchOpts);
    if (apiJson) {
      try { apiManifest = JSON.parse(apiJson); break; } catch { /* skip */ }
    }
  }

  // 5. Select representatives (with fingerprinting for large groups)
  const groups = [];
  const scanList = [];

  const sorted = [...groupMap.values()].sort((a, b) => {
    const aIsTopLevel = !a.pattern.includes('/') && !a.pattern.includes('*');
    const bIsTopLevel = !b.pattern.includes('/') && !b.pattern.includes('*');
    if (aIsTopLevel && !bIsTopLevel) return -1;
    if (!aIsTopLevel && bIsTopLevel) return 1;
    return b.urls.length - a.urls.length;
  });

  let fingerprintCount = 0;
  for (const group of sorted) {
    const isTopLevel = !group.pattern.includes('/') && !group.pattern.includes('*');
    let selected, reason, fingerprints;

    if (isTopLevel || group.urls.length === 1) {
      selected = group.urls.sort();
      reason = isTopLevel ? 'top-level page — always included' : 'singleton — always included';
    } else {
      // Only fingerprint groups with 4+ pages to limit HTTP requests
      const shouldFingerprint = useFingerprint && group.urls.length >= 4;
      ({ selected, reason, fingerprints } = await selectRepresentatives(group, maxPerGroup, shouldFingerprint, fetchOpts));
      if (shouldFingerprint) fingerprintCount += 1;
    }

    // Enrich with API data
    const enrichment = enrichGroupLabel(group.pattern, apiManifest);

    const groupEntry = {
      pattern: group.pattern,
      count: group.urls.length,
      selected,
      reason,
    };
    if (enrichment) groupEntry.entity = enrichment;
    if (fingerprints) groupEntry.fingerprints = fingerprints.slice(0, 5); // keep top 5

    groups.push(groupEntry);
    scanList.push(...selected);
  }

  const discoveredOrigins = [...new Set(allUrls.map((url) => {
    try {
      return new URL(url).origin;
    } catch {
      return null;
    }
  }).filter(Boolean))].sort();

  return {
    source,
    runtimeUrl,
    originPolicy: allowCrossOriginSitemaps ? 'cross-origin-sitemaps-allowed' : 'same-origin',
    discoveredOrigins,
    blockedFetches,
    totalPages: allUrls.length,
    selectedPages: scanList.length,
    coverageRatio: `${groups.length} template groups, ${scanList.length} pages selected`,
    fingerprintedGroups: fingerprintCount,
    apiManifest: apiManifest ? {
      version: apiManifest.meta?.version,
      endpoints: Object.keys(apiManifest.endpoints || apiManifest.files || {}).length,
    } : null,
    groups,
    scanList,
  };
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const url = args.url;
  if (!url) {
    console.error('Usage: discover.js --url <base-url> [--output <path>] [--max-per-group N] [--no-sitemap] [--no-fingerprint] [--allow-cross-origin-sitemaps]');
    process.exit(1);
  }

  const result = await discover(url, {
    maxPerGroup: args['max-per-group'],
    noSitemap: args['no-sitemap'] === true || args['no-sitemap'] === 'true',
    fingerprint: !(args['no-fingerprint'] === true || args['no-fingerprint'] === 'true'),
    allowCrossOriginSitemaps: args['allow-cross-origin-sitemaps'] === true || args['allow-cross-origin-sitemaps'] === 'true',
  });

  if (result.error) {
    console.error(result.error);
    process.exit(1);
  }

  const outputPath = args.output ? path.resolve(args.output) : null;
  const json = JSON.stringify(result, null, 2);

  if (outputPath) {
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, json);
    console.log(outputPath);
  } else {
    console.log(json);
  }

  // Summary to stderr
  console.error(`\nDiscovery: ${result.totalPages} pages found via ${result.source}`);
  console.error(`Origin policy: ${result.originPolicy}; origins: ${result.discoveredOrigins.join(', ') || 'none'}`);
  if (result.blockedFetches.length > 0) {
    console.error(`Blocked fetches: ${result.blockedFetches.length}`);
  }
  console.error(`Selected ${result.selectedPages} pages across ${result.groups.length} template groups`);
  if (result.fingerprintedGroups > 0) {
    console.error(`DOM fingerprinting used on ${result.fingerprintedGroups} groups`);
  }
  for (const g of result.groups) {
    const label = g.entity && g.entity.count ? ` (${g.entity.count} ${g.entity.entityType})` : '';
    console.error(`  ${g.pattern}${label}: ${g.count} pages → ${g.selected.length} selected (${g.reason})`);
  }
}

module.exports = {
  buildCandidateIndexes,
  classifyUrl,
  computeFingerprint,
  discover,
  extractLinks,
  fetchResource,
  fingerprintCandidates,
  httpFetch,
  parseSitemap,
  selectRepresentatives,
};

if (require.main === module) {
  main().catch((err) => {
    console.error(err.stack || String(err));
    process.exit(1);
  });
}
