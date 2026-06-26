import test from "node:test";
import assert from "node:assert/strict";

import { normalizeTransferLookupResponse, normalizeWalletBalanceResponse, resolveApiKey } from "../scripts/raven-transfer.mjs";

const apiBase = process.env.RAVEN_API_BASE || "https://integrations.getravenbank.com/v1";
const runLive = process.env.RAVEN_CONTRACT_TESTS === "1";
const apiKey = (() => {
  try {
    return resolveApiKey(process.env);
  } catch {
    return null;
  }
})();

async function ravenLive(method, path, body) {
  const response = await fetch(`${apiBase}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

  const data = await response.json().catch(() => ({}));
  return { response, data };
}

test("contract: /accounts/wallet_balance shape remains parseable", { skip: !runLive || !apiKey }, async () => {
  const { response, data } = await ravenLive("POST", "/accounts/wallet_balance");
  assert.equal(response.ok, true, JSON.stringify(data));

  const normalized = normalizeWalletBalanceResponse(data);
  assert.ok(Array.isArray(normalized.wallets));
  assert.ok(normalized.wallets.length >= 1);
});

test("contract: /account_number_lookup responds with account fields", {
  skip: !runLive || !apiKey || !process.env.RAVEN_TEST_ACCOUNT_NUMBER || (!process.env.RAVEN_TEST_BANK && !process.env.RAVEN_TEST_BANK_CODE),
}, async () => {
  const body = {
    account_number: process.env.RAVEN_TEST_ACCOUNT_NUMBER,
    bank: process.env.RAVEN_TEST_BANK || process.env.RAVEN_TEST_BANK_CODE,
    ...(process.env.RAVEN_TEST_BANK_CODE ? { bank_code: process.env.RAVEN_TEST_BANK_CODE } : {}),
  };

  const { response, data } = await ravenLive("POST", "/account_number_lookup", body);
  assert.equal(response.ok, true, JSON.stringify(data));

  const payload = data?.data ?? data;
  assert.ok(payload?.account_name, JSON.stringify(data));
  assert.ok(payload?.account_number, JSON.stringify(data));
});

test("contract: /transfers/create shape check (explicitly gated)", {
  skip: process.env.RAVEN_RUN_LIVE_TRANSFER_CREATE !== "I_UNDERSTAND" || !runLive || !apiKey || !process.env.RAVEN_TEST_TRANSFER_BANK || !process.env.RAVEN_TEST_TRANSFER_ACCOUNT_NUMBER || !process.env.RAVEN_TEST_TRANSFER_ACCOUNT_NAME,
}, async () => {
  const ref = `CONTRACT_${Date.now()}`;
  const body = {
    amount: Number(process.env.RAVEN_TEST_TRANSFER_AMOUNT || "10"),
    bank: process.env.RAVEN_TEST_TRANSFER_BANK,
    ...(process.env.RAVEN_TEST_TRANSFER_BANK_CODE ? { bank_code: process.env.RAVEN_TEST_TRANSFER_BANK_CODE } : {}),
    account_number: process.env.RAVEN_TEST_TRANSFER_ACCOUNT_NUMBER,
    account_name: process.env.RAVEN_TEST_TRANSFER_ACCOUNT_NAME,
    narration: "Contract test",
    reference: ref,
    merchant_ref: ref,
    currency: "NGN",
  };

  const { response, data } = await ravenLive("POST", "/transfers/create", body);
  assert.equal(response.ok, true, JSON.stringify(data));

  const payload = data?.data ?? data;
  assert.ok(payload?.status, JSON.stringify(data));
});

test("contract: /get-transfer shape remains parseable", {
  skip: !runLive || !apiKey || !process.env.RAVEN_TEST_TRX_REF,
}, async () => {
  const trxRef = process.env.RAVEN_TEST_TRX_REF;
  const { response, data } = await ravenLive("GET", `/get-transfer?trx_ref=${encodeURIComponent(trxRef)}`);
  assert.equal(response.ok, true, JSON.stringify(data));

  const normalized = normalizeTransferLookupResponse(data, { trx_ref: trxRef });
  assert.ok(normalized.trx_ref, JSON.stringify(normalized));
  assert.ok(normalized.status, JSON.stringify(normalized));
});
