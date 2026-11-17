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
var CONTACT_EMAIL_MAX_LENGTH = 254;
var EMAIL_RE = /^[a-z0-9][^\s@]*@[^\s@.]+(\.[^\s@.]+)+$/;
function normalizeContactEmail(raw) {
  if (raw === void 0 || raw === null) return null;
  if (typeof raw !== "string") return void 0;
  const email = raw.trim().toLowerCase();
  if (email.length === 0) return null;
  if (email.length > CONTACT_EMAIL_MAX_LENGTH) return void 0;
  if (/[\x00-\x1f\x7f]/.test(email) || !EMAIL_RE.test(email)) return void 0;
  return email;
}
function contactEmailAttached(email, reused) {
  return Boolean(email) && !reused;
}
function contactEmailFromArgs(args) {
  if (args.email === void 0) return null;
  const email = args.email === true ? void 0 : normalizeContactEmail(String(args.email));
  if (email === void 0) {
    const err = new Error(
      "--email must be a valid email address, for example name@example.com. It is optional: leave it out to continue without one."
    );
    err.code = "INVALID_EMAIL";
    throw err;
  }
  return email;
}

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
var UUID_RE = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
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
function assertRozoPaymentId(value) {
  const s = String(value || "").trim();
  if (!UUID_RE.test(s)) {
    throw new IdError("BAD_ROZO_PAYMENT_ID", "rozoPaymentId must be a UUID.");
  }
  return s;
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
function postJson(url, body, opts) {
  return request("POST", url, { ...opts, body });
}

// scripts/src/lib/utm.mjs
function normalizeUtmSource(value) {
  if (typeof value !== "string") return null;
  const s = value.trim().toLowerCase();
  if (!s || s.length > 100 || !/^[a-z0-9][a-z0-9._-]*$/.test(s)) return null;
  return s;
}

// scripts/src/lib/identity.mjs
import crypto2 from "node:crypto";

// scripts/src/lib/prefs.mjs
import fs2 from "node:fs";
import path2 from "node:path";
import os2 from "node:os";

// scripts/src/lib/state.mjs
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
var LOCK_STALE_MS = 6e4;
var LOCK_WAIT_MS = 1e4;
var LOCK_POLL_MS = 25;
function lockPath() {
  return path.join(stateRoot(), ".send.lock");
}
function sleepSync(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}
function tryAcquire(file) {
  try {
    const fd = fs.openSync(file, "wx", 384);
    fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, at: (/* @__PURE__ */ new Date()).toISOString() }));
    fs.closeSync(fd);
    return true;
  } catch (err) {
    if (err.code !== "EEXIST") throw err;
    return false;
  }
}
function withLock(fn) {
  const file = lockPath();
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 448 });
  const deadline = Date.now() + LOCK_WAIT_MS;
  for (; ; ) {
    if (tryAcquire(file)) break;
    try {
      const age = Date.now() - fs.statSync(file).mtimeMs;
      if (age > LOCK_STALE_MS) {
        const stolen = `${file}.stale.${crypto.randomBytes(4).toString("hex")}`;
        try {
          fs.renameSync(file, stolen);
          fs.unlinkSync(stolen);
        } catch {
        }
        continue;
      }
    } catch (err) {
      if (err.code !== "ENOENT") throw err;
      continue;
    }
    if (Date.now() > deadline) {
      throw new SkillError(
        "LOCK_TIMEOUT",
        "Another rozo-checkout process is holding the send lock. Refusing to proceed rather than risk a concurrent second send."
      );
    }
    sleepSync(LOCK_POLL_MS);
  }
  try {
    return fn();
  } finally {
    try {
      fs.unlinkSync(file);
    } catch {
    }
  }
}
function stateRoot() {
  return process.env.ROZO_CHECKOUT_STATE_DIR || path.join(os.homedir(), ".rozo-checkout", "state");
}
function statePath(rozoPaymentId) {
  if (!/^[A-Za-z0-9-]{8,64}$/.test(String(rozoPaymentId || ""))) {
    throw new SkillError("BAD_ROZO_PAYMENT_ID", "Refusing to build a state path from that id.");
  }
  return path.join(stateRoot(), `${rozoPaymentId}.json`);
}
function writeAtomic(file, data) {
  const dir = path.dirname(file);
  fs.mkdirSync(dir, { recursive: true, mode: 448 });
  const tmp = path.join(dir, `.${path.basename(file)}.${crypto.randomBytes(6).toString("hex")}.tmp`);
  const fd = fs.openSync(tmp, "wx", 384);
  try {
    fs.writeFileSync(fd, JSON.stringify(data, null, 2) + "\n", "utf8");
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
  fs.renameSync(tmp, file);
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
function createOrderRecord(record) {
  return withLock(() => createOrderRecordUnlocked(record));
}
function mergeBitrefill(prev, next) {
  if (!next) return prev ?? null;
  if (!prev?.expiresAt || !next.expiresAt) return { ...next, expiresAt: next.expiresAt ?? prev?.expiresAt ?? null };
  const a = Date.parse(prev.expiresAt);
  const b = Date.parse(next.expiresAt);
  return { ...next, expiresAt: Number.isFinite(a) && (!Number.isFinite(b) || a < b) ? prev.expiresAt : next.expiresAt };
}
function createOrderRecordUnlocked(record) {
  const { rozoPaymentId } = record;
  const existing = readState(rozoPaymentId);
  const next = {
    version: 1,
    rozoPaymentId,
    // 'coinbase' (default, historical records) or 'bitrefill'. Drives which
    // payability checks presend and status run.
    provider: record.provider ?? existing?.provider ?? "coinbase",
    bitrefill: mergeBitrefill(existing?.bitrefill, record.bitrefill),
    linkId: record.linkId,
    paymentLink: record.paymentLink ?? null,
    merchant: record.merchant ?? null,
    invoiceAmount: record.invoiceAmount ?? null,
    source: record.source,
    receiverAddress: record.receiverAddress,
    receiverMemo: record.receiverMemo ?? null,
    amount: record.amount,
    amountUnit: record.amountUnit ?? null,
    expiresAt: record.expiresAt ?? null,
    // Native coin orders only: the price lock the backend reported at create.
    quoteExpiresAt: record.quoteExpiresAt ?? existing?.quoteExpiresAt ?? null,
    createdAt: existing?.createdAt ?? (/* @__PURE__ */ new Date()).toISOString(),
    updatedAt: (/* @__PURE__ */ new Date()).toISOString(),
    confirmation: existing?.confirmation ?? null,
    send: existing?.send ?? null
  };
  writeAtomic(statePath(rozoPaymentId), next);
  return next;
}
function depositDigest(source) {
  const canonical = JSON.stringify({
    chainId: String(source?.chainId ?? ""),
    tokenSymbol: String(source?.tokenSymbol ?? "").toUpperCase(),
    tokenAddress: String(source?.tokenAddress ?? ""),
    receiverAddress: String(source?.receiverAddress ?? ""),
    receiverMemo: source?.receiverMemo ?? null,
    amount: String(source?.amount ?? ""),
    amountUnit: source?.amountUnit ?? null,
    lnInvoice: source?.lnInvoice ?? null
  });
  return crypto.createHash("sha256").update(canonical, "utf8").digest("hex");
}
function recordConfirmation(rozoPaymentId, { source, invoiceAmount, tier, quoteExpiresAt = null }) {
  return withLock(() => {
    const state = readState(rozoPaymentId);
    if (!state) {
      throw new SkillError("NO_ORDER_STATE", "Cannot confirm an order with no local record.");
    }
    const next = {
      ...state,
      updatedAt: (/* @__PURE__ */ new Date()).toISOString(),
      confirmation: {
        confirmedAt: (/* @__PURE__ */ new Date()).toISOString(),
        depositDigest: depositDigest(source),
        invoiceAmount: invoiceAmount ?? state.invoiceAmount ?? null,
        tier: tier ?? null,
        // The native price lock the human was shown. A send never goes out
        // after it, even if the backend later reports a later one.
        quoteExpiresAt: quoteExpiresAt ?? null
      }
    };
    writeAtomic(statePath(rozoPaymentId), next);
    return next;
  });
}

// scripts/src/lib/prefs.mjs
function prefsPath() {
  const root = process.env.ROZO_CHECKOUT_STATE_DIR ? path2.dirname(stateRoot()) : path2.join(os2.homedir(), ".rozo-checkout");
  return path2.join(root, "prefs.json");
}
var ALLOWED = ["lastPayerAddress", "lastAddressFamily", "lastPreset", "installId", "updatedAt"];
var INSTALL_ID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
var LOCK_WAIT_MS2 = 2e3;
var LOCK_STALE_MS2 = 1e4;
function sleepSync2(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}
function withPrefsLock(fn) {
  const lock = `${prefsPath()}.lock`;
  fs2.mkdirSync(path2.dirname(lock), { recursive: true, mode: 448 });
  const deadline = Date.now() + LOCK_WAIT_MS2;
  for (; ; ) {
    try {
      fs2.closeSync(fs2.openSync(lock, "wx", 384));
      break;
    } catch (err) {
      if (err.code !== "EEXIST") throw err;
    }
    try {
      if (Date.now() - fs2.statSync(lock).mtimeMs > LOCK_STALE_MS2) {
        fs2.rmSync(lock, { force: true });
        continue;
      }
    } catch {
      continue;
    }
    if (Date.now() > deadline) return void 0;
    sleepSync2(10);
  }
  try {
    return fn();
  } finally {
    fs2.rmSync(lock, { force: true });
  }
}
var USER_FIELDS = ["lastPayerAddress", "lastAddressFamily", "lastPreset"];
function readPrefs() {
  let raw;
  try {
    raw = fs2.readFileSync(prefsPath(), "utf8");
  } catch {
    return null;
  }
  let doc;
  try {
    doc = JSON.parse(raw);
  } catch {
    return null;
  }
  if (!doc || typeof doc !== "object" || Array.isArray(doc)) return null;
  const out = {};
  for (const k of ALLOWED) {
    const v = doc[k];
    if (typeof v === "string" && v.trim()) out[k] = v.trim();
  }
  return Object.keys(out).length ? out : null;
}
function savePrefs(update, { installIdIfAbsent } = {}) {
  try {
    const saved = withPrefsLock(() => {
      const existing = readPrefs() || {};
      const next = { ...existing };
      for (const k of USER_FIELDS) {
        const v = update?.[k];
        if (typeof v === "string" && v.trim()) next[k] = v.trim();
      }
      if (!INSTALL_ID_RE.test(String(existing.installId ?? "")) && INSTALL_ID_RE.test(String(installIdIfAbsent ?? ""))) {
        next.installId = installIdIfAbsent;
      }
      next.updatedAt = (/* @__PURE__ */ new Date()).toISOString();
      writeAtomic(prefsPath(), next);
      return next;
    });
    return saved ?? null;
  } catch {
    return null;
  }
}

// scripts/src/lib/identity.mjs
var ACCOUNT_HASH_PREFIX = "rozo-acct-v1:";
function isValidInstallId(value) {
  return typeof value === "string" && INSTALL_ID_RE.test(value);
}
function attributionDisabled(env = process.env) {
  const v = String(env.ROZO_CHECKOUT_ANON_ID ?? "").trim().toLowerCase();
  return ["off", "0", "false", "no"].includes(v);
}
function getOrCreateInstallId() {
  const existing = readPrefs()?.installId;
  if (isValidInstallId(existing)) return existing;
  const saved = savePrefs({}, { installIdIfAbsent: crypto2.randomUUID().toLowerCase() });
  if (isValidInstallId(saved?.installId)) return saved.installId;
  const onDisk = readPrefs()?.installId;
  return isValidInstallId(onDisk) ? onDisk : crypto2.randomUUID().toLowerCase();
}
function hashAccount(raw) {
  return crypto2.createHash("sha256").update(`${ACCOUNT_HASH_PREFIX}${raw}`, "utf8").digest("hex");
}
function rawApiKey(env) {
  const v = typeof env.OPENROUTER_API_KEY === "string" ? env.OPENROUTER_API_KEY.trim() : "";
  return v && v.length <= 1024 ? v : null;
}
function attributionIdentity(env = process.env) {
  if (attributionDisabled(env)) return {};
  const out = {};
  try {
    const id = getOrCreateInstallId();
    if (isValidInstallId(id)) out.install_id = id;
  } catch {
  }
  const raw = rawApiKey(env);
  if (raw) out.account_hash = hashAccount(raw);
  return out;
}

// scripts/src/lib/api.mjs
var MPP_BASE = process.env.ROZO_CHECKOUT_MPP_BASE || "https://apiserver.mpprouter.dev/v1/services/rozo-agent-api";
var CLIENT_LABEL = `rozo-checkout-cli/${PKG_VERSION}`;
var ATTRIBUTION_CLIENT = `rozo-checkout-skill/${PKG_VERSION}`;
function buildAttribution({ utmSource, identity } = {}) {
  const raw = utmSource !== void 0 ? utmSource : process.env.ROZO_CHECKOUT_UTM_SOURCE;
  const utm_source = normalizeUtmSource(raw);
  const ids = identity ?? attributionIdentity();
  return {
    client: ATTRIBUTION_CLIENT,
    ...utm_source ? { utm_source } : {},
    ...ids.install_id ? { install_id: ids.install_id } : {},
    ...ids.account_hash ? { account_hash: ids.account_hash } : {}
  };
}
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
var QUOTE_RECEIPT_RETRY_BUDGET_MS = 2e4;
async function createInvoice({ url, linkId, source, quoteReceipt, utmSource, email, beta }) {
  const body = {
    ...url ? { url } : { payment_id: linkId },
    source: {
      chainId: String(source.chainId),
      tokenSymbol: source.tokenSymbol,
      // Shielded ZEC: the router passes this to intents, which hands out a
      // pool Unified Address instead of a transparent one. Never sent otherwise.
      ...source.shielded === true ? { shielded: true } : {}
    },
    ...quoteReceipt ? { quoteReceipt } : {},
    client: CLIENT_LABEL,
    attribution: buildAttribution({ utmSource }),
    // Optional payer contact email (validated by the caller). Omitted, never
    // sent empty, when the user gave none.
    ...email ? { email } : {}
  };
  return postJson(
    withBeta(`${MPP_BASE}/create-invoice`, beta),
    body,
    quoteReceipt ? { maxTotalWaitMs: QUOTE_RECEIPT_RETRY_BUDGET_MS } : void 0
  );
}
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

// scripts/src/lib/gas.mjs
var EVM_FEE_COIN = Object.freeze({
  1: { symbol: "ETH", network: "Ethereum" },
  56: { symbol: "BNB", network: "BNB Chain" },
  137: { symbol: "POL", network: "Polygon" },
  8453: { symbol: "ETH", network: "Base" },
  42161: { symbol: "ETH", network: "Arbitrum" }
});

// scripts/src/lib/rpc.mjs
var DEFAULT_RPC = Object.freeze({
  // eth.llamarpc.com and polygon-rpc.com stopped answering (checked
  // 2026-10-12: HTTP 525, and "API key disabled"); publicnode serves both.
  1: "https://ethereum-rpc.publicnode.com",
  56: "https://bsc-dataseed.binance.org",
  137: "https://polygon-bor-rpc.publicnode.com",
  8453: "https://mainnet.base.org",
  42161: "https://arb1.arbitrum.io/rpc",
  900: "https://api.mainnet-beta.solana.com"
});

// scripts/src/lib/native.mjs
function nativeDepositWarnings({ tokenSymbol, chainId }) {
  const coin = String(tokenSymbol || "").toUpperCase();
  return [
    `This is an exact-out ${coin} order: send exactly the amount shown, in one transfer. The coin price is locked only until the time shown; after that, do not send, start a new order.`,
    `The ${coin} amount includes an FX spread on top of the service fee.`,
    `Your wallet also needs some ${coin} on ${chainName(chainId)} for the network fee, on top of the amount shown.`,
    "Paying from an exchange: make sure the amount that ARRIVES is exactly the amount shown. Exchanges often subtract their withdrawal fee, and a short payment may need manual review."
  ];
}

// scripts/src/lib/zec.mjs
var ZEC_CHAIN_ID = "9133";
var ZEC_SYMBOL = "ZEC";
var ZEC_SOURCE_META_KEY = "ZEC@9133";
var ZEC_BETA_PARAM = "zec,zec_shielded";
var ZEC_SHIELDED_MAX_USD = 1200;
var ZEC_MIN_USD = 5;
var ZEC_TWO_CONF_FROM_USD = 110;
var ZEC_PAYIN_STATES = /* @__PURE__ */ new Set(["awaiting", "seen", "confirming", "eligible", "expired", "reorged"]);
var UA_RE = /^u1[02-9ac-hj-np-z]{100,400}$/;
function isZecSource(chainId, tokenSymbol) {
  return String(chainId ?? "").trim() === ZEC_CHAIN_ID && String(tokenSymbol ?? "").trim().toUpperCase() === ZEC_SYMBOL;
}
function isUnifiedAddress(value) {
  return typeof value === "string" && UA_RE.test(value.trim());
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
function zecDepositWarnings({ requiredConfirmations }) {
  return [
    "Pay from a shielded balance, in ONE transaction, exactly the amount shown. The price is locked only until the time shown; after that, do not send, start a new order.",
    "Underpayments are not refunded automatically: a short payment is held for support, not credited.",
    `Scan the payment URI (QR content) with a shielded wallet such as Zashi; it carries the address, the amount and the order memo. Do not edit any of them.`,
    `The merchant is paid after ${requiredConfirmations ?? 1} confirmation${requiredConfirmations === 2 ? "s" : ""} (about 75 seconds each).`,
    `Beta: up to $${ZEC_SHIELDED_MAX_USD} per payment.`
  ];
}

// scripts/src/lib/guards.mjs
var UNPAID_STATUS = "payment_unpaid";
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
function verifyCreateAgainstQuote({ snapshot, created, requested }) {
  const drift = [];
  const require2 = (field, a, b, normalize = defaultNormalize) => {
    const na = normalize(a);
    const nb = normalize(b);
    if (na === null) {
      drift.push({ field, quoted: null, created: nb, note: "missing in quote" });
      return;
    }
    if (nb === null) {
      drift.push({ field, quoted: na, created: null, note: "missing in create response" });
      return;
    }
    if (na !== nb) drift.push({ field, quoted: na, created: nb });
  };
  require2("linkId", snapshot?.linkId, created?.linkId);
  require2("merchant", snapshot?.merchant, created?.merchant, normalizeMerchant);
  require2("original", snapshot?.original, created?.original, normalizeDecimal);
  require2("callerPays", snapshot?.callerPays, created?.callerPays, normalizeDecimal);
  const wantChain = String(requested?.chainId ?? "").trim();
  const wantToken = String(requested?.tokenSymbol ?? "").trim().toUpperCase();
  const gotChain = String(created?.source?.chainId ?? "").trim();
  const gotToken = String(created?.source?.tokenSymbol ?? "").trim().toUpperCase();
  if (!gotChain || gotChain !== wantChain) {
    drift.push({ field: "source.chainId", quoted: wantChain, created: gotChain || null });
  }
  if (!gotToken || gotToken !== wantToken) {
    drift.push({ field: "source.tokenSymbol", quoted: wantToken, created: gotToken || null });
  }
  if (drift.length) {
    return {
      ok: false,
      code: "CREATE_DRIFT",
      reason: "The created order does not match what was quoted. Refusing to continue.",
      drift
    };
  }
  const quoted = checkQuotePricing(snapshot);
  if (!quoted.ok) return { ...quoted, drift: [{ field: quoted.field, quoted: quoted.value, created: null, note: "quote" }] };
  const got = checkPricing(created);
  if (!got.ok) return { ...got, drift: [{ field: got.field, quoted: null, created: got.value }] };
  const feeDrift = [];
  if (quoted.pricing.serviceFee !== got.pricing.serviceFee) {
    feeDrift.push({ field: "serviceFee", quoted: quoted.pricing.serviceFee, created: got.pricing.serviceFee });
  }
  if (quoted.pricing.feeBps !== got.pricing.feeBps) {
    feeDrift.push({ field: "feeBps", quoted: quoted.pricing.feeBps, created: got.pricing.feeBps });
  }
  if (feeDrift.length) {
    return {
      ok: false,
      code: "CREATE_DRIFT",
      reason: "The created order does not match what was quoted. Refusing to continue.",
      drift: feeDrift
    };
  }
  return { ok: true, code: null, reason: null, drift: [] };
}
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
function normalizeMerchant(v) {
  if (v === null || v === void 0) return null;
  if (typeof v === "object") {
    const name = v.name ?? v.merchantName ?? null;
    return name ? String(name).trim() || null : null;
  }
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

// scripts/src/lib/blacklist.mjs
import fs3 from "node:fs";
import path3 from "node:path";
import crypto3 from "node:crypto";
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
  const digest = crypto3.createHash("sha256").update(JSON.stringify(addresses), "utf8").digest("hex");
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
  const here = path3.dirname(fileURLToPath(moduleUrl));
  return [
    path3.join(here, "blacklist.json"),
    path3.join(here, "..", "src", "lib", "blacklist.json"),
    path3.join(here, "..", "..", "src", "lib", "blacklist.json")
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
      raw = fs3.readFileSync(p, "utf8");
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

// scripts/src/create-order.mjs
function confirmTier(usdAmount) {
  const usd = Number(usdAmount);
  if (!Number.isFinite(usd)) return "explicit";
  if (usd <= 1) return "silent";
  if (usd <= 10) return "one-line";
  return "explicit";
}
async function main(argv) {
  const args = parseArgs(argv);
  const url = args.url || args._[0];
  if (!url || url === true) usage('Required: --url "<coinbase payment link url or id>"');
  const chainId = String(args.chain ?? "").trim();
  const tokenSymbol = String(args.token ?? "").trim().toUpperCase();
  if (!chainId || !tokenSymbol) {
    usage("Required: --chain <chainId> --token <SYMBOL>. Run quote.js to see supported sources.");
  }
  if (!isSupportedSource(chainId, tokenSymbol)) {
    throw new SkillError(
      "UNSUPPORTED_SOURCE",
      `${tokenSymbol} on ${chainName(chainId)} is not a supported source.`,
      { supported: SUPPORTED_SOURCES }
    );
  }
  const zec = isZecSource(chainId, tokenSymbol);
  const shielded = Boolean(args.shielded);
  if (zec && !shielded) {
    throw new SkillError(
      "ZEC_SHIELDED_REQUIRED",
      "ZEC orders from this CLI pay from a shielded balance: add --shielded. For transparent ZEC use https://checkout.rozo.ai/zec."
    );
  }
  if (shielded && !zec) {
    throw new SkillError("CONFLICTING_FLAGS", "--shielded only applies to ZEC (--chain 9133 --token ZEC).");
  }
  const requested = zec ? { chainId, tokenSymbol, shielded: true } : { chainId, tokenSymbol };
  const beta = zec ? ZEC_BETA_PARAM : void 0;
  const confirmed = Boolean(args.confirm);
  const email = contactEmailFromArgs(args);
  let blacklist;
  try {
    blacklist = loadBlacklist();
  } catch (err) {
    throw new SkillError(
      "BLACKLIST_UNAVAILABLE",
      `Compromised-address list unusable: ${err.message} Refusing to proceed.`
    );
  }
  const { linkId: parsedLinkId } = extractLinkId(String(url));
  const quote = await quoteInvoice({ url: String(url), beta });
  const snapshot = snapshotFromQuote(quote);
  const quoteReceipt = quote?.quoteReceipt ?? null;
  const quotedPricing = checkQuotePricing(snapshot);
  if (!quotedPricing.ok) {
    emit(
      {
        success: false,
        step: "quote-pricing",
        error: { code: quotedPricing.code, message: quotedPricing.reason },
        linkId: snapshot.linkId ?? parsedLinkId,
        guidance: "Nothing was created. The quoted amounts do not add up; do not pay this link through the CLI."
      },
      EXIT_ERROR
    );
  }
  const native = isNativeSource(chainId, tokenSymbol);
  if (native) {
    const offer = nativeOfferFor({
      chainId,
      tokenSymbol,
      supportedSources: quote?.supportedSources,
      nativeMinUsd: quote?.nativeMinUsd,
      callerPaysUsd: snapshot.callerPays ?? snapshot.original
    });
    if (!offer.ok) {
      emit(
        {
          success: false,
          step: "native-offer",
          error: { code: offer.code, message: offer.reason },
          linkId: snapshot.linkId ?? parsedLinkId,
          guidance: "Nothing was created. Choose USDC or USDT, or another coin the quote lists."
        },
        EXIT_ERROR
      );
    }
  }
  let zecOffer = null;
  if (zec) {
    zecOffer = zecShieldedOfferFor({
      supportedSources: quote?.supportedSources,
      sourceMeta: quote?.sourceMeta,
      callerPaysUsd: snapshot.callerPays ?? snapshot.original
    });
    if (!zecOffer.ok) {
      emit(
        {
          success: false,
          step: "zec-offer",
          error: { code: zecOffer.code, message: zecOffer.reason },
          linkId: snapshot.linkId ?? parsedLinkId,
          guidance: "Nothing was created. Choose USDC or USDT, or another coin the quote lists."
        },
        EXIT_ERROR
      );
    }
  }
  const created = await createInvoice({
    url: String(url),
    source: requested,
    quoteReceipt,
    beta,
    utmSource: typeof args["utm-source"] === "string" ? args["utm-source"] : void 0,
    email
  });
  if (!created?.rozoPaymentId) {
    throw new SkillError("CREATE_FAILED", "create-invoice returned no rozoPaymentId.", {
      response: created
    });
  }
  const rozoPaymentId = assertRozoPaymentId(created.rozoPaymentId);
  if (zec && (created.sourceMismatch === true || created.sourceMismatchCode === "ZEC_RECEIVE_MODE_MISMATCH")) {
    const remainingMs = created.expiresAt ? Date.parse(created.expiresAt) - Date.now() : NaN;
    emit(
      {
        success: false,
        step: "reuse-source-mismatch",
        error: {
          code: "ZEC_RECEIVE_MODE_MISMATCH",
          message: "This link already has an unpaid ZEC order of the other kind (transparent or shielded). Only one order exists per link at a time, so nothing new was created."
        },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        paymentLink: created.paymentLink ?? null,
        existingOrder: {
          rozoPaymentId,
          chainId: created.source?.chainId ?? null,
          tokenSymbol: created.source?.tokenSymbol ?? null,
          receive: created.source?.zec?.receive ?? null,
          expiresAt: created.expiresAt ?? null,
          expiresIn: Number.isFinite(remainingMs) ? formatRemaining(remainingMs) : null
        },
        nextAction: { type: "choose_method", canRetryQuery: true, canCreateOrder: false, canSend: false, switchPossibleAfter: created.expiresAt ?? null },
        guidance: "Pay the existing order on https://checkout.rozo.ai/zec with the mode it was made for, or wait for its price lock to expire unfunded (about 30 minutes) and run pay again: an expired, unfunded ZEC order is replaced."
      },
      EXIT_ERROR
    );
  }
  const verify = verifyCreateAgainstQuote({ snapshot, created, requested });
  if (!verify.ok) {
    const onlySourceDrift = verify.drift.length > 0 && verify.drift.every((d) => d.field.startsWith("source."));
    if (created.reused && onlySourceDrift) {
      const existing = created.source || {};
      const remainingMs = created.expiresAt ? Date.parse(created.expiresAt) - Date.now() : NaN;
      emit(
        {
          success: false,
          step: "reuse-source-mismatch",
          error: {
            code: "REUSED_SOURCE_MISMATCH",
            message: `This link already has an unpaid order, created for ${existing.tokenSymbol ?? "?"} on chain ${existing.chainId ?? "?"}. You asked for ${tokenSymbol} on chain ${chainId}. Only one order exists per link at a time, so nothing new was created.`
          },
          linkId: created.linkId ?? parsedLinkId,
          rozoPaymentId,
          paymentLink: created.paymentLink ?? null,
          existingOrder: {
            rozoPaymentId,
            chainId: existing.chainId ?? null,
            tokenSymbol: existing.tokenSymbol ?? null,
            expiresAt: created.expiresAt ?? null,
            expiresIn: Number.isFinite(remainingMs) ? formatRemaining(remainingMs) : null
          },
          // Machine-readable form of the guidance below. The live order keeps
          // its own coin; a different coin is only possible once it has
          // expired unfunded (then pay on the same link creates a new order).
          nextAction: {
            type: "choose_method",
            canRetryQuery: true,
            canCreateOrder: false,
            canSend: false,
            payExistingWith: { chainId: existing.chainId ?? null, tokenSymbol: existing.tokenSymbol ?? null },
            switchPossibleAfter: created.expiresAt ?? null
          },
          guidance: `Either pay the existing order with ${existing.tokenSymbol ?? "its own coin"} (re-run with --chain ${existing.chainId} --token ${existing.tokenSymbol}), or wait ${Number.isFinite(remainingMs) ? formatRemaining(remainingMs) : "for it to expire"} for it to expire and then create a new one. Unpaid orders cost nothing.`
        },
        EXIT_ERROR
      );
    }
    emit(
      {
        success: false,
        step: "verify-create",
        error: { code: verify.code, message: verify.reason, details: { drift: verify.drift } },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        paymentLink: created.paymentLink ?? null,
        guidance: "The order exists but was NOT validated. Do not fund it. Let it expire unfunded."
      },
      EXIT_ERROR
    );
  }
  const createdPricing = checkPricing(created).pricing;
  const payment = await getPayment(rozoPaymentId);
  const source = payment?.source || {};
  const guard = reuseGuard({ payment, requested, reused: created.reused });
  if (!guard.ok) {
    emit(
      {
        success: false,
        step: "reuse-guard",
        error: { code: guard.code, message: guard.reason, details: guard.evidence },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        paymentLink: created.paymentLink ?? null,
        moneyDetected: guard.moneyDetected,
        guidance: guard.moneyDetected ? "MONEY DETECTED. Do not pay again, do not retry into a new order. Preserve every id and tx hash above and escalate to the operator for manual reconciliation." : "Abort this run. Nothing was funded."
      },
      EXIT_ERROR
    );
  }
  const lightning = String(source.chainId) === "lightning";
  const bolt11 = source.lnInvoice ?? payment?.lnInvoice ?? null;
  let prior = null;
  try {
    prior = native ? readState(rozoPaymentId) : null;
  } catch {
    prior = null;
  }
  const zecStatus = zec ? zecStatusOf(source) : null;
  const quoteExpiresAt = zec ? zecStatus?.quoteExpiresAt ?? null : priceLockFor({
    native,
    payment,
    others: [created?.quoteExpiresAt, prior?.quoteExpiresAt, prior?.confirmation?.quoteExpiresAt]
  });
  const expiry = checkExpiry({
    now: Date.now(),
    chainId: source.chainId ?? chainId,
    intentExpiresAt: payment?.expiresAt,
    coinbaseExpiry: snapshot?.coinbase?.preApprovalExpiry,
    // For Lightning the BOLT11's own validity is an extra gate. We only have a
    // separate expiry if the backend exposes one; otherwise the intent expiry
    // governs and we still require the 10-minute floor via the margin.
    ...lightning ? { bolt11ExpiresAt: payment?.expiresAt } : {},
    ...native || zec ? { quoteExpiresAt } : {}
  });
  if (!expiry.ok) {
    emit(
      {
        success: false,
        step: "expiry-guard",
        error: { code: expiry.code, message: expiry.reason, details: expiry },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        guidance: String(expiry.code).startsWith("QUOTE_") ? "The coin price lock for this order has run out, or is about to. Do not fund it. An unfunded order costs nothing; once it has expired, run pay again for a fresh price." : "Not enough time remains to fund, bridge and settle safely. Ask the merchant for a fresh link and start over. Do not fund this order."
      },
      EXIT_ERROR
    );
  }
  try {
    assertNotBlacklisted(
      [
        {
          address: source.receiverAddress,
          family: chainFamily(source.chainId),
          role: "deposit address"
        }
      ],
      blacklist
    );
  } catch (err) {
    emit(
      {
        success: false,
        step: "blacklist",
        error: { code: err.code, message: err.message },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        guidance: "Do NOT send anything. Report this to the operator immediately."
      },
      EXIT_ERROR
    );
  }
  const statusNow = await invoiceStatus({ linkId: created.linkId ?? parsedLinkId });
  const payable = checkPayable(statusNow, Date.now());
  if (!payable.ok) {
    emit(
      {
        success: false,
        step: "payability-revalidation",
        error: { code: payable.code, message: payable.reason, details: payable.derived },
        linkId: created.linkId ?? parsedLinkId,
        rozoPaymentId,
        guidance: "The Coinbase resource stopped being payable between quote and now (someone else may have paid it). Do NOT fund this order."
      },
      EXIT_ERROR
    );
  }
  createOrderRecord({
    rozoPaymentId,
    linkId: created.linkId ?? parsedLinkId,
    paymentLink: created.paymentLink ?? null,
    merchant: created.merchant ?? snapshot.merchant,
    invoiceAmount: created.original ?? snapshot.original,
    source: { chainId: source.chainId, tokenSymbol: source.tokenSymbol, ...zec ? { receive: "shielded" } : {} },
    receiverAddress: source.receiverAddress,
    receiverMemo: source.receiverMemo ?? null,
    amount: source.amount,
    amountUnit: source.amountUnit ?? null,
    expiresAt: payment?.expiresAt ?? null,
    ...native || zec ? { quoteExpiresAt } : {}
  });
  const usd = created.original ?? snapshot.original;
  const family = chainFamily(source.chainId);
  const tier = confirmTier(usd);
  const depositInfo = guard.deposit;
  if (confirmed) {
    recordConfirmation(rozoPaymentId, {
      source,
      invoiceAmount: usd,
      tier,
      ...native || zec ? { quoteExpiresAt } : {}
    });
  }
  const memoRequirement = lightning ? "Lightning invoices carry their own routing data; there is no separate memo." : zec ? "The order memo is inside the payment URI; scanning it fills the memo for you. Do not type one." : source.receiverMemo ? "This deposit REQUIRES the memo/tag below. Sending without it will very likely lose the funds." : family === "stellar" ? "A Stellar deposit always requires a memo." : "This deposit does not use a memo. Leave the memo field empty.";
  emit({
    success: true,
    step: "create-order",
    confirmed,
    // True only when an email went out with a NEW order. A reused order keeps
    // whatever email it was first created with (the router never rebinds), so
    // reporting true there would be a false promise. The address itself is
    // never echoed. Note the --confirm run always sees the order as reused;
    // the CLI carries the first run's value forward.
    contactEmailProvided: contactEmailAttached(email, created.reused),
    support: SUPPORT,
    reused: Boolean(created.reused),
    reusedNote: created.reused ? `An existing unpaid order for this link was reused (${rozoPaymentId}), valid for another ${formatRemaining(expiry.msRemaining)}. Nothing new was created.` : null,
    orderCost: "Creating an order moves no money. An order you never fund simply expires and costs nothing.",
    linkId: created.linkId ?? parsedLinkId,
    rozoPaymentId,
    paymentLink: created.paymentLink ?? null,
    merchant: normalizeMerchant(created.merchant ?? snapshot.merchant),
    invoice: { amount: usd, currency: snapshot?.fiat?.currency ?? "USD" },
    // Verified above: callerPays == invoice + serviceFee, fee explicit and capped.
    callerPays: createdPricing.callerPays,
    serviceFee: createdPricing.serviceFee,
    feeBps: createdPricing.feeBps,
    discount: created.discount ?? "0",
    // Machine-readable, copy-pastable — and WITHHELD until --confirm. This is
    // the only place the full address, memo and BOLT11 ever appear.
    deposit: confirmed ? {
      chainId: source.chainId,
      chain: chainName(source.chainId),
      tokenSymbol: source.tokenSymbol,
      tokenAddress: source.tokenAddress || null,
      // Lightning has no deposit address: the BOLT11 IS the instruction.
      receiverAddress: lightning ? null : source.receiverAddress,
      receiverMemo: source.receiverMemo ?? null,
      // Stellar memos are TEXT even when they look numeric. Sending one as
      // MEMO_ID produces a different memo and the payment will not match.
      receiverMemoType: source.receiverMemo ? STELLAR_MEMO_TYPE : null,
      amount: source.amount,
      amountUnit: source.amountUnit ?? null,
      isSats: isSatsUnit(source.amountUnit),
      lnInvoice: bolt11 || null,
      payTo: depositInfo.payTo,
      expiresAt: payment?.expiresAt ?? null,
      expiresIn: formatRemaining(expiry.msRemaining),
      // Native coins are exact-out like Lightning: this exact coin amount,
      // at a price locked only until quoteExpiresAt.
      native,
      exactOut: native || lightning || zec,
      quoteExpiresAt: native || zec ? quoteExpiresAt : null,
      // Shielded ZEC: what the payer scans. The QR content is the URI,
      // shown verbatim; it carries the address, the amount and the memo.
      ...zec ? {
        shielded: true,
        paymentUri: depositInfo.paymentUri,
        requiredConfirmations: zecStatus?.requiredConfirmations ?? zecOffer?.requiredConfirmations ?? null,
        payinState: zecStatus?.payinState ?? null
      } : {}
    } : null,
    depositWithheld: !confirmed,
    // Safe for prose / chat.
    display: {
      chain: chainName(source.chainId),
      token: source.tokenSymbol,
      amount: formatAmount(source),
      isSats: isSatsUnit(source.amountUnit),
      payToMasked: maskAddress(depositInfo.payTo),
      receiverMemoMasked: maskMemo(source.receiverMemo),
      hasMemo: Boolean(source.receiverMemo),
      memoType: source.receiverMemo ? STELLAR_MEMO_TYPE : null,
      memoRequirement,
      native,
      priceLockedUntil: native || zec ? quoteExpiresAt : null,
      // The bare decimal amount (not secret), for balance comparisons.
      coinAmount: isSatsUnit(source.amountUnit) ? null : String(source.amount ?? ""),
      ...zec ? { shielded: true, requiredConfirmations: zecStatus?.requiredConfirmations ?? zecOffer?.requiredConfirmations ?? null } : {}
    },
    expiry: {
      intentExpiresAt: payment?.expiresAt ?? null,
      coinbaseExpiry: snapshot?.coinbase?.preApprovalExpiry ?? null,
      quoteExpiresAt: native || zec ? quoteExpiresAt : null,
      effectiveDeadlineIso: new Date(expiry.effectiveDeadlineMs).toISOString(),
      // A duration, not just a timestamp: this is what a payer actually needs.
      expiresIn: formatRemaining(expiry.msRemaining),
      msRemaining: expiry.msRemaining,
      marginMinutes: Math.round(expiry.marginMs / 6e4),
      minutesOfSlack: Math.floor(expiry.msOfSlack / 6e4)
    },
    confirmation: {
      required: tier,
      satisfied: confirmed,
      note: confirmed ? "Confirmation recorded. The send scripts will verify it against the live deposit data." : "BINDING CONFIRMATION POINT. Present chain, token, exact amount, the masked address, the memo requirement, both expiries and the reused flag, and get an explicit yes. Then re-run this command with --confirm to release the full deposit details.",
      warnings: [
        "Wrong token, wrong network, or wrong amount is usually unrecoverable.",
        memoRequirement,
        "Send exactly once. A second send to the same one-time address is not guaranteed to be credited.",
        "The deposit amount can exceed the invoice: it includes the bridge and network fees.",
        ...native ? nativeDepositWarnings({ tokenSymbol: source.tokenSymbol, chainId: source.chainId }) : [],
        ...zec ? zecDepositWarnings({ requiredConfirmations: zecStatus?.requiredConfirmations ?? zecOffer?.requiredConfirmations ?? null }) : []
      ]
    },
    blacklist: {
      checked: true,
      addressesInList: blacklist.entries.length,
      digest: blacklist.provenance.addressesSha256
    },
    nextStep: confirmed ? {
      modeA: "Give the user the `deposit` block, then poll: status.js --rozo-payment-id <id>",
      modeB: family === "evm" ? `send-evm.js --rozo-payment-id ${rozoPaymentId} --send  (requires ROZO_CHECKOUT_EVM_KEY)` : family === "solana" ? `send-sol.js --rozo-payment-id ${rozoPaymentId} --send  (requires ROZO_CHECKOUT_SOL_KEY)` : zec ? "not available: scan deposit.paymentUri with a shielded Zcash wallet (Mode A)" : "not available for this chain \u2014 pay from a wallet (Mode A)"
    } : {
      confirm: "Re-run this exact command with --confirm once the user has said yes."
    }
  });
}
async function run(argv = process.argv.slice(2)) {
  return main(argv);
}

// scripts/src/bin/create-order.mjs
run().catch((err) => fail(err));
