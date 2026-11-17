// providers/coinbase.js
// v1 Coinbase provider (isolated portfolio only)
//
// Worker is live. Coinbase transfer is still TODO (v1.1).
// Right now: mints real one-time URLs on the Worker, but no actual
// funds move yet. When Coinbase API is wired, Step 2 sends USDC
// before minting the URL.

import { execSync } from 'node:child_process';

const WORKER_URL = 'https://pay-wip-computer.wipcomputer.workers.dev';

export default async function authorize(amount, service, note = '') {
  console.log(`\n  wip-agent-pay ... authorizing`);
  console.log(`  Amount: ${amount}`);
  console.log(`  Service: ${service}`);
  if (note) console.log(`  Note: ${note}`);

  // --- Step 1: Pull Worker secret from 1Password ---
  let workerSecret;
  try {
    workerSecret = execSync(
      'OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) ' +
      'op item get "wip-agent-pay-worker-secret" --vault "Agent Secrets" --fields label=credential --reveal',
      { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim();
  } catch (err) {
    return { success: false, error: '1Password: could not retrieve worker secret' };
  }

  // --- Step 2: Send funds via Coinbase Advanced Trade API ---
  // TODO (v1.1): Wire real Coinbase transfer
  // When wired, this step will:
  //   1. Pull API key + secret from 1Password (wip-agent-pay-coinbase)
  //   2. Send USDC from isolated "wip-agent-pay" portfolio
  //   3. Only proceed to Step 3 if transfer succeeds

  // --- Step 3: Mint one-time URL via Worker ---
  const res = await fetch(`${WORKER_URL}/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${workerSecret}`
    },
    body: JSON.stringify({ amount, service, note, expiresMin: 3 })
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    return { success: false, error: `Worker returned ${res.status}: ${body}` };
  }

  const { url } = await res.json();
  return { success: true, provider: 'coinbase', amount, service, note, url };
}
