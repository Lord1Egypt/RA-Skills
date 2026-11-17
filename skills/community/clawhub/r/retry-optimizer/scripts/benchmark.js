'use strict';

/**
 * Benchmark: fixed-interval retry vs exponential backoff + jitter
 *
 * Usage:
 *   node skills/retry-optimizer/scripts/benchmark.js
 *   node skills/retry-optimizer/scripts/benchmark.js --scenarios=3 --attempts=5
 */

const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { scenarios: 3, attempts: 5, seed: Date.now() };
  for (const arg of args) {
    if (arg.startsWith('--scenarios=')) opts.scenarios = Number(arg.split('=')[1]);
    else if (arg.startsWith('--attempts=')) opts.attempts = Number(arg.split('=')[1]);
    else if (arg.startsWith('--seed=')) opts.seed = Number(arg.split('=')[1]);
  }
  return opts;
}

function jitter(ms, seed) {
  // Simple pseudo-random jitter in range [0, ms]
  const x = Math.sin(seed++) * 10000;
  const r = x - Math.floor(x);
  return Math.floor(r * ms);
}

function simulateFixed(retries, fixedDelayMs) {
  const timeline = [];
  let totalWait = 0;
  for (let i = 0; i < retries; i++) {
    timeline.push({ attempt: i + 1, waitMs: fixedDelayMs, cumulative: totalWait + fixedDelayMs });
    totalWait += fixedDelayMs;
  }
  return { timeline, totalWait, attempts: retries };
}

function simulateBackoff(config, seed) {
  const timeline = [];
  let totalWait = 0;
  let delay = config.initialDelayMs;
  for (let i = 0; i < config.retries; i++) {
    const wait = Math.min(delay + jitter(config.jitterMs, seed++), config.maxDelayMs);
    timeline.push({ attempt: i + 1, waitMs: wait, cumulative: totalWait + wait });
    totalWait += wait;
    delay = delay * (config.backoffFactor || 2);
  }
  return { timeline, totalWait, attempts: config.retries };
}

function printComparison(label, fixed, backoff) {
  const improvement = ((fixed.totalWait - backoff.totalWait) / fixed.totalWait) * 100;
  console.log(`\n=== ${label} ===`);
  console.log(`Fixed interval:   ${fixed.totalWait}ms total (${fixed.attempts} attempts)`);
  console.log(`Backoff + jitter: ${backoff.totalWait}ms total (${backoff.attempts} attempts)`);
  console.log(`Improvement:      ${improvement.toFixed(1)}% faster`);

  console.log('\nTimeline comparison:');
  console.log('Attempt | Fixed Wait | Backoff Wait');
  console.log('--------|------------|-------------');
  const maxLen = Math.max(fixed.timeline.length, backoff.timeline.length);
  for (let i = 0; i < maxLen; i++) {
    const f = fixed.timeline[i] || { waitMs: '-', cumulative: '-' };
    const b = backoff.timeline[i] || { waitMs: '-', cumulative: '-' };
    console.log(`  ${(i + 1).toString().padStart(2)}    | ${String(f.waitMs).padStart(10)} | ${String(b.waitMs).padStart(11)}`);
  }
}

function main() {
  const opts = parseArgs();
  console.log('Retry Optimizer Benchmark');
  console.log(`Scenarios: ${opts.scenarios}, Attempts: ${opts.attempts}, Seed: ${opts.seed}`);

  const configs = [
    { name: '30s fixed → optimized', fixed: 30000, backoff: { retries: opts.attempts, initialDelayMs: 1000, maxDelayMs: 30000, backoffFactor: 2, jitterMs: 500 } },
    { name: '60s fixed → optimized', fixed: 60000, backoff: { retries: opts.attempts, initialDelayMs: 1000, maxDelayMs: 60000, backoffFactor: 2, jitterMs: 500 } },
    { name: '10s fixed → optimized', fixed: 10000, backoff: { retries: opts.attempts, initialDelayMs: 500, maxDelayMs: 10000, backoffFactor: 2, jitterMs: 250 } }
  ];

  for (let i = 0; i < Math.min(opts.scenarios, configs.length); i++) {
    const cfg = configs[i];
    const fixed = simulateFixed(opts.attempts, cfg.fixed);
    const backoff = simulateBackoff(cfg.backoff, opts.seed + i);
    printComparison(cfg.name, fixed, backoff);
  }

  console.log('\nNote: This is a simulation. Real-world improvement may vary based on error rates and network conditions.');
}

main();
