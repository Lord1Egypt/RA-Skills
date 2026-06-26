#!/usr/bin/env node
'use strict';

/**
 * Intent Parser — Local query classification
 *
 * ClawHub Security: NO network access. NO file system writes.
 * Pure synchronous computation. Deterministic output.
 *
 * Usage:
 *   node scripts/intent-parser.js "<query>"
 *   echo '{"query":"..."}' | node scripts/intent-parser.js
 *
 * Output JSON:
 *   { intent, confidence, scores, entities, lang, query }
 */

const path = require('path');
const fs   = require('fs');

// ---------------------------------------------------------------------------
// Load patterns (relative to this script)
// ---------------------------------------------------------------------------
const PATTERNS_PATH = path.join(__dirname, '..', 'data', 'intent-patterns.json');
const PATTERNS = JSON.parse(fs.readFileSync(PATTERNS_PATH, 'utf8'));

// ---------------------------------------------------------------------------
// Scoring
// ---------------------------------------------------------------------------
function scoreIntents(query) {
  const lower = query.toLowerCase();
  const scores = {};

  for (const [intent, spec] of Object.entries(PATTERNS)) {
    if (intent === 'version') continue;
    let score = 0;
    for (const rule of spec.rules) {
      if (rule.keywords.some(kw => lower.includes(kw))) {
        score += rule.weight;
      }
    }
    scores[intent] = score;
  }
  return scores;
}

// ---------------------------------------------------------------------------
// Entity extraction (no regex with catastrophic backtracking)
// ---------------------------------------------------------------------------
function extractEntities(query) {
  const lower = query.toLowerCase();

  // File extensions: simple split-based, no unbounded lookahead
  const fileTypes = query.split(/\s+/)
    .filter(t => /^\.[a-zA-Z]{2,5}$/.test(t))
    .slice(0, 5);

  // URLs: safe, anchored
  const urlMatches = query.match(/https?:\/\/[a-zA-Z0-9\-._~:/?#[\]@!$&'()*+,;=%]+/g) || [];

  // Technologies: keyword list lookup (no unbounded regex)
  const techList = [
    'vue', 'react', 'angular', 'svelte', 'typescript', 'javascript',
    'python', 'nodejs', 'node', 'css', 'html', 'api', 'rest',
    'graphql', 'sql', 'mongodb', 'redis', 'docker', 'kubernetes'
  ];
  const technologies = techList.filter(t => lower.includes(t));

  return { fileTypes, urls: urlMatches.slice(0, 3), technologies };
}

// ---------------------------------------------------------------------------
// Language detection
// ---------------------------------------------------------------------------
function detectLang(query) {
  return /[\u4e00-\u9fff]/.test(query) ? 'zh' : 'en';
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function parse(query) {
  if (typeof query !== 'string' || query.trim().length === 0) {
    return { error: 'Invalid query: must be a non-empty string' };
  }

  // Sanitize: strip control characters, cap length
  const sanitized = query.replace(/[\x00-\x1f\x7f]/g, ' ').slice(0, 500).trim();

  const scores = scoreIntents(sanitized);
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const [topIntent, topScore] = entries[0] || ['web_search', 0];
  const total = entries.reduce((s, [, v]) => s + v, 0);
  const confidence = total > 0 ? +(topScore / total).toFixed(3) : 0.2;

  return {
    intent:     topIntent,
    confidence,
    scores,
    entities:   extractEntities(sanitized),
    lang:       detectLang(sanitized),
    query:      sanitized
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const arg = process.argv[2];

  if (arg) {
    // Try JSON first, fall back to raw string
    try {
      const parsed = JSON.parse(arg);
      console.log(JSON.stringify(parse(parsed.query ?? arg)));
    } catch {
      console.log(JSON.stringify(parse(arg)));
    }
    return;
  }

  // Stdin mode
  if (!process.stdin.isTTY) {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', c => { buf += c; });
    process.stdin.on('end', () => {
      try {
        const obj = JSON.parse(buf.trim());
        console.log(JSON.stringify(parse(obj.query ?? buf.trim())));
      } catch {
        console.log(JSON.stringify(parse(buf.trim())));
      }
    });
    return;
  }

  console.error('Usage: node scripts/intent-parser.js "<query>"');
  process.exit(1);
}

main();
