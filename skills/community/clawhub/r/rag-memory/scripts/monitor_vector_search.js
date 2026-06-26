#!/usr/bin/env node
/**
 * monitor_vector_search.js — track performance over time
 *
 * 1. Runs the analyzer to generate today's report
 * 2. Saves it to logs/vector_search_reports/YYYY-MM-DD.json
 * 3. Prints a table of metrics for the last 7 days (or all available)
 *
 * Usage: node /home/openclaw/.openclaw/workspace/scripts/monitor_vector_search.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const analyzerPath = '/home/openclaw/.openclaw/skills/rag-memory/scripts/analyze_vector_search.js';
const usageLog = '/home/openclaw/.openclaw/workspace/logs/vector_search_usage.jsonl';
const reportsDir = '/home/openclaw/.openclaw/workspace/logs/vector_search_reports';

// Ensure reports dir exists
fs.mkdirSync(reportsDir, { recursive: true });

// 1. Run analyzer and capture output
let todayReport;
try {
  const raw = execSync(`node "${analyzerPath}" "${usageLog}"`, { encoding: 'utf8' });
  todayReport = JSON.parse(raw);
} catch (e) {
  console.error('Analyzer failed:', e.message);
  process.exit(1);
}

// 2. Save today's report
const today = new Date().toISOString().slice(0, 10);
const todayPath = path.join(reportsDir, `${today}.json`);
fs.writeFileSync(todayPath, JSON.stringify(todayReport, null, 2));
console.log(`Saved report: ${todayPath}`);

// 3. Load all reports (sorted by date)
const reports = [];
for (const file of fs.readdirSync(reportsDir)) {
  if (file.endsWith('.json')) {
    const date = file.slice(0, 10); // YYYY-MM-DD
    try {
      const content = JSON.parse(fs.readFileSync(path.join(reportsDir, file), 'utf8'));
      reports.push({ date, ...content });
    } catch (_) {}
  }
}
reports.sort((a, b) => a.date.localeCompare(b.date));

if (reports.length === 0) {
  console.log('No historical reports found.');
  process.exit(0);
}

// 4. Print table header
console.log('\n=== Performance History (last 7 days) ===');
console.log(
  'Date'.padEnd(12) +
  'Queries'.padEnd(10) +
  'Hit%'.padEnd(8) +
  'MaxScore'.padEnd(10) +
  'AvgDur(ms)'.padEnd(12)
);
console.log('-'.repeat(50));

// 5. Show last 7 (or all)
const recent = reports.slice(-7);
for (const r of recent) {
  const q = r.entries_total || 0;
  const hr = r.hit_rate != null ? `${Math.round(r.hit_rate * 100)}%` : 'N/A';
  const ms = r.avg_max_score != null ? r.avg_max_score.toFixed(3) : 'N/A';
  const dur = r.avg_duration_ms != null ? r.avg_duration_ms : 'N/A';
  console.log(
    r.date.padEnd(12) +
    q.toString().padEnd(10) +
    hr.padEnd(8) +
    ms.padEnd(10) +
    dur.toString().padEnd(12)
  );
}
console.log('\nFull history in:', reportsDir);