import test from "node:test";
import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import {
  assessFunds,
  computeConfirmationToken,
  computeIntentHash,
  normalizeTransferLookupResponse,
  normalizeTransferStatus,
  normalizeWalletBalanceResponse,
  readApiKeyFromFile,
  redactForLogs,
  resolveApiKey,
  sanitizeTransferStateSnapshot,
} from "../scripts/raven-transfer.mjs";

test("normalizeWalletBalanceResponse handles wallet array payload", () => {
  const input = {
    data: [
      { currency: "USD", balance: "10", available_balance: "8" },
      { currency: "NGN", balance: "10000", available_balance: "9500" },
    ],
  };

  const out = normalizeWalletBalanceResponse(input);
  assert.equal(out.available_ngn, 9500);
  assert.equal(out.balance_ngn, 10000);
  assert.equal(out.wallets.length, 2);
});

test("normalizeWalletBalanceResponse handles legacy object payload", () => {
  const input = { data: { currency: "NGN", balance: "5000" } };
  const out = normalizeWalletBalanceResponse(input);
  assert.equal(out.available_ngn, 5000);
  assert.equal(out.balance_ngn, 5000);
});

test("confirmation token is deterministic for same intent", () => {
  const intent = {
    beneficiary_type: "bank",
    amount: 5000,
    currency: "NGN",
    bank: "GTBank",
    bank_code: "058",
    account_number: "0690000031",
    account_name: "John Doe",
    narration: "Invoice 182",
  };

  const h1 = computeIntentHash(intent);
  const h2 = computeIntentHash(intent);
  assert.equal(h1, h2);
  assert.equal(computeConfirmationToken(h1), computeConfirmationToken(h2));
});

test("assessFunds computes strict pre-transfer checks", () => {
  const okCase = assessFunds(10000, 5000, 50);
  assert.equal(okCase.sufficient, true);
  assert.equal(okCase.total_debit, 5050);
  assert.equal(okCase.projected_post_balance, 4950);

  const failCase = assessFunds(5000, 5000, 50);
  assert.equal(failCase.sufficient, false);
  assert.equal(failCase.total_debit, 5050);
  assert.equal(failCase.projected_post_balance, -50);
});

test("normalizeTransferStatus maps reversed values", () => {
  assert.equal(normalizeTransferStatus("reversed"), "reversed");
  assert.equal(normalizeTransferStatus("reversal_completed"), "reversed");
  assert.equal(normalizeTransferStatus("refund"), "reversed");
});

test("normalizeTransferLookupResponse extracts transfer status fields", () => {
  const input = {
    data: {
      trx_ref: "rav_123",
      merchant_ref: "INV_1",
      status: "pending",
      amount: "5000",
      fee: "50",
    },
  };

  const out = normalizeTransferLookupResponse(input);
  assert.equal(out.trx_ref, "rav_123");
  assert.equal(out.merchant_ref, "INV_1");
  assert.equal(out.status, "pending");
  assert.equal(out.raw_status, "pending");
  assert.equal(out.amount, 5000);
  assert.equal(out.fee, 50);
  assert.equal(out.total_debit, 5050);
});

test("normalizeTransferLookupResponse honors reversal flag", () => {
  const input = {
    data: {
      trx_ref: "rav_456",
      status: "pending",
      reversed: true,
    },
  };

  const out = normalizeTransferLookupResponse(input);
  assert.equal(out.status, "reversed");
});

test("sanitizeTransferStateSnapshot strips account PII and payload fields", () => {
  const state = {
    refs: {
      "INV-100": {
        merchant_ref: "INV-100",
        trx_ref: "rav_100",
        status: "pending",
        raw_status: "pending",
        amount: 1000,
        fee: 10,
        account_name: "Jane Doe",
        account_number: "0123456789",
        bank: "058",
        payload: { secret: true },
      },
    },
    intents: {
      abc123: {
        intent_hash: "abc123",
        merchant_ref: "INV-100",
        trx_ref: "rav_100",
        status: "pending",
        raw_status: "pending",
        amount: 1000,
        fee: 10,
        account_name: "Jane Doe",
        payload: { secret: true },
      },
    },
  };

  const out = sanitizeTransferStateSnapshot(state);
  assert.deepEqual(out.refs["INV-100"], {
    merchant_ref: "INV-100",
    trx_ref: "rav_100",
    status: "pending",
    raw_status: "pending",
    amount: 1000,
    fee: 10,
  });
  assert.deepEqual(out.intents.abc123, {
    intent_hash: "abc123",
    merchant_ref: "INV-100",
    trx_ref: "rav_100",
    status: "pending",
    raw_status: "pending",
    amount: 1000,
    fee: 10,
  });
});

test("resolveApiKey supports secure file-based key loading", () => {
  const dir = mkdtempSync(join(tmpdir(), "raven-transfer-test-"));
  const keyFile = join(dir, "api-key.txt");

  try {
    writeFileSync(keyFile, "RVSEC-file-based-key\n");
    chmodSync(keyFile, 0o600);

    const resolved = resolveApiKey({
      RAVEN_API_KEY: "RVSEC-inline-fallback",
      RAVEN_API_KEY_FILE: keyFile,
    });

    assert.equal(resolved, "RVSEC-file-based-key");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("readApiKeyFromFile rejects broad file permissions", () => {
  const dir = mkdtempSync(join(tmpdir(), "raven-transfer-test-"));
  const keyFile = join(dir, "api-key.txt");

  try {
    writeFileSync(keyFile, "RVSEC-bad-perm");
    chmodSync(keyFile, 0o644);

    assert.throws(
      () => readApiKeyFromFile(keyFile),
      /permissions are too broad/i,
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("redactForLogs redacts secret fields and token-like values", () => {
  const out = redactForLogs({
    Authorization: "Bearer abcdefghijklmnopqrstuvwxyz123456",
    RAVEN_API_KEY: "RVSEC-cc9ca22d8d76d8ef7f84a353592b4f0525cd7e4aa8caf9bfb2d884da35d8fbcec8825fb8e6957cc4eb5a95ceca769ff3",
    confirmation_token: "CONFIRM TXN_ABC123DEF456",
    nested: {
      error: "upstream returned RVSEC-12345678901234567890",
    },
  });

  assert.equal(out.Authorization, "[REDACTED]");
  assert.equal(out.RAVEN_API_KEY, "[REDACTED]");
  assert.equal(out.confirmation_token, "CONFIRM TXN_ABC123DEF456");
  assert.equal(out.nested.error, "upstream returned [REDACTED]");
});
