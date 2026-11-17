// providers/stripe.js
// Stripe funding provider. Opens Apple Pay checkout to fund agent wallet.
// Worker creates Stripe Checkout session. User taps Face ID. Done.
//
// The user never sees crypto. Stripe handles fiat. Worker handles the rest.

import { execSync } from 'node:child_process';

const WORKER_URL = 'https://pay-wip-computer.wipcomputer.workers.dev';

/**
 * Fund agent wallet via Apple Pay / Stripe Checkout.
 *
 * @param {number} amount - USD amount to fund
 * @param {object} opts - { wallet: 'cdp'|'privy' }
 * @returns {{ success, checkoutUrl, fundId, error }}
 */
export default async function fund(amount, opts = {}) {
  const wallet = opts.wallet || 'cdp';

  console.log(`\n  wip-agent-pay ... funding wallet`);
  console.log(`  Amount: $${amount}`);
  console.log(`  Wallet: ${wallet}`);

  // Pull Worker secret from 1Password
  let workerSecret;
  try {
    workerSecret = execSync(
      'OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) ' +
      'op item get "wip-agent-pay-worker-secret" --vault "Agent Secrets" --fields label=credential --reveal',
      { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim();
  } catch {
    return { success: false, error: '1Password: could not retrieve worker secret' };
  }

  // Call Worker /stripe/checkout
  const res = await fetch(`${WORKER_URL}/stripe/checkout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ amount, wallet }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { success: false, error: `Worker returned ${res.status}: ${body}` };
  }

  const { checkoutUrl, fundId } = await res.json();
  return { success: true, checkoutUrl, fundId, amount, wallet };
}
