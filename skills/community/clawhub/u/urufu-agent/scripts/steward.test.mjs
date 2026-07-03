import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { chunkTokenIds } from './chain.mjs';
import { evaluateClaimSession, POLICY } from './policy.mjs';

describe('urufu steward helpers', () => {
  it('chunks token ids for multi-batch claims', () => {
    const ids = [1n, 2n, 3n, 4n, 5n];
    assert.deepEqual(chunkTokenIds(ids, 2), [[1n, 2n], [3n, 4n], [5n]]);
  });

  it('evaluateClaimSession allows large portfolios', () => {
    const now = 1_000_000;
    const ids = Array.from({ length: 50 }, (_, i) => BigInt(i + 1));
    const result = evaluateClaimSession(
      { lastClaimAtMs: now - POLICY.claimMinIntervalMs - 1 },
      { totalUruWei: 10n ** 18n, totalWethWei: 0n, tokenIds: ids },
      now,
    );
    assert.equal(result.allowed, true);
  });
});
