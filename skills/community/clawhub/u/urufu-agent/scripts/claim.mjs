import { privateKeyToAccount } from 'viem/accounts';

import {
  chunkTokenIds,
  createChainClient,
  formatYieldReport,
  previewYieldForChibis,
  readClaimNonce,
  relayClaim,
  signClaimIntent,
} from './chain.mjs';
import { requireSigner, requireWallet } from './config.mjs';
import { fetchPortfolio, fetchStats } from './indexer.mjs';
import { runMintPreview } from './mint.mjs';
import { claimRetryBackoffMs, evaluateClaimSession, POLICY } from './policy.mjs';
import { loadState, saveState } from './state.mjs';

export async function runCheck(config) {
  const wallet = requireWallet(config);
  const [stats, chibis, state] = await Promise.all([
    fetchStats(config.indexerUrl),
    fetchPortfolio(config.indexerUrl, wallet),
    loadState(config.statePath),
  ]);

  const client = createChainClient(config);
  const preview = await previewYieldForChibis(client, config.vault, chibis);
  const yieldReport = formatYieldReport(preview);
  const decision = evaluateClaimSession(state, preview, Date.now(), config.claimMinIntervalMs);
  const mintReport = await runMintPreview(config);

  return {
    wallet,
    stats,
    chibiCount: chibis.length,
    yield: yieldReport,
    claim: decision,
    mint: mintReport.mint,
    mintPreview: mintReport.preview,
    state,
  };
}

export async function runClaim(config, { force = false } = {}) {
  const wallet = requireWallet(config);
  const privateKey = requireSigner(config);
  const account = privateKeyToAccount(privateKey);
  if (account.address.toLowerCase() !== wallet.toLowerCase()) {
    throw new Error('URUFU_PRIVATE_KEY does not match URUFU_WALLET');
  }

  const state = await loadState(config.statePath);
  const chibis = await fetchPortfolio(config.indexerUrl, wallet);
  const client = createChainClient(config);
  const preview = await previewYieldForChibis(client, config.vault, chibis);
  const decision = evaluateClaimSession(state, preview, Date.now(), config.claimMinIntervalMs);

  if (!force && !decision.allowed) {
    return { skipped: true, reasons: decision.reasons, preview: formatYieldReport(preview) };
  }

  if (preview.tokenIds.length === 0) {
    return { skipped: true, reasons: ['no eligible token ids'], preview: formatYieldReport(preview) };
  }

  const batches = chunkTokenIds(preview.tokenIds, config.maxBatchSize);
  const txHashes = [];

  for (const batch of batches) {
    const nonce = await readClaimNonce(client, config.vault, wallet);
    const signed = await signClaimIntent(account, config, batch, nonce);
    try {
      const result = await relayClaim(config, batch, nonce, signed);
      txHashes.push(result.txHash);
    } catch (error) {
      state.consecutiveErrors = (state.consecutiveErrors || 0) + 1;
      await saveState(config.statePath, state);
      const backoff = claimRetryBackoffMs(state.consecutiveErrors);
      const err = new Error(error.message || 'relay failed');
      err.status = error.status;
      err.backoffMs = backoff;
      throw err;
    }
  }

  state.lastClaimAtMs = Date.now();
  state.lastClaimTxHash = txHashes[txHashes.length - 1] ?? null;
  state.consecutiveErrors = 0;
  await saveState(config.statePath, state);

  return {
    skipped: false,
    txHashes,
    batches: batches.length,
    preview: formatYieldReport(preview),
  };
}

export function printCheckReport(report) {
  const lines = [
    `wallet: ${report.wallet}`,
    `chibis: ${report.chibiCount}`,
    `pending: ${report.yield.uru} URU, ${report.yield.weth} WETH (${report.yield.eligibleCount} eligible)`,
    `claim allowed: ${report.claim.allowed}`,
  ];
  if (report.claim.reasons.length) {
    lines.push(`reasons: ${report.claim.reasons.join('; ')}`);
  }
  if (report.claim.nextEligibleAtMs) {
    lines.push(`next claim eligible: ${new Date(report.claim.nextEligibleAtMs).toISOString()}`);
  }
  lines.push(`mint allowed: ${report.mint?.allowed ?? false}`);
  if (report.mint?.reasons?.length) {
    lines.push(`mint reasons: ${report.mint.reasons.join('; ')}`);
  }
  if (report.mintPreview?.phaseId != null) {
    lines.push(`gasless phase id: ${report.mintPreview.phaseId}`);
  }
  lines.push(`network total chibis: ${report.stats.totalChibis}`);
  return lines.join('\n');
}

export { POLICY };
