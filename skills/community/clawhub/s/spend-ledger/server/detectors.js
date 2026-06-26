/**
 * Payment detector registry.
 *
 * Each detector examines a tool call result and returns either null (no payment
 * detected) or a partial transaction object with whatever fields it can extract.
 *
 * Detectors are tried in order. The first match wins.
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { loadCachedPatterns } from "./patterns-sync.js";

/**
 * @typedef {object} DetectedPayment
 * @property {object} [service] - { url, name, category }
 * @property {object} [amount]  - { value, currency, chain }
 * @property {string} [tx_hash]
 * @property {string} [idempotency_key]
 * @property {string} [tool_name]
 * @property {string} [tool_args_summary]
 * @property {string} [status]
 * @property {string|null} [failure_type] - null | "pre_payment" | "post_payment"
 */

function tryParseJSON(str) {
  if (typeof str !== "string") return null;
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
}

function dig(obj, path) {
  const parts = path.split(".");
  let cur = obj;
  for (const p of parts) {
    if (cur == null || typeof cur !== "object") return undefined;
    cur = cur[p];
  }
  return cur;
}

function toStr(val) {
  return typeof val === "string" ? val : JSON.stringify(val || "");
}

// --- Argument scanning ---

/**
 * Monetary/payment keywords to look for in tool arguments.
 * Returns true if args contain strong payment signals.
 */
const MONETARY_KEYS = /\b(amount|price|total|cost|fee|subtotal|tip|amount_in_cents)\b/i;
const CURRENCY_KEYS = /\b(currency|usd|eur|btc|eth|usdc|usdt|sol|matic)\b/i;
const RECIPIENT_KEYS = /\b(recipient|payee|beneficiary|wallet_address|to_address|iban|account_number)\b/i;
const PAYMENT_METHOD_KEYS = /\b(payment_method|card|token|pm_|card_)\b/i;

function hasPaymentArgs(argsStr) {
  const hasMonetary = MONETARY_KEYS.test(argsStr);
  const hasCurrency = CURRENCY_KEYS.test(argsStr);
  const hasRecipient = RECIPIENT_KEYS.test(argsStr);
  const hasMethod = PAYMENT_METHOD_KEYS.test(argsStr);
  // Need monetary + at least one other signal
  return hasMonetary && (hasCurrency || hasRecipient || hasMethod);
}

/**
 * Strip query parameters and fragment from a URL before storing it.
 * Prevents accidental capture of API keys or tokens passed as query params.
 */
function sanitizeUrl(raw) {
  if (!raw) return null;
  try {
    const u = new URL(raw);
    u.search = "";
    u.hash = "";
    return u.href;
  } catch {
    return raw.replace(/[?#].*$/, "");
  }
}

/**
 * Extract common payment fields from both args and results.
 */
function extractCommonFields(argsStr, result) {
  const urlMatch = argsStr.match(/https?:\/\/\S+/);
  const amount =
    dig(result, "amount") ||
    dig(result, "payment.amount") ||
    dig(result, "total") ||
    dig(result, "cost") ||
    dig(result, "price");
  const txHash =
    dig(result, "tx_hash") ||
    dig(result, "transaction") ||
    dig(result, "hash") ||
    dig(result, "signature") ||
    dig(result, "payment.tx_hash") ||
    dig(result, "receipt.hash");
  const idempotencyKey =
    dig(result, "idempotency_key") ||
    dig(result, "idempotency") ||
    dig(result, "request_id");
  const currency =
    dig(result, "currency") ||
    dig(result, "payment.currency") ||
    "USDC";
  const chain =
    dig(result, "chain") ||
    dig(result, "network") ||
    null;

  // Failure type detection
  let status = "confirmed";
  let failureType = null;
  const resultStatus = dig(result, "status");
  if (resultStatus === "failed" || resultStatus === "error") {
    status = "failed";
    // If there's a tx_hash, payment went through but something else failed
    failureType = txHash ? "post_payment" : "pre_payment";
  }

  return {
    url: sanitizeUrl(urlMatch?.[0]),
    amount: String(amount || "0"),
    currency,
    chain,
    txHash: txHash ? String(txHash) : null,
    idempotencyKey: idempotencyKey ? String(idempotencyKey) : null,
    status,
    failureType,
  };
}

// --- Individual detectors ---

function detectAgentWalletCli(toolName, toolArgs, toolResult) {
  const nameMatch = /agent-wallet-cli|^wallet$/i.test(toolName);
  const argsStr = toStr(toolArgs);
  const hasX402 = /\bx402\b/i.test(argsStr);

  if (!nameMatch || !hasX402) return null;

  const result = tryParseJSON(toolResult) || {};
  const maxAmountMatch = argsStr.match(/--max-amount\s+([0-9.]+)/);
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url),
      category: null,
    },
    amount: {
      value: common.amount !== "0" ? common.amount : String(maxAmountMatch?.[1] || "0"),
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: "agent-wallet-cli",
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

function detectV402(toolName, toolArgs, toolResult) {
  const argsStr = toStr(toolArgs);
  const nameMatch = /v402/i.test(toolName) || /v402/i.test(argsStr);

  if (!nameMatch) return null;

  const result = tryParseJSON(toolResult) || {};
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url),
      category: null,
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: "v402",
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

function detectClawRouter(toolName, toolArgs, toolResult) {
  const result = tryParseJSON(toolResult) || {};

  const nameMatch = /clawrouter/i.test(toolName);
  const hasCost = dig(result, "cost") != null || dig(result, "price") != null;

  // Require the tool name to match. cost/price fields alone are too broad
  // (many non-payment tools return price data without charging anything).
  if (!nameMatch) return null;

  const argsStr = toStr(toolArgs);
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: null,
      name: "ClawRouter",
      category: "llm-routing",
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: toolName || "ClawRouter",
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

function detectPaymentSkill(toolName, toolArgs, toolResult) {
  const argsStr = toStr(toolArgs);
  const nameMatch = /payment-skill|payment_skill|^pay$/i.test(toolName) || /payment-skill/i.test(argsStr);

  if (!nameMatch) return null;

  const result = tryParseJSON(toolResult) || {};
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url),
      category: null,
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: "payment-skill",
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

function detectGenericX402(toolName, toolArgs, toolResult) {
  const resultStr = toStr(toolResult);

  const hasPaymentHeader = /X-PAYMENT-RESPONSE/i.test(resultStr);
  const hasX402Body = /"x402"/i.test(resultStr) || /payment_required.*paid/i.test(resultStr);

  if (!hasPaymentHeader && !hasX402Body) return null;

  const result = tryParseJSON(toolResult) || {};
  const argsStr = toStr(toolArgs);
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url),
      category: null,
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: toolName || "unknown",
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

const CRYPTO_WALLET_TOOL_NAMES =
  /\b(solana_transfer|sol_transfer|send_usdc|send_sol|transfer_token|transfer_spl|crypto_send|wallet_send|wallet_transfer|send_transaction|transfer_funds)\b/i;

function detectCryptoWallet(toolName, toolArgs, toolResult) {
  if (!CRYPTO_WALLET_TOOL_NAMES.test(toolName)) return null;

  const result = tryParseJSON(toolResult) || {};
  const argsStr = toStr(toolArgs);
  const args = typeof toolArgs === "object" ? toolArgs : tryParseJSON(argsStr) || {};
  const common = extractCommonFields(argsStr, result);

  // Prefer amount from args when result doesn't carry it (common for wallet tools)
  let amountVal = common.amount !== "0" ? common.amount
    : String(dig(args, "amount") || dig(args, "value") || dig(args, "lamports") || "0");

  // Convert lamports → SOL if no explicit currency and value looks like lamports
  const currency = String(dig(args, "currency") || dig(args, "token") || dig(args, "mint") || common.currency);
  if (parseFloat(amountVal) > 1_000_000 && /unknown|sol/i.test(currency) && !dig(args, "currency")) {
    amountVal = String(parseFloat(amountVal) / 1e9);
  }

  // Recipient address for service name
  const recipient = String(dig(args, "to") || dig(args, "recipient") || dig(args, "destination") || "");
  const shortRecipient = recipient.length > 8 ? `${recipient.slice(0, 4)}…${recipient.slice(-4)}` : recipient;

  return {
    service: {
      url: common.url,
      name: shortRecipient || "crypto-wallet",
      category: "crypto",
    },
    amount: {
      value: amountVal,
      currency: currency || "SOL",
      chain: common.chain || "solana",
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: toolName,
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
  };
}

/**
 * Heuristic detector: catches common payment tool names and argument patterns
 * that don't match any specific detector above. Fires last before the catch-all.
 */
const PAYMENT_TOOL_NAMES =
  /\b(stripe|paypal|venmo|square|shopify|braintree|crypto_transfer|send_money|donate|checkout|purchase|buy|invoice|subscribe|billing)\b/i;

const PAYMENT_RESULT_MARKERS =
  /\b(succeeded|completed|charged|payment.confirmed|transaction.id|txid|receipt|transaction\s+confirmed|payment\s+confirmed)\b/i;

// Common transaction ID patterns — includes Solana base58 signatures (87-88 chars)
const TX_ID_PATTERNS =
  /\b(ch_[a-z0-9]{20,}|pi_[a-z0-9]{20,}|pm_[a-z0-9]{20,}|paypal_tx_\w+|0x[a-f0-9]{64}|txn_[a-z0-9]+|[1-9A-HJ-NP-Za-km-z]{87,88})\b/;

// Amount + currency extracted from plain text like "Amount: 0.5 USDC" or "Sent 1.2 ETH"
const PLAIN_TEXT_AMOUNT =
  /(?:amount|sent|sending|transferred?|paid?|payment(?:\s+of)?)[\s:]*([0-9]+(?:\.[0-9]+)?)\s*([A-Z]{2,6})\b/i;

function detectHeuristic(toolName, toolArgs, toolResult) {
  const argsStr = toStr(toolArgs);
  const resultStr = toStr(toolResult);

  const nameMatch = PAYMENT_TOOL_NAMES.test(toolName);
  const argsMatch = hasPaymentArgs(argsStr);
  const resultMatch = PAYMENT_RESULT_MARKERS.test(resultStr);
  // Also check result for monetary signals (handles exec-wrapped payment scripts)
  const resultHasPaymentSignals = hasPaymentArgs(resultStr);

  // Match if: named payment tool, OR args+result confirm, OR result alone is conclusive
  if (!nameMatch && !(argsMatch && resultMatch) && !(resultHasPaymentSignals && resultMatch)) return null;

  const result = tryParseJSON(toolResult) || {};
  const common = extractCommonFields(argsStr, result);

  // For non-JSON results, extract amount/currency from plain text
  if (common.amount === "0") {
    const textMatch = PLAIN_TEXT_AMOUNT.exec(resultStr) || PLAIN_TEXT_AMOUNT.exec(argsStr);
    if (textMatch) {
      common.amount = textMatch[1];
      common.currency = textMatch[2].toUpperCase();
    }
  }

  // For heuristic matches, require a non-zero amount to avoid false positives
  // (e.g., a price lookup API that returns prices without charging)
  if (common.amount === "0" && !nameMatch) return null;

  // Try to extract tx ID from result via regex if not found structurally
  let txHash = common.txHash;
  if (!txHash) {
    const txIdMatch = resultStr.match(TX_ID_PATTERNS);
    if (txIdMatch) txHash = txIdMatch[0];
  }

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url) || toolName,
      category: null,
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: toolName,
    tool_args_summary: truncate(argsStr, 200),
    // Heuristic matches have no formal payment signal — mark as unverified
    // so the owner can review rather than treating them as confirmed spend.
    status: common.failureType ? common.status : "unverified",
    failure_type: common.failureType,
    _detector: "heuristic",
  };
}

// --- Helpers ---

function extractServiceName(url) {
  if (!url) return "unknown";
  try {
    const host = new URL(url).hostname;
    return host.replace(/^www\./, "").replace(/\.(com|io|ai|xyz|org|net)$/, "");
  } catch {
    return "unknown";
  }
}

function truncate(str, maxLen) {
  if (!str) return null;
  return str.length > maxLen ? str.slice(0, maxLen) + "…" : str;
}

// --- User-defined tracked tools ---

const SUGGESTIONS_PATH = resolve(
  process.env.SPEND_LEDGER_SUGGESTIONS ||
    new URL("../data/tracked-tools.json", import.meta.url).pathname
);

/**
 * Load user-tracked tool patterns from disk.
 * Returns an array of { tool_name_pattern, description, submitted }.
 */
function loadTrackedTools() {
  if (!existsSync(SUGGESTIONS_PATH)) return [];
  try {
    return JSON.parse(readFileSync(SUGGESTIONS_PATH, "utf-8"));
  } catch {
    return [];
  }
}

/**
 * Detector for user-defined tracked tools. Users can mark tools as payment-related
 * via the dashboard, and this detector will catch them.
 */
function detectUserTracked(toolName, toolArgs, toolResult) {
  const local = loadTrackedTools();
  const community = loadCachedPatterns();

  // Merge: local patterns take priority — community fills in the rest
  const localPatterns = new Set(local.map((t) => t.tool_name_pattern));
  const tracked = [
    ...local,
    ...community.filter((c) => !localPatterns.has(c.tool_name_pattern)),
  ];

  if (!tracked.length) return null;

  const match = tracked.find((t) => {
    try {
      return new RegExp(t.tool_name_pattern, "i").test(toolName);
    } catch {
      return toolName.toLowerCase() === t.tool_name_pattern.toLowerCase();
    }
  });

  if (!match) return null;

  const argsStr = toStr(toolArgs);
  const result = tryParseJSON(toolResult) || {};
  const common = extractCommonFields(argsStr, result);

  return {
    service: {
      url: common.url,
      name: extractServiceName(common.url) || toolName,
      category: match.category || null,
    },
    amount: {
      value: common.amount,
      currency: common.currency,
      chain: common.chain,
    },
    tx_hash: common.txHash,
    idempotency_key: common.idempotencyKey,
    tool_name: toolName,
    tool_args_summary: truncate(argsStr, 200),
    status: common.status,
    failure_type: common.failureType,
    _detector: "user-tracked",
  };
}

// --- Registry ---

const detectors = [
  detectUserTracked,    // User-defined patterns first (highest priority)
  detectAgentWalletCli,
  detectV402,
  detectClawRouter,
  detectPaymentSkill,
  detectCryptoWallet,   // Solana / crypto wallet tools
  detectHeuristic,      // Broad heuristic before generic x402
  detectGenericX402,    // Catch-all last
];

/**
 * Run all detectors against a tool call result.
 *
 * @param {string} toolName - The name of the tool that was called
 * @param {string|object} toolArgs - The arguments passed to the tool
 * @param {string|object} toolResult - The result returned by the tool
 * @returns {DetectedPayment|null} Extracted payment info, or null if no payment detected
 */
export function detectPayment(toolName, toolArgs, toolResult) {
  for (const detect of detectors) {
    const result = detect(toolName, toolArgs, toolResult);
    if (result) return result;
  }
  return null;
}

// Re-export for use in server
export { hasPaymentArgs, SUGGESTIONS_PATH };
