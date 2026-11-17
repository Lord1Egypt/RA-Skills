'use strict';

const fs = require('fs');
const path = require('path');

function analyze(configPath) {
  const raw = fs.readFileSync(configPath, 'utf8');
  let config;
  try { config = JSON.parse(raw); } catch (e) { console.error('Invalid JSON'); process.exit(1); }

  const issues = [];
  if (!config.retries && config.retries !== 0) issues.push('missing retries');
  if (config.retries > 10) issues.push('retries too high: ' + config.retries);
  if (!config.initialDelayMs && config.initialDelayMs !== 0) issues.push('missing initialDelayMs');
  if (!config.maxDelayMs && config.maxDelayMs !== 0) issues.push('missing maxDelayMs');
  if (config.backoffFactor === undefined) issues.push('missing backoffFactor');
  if (config.jitterMs === undefined) issues.push('missing jitterMs');
  if (!config.timeoutMs && config.timeoutMs !== 0) issues.push('missing timeoutMs');
  if (!config.retryOn || !Array.isArray(config.retryOn) || config.retryOn.length === 0) issues.push('missing retryOn');
  if (!config.abortOn || !Array.isArray(config.abortOn)) issues.push('missing abortOn');

  console.log(JSON.stringify({ issues, optimized: issues.length === 0, config }, null, 2));
}

function generate(configPath) {
  const raw = fs.readFileSync(configPath, 'utf8');
  let config;
  try { config = JSON.parse(raw); } catch (e) { console.error('Invalid JSON'); process.exit(1); }

  const optimized = Object.assign({
    retries: config.retries || 3,
    initialDelayMs: config.initialDelayMs || 1000,
    maxDelayMs: config.maxDelayMs || 30000,
    backoffFactor: config.backoffFactor || 2,
    jitterMs: config.jitterMs || 500,
    timeoutMs: config.timeoutMs || 5000,
    retryOn: config.retryOn && config.retryOn.length ? config.retryOn : ['ECONNRESET', 'ETIMEDOUT', '5xx'],
    abortOn: config.abortOn && config.abortOn.length ? config.abortOn : ['4xx', 'auth_failed']
  }, config);

  console.log(JSON.stringify(optimized, null, 2));
}

function validate(configPath) {
  const raw = fs.readFileSync(configPath, 'utf8');
  let config;
  try { config = JSON.parse(raw); } catch (e) { console.error('Invalid JSON'); process.exit(1); }

  const errors = [];
  if (typeof config.retries !== 'number' || config.retries < 0) errors.push('retries must be a non-negative number');
  if (typeof config.initialDelayMs !== 'number' || config.initialDelayMs < 0) errors.push('initialDelayMs must be a non-negative number');
  if (typeof config.maxDelayMs !== 'number' || config.maxDelayMs < 0) errors.push('maxDelayMs must be a non-negative number');
  if (typeof config.backoffFactor !== 'number' || config.backoffFactor <= 1) errors.push('backoffFactor must be > 1');
  if (typeof config.jitterMs !== 'number' || config.jitterMs < 0) errors.push('jitterMs must be a non-negative number');
  if (typeof config.timeoutMs !== 'number' || config.timeoutMs <= 0) errors.push('timeoutMs must be > 0');
  if (!Array.isArray(config.retryOn) || config.retryOn.length === 0) errors.push('retryOn must be a non-empty array');
  if (!Array.isArray(config.abortOn)) errors.push('abortOn must be an array');

  console.log(JSON.stringify({ valid: errors.length === 0, errors }, null, 2));
  if (errors.length > 0) process.exit(1);
}

if (require.main === module) {
  const cmd = process.argv[2];
  if (cmd === 'analyze') {
    analyze(process.argv[3]);
  } else if (cmd === 'generate') {
    generate(process.argv[3]);
  } else if (cmd === 'validate') {
    validate(process.argv[3]);
  } else {
    console.error('Usage: node optimize.js <analyze|generate|validate> <config.json>');
    process.exit(1);
  }
}
