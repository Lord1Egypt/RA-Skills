/**
 * Urufu agent safety policy — import from steward scripts or agent runtimes.
 * Defaults match .claude/skills/urufu-agent-play/references/agent-policy.json
 */

export const POLICY = {
  claimMinIntervalMs: 6 * 60 * 60 * 1000,
  minTotalClaimableUruWei: 1_000_000_000_000_000n, // 0.001 URU
  maxTokenIdsPerBatch: 25,
  claimBackoffOn429Ms: 60 * 60 * 1000,
  mintAutoAllowed: false,
  mintMinIntervalMs: 24 * 60 * 60 * 1000,
  swapAutoAllowed: false,
  swapMinIntervalMs: 60 * 60 * 1000,
  statsPollMinIntervalMs: 5 * 60 * 1000,
  meadowMaxMessagesPerSecond: 2,
};

/**
 * Session-level claim gate (ignores batch size — use chunkTokenIds for batches).
 * @param {object} state
 * @param {object} preview { totalUruWei, totalWethWei, tokenIds }
 * @param {number} [nowMs=Date.now()]
 * @param {number} [minIntervalMs=POLICY.claimMinIntervalMs]
 */
export function evaluateClaimSession(state, preview, nowMs = Date.now(), minIntervalMs = POLICY.claimMinIntervalMs) {
  const reasons = [];
  const last = state?.lastClaimAtMs ?? 0;
  const elapsed = nowMs - last;
  if (elapsed < minIntervalMs) {
    reasons.push(
      `claim cooldown: ${Math.ceil((minIntervalMs - elapsed) / 60000)} min remaining`,
    );
  }
  const uru = preview.totalUruWei ?? 0n;
  const weth = preview.totalWethWei ?? 0n;
  if (uru === 0n && weth === 0n) {
    reasons.push('zero pending yield');
  }
  if (uru > 0n && uru < POLICY.minTotalClaimableUruWei) {
    reasons.push('URU below minimum dust threshold');
  }
  const ids = preview.tokenIds ?? [];
  if (ids.length === 0 && (uru > 0n || weth > 0n)) {
    reasons.push('no eligible token ids');
  }
  return {
    allowed: reasons.length === 0,
    reasons,
    nextEligibleAtMs: last + minIntervalMs,
  };
}

/** @deprecated use evaluateClaimSession — kept for single-batch checks */
export function evaluateClaim(state, preview, nowMs = Date.now()) {
  const session = evaluateClaimSession(state, preview, nowMs);
  const ids = preview.tokenIds ?? [];
  if (ids.length > POLICY.maxTokenIdsPerBatch) {
    return {
      ...session,
      allowed: false,
      reasons: [...session.reasons, `batch too large (max ${POLICY.maxTokenIdsPerBatch})`],
    };
  }
  return session;
}

/**
 * @param {number} consecutiveErrors
 */
export function claimRetryBackoffMs(consecutiveErrors) {
  if (consecutiveErrors <= 0) return 0;
  const steps = [5 * 60 * 1000, 15 * 60 * 1000, 60 * 60 * 1000];
  return steps[Math.min(consecutiveErrors - 1, steps.length - 1)];
}

const ZERO_MERKLE_ROOT = '0x0000000000000000000000000000000000000000000000000000000000000000';
export const PAYMENT_FREE = 0;

export function parseMintPhase(raw) {
  if (Array.isArray(raw)) {
    return {
      payment: Number(raw[0]),
      price: raw[1],
      maxMints: Number(raw[2]),
      maxPerWallet: Number(raw[3]),
      startTimestamp: raw[4],
      endTimestamp: raw[5],
      merkleRoot: raw[6],
    };
  }
  return {
    payment: Number(raw.payment),
    price: raw.price,
    maxMints: Number(raw.maxMints),
    maxPerWallet: Number(raw.maxPerWallet),
    startTimestamp: raw.startTimestamp,
    endTimestamp: raw.endTimestamp,
    merkleRoot: raw.merkleRoot,
  };
}

export function phaseIsOpen(phase, nowSeconds = Math.floor(Date.now() / 1000)) {
  const now = BigInt(nowSeconds);
  return phase.startTimestamp <= now && (phase.endTimestamp === 0n || phase.endTimestamp >= now);
}

/**
 * @param {object} state
 * @param {object} preview { gaslessEligible, hasAllowlist, phaseOpen }
 * @param {number} [nowMs=Date.now()]
 * @param {number} [minIntervalMs=POLICY.mintMinIntervalMs]
 */
export function evaluateMintSession(state, preview, nowMs = Date.now(), minIntervalMs = POLICY.mintMinIntervalMs) {
  const reasons = [];
  const last = state?.lastMintAtMs ?? 0;
  const elapsed = nowMs - last;
  if (elapsed < minIntervalMs) {
    reasons.push(
      `mint cooldown: ${Math.ceil((minIntervalMs - elapsed) / 60000)} min remaining`,
    );
  }
  if (!preview.gaslessEligible) {
    reasons.push('no gasless free phase available (paid phases need wallet ETH/URU tx)');
  }
  if (preview.gaslessEligible && preview.hasAllowlist === false) {
    reasons.push('wallet not on allowlist for open free phase');
  }
  if (preview.gaslessEligible && !preview.phaseOpen) {
    reasons.push('free phase not open');
  }
  if (preview.walletCapReached) {
    reasons.push('wallet phase mint cap reached');
  }
  if (preview.phaseSoldOut) {
    reasons.push('phase sold out');
  }
  return {
    allowed: reasons.length === 0,
    reasons,
    nextEligibleAtMs: last + minIntervalMs,
  };
}

export { ZERO_MERKLE_ROOT };
