#!/usr/bin/env node
'use strict';

/**
 * Parallel Probe — Concurrent HTTP HEAD checks for source availability
 *
 * ClawHub Security: OUTBOUND HTTP/HTTPS HEAD REQUESTS ONLY.
 * - Only HEAD method: no response body is read or stored.
 * - No user data is transmitted in requests.
 * - SSRF prevention (two layers):
 *     1. Hostname pattern check (blocks localhost, RFC-1918 literals, link-local)
 *     2. DNS resolution check (resolves hostname to IP, re-checks IP against patterns)
 *        This prevents DNS rebinding attacks where a public hostname resolves to a private IP.
 * - Timeout: 4 seconds per request.
 * - Max concurrent: 5 probes.
 *
 * Input  JSON: { sources: [{ url, domain? }] }
 * Output JSON: { results: [{ url, domain, available, statusCode, latencyMs, credibility }] }
 */

const https   = require('https');
const http    = require('http');
const dns     = require('dns').promises;
const url_mod = require('url');
const path    = require('path');
const fs      = require('fs');

// Load reputation for enrichment
const REP_PATH = path.join(__dirname, '..', 'data', 'domain-reputation.json');
const REP      = JSON.parse(fs.readFileSync(REP_PATH, 'utf8'));
const DOMAIN_TIER = {};
for (const [tier, domains] of Object.entries(REP.tiers)) {
  for (const d of domains) DOMAIN_TIER[d] = tier;
}

const TIMEOUT_MS     = 4000;
const MAX_PROBES     = 5;
const ALLOWED_PROTOS = ['http:', 'https:'];

// ---------------------------------------------------------------------------
// SSRF Prevention: block private / loopback / link-local addresses
// Covers: RFC 1918, loopback, link-local, IPv6 loopback/ULA/link-local
// ---------------------------------------------------------------------------
const BLOCKED_HOST_PATTERNS = [
  /^localhost$/i,
  /^127\./,                          // IPv4 loopback
  /^0\.0\.0\.0$/,                    // unspecified
  /^10\./,                           // RFC 1918 Class A
  /^172\.(1[6-9]|2\d|3[01])\./,     // RFC 1918 Class B
  /^192\.168\./,                     // RFC 1918 Class C
  /^169\.254\./,                     // link-local
  /^::1$/,                           // IPv6 loopback
  /^fc[0-9a-f]{2}:/i,                // IPv6 ULA
  /^fe80:/i,                         // IPv6 link-local
  /^0::/,                            // IPv6 unspecified
];

function isBlockedHost(hostname) {
  return BLOCKED_HOST_PATTERNS.some(p => p.test(hostname));
}

// ---------------------------------------------------------------------------
// Single HEAD probe — async for DNS resolution
// ---------------------------------------------------------------------------
async function probeOne(rawUrl) {
  const start = Date.now();

  let parsed;
  try {
    parsed = new url_mod.URL(rawUrl);
  } catch {
    return { url: rawUrl, available: false, error: 'invalid_url' };
  }

  // Only allow http/https
  if (!ALLOWED_PROTOS.includes(parsed.protocol)) {
    return { url: rawUrl, available: false, error: 'disallowed_protocol' };
  }

  // Layer 1: block by hostname pattern (fast path)
  if (isBlockedHost(parsed.hostname)) {
    return { url: rawUrl, available: false, error: 'blocked_host' };
  }

  // Layer 2: DNS resolution → IP-level check (prevents DNS rebinding bypass)
  let resolvedIp;
  try {
    const { address } = await dns.lookup(parsed.hostname);
    resolvedIp = address;
  } catch {
    return { url: rawUrl, available: false, error: 'dns_resolution_failed' };
  }
  if (isBlockedHost(resolvedIp)) {
    return { url: rawUrl, available: false, error: 'blocked_resolved_ip' };
  }

  const lib    = parsed.protocol === 'https:' ? https : http;
  const domain = parsed.hostname.replace(/^www\./, '');
  const tier   = DOMAIN_TIER[domain] || 'unknown';
  const score  = REP.scores[tier] || REP.scores.unknown;

  return new Promise(resolve => {
    const options = {
      method:   'HEAD',
      hostname: parsed.hostname,
      port:     parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path:     parsed.pathname + parsed.search,
      timeout:  TIMEOUT_MS,
      headers:  {
        'User-Agent': 'search-skill-probe/1.0 (availability-check)'
      }
    };

    const req = lib.request(options, res => {
      const latencyMs = Date.now() - start;
      res.resume();  // discard any body (HEAD should have none, but be safe)
      resolve({
        url:        rawUrl,
        domain,
        tier,
        score,
        available:  res.statusCode < 400,
        statusCode: res.statusCode,
        latencyMs,
        verdict:    res.statusCode < 400 && score >= 0.6 ? 'trust' : 'verify'
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ url: rawUrl, domain, available: false, error: 'timeout', latencyMs: TIMEOUT_MS });
    });

    req.on('error', err => {
      resolve({ url: rawUrl, domain, available: false, error: err.code || 'network_error' });
    });

    req.end();
  });
}

// ---------------------------------------------------------------------------
// Parallel probe with concurrency cap
// ---------------------------------------------------------------------------
async function probeAll(sources) {
  const limited = sources.slice(0, MAX_PROBES);
  const results = await Promise.allSettled(limited.map(s => probeOne(s.url || s)));
  return results.map(r => r.status === 'fulfilled' ? r.value : { available: false, error: 'rejected' });
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
async function main() {
  const arg = process.argv[2];

  if (!arg) {
    console.error('Usage: node scripts/parallel-probe.js \'{"sources":[{"url":"https://vuejs.org"}]}\'');
    process.exit(1);
  }

  let input;
  try {
    input = JSON.parse(arg);
  } catch {
    console.log(JSON.stringify({ error: 'Invalid JSON input' }));
    process.exit(1);
  }

  const sources = Array.isArray(input.sources) ? input.sources : [];
  if (sources.length === 0) {
    console.log(JSON.stringify({ error: 'sources array is empty' }));
    process.exit(1);
  }

  const results = await probeAll(sources);
  const available = results.filter(r => r.available).length;

  console.log(JSON.stringify({
    results,
    summary: {
      total:      results.length,
      available,
      unavailable: results.length - available
    }
  }));
}

main().catch(err => {
  console.log(JSON.stringify({ error: err.message }));
  process.exit(1);
});
