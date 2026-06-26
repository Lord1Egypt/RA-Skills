#!/usr/bin/env node
const BASE = "https://api.wise.com";
const token = process.env.WISE_API_TOKEN;
if (!token) throw new Error("Missing WISE_API_TOKEN");

const [,, cmd, ...args] = process.argv;
const rawOutput = args.includes("--raw");

const getArg = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};

const getNumArg = (name, { required = false, defaultValue } = {}) => {
  const v = getArg(name);
  if (v === undefined || v === null || v === "") {
    if (required) throw new Error(`Missing ${name}`);
    return defaultValue;
  }
  const n = Number(v);
  if (!Number.isFinite(n)) throw new Error(`Invalid number for ${name}`);
  return n;
};

const SENSITIVE_KEYS = new Set([
  "firstName", "lastName", "dateOfBirth", "phoneNumber", "avatar", "email", "address",
  "firstNameInKana", "lastNameInKana", "accountHolderName", "accountNumber", "iban",
  "bic", "bicSwift", "bankCode", "sortCode", "routingNumber", "abartn", "clabe",
  "ifsc", "cpf", "nationalId", "taxId"
]);

const LOCALIZED_SENSITIVE_KEYS = new Set(["firstName", "lastName", "firstNameInKana", "lastNameInKana"]);

function redactValue(value) {
  if (Array.isArray(value)) return value.map(redactValue);
  if (!value || typeof value !== "object") return value;

  const out = {};
  for (const [k, v] of Object.entries(value)) {
    if (SENSITIVE_KEYS.has(k)) {
      out[k] = "[REDACTED]";
      continue;
    }

    if (k === "localizedInformation" && Array.isArray(v)) {
      out[k] = v.map((entry) => {
        if (entry && typeof entry === "object" && LOCALIZED_SENSITIVE_KEYS.has(String(entry.key))) {
          return { ...entry, value: "[REDACTED]" };
        }
        return redactValue(entry);
      });
      continue;
    }

    out[k] = redactValue(v);
  }
  return out;
}

function errorSummary(status, text) {
  try {
    const parsed = JSON.parse(text);
    const msg = parsed?.message || parsed?.error || "request failed";
    return `Wise API ${status}: ${msg}`;
  } catch {
    return `Wise API ${status}: request failed`;
  }
}

async function apiGet(path, params = {}) {
  const url = new URL(BASE + path);
  Object.entries(params).forEach(([k, v]) => v != null && v !== "" && url.searchParams.set(k, String(v)));

  const r = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/json"
    }
  });

  const text = await r.text();
  if (!r.ok) throw new Error(errorSummary(r.status, text));
  return text ? JSON.parse(text) : null;
}

function printJson(value, { redact = false } = {}) {
  const out = redact && !rawOutput ? redactValue(value) : value;
  console.log(JSON.stringify(out));
}

switch (cmd) {
  case "list_profiles": {
    const data = await apiGet("/v1/profiles");
    printJson(data, { redact: true });
    break;
  }

  case "get_profile": {
    const id = getNumArg("--profile-id", { required: true });
    const data = await apiGet(`/v1/profiles/${id}`);
    printJson(data, { redact: true });
    break;
  }

  case "list_balances": {
    const id = getNumArg("--profile-id", { required: true });
    const types = getArg("--types") || "STANDARD";
    const data = await apiGet(`/v4/profiles/${id}/balances`, { types });
    printJson(data);
    break;
  }

  case "get_balance": {
    const profileId = getNumArg("--profile-id", { required: true });
    const balanceId = getNumArg("--balance-id", { required: true });
    const data = await apiGet(`/v4/profiles/${profileId}/balances/${balanceId}`);
    printJson(data);
    break;
  }

  case "get_exchange_rate": {
    const source = (getArg("--source") || "").toUpperCase();
    const target = (getArg("--target") || "").toUpperCase();
    if (!source || !target) throw new Error("Missing --source/--target");
    const data = await apiGet("/v1/rates", { source, target });
    printJson(data);
    break;
  }

  case "get_exchange_rate_history": {
    const source = (getArg("--source") || "").toUpperCase();
    const target = (getArg("--target") || "").toUpperCase();
    const from = getArg("--from") || "";
    const to = getArg("--to") || "";
    const group = getArg("--group") || "day";
    if (!source || !target || !from || !to) throw new Error("Missing --source/--target/--from/--to");
    if (!["day", "hour", "minute"].includes(group)) throw new Error("--group must be one of: day, hour, minute");
    const data = await apiGet("/v1/rates", { source, target, from, to, group });
    printJson(data);
    break;
  }

  case "get_temporary_quote": {
    const source = (getArg("--source") || "").toUpperCase();
    const target = (getArg("--target") || "").toUpperCase();
    const sourceAmount = getArg("--source-amount");
    const targetAmount = getArg("--target-amount");
    if (!source || !target) throw new Error("Missing --source/--target");
    if (!sourceAmount && !targetAmount) throw new Error("Provide --source-amount or --target-amount");
    if (sourceAmount && targetAmount) throw new Error("Provide only one of --source-amount or --target-amount");
    const data = await apiGet("/v1/quotes", {
      source,
      target,
      rateType: "FIXED",
      sourceAmount,
      targetAmount
    });
    printJson(data);
    break;
  }

  case "get_quote": {
    const quoteId = getNumArg("--quote-id", { required: true });
    const data = await apiGet(`/v1/quotes/${quoteId}`);
    printJson(data);
    break;
  }

  case "list_recipients": {
    const profileId = getNumArg("--profile-id", { required: true });
    const currency = (getArg("--currency") || "").toUpperCase() || undefined;
    const data = await apiGet("/v1/accounts", { profile: profileId, currency });
    printJson(data, { redact: true });
    break;
  }

  case "get_recipient": {
    const accountId = getNumArg("--account-id", { required: true });
    const data = await apiGet(`/v1/accounts/${accountId}`);
    printJson(data, { redact: true });
    break;
  }

  case "get_account_requirements": {
    const source = (getArg("--source") || "").toUpperCase();
    const target = (getArg("--target") || "").toUpperCase();
    const sourceAmount = getNumArg("--source-amount", { required: true });
    if (!source || !target) throw new Error("Missing --source/--target");
    const data = await apiGet("/v1/account-requirements", { source, target, sourceAmount });
    printJson(data);
    break;
  }

  case "list_transfers": {
    const profileId = getNumArg("--profile-id", { required: true });
    const status = getArg("--status");
    const createdDateStart = getArg("--created-date-start");
    const createdDateEnd = getArg("--created-date-end");
    const limit = getNumArg("--limit", { defaultValue: 10 });
    const offset = getNumArg("--offset", { defaultValue: 0 });
    const data = await apiGet("/v1/transfers", {
      profile: profileId,
      status,
      createdDateStart,
      createdDateEnd,
      limit,
      offset
    });
    printJson(data, { redact: true });
    break;
  }

  case "get_transfer": {
    const transferId = getNumArg("--transfer-id", { required: true });
    const data = await apiGet(`/v1/transfers/${transferId}`);
    printJson(data, { redact: true });
    break;
  }

  case "get_delivery_estimate": {
    const transferId = getNumArg("--transfer-id", { required: true });
    const data = await apiGet(`/v1/delivery-estimates/${transferId}`);
    printJson(data);
    break;
  }

  default:
    throw new Error(
      "Usage: wise_readonly.mjs <list_profiles|get_profile|list_balances|get_balance|get_exchange_rate|get_exchange_rate_history|get_temporary_quote|get_quote|list_recipients|get_recipient|get_account_requirements|list_transfers|get_transfer|get_delivery_estimate> [--raw] ..."
    );
}
