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
var IdError = class extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
};
var PL_RE = /(pl_[0-9a-zA-Z]+)/;
var SESSION_RE = /(paymentSession_[A-Za-z0-9_-]+)/;
function extractLinkId(urlOrId) {
  if (typeof urlOrId !== "string" || !urlOrId.trim()) {
    throw new IdError("BAD_LINK", "A Coinbase payment link URL or id is required.");
  }
  const s = urlOrId.trim();
  const session = s.match(SESSION_RE);
  if (session) return { linkId: session[1], kind: "payment_session" };
  const link = s.match(PL_RE);
  if (link) return { linkId: link[1], kind: "payment_link" };
  if (/commerce\.coinbase\.com\/pay\//.test(s)) {
    throw new IdError(
      "LEGACY_COMMERCE_URL",
      "commerce.coinbase.com/pay/<uuid> uses the legacy protocol; this skill does not handle it."
    );
  }
  throw new IdError(
    "BAD_LINK",
    "Could not find a `pl_*` or `paymentSession_*` id in the supplied value."
  );
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
function postJson(url, body, opts) {
  return request("POST", url, { ...opts, body });
}

// scripts/src/lib/api.mjs
var MPP_BASE = process.env.ROZO_CHECKOUT_MPP_BASE || "https://apiserver.mpprouter.dev/v1/services/rozo-agent-api";
var CLIENT_LABEL = `rozo-checkout-cli/${PKG_VERSION}`;
var ATTRIBUTION_CLIENT = `rozo-checkout-skill/${PKG_VERSION}`;
var INTENTS_BASE = process.env.ROZO_CHECKOUT_INTENTS_BASE || "https://intentapiv4.rozo.ai/functions/v1/payment-api";
async function quoteInvoice({ url, linkId, beta }) {
  const body = url ? { url } : { payment_id: linkId };
  return postJson(withBeta(`${MPP_BASE}/quote-invoice`, beta), body);
}
function withBeta(url, beta) {
  if (!beta) return url;
  const u = new URL(url);
  u.searchParams.set("beta", beta);
  return u.toString();
}
function snapshotFromQuote(quote) {
  const cb = quote?.coinbasePayment || quote?.paymentLink || null;
  return {
    linkId: quote?.linkId ?? quote?.paymentId ?? null,
    protocolVersion: quote?.protocolVersion ?? null,
    merchant: quote?.merchant ?? null,
    original: quote?.invoice?.amount ?? null,
    // The router's own pricing block (top level). quote.quote.callerPays is the
    // upstream invoice quote and never includes the Rozo service fee, so it is
    // only a fallback for a router that states no pricing at all.
    quotedOriginal: quote?.original ?? null,
    callerPays: quote?.callerPays ?? quote?.quote?.callerPays ?? null,
    serviceFee: quote?.serviceFee ?? null,
    feeBps: quote?.feeBps ?? null,
    fiat: quote?.invoice?.fiat ?? null,
    coinbase: cb ? {
      id: cb.id ?? null,
      status: cb.status ?? null,
      usageCount: cb.usageCount ?? null,
      maxUsage: cb.maxUsage ?? null,
      preApprovalExpiry: cb.preApprovalExpiry ?? cb.expiresAt ?? null
    } : null
  };
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
var SUPPORTED_SOURCES = [
  { chainId: "1", chain: "Ethereum", tokens: ["USDC", "USDT", "ETH"] },
  { chainId: "56", chain: "BNB Chain", tokens: ["USDC", "USDT", "BNB"] },
  { chainId: "137", chain: "Polygon", tokens: ["USDC", "USDT", "POL"] },
  { chainId: "900", chain: "Solana", tokens: ["USDC", "USDT", "SOL"] },
  { chainId: "8453", chain: "Base", tokens: ["USDC", "ETH"] },
  { chainId: "42161", chain: "Arbitrum", tokens: ["USDC", "USDT", "ETH"] },
  { chainId: "1500", chain: "Stellar", tokens: ["USDC"] },
  { chainId: "lightning", chain: "Bitcoin Lightning", tokens: ["BTC"] },
  // ZEC (Beta): shielded orders only, offered per invoice by the router (see lib/zec.mjs).
  { chainId: "9133", chain: "Zcash", tokens: ["ZEC"] }
];
var NATIVE_COINS = Object.freeze({
  "1:ETH": { chainId: "1", symbol: "ETH", decimals: 18 },
  "8453:ETH": { chainId: "8453", symbol: "ETH", decimals: 18 },
  "42161:ETH": { chainId: "42161", symbol: "ETH", decimals: 18 },
  "56:BNB": { chainId: "56", symbol: "BNB", decimals: 18 },
  "137:POL": { chainId: "137", symbol: "POL", decimals: 18 },
  "900:SOL": { chainId: "900", symbol: "SOL", decimals: 9 }
});
var NATIVE_MAX_USD = 3500;
var NATIVE_MIN_USD_FALLBACK = Object.freeze({ "1:ETH": 1 });
var AmountError = class extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
};
function decimalsKey(chainId, tokenSymbol) {
  return `${String(chainId).trim()}:${String(tokenSymbol || "").trim().toUpperCase()}`;
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
function chainName(chainId) {
  return CHAIN_NAMES[String(chainId)] || CHAIN_NAMES[chainId] || `chain ${chainId}`;
}
function isSupportedSource(chainId, tokenSymbol) {
  const cid = String(chainId).trim();
  const sym = String(tokenSymbol || "").trim().toUpperCase();
  return SUPPORTED_SOURCES.some((s) => s.chainId === cid && s.tokens.includes(sym));
}
function isNativeSource(chainId, tokenSymbol) {
  return Object.prototype.hasOwnProperty.call(NATIVE_COINS, decimalsKey(chainId, tokenSymbol));
}
function nativeMinUsdFor(chainId, tokenSymbol, quoteNativeMinUsd) {
  const cid = String(chainId).trim();
  const sym = String(tokenSymbol || "").trim().toUpperCase();
  const fromQuote = quoteNativeMinUsd?.[cid]?.[sym];
  const n = Number(fromQuote);
  if (fromQuote !== void 0 && fromQuote !== null && Number.isFinite(n) && n > 0) return n;
  return NATIVE_MIN_USD_FALLBACK[`${cid}:${sym}`] ?? null;
}
function nativeOfferFor({ chainId, tokenSymbol, supportedSources, nativeMinUsd, callerPaysUsd }) {
  const cid = String(chainId).trim();
  const sym = String(tokenSymbol || "").trim().toUpperCase();
  const label = `${sym} on ${chainName(cid)}`;
  const minUsd = nativeMinUsdFor(cid, sym, nativeMinUsd);
  if (!isNativeSource(cid, sym)) {
    return { ok: false, code: "NOT_NATIVE", reason: `${label} is not a native coin.`, minUsd: null };
  }
  const list = supportedSources && typeof supportedSources === "object" ? supportedSources[cid] : null;
  if (!Array.isArray(list) || !list.map((t) => String(t).toUpperCase()).includes(sym)) {
    return {
      ok: false,
      code: "NATIVE_NOT_OFFERED",
      reason: `${label} is not offered for this invoice. Pay with USDC or USDT instead.`,
      minUsd
    };
  }
  const usd = Number(callerPaysUsd);
  if (!Number.isFinite(usd) || usd <= 0) {
    return {
      ok: false,
      code: "NATIVE_AMOUNT_UNKNOWN",
      reason: `The quote carries no USD amount, so ${label} cannot be checked against the native limits. Pay with USDC or USDT instead.`,
      minUsd
    };
  }
  {
    if (usd > NATIVE_MAX_USD) {
      return {
        ok: false,
        code: "NATIVE_AMOUNT_TOO_HIGH",
        reason: `Native coin orders are limited to $${NATIVE_MAX_USD} per invoice; this one is $${usd}. Pay with USDC or USDT instead.`,
        minUsd
      };
    }
    if (minUsd !== null && usd < minUsd) {
      return {
        ok: false,
        code: "NATIVE_AMOUNT_TOO_LOW",
        reason: `${label} needs an invoice of at least $${minUsd}; this one is $${usd}. Pay with another coin.`,
        minUsd
      };
    }
  }
  return { ok: true, code: null, reason: null, minUsd };
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

// scripts/src/lib/zec.mjs
var ZEC_CHAIN_ID = "9133";
var ZEC_SYMBOL = "ZEC";
var ZEC_SOURCE_META_KEY = "ZEC@9133";
var ZEC_BETA_PARAM = "zec,zec_shielded";
var ZEC_SHIELDED_MAX_USD = 1200;
var ZEC_MIN_USD = 5;
var ZEC_TWO_CONF_FROM_USD = 110;
function isZecSource(chainId, tokenSymbol) {
  return String(chainId ?? "").trim() === ZEC_CHAIN_ID && String(tokenSymbol ?? "").trim().toUpperCase() === ZEC_SYMBOL;
}
function zecRequiredConfirmations(usd) {
  const n = Number(usd);
  return Number.isFinite(n) && n >= ZEC_TWO_CONF_FROM_USD ? 2 : 1;
}
function zecShieldedOfferFor({ supportedSources, sourceMeta, callerPaysUsd }) {
  const list = supportedSources && typeof supportedSources === "object" ? supportedSources[ZEC_CHAIN_ID] : null;
  if (!Array.isArray(list) || !list.map((t) => String(t).toUpperCase()).includes(ZEC_SYMBOL)) {
    return {
      ok: false,
      code: "ZEC_NOT_OFFERED",
      reason: "ZEC is not offered for this invoice. Pay with USDC or USDT instead.",
      requiredConfirmations: null
    };
  }
  const meta = sourceMeta && typeof sourceMeta === "object" ? sourceMeta[ZEC_SOURCE_META_KEY] : null;
  const available = meta && typeof meta === "object" && (meta.shieldedAvailable === true || meta.shielded_available === true);
  if (!available) {
    return {
      ok: false,
      code: "ZEC_SHIELDED_NOT_AVAILABLE",
      reason: "Paying from a shielded balance is not available for this invoice right now.",
      requiredConfirmations: null
    };
  }
  const usd = Number(callerPaysUsd);
  if (!Number.isFinite(usd) || usd <= 0) {
    return {
      ok: false,
      code: "ZEC_AMOUNT_UNKNOWN",
      reason: "The quote carries no USD amount, so the shielded ZEC limits cannot be checked. Pay with USDC or USDT instead.",
      requiredConfirmations: null
    };
  }
  if (usd > ZEC_SHIELDED_MAX_USD) {
    return {
      ok: false,
      code: "ZEC_AMOUNT_TOO_HIGH",
      reason: `Shielded ZEC is limited to $${ZEC_SHIELDED_MAX_USD} per payment during the beta; this invoice is $${usd}. Pay with USDC or USDT instead.`,
      requiredConfirmations: null
    };
  }
  if (usd < ZEC_MIN_USD) {
    return {
      ok: false,
      code: "ZEC_AMOUNT_TOO_LOW",
      reason: `ZEC payments need an invoice of at least $${ZEC_MIN_USD}; this one is $${usd}. Pay with another coin.`,
      requiredConfirmations: null
    };
  }
  return { ok: true, code: null, reason: null, requiredConfirmations: zecRequiredConfirmations(usd) };
}

// scripts/src/lib/guards.mjs
function checkQuotePricing(snapshot) {
  if (snapshot?.quotedOriginal !== void 0 && snapshot?.quotedOriginal !== null && normalizeDecimal(snapshot.quotedOriginal) !== normalizeDecimal(snapshot.original)) {
    return {
      ok: false,
      code: "PRICING_VIOLATION",
      reason: `The quote's amount (${snapshot.quotedOriginal}) differs from the invoice amount (${snapshot.original}).`,
      field: "original",
      value: String(snapshot.quotedOriginal),
      drift: []
    };
  }
  return checkPricing(snapshot);
}
var MAX_SERVICE_FEE_BPS = 100;
var USDC_DECIMALS = 6;
var ATOMIC_PER_CENT = 10000n;
function serviceFeeAtomicFor(originalAtomic, feeBps) {
  if (feeBps === 0 || originalAtomic === 0n) return 0n;
  const divisor = 10000n * ATOMIC_PER_CENT;
  return (originalAtomic * BigInt(feeBps) + divisor - 1n) / divisor * ATOMIC_PER_CENT;
}
function formatAtomicUsd(atomic) {
  const whole = atomic / 1000000n;
  const frac = (atomic % 1000000n).toString().padStart(USDC_DECIMALS, "0").replace(/0+$/, "");
  return frac ? `${whole}.${frac}` : whole.toString();
}
function parseFeeBps(v) {
  if (typeof v === "number") return Number.isSafeInteger(v) ? v : NaN;
  if (typeof v === "string" && /^\d+$/.test(v.trim())) return Number(v.trim());
  return NaN;
}
function checkPricing(obj) {
  const bad = (code, field, value, reason) => ({ ok: false, code, reason, field, value: value ?? null, drift: [] });
  const disc = obj?.discount;
  if (disc !== void 0 && disc !== null && normalizeDecimal(disc) !== "0") {
    return bad("NO_DISCOUNT_VIOLATION", "discount", String(disc), `Server reported a discount of "${disc}"; this flow must charge the full invoice.`);
  }
  const parse = (field) => {
    const raw = defaultNormalize(obj?.[field]);
    if (raw === null) return { missing: true };
    try {
      return { atomic: toAtomic(raw, USDC_DECIMALS) };
    } catch {
      return { invalid: raw };
    }
  };
  const original = parse("original");
  const callerPays = parse("callerPays");
  for (const [field, v] of [["original", original], ["callerPays", callerPays]]) {
    if (v.missing) return bad("PRICING_VIOLATION", field, null, `The ${field} amount is missing.`);
    if (v.invalid !== void 0) return bad("PRICING_VIOLATION", field, v.invalid, `The ${field} amount "${v.invalid}" is not a USD amount.`);
  }
  const feeGiven = defaultNormalize(obj?.serviceFee) !== null;
  const bpsGiven = obj?.feeBps !== void 0 && obj?.feeBps !== null && String(obj.feeBps).trim() !== "";
  let feeAtomic = 0n;
  let feeBps = 0;
  if (feeGiven || bpsGiven) {
    if (!feeGiven || !bpsGiven) {
      return bad(
        "PRICING_VIOLATION",
        feeGiven ? "feeBps" : "serviceFee",
        null,
        "The server stated a service fee without its rate, or a rate without the fee. Refusing to guess."
      );
    }
    feeBps = parseFeeBps(obj.feeBps);
    if (!Number.isSafeInteger(feeBps) || feeBps < 0 || feeBps > MAX_SERVICE_FEE_BPS) {
      return bad(
        "PRICING_VIOLATION",
        "feeBps",
        String(obj.feeBps),
        `Service fee rate ${obj.feeBps} bps is outside 0..${MAX_SERVICE_FEE_BPS} bps; this CLI does not accept it.`
      );
    }
    const fee = parse("serviceFee");
    if (fee.invalid !== void 0) return bad("PRICING_VIOLATION", "serviceFee", fee.invalid, `The service fee "${fee.invalid}" is not a USD amount.`);
    feeAtomic = fee.atomic;
    const expected = serviceFeeAtomicFor(original.atomic, feeBps);
    if (feeAtomic !== expected) {
      return bad(
        "PRICING_VIOLATION",
        "serviceFee",
        String(obj.serviceFee),
        `Service fee ${obj.serviceFee} is not ${feeBps} bps of ${obj.original} (expected ${formatAtomicUsd(expected)}).`
      );
    }
  }
  if (callerPays.atomic !== original.atomic + feeAtomic) {
    return bad(
      "PRICING_VIOLATION",
      "callerPays",
      String(obj.callerPays),
      `callerPays (${obj.callerPays}) is not the invoice amount (${obj.original}) plus the stated service fee (${formatAtomicUsd(feeAtomic)}).`
    );
  }
  return {
    ok: true,
    code: null,
    reason: null,
    pricing: {
      original: formatAtomicUsd(original.atomic),
      serviceFee: formatAtomicUsd(feeAtomic),
      callerPays: formatAtomicUsd(callerPays.atomic),
      feeBps
    }
  };
}
function defaultNormalize(v) {
  if (v === null || v === void 0) return null;
  const s = String(v).trim();
  return s === "" ? null : s;
}
function normalizeDecimal(v) {
  if (v === null || v === void 0) return null;
  const s = String(v).trim();
  if (!/^\d+(\.\d+)?$/.test(s)) return s;
  const [w, f = ""] = s.split(".");
  const frac = f.replace(/0+$/, "");
  const whole = w.replace(/^0+(?=\d)/, "");
  return frac ? `${whole}.${frac}` : whole;
}

// scripts/src/quote.mjs
function derivePayable(snapshot, now) {
  const cb = snapshot.coinbase;
  if (!cb) {
    return { payable: false, code: "LINK_NO_LONGER_PAYABLE", reason: "No Coinbase state in the quote." };
  }
  if (snapshot.protocolVersion === "v3" && cb.status && cb.status !== "PAYMENT_SESSION_STATUS_CREATED") {
    return {
      payable: false,
      code: "LINK_NO_LONGER_PAYABLE",
      reason: `Payment Session status is ${cb.status}; only PAYMENT_SESSION_STATUS_CREATED is payable.`
    };
  }
  if (cb.usageCount !== null && cb.usageCount !== void 0) {
    const max = cb.maxUsage ?? 1;
    if (Number(cb.usageCount) >= Number(max)) {
      return {
        payable: false,
        code: "LINK_NO_LONGER_PAYABLE",
        reason: `This payment link has already been used (${cb.usageCount}/${max}).`
      };
    }
  }
  const exp = parseDeadline(cb.preApprovalExpiry);
  if (exp === null) {
    return {
      payable: false,
      code: "EXPIRY_UNPARSABLE",
      reason: "The Coinbase expiry is missing or unparsable; refusing to treat it as payable."
    };
  }
  if (exp <= now) {
    return {
      payable: false,
      code: "LINK_NO_LONGER_PAYABLE",
      reason: `This payment link expired at ${new Date(exp).toISOString()}. Ask for a fresh one.`
    };
  }
  return { payable: true, code: null, reason: null, expiryMs: exp };
}
async function main(argv) {
  const args = parseArgs(argv);
  const url = args.url || args._[0];
  if (!url || url === true) {
    usage('Required: --url "<coinbase payment link or paymentSession url/id>"');
  }
  const { linkId, kind } = extractLinkId(String(url));
  let chosenSource = null;
  if (args.chain || args.token) {
    const chainId = String(args.chain ?? "").trim();
    const tokenSymbol = String(args.token ?? "").trim().toUpperCase();
    if (!chainId || !tokenSymbol) {
      usage("--chain and --token must be given together, e.g. --chain 900 --token USDT");
    }
    if (!isSupportedSource(chainId, tokenSymbol)) {
      throw new SkillError(
        "UNSUPPORTED_SOURCE",
        `${tokenSymbol} on ${chainName(chainId)} is not a supported source.`,
        { supported: SUPPORTED_SOURCES }
      );
    }
    chosenSource = { chainId, tokenSymbol };
  }
  const now = Date.now();
  const quote = await quoteInvoice({ url: String(url), beta: ZEC_BETA_PARAM });
  const snapshot = snapshotFromQuote(quote);
  const payability = derivePayable(snapshot, now);
  const nativeOffered = Object.values(NATIVE_COINS).map((c) => ({
    chainId: c.chainId,
    tokenSymbol: c.symbol,
    chain: chainName(c.chainId),
    offer: nativeOfferFor({
      chainId: c.chainId,
      tokenSymbol: c.symbol,
      supportedSources: quote?.supportedSources,
      nativeMinUsd: quote?.nativeMinUsd,
      callerPaysUsd: snapshot.callerPays ?? snapshot.original
    })
  })).filter((c) => c.offer.ok).map((c) => ({ chainId: c.chainId, tokenSymbol: c.tokenSymbol, chain: c.chain, minUsd: c.offer.minUsd }));
  const zecOffer = zecShieldedOfferFor({
    supportedSources: quote?.supportedSources,
    sourceMeta: quote?.sourceMeta,
    callerPaysUsd: snapshot.callerPays ?? snapshot.original
  });
  const zecShielded = {
    offered: zecOffer.ok,
    code: zecOffer.code,
    reason: zecOffer.reason,
    requiredConfirmations: zecOffer.requiredConfirmations,
    maxUsd: ZEC_SHIELDED_MAX_USD,
    note: "ZEC (Beta) is paid from a shielded wallet, exact amount in one transaction; the CLI shows the address, amount and payment URI and never sends. Underpayments are not refunded automatically."
  };
  const zecRequested = chosenSource && isZecSource(chosenSource.chainId, chosenSource.tokenSymbol) ? zecOffer : null;
  const nativeRequested = chosenSource && isNativeSource(chosenSource.chainId, chosenSource.tokenSymbol) ? nativeOfferFor({
    ...chosenSource,
    supportedSources: quote?.supportedSources,
    nativeMinUsd: quote?.nativeMinUsd,
    callerPaysUsd: snapshot.callerPays ?? snapshot.original
  }) : null;
  const pricing = checkQuotePricing(snapshot);
  const payload = {
    success: payability.payable,
    step: "quote",
    linkId: snapshot.linkId ?? linkId,
    linkKind: kind,
    protocolVersion: snapshot.protocolVersion,
    merchant: snapshot.merchant,
    invoice: {
      amount: snapshot.original,
      fiat: snapshot.fiat
    },
    // No discount on this line. callerPays is the total to pay: the invoice
    // amount plus the Rozo service fee the router states (serviceFee, feeBps).
    callerPays: pricing.ok ? pricing.pricing.callerPays : snapshot.callerPays,
    serviceFee: pricing.ok ? pricing.pricing.serviceFee : snapshot.serviceFee ?? null,
    feeBps: pricing.ok ? pricing.pricing.feeBps : snapshot.feeBps ?? null,
    discountPolicy: "none: callerPays is the invoice amount plus the stated service fee",
    coinbase: snapshot.coinbase,
    coinbaseExpiryIso: payability.expiryMs ? new Date(payability.expiryMs).toISOString() : null,
    chosenSource,
    supportedSources: SUPPORTED_SOURCES,
    // The router's own per-invoice list ({ chainId: [symbols] }), verbatim,
    // and the native coins it makes payable for this invoice.
    routerSupportedSources: quote?.supportedSources && typeof quote.supportedSources === "object" ? quote.supportedSources : null,
    nativeOffered,
    zecShielded,
    nativeNote: "Native coins are exact-out: the coin amount is fixed at order creation and its price is locked only until quoteExpiresAt. Up to $3,500 per invoice; native ETH on Ethereum needs $1.",
    quoteReceipt: quote?.quoteReceipt ?? null,
    quoteReceiptTtlSeconds: 60,
    quoteReceiptNote: "Short-lived (~60s). create-order.js takes its own fresh quote; do not carry this over.",
    snapshot,
    nextStep: payability.payable ? "create-order.js --url <url> --chain <chainId> --token <SYMBOL>" : null
  };
  if (!payability.payable) {
    payload.error = { code: payability.code, message: payability.reason };
    emit(payload, EXIT_ERROR);
  }
  if (nativeRequested && !nativeRequested.ok) {
    payload.success = false;
    payload.nextStep = null;
    payload.error = { code: nativeRequested.code, message: nativeRequested.reason };
    emit(payload, EXIT_ERROR);
  }
  if (zecRequested && !zecRequested.ok) {
    payload.success = false;
    payload.nextStep = null;
    payload.error = { code: zecRequested.code, message: zecRequested.reason };
    emit(payload, EXIT_ERROR);
  }
  if (zecRequested) payload.nextStep = "create-order.js --url <url> --chain 9133 --token ZEC --shielded";
  if (!pricing.ok) {
    payload.success = false;
    payload.nextStep = null;
    payload.error = { code: pricing.code, message: pricing.reason };
    emit(payload, EXIT_ERROR);
  }
  emit(payload);
}
async function run(argv = process.argv.slice(2)) {
  return main(argv);
}

// scripts/src/bin/quote.mjs
run().catch((err) => fail(err));
