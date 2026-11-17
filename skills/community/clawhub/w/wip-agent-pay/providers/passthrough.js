// providers/passthrough.js
// Pool Mode (Mode A): User pays via Apple Pay (Stripe Checkout).
// Worker signs x402 from Parker's pool wallet. Content returned.
//
// Pricing: x402 price + Stripe fees + $0.25 flat fee.
// Max pool transaction: $25. Over $25 redirects to Mode C (user's own wallet).

import { execSync } from 'node:child_process';

const WORKER_URL = 'https://pay-wip-computer.wipcomputer.workers.dev';

function getWorkerSecret() {
  return execSync(
    'OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) ' +
    'op item get "wip-agent-pay-worker-secret" --vault "Agent Secrets" --fields label=credential --reveal',
    { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
  ).trim();
}

/**
 * Pay for a paywalled URL via Pool Mode.
 * Worker fetches 402, calculates total (x402 + Stripe fees + $0.25),
 * creates Stripe Checkout. Returns checkout URL for Apple Pay.
 *
 * @param {string} url - The paywalled URL
 * @returns {{ success, checkoutUrl, paymentId, amount, pricing, service, error }}
 */
export default async function pool(url) {
  console.log(`\n  wip-pay ... checking price`);
  console.log(`  URL: ${url}`);

  let workerSecret;
  try { workerSecret = getWorkerSecret(); } catch {
    return { success: false, error: '1Password: could not retrieve worker secret' };
  }

  // Hit the URL via Worker to get 402 + create Stripe Checkout
  const res = await fetch(`${WORKER_URL}/pool/pay`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    try {
      const data = JSON.parse(body);
      // Over pool limit ... redirect to Mode C
      if (data.status === 'over-pool-limit') {
        return {
          success: false,
          overPoolLimit: true,
          amount: data.amount,
          service: data.service,
          poolMax: data.poolMax,
          error: data.error,
        };
      }
    } catch { /* not JSON */ }
    return { success: false, error: `Worker returned ${res.status}: ${body}` };
  }

  const data = await res.json();

  // No paywall ... content came back free
  if (data.status === 'no-paywall') {
    return { success: true, content: data.content, amount: 0, free: true };
  }

  // 402 found ... checkout URL ready
  return {
    success: true,
    needsPayment: true,
    checkoutUrl: data.checkoutUrl,
    paymentId: data.paymentId,
    amount: data.amount,
    pricing: data.pricing,
    service: data.service,
  };
}

/**
 * Check if a pool payment has been confirmed.
 * Call this after user completes Apple Pay checkout.
 * Worker checks Stripe, signs x402 from pool wallet, returns content.
 *
 * @param {string} paymentId - The payment ID from pool()
 * @returns {{ success, content, amount, service, error }}
 */
export async function confirm(paymentId) {
  let workerSecret;
  try { workerSecret = getWorkerSecret(); } catch {
    return { success: false, error: '1Password: could not retrieve worker secret' };
  }

  const res = await fetch(`${WORKER_URL}/pool/confirm`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ paymentId }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { success: false, error: `Worker returned ${res.status}: ${body}` };
  }

  return res.json();
}

/**
 * Poll for payment confirmation with timeout.
 * Stripe Checkout -> webhook -> Worker signs x402 -> content returned.
 *
 * @param {string} paymentId
 * @param {number} timeoutMs - Max wait time (default: 120s)
 * @param {number} intervalMs - Poll interval (default: 2s)
 */
export async function waitForPayment(paymentId, timeoutMs = 120000, intervalMs = 2000) {
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    const result = await confirm(paymentId);
    if (result.success && result.status === 'paid') {
      return result;
    }
    if (result.error && result.error !== 'pending') {
      return result;
    }
    await new Promise(r => setTimeout(r, intervalMs));
  }

  return { success: false, error: 'Payment timed out. User may not have completed checkout.' };
}
