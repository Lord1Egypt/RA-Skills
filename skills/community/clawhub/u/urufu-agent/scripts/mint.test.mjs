import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  evaluateMintSession,
  parseMintPhase,
  PAYMENT_FREE,
  phaseIsOpen,
  POLICY,
} from './policy.mjs';

describe('urufu mint policy', () => {
  it('parseMintPhase reads tuple shape', () => {
    const phase = parseMintPhase([
      PAYMENT_FREE,
      0n,
      500,
      1,
      0n,
      0n,
      '0x0000000000000000000000000000000000000000000000000000000000000000',
      0n,
      0n,
      0n,
    ]);
    assert.equal(phase.payment, PAYMENT_FREE);
    assert.equal(phase.maxMints, 500);
  });

  it('phaseIsOpen respects timestamps', () => {
    const phase = parseMintPhase([
      PAYMENT_FREE,
      0n,
      500,
      1,
      100n,
      200n,
      '0x0000000000000000000000000000000000000000000000000000000000000000',
      0n,
      0n,
      0n,
    ]);
    assert.equal(phaseIsOpen(phase, 150), true);
    assert.equal(phaseIsOpen(phase, 50), false);
  });

  it('evaluateMintSession blocks inside 24h cooldown', () => {
    const now = 1_000_000;
    const result = evaluateMintSession(
      { lastMintAtMs: now - 1000 },
      { gaslessEligible: true, hasAllowlist: true, phaseOpen: true },
      now,
    );
    assert.equal(result.allowed, false);
  });

  it('evaluateMintSession allows eligible gasless mint', () => {
    const now = 1_000_000;
    const result = evaluateMintSession(
      { lastMintAtMs: now - POLICY.mintMinIntervalMs - 1 },
      {
        gaslessEligible: true,
        hasAllowlist: true,
        phaseOpen: true,
        walletCapReached: false,
        phaseSoldOut: false,
      },
      now,
    );
    assert.equal(result.allowed, true);
  });
});
