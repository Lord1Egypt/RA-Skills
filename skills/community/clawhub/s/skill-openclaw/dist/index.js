"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/index.ts
var index_exports = {};
__export(index_exports, {
  COMMANDS: () => COMMANDS,
  CONFIG_DIR: () => CONFIG_DIR,
  CONFIG_FILE_NAME: () => CONFIG_FILE_NAME,
  clearConfig: () => clearConfig,
  hasConfig: () => hasConfig,
  readConfig: () => readConfig,
  runSetup: () => runSetup,
  translateError: () => translateError,
  translateToolError: () => translateToolError,
  validateApiKey: () => validateApiKey,
  validateApiSecret: () => validateApiSecret,
  writeConfig: () => writeConfig
});
module.exports = __toCommonJS(index_exports);

// src/onboarding.ts
var import_oris_sdk = require("oris-sdk");

// src/config.ts
var fs = __toESM(require("fs/promises"));
var path = __toESM(require("path"));
var CONFIG_DIR = path.join(
  process.env["HOME"] || process.env["USERPROFILE"] || "~",
  ".openclaw"
);
var CONFIG_FILE_NAME = "config.json";
function configFilePath() {
  return path.join(CONFIG_DIR, CONFIG_FILE_NAME);
}
async function readOpenClawConfig() {
  try {
    const raw = await fs.readFile(configFilePath(), "utf-8");
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === "ENOENT") return {};
    throw err;
  }
}
async function writeOpenClawConfig(config) {
  await fs.mkdir(CONFIG_DIR, { recursive: true, mode: 448 });
  await fs.writeFile(configFilePath(), JSON.stringify(config, null, 2), {
    encoding: "utf-8",
    mode: 384
  });
}
async function writeConfig(data) {
  const existing = await readOpenClawConfig();
  existing.oris = {
    ...data,
    configuredAt: (/* @__PURE__ */ new Date()).toISOString()
  };
  await writeOpenClawConfig(existing);
}
async function readConfig() {
  const config = await readOpenClawConfig();
  return config.oris ?? null;
}
async function hasConfig() {
  const config = await readOpenClawConfig();
  return config.oris !== void 0 && config.oris !== null;
}
async function clearConfig() {
  try {
    const config = await readOpenClawConfig();
    delete config.oris;
    await writeOpenClawConfig(config);
  } catch (err) {
    if (err.code === "ENOENT") return;
    throw err;
  }
}

// src/errors.ts
var ERROR_MESSAGES = {
  // Auth
  "auth.invalid_key": "The API key is invalid or has been revoked. Generate a new key at useoris.finance.",
  "auth.invalid_signature": "Request signature verification failed. Check that your API secret is correct.",
  "auth.expired_timestamp": "Request timestamp is outside the 30-second tolerance window. Check your system clock.",
  "auth.duplicate_nonce": "Duplicate request detected. This payment was already submitted.",
  "auth.rate_limited": "Rate limit exceeded. Wait a moment before retrying.",
  // KYA
  "kya.not_verified": "Agent is not verified. Complete KYA verification at useoris.finance before making payments.",
  "kya.suspended": "Agent has been suspended. Contact support at sales@fluxa.ventures.",
  "kya.revoked": "Agent credentials have been revoked. Register a new agent.",
  "kya.insufficient_level": "Your KYA tier does not permit this operation. Check your tier limits with the tier command.",
  // Policy
  "policy.max_per_transaction": "Payment exceeds the per-transaction limit. Reduce the amount or update your spending policy.",
  "policy.max_daily": "Daily spending limit reached. Wait until tomorrow or adjust your policy at useoris.finance.",
  "policy.max_monthly": "Monthly spending limit reached. Adjust your policy at useoris.finance.",
  "policy.chain_not_allowed": "This blockchain network is not allowed by your spending policy.",
  "policy.counterparty_blocked": "The recipient address is on your blocklist.",
  "policy.escalation_required": "This payment requires manual approval. Use the approve command to proceed.",
  // Compliance
  "compliance.sanctions_hit": "The recipient address is flagged by sanctions screening. This payment cannot proceed.",
  "compliance.high_risk": "Compliance screening flagged this transaction as high risk. Review required.",
  "compliance.service_unavailable": "Compliance screening service is temporarily unavailable. The system is fail-closed and will not process payments until screening is restored.",
  // Balance
  "balance.insufficient": "Insufficient balance. Fund your wallet using the fund command.",
  "balance.wallet_frozen": "Wallet is frozen. Contact support at sales@fluxa.ventures.",
  // Network
  "network.timeout": "Request timed out. The Oris API may be experiencing high load. Try again in a few seconds.",
  "network.unavailable": "Cannot reach the Oris API. Check your internet connection."
};
var HTTP_STATUS_MESSAGES = {
  400: "Invalid request. Check the command parameters.",
  401: 'Authentication failed. Run "openclaw run oris setup" to reconfigure credentials.',
  403: "Access denied. Your account may not have permission for this operation.",
  404: "Resource not found. The specified agent, wallet, or payment does not exist.",
  409: "Conflict. This operation has already been performed.",
  422: "Validation error. One or more parameters are invalid.",
  429: "Too many requests. Wait a moment before retrying.",
  500: "Oris server error. Try again shortly. If the problem persists, check status.useoris.finance.",
  502: "Oris API is temporarily unreachable. Try again in a few seconds.",
  503: "Oris API is under maintenance. Try again shortly."
};
var OPERATION_CONTEXT = {
  register: "Failed to register the agent.",
  createWallet: "Failed to create the wallet.",
  setPolicy: "Failed to set the spending policy.",
  pay: "Payment failed.",
  checkBalance: "Failed to retrieve balance.",
  getSpending: "Failed to retrieve spending summary.",
  findService: "Marketplace search failed.",
  approvePending: "Failed to approve the payment.",
  fiatOnramp: "Fiat on-ramp failed.",
  fiatOfframp: "Fiat off-ramp failed.",
  exchangeRate: "Failed to retrieve exchange rate.",
  crossChainQuote: "Cross-chain quote failed.",
  placeOrder: "Marketplace order failed.",
  getTierInfo: "Failed to retrieve tier information.",
  generateAttestation: "Attestation generation failed.",
  promotionStatus: "Failed to check promotion status."
};
function translateError(operation, err) {
  const context = OPERATION_CONTEXT[operation] || "Operation failed.";
  if (err instanceof Error) {
    const orisErr = err;
    if (orisErr.errorCode && ERROR_MESSAGES[orisErr.errorCode]) {
      return `${context} ${ERROR_MESSAGES[orisErr.errorCode]}`;
    }
    if (orisErr.statusCode && HTTP_STATUS_MESSAGES[orisErr.statusCode]) {
      return `${context} ${HTTP_STATUS_MESSAGES[orisErr.statusCode]}`;
    }
    if (err.message.includes("ECONNREFUSED") || err.message.includes("ENOTFOUND")) {
      return `${context} Cannot reach the Oris API. Check your internet connection.`;
    }
    if (err.message.includes("ETIMEDOUT") || err.message.includes("timeout")) {
      return `${context} Request timed out. Try again in a few seconds.`;
    }
    return `${context} ${err.message}`;
  }
  return `${context} An unexpected error occurred.`;
}
function translateToolError(toolName, error) {
  const code = error["code"] || "";
  const message = error["message"] || "";
  const toolToOp = {
    oris_pay: "pay",
    oris_check_balance: "checkBalance",
    oris_get_spending: "getSpending",
    oris_find_service: "findService",
    oris_approve_pending: "approvePending",
    oris_fiat_onramp: "fiatOnramp",
    oris_fiat_offramp: "fiatOfframp",
    oris_exchange_rate: "exchangeRate",
    oris_cross_chain_quote: "crossChainQuote",
    oris_place_order: "placeOrder",
    oris_get_tier_info: "getTierInfo",
    oris_generate_attestation: "generateAttestation",
    oris_promotion_status: "promotionStatus"
  };
  const operation = toolToOp[toolName] || toolName;
  const context = OPERATION_CONTEXT[operation] || "Operation failed.";
  if (code && ERROR_MESSAGES[code]) {
    return `${context} ${ERROR_MESSAGES[code]}`;
  }
  if (message) {
    return `${context} ${message}`;
  }
  return `${context} An unexpected error occurred.`;
}

// src/onboarding.ts
var API_KEY_PREFIX = "oris_sk_live_";
var API_SECRET_PREFIX = "oris_ss_live_";
var MIN_KEY_LENGTH = 24;
var MIN_SECRET_LENGTH = 24;
function validateApiKey(key) {
  return key.startsWith(API_KEY_PREFIX) && key.length >= MIN_KEY_LENGTH;
}
function validateApiSecret(secret) {
  return secret.startsWith(API_SECRET_PREFIX) && secret.length >= MIN_SECRET_LENGTH;
}
async function runSetup(input, options) {
  const configured = await hasConfig();
  if (configured && !options?.force) {
    throw new Error(
      "Oris is already configured. Use --force to reconfigure."
    );
  }
  if (!validateApiKey(input.apiKey)) {
    throw new Error(
      `Invalid API key format. Keys must start with "${API_KEY_PREFIX}" and be at least ${MIN_KEY_LENGTH} characters.`
    );
  }
  if (!validateApiSecret(input.apiSecret)) {
    throw new Error(
      `Invalid API secret format. Secrets must start with "${API_SECRET_PREFIX}" and be at least ${MIN_SECRET_LENGTH} characters.`
    );
  }
  let registration;
  try {
    const agent = new import_oris_sdk.Agent({
      apiKey: input.apiKey,
      apiSecret: input.apiSecret
    });
    registration = await agent.register({
      externalAgentId: "openclaw-agent",
      agentName: "OpenClaw Agent",
      agentType: "autonomous",
      platform: "custom",
      declaredCapabilities: ["payments", "marketplace", "compliance"],
      operatingChains: ["base"]
    });
  } catch (err) {
    throw new Error(translateError("register", err));
  }
  const registeredAgent = new import_oris_sdk.Agent({
    apiKey: input.apiKey,
    apiSecret: input.apiSecret,
    agentId: registration.id
  });
  let wallet;
  try {
    wallet = await registeredAgent.createWallet({ chain: "base" });
  } catch (err) {
    throw new Error(translateError("createWallet", err));
  }
  try {
    await registeredAgent.setPolicy({
      policyName: "openclaw-default",
      maxPerTx: 50,
      maxDaily: 200,
      enforcementMode: "enforce"
    });
  } catch (err) {
    throw new Error(translateError("setPolicy", err));
  }
  await writeConfig({
    apiKey: input.apiKey,
    apiSecret: input.apiSecret,
    agentId: registration.id,
    walletAddress: wallet.smart_account_address || "",
    chain: "base"
  });
  return {
    agentId: registration.id,
    walletAddress: wallet.smart_account_address || "",
    chain: "base",
    tier: `KYA Level ${registration.kya_level}`
  };
}

// src/commands.ts
var COMMANDS = [
  {
    name: "pay",
    toolName: "oris_pay",
    description: "Send a payment to a recipient. Use this when you need to pay for a service, purchase something, or transfer funds."
  },
  {
    name: "balance",
    toolName: "oris_check_balance",
    description: "Check how much funds are available in your wallet before making a payment."
  },
  {
    name: "spending",
    toolName: "oris_get_spending",
    description: "Review spending history and remaining budget for today, this week, or this month."
  },
  {
    name: "find-service",
    toolName: "oris_find_service",
    description: "Search the Oris marketplace for AI agent services you can hire and pay automatically."
  },
  {
    name: "approve",
    toolName: "oris_approve_pending",
    description: "Approve a pending payment that was escalated because it exceeded spending policy thresholds."
  },
  {
    name: "fund",
    toolName: "oris_fiat_onramp",
    description: "Convert fiat currency (USD, EUR, GBP) to USDC or another stablecoin to fund your wallet."
  },
  {
    name: "withdraw",
    toolName: "oris_fiat_offramp",
    description: "Withdraw stablecoins to a bank account as fiat currency."
  },
  {
    name: "rate",
    toolName: "oris_exchange_rate",
    description: "Check the current exchange rate between a fiat currency and a stablecoin, including fees."
  },
  {
    name: "cross-chain",
    toolName: "oris_cross_chain_quote",
    description: "Get a price quote for transferring stablecoins between different blockchain networks."
  },
  {
    name: "order",
    toolName: "oris_place_order",
    description: "Purchase a service from the agent marketplace with escrow-backed payment."
  },
  {
    name: "tier",
    toolName: "oris_get_tier_info",
    description: "Check your verification tier, spending limits, and current usage against those limits."
  },
  {
    name: "attest",
    toolName: "oris_generate_attestation",
    description: "Generate a zero-knowledge proof of your KYA verification status for on-chain use."
  },
  {
    name: "promotion",
    toolName: "oris_promotion_status",
    description: "Check whether you meet the requirements for promotion to the next KYA tier."
  }
];
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  COMMANDS,
  CONFIG_DIR,
  CONFIG_FILE_NAME,
  clearConfig,
  hasConfig,
  readConfig,
  runSetup,
  translateError,
  translateToolError,
  validateApiKey,
  validateApiSecret,
  writeConfig
});
