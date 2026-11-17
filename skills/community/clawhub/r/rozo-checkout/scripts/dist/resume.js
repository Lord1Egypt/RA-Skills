#!/usr/bin/env node
import { createRequire as __rozoCreateRequire } from 'node:module';
import { fileURLToPath as __rozoFileURLToPath } from 'node:url';
import { dirname as __rozoDirname } from 'node:path';
const require = __rozoCreateRequire(import.meta.url);
const __filename = __rozoFileURLToPath(import.meta.url);
const __dirname = __rozoDirname(__filename);

// scripts/src/lib/support.mjs
var SUPPORT = Object.freeze({
  email: "hi@rozo.ai",
  x: "https://x.com/ROZOai",
  discord: "https://discord.gg/EfWejgTbuU"
});
var SUPPORT_TEXT = `Need help? Email ${SUPPORT.email}, or reach ROZO on X ${SUPPORT.x} or Discord ${SUPPORT.discord}.`;
var BULK_DOCS_URL = "https://docs.rozo.ai/products/checkout/bulk-and-agents";
var BULK_HINT_TEXT = `Buying regularly or for others? ${BULK_DOCS_URL}`;

// scripts/src/lib/output.mjs
var PUBLIC_SUPPORT_URLS = /* @__PURE__ */ new Set([SUPPORT.x, SUPPORT.discord]);
var EXIT_OK = 0;
var EXIT_ERROR = 1;
var EXIT_USAGE = 2;
function redact(text) {
  if (text === null || text === void 0) return text;
  let s = typeof text === "string" ? text : String(text);
  s = s.replace(/0x[0-9a-fA-F]{64}/g, "0x<redacted>");
  s = s.replace(/\b[0-9a-fA-F]{64}\b/g, "<redacted>");
  s = s.replace(/\b[1-9A-HJ-NP-Za-km-z]{80,90}\b/g, "<redacted>");
  s = s.replace(/\[(?:\s*\d{1,3}\s*,){40,}\s*\d{1,3}\s*\]/g, "[<redacted>]");
  s = s.replace(/\b([a-zA-Z][a-zA-Z0-9+.-]*):\/\/([^\s"'<>]+)/g, (m, scheme, rest) => {
    if (PUBLIC_SUPPORT_URLS.has(m.replace(/[.,;:!?)]+$/, ""))) return m;
    const withoutUserinfo = rest.includes("@") ? rest.slice(rest.indexOf("@") + 1) : rest;
    const host = withoutUserinfo.split(/[/?#]/)[0];
    const hadMore = withoutUserinfo.length > host.length;
    return `${scheme}://${host}${hadMore ? "/<redacted>" : ""}`;
  });
  s = s.replace(/\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}/gi, "$1 <redacted>");
  s = s.replace(/\bak_[A-Za-z0-9_-]{8,}/g, "ak_<redacted>");
  s = s.replace(
    /\b(api[-_]?key|apikey|access[-_]?token|auth[-_]?token|secret|token|password|passwd|pwd)\b(\s*[:=]\s*)("?)[A-Za-z0-9._~+/=-]{6,}\3/gi,
    "$1$2<redacted>"
  );
  return s;
}
var PublicHash = class {
  constructor(value) {
    this.value = value;
  }
  toJSON() {
    return this.value;
  }
};
var TX_HASH_VALUE = /^(0x[0-9a-fA-F]{64}|[1-9A-HJ-NP-Za-km-z]{86,88})$/;
function publicHash(value) {
  return typeof value === "string" && TX_HASH_VALUE.test(value) ? new PublicHash(value) : value;
}
var PUBLIC_PAY_PAGE_HOSTS = /* @__PURE__ */ new Set(["invoice.rozo.ai", "checkout.rozo.ai"]);
var PAY_PAGE_ID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function publicPayPage(value) {
  if (typeof value !== "string") return value;
  let u;
  try {
    u = new URL(value);
  } catch {
    return value;
  }
  if (u.protocol !== "https:" || u.username || u.password || u.port || !PUBLIC_PAY_PAGE_HOSTS.has(u.hostname)) return value;
  if (u.pathname !== "/checkout") return value;
  const id = u.searchParams.get("id");
  if (!id || !PAY_PAGE_ID.test(id)) return value;
  return new PublicHash(`https://${u.hostname}/checkout?id=${id.toLowerCase()}`);
}
function redactDeep(value) {
  if (value instanceof PublicHash) return value.value;
  if (typeof value === "string") return redact(value);
  if (Array.isArray(value)) return value.map(redactDeep);
  if (value && typeof value === "object") {
    const out = {};
    for (const [k, v] of Object.entries(value)) {
      if (/priv(ate)?[-_]?key|secret|mnemonic|seed/i.test(k)) {
        out[k] = "<redacted>";
        continue;
      }
      out[k] = redactDeep(v);
    }
    return out;
  }
  return value;
}
var capturing = false;
var EmitSignal = class extends Error {
  constructor(payload, exitCode) {
    super("emit");
    this.payload = payload;
    this.exitCode = exitCode;
  }
};
function formatFailure(err, fallbackCode = "RUNTIME_ERROR") {
  const code = err && err.code || fallbackCode;
  const message = redact(err && err.message || String(err));
  const payload = { success: false, error: { code, message } };
  if (err && err.details) payload.error.details = redactDeep(err.details);
  return payload;
}
function emit(payload, exitCode = EXIT_OK) {
  const redacted = redactDeep(payload);
  if (capturing) throw new EmitSignal(redacted, exitCode);
  process.stdout.write(JSON.stringify(redacted, null, 2) + "\n");
  process.exit(exitCode);
}
function fail(err, fallbackCode = "RUNTIME_ERROR", exitCode = EXIT_ERROR) {
  const payload = formatFailure(err, fallbackCode);
  if (capturing) throw new EmitSignal(payload, exitCode);
  process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
  process.exit(exitCode);
}
function usage(message) {
  fail({ code: "USAGE", message }, "USAGE", EXIT_USAGE);
}
function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === void 0 || next.startsWith("--")) {
        out[key] = true;
      } else {
        out[key] = next;
        i++;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}
var SkillError = class extends Error {
  constructor(code, message, details) {
    super(message);
    this.code = code;
    if (details) this.details = details;
  }
};

// scripts/src/lib/ids.mjs
var UUID_RE = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
function isRozoPaymentId(value) {
  return UUID_RE.test(String(value || "").trim());
}
function maskAddress(address) {
  const s = String(address ?? "").trim();
  if (!s) return "(none)";
  if (s.length <= 12) return s;
  return `${s.slice(0, 6)}...${s.slice(-4)}`;
}
function maskMemo(memo) {
  const s = String(memo ?? "").trim();
  if (!s) return null;
  if (s.length <= 8) return s;
  return `${s.slice(0, 4)}...${s.slice(-3)}`;
}

// scripts/src/lib/version.mjs
import { createRequire } from "node:module";
var PKG_VERSION = (() => {
  const requireFrom = createRequire(import.meta.url);
  for (const candidate of ["../../package.json", "../../../package.json"]) {
    try {
      const pkg = requireFrom(candidate);
      if (pkg?.name === "@rozoai/checkout" && pkg.version) return pkg.version;
    } catch {
    }
  }
  return "0.0.0";
})();

// scripts/src/lib/http.mjs
var DEFAULT_TIMEOUT_MS = 2e4;
var USER_AGENT = `rozo-checkout-skill/${PKG_VERSION}`;
var MAX_RETRIES = 3;
var MAX_TOTAL_WAIT_MS = 12e4;
var FALLBACK_BACKOFF_MS = [2e3, 4e3, 8e3];
var defaultSleep = (ms) => new Promise((r) => setTimeout(r, ms));
function parseRetryAfter(value, now = Date.now()) {
  if (value === null || value === void 0) return null;
  const s = String(value).trim();
  if (!s) return null;
  if (/^\d+(\.\d+)?$/.test(s)) return Math.round(Number(s) * 1e3);
  const at = Date.parse(s);
  if (!Number.isFinite(at)) return null;
  return Math.max(0, at - now);
}
function bodyRetryAfterMs(json) {
  const raw = json?.retryAfterSeconds ?? json?.error?.retryAfterSeconds;
  if (raw === null || raw === void 0 || raw === "") return null;
  const n = Number(raw);
  return Number.isFinite(n) && n >= 0 ? Math.round(n * 1e3) : null;
}
function rateLimitInfo(res) {
  const pick = (name) => res.headers?.get?.(name) ?? null;
  const info = {
    limit: pick("x-ratelimit-limit"),
    remaining: pick("x-ratelimit-remaining"),
    tier: pick("x-ratelimit-tier"),
    scope: pick("x-ratelimit-scope")
  };
  const present = Object.fromEntries(Object.entries(info).filter(([, v]) => v !== null));
  return Object.keys(present).length ? present : null;
}
function parseBody(text) {
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}
async function fetchOnce(method, url, body, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      method,
      headers: {
        accept: "application/json",
        "user-agent": USER_AGENT,
        ...body !== void 0 ? { "content-type": "application/json" } : {}
      },
      body: body !== void 0 ? JSON.stringify(body) : void 0,
      signal: controller.signal
    });
    const text = await res.text();
    return { res, text };
  } catch (err) {
    throw new SkillError(
      err?.name === "AbortError" ? "HTTP_TIMEOUT" : "HTTP_UNREACHABLE",
      `${method} request failed: ${redact(err?.message || String(err))}`,
      { url: redactUrl(url) }
    );
  } finally {
    clearTimeout(timer);
  }
}
async function request(method, url, {
  body,
  timeoutMs = DEFAULT_TIMEOUT_MS,
  sleep = defaultSleep,
  now = Date.now,
  maxTotalWaitMs = MAX_TOTAL_WAIT_MS
} = {}) {
  let waitedMs = 0;
  let retries = 0;
  for (; ; ) {
    const { res, text } = await fetchOnce(method, url, body, timeoutMs);
    const json = parseBody(text);
    if (res.ok) {
      if (json === null) {
        throw new SkillError("HTTP_BAD_JSON", "Endpoint returned a non-JSON body.", {
          url: redactUrl(url),
          snippet: redact(text).slice(0, 400)
        });
      }
      return json;
    }
    const headerWaitMs = parseRetryAfter(res.headers?.get?.("retry-after"), now());
    const hintMs = headerWaitMs ?? bodyRetryAfterMs(json);
    const retryable = res.status === 429 || res.status === 503 && hintMs !== null;
    if (retryable && retries < MAX_RETRIES) {
      const waitMs = hintMs ?? FALLBACK_BACKOFF_MS[retries];
      if (waitedMs + waitMs <= Math.min(maxTotalWaitMs, MAX_TOTAL_WAIT_MS)) {
        retries += 1;
        waitedMs += waitMs;
        await sleep(waitMs);
        continue;
      }
    }
    const code = json?.code || json?.error?.code || (typeof json?.error === "string" && /^[A-Z][A-Z0-9_]+$/.test(json.error) ? json.error : null) || `HTTP_${res.status}`;
    const message = json?.message || (typeof json?.error === "string" ? json.error : json?.error?.message) || `HTTP ${res.status}`;
    const rateLimit = rateLimitInfo(res);
    throw new SkillError(code, redact(String(message)), {
      httpStatus: res.status,
      url: redactUrl(url),
      body: json ?? redact(text).slice(0, 800),
      ...retryable ? {
        retries,
        retryAfterSeconds: hintMs === null ? null : Math.ceil(hintMs / 1e3)
      } : {},
      ...rateLimit ? { rateLimit } : {}
    });
  }
}
function redactUrl(url) {
  try {
    const u = new URL(url);
    return `${u.origin}${u.pathname}`;
  } catch {
    return String(url);
  }
}
function getJson(url, opts) {
  return request("GET", url, opts);
}

// scripts/src/lib/state.mjs
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
function stateRoot() {
  return process.env.ROZO_CHECKOUT_STATE_DIR || path.join(os.homedir(), ".rozo-checkout", "state");
}
function statePath(rozoPaymentId) {
  if (!/^[A-Za-z0-9-]{8,64}$/.test(String(rozoPaymentId || ""))) {
    throw new SkillError("BAD_ROZO_PAYMENT_ID", "Refusing to build a state path from that id.");
  }
  return path.join(stateRoot(), `${rozoPaymentId}.json`);
}
function readState(rozoPaymentId) {
  const file = statePath(rozoPaymentId);
  let raw;
  try {
    raw = fs.readFileSync(file, "utf8");
  } catch (err) {
    if (err.code === "ENOENT") return null;
    throw new SkillError("STATE_UNREADABLE", `Cannot read local state: ${err.code}`);
  }
  try {
    return JSON.parse(raw);
  } catch {
    throw new SkillError(
      "STATE_CORRUPT",
      "The local state file for this order is corrupt. Refusing to act; inspect it manually."
    );
  }
}
function findByLinkId(linkId) {
  const dir = stateRoot();
  let files = [];
  try {
    files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  } catch {
    return null;
  }
  let best = null;
  for (const f of files) {
    try {
      const s = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
      if (s?.linkId !== linkId) continue;
      if (!best || String(s.createdAt) > String(best.createdAt)) best = s;
    } catch {
    }
  }
  return best;
}

// scripts/src/lib/api.mjs
var MPP_BASE = process.env.ROZO_CHECKOUT_MPP_BASE || "https://apiserver.mpprouter.dev/v1/services/rozo-agent-api";
var CLIENT_LABEL = `rozo-checkout-cli/${PKG_VERSION}`;
var ATTRIBUTION_CLIENT = `rozo-checkout-skill/${PKG_VERSION}`;
var INTENTS_BASE = process.env.ROZO_CHECKOUT_INTENTS_BASE || "https://intentapiv4.rozo.ai/functions/v1/payment-api";
async function invoiceStatus({ linkId, rozoPaymentId }) {
  const qs = new URLSearchParams();
  if (linkId) qs.set("payment_id", linkId);
  if (rozoPaymentId) qs.set("rozo_payment_id", rozoPaymentId);
  if (![...qs.keys()].length) {
    throw new SkillError("USAGE", "invoiceStatus needs linkId or rozoPaymentId.");
  }
  return getJson(`${MPP_BASE}/invoice-status?${qs.toString()}`);
}
async function getPayment(rozoPaymentId) {
  return getJson(`${INTENTS_BASE}/payments/${encodeURIComponent(rozoPaymentId)}`);
}

// scripts/src/lib/amounts.mjs
var CHAIN_NAMES = {
  1: "Ethereum",
  56: "BNB Chain",
  137: "Polygon",
  8453: "Base",
  42161: "Arbitrum",
  900: "Solana",
  1500: "Stellar",
  lightning: "Bitcoin Lightning",
  9133: "Zcash"
};
var CHAIN_FAMILY = {
  1: "evm",
  56: "evm",
  137: "evm",
  8453: "evm",
  42161: "evm",
  900: "solana",
  1500: "stellar",
  lightning: "lightning",
  // Zcash: the CLI creates shielded orders only (pool Unified Address); it never signs.
  9133: "zcash"
};
var NATIVE_COINS = Object.freeze({
  "1:ETH": { chainId: "1", symbol: "ETH", decimals: 18 },
  "8453:ETH": { chainId: "8453", symbol: "ETH", decimals: 18 },
  "42161:ETH": { chainId: "42161", symbol: "ETH", decimals: 18 },
  "56:BNB": { chainId: "56", symbol: "BNB", decimals: 18 },
  "137:POL": { chainId: "137", symbol: "POL", decimals: 18 },
  "900:SOL": { chainId: "900", symbol: "SOL", decimals: 9 }
});
var NATIVE_MIN_USD_FALLBACK = Object.freeze({ "1:ETH": 1 });
var DECIMALS = {
  "1:USDC": 6,
  "1:USDT": 6,
  // BNB Chain: BEP-20 USDT and USDC are both 18-decimals.
  "56:USDC": 18,
  "56:USDT": 18,
  "137:USDC": 6,
  "137:USDT": 6,
  "8453:USDC": 6,
  // Arbitrum One: native USDC and USDT0 are both 6-decimals.
  "42161:USDC": 6,
  "42161:USDT": 6,
  "900:USDC": 6,
  "900:USDT": 6,
  // Stellar classic assets carry 7 decimal places.
  "1500:USDC": 7,
  // Native coins: wei (18) on every EVM chain, lamports (9) on Solana.
  "1:ETH": 18,
  "8453:ETH": 18,
  "42161:ETH": 18,
  "56:BNB": 18,
  "137:POL": 18,
  "900:SOL": 9,
  // Zcash: zatoshi.
  "9133:ZEC": 8
};
var AmountError = class extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
};
function decimalsKey(chainId, tokenSymbol) {
  return `${String(chainId).trim()}:${String(tokenSymbol || "").trim().toUpperCase()}`;
}
function decimalsFor(chainId, tokenSymbol) {
  const key = decimalsKey(chainId, tokenSymbol);
  const d = DECIMALS[key];
  if (d === void 0) {
    throw new AmountError(
      "UNKNOWN_DECIMALS",
      `No decimals known for ${key}; refusing to guess.`
    );
  }
  return d;
}
function isSatsUnit(amountUnit) {
  return String(amountUnit || "").trim().toLowerCase() === "sats";
}
function toAtomic(decimalString, decimals) {
  if (typeof decimalString === "number") decimalString = String(decimalString);
  if (typeof decimalString !== "string") {
    throw new AmountError("BAD_AMOUNT", "Amount must be a string or number.");
  }
  const s = decimalString.trim();
  if (!/^\d+(\.\d+)?$/.test(s)) {
    throw new AmountError("BAD_AMOUNT", `Not a plain decimal amount: ${s}`);
  }
  if (!Number.isInteger(decimals) || decimals < 0 || decimals > 36) {
    throw new AmountError("BAD_DECIMALS", `Invalid decimals: ${decimals}`);
  }
  const [whole, frac = ""] = s.split(".");
  if (frac.length > decimals) {
    const excess = frac.slice(decimals);
    if (/[^0]/.test(excess)) {
      throw new AmountError(
        "AMOUNT_PRECISION",
        `Amount ${s} has more precision than ${decimals} decimals allow.`
      );
    }
  }
  const padded = (frac + "0".repeat(decimals)).slice(0, decimals);
  return BigInt(whole + (decimals > 0 ? padded : ""));
}
function satsToAtomic(value) {
  const s = typeof value === "number" ? String(value) : String(value ?? "").trim();
  if (!/^\d+$/.test(s)) {
    throw new AmountError("BAD_SATS", `Lightning amount must be integer sats: ${s}`);
  }
  return BigInt(s);
}
function sourceAtomic(source, field) {
  const raw = source?.[field];
  if (raw === null || raw === void 0 || raw === "") return null;
  if (isSatsUnit(source?.amountUnit)) return satsToAtomic(raw);
  return toAtomic(raw, decimalsFor(source?.chainId, source?.tokenSymbol));
}
function comparePayment(source) {
  const expected = sourceAtomic(source, "amount");
  if (expected === null) {
    throw new AmountError("MISSING_EXPECTED_AMOUNT", "source.amount is missing.");
  }
  const received = sourceAtomic(source, "amountReceived");
  if (received === null || received === 0n) {
    return {
      state: "none",
      expectedAtomic: expected.toString(),
      receivedAtomic: (received ?? 0n).toString(),
      deltaAtomic: (0n - expected).toString()
    };
  }
  const delta = received - expected;
  return {
    state: delta === 0n ? "exact" : delta < 0n ? "underpaid" : "overpaid",
    expectedAtomic: expected.toString(),
    receivedAtomic: received.toString(),
    deltaAtomic: delta.toString()
  };
}
function formatAmount(source) {
  const amount = source?.amount;
  if (isSatsUnit(source?.amountUnit)) return `${amount} sats`;
  return `${amount} ${source?.tokenSymbol ?? ""}`.trim();
}
function chainName(chainId) {
  return CHAIN_NAMES[String(chainId)] || CHAIN_NAMES[chainId] || `chain ${chainId}`;
}
var STELLAR_MEMO_TYPE = "MEMO_TEXT";
function chainFamily(chainId) {
  return CHAIN_FAMILY[String(chainId)] || CHAIN_FAMILY[chainId] || null;
}
function isNativeSource(chainId, tokenSymbol) {
  return Object.prototype.hasOwnProperty.call(NATIVE_COINS, decimalsKey(chainId, tokenSymbol));
}

// scripts/src/lib/zec.mjs
var ZEC_CHAIN_ID = "9133";
var ZEC_SYMBOL = "ZEC";
var ZEC_PAYIN_STATES = /* @__PURE__ */ new Set(["awaiting", "seen", "confirming", "eligible", "expired", "reorged"]);
var UA_RE = /^u1[02-9ac-hj-np-z]{100,400}$/;
function isZecSource(chainId, tokenSymbol) {
  return String(chainId ?? "").trim() === ZEC_CHAIN_ID && String(tokenSymbol ?? "").trim().toUpperCase() === ZEC_SYMBOL;
}
function isUnifiedAddress(value) {
  return typeof value === "string" && UA_RE.test(value.trim());
}
function zecStatusOf(source) {
  const z = source?.zec;
  if (!z || typeof z !== "object") return null;
  const receive = z.receive === "shielded" || z.receive === "transparent" ? z.receive : null;
  const payinState = ZEC_PAYIN_STATES.has(z.payinState) ? z.payinState : null;
  const confirmations = Number.isInteger(z.confirmations) && z.confirmations >= 0 ? z.confirmations : null;
  const requiredConfirmations = z.requiredConfirmations === 1 || z.requiredConfirmations === 2 ? z.requiredConfirmations : null;
  const quoteExpiresAt = typeof z.quoteExpiresAt === "string" && z.quoteExpiresAt ? z.quoteExpiresAt : null;
  const receivedZat = typeof z.receivedZat === "string" && /^\d+$/.test(z.receivedZat) ? z.receivedZat : null;
  return { receive, payinState, confirmations, requiredConfirmations, quoteExpiresAt, receivedZat };
}
function zecMoneySeen(zec) {
  if (!zec) return false;
  if (zec.payinState === "seen" || zec.payinState === "confirming" || zec.payinState === "eligible") return true;
  if (zec.receivedZat !== null && zec.receivedZat !== "0") return true;
  if (zec.payinState === null) return true;
  return false;
}
function parsePaymentUri(uri) {
  if (typeof uri !== "string") return null;
  const m = /^zcash:([0-9a-z]+)\?([^#]*)$/i.exec(uri.trim());
  if (!m) return null;
  const address = m[1];
  const out = { address, amount: null, memo: null };
  const seen = /* @__PURE__ */ new Set();
  for (const part of m[2].split("&")) {
    if (!part) return null;
    const eq = part.indexOf("=");
    if (eq <= 0) return null;
    const key = part.slice(0, eq);
    const value = part.slice(eq + 1);
    if (seen.has(key)) return null;
    seen.add(key);
    if (key === "amount") {
      if (!/^\d+(\.\d{1,8})?$/.test(value)) return null;
      out.amount = value;
    } else if (key === "memo") {
      if (!/^[A-Za-z0-9_-]{1,684}$/.test(value)) return null;
      out.memo = value;
    } else {
      return null;
    }
  }
  if (out.amount === null) return null;
  return out;
}
function sameDecimal(a, b) {
  const norm = (v) => {
    const s = String(v ?? "").trim();
    if (!/^\d+(\.\d+)?$/.test(s)) return null;
    const [w, f = ""] = s.split(".");
    const frac = f.replace(/0+$/, "");
    return `${w.replace(/^0+(?=\d)/, "")}${frac ? `.${frac}` : ""}`;
  };
  const na = norm(a);
  return na !== null && na === norm(b);
}
function validateShieldedDeposit(source) {
  const address = typeof source?.receiverAddress === "string" ? source.receiverAddress.trim() : "";
  if (!isUnifiedAddress(address)) {
    return { ok: false, code: "ZEC_ADDRESS_INVALID", reason: "The order did not return a mainnet Unified Address (u1...). Refusing to show it as payable." };
  }
  const uri = typeof source?.paymentUri === "string" ? source.paymentUri.trim() : "";
  if (!uri) {
    return { ok: false, code: "ZEC_PAYMENT_URI_MISSING", reason: "The order carries no payment URI yet. Nothing is payable until it appears." };
  }
  const parsed = parsePaymentUri(uri);
  if (!parsed) {
    return { ok: false, code: "ZEC_PAYMENT_URI_INVALID", reason: "The payment URI is not a single-payment ZIP-321 URI. Refusing to show it." };
  }
  if (parsed.address !== address) {
    return { ok: false, code: "ZEC_PAYMENT_URI_MISMATCH", reason: "The payment URI names a different address than the order. Refusing to show it." };
  }
  if (!sameDecimal(parsed.amount, source?.amount)) {
    return { ok: false, code: "ZEC_PAYMENT_URI_MISMATCH", reason: "The payment URI amount differs from the order amount. Refusing to show it." };
  }
  return { ok: true, code: null, reason: null, address, paymentUri: uri, memo: parsed.memo };
}

// scripts/src/lib/guards.mjs
var UNPAID_STATUS = "payment_unpaid";
var NATIVE_PROGRESS_STATUSES = /* @__PURE__ */ new Set([
  "payment_payin_completed",
  "payment_bridging",
  "payment_payout_started",
  "payment_payout_completed",
  "payment_completed"
]);
function receiptSignal(source) {
  const raw = source?.amountReceived;
  if (raw === null || raw === void 0 || raw === "") {
    return { money: false, receipt: null, unparsable: false };
  }
  try {
    const receipt = comparePayment(source);
    return { money: receipt.state !== "none", receipt, unparsable: false };
  } catch {
    return { money: true, receipt: null, unparsable: true };
  }
}
function validateDepositInstructions(source) {
  const family = chainFamily(source?.chainId);
  const address = typeof source?.receiverAddress === "string" ? source.receiverAddress.trim() : "";
  const memo = typeof source?.receiverMemo === "string" ? source.receiverMemo.trim() : "";
  const bolt11 = typeof source?.lnInvoice === "string" && source.lnInvoice.trim() ? source.lnInvoice.trim() : "";
  let amountAtomic;
  try {
    amountAtomic = sourceAtomic(source, "amount");
  } catch (err) {
    return {
      ok: false,
      code: "DEPOSIT_INCOMPLETE",
      reason: `The deposit amount is unusable: ${err.message}`
    };
  }
  if (amountAtomic === null || amountAtomic <= 0n) {
    return {
      ok: false,
      code: "DEPOSIT_INCOMPLETE",
      reason: "The order carries no positive deposit amount."
    };
  }
  if (family === "lightning") {
    if (!bolt11) {
      return {
        ok: false,
        code: "DEPOSIT_INCOMPLETE",
        reason: "The Lightning order has no BOLT11 invoice yet (the swap may still be being created). Nothing is payable until it appears."
      };
    }
    return { ok: true, code: null, reason: null, family, amountAtomic, payTo: bolt11, memo: null };
  }
  if (!address) {
    return {
      ok: false,
      code: "DEPOSIT_NOT_LIVE",
      reason: "The live payments response returned no deposit address."
    };
  }
  if (family === "zcash" && zecStatusOf(source)?.receive === "shielded") {
    const zec = validateShieldedDeposit(source);
    if (!zec.ok) return { ok: false, code: zec.code, reason: zec.reason };
    return { ok: true, code: null, reason: null, family, amountAtomic, payTo: zec.address, memo: null, paymentUri: zec.paymentUri };
  }
  if (family === "stellar" && !memo) {
    return {
      ok: false,
      code: "DEPOSIT_MEMO_REQUIRED",
      reason: "A Stellar deposit requires a memo, and this order did not supply one. Sending without it would very likely lose the funds. Refusing to display it as payable."
    };
  }
  return {
    ok: true,
    code: null,
    reason: null,
    family,
    amountAtomic,
    payTo: address,
    memo: memo || null
  };
}
function reuseGuard({ payment, requested, reused = false }) {
  const source = payment?.source || {};
  const evidence = {
    reused: Boolean(reused),
    status: payment?.status ?? null,
    txHash: source.txHash ?? null,
    amountReceived: source.amountReceived ?? null,
    confirmedAt: source.confirmedAt ?? null,
    chainId: source.chainId ?? null,
    tokenSymbol: source.tokenSymbol ?? null,
    senderAddress: source.senderAddress ?? null
  };
  const hasTx = source.txHash !== null && source.txHash !== void 0 && source.txHash !== "";
  const signal = receiptSignal(source);
  const hasConfirm = source.confirmedAt !== null && source.confirmedAt !== void 0 && source.confirmedAt !== "";
  const zecSeen = isZecSource(source.chainId, source.tokenSymbol) && zecMoneySeen(zecStatusOf(source));
  if (hasTx || signal.money || hasConfirm || zecSeen) {
    return {
      ok: false,
      code: "ORDER_ALREADY_FUNDED",
      reason: signal.unparsable ? "This order reports an amountReceived that cannot be read. It is treated as funded until a human confirms otherwise \u2014 do NOT pay again." : zecSeen && !hasTx && !signal.money && !hasConfirm ? "A shielded ZEC payment to this order has already been seen on the network. Do NOT pay again; watch it with status instead." : "This Coinbase link already has a funded Rozo order (it may have been paid elsewhere). Do NOT pay again \u2014 escalate for manual reconciliation.",
      moneyDetected: true,
      evidence: { ...evidence, receipt: signal.receipt, receiptUnparsable: signal.unparsable, ...zecSeen ? { zec: zecStatusOf(source) } : {} }
    };
  }
  if (payment?.status !== UNPAID_STATUS) {
    const terminal = ["payment_expired", "payment_bounced", "payment_refunded"].includes(
      payment?.status
    );
    return {
      ok: false,
      code: terminal ? "ORDER_NOT_PAYABLE" : "ORDER_ALREADY_FUNDED",
      reason: `Existing order status is "${payment?.status ?? "unknown"}", not "${UNPAID_STATUS}".`,
      moneyDetected: !terminal,
      evidence
    };
  }
  const wantChain = String(requested?.chainId ?? "").trim();
  const wantToken = String(requested?.tokenSymbol ?? "").trim().toUpperCase();
  const gotChain = String(source.chainId ?? "").trim();
  const gotToken = String(source.tokenSymbol ?? "").trim().toUpperCase();
  if (!gotChain || !gotToken || gotChain !== wantChain || gotToken !== wantToken) {
    return {
      ok: false,
      code: "REUSED_SOURCE_MISMATCH",
      reason: `The order expects ${gotToken || "?"} on chain ${gotChain || "?"}, but you chose ${wantToken} on chain ${wantChain}. Paying the wrong asset or network is usually unrecoverable.`,
      moneyDetected: false,
      evidence
    };
  }
  if (isZecSource(gotChain, gotToken)) {
    const zec = zecStatusOf(source);
    const wantReceive = requested?.shielded === true ? "shielded" : "transparent";
    if (!zec || zec.receive !== wantReceive) {
      return {
        ok: false,
        code: "ZEC_RECEIVE_MODE_MISMATCH",
        reason: `This link already has a ZEC order that is paid ${zec?.receive ?? "in an unknown way"}, but you asked for ${wantReceive}. Nothing new was created. Pay that order the way it was made, or wait for it to expire unfunded.`,
        moneyDetected: false,
        evidence: { ...evidence, zec }
      };
    }
    if (zec.payinState === "expired" || zec.payinState === "reorged") {
      return {
        ok: false,
        code: "ZEC_QUOTE_EXPIRED",
        reason: `The ZEC price lock on this order has ${zec.payinState === "reorged" ? "been disturbed by a reorg" : "expired"} with nothing received. Do not pay it; re-run pay to get a fresh order.`,
        moneyDetected: false,
        evidence: { ...evidence, zec }
      };
    }
  }
  const deposit = validateDepositInstructions(source);
  if (!deposit.ok) {
    return {
      ok: false,
      code: deposit.code,
      reason: deposit.reason,
      moneyDetected: false,
      evidence
    };
  }
  return { ok: true, code: null, reason: null, moneyDetected: false, evidence, deposit };
}
function checkPayable(statusResponse, now = Date.now()) {
  const cb = statusResponse?.coinbase;
  if (!cb) {
    return {
      ok: false,
      code: "LINK_NO_LONGER_PAYABLE",
      reason: "invoice-status returned no Coinbase state; cannot prove the link is still payable.",
      derived: null
    };
  }
  const protocolVersion = cb.protocolVersion ?? statusResponse?.protocolVersion ?? null;
  const derived = {
    protocolVersion,
    status: cb.status ?? null,
    settled: cb.settled ?? null,
    usageCount: cb.usageCount ?? null,
    maxUsage: cb.maxUsage ?? null,
    preApprovalExpiry: cb.preApprovalExpiry ?? null
  };
  if (cb.settled === true) {
    return {
      ok: false,
      code: "LINK_NO_LONGER_PAYABLE",
      reason: "The Coinbase resource is already settled \u2014 someone has paid it.",
      derived
    };
  }
  if (protocolVersion === "v3") {
    if (!cb.status) {
      return {
        ok: false,
        code: "LINK_PAYABILITY_UNKNOWN",
        reason: "The Payment Session response carries no status; cannot prove it is still payable.",
        derived
      };
    }
    if (cb.status !== "PAYMENT_SESSION_STATUS_CREATED") {
      return {
        ok: false,
        code: "LINK_NO_LONGER_PAYABLE",
        reason: `Payment Session status is ${cb.status}; only PAYMENT_SESSION_STATUS_CREATED is payable.`,
        derived
      };
    }
    return { ok: true, code: null, reason: null, derived };
  }
  const usage2 = Number(cb.usageCount);
  const max = Number(cb.maxUsage);
  if (cb.usageCount === null || cb.usageCount === void 0 || cb.maxUsage === null || cb.maxUsage === void 0 || !Number.isFinite(usage2) || !Number.isFinite(max)) {
    return {
      ok: false,
      code: "LINK_PAYABILITY_UNKNOWN",
      reason: "The payment link response is missing usageCount/maxUsage; cannot prove it has not already been used.",
      derived
    };
  }
  if (usage2 >= max) {
    return {
      ok: false,
      code: "LINK_NO_LONGER_PAYABLE",
      reason: `Payment link already used (${usage2}/${max}).`,
      derived
    };
  }
  return { ok: true, code: null, reason: null, derived };
}
function classifyStatus({
  payment,
  routerState,
  coinbase,
  now = Date.now(),
  viewsFailed = false,
  provider = "coinbase"
}) {
  const bitrefill = provider === "bitrefill";
  const source = payment?.source || {};
  const hasTx = Boolean(source.txHash);
  const confirmed = Boolean(source.confirmedAt);
  const signal = receiptSignal(source);
  const receipt = signal.receipt;
  const moneyDetected = hasTx || confirmed || signal.money;
  const routerStatus = routerState?.status ?? null;
  const mk = (state, detail, opts = {}) => ({
    state,
    moneyDetected: Boolean(moneyDetected),
    terminal: Boolean(opts.terminal),
    escalate: Boolean(opts.escalate),
    unknown: Boolean(opts.unknown),
    detail,
    receipt,
    receiptUnparsable: signal.unparsable,
    routerStatus
  });
  if (viewsFailed || !payment?.status && !routerStatus && !coinbase) {
    return mk(
      "unknown",
      "Could not read the order state from the backend. This is NOT evidence that nothing has been paid \u2014 do not act on it.",
      { unknown: true }
    );
  }
  if (signal.unparsable) {
    return mk(
      "stuck_after_payment",
      "The order reports an amountReceived that cannot be read. Treating it as funded until a human confirms otherwise.",
      { escalate: true }
    );
  }
  if (routerStatus === "failed_pay_invoice" || routerStatus === "failed_insufficient_balance") {
    return mk(
      "stuck_after_payment",
      `Fulfillment failed (${routerStatus}) after the pay-in. Do not pay again \u2014 escalate for manual reconciliation.`,
      { terminal: false, escalate: true }
    );
  }
  if (!bitrefill && coinbase?.settled === true && (routerStatus === null || routerStatus === "paid")) {
    return mk("settled", "Coinbase invoice settled by the funder wallet.", { terminal: true });
  }
  if (!bitrefill && routerStatus === "paid") {
    return mk(
      "paying_coinbase",
      "The funder wallet paid, but Coinbase has not shown the capture yet. Keep polling; do not pay again."
    );
  }
  const nativeAccepted = isNativeSource(source.chainId, source.tokenSymbol) && NATIVE_PROGRESS_STATUSES.has(payment?.status);
  if (moneyDetected && receipt && receipt.state === "underpaid" && !nativeAccepted) {
    return mk(
      "underpaid",
      "Less arrived than the order requires. Do NOT send a top-up to the same address \u2014 escalate.",
      { escalate: true }
    );
  }
  if (moneyDetected && receipt && receipt.state === "overpaid") {
    return mk("payin_detected", "More arrived than required; escalate for operator follow-up.", {
      escalate: true
    });
  }
  if (bitrefill) {
    const payoutTx = Boolean(payment?.destination?.txHash);
    if (payment?.status === "payment_payout_completed" || payment?.status === "payment_completed" && payoutTx) {
      return mk("settled", "USDC delivered to the Bitrefill invoice address on Base.", {
        terminal: true
      });
    }
    if (payment?.status === "payment_completed") {
      return mk("bridging", "Payment completed but no payout transaction is visible yet. Keep polling.");
    }
  }
  switch (payment?.status) {
    case "payment_unpaid": {
      if (moneyDetected) {
        return mk("payin_detected", "Pay-in seen on chain, waiting for confirmations.");
      }
      const exp = payment?.expiresAt ? Date.parse(payment.expiresAt) : NaN;
      if (Number.isFinite(exp) && exp < now) {
        return mk("expired_unfunded", "The order expired before any funds arrived. This order can no longer be paid.", {
          terminal: true
        });
      }
      return mk("awaiting_deposit", "Waiting for the deposit.");
    }
    case "payment_started":
      return mk("payin_detected", "Pay-in seen, waiting for confirmations.");
    case "payment_payin_completed":
      return mk("payin_confirmed", "Pay-in confirmed; fulfillment can start.");
    case "payment_bridging":
    case "payment_payout_started":
      return mk("bridging", "Bridging the pay-in toward the funder.");
    case "payment_payout_completed":
      return mk(
        routerStatus === "paying" ? "paying_coinbase" : "bridging",
        routerStatus === "paying" ? "Funder is paying the Coinbase invoice." : "Payout landed; waiting on Coinbase settlement."
      );
    case "payment_completed":
      return mk(
        "paying_coinbase",
        "The bridge leg completed, but Coinbase settlement is not yet confirmed. Keep polling."
      );
    case "payment_expired":
      return moneyDetected ? mk("stuck_after_payment", "Order expired AFTER funds arrived \u2014 escalate immediately.", {
        escalate: true
      }) : mk("expired_unfunded", "Order expired unfunded. This order can no longer be paid.", { terminal: true });
    case "payment_bounced":
    case "payment_refunded":
      return mk("stuck_after_payment", `Order ended as ${payment.status} \u2014 escalate.`, {
        escalate: true
      });
    default:
      break;
  }
  if (routerStatus === "payin_seen") return mk("payin_confirmed", "Router saw the pay-in.");
  if (routerStatus === "paying") return mk("paying_coinbase", "Funder is paying Coinbase.");
  return mk(
    moneyDetected ? "stuck_after_payment" : "unknown",
    `Unrecognized backend status "${payment?.status ?? "unknown"}"; not assuming anything about it.`,
    { escalate: Boolean(moneyDetected), unknown: !moneyDetected }
  );
}

// scripts/src/lib/blacklist.mjs
import fs2 from "node:fs";
import path2 from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
var BlacklistError = class extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
};
function normalizeAddress(address, family) {
  if (typeof address !== "string") return null;
  const trimmed = address.trim();
  if (!trimmed) return null;
  if (family === "evm" || /^0x[0-9a-fA-F]{40}$/.test(trimmed)) {
    return trimmed.toLowerCase();
  }
  return trimmed;
}
function parseBlacklist(doc) {
  if (!doc || typeof doc !== "object" || Array.isArray(doc)) {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist document is not an object.");
  }
  const { provenance, entries } = doc;
  if (!provenance || typeof provenance !== "object") {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist provenance header is missing.");
  }
  if (!Array.isArray(entries) || entries.length === 0) {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist is empty or not an array.");
  }
  const addresses = [];
  for (const e of entries) {
    if (!e || typeof e !== "object" || typeof e.address !== "string" || !e.address.trim()) {
      throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist entry has no address.");
    }
    addresses.push(e.address);
  }
  const digest = crypto.createHash("sha256").update(JSON.stringify(addresses), "utf8").digest("hex");
  if (typeof provenance.addressesSha256 !== "string" || !provenance.addressesSha256) {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist provenance digest is missing.");
  }
  if (digest !== provenance.addressesSha256) {
    throw new BlacklistError(
      "BLACKLIST_UNAVAILABLE",
      "Blacklist digest mismatch \u2014 the vendored address list was modified without re-signing."
    );
  }
  if (provenance.addressCount !== void 0 && provenance.addressCount !== entries.length) {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Blacklist addressCount does not match entries.");
  }
  const index = /* @__PURE__ */ new Map();
  for (const e of entries) {
    const key = normalizeAddress(e.address, e.family);
    if (key) index.set(key, e);
    const lower = e.address.trim().toLowerCase();
    if (/^0x[0-9a-f]{40}$/.test(lower)) index.set(lower, e);
  }
  return { entries, index, provenance, digest };
}
function candidatePaths(moduleUrl) {
  const here = path2.dirname(fileURLToPath(moduleUrl));
  return [
    path2.join(here, "blacklist.json"),
    path2.join(here, "..", "src", "lib", "blacklist.json"),
    path2.join(here, "..", "..", "src", "lib", "blacklist.json")
  ];
}
var cached = null;
function loadBlacklist(explicitPath) {
  if (!explicitPath && cached) return cached;
  const paths = explicitPath ? [explicitPath] : candidatePaths(import.meta.url);
  let lastErr = null;
  for (const p of paths) {
    let raw;
    try {
      raw = fs2.readFileSync(p, "utf8");
    } catch (err) {
      lastErr = err;
      continue;
    }
    let doc;
    try {
      doc = JSON.parse(raw);
    } catch {
      throw new BlacklistError("BLACKLIST_UNAVAILABLE", `Blacklist file is not valid JSON: ${p}`);
    }
    const parsed = parseBlacklist(doc);
    parsed.sourceFile = p;
    if (!explicitPath) cached = parsed;
    return parsed;
  }
  throw new BlacklistError(
    "BLACKLIST_UNAVAILABLE",
    `Blacklist file not found (looked in ${paths.length} locations). Refusing to proceed.` + (lastErr ? ` Last error: ${lastErr.code || lastErr.message}` : "")
  );
}
function checkAddress(address, family, blacklist) {
  const bl = blacklist || loadBlacklist();
  const normalized = normalizeAddress(address, family);
  if (!normalized) {
    throw new BlacklistError("BLACKLIST_UNAVAILABLE", "Cannot check an empty address.");
  }
  const entry = bl.index.get(normalized) || bl.index.get(normalized.toLowerCase()) || null;
  return { hit: Boolean(entry), entry, normalized };
}
function assertNotBlacklisted(targets, blacklist) {
  const bl = blacklist || loadBlacklist();
  for (const t of targets) {
    if (!t || !t.address) continue;
    const { hit, entry } = checkAddress(t.address, t.family, bl);
    if (hit) {
      const err = new BlacklistError(
        "BLACKLIST_HIT",
        `${t.role || "address"} is on the compromised-wallet blacklist (reported ${entry.reportedOn}: ${entry.note}). Refusing.`
      );
      err.role = t.role || "address";
      throw err;
    }
  }
  return true;
}

// scripts/src/lib/expiry.mjs
var MINUTE = 6e4;
var MARGINS_MS = {
  1: 10 * MINUTE,
  56: 10 * MINUTE,
  137: 10 * MINUTE,
  8453: 10 * MINUTE,
  42161: 10 * MINUTE,
  900: 5 * MINUTE,
  1500: 10 * MINUTE,
  lightning: 10 * MINUTE,
  // Zcash: 75 s blocks, 1 to 2 confirmations, then the hub advances the merchant.
  9133: 10 * MINUTE
};
var BOLT11_MIN_VALIDITY_MS = 10 * MINUTE;
var DEFAULT_MARGIN_MS = 10 * MINUTE;
var DEFAULT_WATCH_MS = 10 * MINUTE;
var LIGHTNING_WATCH_CAP_MS = 60 * MINUTE;
function formatRemaining(ms) {
  if (!Number.isFinite(ms)) return "unknown";
  if (ms <= 0) return "expired";
  const totalMinutes = Math.floor(ms / 6e4);
  if (totalMinutes < 1) return `${Math.floor(ms / 1e3)}s`;
  if (totalMinutes < 60) return `${totalMinutes}m`;
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return m ? `${h}h ${m}m` : `${h}h`;
}
function marginFor(chainId) {
  const key = String(chainId);
  return MARGINS_MS[key] ?? MARGINS_MS[chainId] ?? DEFAULT_MARGIN_MS;
}
function parseDeadline(value) {
  if (value === null || value === void 0 || value === "") return null;
  if (typeof value === "number" && Number.isFinite(value)) {
    return value < 1e12 ? Math.round(value * 1e3) : Math.round(value);
  }
  const s = String(value).trim();
  if (/^\d+$/.test(s)) {
    const n = Number(s);
    return n < 1e12 ? n * 1e3 : n;
  }
  const t = Date.parse(s);
  return Number.isFinite(t) ? t : null;
}
function checkExpiry({
  now,
  chainId,
  intentExpiresAt,
  coinbaseExpiry,
  bolt11ExpiresAt = void 0,
  quoteExpiresAt = void 0
}) {
  const marginMs = marginFor(chainId);
  const intentMs = parseDeadline(intentExpiresAt);
  const coinbaseMs = parseDeadline(coinbaseExpiry);
  const bolt11Ms = bolt11ExpiresAt === void 0 ? void 0 : parseDeadline(bolt11ExpiresAt);
  const native = quoteExpiresAt !== void 0;
  const quoteMs = native ? parseDeadline(quoteExpiresAt) : null;
  const deadlines = { intentMs, coinbaseMs, bolt11Ms: bolt11Ms ?? null, quoteMs };
  const base = {
    marginMs,
    effectiveDeadlineMs: null,
    msRemaining: null,
    msOfSlack: null,
    deadlines
  };
  if (intentMs === null) {
    return {
      ...base,
      ok: false,
      code: "EXPIRY_UNPARSABLE",
      reason: "Intent expiresAt is missing or unparsable."
    };
  }
  if (coinbaseMs === null) {
    return {
      ...base,
      ok: false,
      code: "EXPIRY_UNPARSABLE",
      reason: "Coinbase preApprovalExpiry is missing or unparsable."
    };
  }
  if (native && quoteMs === null) {
    return {
      ...base,
      ok: false,
      code: "EXPIRY_UNPARSABLE",
      reason: "This native coin order carries no price lock (quoteExpiresAt), so the coin amount cannot be trusted to be honoured. Refusing to treat it as payable."
    };
  }
  const effective = native ? Math.min(intentMs, coinbaseMs, quoteMs) : Math.min(intentMs, coinbaseMs);
  const lockBinds = native && quoteMs <= Math.min(intentMs, coinbaseMs);
  const msRemaining = effective - now;
  const msOfSlack = msRemaining - marginMs;
  const withDeadline = {
    ...base,
    effectiveDeadlineMs: effective,
    msRemaining,
    msOfSlack
  };
  if (msRemaining <= 0) {
    return {
      ...withDeadline,
      ok: false,
      code: lockBinds ? "QUOTE_EXPIRED" : "EXPIRED",
      reason: lockBinds ? "The coin price for this order was locked until quoteExpiresAt, and that has passed. A payment now would be valued at the price when it arrives and may fall short. Do not send it; let the order expire unfunded and start a new one." : "The order or the Coinbase link has already expired."
    };
  }
  if (msOfSlack <= 0) {
    return {
      ...withDeadline,
      ok: false,
      code: lockBinds ? "QUOTE_EXPIRY_MARGIN" : "EXPIRY_MARGIN",
      reason: `Only ${Math.floor(msRemaining / 1e3)}s left before the earliest deadline${lockBinds ? " (the coin price lock)" : ""}; this chain needs a ${Math.floor(marginMs / 6e4)} min safety margin.`
    };
  }
  if (bolt11ExpiresAt !== void 0) {
    if (bolt11Ms === null) {
      return {
        ...withDeadline,
        ok: false,
        code: "EXPIRY_UNPARSABLE",
        reason: "BOLT11 invoice expiry is missing or unparsable."
      };
    }
    const bolt11Remaining = bolt11Ms - now;
    if (bolt11Remaining < BOLT11_MIN_VALIDITY_MS) {
      return {
        ...withDeadline,
        ok: false,
        code: "BOLT11_TOO_SHORT",
        reason: `BOLT11 invoice has ${Math.max(0, Math.floor(bolt11Remaining / 1e3))}s of validity left; at least 10 min is required. Request a fresh invoice.`
      };
    }
  }
  return { ...withDeadline, ok: true, code: null, reason: null };
}
function priceLockFor({ native, payment = null, others = [] }) {
  if (!native) return void 0;
  const candidates = [payment?.quoteExpiresAt, payment?.source?.quoteExpiresAt, ...others].map(parseDeadline).filter((ms) => ms !== null);
  if (!candidates.length) return null;
  return new Date(Math.min(...candidates)).toISOString();
}

// scripts/src/lib/bitrefill.mjs
var PROVIDER_BITREFILL = "bitrefill";
var BITREFILL_DESTINATION = Object.freeze({ chainId: "8453", tokenSymbol: "USDC" });
var BITREFILL_MIN_EXPIRY_MS = 5 * 60 * 1e3;
var BITREFILL_MIN_PAY_WINDOW_MS = 2 * 60 * 1e3;
var BITREFILL_MAX_EXPIRY_AHEAD_MS = 61 * 60 * 1e3;
function providerFromPayment(payment) {
  if (!payment) return null;
  if (String(payment.orderId ?? payment.order_id ?? "").startsWith("bitrefill_")) return PROVIDER_BITREFILL;
  const meta = payment.metadata?.provider;
  if (meta) return String(meta).toLowerCase();
  return null;
}
function earliestExpiry(...values) {
  const ms = values.map((v) => parseDeadline(v)).filter((v) => v !== null);
  return ms.length ? new Date(Math.min(...ms)).toISOString() : null;
}
function intentBitrefillExpiry(payment) {
  return payment?.metadata?.bitrefillExpiresAt ?? null;
}

// scripts/src/lib/receipt.mjs
var PAYMENT_OUTCOMES = Object.freeze([
  "awaiting_payment",
  "processing",
  "settled",
  "expired_unfunded",
  "needs_attention",
  "unknown"
]);
var NEXT_ACTION_TYPES = Object.freeze([
  "pay",
  "check_status",
  "choose_method",
  "request_new_invoice",
  "contact_support",
  "none"
]);
var STATE_TO_OUTCOME = Object.freeze({
  awaiting_deposit: "awaiting_payment",
  payin_detected: "processing",
  payin_confirmed: "processing",
  bridging: "processing",
  paying_coinbase: "processing",
  settled: "settled",
  expired_unfunded: "expired_unfunded",
  invoice_expired: "expired_unfunded",
  deadline_unknown: "needs_attention",
  underpaid: "needs_attention",
  stuck_after_payment: "needs_attention",
  unknown: "unknown"
});

// scripts/src/status.mjs
function resolveProvider(explicit, rozoPaymentId) {
  if (explicit) return String(explicit).toLowerCase();
  if (rozoPaymentId && isRozoPaymentId(rozoPaymentId)) {
    try {
      return readState(rozoPaymentId)?.provider ?? null;
    } catch {
      return null;
    }
  }
  return null;
}
function localSendFor(id, read = readState) {
  if (!id || !isRozoPaymentId(id)) return null;
  let state;
  try {
    state = read(id);
  } catch (err) {
    return { status: "unreadable", txHash: null, claimedAt: null, error: err?.code ?? "STATE_UNREADABLE" };
  }
  const send = state?.send;
  if (!send || !send.status) return null;
  return { status: send.status, txHash: publicHash(send.txHash ?? null), claimedAt: send.claimedAt ?? null };
}
function sendWindowFor({ provider, chainId, payment, status, bitrefillExpiry, quoteExpiresAt, now = Date.now() }) {
  if (provider === "bitrefill") {
    const deadline = bitrefillExpiry ?? null;
    const expiry2 = checkExpiry({
      now,
      chainId,
      intentExpiresAt: payment?.expiresAt ?? deadline,
      coinbaseExpiry: deadline
    });
    return expiry2.ok ? { ok: true, code: null, minutesOfSlack: Math.floor(expiry2.msOfSlack / 6e4), deadlineMs: expiry2.effectiveDeadlineMs } : { ok: false, code: expiry2.code, reason: expiry2.reason };
  }
  if (!status) {
    return { ok: false, code: "LINK_PAYABILITY_UNKNOWN", reason: "The Coinbase link state could not be read." };
  }
  const payable = checkPayable(status, now);
  if (!payable.ok) return { ok: false, code: payable.code, reason: payable.reason };
  const expiry = checkExpiry({
    now,
    chainId,
    intentExpiresAt: payment?.expiresAt ?? status?.rozoPayment?.expiresAt,
    coinbaseExpiry: status?.coinbase?.preApprovalExpiry,
    // Native orders: the price lock is a deadline too (undefined otherwise).
    ...quoteExpiresAt !== void 0 ? { quoteExpiresAt } : {}
  });
  return expiry.ok ? { ok: true, code: null, minutesOfSlack: Math.floor(expiry.msOfSlack / 6e4), deadlineMs: expiry.effectiveDeadlineMs } : { ok: false, code: expiry.code, reason: expiry.reason };
}
async function snapshot({ rozoPaymentId, linkId, provider: explicitProvider }) {
  let provider = resolveProvider(explicitProvider, rozoPaymentId);
  let prefetched = null;
  if (!provider && rozoPaymentId && isRozoPaymentId(rozoPaymentId)) {
    try {
      prefetched = await getPayment(rozoPaymentId);
      provider = providerFromPayment(prefetched);
    } catch {
      prefetched = null;
    }
  }
  provider = provider === "bitrefill" ? "bitrefill" : "coinbase";
  let status = null;
  let statusError = null;
  if (provider !== "bitrefill") {
    try {
      status = await invoiceStatus({ linkId, rozoPaymentId });
    } catch (err) {
      statusError = { code: err.code, message: err.message };
    }
  }
  let id = rozoPaymentId || status?.rozo_payment_id || null;
  let idSource = rozoPaymentId ? "argument" : status?.rozo_payment_id ? "invoice-status" : null;
  if (!id && linkId) {
    const local = findByLinkId(linkId);
    if (local) {
      id = local.rozoPaymentId;
      idSource = "local state";
    }
  }
  let payment = null;
  let paymentError = null;
  if (prefetched && id === rozoPaymentId) {
    payment = prefetched;
  } else if (id && isRozoPaymentId(id)) {
    try {
      payment = await getPayment(id);
    } catch (err) {
      paymentError = { code: err.code, message: err.message };
    }
  }
  const viewsFailed = provider === "bitrefill" ? !payment : Boolean(statusError) && !payment;
  const verdict = classifyStatus({
    payment: payment || status?.rozoPayment || {},
    routerState: status?.routerState,
    coinbase: status?.coinbase,
    viewsFailed,
    provider
  });
  const source = payment?.source || status?.rozoPayment?.source || {};
  const native = isNativeSource(source.chainId, source.tokenSymbol);
  const isZec = isZecSource(source.chainId, source.tokenSymbol);
  const zec = isZec ? zecStatusOf(source) : null;
  let localState = null;
  try {
    localState = id && isRozoPaymentId(id) ? readState(id) : null;
  } catch {
    localState = null;
  }
  const quoteExpiresAt = isZec ? zec?.quoteExpiresAt ?? null : priceLockFor({
    native,
    payment: payment || status?.rozoPayment || null,
    others: [localState?.confirmation?.quoteExpiresAt, localState?.quoteExpiresAt]
  });
  let bitrefillExpiry = null;
  let state = verdict.state;
  let terminal = verdict.terminal;
  let detail = verdict.detail;
  const zecMoney = Boolean(zec && zecMoneySeen(zec));
  let escalate = verdict.escalate;
  if (zecMoney && state === "expired_unfunded") {
    state = "stuck_after_payment";
    terminal = false;
    escalate = true;
    detail = "The order expired but the custody rail reports a ZEC pay-in. Do not pay again; escalate for manual reconciliation.";
  } else if (zecMoney && state === "awaiting_deposit") {
    state = "payin_detected";
    detail = zec.payinState === "seen" || zec.payinState === "confirming" ? `Shielded pay-in ${zec.payinState}: ${zec.confirmations ?? 0} of ${zec.requiredConfirmations ?? "?"} confirmations.` : `The custody rail reports a ZEC pay-in (${zec.payinState ?? "state unreadable"}). Do not pay again.`;
  }
  if (provider === "bitrefill") {
    let local = null;
    try {
      local = id && isRozoPaymentId(id) ? readState(id) : null;
    } catch {
      local = null;
    }
    bitrefillExpiry = earliestExpiry(local?.bitrefill?.expiresAt, intentBitrefillExpiry(payment));
    if (!verdict.moneyDetected && ["awaiting_deposit", "expired_unfunded"].includes(verdict.state)) {
      const ms = bitrefillExpiry ? Date.parse(bitrefillExpiry) : NaN;
      if (Number.isFinite(ms) && ms <= Date.now()) {
        state = "invoice_expired";
        terminal = true;
        detail = "The Bitrefill invoice has expired. Do NOT fund this order; create a fresh invoice.";
      } else if (!bitrefillExpiry && verdict.state === "awaiting_deposit") {
        state = "deadline_unknown";
        detail = "The Bitrefill invoice deadline is unknown on this machine, so this order is NOT shown as payable. Re-run pay with the invoice details, or create a fresh invoice.";
      }
    }
  }
  return {
    provider,
    rozoPaymentId: id,
    rozoPaymentIdSource: idSource,
    // Without the authoritative payment object we are reading a partial view.
    authoritativeView: Boolean(payment),
    linkId: linkId || status?.pl_id || null,
    state,
    unknown: verdict.unknown,
    moneyDetected: verdict.moneyDetected || zecMoney,
    terminal,
    escalate,
    detail,
    backend: {
      paymentStatus: payment?.status ?? status?.rozoPayment?.status ?? null,
      routerStatus: verdict.routerStatus,
      coinbaseSettled: status?.coinbase?.settled ?? null,
      coinbaseStatus: status?.coinbase?.status ?? null
    },
    payin: {
      expected: source.amount ? formatAmount(source) : null,
      received: source.amountReceived ?? null,
      receipt: verdict.receipt,
      txHash: publicHash(source.txHash ?? null),
      confirmedAt: source.confirmedAt ?? null,
      senderAddressMasked: source.senderAddress ? maskAddress(source.senderAddress) : null,
      chain: source.chainId ? chainName(source.chainId) : null,
      // Shielded ZEC only: the custody rail's own view of the pay-in.
      ...zec ? { zec } : {}
    },
    expiry: (() => {
      if (provider === "bitrefill" && !bitrefillExpiry) {
        return { expiresAt: null, expiresIn: null, msRemaining: null, deadlineUnknown: true };
      }
      const iso = provider === "bitrefill" ? bitrefillExpiry : payment?.expiresAt ?? status?.rozoPayment?.expiresAt ?? null;
      if (!iso) return { expiresAt: null, expiresIn: null, msRemaining: null };
      const ms = Date.parse(iso) - Date.now();
      const lockMs = quoteExpiresAt ? Date.parse(quoteExpiresAt) - Date.now() : NaN;
      return {
        expiresAt: iso,
        expiresIn: formatRemaining(ms),
        msRemaining: Number.isFinite(ms) ? ms : null,
        // Native orders: the order stays open after the price lock, but a
        // payment after it is valued at the arrival price. Pay before this.
        ...native || isZec ? {
          quoteExpiresAt: quoteExpiresAt ?? null,
          priceLockExpiresIn: Number.isFinite(lockMs) ? formatRemaining(lockMs) : null
        } : {}
      };
    })(),
    payout: {
      txHash: publicHash(payment?.destination?.txHash ?? status?.rozoPayment?.destination?.txHash ?? null),
      confirmedAt: payment?.destination?.confirmedAt ?? status?.rozoPayment?.destination?.confirmedAt ?? null
    },
    localSend: localSendFor(id),
    // Never a send window once the custody rail has seen a ZEC pay-in.
    sendWindow: state === "awaiting_deposit" && !zecMoney ? sendWindowFor({ provider, chainId: source.chainId, payment, status, bitrefillExpiry, quoteExpiresAt }) : null,
    errors: [statusError, paymentError].filter(Boolean)
  };
}
var EXPIRED_UNFUNDED_GUIDANCE = "This order expired before any funds arrived. First check your own wallet: if anything was sent to the old deposit address, or a Lightning payment is still pending, do not pay again; contact support with the linkId and rozoPaymentId (the router cannot see a pending Lightning payment). If nothing was sent, re-run the same pay on the same link with the same --with: it creates a new order for this link. If pay answers PAYMENT_EXPIRED with retryable: true, the old order cannot be verified yet; wait a few minutes and retry. If it answers LINK_USED_OR_EXPIRED, or PAYMENT_EXPIRED with confirmed: true, this link cannot be paid any more; get a new payment link from the merchant (OpenRouter). If it answers ORDER_ALREADY_ACTIVE, a payment was found: do not pay again; contact support.";
function statusGuidance(result) {
  if (result.escalate) {
    return "MONEY DETECTED and the order is not on a healthy path. Do NOT pay again and do NOT create a new order for this link. Preserve linkId, rozoPaymentId and every tx hash, then escalate to the operator for manual reconciliation.";
  }
  if (result.unknown) {
    return "The order state could not be established. This is NOT evidence that nothing was paid \u2014 do not create a new order and do not send again on the strength of it. Retry, or pass --rozo-payment-id so the authoritative pay-in view can be read.";
  }
  if (!result.authoritativeView) {
    return "Only the fulfilment view was readable; the pay-in view is unavailable, so the money-detected rule cannot be enforced. Pass --rozo-payment-id for a complete answer.";
  }
  if ((result.state === "expired_unfunded" || result.state === "invoice_expired") && result.provider === "bitrefill") {
    return "Nothing was funded, so nothing was lost. Create a fresh Bitrefill invoice and run rozo-checkout pay --bitrefill-invoice <id> --to <0x\u2026> --amount <USDC> --with <coin>";
  }
  if (result.state === "expired_unfunded") return EXPIRED_UNFUNDED_GUIDANCE;
  return result.terminal ? "Done." : "Still in flight. Poll again in ~10s.";
}

// scripts/src/resume.mjs
var PAID_STATES = /* @__PURE__ */ new Set([
  "payin_detected",
  "payin_confirmed",
  "bridging",
  "paying_coinbase",
  "settled"
]);
var EXPIRED_STATES = /* @__PURE__ */ new Set(["expired_unfunded", "invoice_expired"]);
function localPaymentLink(id) {
  try {
    return readState(id)?.paymentLink ?? null;
  } catch {
    return null;
  }
}
function resumeVerdict(snap) {
  const base = {
    rozoPaymentId: snap.rozoPaymentId,
    linkId: snap.linkId ?? null,
    provider: snap.provider,
    state: snap.state,
    moneyDetected: Boolean(snap.moneyDetected)
  };
  if (snap.escalate) {
    return { ...base, resumable: false, outcome: "needs_attention", code: "ORDER_NEEDS_ATTENTION", exitCode: EXIT_ERROR, message: statusGuidance(snap) };
  }
  if (snap.unknown || !snap.authoritativeView) {
    return { ...base, resumable: false, outcome: "unknown", code: "ORDER_STATE_UNKNOWN", exitCode: EXIT_ERROR, message: statusGuidance(snap) };
  }
  if (snap.moneyDetected || PAID_STATES.has(snap.state)) {
    const done = snap.state === "settled";
    return {
      ...base,
      resumable: false,
      outcome: done ? "paid" : "paid_in_progress",
      code: "ORDER_ALREADY_PAID",
      exitCode: EXIT_OK,
      message: done ? "This order is already paid and settled. Nothing to resume. Do not pay again." : `A payment for this order was already detected (state: ${snap.state}). Do NOT pay again. Follow it with: rozo-checkout status ${snap.rozoPaymentId} --watch`
    };
  }
  if (EXPIRED_STATES.has(snap.state)) {
    return {
      ...base,
      resumable: false,
      outcome: "expired",
      code: "ORDER_EXPIRED",
      exitCode: EXIT_ERROR,
      message: snap.provider === "bitrefill" ? "This order expired before any funds arrived. Nothing was lost. Create a fresh Bitrefill invoice and run pay again." : EXPIRED_UNFUNDED_GUIDANCE
    };
  }
  if (snap.localSend) {
    return {
      ...base,
      resumable: false,
      outcome: "sent_locally",
      code: "ALREADY_SENT",
      exitCode: EXIT_ERROR,
      message: `This machine already recorded a send for this order (${snap.localSend.status}). Do NOT pay again. Check it with: rozo-checkout status ${snap.rozoPaymentId}`
    };
  }
  if (snap.state !== "awaiting_deposit") {
    return {
      ...base,
      resumable: false,
      outcome: "not_payable",
      code: "ORDER_NOT_RESUMABLE",
      exitCode: EXIT_ERROR,
      message: `This order is in state "${snap.state}" and cannot be paid now. ${statusGuidance(snap)}`
    };
  }
  if (!snap.sendWindow?.ok) {
    return {
      ...base,
      resumable: false,
      outcome: "expired",
      code: snap.sendWindow?.code ?? "SEND_WINDOW_CLOSED",
      exitCode: EXIT_ERROR,
      message: `${snap.sendWindow?.reason ?? "Not enough time is left to pay this order safely."} Do not fund it. Let it expire unfunded, then create a new order for the same link.`
    };
  }
  return { ...base, resumable: true, outcome: "awaiting_deposit", code: null, exitCode: EXIT_OK, message: null };
}
async function main(argv) {
  const args = parseArgs(argv);
  const rozoPaymentId = args["rozo-payment-id"] || args._[0];
  if (!rozoPaymentId || rozoPaymentId === true) usage("Required: <rozoPaymentId> (the order id printed by pay)");
  if (!isRozoPaymentId(String(rozoPaymentId))) {
    usage("resume takes the order id (rozoPaymentId, a UUID) printed by pay, not a payment link.");
  }
  const id = String(rozoPaymentId);
  const confirmed = Boolean(args.confirm);
  let blacklist;
  try {
    blacklist = loadBlacklist();
  } catch (err) {
    throw new SkillError("BLACKLIST_UNAVAILABLE", `Compromised-address list unusable: ${err.message} Refusing to proceed.`);
  }
  const snap = await snapshot({ rozoPaymentId: id });
  const verdict = resumeVerdict(snap);
  if (!verdict.resumable) {
    emit(
      {
        success: verdict.exitCode === EXIT_OK,
        step: "resume",
        resumable: false,
        outcome: verdict.outcome,
        rozoPaymentId: id,
        linkId: verdict.linkId,
        state: verdict.state,
        moneyDetected: verdict.moneyDetected,
        ...verdict.exitCode === EXIT_OK ? { message: verdict.message } : { error: { code: verdict.code, message: verdict.message } },
        payin: snap.payin,
        ...verdict.exitCode === EXIT_OK ? {} : { support: SUPPORT }
      },
      verdict.exitCode
    );
  }
  const payment = await getPayment(id);
  const source = payment?.source || {};
  const resumedShielded = isZecSource(source.chainId, source.tokenSymbol) && zecStatusOf(source)?.receive === "shielded";
  const guard = reuseGuard({
    payment,
    requested: { chainId: source.chainId, tokenSymbol: source.tokenSymbol, ...resumedShielded ? { shielded: true } : {} },
    reused: true
  });
  if (!guard.ok) {
    emit(
      {
        success: false,
        step: "resume",
        resumable: false,
        outcome: guard.moneyDetected ? "paid_in_progress" : "not_payable",
        rozoPaymentId: id,
        moneyDetected: guard.moneyDetected,
        error: { code: guard.code, message: guard.reason },
        guidance: guard.moneyDetected ? "A payment for this order was detected. Do NOT pay again." : "This order cannot be paid as it stands. Do not fund it.",
        support: SUPPORT
      },
      EXIT_ERROR
    );
  }
  const native = isNativeSource(source.chainId, source.tokenSymbol);
  const isZec = isZecSource(source.chainId, source.tokenSymbol);
  const zecStatus = isZec ? zecStatusOf(source) : null;
  const zec = Boolean(zecStatus && zecStatus.receive === "shielded");
  const quoteExpiresAt = isZec ? zecStatus?.quoteExpiresAt ?? null : priceLockFor({ native, payment, others: [snap.expiry?.quoteExpiresAt] });
  const finalWindow = checkExpiry({
    now: Date.now(),
    chainId: source.chainId,
    intentExpiresAt: payment?.expiresAt ?? snap.sendWindow?.deadlineMs,
    coinbaseExpiry: snap.sendWindow?.deadlineMs,
    ...native || isZec ? { quoteExpiresAt } : {}
  });
  if (!finalWindow.ok) {
    emit(
      {
        success: false,
        step: "resume",
        resumable: false,
        outcome: "expired",
        rozoPaymentId: id,
        moneyDetected: false,
        error: { code: finalWindow.code, message: finalWindow.reason },
        guidance: "Not enough time is left to pay this order safely. Do not fund it; let it expire unfunded and create a new order.",
        support: SUPPORT
      },
      EXIT_ERROR
    );
  }
  const lightning = String(source.chainId) === "lightning";
  if (!lightning) {
    try {
      assertNotBlacklisted(
        [{ address: source.receiverAddress, family: chainFamily(source.chainId), role: "deposit address" }],
        blacklist
      );
    } catch (err) {
      emit(
        {
          success: false,
          step: "resume",
          resumable: false,
          rozoPaymentId: id,
          error: { code: err.code, message: err.message },
          guidance: "Do NOT send anything. Report this to the operator immediately.",
          support: SUPPORT
        },
        EXIT_ERROR
      );
    }
  }
  const expiresAt = payment?.expiresAt ?? snap.expiry?.expiresAt ?? null;
  const msRemaining = Number.isFinite(finalWindow.effectiveDeadlineMs) ? finalWindow.effectiveDeadlineMs - Date.now() : NaN;
  const expiresIn = Number.isFinite(msRemaining) ? formatRemaining(msRemaining) : null;
  const paymentLink = payment?.paymentLink ?? localPaymentLink(id);
  const bolt11 = source.lnInvoice ?? payment?.lnInvoice ?? null;
  emit({
    success: true,
    step: "resume",
    resumable: true,
    outcome: "awaiting_deposit",
    confirmed,
    rozoPaymentId: id,
    linkId: snap.linkId ?? payment?.orderId ?? null,
    provider: snap.provider,
    state: snap.state,
    // Hosted pay page for this order: a human can open it and pay from there.
    // Shown in full only for Rozo's own pay-page hosts; anything else is
    // reduced to its host by the normal output redaction.
    paymentLink: publicPayPage(paymentLink),
    deposit: confirmed ? {
      chainId: source.chainId,
      chain: chainName(source.chainId),
      tokenSymbol: source.tokenSymbol,
      tokenAddress: source.tokenAddress || null,
      receiverAddress: lightning ? null : source.receiverAddress,
      receiverMemo: source.receiverMemo ?? null,
      receiverMemoType: source.receiverMemo ? STELLAR_MEMO_TYPE : null,
      amount: source.amount,
      amountUnit: source.amountUnit ?? null,
      isSats: isSatsUnit(source.amountUnit),
      lnInvoice: bolt11 || null,
      payTo: guard.deposit.payTo,
      expiresAt,
      expiresIn,
      native,
      exactOut: native || lightning || zec,
      quoteExpiresAt: native || zec ? quoteExpiresAt : null,
      ...zec ? {
        shielded: true,
        paymentUri: guard.deposit.paymentUri,
        requiredConfirmations: zecStatus.requiredConfirmations,
        payinState: zecStatus.payinState
      } : {}
    } : null,
    depositWithheld: !confirmed,
    display: {
      chain: chainName(source.chainId),
      token: source.tokenSymbol,
      amount: formatAmount(source),
      isSats: isSatsUnit(source.amountUnit),
      payToMasked: maskAddress(guard.deposit.payTo),
      receiverMemoMasked: maskMemo(source.receiverMemo),
      hasMemo: Boolean(source.receiverMemo),
      memoType: source.receiverMemo ? STELLAR_MEMO_TYPE : null,
      native,
      priceLockedUntil: native || zec ? quoteExpiresAt : null,
      ...zec ? { shielded: true } : {}
    },
    expiry: {
      expiresAt,
      expiresIn,
      ...native || zec ? { quoteExpiresAt } : {},
      minutesOfSlack: snap.sendWindow?.minutesOfSlack ?? null
    },
    note: confirmed ? "Send exactly once, exactly this amount, on this chain. Then: rozo-checkout status <id> --watch" : "Deposit address withheld. Confirm the chain, token and amount with the payer, then re-run with --confirm, or open paymentLink."
  });
}
async function run(argv = process.argv.slice(2)) {
  return main(argv);
}

// scripts/src/bin/resume.mjs
run().catch((err) => fail(err));
