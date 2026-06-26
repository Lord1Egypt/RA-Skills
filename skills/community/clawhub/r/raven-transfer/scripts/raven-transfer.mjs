#!/usr/bin/env node

import { createHash, randomBytes } from "node:crypto";
import { chmodSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const API_BASE = process.env.RAVEN_API_BASE || "https://integrations.getravenbank.com/v1";
const TIMEOUT_MS = Number(process.env.RAVEN_TIMEOUT_MS || "30000");
const READ_RETRY_COUNT = Number(process.env.RAVEN_READ_RETRIES || "2");
const RETRY_BASE_DELAY_MS = Number(process.env.RAVEN_RETRY_DELAY_MS || "300");
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const STATE_FILE = join(SCRIPT_DIR, ".state", "transfer-state.json");
const MAX_STATE_ENTRIES = 500;
const STATE_DIR_MODE = 0o700;
const STATE_FILE_MODE = 0o600;
const LOCAL_STATE_DISABLED = process.env.RAVEN_DISABLE_LOCAL_STATE === "1";
const REDACTED = "[REDACTED]";
const SENSITIVE_KEY_PATTERN = /(?:^|_|-)(?:authorization|api(?:_|-)?key|token|secret|password|cookie)(?:$|_|-)/i;
const SENSITIVE_VALUE_PATTERNS = [
  /\bRVSEC-[A-Za-z0-9-]{20,}\b/g,
  /\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b/gi,
];
const LOG_SAFE_TOKEN_KEYS = new Set(["confirmation_token"]);
let cachedApiKey = null;

function redactString(value) {
  let redacted = value;
  for (const pattern of SENSITIVE_VALUE_PATTERNS) {
    redacted = redacted.replace(pattern, (match) => {
      if (/^bearer\s+/i.test(match)) {
        return "Bearer [REDACTED]";
      }
      return REDACTED;
    });
  }
  return redacted;
}

export function redactForLogs(value, seen = new WeakSet()) {
  if (typeof value === "string") {
    return redactString(value);
  }

  if (value === null || value === undefined) {
    return value;
  }

  if (typeof value !== "object") {
    return value;
  }

  if (seen.has(value)) {
    return "[Circular]";
  }
  seen.add(value);

  if (Array.isArray(value)) {
    return value.map((entry) => redactForLogs(entry, seen));
  }

  const redacted = {};
  for (const [key, entry] of Object.entries(value)) {
    if (SENSITIVE_KEY_PATTERN.test(key) && !LOG_SAFE_TOKEN_KEYS.has(key.toLowerCase())) {
      redacted[key] = REDACTED;
      continue;
    }
    redacted[key] = redactForLogs(entry, seen);
  }
  return redacted;
}

function ok(data) {
  console.log(JSON.stringify(redactForLogs({ ok: true, ...data })));
}

function fail(error, raw) {
  console.error(JSON.stringify(redactForLogs({ ok: false, error, ...(raw ? { raw } : {}) })));
  process.exit(1);
}

function usage(exitCode = 0) {
  const text = [
    "Usage:",
    "  node ./scripts/raven-transfer.mjs --cmd=balance",
    "  node ./scripts/raven-transfer.mjs --cmd=banks [--search=<keyword>]",
    "  node ./scripts/raven-transfer.mjs --cmd=lookup --account_number=<number> [--bank=<name_or_code>] [--bank_code=<code>]",
    "  node ./scripts/raven-transfer.mjs --cmd=transfer-status [--trx_ref=<ref>] [--merchant_ref=<ref>]",
    "  node ./scripts/raven-transfer.mjs --cmd=transfer --amount=<n> --bank=<name> --account_number=<number> --account_name=<name> [--bank_code=<code>] [--expected_fee=<n>] [--merchant_ref=<ref>] [--confirm=\"CONFIRM TXN_...\"] [--narration=<text>] [--currency=NGN]",
    "  node ./scripts/raven-transfer.mjs --cmd=transfer-merchant --merchant=<name> --amount=<n> --bank=<name> --account_number=<number> --account_name=<name> [--bank_code=<code>] [--expected_fee=<n>] [--merchant_ref=<ref>] [--confirm=\"CONFIRM TXN_...\"] [--narration=<text>] [--currency=NGN]",
  ].join("\n");

  if (exitCode === 0) {
    console.log(text);
  } else {
    console.error(text);
  }
  process.exit(exitCode);
}

function formatMode(mode) {
  return `0${(mode & 0o777).toString(8)}`;
}

export function readApiKeyFromFile(filePath) {
  const resolvedPath = `${filePath || ""}`.trim();
  if (!resolvedPath) {
    throw new Error("RAVEN_API_KEY_FILE is empty.");
  }

  let stats;
  try {
    stats = statSync(resolvedPath);
  } catch {
    throw new Error(`Unable to read RAVEN_API_KEY_FILE at ${resolvedPath}.`);
  }

  if (!stats.isFile()) {
    throw new Error(`RAVEN_API_KEY_FILE must point to a regular file: ${resolvedPath}`);
  }

  const mode = stats.mode & 0o777;
  if ((mode & 0o077) !== 0) {
    throw new Error(`RAVEN_API_KEY_FILE permissions are too broad (${formatMode(mode)}). Run chmod 600 ${resolvedPath}.`);
  }

  const key = readFileSync(resolvedPath, "utf8").trim();
  if (!key) {
    throw new Error(`RAVEN_API_KEY_FILE is empty: ${resolvedPath}`);
  }

  return key;
}

export function resolveApiKey(env = process.env) {
  const apiKeyFile = `${env.RAVEN_API_KEY_FILE || ""}`.trim();
  if (apiKeyFile) {
    return readApiKeyFromFile(apiKeyFile);
  }

  const key = `${env.RAVEN_API_KEY || ""}`.trim();
  if (!key) {
    throw new Error("RAVEN_API_KEY is not set. Set RAVEN_API_KEY or RAVEN_API_KEY_FILE in the skill runtime.");
  }

  return key;
}

function getApiKey() {
  if (cachedApiKey) {
    return cachedApiKey;
  }

  try {
    cachedApiKey = resolveApiKey();
  } catch (error) {
    fail(error?.message || "Unable to resolve Raven API key");
  }

  return cachedApiKey;
}

function getRequired(values, names, cmd) {
  const missing = names.filter((name) => {
    const value = values[name];
    return value === undefined || value === null || `${value}`.trim() === "";
  });

  if (missing.length > 0) {
    fail(`Missing required args for ${cmd}: ${missing.join(", ")}`);
  }
}

function asNumber(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function parsePositiveAmount(rawAmount) {
  const amount = asNumber(rawAmount);
  if (amount === null || amount <= 0) {
    fail("--amount must be a positive number");
  }
  return amount;
}

function parseExpectedFee(rawFee) {
  if (rawFee === undefined || rawFee === null || `${rawFee}`.trim() === "") {
    return 0;
  }

  const fee = asNumber(rawFee);
  if (fee === null || fee < 0) {
    fail("--expected_fee must be a non-negative number");
  }
  return fee;
}

function sleep(ms) {
  return new Promise((resolveSleep) => setTimeout(resolveSleep, ms));
}

function isTransientHttp(status) {
  return status === 408 || status === 425 || status === 429 || (status >= 500 && status < 600);
}

function isTransientNetworkError(error) {
  if (!error) {
    return false;
  }

  if (error.name === "AbortError") {
    return true;
  }

  const message = `${error.message || error}`.toLowerCase();
  return (
    message.includes("network") ||
    message.includes("fetch") ||
    message.includes("econn") ||
    message.includes("etimedout") ||
    message.includes("enotfound") ||
    message.includes("socket")
  );
}

function makeRequestError(message, context) {
  const error = new Error(message);
  error.context = context;
  return error;
}

export async function ravenRequest(method, path, body, options = {}) {
  const {
    retries = 0,
    operation = "request",
    timeoutMs = TIMEOUT_MS,
    fetchImpl = fetch,
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetchImpl(`${API_BASE}${path}`, {
        method,
        headers: {
          Authorization: `Bearer ${getApiKey()}`,
          "Content-Type": "application/json",
        },
        ...(body ? { body: JSON.stringify(body) } : {}),
        signal: controller.signal,
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok || data?.status === "error") {
        const message = data?.message ?? `HTTP ${response.status}`;
        const retriable = isTransientHttp(response.status);

        if (retriable && attempt < retries) {
          await sleep(RETRY_BASE_DELAY_MS * (attempt + 1));
          continue;
        }

        throw makeRequestError(message, {
          operation,
          retriable,
          attempt: attempt + 1,
          http_status: response.status,
          raw: data,
        });
      }

      return data;
    } catch (error) {
      const retriable = isTransientNetworkError(error);

      if (retriable && attempt < retries) {
        await sleep(RETRY_BASE_DELAY_MS * (attempt + 1));
        continue;
      }

      if (error?.context) {
        lastError = error;
      } else {
        const context = {
          operation,
          retriable,
          attempt: attempt + 1,
          raw: { message: String(error?.message || error) },
        };

        if (error?.name === "AbortError") {
          lastError = makeRequestError("Request timeout while calling Raven API", context);
        } else {
          lastError = makeRequestError("Unable to reach Raven API", context);
        }
      }
    } finally {
      clearTimeout(timer);
    }
  }

  throw lastError || makeRequestError("Unknown Raven API error", { operation: "request", retriable: false, attempt: 1 });
}

function asWalletList(balancePayload) {
  if (Array.isArray(balancePayload)) {
    return balancePayload;
  }

  if (Array.isArray(balancePayload?.wallets)) {
    return balancePayload.wallets;
  }

  if (balancePayload && typeof balancePayload === "object") {
    return [balancePayload];
  }

  return [];
}

function normalizeWallet(wallet) {
  const currency = `${wallet?.currency ?? wallet?.wallet_currency ?? ""}`.toUpperCase();
  const balance = asNumber(wallet?.balance ?? wallet?.ledger_balance ?? wallet?.ledger_bal ?? wallet?.available_balance ?? wallet?.available_bal);
  const availableBalance = asNumber(wallet?.available_balance ?? wallet?.available_bal ?? wallet?.available ?? wallet?.balance ?? wallet?.ledger_balance ?? wallet?.ledger_bal);

  return {
    currency,
    balance,
    available_balance: availableBalance,
  };
}

export function normalizeWalletBalanceResponse(response) {
  const payload = response?.data ?? response;
  const wallets = asWalletList(payload).map(normalizeWallet).filter((wallet) => wallet.currency || wallet.balance !== null || wallet.available_balance !== null);

  if (wallets.length === 0) {
    throw new Error("Unexpected wallet balance response shape");
  }

  const ngn = wallets.find((wallet) => wallet.currency === "NGN");
  const availableNgn = ngn?.available_balance ?? ngn?.balance ?? null;
  const balanceNgn = ngn?.balance ?? ngn?.available_balance ?? null;

  return {
    wallets,
    available_ngn: availableNgn,
    balance_ngn: balanceNgn,
  };
}

export function computeIntentHash(intent) {
  const stable = [
    intent.beneficiary_type,
    intent.merchant || "",
    intent.amount,
    intent.currency || "NGN",
    intent.bank,
    intent.bank_code || "",
    intent.account_number,
    intent.account_name,
    intent.narration,
  ].join("|").toLowerCase();

  return createHash("sha256").update(stable).digest("hex");
}

export function computeConfirmationToken(intentHash) {
  return `CONFIRM TXN_${intentHash.slice(0, 12).toUpperCase()}`;
}

export function summarizeDebit(amount, fee) {
  return {
    amount,
    fee,
    total_debit: amount + fee,
  };
}

export function assessFunds(availableBalance, amount, fee) {
  const { total_debit: totalDebit } = summarizeDebit(amount, fee);
  const projectedPostBalance = availableBalance - totalDebit;
  return {
    sufficient: availableBalance >= totalDebit,
    total_debit: totalDebit,
    projected_post_balance: projectedPostBalance,
  };
}

function defaultNarration(values, beneficiaryType) {
  if (values.narration && values.narration.trim()) {
    return values.narration.trim();
  }

  if (beneficiaryType === "merchant") {
    return `Merchant payout to ${values.merchant}`;
  }

  return `Transfer to ${values.account_name}`;
}

function sanitizeRef(raw) {
  if (raw === undefined || raw === null) {
    return null;
  }

  const value = `${raw}`.trim();
  return value ? value : null;
}

function makeMerchantRef(raw) {
  const supplied = sanitizeRef(raw);
  if (supplied) {
    return supplied;
  }

  return `MREF_${Date.now()}_${randomBytes(3).toString("hex").toUpperCase()}`;
}

function compactDefined(object) {
  return Object.fromEntries(
    Object.entries(object).filter(([, value]) => value !== undefined && value !== null),
  );
}

function sanitizeText(value) {
  if (value === undefined || value === null) {
    return undefined;
  }

  const text = `${value}`.trim();
  return text ? text : undefined;
}

function sanitizeNumber(value) {
  const number = asNumber(value);
  return number === null ? undefined : number;
}

function sanitizeRefStateRecord(record, fallbackMerchantRef) {
  const merchantRef = sanitizeRef(record?.merchant_ref ?? fallbackMerchantRef);
  if (!merchantRef) {
    return null;
  }

  return compactDefined({
    merchant_ref: merchantRef,
    trx_ref: sanitizeRef(record?.trx_ref ?? record?.transfer_ref ?? record?.reference),
    status: sanitizeText(record?.status),
    raw_status: sanitizeText(record?.raw_status),
    amount: sanitizeNumber(record?.amount),
    fee: sanitizeNumber(record?.fee),
    created_at: sanitizeText(record?.created_at),
    updated_at: sanitizeText(record?.updated_at),
    intent_hash: sanitizeText(record?.intent_hash),
  });
}

function sanitizeIntentStateRecord(record, fallbackIntentHash) {
  const intentHash = sanitizeText(record?.intent_hash ?? fallbackIntentHash);
  if (!intentHash) {
    return null;
  }

  return compactDefined({
    intent_hash: intentHash,
    merchant_ref: sanitizeRef(record?.merchant_ref),
    trx_ref: sanitizeRef(record?.trx_ref ?? record?.transfer_ref ?? record?.reference),
    status: sanitizeText(record?.status),
    raw_status: sanitizeText(record?.raw_status),
    amount: sanitizeNumber(record?.amount),
    fee: sanitizeNumber(record?.fee),
    updated_at: sanitizeText(record?.updated_at),
  });
}

export function sanitizeTransferStateSnapshot(rawState) {
  const refs = {};
  const intents = {};

  const rawRefs = rawState?.refs && typeof rawState.refs === "object" ? rawState.refs : {};
  for (const [refKey, rawRecord] of Object.entries(rawRefs)) {
    const record = sanitizeRefStateRecord(rawRecord, refKey);
    if (record) {
      refs[record.merchant_ref] = record;
    }
  }

  const rawIntents = rawState?.intents && typeof rawState.intents === "object" ? rawState.intents : {};
  for (const [intentKey, rawRecord] of Object.entries(rawIntents)) {
    const record = sanitizeIntentStateRecord(rawRecord, intentKey);
    if (record) {
      intents[record.intent_hash] = record;
    }
  }

  return {
    refs: pruneToLimit(refs),
    intents: pruneToLimit(intents),
  };
}

function readTransferState() {
  if (LOCAL_STATE_DISABLED) {
    return { refs: {}, intents: {} };
  }

  if (!existsSync(STATE_FILE)) {
    return { refs: {}, intents: {} };
  }

  try {
    const raw = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    return sanitizeTransferStateSnapshot(raw);
  } catch {
    return { refs: {}, intents: {} };
  }
}

function pruneToLimit(recordMap) {
  const entries = Object.entries(recordMap);
  if (entries.length <= MAX_STATE_ENTRIES) {
    return recordMap;
  }

  entries.sort((a, b) => {
    const at = `${a[1]?.updated_at || a[1]?.created_at || ""}`;
    const bt = `${b[1]?.updated_at || b[1]?.created_at || ""}`;
    return at.localeCompare(bt);
  });

  const keep = entries.slice(entries.length - MAX_STATE_ENTRIES);
  return Object.fromEntries(keep);
}

function writeTransferState(state) {
  if (LOCAL_STATE_DISABLED) {
    return;
  }

  const dir = dirname(STATE_FILE);
  mkdirSync(dir, { recursive: true, mode: STATE_DIR_MODE });
  try {
    chmodSync(dir, STATE_DIR_MODE);
  } catch {
    // Best effort only. Continue if chmod is not supported.
  }

  const normalized = sanitizeTransferStateSnapshot(state);
  writeFileSync(STATE_FILE, JSON.stringify(normalized, null, 2), { mode: STATE_FILE_MODE });
  try {
    chmodSync(STATE_FILE, STATE_FILE_MODE);
  } catch {
    // Best effort only. Continue if chmod is not supported.
  }
}

export function normalizeTransferStatus(rawStatus) {
  const value = `${rawStatus || ""}`.toLowerCase();

  if (value.includes("revers") || value.includes("refund") || value.includes("return")) {
    return "reversed";
  }

  if (value === "successful" || value === "success" || value === "completed") {
    return "success";
  }

  if (value === "failed" || value === "error" || value === "rejected") {
    return "failed";
  }

  if (value === "pending" || value === "processing" || value === "queued") {
    return "pending";
  }

  return "submitted";
}

function firstDefined(...values) {
  for (const value of values) {
    if (value !== undefined && value !== null && `${value}` !== "") {
      return value;
    }
  }
  return null;
}

function pickTransferRecord(payload) {
  if (Array.isArray(payload)) {
    return payload.find((item) => item && typeof item === "object") || {};
  }

  if (!payload || typeof payload !== "object") {
    return {};
  }

  const nested = firstDefined(payload.transaction, payload.transfer, payload.record, payload.result);
  if (nested && typeof nested === "object" && !Array.isArray(nested)) {
    return nested;
  }

  return payload;
}

function statusGuidance(normalizedStatus) {
  if (normalizedStatus === "pending") {
    return "Transfer is pending settlement. Recheck status with transfer-status before any retry.";
  }

  if (normalizedStatus === "reversed") {
    return "Transfer appears reversed. Do not resend automatically. Reconcile with user and create a fresh transfer only after explicit approval.";
  }

  if (normalizedStatus === "failed") {
    return "Transfer failed. Confirm failure reason before attempting any new transfer.";
  }

  return null;
}

export function normalizeTransferLookupResponse(response, fallback = {}) {
  const payload = response?.data ?? response;
  const record = pickTransferRecord(payload);

  const reversalHint = firstDefined(
    record.reversal_status,
    record.reversalState,
    record.reversed === true ? "reversed" : null,
  );

  const rawStatusValue = firstDefined(
    reversalHint,
    record.transaction_status,
    record.transfer_status,
    record.status,
    record.state,
    record.transaction_state,
    payload?.transaction_status,
    payload?.transfer_status,
    payload?.status,
    response?.status,
    "unknown",
  );

  const rawStatus = `${rawStatusValue}`;
  const normalizedStatus = normalizeTransferStatus(rawStatus);
  const amount = asNumber(firstDefined(record.amount, record.transfer_amount, record.value));
  const fee = asNumber(firstDefined(record.fee, record.transfer_fee, record.charges)) ?? 0;

  return {
    trx_ref: firstDefined(record.trx_ref, record.transfer_ref, record.reference, fallback.trx_ref),
    merchant_ref: firstDefined(record.merchant_ref, record.reference, fallback.merchant_ref),
    amount,
    fee,
    total_debit: amount === null ? null : amount + fee,
    status: normalizedStatus,
    raw_status: rawStatus,
    created_at: firstDefined(record.created_at, record.createdAt),
    updated_at: firstDefined(record.updated_at, record.updatedAt),
    account_name: firstDefined(record.account_name, record.beneficiary_name),
    account_number: firstDefined(record.account_number, record.beneficiary_account),
    bank: firstDefined(record.bank, record.bank_name, record.bank_code),
    payload: record,
  };
}

function getRetryGuidance(operation, retriable) {
  if (operation === "transfer" || operation === "transfer-merchant") {
    return "Do not auto-retry transfer. Confirm final state with the reference and request a fresh confirmation token before retrying.";
  }

  if (retriable) {
    return "Transient error detected. Safe to retry the same command.";
  }

  return "Fix request data and retry.";
}

function emitRequestError(error, operation) {
  const context = error?.context || {};
  fail(error?.message || "Raven request failed", {
    operation,
    retriable: Boolean(context.retriable),
    attempt: context.attempt,
    http_status: context.http_status,
    retry_guidance: getRetryGuidance(operation, Boolean(context.retriable)),
    raw: context.raw,
  });
}

async function fetchBalanceSnapshot() {
  const response = await ravenRequest("POST", "/accounts/wallet_balance", undefined, {
    retries: READ_RETRY_COUNT,
    operation: "balance",
  });

  return normalizeWalletBalanceResponse(response);
}

async function cmdBalance() {
  try {
    const snapshot = await fetchBalanceSnapshot();
    ok({
      status: "ready",
      raw_status: "ok",
      currency: "NGN",
      available_balance: snapshot.available_ngn,
      balance: snapshot.balance_ngn,
      fee: 0,
      total_debit: 0,
      wallets: snapshot.wallets,
    });
  } catch (error) {
    emitRequestError(error, "balance");
  }
}

async function cmdBanks(search) {
  try {
    const response = await ravenRequest("GET", "/banks", undefined, {
      retries: READ_RETRY_COUNT,
      operation: "banks",
    });

    let banks = response?.data ?? response;

    if (!Array.isArray(banks)) {
      fail("Unexpected banks response", response);
    }

    if (search) {
      const query = search.toLowerCase();
      banks = banks.filter((bank) => {
        const name = `${bank?.name ?? ""}`.toLowerCase();
        const code = `${bank?.code ?? ""}`.toLowerCase();
        return name.includes(query) || code.includes(query);
      });
    }

    ok({
      status: "ready",
      raw_status: "ok",
      available_balance: null,
      fee: 0,
      total_debit: 0,
      banks: banks.map((bank) => ({ name: bank?.name, code: bank?.code })),
    });
  } catch (error) {
    emitRequestError(error, "banks");
  }
}

async function cmdLookup(values) {
  getRequired(values, ["account_number"], "lookup");

  if (!values.bank && !values.bank_code) {
    fail("lookup requires at least one of --bank or --bank_code");
  }

  const requestBody = {
    account_number: values.account_number,
    bank: values.bank || values.bank_code,
    ...(values.bank_code ? { bank_code: values.bank_code } : {}),
  };

  try {
    const response = await ravenRequest("POST", "/account_number_lookup", requestBody, {
      retries: READ_RETRY_COUNT,
      operation: "lookup",
    });

    const data = response?.data ?? response;
    const resolvedName = typeof data === "string" ? data : data?.account_name;
    const resolvedAccountNumber = typeof data === "string" ? values.account_number : data?.account_number ?? values.account_number;
    ok({
      status: "resolved",
      raw_status: `${response?.status || "ok"}`,
      available_balance: null,
      fee: 0,
      total_debit: 0,
      account_name: resolvedName,
      account_number: resolvedAccountNumber,
      bank: values.bank || values.bank_code,
    });
  } catch (error) {
    emitRequestError(error, "lookup");
  }
}

function prepareTransferIntent(values, beneficiaryType) {
  getRequired(values, ["amount", "bank", "account_number", "account_name"], beneficiaryType === "merchant" ? "transfer-merchant" : "transfer");

  if (beneficiaryType === "merchant") {
    getRequired(values, ["merchant"], "transfer-merchant");
  }

  const amount = parsePositiveAmount(values.amount);
  const expectedFee = parseExpectedFee(values.expected_fee);
  const narration = defaultNarration(values, beneficiaryType);
  const merchantRef = makeMerchantRef(values.merchant_ref);

  const intent = {
    beneficiary_type: beneficiaryType,
    merchant: beneficiaryType === "merchant" ? values.merchant : undefined,
    amount,
    expected_fee: expectedFee,
    bank: values.bank,
    bank_code: values.bank_code,
    account_number: values.account_number,
    account_name: values.account_name,
    narration,
    currency: values.currency ?? "NGN",
    merchant_ref: merchantRef,
  };

  const intentHash = computeIntentHash(intent);
  const confirmationToken = computeConfirmationToken(intentHash);

  return {
    intent,
    intent_hash: intentHash,
    confirmation_token: confirmationToken,
  };
}

function assertNoDuplicates(state, merchantRef, intentHash) {
  const existingRef = state.refs[merchantRef];
  if (existingRef) {
    fail("Duplicate merchant_ref detected. Ref already used.", {
      merchant_ref: merchantRef,
      existing: existingRef,
      retry_guidance: "Use a new merchant_ref after verifying prior transfer outcome.",
    });
  }

  const existingIntent = state.intents[intentHash];
  if (existingIntent && ["pending", "success", "submitted"].includes(existingIntent.status)) {
    fail("Possible duplicate transfer intent detected. Aborting to avoid double-send.", {
      intent_hash: intentHash,
      existing: existingIntent,
      retry_guidance: "Verify prior transfer status before submitting another transfer.",
    });
  }
}

function persistTransfer(state, params) {
  const now = new Date().toISOString();

  state.refs[params.merchant_ref] = {
    merchant_ref: params.merchant_ref,
    trx_ref: params.trx_ref,
    status: params.status,
    raw_status: params.raw_status,
    amount: params.amount,
    fee: params.fee,
    updated_at: now,
    created_at: params.created_at || now,
    intent_hash: params.intent_hash,
  };

  state.intents[params.intent_hash] = {
    intent_hash: params.intent_hash,
    merchant_ref: params.merchant_ref,
    trx_ref: params.trx_ref,
    status: params.status,
    raw_status: params.raw_status,
    amount: params.amount,
    fee: params.fee,
    updated_at: now,
  };

  writeTransferState(state);
}

function pendingGuidance(normalizedStatus) {
  return statusGuidance(normalizedStatus);
}

function findRefByTrxRef(state, trxRef) {
  return Object.entries(state.refs || {}).find(([, record]) => record?.trx_ref === trxRef) || null;
}

function upsertRefRecord(state, refKey, patch) {
  const safeRefKey = sanitizeRef(refKey);
  if (!safeRefKey) {
    return;
  }

  const existing = state.refs[safeRefKey] || {};
  const next = sanitizeRefStateRecord({
    ...existing,
    ...patch,
    merchant_ref: safeRefKey,
    created_at: existing.created_at || patch?.created_at,
    updated_at: new Date().toISOString(),
  }, safeRefKey);

  if (next) {
    state.refs[safeRefKey] = next;
  }
}

function syncStatusToState(state, transferStatus, providedMerchantRef) {
  const merchantRef = transferStatus.merchant_ref || providedMerchantRef;

  if (!merchantRef && transferStatus.trx_ref) {
    const found = findRefByTrxRef(state, transferStatus.trx_ref);
    if (found) {
      upsertRefRecord(state, found[0], transferStatus);
    }
    return;
  }

  upsertRefRecord(state, merchantRef, transferStatus);
  const intentHash = state.refs[merchantRef]?.intent_hash;
  if (intentHash) {
    const existingIntent = state.intents[intentHash] || {};
    const nextIntent = sanitizeIntentStateRecord({
      ...existingIntent,
      intent_hash: intentHash,
      merchant_ref: merchantRef,
      trx_ref: transferStatus.trx_ref || existingIntent.trx_ref,
      status: transferStatus.status || existingIntent.status,
      raw_status: transferStatus.raw_status || existingIntent.raw_status,
      amount: transferStatus.amount ?? existingIntent.amount,
      fee: transferStatus.fee ?? existingIntent.fee,
      updated_at: new Date().toISOString(),
    }, intentHash);

    if (nextIntent) {
      state.intents[intentHash] = nextIntent;
    }
  }
}

async function cmdTransferStatus(values) {
  if (!values.trx_ref && !values.merchant_ref) {
    fail("transfer-status requires --trx_ref or --merchant_ref");
  }

  const state = readTransferState();
  let trxRef = values.trx_ref;
  if (!trxRef && values.merchant_ref) {
    trxRef = state.refs[values.merchant_ref]?.trx_ref;
  }

  if (!trxRef) {
    fail("Unable to resolve trx_ref for status check", {
      merchant_ref: values.merchant_ref,
      retry_guidance: "Pass --trx_ref directly or run transfer command to persist refs first.",
    });
  }

  try {
    const response = await ravenRequest("GET", `/get-transfer?trx_ref=${encodeURIComponent(trxRef)}`, undefined, {
      retries: READ_RETRY_COUNT,
      operation: "transfer-status",
    });

    const transferStatus = normalizeTransferLookupResponse(response, {
      trx_ref: trxRef,
      merchant_ref: values.merchant_ref,
    });

    syncStatusToState(state, transferStatus, values.merchant_ref);
    writeTransferState(state);

    ok({
      ...transferStatus,
      available_balance: null,
      settlement_guidance: statusGuidance(transferStatus.status),
      checked_at: new Date().toISOString(),
    });
  } catch (error) {
    emitRequestError(error, "transfer-status");
  }
}

async function cmdTransfer(values, beneficiaryType) {
  const operation = beneficiaryType === "merchant" ? "transfer-merchant" : "transfer";
  const prepared = prepareTransferIntent(values, beneficiaryType);

  let snapshot;
  try {
    snapshot = await fetchBalanceSnapshot();
  } catch (error) {
    emitRequestError(error, "balance");
  }

  const availableNgn = snapshot.available_ngn;
  if (availableNgn === null) {
    fail("Unable to determine NGN wallet balance for pre-transfer checks", {
      wallets: snapshot.wallets,
    });
  }

  const funds = assessFunds(availableNgn, prepared.intent.amount, prepared.intent.expected_fee);

  if (!funds.sufficient) {
    fail("Insufficient NGN balance for requested transfer", {
      available_balance: availableNgn,
      amount: prepared.intent.amount,
      fee: prepared.intent.expected_fee,
      total_debit: funds.total_debit,
      projected_post_balance: funds.projected_post_balance,
    });
  }

  const confirmInput = values.confirm ? values.confirm.trim() : "";
  if (confirmInput !== prepared.confirmation_token) {
    ok({
      status: "requires_confirmation",
      raw_status: "awaiting_confirmation_token",
      confirmation_token: prepared.confirmation_token,
      beneficiary_type: beneficiaryType,
      ...(beneficiaryType === "merchant" ? { merchant: prepared.intent.merchant } : {}),
      account_name: prepared.intent.account_name,
      account_number: prepared.intent.account_number,
      bank: prepared.intent.bank,
      bank_code: prepared.intent.bank_code,
      amount: prepared.intent.amount,
      fee: prepared.intent.expected_fee,
      total_debit: funds.total_debit,
      available_balance: availableNgn,
      projected_post_balance: funds.projected_post_balance,
      merchant_ref: prepared.intent.merchant_ref,
      narration: prepared.intent.narration,
      confirmation_hint: `Re-run with --confirm=\"${prepared.confirmation_token}\"`,
    });
    return;
  }

  const state = readTransferState();
  assertNoDuplicates(state, prepared.intent.merchant_ref, prepared.intent_hash);

  try {
    const response = await ravenRequest("POST", "/transfers/create", {
      amount: prepared.intent.amount,
      bank: prepared.intent.bank,
      ...(prepared.intent.bank_code ? { bank_code: prepared.intent.bank_code } : {}),
      account_number: prepared.intent.account_number,
      account_name: prepared.intent.account_name,
      narration: prepared.intent.narration,
      reference: prepared.intent.merchant_ref,
      merchant_ref: prepared.intent.merchant_ref,
      currency: prepared.intent.currency,
    }, {
      retries: 0,
      operation,
    });

    const data = response?.data ?? response;
    const rawStatus = `${data?.status ?? response?.status ?? "unknown"}`;
    const normalizedStatus = normalizeTransferStatus(rawStatus);
    const fee = asNumber(data?.fee) ?? prepared.intent.expected_fee;
    const debit = summarizeDebit(prepared.intent.amount, fee);

    persistTransfer(state, {
      merchant_ref: prepared.intent.merchant_ref,
      intent_hash: prepared.intent_hash,
      trx_ref: data?.trx_ref,
      status: normalizedStatus,
      raw_status: rawStatus,
      amount: prepared.intent.amount,
      fee,
      created_at: data?.created_at,
    });

    ok({
      beneficiary_type: beneficiaryType,
      ...(beneficiaryType === "merchant" ? { merchant: prepared.intent.merchant } : {}),
      trx_ref: data?.trx_ref,
      merchant_ref: data?.merchant_ref ?? prepared.intent.merchant_ref,
      amount: prepared.intent.amount,
      available_balance: availableNgn,
      fee,
      total_debit: debit.total_debit,
      projected_post_balance: availableNgn - debit.total_debit,
      status: normalizedStatus,
      raw_status: rawStatus,
      created_at: data?.created_at,
      settlement_guidance: pendingGuidance(normalizedStatus),
      status_check_command: data?.trx_ref
        ? `node ./scripts/raven-transfer.mjs --cmd=transfer-status --trx_ref=${data.trx_ref}`
        : null,
    });
  } catch (error) {
    emitRequestError(error, operation);
  }
}

function isMainModule() {
  if (!process.argv[1]) {
    return false;
  }

  return resolve(process.argv[1]) === fileURLToPath(import.meta.url);
}

export async function main(argv = process.argv.slice(2)) {
  const { values } = parseArgs({
    args: argv,
    options: {
      help: { type: "boolean", short: "h", default: false },
      cmd: { type: "string" },
      search: { type: "string" },
      trx_ref: { type: "string" },
      bank: { type: "string" },
      bank_code: { type: "string" },
      account_number: { type: "string" },
      amount: { type: "string" },
      account_name: { type: "string" },
      narration: { type: "string" },
      merchant: { type: "string" },
      merchant_ref: { type: "string" },
      expected_fee: { type: "string" },
      confirm: { type: "string" },
      currency: { type: "string", default: "NGN" },
    },
    strict: true,
  });

  if (values.help) {
    usage(0);
  }

  if (!values.cmd) {
    usage(1);
  }

  if (values.cmd === "balance") {
    await cmdBalance();
  } else if (values.cmd === "banks") {
    await cmdBanks(values.search);
  } else if (values.cmd === "lookup") {
    await cmdLookup(values);
  } else if (values.cmd === "transfer-status") {
    await cmdTransferStatus(values);
  } else if (values.cmd === "transfer") {
    await cmdTransfer(values, "bank");
  } else if (values.cmd === "transfer-merchant") {
    await cmdTransfer(values, "merchant");
  } else {
    fail(`Unsupported --cmd value: ${values.cmd}`);
  }
}

if (isMainModule()) {
  await main();
}
