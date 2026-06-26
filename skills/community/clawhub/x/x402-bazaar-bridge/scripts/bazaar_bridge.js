#!/usr/bin/env node
// sig: conan-x402-bridge-v1 | forged in fire, signed in blood 🥩
/**
 * bazaar_bridge.mjs — x402 Bazaar Bridge Core Engine
 *
 * Discover, pay, and fetch data from x402-enabled APIs on the Coinbase Bazaar.
 *
 * ⚠️ SECURITY WARNING ⚠️
 * This script requires a PRIVATE KEY (WALLET_KEY) to sign payments.
 * - NEVER commit .env to git
 * - Keep your .env file permissions at 0600 (owner read-only)
 * - The private key stays on YOUR machine — never leaves it
 * - Error messages intentionally hide wallet addresses and keys
 *
 * Usage:
 *   node bazaar_bridge.mjs search "bitcoin fee rates"
 *   node bazaar_bridge.mjs fetch https://btcnode.uk/api/fees
 *   node bazaar_bridge.mjs resolve "bitcoin fee rates"
 *   node bazaar_bridge.mjs budget
 *
 * Env (set via .env or environment):
 *   WALLET_KEY       - Private key (0x hex). WITHOUT THIS = read-only mode
 *   WALLET_ADDRESS   - Wallet address (for display only, derived from key if omitted)
 *   DAILY_BUDGET_USD - Max daily spend (default: 1.00)
 */

import { existsSync, readFileSync, writeFileSync, appendFileSync, mkdirSync, chmodSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = resolve(__dirname, '..');
const LOG_DIR = resolve(SKILL_DIR, 'logs');
mkdirSync(LOG_DIR, { recursive: true });

// Secure file permissions — 0o600 = owner read/write only
// (macOS default umask often makes files 0644, world-readable)
try { chmodSync(LOG_DIR, 0o700); } catch {}

const CACHE_FILE = resolve(LOG_DIR, 'bazaar_cache.json');
const BUDGET_FILE = resolve(LOG_DIR, 'bazaar_budget.json');
const LOG_FILE = resolve(LOG_DIR, 'bazaar_bridge.log');
const DISCOVERY_API = 'https://api.cdp.coinbase.com/platform/v2/x402/discovery';
const REQUEST_TIMEOUT = 15_000; // 15s fetch timeout

// ─── Secure File Helpers ───────────────────────────────────

function secureWrite(path, data) {
  try {
    writeFileSync(path, data, { mode: 0o600, encoding: 'utf-8' });
  } catch (err) {
    log(`Write error ${path}: ${err.message}`);
  }
}

function secureRead(path) {
  try {
    return readFileSync(path, 'utf-8');
  } catch {
    return null;
  }
}

// ─── Logging ────────────────────────────────────────────────

function log(...args) {
  const ts = new Date().toISOString();
  const msg = `[${ts}] ${args.join(' ')}`;
  try { appendFileSync(LOG_FILE, msg + '\n', { mode: 0o600, encoding: 'utf-8' }); } catch {}
  // stderr for agent diagnostic visibility
  console.error('[bridge]', ...args);
}

// ─── Input Validation ──────────────────────────────────────

/**
 * Validates a URL is safe to fetch via x402.
 * Rejects: file://, ftp://, internal IPs, localhost, empty URLs
 */
function validateUrl(raw) {
  if (!raw || typeof raw !== 'string') return { ok: false, error: 'URL is required' };
  const trimmed = raw.trim();
  if (trimmed.length < 4 || trimmed.length > 2048) return { ok: false, error: 'Invalid URL length' };

  let parsed;
  try { parsed = new URL(trimmed); } catch { return { ok: false, error: 'Malformed URL' }; }

  // Only allow https
  if (parsed.protocol !== 'https:') return { ok: false, error: 'Only https:// URLs are allowed' };

  // Block internal/reserved IPs
  const hostname = parsed.hostname.toLowerCase();
  if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '0.0.0.0' ||
      hostname === '[::1]' || hostname.endsWith('.local') || hostname.endsWith('.internal')) {
    return { ok: false, error: 'Internal/host-local URLs are not allowed' };
  }
  // Block private IP ranges (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
  const ipMatch = hostname.match(/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/);
  if (ipMatch) {
    const [_, a, b] = ipMatch.map(Number);
    if (a === 10 || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168)) {
      return { ok: false, error: 'Private IP ranges are not allowed' };
    }
  }

  // Block link-local/multicast (169.254.x.x, 224-239.x.x.x)
  if (ipMatch) {
    const a = Number(ipMatch[1]);
    if (a === 169 || (a >= 224 && a <= 239)) {
      return { ok: false, error: 'Link-local and multicast IPs are not allowed' };
    }
  }

  return { ok: true, url: trimmed };
}

function validateQuery(query) {
  if (!query || typeof query !== 'string') return { ok: false, error: 'Query is required' };
  const trimmed = query.trim();
  if (trimmed.length < 1) return { ok: false, error: 'Query cannot be empty' };
  if (trimmed.length > 200) return { ok: false, error: 'Query too long (max 200 chars)' };
  return { ok: true, query: trimmed };
}

// ─── .env Security Warning ────────────────────────────────


// ─── Config ─────────────────────────────────────────────────

function loadEnv() {
  const envPath = resolve(SKILL_DIR, '.env');
  if (existsSync(envPath)) {
    const content = secureRead(envPath);
    if (content) {
      for (const line of content.split('\n')) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#') || !trimmed.includes('=')) continue;
        const eq = trimmed.indexOf('=');
        const key = trimmed.slice(0, eq).trim();
        const val = trimmed.slice(eq + 1).trim();
        // Only set if not already in environment (env vars take priority)
        if (!process.env[key]) process.env[key] = val;
      }
    }
  }

  const rawKey = process.env.WALLET_KEY || null;
  const rawAddress = process.env.WALLET_ADDRESS || null;

  return {
    // Store only a boolean + truncated fingerprint for identification
    walletConfigured: !!rawKey,
    walletKey: rawKey, // Used for signing, never returned in output
    walletAddress: rawAddress,
    dailyBudget: Math.max(0.01, parseFloat(process.env.DAILY_BUDGET_USD || '1.00')),
  };
}

// ─── ClawHub Install Check ────────────────────────────────


// ─── Cache ──────────────────────────────────────────────────

const CACHE_TTL = {
  search: 60_000,    // 1 min — Bazaar changes fast
  fetch: 300_000,    // 5 min — most data is semi-stale
};

function loadCache() {
  if (!existsSync(CACHE_FILE)) return {};
  try {
    return JSON.parse(secureRead(CACHE_FILE) || '{}');
  } catch {
    // Corrupted cache — start fresh
    secureWrite(CACHE_FILE, '{}');
    return {};
  }
}

function saveCache(cache) {
  secureWrite(CACHE_FILE, JSON.stringify(cache));
}

function getCached(key) {
  const cache = loadCache();
  const entry = cache[key];
  if (!entry) return null;
  if (Date.now() - entry.ts > entry.ttl) {
    delete cache[key];
    saveCache(cache);
    return null;
  }
  return entry.data;
}

function setCache(key, data, ttl) {
  const cache = loadCache();
  cache[key] = { ts: Date.now(), ttl, data };
  // Prune expired entries silently
  const now = Date.now();
  for (const k of Object.keys(cache)) {
    if (cache[k].ts + cache[k].ttl < now) delete cache[k];
  }
  // Hard cap on cache size (1000 entries max)
  const keys = Object.keys(cache);
  if (keys.length > 1000) {
    const sorted = keys.sort((a, b) => cache[a].ts - cache[b].ts);
    for (let i = 0; i < sorted.length - 800; i++) delete cache[sorted[i]];
  }
  saveCache(cache);
}

// ─── Budget & Rate Limits ──────────────────────────────────

function loadBudget() {
  if (!existsSync(BUDGET_FILE)) {
    return { date: today(), spent: 0, calls: 0, rejected: 0 };
  }
  try {
    const raw = secureRead(BUDGET_FILE);
    if (!raw) return { date: today(), spent: 0, calls: 0, rejected: 0 };
    const b = JSON.parse(raw);
    if (b.date !== today()) return { date: today(), spent: 0, calls: 0, rejected: 0 };
    return { ...{ date: today(), spent: 0, calls: 0, rejected: 0 }, ...b };
  } catch {
    return { date: today(), spent: 0, calls: 0, rejected: 0 };
  }
}

function today() {
  return new Date().toISOString().split('T')[0];
}

function saveBudget(b) {
  secureWrite(BUDGET_FILE, JSON.stringify(b));
}

function checkBudget(costUsd, config) {
  const budget = loadBudget();
  const wouldBe = budget.spent + costUsd;
  if (wouldBe > config.dailyBudget) {
    budget.rejected++;
    saveBudget(budget);
    return { allowed: false, budget };
  }
  return { allowed: true, budget };
}

function recordSpend(costUsd) {
  const budget = loadBudget();
  budget.spent += costUsd;
  budget.calls += 1;
  saveBudget(budget);
  log(`Spent $${costUsd.toFixed(4)} | Total today: $${budget.spent.toFixed(4)} (${budget.calls} calls)`);
}

// ─── Bazaar Discovery API ───────────────────────────────────

async function searchBazaar(query, limit = 10) {
  const queryVal = validateQuery(query);
  if (!queryVal.ok) return { ok: false, error: queryVal.error, resources: [] };

  const cacheKey = `search:${queryVal.query}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const safeLimit = Math.max(1, Math.min(50, limit || 10));
  const url = `${DISCOVERY_API}/search?query=${encodeURIComponent(queryVal.query)}&limit=${safeLimit}`;
  log(`Searching Bazaar: "${queryVal.query}"`);

  let res;
  try {
    res = await fetch(url, { signal: AbortSignal.timeout(REQUEST_TIMEOUT) });
  } catch (err) {
    return { ok: false, error: `Bazaar search unreachable: ${err.message}`, resources: [] };
  }

  if (res.status === 429) {
    return { ok: false, error: 'Bazaar rate limit hit. Try again in 30 seconds.', resources: [] };
  }
  if (!res.ok) {
    return { ok: false, error: `Bazaar search returned HTTP ${res.status}`, resources: [] };
  }

  let data;
  try {
    data = await res.json();
  } catch {
    return { ok: false, error: 'Bazaar returned invalid JSON', resources: [] };
  }

  if (!data || !Array.isArray(data.resources)) {
    return { ok: false, error: 'Unexpected Bazaar response format', resources: [] };
  }

  const resources = data.resources.map(r => ({
    url: r.resource || r.url || null,
    description: (r.description || '').slice(0, 200),
    price: parsePrice(r),
    mimeType: r.mimeType || 'application/json',
  })).filter(r => r.url !== null); // Skip entries without URLs

  const result = { ok: true, error: null, resources, query: queryVal.query };
  setCache(cacheKey, result, CACHE_TTL.search);
  return result;
}

function parsePrice(item) {
  try {
    const accepts = item.accepts || [];
    if (accepts.length > 0 && accepts[0].amount) {
      const amount = parseInt(accepts[0].amount, 10);
      if (!isNaN(amount) && amount > 0) return amount / 1_000_000;
    }
    if (item.price && typeof item.price === 'string') {
      const cleaned = parseFloat(item.price.replace('$', '').trim());
      if (!isNaN(cleaned)) return cleaned;
    }
  } catch {}
  return null;
}

// ─── x402 Payment & Fetch ───────────────────────────────────

async function fetchEndpoint(url, config) {
  // Validate URL first
  const urlVal = validateUrl(url);
  if (!urlVal.ok) return { ok: false, error: urlVal.error };

  const cacheKey = `fetch:${urlVal.url}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  log(`Fetching ${redactUrl(urlVal.url)}...`);

  // Step 1: Initial request
  let res;
  try {
    res = await fetch(urlVal.url, { signal: AbortSignal.timeout(REQUEST_TIMEOUT) });
  } catch (err) {
    return { ok: false, error: `Endpoint unreachable: ${err.message}` };
  }

  // Free/200 response
  if (res.status === 200) {
    const data = await safeParseJson(res);
    const result = { ok: true, data, paid: false };
    setCache(cacheKey, result, CACHE_TTL.fetch);
    return result;
  }

  // Not 402 = unexpected
  if (res.status !== 402) {
    return { ok: false, error: `Endpoint returned HTTP ${res.status} (expected 402 for payment)` };
  }

  // Step 2: Parse payment requirements
  const paymentRequired = parsePaymentRequired(res);
  if (!paymentRequired) {
    return { ok: false, error: 'Payment required but no payment metadata returned' };
  }

  // Find Base USDC option
  const baseOption = findBaseUsdcOption(paymentRequired.accepts);
  if (!baseOption) {
    return { ok: false, error: 'This endpoint does not support Base USDC payments' };
  }

  const cost = parsePriceFromAccepts(baseOption);
  if (cost === null) {
    return { ok: false, error: 'Could not determine payment amount' };
  }

  // Step 3: Budget check
  const budgetCheck = checkBudget(cost, config);
  if (!budgetCheck.allowed) {
    return { ok: false, error: `Daily budget $${config.dailyBudget.toFixed(2)} exceeded ($${budgetCheck.budget.spent.toFixed(4)} spent, need $${cost.toFixed(4)})` };
  }

  // Step 4: Read-only mode check
  if (!config.walletKey) {
    return {
      ok: false,
      error: 'Payment required — configure WALLET_KEY in .env to enable payments',
      readOnly: true,
      costUsd: cost,
    };
  }

  // Step 5: Execute payment
  try {
    const paidData = await executePayment(urlVal.url, paymentRequired, baseOption, config);
    recordSpend(cost);
    const result = { ok: true, data: paidData, paid: true, costUsd: cost };
    setCache(cacheKey, result, CACHE_TTL.fetch);
    return result;
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

function redactUrl(url) {
  try {
    const u = new URL(url);
    return `${u.protocol}//${u.hostname}${u.pathname.slice(0, 40)}${u.pathname.length > 40 ? '...' : ''}`;
  } catch { return '(invalid url)'; }
}

async function safeParseJson(res) {
  try {
    const text = await res.text();
    try { return JSON.parse(text); } catch { return text; }
  } catch { return null; }
}

function parsePaymentRequired(res) {
  try {
    const header = res.headers.get('payment-required') || res.headers.get('x-payment-required');
    if (!header) return null;

    // Try base64-decoded JSON first (standard), then raw JSON
    let parsed;
    try { parsed = JSON.parse(Buffer.from(header, 'base64').toString('utf-8')); }
    catch { try { parsed = JSON.parse(header); } catch { return null; } }

    return parsed;
  } catch { return null; }
}

function findBaseUsdcOption(accepts) {
  if (!Array.isArray(accepts)) return null;
  return accepts.find(a =>
    a &&
    typeof a === 'object' &&
    a.network === 'eip155:8453' &&
    a.amount &&
    String(a.amount) !== '0'
  ) || null;
}

function parsePriceFromAccepts(option) {
  try {
    const amount = parseInt(option.amount, 10);
    if (isNaN(amount) || amount <= 0) return null;
    return amount / 1_000_000;
  } catch { return null; }
}

async function executePayment(url, paymentRequired, acceptedOption, config) {
  // Dynamic imports — only loaded when actually paying
  let privateKeyToAccount, http, createWalletClient, base;
  try {
    const viemAccounts = await import('viem/accounts');
    privateKeyToAccount = viemAccounts.privateKeyToAccount;
    const viem = await import('viem');
    http = viem.http;
    createWalletClient = viem.createWalletClient;
    const chains = await import('viem/chains');
    base = chains.base;
  } catch (err) {
    throw new Error('viem SDK not installed. Run: npm install viem');
  }

  let account;
  try {
    account = privateKeyToAccount(config.walletKey);
  } catch (err) {
    throw new Error('Invalid WALLET_KEY — must be a valid 0x-prefixed hex private key');
  }

  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http('https://mainnet.base.org'),
  });

  const USDC_BASE = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
  const value = BigInt(acceptedOption.amount || '0');
  const validAfter = BigInt(Math.floor(Date.now() / 1000));
  const validBefore = validAfter + BigInt(acceptedOption.maxTimeoutSeconds || 300);

  // Secure random nonce
  const nonceBytes = new Uint8Array(32);
  crypto.getRandomValues(nonceBytes);
  const nonceHex = '0x' + Array.from(nonceBytes).map(b => b.toString(16).padStart(2, '0')).join('');

  log(`Signing payment...`);

  let signature;
  try {
    signature = await walletClient.signTypedData({
      domain: { name: 'USD Coin', version: '2', chainId: 8453, verifyingContract: USDC_BASE },
      types: {
        TransferWithAuthorization: [
          { name: 'from', type: 'address' }, { name: 'to', type: 'address' },
          { name: 'value', type: 'uint256' }, { name: 'validAfter', type: 'uint256' },
          { name: 'validBefore', type: 'uint256' }, { name: 'nonce', type: 'bytes32' },
        ],
      },
      message: {
        from: account.address,
        to: acceptedOption.payTo,
        value,
        validAfter,
        validBefore,
        nonce: nonceHex,
      },
      primaryType: 'TransferWithAuthorization',
    });
  } catch (err) {
    throw new Error(`Payment signing failed: ${err.message}`);
  }

  // Build v2 payment payload — DO NOT log this (contains signature)
  const paymentPayload = {
    x402Version: 2,
    accepted: acceptedOption,
    resource: paymentRequired.resource || { url },
    payload: {
      signature,
      authorization: {
        from: account.address,
        to: acceptedOption.payTo,
        value: value.toString(),
        validAfter: validAfter.toString(),
        validBefore: validBefore.toString(),
        nonce: nonceHex,
      },
    },
  };

  const encoded = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');

  // Retry request with payment proof
  let paidRes;
  try {
    paidRes = await fetch(url, {
      headers: { 'payment-signature': encoded },
      signal: AbortSignal.timeout(REQUEST_TIMEOUT),
    });
  } catch (err) {
    // Payment was signed and broadcast, but we couldn't verify the result
    // The settlement may have gone through — check your wallet
    throw new Error(`Payment sent but result unknown: ${err.message}. Check wallet for settlement.`);
  }

  if (paidRes.status === 200) {
    const data = await safeParseJson(paidRes);
    log('✅ Payment settled');
    return data;
  }

  if (paidRes.status === 402) {
    throw new Error('Payment rejected — insufficient USDC balance or invalid signature. Check wallet.');
  }

  const body = await paidRes.text().catch(() => '');
  throw new Error(`Endpoint returned HTTP ${paidRes.status} after payment`);
}

// ─── Resolve (search + cheapest + pay) ──────────────────────

async function resolveQuery(query, config) {
  const search = await searchBazaar(query);
  if (!search.ok) return { ok: false, error: search.error };
  if (search.resources.length === 0) {
    return { ok: false, error: `No matching x402 resources found` };
  }

  // Sort by price ascending (cheapest first), null prices last
  const sorted = [...search.resources].sort((a, b) => {
    if (a.price === null && b.price === null) return 0;
    if (a.price === null) return 1;
    if (b.price === null) return -1;
    return a.price - b.price;
  });

  const best = sorted[0];
  log(`Best match: ${redactUrl(best.url)} at $${best.price?.toFixed(3) || '?'}`);

  const result = await fetchEndpoint(best.url, config);
  return { ...result, resource: best };
}

// ─── Budget Report (no wallet info exposed) ────────────────

function budgetReport(config) {
  const budget = loadBudget();
  return {
    date: budget.date,
    spent: parseFloat(budget.spent.toFixed(4)),
    calls: budget.calls,
    rejected: budget.rejected,
    dailyLimit: config.dailyBudget,
    remaining: parseFloat(Math.max(0, config.dailyBudget - budget.spent).toFixed(4)),
    walletConfigured: config.walletConfigured,
  };
}

// ─── .gitignore Check ─────────────────────────────────────

function envCheck() {
  const envPath = resolve(SKILL_DIR, '.env');
  const gitignorePath = resolve(SKILL_DIR, '.gitignore');
  const skillGitignore = resolve(SKILL_DIR, '..', '.gitignore');

  if (existsSync(envPath)) {
    // Check if .env is gitignored
    const checkGit = (path) => {
      if (!existsSync(path)) return false;
      const content = secureRead(path) || '';
      return content.includes('.env') || content.includes('.env.example');
    };

    if (!checkGit(gitignorePath) && !checkGit(skillGitignore)) {
      log('⚠️ WARNING: .env file found but no .gitignore with .env entry.');
      log('   Run: echo \".env\" >> .gitignore');
    }
  }
}

// ─── Main ──────────────────────────────────────────────────

async function main() {
  const config = loadEnv();

  // Security checks on startup
  envCheck();

  const args = process.argv.slice(2);
  const command = args[0] || '';
  const isJsonOutput = command !== ''; // Always JSON for commands, pretty for help

  if (['--help', '-h', ''].includes(command)) {
    console.log(helpText(config));
    return;
  }

  let result;
  switch (command) {
    case 'search': {
      // Parse query: collect all non-flag args
      const flagIdx = args.findIndex(a => a.startsWith('--'));
      const queryParts = flagIdx === -1 ? args.slice(1) : args.slice(1, flagIdx);
      const limit = args.includes('--limit') ? Math.min(50, parseInt(args[args.indexOf('--limit') + 1], 10) || 10) : 10;
      if (queryParts.length === 0) { result = { ok: false, error: 'Usage: bazaar_bridge.mjs search \"<query>\"' }; break; }
      result = await searchBazaar(queryParts.join(' '), limit);
      break;
    }

    case 'fetch': {
      const url = args[1];
      if (!url) { result = { ok: false, error: 'Usage: bazaar_bridge.mjs fetch <https://...>' }; break; }
      result = await fetchEndpoint(url, config);
      break;
    }

    case 'resolve': {
      const flagIdx = args.findIndex(a => a.startsWith('--'));
      const queryParts = flagIdx === -1 ? args.slice(1) : args.slice(1, flagIdx);
      if (queryParts.length === 0) { result = { ok: false, error: 'Usage: bazaar_bridge.mjs resolve \"<query>\"' }; break; }
      result = await resolveQuery(queryParts.join(' '), config);
      break;
    }

    case 'budget': {
      result = budgetReport(config);
      break;
    }

    default:
      result = { ok: false, error: `Unknown command: "${command}". Use --help for usage.` };
  }

  console.log(JSON.stringify(result));
}

function helpText(config) {
  return JSON.stringify({
    usage: 'bazaar_bridge.mjs <command> [args]',
    commands: {
      search: 'node bazaar_bridge.mjs search "<query>" [--limit N]',
      fetch: 'node bazaar_bridge.mjs fetch <url>',
      resolve: 'node bazaar_bridge.mjs resolve "<query>"',
      budget: 'node bazaar_bridge.mjs budget',
    },
    wallet: config.walletConfigured ? '✅ Configured' : '❌ Read-only mode',
    dailyBudget: `$${config.dailyBudget.toFixed(2)}`,
    security: {
      urlValidation: 'Only https://, no localhost/private IPs',
      cachePermissions: '0600 (owner only)',
      keyExposure: 'Never logged or exposed in output',
    },
  }, null, 2);
}

main().catch(err => {
  log(`Fatal: ${err.message}`);
  console.log(JSON.stringify({ ok: false, error: 'Internal error' }));
  process.exit(0);
});
