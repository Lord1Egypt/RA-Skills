// providers/x402.js
// x402 payment provider. Agent hits a paywalled URL, Worker handles
// the 402 negotiation, CDP signing, and retry. Returns content.
//
// The agent never sees crypto. The Worker does everything.

import { execSync } from 'node:child_process';

const WORKER_URL = 'https://pay-wip-computer.wipcomputer.workers.dev';

/**
 * Pay for a paywalled URL via x402.
 *
 * @param {string} url - The paywalled URL
 * @returns {{ success, content, amount, service, txHash, error }}
 */
export default async function pay(url) {
  console.log(`\n  wip-agent-pay ... paying via x402`);
  console.log(`  URL: ${url}`);

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

  // Call Worker /x402/pay ... Worker handles 402 negotiation, CDP signing, retry
  const res = await fetch(`${WORKER_URL}/x402/pay`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`,
    },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { success: false, error: `Worker returned ${res.status}: ${body}` };
  }

  const result = await res.json();
  return { success: true, ...result };
}
