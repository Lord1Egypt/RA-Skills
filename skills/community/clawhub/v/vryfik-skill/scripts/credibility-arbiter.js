#!/usr/bin/env node
'use strict';

/**
 * Credibility Arbiter — Domain reputation scoring (pure computation)
 *
 * ClawHub Security: NO network access. NO file system writes.
 * Reads domain-reputation.json once at startup. Pure synchronous scoring.
 *
 * Input  JSON: { sources: [{ url, domain?, content? }] }
 * Output JSON: { results: [{ domain, tier, score, verdict }], overallScore }
 */

const fs   = require('fs');
const path = require('path');
const url  = require('url');

// ---------------------------------------------------------------------------
// Load reputation data
// ---------------------------------------------------------------------------
const REP_PATH = path.join(__dirname, '..', 'data', 'domain-reputation.json');
const REP      = JSON.parse(fs.readFileSync(REP_PATH, 'utf8'));

// Build fast lookup: domain → tier
const DOMAIN_TIER = {};
for (const [tier, domains] of Object.entries(REP.tiers)) {
  for (const d of domains) DOMAIN_TIER[d] = tier;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function extractDomain(rawUrl) {
  try {
    const parsed = new url.URL(rawUrl.startsWith('http') ? rawUrl : `https://${rawUrl}`);
    // Remove www. prefix for consistent lookup
    return parsed.hostname.replace(/^www\./, '');
  } catch {
    return rawUrl.toLowerCase().replace(/^www\./, '').split('/')[0];
  }
}

function scoreDomain(domain) {
  // Exact match first
  if (DOMAIN_TIER[domain] !== undefined) {
    const tier = DOMAIN_TIER[domain];
    return { tier, score: REP.scores[tier] };
  }

  // Subdomain fallback: check parent domain
  const parts = domain.split('.');
  if (parts.length > 2) {
    const parent = parts.slice(-2).join('.');
    if (DOMAIN_TIER[parent] !== undefined) {
      const tier = DOMAIN_TIER[parent];
      return { tier, score: REP.scores[tier] };
    }
  }

  // Blocked patterns
  if (REP.tiers.blocked.includes(domain)) {
    return { tier: 'blocked', score: 0 };
  }

  return { tier: 'unknown', score: REP.scores.unknown };
}

// Content heuristic scoring (no network — works on provided content snippet)
function scoreContent(content) {
  if (!content || typeof content !== 'string') return 1.0;  // neutral

  const lower = content.toLowerCase();
  let score = 1.0;

  // Positive signals
  if (/```|<code>|\.js|\.ts|\.py/.test(lower))   score += 0.1;  // has code
  if (/\d{4}/.test(lower))                        score += 0.05; // has dates
  if (lower.includes('example') || lower.includes('示例')) score += 0.05;

  // Negative signals
  if (lower.includes('click here') || lower.includes('buy now')) score -= 0.3;
  if ((lower.match(/!/g) || []).length > 5)       score -= 0.2;  // excessive exclamation

  return Math.min(1.2, Math.max(0.1, score));
}

// ---------------------------------------------------------------------------
// Dual-source agreement check
// ---------------------------------------------------------------------------
function dualSourceAgreement(results) {
  if (results.length < 2) return { agreed: null, reason: 'single_source' };

  const highQuality = results.filter(r => r.score >= 0.6);
  if (highQuality.length < 2) return { agreed: false, reason: 'insufficient_quality_sources' };

  // Simple agreement: both high-quality sources returned results
  return { agreed: true, sources: highQuality.map(r => r.domain) };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function arbitrate(sources) {
  if (!Array.isArray(sources) || sources.length === 0) {
    return { error: 'sources must be a non-empty array' };
  }

  const results = sources.slice(0, 10).map(src => {
    const domain    = src.domain || extractDomain(src.url || '');
    const { tier, score: domainScore } = scoreDomain(domain);
    const contentMult = scoreContent(src.content);
    const finalScore  = +(domainScore * contentMult).toFixed(3);

    return {
      domain,
      tier,
      domainScore,
      contentMultiplier: +contentMult.toFixed(3),
      finalScore,
      verdict: finalScore >= 0.7 ? 'trust' : finalScore >= 0.4 ? 'verify' : 'reject'
    };
  });

  const overallScore = results.length > 0
    ? +(results.reduce((s, r) => s + r.finalScore, 0) / results.length).toFixed(3)
    : 0;

  return {
    results,
    overallScore,
    dualSource: dualSourceAgreement(results),
    recommendation: overallScore >= 0.7 ? 'proceed'
      : overallScore >= 0.4             ? 'verify_before_use'
      :                                   'reject_find_better_sources'
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const arg = process.argv[2];

  if (!arg) {
    console.error('Usage: node scripts/credibility-arbiter.js \'{"sources":[{"url":"..."}]}\'');
    process.exit(1);
  }

  try {
    const input = JSON.parse(arg);
    console.log(JSON.stringify(arbitrate(input.sources)));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

main();
