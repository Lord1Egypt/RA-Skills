import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { claimRetryBackoffMs, evaluateClaim, POLICY } from './policy.mjs';

describe('urufu agent policy', () => {
  it('blocks claim inside cooldown window', () => {
    const now = 1_000_000;
    const result = evaluateClaim(
      { lastClaimAtMs: now - 1000 },
      { totalUruWei: 10n ** 18n, totalWethWei: 0n, tokenIds: [1n] },
      now,
    );
    assert.equal(result.allowed, false);
    assert.ok(result.reasons.some((r) => r.includes('cooldown')));
  });

  it('allows claim after cooldown with yield', () => {
    const now = 1_000_000;
    const result = evaluateClaim(
      { lastClaimAtMs: now - POLICY.claimMinIntervalMs - 1 },
      { totalUruWei: 10n ** 18n, totalWethWei: 0n, tokenIds: [1n, 2n] },
      now,
    );
    assert.equal(result.allowed, true);
  });

  it('blocks zero yield', () => {
    const result = evaluateClaim(
      { lastClaimAtMs: 0 },
      { totalUruWei: 0n, totalWethWei: 0n, tokenIds: [1n] },
    );
    assert.equal(result.allowed, false);
  });

  it('backs off on repeated errors', () => {
    assert.equal(claimRetryBackoffMs(1), 5 * 60 * 1000);
    assert.equal(claimRetryBackoffMs(3), 60 * 60 * 1000);
  });
});
