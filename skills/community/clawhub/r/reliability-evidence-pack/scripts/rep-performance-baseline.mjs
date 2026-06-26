#!/usr/bin/env node
/**
 * REP Performance Baseline - Generate performance_baseline artifacts
 * 
 * Usage:
 *   node rep-performance-baseline.mjs --metric-name <name> --baseline-value <num> --current-value <num> [--threshold <pct>]
 * 
 * Example:
 *   node rep-performance-baseline.mjs --metric-name response_time_ms --baseline-value 150 --current-value 120
 * 
 * Calculates trend: improving (current < baseline), degrading (current > baseline), stable (within threshold)
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuration
const DEFAULT_BUNDLE = path.join(__dirname, '..', 'rep-bundle', 'artifacts');
const DEFAULT_OUTPUT = path.join(DEFAULT_BUNDLE, 'performance_baseline.jsonl');
const DEFAULT_THRESHOLD = 5; // 5% threshold for stable

// Parse args
const args = process.argv.slice(2);
const opts = {
  metricName: null,
  baselineValue: null,
  currentValue: null,
  threshold: DEFAULT_THRESHOLD,
  output: null,
  bundle: null
};

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--metric-name' || arg === '-m') {
    opts.metricName = args[++i];
  } else if (arg === '--baseline-value' || arg === '-b') {
    opts.baselineValue = parseFloat(args[++i]);
  } else if (arg === '--current-value' || arg === '-c') {
    opts.currentValue = parseFloat(args[++i]);
  } else if (arg === '--threshold' || arg === '-t') {
    opts.threshold = parseFloat(args[++i]);
  } else if (arg === '--output' || arg === '-o') {
    opts.output = args[++i];
  } else if (arg === '--bundle' || arg === '-B') {
    opts.bundle = args[++i];
  } else if (arg === '--help' || arg === '-h') {
    console.log(`REP Performance Baseline

Usage:
  node rep-performance-baseline.mjs [options]

Options:
  -m, --metric-name <name>    Metric name (e.g., response_time_ms, token_usage, api_latency) [required]
  -b, --baseline-value <num>  Baseline value [required]
  -c, --current-value <num>  Current measured value [required]
  -t, --threshold <pct>      Threshold percentage for stable (default: 5)
  -o, --output <path>        Output file (default: rep-bundle/artifacts/performance_baseline.jsonl)
  -B, --bundle <dir>         Bundle directory (infers output path)
  -h, --help                 Show this help

Environment:
  REP_BUNDLE_PATH            Override default bundle path

Examples:
  node rep-performance-baseline.mjs -m response_time_ms -b 150 -c 120
  node rep-performance-baseline.mjs -m token_usage -b 1000 -c 1100 -t 10
`);
    process.exit(0);
  }
}

// Validate required arguments
if (!opts.metricName) {
  console.error('Error: --metric-name is required');
  process.exit(1);
}
if (opts.baselineValue === null || isNaN(opts.baselineValue)) {
  console.error('Error: --baseline-value is required and must be a number');
  process.exit(1);
}
if (opts.currentValue === null || isNaN(opts.currentValue)) {
  console.error('Error: --current-value is required and must be a number');
  process.exit(1);
}

// Calculate trend
function calculateTrend(baseline, current, thresholdPct) {
  if (baseline === 0) {
    return current === 0 ? 'stable' : 'degrading';
  }
  
  const pctChange = ((current - baseline) / baseline) * 100;
  const threshold = thresholdPct;
  
  if (Math.abs(pctChange) <= threshold) {
    return 'stable';
  } else if (pctChange < 0) {
    return 'improving';
  } else {
    return 'degrading';
  }
}

// Determine output path
let outputPath = opts.output;
if (!outputPath) {
  const bundlePath = opts.bundle || process.env.REP_BUNDLE_PATH || DEFAULT_BUNDLE;
  outputPath = path.join(bundlePath, 'performance_baseline.jsonl');
}

// Ensure directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Get existing artifact count for sequence
function getNextSequence(filePath) {
  if (!fs.existsSync(filePath)) return 1;
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n').filter(Boolean);
  if (lines.length === 0) return 1;
  
  // Find max sequence
  let maxSeq = 0;
  for (const line of lines) {
    try {
      const artifact = JSON.parse(line);
      if (artifact.baseline_seq && artifact.baseline_seq > maxSeq) {
        maxSeq = artifact.baseline_seq;
      }
    } catch (e) {}
  }
  return maxSeq + 1;
}

// Generate artifact
function generateBaseline(metricName, baselineValue, currentValue, threshold, seq) {
  const trend = calculateTrend(baselineValue, currentValue, threshold);
  const pctChange = baselineValue !== 0 
    ? ((currentValue - baselineValue) / baselineValue) * 100 
    : (currentValue === 0 ? 0 : 100);
  
  const artifact = {
    rep_version: '0.3',
    artifact_type: 'performance_baseline',
    artifact_id: `perf-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    session_id: process.env.OPENCLAW_SESSION_ID || 'system-cron',
    interaction_id: null,
    created_at: new Date().toISOString(),
    actor: {
      id: 'agent:christine',
      role: 'agent'
    },
    content_hash: '',
    prev_hash: null,
    
    // Baseline-specific fields
    metric_name: metricName,
    baseline_value: baselineValue,
    current_value: currentValue,
    threshold_pct: threshold,
    trend: trend,
    pct_change: Math.round(pctChange * 100) / 100,
    baseline_seq: seq,
    
    // Additional metadata
    node: process.env.HOSTNAME || 'unknown',
    pid: process.pid
  };
  
  // Compute content hash
  const canonical = JSON.stringify(artifact, Object.keys(artifact).sort());
  const hash = crypto.createHash('sha256').update(canonical).digest('hex');
  artifact.content_hash = `sha256:${hash.slice(0, 64)}`;
  
  return artifact;
}

// Main execution
const seq = getNextSequence(outputPath);
const artifact = generateBaseline(
  opts.metricName,
  opts.baselineValue,
  opts.currentValue,
  opts.threshold,
  seq
);

// Append to file
fs.appendFileSync(outputPath, JSON.stringify(artifact) + '\n');

console.log(`✓ Emitted performance baseline #${seq} to ${outputPath}`);
console.log(`  artifact_id: ${artifact.artifact_id}`);
console.log(`  metric: ${artifact.metric_name}`);
console.log(`  baseline: ${artifact.baseline_value} → current: ${artifact.current_value}`);
console.log(`  trend: ${artifact.trend} (${artifact.pct_change}%)`);
