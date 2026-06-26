#!/usr/bin/env node
/**
 * analyze_vector_search.js — summarize vector_search usage logs
 *
 * Outputs JSON report: total queries, hit rate, avg score, avg duration, date range
 *
 * Usage: node /home/openclaw/.openclaw/workspace/scripts/analyze_vector_search.js [logfile]
 * Default logfile: /home/openclaw/.openclaw/workspace/logs/vector_search_usage.jsonl
 */

const fs = require('fs');
const path = require('path');

const logPath = process.argv[2] || '/home/openclaw/.openclaw/workspace/logs/vector_search_usage.jsonl';

if (!fs.existsSync(logPath)) {
  console.log(JSON.stringify({ error: 'No logfile found', path: logPath }));
  process.exit(1);
}

const lines = fs.readFileSync(logPath, 'utf8').trim().split('\n');
const entries = [];
let malformed = 0;

for (const line of lines) {
  try {
    const obj = JSON.parse(line);
    entries.push(obj);
  } catch {
    malformed++;
  }
}

if (entries.length === 0) {
  console.log(JSON.stringify({ error: 'No valid log entries', malformed }));
  process.exit(1);
}

// Sort by timestamp
entries.sort((a, b) => new Date(a.ts) - new Date(b.ts));

const first = entries[0].ts;
const last = entries[entries.length - 1].ts;

// Metrics
const total = entries.length;
const hits = entries.filter(e => e.results > 0).length;
const hitRate = hits / total;
const scores = entries.filter(e => e.max_score != null).map(e => e.max_score);
const avgScore = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
const durations = entries.filter(e => e.duration_ms != null).map(e => e.duration_ms);
const avgDuration = durations.length ? durations.reduce((a, b) => a + b, 0) / durations.length : null;

const report = {
  generated_at: new Date().toISOString(),
  logfile: logPath,
  entries_total: total,
  malformed_lines: malformed,
  period: { first, last },
  hit_rate: round3(hitRate),
  avg_max_score: avgScore != null ? round3(avgScore) : null,
  avg_duration_ms: avgDuration != null ? Math.round(avgDuration) : null,
  by_scope: {},
};

for (const scope of ['memory', 'docs', 'all']) {
  const subset = entries.filter(e => e.scope === scope);
  if (subset.length) {
    const subHits = subset.filter(e => e.results > 0).length;
    report.by_scope[scope] = {
      queries: subset.length,
      hit_rate: round3(subHits / subset.length),
      avg_score: round3(subset.filter(e => e.max_score != null).reduce((sum, e) => sum + e.max_score, 0) / subset.filter(e => e.max_score != null).length),
    };
  }
}

function round3(num) {
  return typeof num === 'number' ? Math.round(num * 1000) / 1000 : num;
}

console.log(JSON.stringify(report, null, 2));