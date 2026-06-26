#!/usr/bin/env node
/**
 * setup-check.js — Pre-flight Configuration Validator
 *
 * Run this before launching the agent for the first time:
 *   node src/setup-check.js
 *
 * Checks:
 *   1. All required env vars are present and properly formatted
 *   2. API connectivity: Hyperliquid, CoinGecko, Midgard, THORNode
 *   3. Hyperliquid account: key derivation matches wallet address, balance readable
 *   4. Optional: Ollama reachability if configured
 *
 * Exit codes:
 *   0 = all checks pass (or pass with warnings)
 *   1 = one or more FAIL checks — fix before running
 */

'use strict';

require('dotenv').config();

const https = require('https');

// ── Result tracking ───────────────────────────────────────────────────────────

const _results = [];

function _pass(name, detail) {
  _results.push({ status: 'PASS', name, detail });
  console.log(`  \u2713 ${name}: ${detail}`);
}

function _fail(name, detail) {
  _results.push({ status: 'FAIL', name, detail });
  console.log(`  \u2717 ${name}: ${detail}`);
}

function _warn(name, detail) {
  _results.push({ status: 'WARN', name, detail });
  console.log(`  \u26a0 ${name}: ${detail}`);
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────

function _httpGet(url, timeoutMs = 8000) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': 'HL-TradingAgent/2.0' } }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        if (res.statusCode >= 400) { reject(new Error(`HTTP ${res.statusCode}`)); return; }
        try { resolve(JSON.parse(raw)); } catch (_) { resolve(raw); }
      });
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); reject(new Error('Timeout')); });
    req.on('error', reject);
  });
}

function _httpPost(url, body, extraHeaders = {}, timeoutMs = 8000) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const u       = new URL(url);
    const req     = https.request({
      hostname: u.hostname,
      path:     u.pathname,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
        ...extraHeaders,
      },
    }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        if (res.statusCode >= 400) { reject(new Error(`HTTP ${res.statusCode}`)); return; }
        try { resolve(JSON.parse(raw)); } catch (_) { resolve(raw); }
      });
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); reject(new Error('Timeout')); });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// ── Check: Environment Variables ──────────────────────────────────────────────

async function _checkEnvVars() {
  console.log('\n\u2500\u2500 Environment Variables \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500');

  const required = [
    'HYPERLIQUID_PRIVATE_KEY',
    'HYPERLIQUID_WALLET_ADDRESS',
    'MAX_POSITION_SIZE_USD',
    'MAX_OPEN_POSITIONS',
    'MAX_ACCOUNT_RISK_PCT',
    'KELLY_FRACTION',
    'CRON_INTERVAL_MINUTES',
  ];

  for (const key of required) {
    if (process.env[key]) _pass(key, 'set');
    else _fail(key, 'MISSING \u2014 required');
  }

  // Private key format check
  const pk = process.env.HYPERLIQUID_PRIVATE_KEY;
  if (pk) {
    if (/^0x[0-9a-fA-F]{64}$/.test(pk)) _pass('PRIVATE_KEY format', 'valid 0x + 64 hex chars');
    else _fail('PRIVATE_KEY format', 'must be 0x-prefixed 64-character hex string (32 bytes)');
  }

  // Wallet address format
  const addr = process.env.HYPERLIQUID_WALLET_ADDRESS;
  if (addr) {
    if (/^0x[0-9a-fA-F]{40}$/.test(addr)) _pass('WALLET_ADDRESS format', 'valid EVM address');
    else _fail('WALLET_ADDRESS format', 'must be 0x-prefixed 40-character hex string');
  }

  // Numeric sanity checks
  const numerics = { MAX_POSITION_SIZE_USD: [1, 100_000], MAX_OPEN_POSITIONS: [1, 50], MAX_ACCOUNT_RISK_PCT: [0.1, 20], KELLY_FRACTION: [0.01, 1], CRON_INTERVAL_MINUTES: [1, 1440] };
  for (const [key, [min, max]] of Object.entries(numerics)) {
    const val = parseFloat(process.env[key]);
    if (isNaN(val)) {
      if (process.env[key]) _fail(`${key} value`, `"${process.env[key]}" is not a number`);
    } else if (val < min || val > max) {
      _warn(`${key} value`, `${val} is outside expected range [${min}, ${max}]`);
    }
  }

  const kf = parseFloat(process.env.KELLY_FRACTION);
  if (kf > 0.5) _warn('KELLY_FRACTION', `${kf} is aggressive — recommend 0.25 or lower`);

  // Decision layer
  if (process.env.OLLAMA_URL) {
    _pass('OLLAMA_URL', process.env.OLLAMA_URL);
    if (!process.env.OLLAMA_MODEL) _warn('OLLAMA_MODEL', 'not set — will use qwen3.5:35b');
  } else if (process.env.OPENAI_API_KEY) {
    _pass('OPENAI_API_KEY', 'set \u2014 will use OpenAI as decision layer');
  } else {
    _warn('Decision layer', 'no LLM configured \u2014 using rule-based fallback (confidence \u2265 0.7 = trade)');
  }

  // Profit sweep
  if (process.env.PROFIT_SWEEP_ENABLED === 'true') {
    if (process.env.PROFIT_SWEEP_ADDRESS) _pass('PROFIT_SWEEP_ADDRESS', 'set');
    else _fail('PROFIT_SWEEP_ADDRESS', 'profit sweep enabled but address not set');
  }
}

// ── Check: API Connectivity ───────────────────────────────────────────────────

async function _checkConnectivity() {
  console.log('\n\u2500\u2500 API Connectivity \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500');

  // Hyperliquid
  try {
    const data = await _httpPost('https://api.hyperliquid.xyz/info', { type: 'allMids' });
    const n    = Object.keys(data || {}).length;
    _pass('Hyperliquid API', `reachable \u2014 ${n} markets live`);
  } catch (err) { _fail('Hyperliquid API', `unreachable: ${err.message}`); }

  // CoinGecko
  try {
    const data = await _httpGet('https://api.coingecko.com/api/v3/simple/price?ids=thorchain&vs_currencies=usd');
    const price = data?.thorchain?.usd;
    _pass('CoinGecko API', price ? `reachable \u2014 RUNE $${price}` : 'reachable');
  } catch (err) { _fail('CoinGecko API', `unreachable: ${err.message}`); }

  // Midgard
  try {
    const data  = await _httpGet('https://midgard.ninerealms.com/v2/stats');
    const rune  = parseFloat(data?.runePriceUSD || 0);
    _pass('Midgard API', rune ? `reachable \u2014 RUNE $${rune.toFixed(4)} USD` : 'reachable');
  } catch (err) { _fail('Midgard API', `unreachable: ${err.message}`); }

  // THORNode (optional)
  try {
    await _httpGet('https://thornode.ninerealms.com/thorchain/network');
    _pass('THORNode API', 'reachable');
  } catch (err) { _warn('THORNode API', `unreachable: ${err.message} (optional)`); }

  // Ollama (if configured)
  if (process.env.OLLAMA_URL) {
    try {
      const url = process.env.OLLAMA_URL.replace(/\/$/, '') + '/api/version';
      await _httpGet(url.replace('https://', 'http://').startsWith('http') ? url : 'http://' + url, 5000);
      _pass('Ollama', `reachable at ${process.env.OLLAMA_URL}`);
    } catch (err) { _fail('Ollama', `unreachable at ${process.env.OLLAMA_URL}: ${err.message}`); }
  }
}

// ── Check: Hyperliquid Account ────────────────────────────────────────────────

async function _checkAccount() {
  console.log('\n\u2500\u2500 Hyperliquid Account \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500');

  const pk   = process.env.HYPERLIQUID_PRIVATE_KEY;
  const addr = process.env.HYPERLIQUID_WALLET_ADDRESS;

  if (!pk || !addr) {
    _warn('Account check', 'skipped \u2014 PRIVATE_KEY or WALLET_ADDRESS not set');
    return;
  }

  // Validate key → address derivation using ethers
  try {
    const { Wallet } = require('ethers');
    const wallet = new Wallet(pk);
    if (wallet.address.toLowerCase() === addr.toLowerCase()) {
      _pass('Key \u2192 address match', `${wallet.address}`);
    } else {
      _fail('Key \u2192 address match', `key derives ${wallet.address} but WALLET_ADDRESS is ${addr}`);
    }
  } catch (err) {
    if (err.code === 'MODULE_NOT_FOUND') {
      _warn('Key validation', 'ethers not installed \u2014 run: npm install ethers @msgpack/msgpack');
    } else {
      _fail('Key validation', err.message);
    }
  }

  // Fetch live balance
  try {
    const data    = await _httpPost('https://api.hyperliquid.xyz/info', { type: 'clearinghouseState', user: addr });
    const balance = parseFloat(data?.marginSummary?.accountValue || 0);
    _pass('Account balance', `$${balance.toFixed(2)} USDC`);

    const maxPos = parseFloat(process.env.MAX_POSITION_SIZE_USD || 500);
    if (balance < maxPos) {
      _warn('Balance vs MAX_POSITION_SIZE_USD', `balance $${balance.toFixed(2)} < max position $${maxPos} \u2014 fund your account or lower MAX_POSITION_SIZE_USD`);
    }
  } catch (err) {
    _fail('Account balance fetch', err.message);
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  console.log('\n\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557');
  console.log('\u2551  HL Trading Agent \u2014 Setup Check                    \u2551');
  console.log('\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d');

  await _checkEnvVars();
  await _checkConnectivity();
  await _checkAccount();

  const fails  = _results.filter((r) => r.status === 'FAIL');
  const warns  = _results.filter((r) => r.status === 'WARN');
  const passes = _results.filter((r) => r.status === 'PASS');

  console.log('\n\u2500\u2500 Summary \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500');
  console.log(`  PASS: ${passes.length}   WARN: ${warns.length}   FAIL: ${fails.length}`);

  if (fails.length > 0) {
    console.log('\nFailed checks — fix these before running the agent:');
    fails.forEach((f) => console.log(`  \u2717 ${f.name}: ${f.detail}`));
    console.log('');
    process.exit(1);
  }

  if (warns.length > 0) {
    console.log('\nSetup is functional. Review warnings above before going live.\n');
  } else {
    console.log('\nAll checks passed. You are ready to trade.\n');
  }

  process.exit(0);
}

main().catch((err) => {
  console.error('Setup check crashed:', err.message);
  process.exit(1);
});
