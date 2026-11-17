// providers/index.js
// Provider router. Picks the right provider based on command + flags.
//
// Default (no flag): Pool Mode A. Apple Pay per transaction. Parker's float.
// --wallet=cdp:     Path 1. Sign from user's CDP wallet.
// --wallet=privy:   Path 1. Sign from user's Privy wallet.

import { execSync } from 'node:child_process';
import mintAuthorize from './coinbase.js';

const WORKER_URL = 'https://pay-wip-computer.wipcomputer.workers.dev';

// Lazy imports ... only load what's needed
async function getX402() { return (await import('./x402.js')).default; }
async function getStripe() { return (await import('./stripe.js')).default; }
async function getPrivy() { return (await import('./privy.js')).default; }
async function getPool() { return await import('./passthrough.js'); }

function getWorkerSecret() {
  return execSync(
    'OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) ' +
    'op item get "wip-agent-pay-worker-secret" --vault "Agent Secrets" --fields label=credential --reveal',
    { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
  ).trim();
}

/**
 * Pay for a paywalled URL.
 *
 * Default (Pool Mode A): Apple Pay per transaction. Parker's float covers x402.
 * --wallet=cdp (Path 1): Sign with user's CDP wallet.
 * --wallet=privy (Path 1): Sign with user's Privy wallet.
 */
export async function pay(url, opts = {}) {
  // Path 1: self-custody wallet
  if (opts.wallet === 'cdp') {
    const x402Pay = await getX402();
    return x402Pay(url);
  }
  if (opts.wallet === 'privy') {
    const privyPay = await getPrivy();
    return privyPay(url);
  }

  // Pool Mode A (default): Apple Pay + pool wallet
  const pool = await getPool();
  return pool.default(url);
}

/**
 * Fund wallet via Stripe (money in).
 * Opens Apple Pay checkout, deposits to agent wallet.
 */
export async function fund(amount, opts = {}) {
  const stripeFund = await getStripe();
  return stripeFund(amount, opts);
}

/**
 * Mint a one-time URL (existing Mode B flow).
 */
export async function mint(amount, service, note = '') {
  return mintAuthorize(amount, service, note);
}

/**
 * Check wallet balance.
 */
export async function balance(opts = {}) {
  let workerSecret;
  try { workerSecret = getWorkerSecret(); } catch {
    return { error: '1Password: could not retrieve worker secret' };
  }

  const wallet = opts.wallet || 'cdp';
  const res = await fetch(`${WORKER_URL}/balance`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ wallet }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { error: `Worker returned ${res.status}: ${body}` };
  }

  return res.json();
}

/**
 * Get transaction history.
 */
export async function history(opts = {}) {
  let workerSecret;
  try { workerSecret = getWorkerSecret(); } catch {
    return { error: '1Password: could not retrieve worker secret' };
  }

  const wallet = opts.wallet || 'cdp';
  const limit = opts.limit || 20;
  const res = await fetch(`${WORKER_URL}/history`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ wallet, limit }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { error: `Worker returned ${res.status}: ${body}` };
  }

  return res.json();
}

/**
 * Get or set budget (spending limits).
 */
export async function budget(opts = {}) {
  let workerSecret;
  try { workerSecret = getWorkerSecret(); } catch {
    return { error: '1Password: could not retrieve worker secret' };
  }

  const wallet = opts.wallet || 'cdp';
  const res = await fetch(`${WORKER_URL}/budget`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({
      wallet,
      // If setting a budget
      ...(opts.daily !== undefined && { daily: opts.daily }),
      ...(opts.perTx !== undefined && { perTx: opts.perTx }),
      ...(opts.total !== undefined && { total: opts.total }),
    }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { error: `Worker returned ${res.status}: ${body}` };
  }

  return res.json();
}

// Default export for backwards compatibility (mint flow)
export default mintAuthorize;
