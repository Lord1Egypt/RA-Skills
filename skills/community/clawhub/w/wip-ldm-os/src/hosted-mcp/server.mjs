// server.mjs: Hosted MCP server for wip.computer
// MCP Streamable HTTP transport at /mcp, health check at /health.
// Auth: Bearer ck-... API key maps to an immutable tenant ID.
// OAuth 2.0: Minimal flow for Claude iOS custom connector.
// WebAuthn: Passkey-based signup/login (replaces agent name text form).

import { randomUUID, randomBytes, createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync, accessSync, constants as fsConstants } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createServer } from "node:http";
import { PrismaClient } from "@prisma/client";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import { registerTools } from "./tools.mjs";
import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse,
} from "@simplewebauthn/server";
import QRCode from "qrcode";
import { WebSocketServer } from "ws";
import { parse as parseUrlQs } from "node:querystring";
import {
  buildCodexBootstrapPayload,
  codexDaemonPubkeyFingerprint,
  createCodexDaemonPubkeyRegistry,
  evaluateCodexDaemonReconnectPubkey,
} from "./codex-relay-e2ee-registry.mjs";
import {
  codexWsFrameByteLength,
  createCodexWsAbuseLimitConfig,
  createCodexWsConnectionGuard,
  formatCodexWsLimitLog,
  isCodexWsAgentDisabled,
} from "./codex-relay-ws-abuse-limits.mjs";

// ── Settings ─────────────────────────────────────────────────────────

const PORT = parseInt(process.env.MCP_PORT || "18800", 10);
// Dev mode: opt-in to JSON-file fallbacks for the data layer and to
// reading tokens/passkeys from local JSON files. Production must run
// without this flag set (production fails closed when Prisma is
// unavailable, and never reads/writes the local JSON token files).
// Tracked by ai/product/bugs/security/2026-04-28--cc-mini--vps-hosted-mcp-audit.md (F-002, F-005a).
const DEV_MODE = process.env.LDM_HOSTED_MCP_DEV_MODE === "1";
// WebSocket Origin allowlist (F-003 in the VPS hosted-mcp audit).
// Browser-borne web WS upgrades must present an Origin from this list.
// Comma-separated env var; default is the production origin.
// Daemon WS upgrades (CLI / agent connections) are NOT gated on Origin
// because they do not send a browser Origin header.
const WS_ORIGIN_ALLOWLIST = (process.env.LDM_HOSTED_MCP_WS_ORIGIN_ALLOWLIST || "https://wip.computer")
  .split(",")
  .map(s => s.trim())
  .filter(Boolean);
const CODEX_WS_ABUSE_LIMITS = createCodexWsAbuseLimitConfig(process.env);

function isWsOriginAllowed(origin) {
  if (!origin) return false;
  return WS_ORIGIN_ALLOWLIST.includes(origin);
}
// F-001: WS URL-token fallback (browser sends ?token=ck-... on upgrade).
// Default off in production. Set LDM_HOSTED_MCP_ALLOW_WS_URL_TOKEN=1 to
// allow the legacy back-compat path. Independent of any other dev flag
// so that this can be toggled without enabling other dev-mode behavior.
const ALLOW_WS_URL_TOKEN = process.env.LDM_HOSTED_MCP_ALLOW_WS_URL_TOKEN === "1";
const SESSION_TIMEOUT_MS = 30 * 60 * 1000;
const SESSION_CLEANUP_INTERVAL_MS = 5 * 60 * 1000;
const OAUTH_CODE_EXPIRY_MS = 10 * 60 * 1000;
const MAX_REQUEST_BODY_MS = 30_000;
const SERVER_VERSION = "0.2.0";
const SERVER_NAME = "wip-mcp";
const SERVER_BIND = "0.0.0.0";
const ISSUER_URL = "https://wip.computer";
const MCP_RESOURCE_URL = "https://wip.computer/mcp";

// WebAuthn relying party config
const RP_NAME = "Memory Crystal";
const RP_ID = "wip.computer";
const RP_ORIGIN = "https://wip.computer";

// ── Data layer ──────────────────────────────────────────────────────
//
// Production: Postgres via Prisma is the canonical store. If Prisma
// cannot connect, the server refuses to start (F-005a).
//
// Dev mode (LDM_HOSTED_MCP_DEV_MODE=1): JSON files are used as a
// fallback for tokens and passkeys when Prisma is unavailable, and
// are also seeded into the in-memory cache on boot. Production must
// not set this flag.

const __dirname = dirname(fileURLToPath(import.meta.url));
const TOKEN_FILE = join(__dirname, "tokens.json");
const PASSKEY_FILE = join(__dirname, "passkeys.json");
const WALLET_FILE_LEGACY = join(__dirname, "wallets.json");

let prisma = null;
let usePrisma = false;
try {
  prisma = new PrismaClient();
  await prisma.$connect();
  usePrisma = true;
  console.log("Database: Postgres via Prisma");
} catch (err) {
  if (!DEV_MODE) {
    console.error("FATAL: Prisma unavailable; refusing to start.");
    console.error("Cause: " + err.message);
    console.error("Set LDM_HOSTED_MCP_DEV_MODE=1 to allow the JSON fallback (dev only).");
    process.exit(1);
  }
  console.warn("Database: JSON files (DEV MODE; Prisma not available: " + err.message + ")");
}

// ── API Keys ────────────────────────────────────────────────────────
//
// Hardcoded production defaults removed (F-002). Production keys live
// in the Postgres ApiKey table and are loaded on boot. In DEV_MODE,
// the local tokens.json file is also seeded into the in-memory cache.

const API_KEYS = {};
const API_KEY_HANDLES = {};
const ACCOUNT_TENANT_PREFIX = "acct:";
const LEGACY_API_KEY_TENANT_PREFIX = "key:";
const OAUTH_API_KEY_TENANT_PREFIX = "oauth:";

function isInternalTenantId(id) {
  return typeof id === "string"
    && (id.startsWith(ACCOUNT_TENANT_PREFIX)
      || id.startsWith(LEGACY_API_KEY_TENANT_PREFIX)
      || id.startsWith(OAUTH_API_KEY_TENANT_PREFIX));
}

function accountTenantIdForUserId(userId) {
  return ACCOUNT_TENANT_PREFIX + userId;
}

function legacyTenantIdForApiKey(key) {
  return LEGACY_API_KEY_TENANT_PREFIX + createHash("sha256").update(key).digest("base64url").slice(0, 32);
}

function oauthTenantIdForApiKey(key) {
  return OAUTH_API_KEY_TENANT_PREFIX + createHash("sha256").update(key).digest("base64url").slice(0, 32);
}

function rememberApiKeyInMemory(key, tenantId, handle = null) {
  API_KEYS[key] = tenantId;
  if (handle) API_KEY_HANDLES[key] = handle;
  else delete API_KEY_HANDLES[key];
}

function rememberLoadedApiKey(key, storedAgentId) {
  const tenantId = isInternalTenantId(storedAgentId) ? storedAgentId : legacyTenantIdForApiKey(key);
  const handle = isInternalTenantId(storedAgentId) ? null : storedAgentId;
  rememberApiKeyInMemory(key, tenantId, handle);
}

function identityForApiKey(key) {
  const tenantId = API_KEYS[key];
  if (!tenantId) return null;
  return {
    agentId: tenantId,
    tenantId,
    handle: API_KEY_HANDLES[key] || tenantId,
    apiKey: key,
  };
}

function loadTokensFromFile() {
  let rows = {};
  try { rows = JSON.parse(readFileSync(TOKEN_FILE, "utf8")); } catch { return; }
  for (const [key, storedAgentId] of Object.entries(rows)) {
    rememberLoadedApiKey(key, storedAgentId);
  }
}

async function loadApiKeysFromDb() {
  if (!usePrisma) return;
  try {
    const rows = await prisma.apiKey.findMany();
    for (const row of rows) rememberLoadedApiKey(row.key, row.agentId);
  } catch (err) {
    if (!DEV_MODE) {
      console.error("FATAL: Prisma loadApiKeys failed; refusing to start.");
      console.error("Cause: " + err.message);
      process.exit(1);
    }
    console.error("Prisma loadApiKeys error (DEV_MODE):", err.message);
  }
}

if (DEV_MODE) {
  loadTokensFromFile();
}
await loadApiKeysFromDb();

async function saveApiKey(key, agentId, { handle = null } = {}) {
  // Persist before advertising in memory: a newly issued key must not
  // become valid in the in-memory cache if the canonical store did not
  // accept it. Otherwise the key would work for the lifetime of the
  // process and disappear on restart.
  if (usePrisma) {
    try {
      await prisma.apiKey.upsert({
        where: { key },
        update: { agentId },
        create: { key, agentId },
      });
    } catch (err) {
      console.error("Prisma saveApiKey error:", err.message);
      if (!DEV_MODE) throw new Error("saveApiKey persistence failed: " + err.message);
    }
  } else if (!DEV_MODE) {
    // Production should never reach here (boot exits if Prisma is
    // unavailable), but guard explicitly.
    throw new Error("saveApiKey called without Prisma in production");
  }
  rememberApiKeyInMemory(key, agentId, handle);
  if (DEV_MODE) {
    try { writeFileSync(TOKEN_FILE, JSON.stringify(API_KEYS, null, 2) + "\n"); } catch {}
  }
}

// ── Passkeys ────────────────────────────────────────────────────────

// In-memory array (populated from DB or JSON on boot)
let passkeys = [];

function loadPasskeysFromFile() {
  try { return JSON.parse(readFileSync(PASSKEY_FILE, "utf8")); } catch { return []; }
}

async function loadPasskeysFromDb() {
  if (!usePrisma) {
    return DEV_MODE ? loadPasskeysFromFile() : [];
  }
  try {
    const creds = await prisma.credential.findMany({ include: { user: true } });
    const handleUserIds = new Map();
    for (const c of creds) {
      const handle = c.user?.name || (c.userId ? "user-" + c.userId.slice(0, 8) : "unknown");
      if (!handleUserIds.has(handle)) handleUserIds.set(handle, new Set());
      handleUserIds.get(handle).add(c.userId);
    }
    const out = [];
    for (const c of creds) {
      const handle = c.user?.name || (c.userId ? "user-" + c.userId.slice(0, 8) : "unknown");
      const agentId = accountTenantIdForUserId(c.userId);
      let apiKey = null;
      for (const [key, tenantId] of Object.entries(API_KEYS)) {
        if (tenantId === agentId || (handleUserIds.get(handle)?.size === 1 && API_KEY_HANDLES[key] === handle)) {
          apiKey = key;
          break;
        }
      }
      if (apiKey) {
        API_KEY_HANDLES[apiKey] = handle;
        if (API_KEYS[apiKey] !== agentId) {
          try {
            await saveApiKey(apiKey, agentId, { handle });
            console.log("loadPasskeysFromDb: migrated API key tenant for handle '" + handle + "' to immutable account id");
          } catch (err) {
            console.error("loadPasskeysFromDb: failed to migrate API key tenant for handle '" + handle + "':", err.message);
            if (!DEV_MODE) throw err;
          }
        }
      } else if (handle !== "unknown") {
        console.warn("loadPasskeysFromDb: no ApiKey row for account tenant '" + agentId + "'; auth-verify will mint on next successful login");
      }
      out.push({
        credentialId: c.id,
        publicKey: Buffer.from(c.publicKey).toString("base64url"),
        counter: c.counter,
        userId: c.userId,
        agentId,
        handle,
        apiKey,
        createdAt: c.createdAt.toISOString(),
        transports: c.transports || [],
      });
    }
    return out;
  } catch (err) {
    console.error("Prisma loadPasskeys error:", err.message);
    return DEV_MODE ? loadPasskeysFromFile() : [];
  }
}

async function savePasskey(entry) {
  // Persist before pushing to in-memory: a passkey must not exist in
  // memory if it was never persisted, or it would authenticate for the
  // lifetime of the process and disappear on restart.
  if (usePrisma) {
    try {
      // Ensure user exists
      let user = await prisma.user.findUnique({ where: { id: entry.userId } });
      if (!user) {
        user = await prisma.user.create({
          data: { id: entry.userId, name: entry.handle || "user" },
        });
      }
      await prisma.credential.create({
        data: {
          id: entry.credentialId,
          userId: entry.userId,
          publicKey: Buffer.from(entry.publicKey, "base64url"),
          counter: entry.counter || 0,
          transports: entry.transports || [],
        },
      });
    } catch (err) {
      console.error("Prisma savePasskey error:", err.message);
      if (!DEV_MODE) throw new Error("savePasskey persistence failed: " + err.message);
    }
  } else if (!DEV_MODE) {
    throw new Error("savePasskey called without Prisma in production");
  }
  passkeys.push(entry);
  if (DEV_MODE) {
    try { writeFileSync(PASSKEY_FILE, JSON.stringify(passkeys, null, 2) + "\n"); } catch {}
  }
}

async function updatePasskeyCounter(credentialId, newCounter) {
  // Persist before updating in-memory. The counter is the WebAuthn
  // replay-protection state; advancing it in memory while the DB row
  // stays behind would let a replayed assertion validate after a
  // restart re-loaded the stale counter.
  if (usePrisma) {
    try {
      await prisma.credential.update({
        where: { id: credentialId },
        data: { counter: newCounter },
      });
    } catch (err) {
      console.error("Prisma updateCounter error:", err.message);
      if (!DEV_MODE) throw new Error("updatePasskeyCounter persistence failed: " + err.message);
    }
  } else if (!DEV_MODE) {
    throw new Error("updatePasskeyCounter called without Prisma in production");
  }
  const entry = passkeys.find(p => p.credentialId === credentialId);
  if (entry) entry.counter = newCounter;
  if (DEV_MODE) {
    try { writeFileSync(PASSKEY_FILE, JSON.stringify(passkeys, null, 2) + "\n"); } catch {}
  }
}

// Boot: load passkeys
passkeys = await loadPasskeysFromDb();

// Challenge store: challengeId -> { challenge, type, userId, expires }
// Short-lived, in-memory only. Cleared on restart.
const challenges = {};

// Agent QR auth challenges: challengeId -> { qrBuffer, status, token, agentId, expires }
const agentAuthChallenges = {};
const AGENT_AUTH_EXPIRY_MS = 5 * 60 * 1000;

// QR login sessions (Chrome fallback): sessionId -> { qrBuffer, status, agentId, apiKey, handle, expires }
const qrLoginSessions = {};
const QR_LOGIN_EXPIRY_MS = 5 * 60 * 1000;

// Session ID -> { transport, server, identity, lastActivity }
const sessions = {};

// ---------- OAuth 2.0 in-memory stores ----------
const oauthClients = {};
const oauthCodes = {};

const OAUTH_METADATA = {
  issuer: ISSUER_URL,
  authorization_endpoint: ISSUER_URL + "/oauth/authorize",
  token_endpoint: ISSUER_URL + "/oauth/token",
  registration_endpoint: ISSUER_URL + "/oauth/register",
  response_types_supported: ["code"],
  grant_types_supported: ["authorization_code"],
  code_challenge_methods_supported: ["S256"],
  token_endpoint_auth_methods_supported: ["none"],
};

const PROTECTED_RESOURCE = {
  resource: MCP_RESOURCE_URL,
  authorization_servers: [ISSUER_URL],
};

// ---------- Helpers ----------

function authenticate(req) {
  const auth = req.headers["authorization"];
  if (!auth?.startsWith("Bearer ")) return null;
  const key = auth.slice(7).trim();
  return identityForApiKey(key);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Request body read timeout")), MAX_REQUEST_BODY_MS);
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      clearTimeout(timer);
      try { const raw = Buffer.concat(chunks).toString(); resolve(raw ? JSON.parse(raw) : undefined); }
      catch (e) { reject(e); }
    });
    req.on("error", (e) => { clearTimeout(timer); reject(e); });
  });
}

function readBodyRaw(req) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Request body read timeout")), MAX_REQUEST_BODY_MS);
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => { clearTimeout(timer); resolve(Buffer.concat(chunks).toString()); });
    req.on("error", (e) => { clearTimeout(timer); reject(e); });
  });
}

function json(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

function htmlResponse(res, status, body) {
  res.writeHead(status, { "Content-Type": "text/html; charset=utf-8" });
  res.end(body);
}

function rpcError(res, status, code, message) {
  json(res, status, { jsonrpc: "2.0", error: { code, message }, id: null });
}

function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, Mcp-Session-Id, Last-Event-ID");
  res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
}

function generateApiKey() {
  return "ck-" + randomUUID().replace(/-/g, "");
}

function parseUrl(reqUrl) {
  return new URL(reqUrl, "http://localhost");
}

// ── Rate limiting (F-008 in the VPS hosted-mcp audit) ───────────────
//
// Per-IP, per-bucket fixed-window counter. In-process Map; resets on
// restart. nginx-side limit_req would be more durable but harder to
// scope per route; in-process keeps the policy with the code that
// mints/validates the auth tokens. Defaults are conservative; tune via
// env. Stale entries are pruned periodically so memory stays bounded.
//
// Buckets:
//   mint     ... endpoints that issue a credential or ticket
//   validate ... endpoints that consume / verify a credential
//   status   ... poll-friendly endpoints (higher limit)

const RATE_LIMIT_BUCKETS = {
  mint:     { limit: parseInt(process.env.LDM_HOSTED_MCP_RL_MINT     || "30",  10), windowMs: 60_000 },
  validate: { limit: parseInt(process.env.LDM_HOSTED_MCP_RL_VALIDATE || "60",  10), windowMs: 60_000 },
  status:   { limit: parseInt(process.env.LDM_HOSTED_MCP_RL_STATUS   || "120", 10), windowMs: 60_000 },
};

const rateLimitState = new Map(); // key: "<bucket>:<ip>" -> { count, windowStart }

function getClientIp(req) {
  // Prefer X-Real-IP (nginx overwrites on proxy hop, harder to spoof
  // through the proxy). Fall back to the LAST entry in X-Forwarded-For
  // (nginx appends $remote_addr via proxy_add_x_forwarded_for, so the
  // last entry is the real client IP from nginx's perspective; the
  // first entries are attacker-controlled). Last fallback: socket.
  const xRealIp = req.headers["x-real-ip"];
  if (typeof xRealIp === "string" && xRealIp.length > 0) return xRealIp.trim();
  const xff = req.headers["x-forwarded-for"];
  if (typeof xff === "string" && xff.length > 0) {
    const parts = xff.split(",").map(s => s.trim()).filter(Boolean);
    if (parts.length > 0) return parts[parts.length - 1];
  }
  return req.socket?.remoteAddress || "unknown";
}

function rateLimitCheck(req, bucket) {
  const config = RATE_LIMIT_BUCKETS[bucket];
  if (!config) return { ok: true };
  const ip = getClientIp(req);
  const key = bucket + ":" + ip;
  const now = Date.now();
  const entry = rateLimitState.get(key);
  if (!entry || now - entry.windowStart > config.windowMs) {
    rateLimitState.set(key, { count: 1, windowStart: now });
    return { ok: true };
  }
  entry.count += 1;
  if (entry.count > config.limit) {
    const retryAfterSec = Math.max(1, Math.ceil((config.windowMs - (now - entry.windowStart)) / 1000));
    return { ok: false, retryAfterSec };
  }
  return { ok: true };
}

// Returns true if the request is allowed. If limited, writes 429 and
// returns false; the caller must `return` immediately on false.
function applyRateLimit(req, res, bucket) {
  const result = rateLimitCheck(req, bucket);
  if (!result.ok) {
    res.setHeader("Retry-After", String(result.retryAfterSec));
    json(res, 429, { error: "rate_limit_exceeded", error_description: "Too many requests. Retry after " + result.retryAfterSec + "s." });
    console.warn("rate-limit hit:", bucket, getClientIp(req), req.method, req.url?.split("?")[0]);
    return false;
  }
  return true;
}

// Keep memory bounded: drop entries older than 2 windows.
setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of rateLimitState) {
    if (now - entry.windowStart > 2 * 60_000) {
      rateLimitState.delete(key);
    }
  }
}, 5 * 60_000).unref();

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function sanitizeDisplayLabel(raw) {
  if (!raw || typeof raw !== "string") return null;
  const cleaned = raw.replace(/[\u0000-\u001f\u007f]/g, "").replace(/\s+/g, " ").trim().slice(0, 64);
  return cleaned.length > 0 ? cleaned : null;
}

// ---------- Session cleanup ----------

function touchSession(sid) {
  if (sessions[sid]) sessions[sid].lastActivity = Date.now();
}

function cleanupStaleSessions() {
  const now = Date.now();
  let cleaned = 0;
  for (const sid of Object.keys(sessions)) {
    const age = now - (sessions[sid].lastActivity || 0);
    if (age > SESSION_TIMEOUT_MS) {
      try { sessions[sid].transport.close(); } catch {}
      delete sessions[sid];
      cleaned++;
    }
  }
  if (cleaned > 0) {
    console.log("Session cleanup: removed " + cleaned + " stale session(s). Active: " + Object.keys(sessions).length);
  }
}

const cleanupTimer = setInterval(cleanupStaleSessions, SESSION_CLEANUP_INTERVAL_MS);
cleanupTimer.unref();

function cleanupExpiredCodes() {
  const now = Date.now();
  for (const code of Object.keys(oauthCodes)) {
    if (now > oauthCodes[code].expires) delete oauthCodes[code];
  }
}

function cleanupExpiredChallenges() {
  const now = Date.now();
  for (const id of Object.keys(challenges)) {
    if (now > challenges[id].expires) delete challenges[id];
  }
  for (const id of Object.keys(agentAuthChallenges)) {
    if (now > agentAuthChallenges[id].expires) delete agentAuthChallenges[id];
  }
  for (const id of Object.keys(qrLoginSessions)) {
    if (now > qrLoginSessions[id].expires) delete qrLoginSessions[id];
  }
}

// ---------- Shared HTML / CSS ----------

const PAGE_STYLES = `
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #0a0a0a; color: #e0e0e0;
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; padding: 20px;
}
.card {
  background: #1a1a1a; border: 1px solid #333; border-radius: 12px;
  padding: 40px; max-width: 400px; width: 100%; text-align: center;
}
.crystal { font-size: 48px; margin-bottom: 16px; }
h1 { font-size: 20px; font-weight: 600; margin-bottom: 8px; }
.subtitle { color: #888; font-size: 14px; margin-bottom: 24px; }
.btn {
  display: block; width: 100%; padding: 14px; border: none; border-radius: 8px;
  font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s;
  margin-bottom: 12px; text-decoration: none; text-align: center;
}
.btn-primary { background: #7c5cbf; color: white; }
.btn-primary:hover { background: #6a4dab; }
.btn-secondary { background: #2a2a2a; color: #e0e0e0; border: 1px solid #444; }
.btn-secondary:hover { background: #333; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.divider { color: #555; font-size: 13px; margin: 8px 0 16px; }
.footer { margin-top: 24px; font-size: 12px; color: #555; }
.status { margin-top: 16px; font-size: 14px; padding: 12px; border-radius: 8px; display: none; }
.status.success { display: block; background: #1a2e1a; color: #4caf50; border: 1px solid #2e4a2e; }
.status.error { display: block; background: #2e1a1a; color: #ef5350; border: 1px solid #4a2e2e; }
.status.loading { display: block; background: #1a1a2e; color: #7c5cbf; border: 1px solid #2e2e4a; }
.link { color: #7c5cbf; text-decoration: none; font-size: 13px; }
.link:hover { text-decoration: underline; }
`;

function pageShell(title, bodyContent) {
  return '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    + '<meta charset="utf-8">\n'
    + '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    + '<title>' + esc(title) + '</title>\n'
    + '<style>' + PAGE_STYLES + '</style>\n'
    + '</head>\n<body>\n' + bodyContent + '\n</body>\n</html>';
}

// ---------- Shared WebAuthn JS helpers (inlined into pages) ----------

const WEBAUTHN_HELPERS = `
function b64urlToBytes(b64url) {
  const b64 = b64url.replace(/-/g, "+").replace(/_/g, "/");
  const pad = b64.length % 4 === 0 ? "" : "=".repeat(4 - (b64.length % 4));
  const bin = atob(b64 + pad);
  return Uint8Array.from(bin, c => c.charCodeAt(0));
}
function bytesToB64url(bytes) {
  let bin = "";
  for (const b of new Uint8Array(bytes)) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\\+/g, "-").replace(/\\//g, "_").replace(/=+$/, "");
}
function setStatus(msg, type) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = "status " + type;
}
`;

// ---------- WebAuthn route handlers ----------

// POST /webauthn/register-options
async function handleRegisterOptions(req, res) {
  cleanupExpiredChallenges();

  let body;
  try { body = await readBody(req); } catch { body = {}; }

  // Accept the existing `username` field for wire compatibility, but
  // treat it only as a display label for the passkey prompt. It is not
  // a public username, account handle, or relay tenant boundary.
  // Duplicate display labels are allowed.
  const displayLabel = sanitizeDisplayLabel(body?.displayName || body?.username);

  const userId = randomBytes(16);
  const userIdB64 = userId.toString("base64url");

  const userName = displayLabel || ("user-" + userIdB64.slice(0, 8));
  const displayName = displayLabel || "Memory Crystal User";

  let options;
  try {
    options = await generateRegistrationOptions({
      rpName: RP_NAME,
      rpID: RP_ID,
      userName: userName,
      userDisplayName: displayName,
      userID: userId,
      attestationType: "none",
      authenticatorSelection: {
        authenticatorAttachment: "platform",
        userVerification: "required",
        residentKey: "required",
      },
      supportedAlgorithmIDs: [-7, -257],
    });
  } catch (err) {
    console.error("WebAuthn register-options error:", err);
    json(res, 500, { error: "Failed to generate registration options" });
    return;
  }

  const challengeId = randomUUID();
  challenges[challengeId] = {
    challenge: options.challenge,
    type: "registration",
    userId: userIdB64,
    displayLabel,
    expires: Date.now() + 120000,
  };

  json(res, 200, { challengeId, options });
}

// POST /webauthn/register-verify
async function handleRegisterVerify(req, res) {
  let body;
  try { body = await readBody(req); } catch { json(res, 400, { error: "Invalid request body" }); return; }

  const { challengeId, credential } = body || {};
  if (!challengeId || !credential) {
    json(res, 400, { error: "Missing challengeId or credential" });
    return;
  }

  const stored = challenges[challengeId];
  if (!stored || stored.type !== "registration") {
    json(res, 400, { error: "Invalid or expired challenge" });
    return;
  }
  if (Date.now() > stored.expires) {
    delete challenges[challengeId];
    json(res, 400, { error: "Challenge expired" });
    return;
  }

  delete challenges[challengeId];

  let verification;
  try {
    verification = await verifyRegistrationResponse({
      response: credential,
      expectedChallenge: stored.challenge,
      expectedOrigin: RP_ORIGIN,
      expectedRPID: RP_ID,
      requireUserVerification: true,
    });
  } catch (err) {
    console.error("WebAuthn register-verify error:", err);
    json(res, 400, { error: "Verification failed: " + err.message });
    return;
  }

  if (!verification.verified || !verification.registrationInfo) {
    json(res, 400, { error: "Registration verification failed" });
    return;
  }

  const { credential: cred, credentialDeviceType, credentialBackedUp } = verification.registrationInfo;

  // Internal tenancy is the immutable WebAuthn user id. The user-entered
  // display label is metadata only and never owns a relay namespace.
  const agentId = accountTenantIdForUserId(stored.userId);
  // credentialLabel matches the userName passed to
  // generateRegistrationOptions in handleRegisterOptions, which is what
  // iOS Passwords / 1Password show next to the saved passkey. The
  // welcome view should display this, not agentId. Auth semantics are
  // unchanged; only the user-facing label is aligned with the saved
  // credential.
  const credentialLabel = stored.displayLabel || ("user-" + stored.userId.slice(0, 8));
  const apiKey = generateApiKey();

  const entry = {
    credentialId: cred.id,
    publicKey: Buffer.from(cred.publicKey).toString("base64url"),
    counter: cred.counter,
    userId: stored.userId,
    agentId,
    handle: credentialLabel,
    apiKey,
    deviceType: credentialDeviceType,
    backedUp: credentialBackedUp,
    transports: credential.response?.transports || [],
    createdAt: new Date().toISOString(),
  };
  try {
    await savePasskey(entry);
    await saveApiKey(apiKey, agentId, { handle: credentialLabel });
  } catch (err) {
    console.error("Persistence failure during passkey registration:", err.message);
    json(res, 500, { error: "persistence_failure", error_description: "Could not persist credentials. Try again." });
    return;
  }

  console.log("WebAuthn: registered passkey for tenant '" + agentId + "' handle '" + credentialLabel + "' (credId: " + cred.id.slice(0, 16) + "...)");

  json(res, 200, {
    success: true,
    agentId: credentialLabel,
    tenantId: agentId,
    apiKey,
    credentialLabel,
    codex_pair_presence_token: generateCodexPairPresenceToken(agentId),
  });
}

// POST /webauthn/auth-options
async function handleAuthOptions(req, res) {
  cleanupExpiredChallenges();

  let options;
  try {
    options = await generateAuthenticationOptions({
      rpID: RP_ID,
      userVerification: "required",
    });
  } catch (err) {
    console.error("WebAuthn auth-options error:", err);
    json(res, 500, { error: "Failed to generate authentication options" });
    return;
  }

  const challengeId = randomUUID();
  challenges[challengeId] = {
    challenge: options.challenge,
    type: "authentication",
    expires: Date.now() + 120000,
  };

  json(res, 200, { challengeId, options });
}

// POST /webauthn/auth-verify
async function handleAuthVerify(req, res) {
  let body;
  try { body = await readBody(req); } catch { json(res, 400, { error: "Invalid request body" }); return; }

  const { challengeId, credential } = body || {};
  if (!challengeId || !credential) {
    json(res, 400, { error: "Missing challengeId or credential" });
    return;
  }

  const stored = challenges[challengeId];
  if (!stored || stored.type !== "authentication") {
    json(res, 400, { error: "Invalid or expired challenge" });
    return;
  }
  if (Date.now() > stored.expires) {
    delete challenges[challengeId];
    json(res, 400, { error: "Challenge expired" });
    return;
  }

  delete challenges[challengeId];

  const credId = credential.id;
  const entry = passkeys.find((p) => p.credentialId === credId);
  if (!entry) {
    json(res, 400, { error: "Unknown credential. Please create an account first." });
    return;
  }

  let verification;
  try {
    verification = await verifyAuthenticationResponse({
      response: credential,
      expectedChallenge: stored.challenge,
      expectedOrigin: RP_ORIGIN,
      expectedRPID: RP_ID,
      requireUserVerification: true,
      credential: {
        id: entry.credentialId,
        publicKey: Uint8Array.from(Buffer.from(entry.publicKey, "base64url")),
        counter: entry.counter,
        transports: entry.transports || [],
      },
    });
  } catch (err) {
    console.error("WebAuthn auth-verify error:", err);
    json(res, 400, { error: "Authentication failed: " + err.message });
    return;
  }

  if (!verification.verified) {
    json(res, 400, { error: "Authentication verification failed" });
    return;
  }

  // Persist new counter before mutating in-memory entry. updatePasskeyCounter
  // performs the in-memory update only on success, so the in-memory counter
  // stays consistent with the DB and replay protection holds across restarts.
  try {
    await updatePasskeyCounter(entry.credentialId, verification.authenticationInfo.newCounter);
  } catch (err) {
    console.error("Persistence failure during passkey counter update:", err.message);
    json(res, 500, { error: "persistence_failure", error_description: "Could not persist counter. Try again." });
    return;
  }

  let credentialLabel = entry.handle;
  if (!credentialLabel && entry.agentId && entry.agentId.startsWith("passkey-")) {
    credentialLabel = (typeof entry.userId === "string" && entry.userId.length >= 8)
      ? "user-" + entry.userId.slice(0, 8)
      : entry.agentId;
  } else if (!credentialLabel && !isInternalTenantId(entry.agentId)) {
    credentialLabel = entry.agentId;
  } else if (!credentialLabel && typeof entry.userId === "string" && entry.userId.length >= 8) {
    credentialLabel = "user-" + entry.userId.slice(0, 8);
  } else if (!credentialLabel) {
    credentialLabel = "you";
  }

  // Recovery path: a passkey reloaded from Postgres after a restart may
  // have entry.apiKey = null if no ApiKey row was found for its agent
  // at boot. Mint a fresh ck- now so the login response always carries
  // a usable token. Without this, the browser would store
  // sessionStorage.wip_api_key = null and Remote Control would 401 on
  // /bootstrap and /ws-ticket.
  if (!entry.apiKey) {
    const newKey = generateApiKey();
    try {
      await saveApiKey(newKey, entry.agentId, { handle: credentialLabel });
    } catch (err) {
      console.error("Persistence failure minting recovery key for tenant '" + entry.agentId + "':", err.message);
      json(res, 500, { error: "persistence_failure", error_description: "Could not mint API key. Try again." });
      return;
    }
    entry.apiKey = newKey;
    entry.handle = credentialLabel;
    console.log("WebAuthn: minted recovery key for tenant '" + entry.agentId + "' (key: " + newKey.slice(0, 6) + "...)");
  }

  console.log("WebAuthn: authenticated tenant '" + entry.agentId + "' handle '" + credentialLabel + "'");

  json(res, 200, {
    success: true,
    agentId: credentialLabel,
    tenantId: entry.agentId,
    apiKey: entry.apiKey,
    credentialLabel,
    codex_pair_presence_token: generateCodexPairPresenceToken(entry.agentId),
  });
}

// ---------- Page handlers ----------

function handleSignupPage(req, res) {
  const body = '<div class="card">\n'
    + '<div class="crystal">\u{1F48E}</div>\n'
    + '<h1>Create your account</h1>\n'
    + '<p class="subtitle">Memory Crystal ... wip.computer</p>\n'
    + '<button class="btn btn-primary" id="createBtn" onclick="createPasskey()">Create Passkey</button>\n'
    + '<div id="status" class="status"></div>\n'
    + '<p class="footer"><a href="/login" class="link">Already have an account? Sign in</a></p>\n'
    + '<p class="footer">Learning Dreaming Machines</p>\n'
    + '</div>\n'
    + '<script>\n'
    + WEBAUTHN_HELPERS
    + 'async function createPasskey() {\n'
    + '  const btn = document.getElementById("createBtn");\n'
    + '  btn.disabled = true;\n'
    + '  setStatus("Preparing...", "loading");\n'
    + '  try {\n'
    + '    const optRes = await fetch("/webauthn/register-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    const { challengeId, options } = await optRes.json();\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    options.user.id = b64urlToBytes(options.user.id);\n'
    + '    if (options.excludeCredentials) {\n'
    + '      options.excludeCredentials = options.excludeCredentials.map(c => ({ ...c, id: b64urlToBytes(c.id) }));\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    const credential = await navigator.credentials.create({ publicKey: options });\n'
    + '    const reqBody = {\n'
    + '      challengeId,\n'
    + '      credential: {\n'
    + '        id: credential.id,\n'
    + '        rawId: bytesToB64url(credential.rawId),\n'
    + '        type: credential.type,\n'
    + '        response: {\n'
    + '          attestationObject: bytesToB64url(credential.response.attestationObject),\n'
    + '          clientDataJSON: bytesToB64url(credential.response.clientDataJSON),\n'
    + '          transports: credential.response.getTransports ? credential.response.getTransports() : [],\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    const verRes = await fetch("/webauthn/register-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    const result = await verRes.json();\n'
    + '    if (result.success) {\n'
    + '      setStatus("Account created. You can close this page.", "success");\n'
    + '      btn.textContent = "Done";\n'
    + '    } else {\n'
    + '      setStatus(result.error || "Registration failed", "error");\n'
    + '      btn.disabled = false;\n'
    + '    }\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") {\n'
    + '      setStatus("Cancelled. Try again when ready.", "error");\n'
    + '    } else {\n'
    + '      setStatus("Error: " + err.message, "error");\n'
    + '    }\n'
    + '    btn.disabled = false;\n'
    + '  }\n'
    + '}\n'
    + '</script>';

  htmlResponse(res, 200, pageShell("Create Account - Memory Crystal", body));
}

function handleLoginPage(req, res) {
  const body = '<div class="card">\n'
    + '<div class="crystal">\u{1F48E}</div>\n'
    + '<h1>Sign in</h1>\n'
    + '<p class="subtitle">Memory Crystal ... wip.computer</p>\n'
    + '<button class="btn btn-primary" id="signInBtn" onclick="signIn()">Sign in with Passkey</button>\n'
    + '<div id="status" class="status"></div>\n'
    + '<p class="footer"><a href="/signup" class="link">Need an account? Create one</a></p>\n'
    + '<p class="footer">Learning Dreaming Machines</p>\n'
    + '</div>\n'
    + '<script>\n'
    + WEBAUTHN_HELPERS
    + 'async function signIn() {\n'
    + '  const btn = document.getElementById("signInBtn");\n'
    + '  btn.disabled = true;\n'
    + '  setStatus("Preparing...", "loading");\n'
    + '  try {\n'
    + '    const optRes = await fetch("/webauthn/auth-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    const { challengeId, options } = await optRes.json();\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    if (options.allowCredentials) {\n'
    + '      options.allowCredentials = options.allowCredentials.map(c => ({ ...c, id: b64urlToBytes(c.id) }));\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    const assertion = await navigator.credentials.get({ publicKey: options });\n'
    + '    const reqBody = {\n'
    + '      challengeId,\n'
    + '      credential: {\n'
    + '        id: assertion.id,\n'
    + '        rawId: bytesToB64url(assertion.rawId),\n'
    + '        type: assertion.type,\n'
    + '        response: {\n'
    + '          authenticatorData: bytesToB64url(assertion.response.authenticatorData),\n'
    + '          clientDataJSON: bytesToB64url(assertion.response.clientDataJSON),\n'
    + '          signature: bytesToB64url(assertion.response.signature),\n'
    + '          userHandle: assertion.response.userHandle ? bytesToB64url(assertion.response.userHandle) : null,\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    const verRes = await fetch("/webauthn/auth-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    const result = await verRes.json();\n'
    + '    if (result.success) {\n'
    + '      setStatus("Signed in as " + result.agentId + ". You can close this page.", "success");\n'
    + '      btn.textContent = "Done";\n'
    + '    } else {\n'
    + '      setStatus(result.error || "Authentication failed", "error");\n'
    + '      btn.disabled = false;\n'
    + '    }\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") {\n'
    + '      setStatus("Cancelled. Try again when ready.", "error");\n'
    + '    } else {\n'
    + '      setStatus("Error: " + err.message, "error");\n'
    + '    }\n'
    + '    btn.disabled = false;\n'
    + '  }\n'
    + '}\n'
    + '</script>';

  htmlResponse(res, 200, pageShell("Sign In - Memory Crystal", body));
}

// ---------- OAuth route handlers ----------

function handleOAuthDiscovery(req, res) {
  json(res, 200, OAUTH_METADATA);
}

function handleProtectedResource(req, res) {
  json(res, 200, PROTECTED_RESOURCE);
}

async function handleOAuthRegister(req, res) {
  let body;
  try { body = await readBody(req); } catch { json(res, 400, { error: "invalid_request" }); return; }

  const clientId = randomUUID();
  const client = {
    client_id: clientId,
    redirect_uris: body?.redirect_uris || [],
    client_name: body?.client_name || "unknown",
    created: Date.now(),
  };
  oauthClients[clientId] = client;
  console.log("OAuth: registered client " + clientId + " (" + client.client_name + ")");

  json(res, 201, {
    client_id: clientId,
    client_name: client.client_name,
    redirect_uris: client.redirect_uris,
    grant_types: ["authorization_code"],
    response_types: ["code"],
    token_endpoint_auth_method: "none",
  });
}

function handleOAuthAuthorize(req, res) {
  const url = parseUrl(req.url);
  const clientId = url.searchParams.get("client_id") || "";
  const responseType = url.searchParams.get("response_type");
  const redirectUri = url.searchParams.get("redirect_uri") || "";
  const state = url.searchParams.get("state") || "";
  const codeChallenge = url.searchParams.get("code_challenge") || "";
  const codeChallengeMethod = url.searchParams.get("code_challenge_method") || "S256";

  if (responseType !== "code") {
    htmlResponse(res, 400, pageShell("Error", '<div class="card"><h1>Error</h1><p class="subtitle">Unsupported response_type</p></div>'));
    return;
  }
  if (!redirectUri) {
    htmlResponse(res, 400, pageShell("Error", '<div class="card"><h1>Error</h1><p class="subtitle">Missing redirect_uri</p></div>'));
    return;
  }

  // Auto-register client
  if (clientId && !oauthClients[clientId]) {
    oauthClients[clientId] = { client_id: clientId, redirect_uris: [redirectUri], client_name: "auto", created: Date.now() };
  }

  // Encode OAuth params for the JS to use after WebAuthn
  const oauthParams = JSON.stringify({
    client_id: clientId,
    redirect_uri: redirectUri,
    state: state,
    code_challenge: codeChallenge,
    code_challenge_method: codeChallengeMethod,
  });

  const pageBody = '<div class="card">\n'
    + '<div class="crystal">\u{1F48E}</div>\n'
    + '<h1>Connect to Memory Crystal</h1>\n'
    + '<p class="subtitle">wip.computer MCP server</p>\n'
    + '<button class="btn btn-primary" id="signInBtn" onclick="doAuth()">Sign In</button>\n'
    + '<div class="divider">or</div>\n'
    + '<button class="btn btn-secondary" id="createBtn" onclick="doRegister()">Create Account</button>\n'
    + '<div id="status" class="status"></div>\n'
    + '<p class="footer">Learning Dreaming Machines</p>\n'
    + '</div>\n'
    + '<script>\n'
    + WEBAUTHN_HELPERS
    + 'const oauthParams = ' + oauthParams + ';\n'
    + 'function disableButtons() {\n'
    + '  document.getElementById("signInBtn").disabled = true;\n'
    + '  document.getElementById("createBtn").disabled = true;\n'
    + '}\n'
    + 'function enableButtons() {\n'
    + '  document.getElementById("signInBtn").disabled = false;\n'
    + '  document.getElementById("createBtn").disabled = false;\n'
    + '}\n'
    + 'function completeOAuth(agentId) {\n'
    + '  setStatus("Connecting...", "loading");\n'
    + '  const form = document.createElement("form");\n'
    + '  form.method = "POST";\n'
    + '  form.action = "/oauth/authorize/submit";\n'
    + '  const fields = {\n'
    + '    client_id: oauthParams.client_id,\n'
    + '    redirect_uri: oauthParams.redirect_uri,\n'
    + '    state: oauthParams.state,\n'
    + '    code_challenge: oauthParams.code_challenge,\n'
    + '    code_challenge_method: oauthParams.code_challenge_method,\n'
    + '    agent_name: agentId,\n'
    + '  };\n'
    + '  for (const [k, v] of Object.entries(fields)) {\n'
    + '    const input = document.createElement("input");\n'
    + '    input.type = "hidden";\n'
    + '    input.name = k;\n'
    + '    input.value = v;\n'
    + '    form.appendChild(input);\n'
    + '  }\n'
    + '  document.body.appendChild(form);\n'
    + '  form.submit();\n'
    + '}\n'
    + 'async function doRegister() {\n'
    + '  disableButtons();\n'
    + '  setStatus("Preparing...", "loading");\n'
    + '  try {\n'
    + '    const optRes = await fetch("/webauthn/register-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    const { challengeId, options } = await optRes.json();\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    options.user.id = b64urlToBytes(options.user.id);\n'
    + '    if (options.excludeCredentials) {\n'
    + '      options.excludeCredentials = options.excludeCredentials.map(c => ({ ...c, id: b64urlToBytes(c.id) }));\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    const credential = await navigator.credentials.create({ publicKey: options });\n'
    + '    const reqBody = {\n'
    + '      challengeId,\n'
    + '      credential: {\n'
    + '        id: credential.id,\n'
    + '        rawId: bytesToB64url(credential.rawId),\n'
    + '        type: credential.type,\n'
    + '        response: {\n'
    + '          attestationObject: bytesToB64url(credential.response.attestationObject),\n'
    + '          clientDataJSON: bytesToB64url(credential.response.clientDataJSON),\n'
    + '          transports: credential.response.getTransports ? credential.response.getTransports() : [],\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    const verRes = await fetch("/webauthn/register-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    const result = await verRes.json();\n'
    + '    if (result.success) {\n'
    + '      completeOAuth(result.agentId);\n'
    + '    } else {\n'
    + '      setStatus(result.error || "Registration failed", "error");\n'
    + '      enableButtons();\n'
    + '    }\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") {\n'
    + '      setStatus("Cancelled. Try again when ready.", "error");\n'
    + '    } else {\n'
    + '      setStatus("Error: " + err.message, "error");\n'
    + '    }\n'
    + '    enableButtons();\n'
    + '  }\n'
    + '}\n'
    + 'async function doAuth() {\n'
    + '  disableButtons();\n'
    + '  setStatus("Preparing...", "loading");\n'
    + '  try {\n'
    + '    const optRes = await fetch("/webauthn/auth-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    const { challengeId, options } = await optRes.json();\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    if (options.allowCredentials) {\n'
    + '      options.allowCredentials = options.allowCredentials.map(c => ({ ...c, id: b64urlToBytes(c.id) }));\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    const assertion = await navigator.credentials.get({ publicKey: options });\n'
    + '    const reqBody = {\n'
    + '      challengeId,\n'
    + '      credential: {\n'
    + '        id: assertion.id,\n'
    + '        rawId: bytesToB64url(assertion.rawId),\n'
    + '        type: assertion.type,\n'
    + '        response: {\n'
    + '          authenticatorData: bytesToB64url(assertion.response.authenticatorData),\n'
    + '          clientDataJSON: bytesToB64url(assertion.response.clientDataJSON),\n'
    + '          signature: bytesToB64url(assertion.response.signature),\n'
    + '          userHandle: assertion.response.userHandle ? bytesToB64url(assertion.response.userHandle) : null,\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    const verRes = await fetch("/webauthn/auth-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    const result = await verRes.json();\n'
    + '    if (result.success) {\n'
    + '      completeOAuth(result.agentId);\n'
    + '    } else {\n'
    + '      setStatus(result.error || "Authentication failed", "error");\n'
    + '      enableButtons();\n'
    + '    }\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") {\n'
    + '      setStatus("Cancelled. Try again when ready.", "error");\n'
    + '    } else {\n'
    + '      setStatus("Error: " + err.message, "error");\n'
    + '    }\n'
    + '    enableButtons();\n'
    + '  }\n'
    + '}\n'
    + '</script>';

  htmlResponse(res, 200, pageShell("Connect to Memory Crystal", pageBody));
}

async function handleOAuthAuthorizeSubmit(req, res) {
  const raw = await readBodyRaw(req);
  const params = new URLSearchParams(raw);
  const clientId = params.get("client_id");
  const redirectUri = params.get("redirect_uri");
  const state = params.get("state");
  const codeChallenge = params.get("code_challenge");
  const codeChallengeMethod = params.get("code_challenge_method") || "S256";
  const agentName = params.get("agent_name") || "unknown";

  cleanupExpiredCodes();

  const code = randomUUID();
  oauthCodes[code] = {
    client_id: clientId,
    redirect_uri: redirectUri,
    code_challenge: codeChallenge,
    code_challenge_method: codeChallengeMethod,
    agent_name: agentName.trim().toLowerCase(),
    expires: Date.now() + OAUTH_CODE_EXPIRY_MS,
  };

  console.log("OAuth: issued code for agent '" + agentName + "' (client: " + clientId + ")");

  const redirect = new URL(redirectUri);
  redirect.searchParams.set("code", code);
  if (state) redirect.searchParams.set("state", state);

  res.writeHead(302, { Location: redirect.toString() });
  res.end();
}

async function handleOAuthToken(req, res) {
  let raw;
  try { raw = await readBodyRaw(req); } catch { json(res, 400, { error: "invalid_request" }); return; }

  const params = new URLSearchParams(raw);
  const grantType = params.get("grant_type");
  const code = params.get("code");
  const redirectUri = params.get("redirect_uri");
  const codeVerifier = params.get("code_verifier");

  if (grantType !== "authorization_code") {
    json(res, 400, { error: "unsupported_grant_type" });
    return;
  }

  const stored = oauthCodes[code];
  if (!stored) {
    json(res, 400, { error: "invalid_grant", error_description: "Unknown or expired code" });
    return;
  }

  delete oauthCodes[code];

  if (Date.now() > stored.expires) {
    json(res, 400, { error: "invalid_grant", error_description: "Code expired" });
    return;
  }

  if (redirectUri && redirectUri !== stored.redirect_uri) {
    json(res, 400, { error: "invalid_grant", error_description: "redirect_uri mismatch" });
    return;
  }

  if (stored.code_challenge && codeVerifier) {
    const expected = createHash("sha256").update(codeVerifier).digest("base64url");
    if (expected !== stored.code_challenge) {
      json(res, 400, { error: "invalid_grant", error_description: "PKCE verification failed" });
      return;
    }
  }

  const agentHandle = stored.agent_name || "oauth-user";
  const apiKey = generateApiKey();
  const agentId = oauthTenantIdForApiKey(apiKey);
  try {
    await saveApiKey(apiKey, agentId, { handle: agentHandle });
  } catch (err) {
    console.error("Persistence failure during OAuth token issuance:", err.message);
    json(res, 500, { error: "server_error", error_description: "Could not issue token. Try again." });
    return;
  }

  console.log("OAuth: issued token for tenant '" + agentId + "' handle '" + agentHandle + "' (key: " + apiKey.slice(0, 10) + "...)");

  json(res, 200, {
    access_token: apiKey,
    token_type: "Bearer",
    scope: "mcp",
  });
}

// ---------- Agent QR Auth handlers ----------

// GET /demo/api/agent-auth?agent=NAME&message=TEXT ... generate a QR challenge for an agent
async function handleAgentAuthStart(req, res) {
  cleanupExpiredChallenges();
  const url = parseUrl(req.url);
  const agentName = (url.searchParams.get("agent") || "").trim().slice(0, 60);
  const agentMessage = (url.searchParams.get("message") || "").trim().slice(0, 200);
  const challengeId = randomUUID();
  const approveUrl = ISSUER_URL + "/approve?c=" + challengeId;
  const qrBuffer = await QRCode.toBuffer(approveUrl, { type: "png", width: 400, margin: 2 });
  agentAuthChallenges[challengeId] = {
    qrBuffer,
    status: "pending",
    token: null,
    agentId: null,
    agentName: agentName || null,
    agentMessage: agentMessage || null,
    expires: Date.now() + AGENT_AUTH_EXPIRY_MS,
  };
  console.log("Agent QR auth: created challenge " + challengeId.slice(0, 8) + "..." + (agentName ? " (agent: " + agentName + ")" : ""));
  json(res, 200, { challengeId, approveUrl, qrUrl: "/demo/api/agent-auth/qr?c=" + challengeId });
}

// GET /demo/api/agent-auth/qr?c=XXX ... serve QR code PNG
function handleAgentAuthQR(req, res) {
  const url = parseUrl(req.url);
  const c = url.searchParams.get("c");
  const entry = agentAuthChallenges[c];
  if (!entry || Date.now() > entry.expires) {
    json(res, 404, { error: "Challenge not found or expired" });
    return;
  }
  res.writeHead(200, { "Content-Type": "image/png", "Content-Length": entry.qrBuffer.length });
  res.end(entry.qrBuffer);
}

// GET /demo/api/agent-auth/status?c=XXX ... poll for approval
function handleAgentAuthStatus(req, res) {
  const url = parseUrl(req.url);
  const c = url.searchParams.get("c");
  const entry = agentAuthChallenges[c];
  if (!entry || Date.now() > entry.expires) {
    json(res, 404, { error: "Challenge not found or expired" });
    return;
  }
  if (entry.status === "approved") {
    json(res, 200, { status: "approved", token: entry.token, agentId: entry.agentId });
    delete agentAuthChallenges[c]; // one-time use
  } else {
    json(res, 200, { status: "pending" });
  }
}

// GET /approve?c=XXX ... page the human sees when authorizing an agent
function handleApprovePage(req, res) {
  const url = parseUrl(req.url);
  let challengeId = url.searchParams.get("c") || "";
  let entry = agentAuthChallenges[challengeId];

  // If no challenge ID but agent params provided, create challenge on the fly
  const agentParam = (url.searchParams.get("agent") || "").trim().slice(0, 60);
  const messageParam = (url.searchParams.get("message") || "").trim().slice(0, 200);
  if (!entry && agentParam) {
    challengeId = randomUUID();
    agentAuthChallenges[challengeId] = {
      qrBuffer: null,
      status: "pending",
      token: null,
      agentId: null,
      agentName: agentParam,
      agentMessage: messageParam || null,
      expires: Date.now() + AGENT_AUTH_EXPIRY_MS,
    };
    entry = agentAuthChallenges[challengeId];
    console.log("Approve page: created inline challenge " + challengeId.slice(0, 8) + "... for agent: " + agentParam);
  }

  const expired = !entry || Date.now() > entry.expires;

  const APPROVE_STYLES = `
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  background: #FFFDF5; color: #1a1a1a;
  -webkit-text-size-adjust: 100%; -webkit-font-smoothing: antialiased;
}
.login-page {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-height: 100vh; min-height: 100dvh; padding: 24px;
}
.login-card {
  position: relative; max-width: 380px; width: 100%; text-align: center;
}
.login-title {
  font-size: 22px; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 8px;
}
.login-byline {
  font-size: 14px; color: #8a8580; margin-bottom: 32px; letter-spacing: 0.2px;
}
.info-section { text-align: left; margin-bottom: 20px; }
.info-section h2 { font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #1a1a1a; }
.info-section ul { list-style: none; padding: 0; margin: 0; }
.info-section ul li { font-size: 13px; color: #8a8580; line-height: 1.6; padding-left: 16px; position: relative; }
.info-section ul li::before { content: "\\2022"; position: absolute; left: 0; color: #c0bbb5; }
.info-section.safe ul li::before { color: #2E7D32; }
.revoke-note { font-size: 13px; color: #8a8580; margin-bottom: 28px; }
.btn {
  display: block; width: 100%; padding: 16px; border: none; border-radius: 12px;
  font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.15s, transform 0.1s;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  -webkit-tap-highlight-color: transparent;
}
.btn:active { transform: scale(0.98); }
.btn-primary { background: #0033FF; color: white; margin-bottom: 12px; }
.btn-primary:hover { background: #0033FF; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.create-link { font-size: 13px; color: #8a8580; cursor: pointer; text-decoration: none; }
.create-link:hover { color: #1a1a1a; }
.login-status { margin-top: 16px; font-size: 14px; padding: 12px 16px; border-radius: 10px; display: none; text-align: center; }
.login-status.show { display: block; }
.login-status.loading { background: #E8EEFF; color: #0033FF; }
.login-status.error { background: #FFF0F0; color: #D32F2F; }
.login-status.success { background: #F0FFF4; color: #2E7D32; }
.success-check { font-size: 48px; margin-bottom: 16px; }
`;

  // Shared sprite JS for rotating nav icon
  const SPRITE_JS = 'var SPRITE_COLS = 8, SPRITE_ROWS = 3, SPRITE_TOTAL = 24;\n'
    + 'function makeIconHTML(size) {\n'
    + '  var idx = Math.floor(Math.random() * SPRITE_TOTAL);\n'
    + '  var col = idx % SPRITE_COLS, row = Math.floor(idx / SPRITE_COLS);\n'
    + '  var bx = (col / (SPRITE_COLS - 1)) * 100, by = (row / (SPRITE_ROWS - 1)) * 100;\n'
    + '  return \'<div style="width:\' + size + \'px;height:\' + size + \'px;overflow:hidden;"><div style="width:100%;height:100%;background:url(/demo/sprites.png);background-size:\' + (SPRITE_COLS * 100) + \'% \' + (SPRITE_ROWS * 100) + \'%;background-position:\' + bx + \'% \' + by + \'%;"></div></div>\';\n'
    + '}\n'
    + 'var loginIcon = document.getElementById("loginIcon");\n'
    + 'if (loginIcon) loginIcon.innerHTML = makeIconHTML(28);\n'
    + 'var rotateIdx = Math.floor(Math.random() * SPRITE_TOTAL);\n'
    + 'setInterval(function() {\n'
    + '  var el = document.getElementById("loginIcon"); if (!el) return;\n'
    + '  rotateIdx = (rotateIdx + 1) % SPRITE_TOTAL;\n'
    + '  var col = rotateIdx % SPRITE_COLS, row = Math.floor(rotateIdx / SPRITE_COLS);\n'
    + '  var bx = (col / (SPRITE_COLS - 1)) * 100, by = (row / (SPRITE_ROWS - 1)) * 100;\n'
    + '  el.innerHTML = \'<div style="width:28px;height:28px;overflow:hidden;transition:opacity 0.5s;"><div style="width:100%;height:100%;background:url(/demo/sprites.png);background-size:\' + (SPRITE_COLS * 100) + \'% \' + (SPRITE_ROWS * 100) + \'%;background-position:\' + bx + \'% \' + by + \'%;"></div></div>\';\n'
    + '}, 6000);\n';

  if (expired) {
    const html = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
      + '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
      + '<title>Expired - Kaleidoscope</title><style>' + APPROVE_STYLES + '</style></head><body>'
      + '<div class="login-page"><div class="login-card">'
      + '<h1 class="login-title"><span id="loginIcon" style="display:inline-block;vertical-align:middle;margin-right:8px;margin-bottom:3px;"></span>Kaleidoscope</h1>'
      + '<p class="login-byline">Every AI. One experience.</p>'
      + '<h2 style="font-size:18px;font-weight:600;margin-bottom:12px;">Link Expired</h2>'
      + '<p style="font-size:14px;color:#8a8580;line-height:1.5;">This authorization link has expired. Ask your agent to generate a new one.</p>'
      + '</div>'
      + '<div id="kscope-footer" style="margin-top:48px;text-align:center;"></div>'
      + '</div></div>'
      + '<script src="/demo/footer.js"></script>'
      + '<script>\n' + SPRITE_JS + '</script></body></html>';
    htmlResponse(res, 200, html);
    return;
  }

  const html = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    + '<title>Authorize Agent - Kaleidoscope</title><style>' + APPROVE_STYLES + '</style></head><body>'
    + '<div class="login-page"><div class="login-card">'
    + '<h1 class="login-title"><span id="loginIcon" style="display:inline-block;vertical-align:middle;margin-right:8px;margin-bottom:3px;"></span>Kaleidoscope</h1>'
    + '<p class="login-byline">Every AI. One experience.</p>'
    + '<div id="authSection">'
    + '<h2 style="font-size:18px;font-weight:600;margin-bottom:' + (entry.agentName ? '16' : '24') + 'px;">Authorize Agent Access</h2>'
    + (entry.agentName ? '<div style="background:#F5F3ED;border:1px solid #E0DDD6;border-radius:12px;padding:16px 20px;margin-bottom:12px;text-align:left;"><div style="font-size:12px;color:#8a8580;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Agent</div><div style="font-weight:600;">' + entry.agentName.replace(/</g, '&lt;') + '</div></div>' : '')
    + (entry.agentMessage ? '<div style="background:#F5F3ED;border:1px solid #E0DDD6;border-radius:12px;padding:16px 20px;margin-bottom:24px;text-align:left;"><div style="font-size:12px;color:#8a8580;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Passphrase</div><div style="font-weight:600;">' + entry.agentMessage.replace(/</g, '&lt;') + '</div></div>' : '')
    + '<div class="info-section"><h2>What they get:</h2><ul>'
    + '<li>A session token to use your account</li>'
    + '<li>Access to your wallet balance</li>'
    + '<li>Ability to generate images, send messages, search memory</li>'
    + '</ul></div>'
    + '<div class="info-section safe"><h2>What they don\'t get:</h2><ul>'
    + '<li>Your passkey (never leaves your device)</li>'
    + '<li>Your biometric data (stays on your device)</li>'
    + '<li>Permanent access (session expires)</li>'
    + '</ul></div>'
    + '<p class="revoke-note">You can revoke access anytime.</p>'
    + '<button class="btn btn-primary" id="authBtn" onclick="doAuthorize()">\ud83e\udec6 Authorize</button>'
    + '<div style="margin-top:8px;text-align:center;">'
    + '<a class="create-link" id="createLink" onclick="doCreateAndAuthorize()">New here? Create an account first...</a>'
    + '</div>'
    + '</div>'
    + '<div id="successSection" style="display:none;">'
    + '<div class="success-check">\u2713</div>'
    + '<h2 style="font-size:18px;font-weight:600;margin-bottom:12px;">Authorized</h2>'
    + '<p style="font-size:14px;color:#8a8580;line-height:1.5;margin-bottom:20px;">Send this token to your agent:</p>'
    + '<div style="position:relative;background:#F5F3ED;border:1px solid #E0DDD6;border-radius:12px;padding:16px 48px 16px 20px;margin-bottom:12px;"><span id="tokenDisplay" style="font-family:monospace;font-size:13px;word-break:break-all;user-select:all;-webkit-user-select:all;cursor:text;"></span><button onclick="navigator.clipboard.writeText(document.getElementById(\'tokenDisplay\').textContent)" style="position:absolute;top:12px;right:12px;background:none;border:none;padding:6px;cursor:pointer;color:#8a8580;opacity:0.5;"><svg width=\\"16\\" height=\\"16\\" viewBox=\\"0 0 16 16\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.5\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"><rect x=\\"5.5\\" y=\\"5.5\\" width=\\"8\\" height=\\"8\\" rx=\\"1.5\\"/><path d=\\"M10.5 5.5V3.5C10.5 2.67 9.83 2 9 2H3.5C2.67 2 2 2.67 2 3.5V9C2 9.83 2.67 10.5 3.5 10.5H5.5\\"/></svg></button></div>'
    + '<p style="font-size:13px;color:#8a8580;">Your agent uses this as: Authorization: Bearer [token]</p>'
    + '</div>'
    + '<div class="login-status" id="status"></div>'
    + '</div>'
    + '<div id="kscope-footer" style="margin-top:48px;text-align:center;"></div>'
    + '</div></div>'
    + '<script src="/demo/footer.js"></script>'
    + '<script>\n'
    + 'var CHALLENGE_ID = ' + JSON.stringify(challengeId) + ';\n'
    + SPRITE_JS
    + 'function setStatus(msg, type) {\n'
    + '  var el = document.getElementById("status");\n'
    + '  el.textContent = msg; el.className = "login-status show " + type;\n'
    + '}\n'
    + 'function b64urlToBytes(b64url) {\n'
    + '  var b64 = b64url.replace(/-/g, "+").replace(/_/g, "/");\n'
    + '  var pad = b64.length % 4 === 0 ? "" : "=".repeat(4 - (b64.length % 4));\n'
    + '  var bin = atob(b64 + pad);\n'
    + '  return Uint8Array.from(bin, function(c) { return c.charCodeAt(0); });\n'
    + '}\n'
    + 'function bytesToB64url(bytes) {\n'
    + '  var bin = ""; var arr = new Uint8Array(bytes);\n'
    + '  for (var i = 0; i < arr.length; i++) bin += String.fromCharCode(arr[i]);\n'
    + '  return btoa(bin).replace(/\\+/g, "-").replace(/\\//g, "_").replace(/=+$/g, "");\n'
    + '}\n'
    + 'async function approveAgent(agentId, apiKey) {\n'
    + '  setStatus("Approving agent access...", "loading");\n'
    + '  var approveRes = await fetch("/demo/api/agent-auth/approve", {\n'
    + '    method: "POST", headers: { "Content-Type": "application/json" },\n'
    + '    body: JSON.stringify({ challengeId: CHALLENGE_ID, agentId: agentId, apiKey: apiKey })\n'
    + '  });\n'
    + '  var approveData = await approveRes.json();\n'
    + '  if (approveData.ok) {\n'
    + '    document.getElementById("authSection").style.display = "none";\n'
    + '    document.getElementById("successSection").style.display = "block";\n'
    + '    document.getElementById("tokenDisplay").textContent = apiKey;\n'
    + '    document.getElementById("status").className = "login-status";\n'
    + '  } else {\n'
    + '    throw new Error(approveData.error || "Failed to approve");\n'
    + '  }\n'
    + '}\n'
    + 'async function doAuthorize() {\n'
    + '  var btn = document.getElementById("authBtn"); btn.disabled = true;\n'
    + '  setStatus("Preparing...", "loading");\n'
    + '  try {\n'
    + '    var optRes = await fetch("/webauthn/auth-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    var optData = await optRes.json();\n'
    + '    var challengeId = optData.challengeId;\n'
    + '    var options = optData.options;\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    if (options.allowCredentials) {\n'
    + '      options.allowCredentials = options.allowCredentials.map(function(c) { return Object.assign({}, c, { id: b64urlToBytes(c.id) }); });\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    var assertion = await navigator.credentials.get({ publicKey: options });\n'
    + '    var reqBody = {\n'
    + '      challengeId: challengeId,\n'
    + '      credential: {\n'
    + '        id: assertion.id, rawId: bytesToB64url(assertion.rawId), type: assertion.type,\n'
    + '        response: {\n'
    + '          authenticatorData: bytesToB64url(assertion.response.authenticatorData),\n'
    + '          clientDataJSON: bytesToB64url(assertion.response.clientDataJSON),\n'
    + '          signature: bytesToB64url(assertion.response.signature),\n'
    + '          userHandle: assertion.response.userHandle ? bytesToB64url(assertion.response.userHandle) : null,\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    var verRes = await fetch("/webauthn/auth-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    var result = await verRes.json();\n'
    + '    if (!result.success) { setStatus(result.error || "Authentication failed", "error"); btn.disabled = false; return; }\n'
    + '    await approveAgent(result.agentId, result.apiKey);\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") { setStatus("Cancelled. Try again when ready.", "error"); }\n'
    + '    else { setStatus("Error: " + err.message, "error"); }\n'
    + '    btn.disabled = false;\n'
    + '  }\n'
    + '}\n'
    + 'async function doCreateAndAuthorize() {\n'
    + '  var btn = document.getElementById("authBtn"); btn.disabled = true;\n'
    + '  document.getElementById("createLink").style.display = "none";\n'
    + '  setStatus("Creating your account...", "loading");\n'
    + '  try {\n'
    + '    var optRes = await fetch("/webauthn/register-options", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });\n'
    + '    var optData = await optRes.json();\n'
    + '    var challengeId = optData.challengeId;\n'
    + '    var options = optData.options;\n'
    + '    if (!options) throw new Error("Server returned no options");\n'
    + '    options.challenge = b64urlToBytes(options.challenge);\n'
    + '    options.user.id = b64urlToBytes(options.user.id);\n'
    + '    if (options.excludeCredentials) {\n'
    + '      options.excludeCredentials = options.excludeCredentials.map(function(c) { return Object.assign({}, c, { id: b64urlToBytes(c.id) }); });\n'
    + '    }\n'
    + '    setStatus("Waiting for biometric...", "loading");\n'
    + '    var credential = await navigator.credentials.create({ publicKey: options });\n'
    + '    var reqBody = {\n'
    + '      challengeId: challengeId,\n'
    + '      credential: {\n'
    + '        id: credential.id, rawId: bytesToB64url(credential.rawId), type: credential.type,\n'
    + '        response: {\n'
    + '          attestationObject: bytesToB64url(credential.response.attestationObject),\n'
    + '          clientDataJSON: bytesToB64url(credential.response.clientDataJSON),\n'
    + '          transports: credential.response.getTransports ? credential.response.getTransports() : [],\n'
    + '        },\n'
    + '      },\n'
    + '    };\n'
    + '    setStatus("Verifying...", "loading");\n'
    + '    var verRes = await fetch("/webauthn/register-verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(reqBody) });\n'
    + '    var result = await verRes.json();\n'
    + '    if (!result.success) { setStatus(result.error || "Registration failed", "error"); btn.disabled = false; document.getElementById("createLink").style.display = ""; return; }\n'
    + '    await approveAgent(result.agentId, result.apiKey);\n'
    + '  } catch (err) {\n'
    + '    if (err.name === "NotAllowedError") { setStatus("Cancelled. Try again when ready.", "error"); }\n'
    + '    else { setStatus("Error: " + err.message, "error"); }\n'
    + '    btn.disabled = false;\n'
    + '    document.getElementById("createLink").style.display = "";\n'
    + '  }\n'
    + '}\n'
    + '</script></body></html>';

  htmlResponse(res, 200, html);
}

// POST /demo/api/agent-auth/approve ... called by the approve page after successful passkey auth
function handleAgentAuthApprove(req, res) {
  readBody(req).then(function(body) {
    const { challengeId, agentId, apiKey } = body || {};
    const entry = agentAuthChallenges[challengeId];
    if (!entry || Date.now() > entry.expires) {
      json(res, 404, { error: "Challenge not found or expired" });
      return;
    }
    if (entry.status === "approved") {
      json(res, 400, { error: "Already approved" });
      return;
    }
    entry.status = "approved";
    entry.token = apiKey;
    entry.agentId = agentId;
    console.log("Agent QR auth: approved challenge " + challengeId.slice(0, 8) + "... for agent '" + agentId + "'");
    json(res, 200, { ok: true });
  }).catch(function() {
    json(res, 400, { error: "Invalid request" });
  });
}

// ---------- QR Login (Chrome fallback) ----------

// `next` whitelist for the QR login flow. Three shapes are allowed; each
// land the user on a known phone-side surface after successful sign-in.
// Anything else is silently dropped. `next` is NOT a general redirect
// primitive.
//
// 1. PAIR_NEXT_REGEX: /pair/<CODE> using the daemon's real alphabet
//    (CODEX_PAIR_ALPHABET, length 6, L IS included; I/O/0/1 excluded).
//    See plan ai/product/plans-prds/codex-remote-control/
//    2026-04-30--cc-mini--pair-via-login-qr-flow.md constraints C1,
//    C8, and round-5. Per C8 the URL fallback for this shape is
//    mobile-only (desktop must not become the pairing authority).
//
// 2. REMOTE_CONTROL_NEXT_REGEX: /codex-remote-control/<UUID> for the
//    Kaleidoscope phone-side remote-control thread surface. Standard
//    ?next semantics; allowed on both desktop and mobile (this is
//    navigation continuation, not authority transfer).
//
// 3. DEMO_NEXT_REGEX: /demo for the homepage CTA. Standard post-login
//    continuation; allowed on both desktop and mobile.
const PAIR_NEXT_REGEX = /^\/pair\/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/;
const REMOTE_CONTROL_NEXT_REGEX = /^\/codex-remote-control\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const DEMO_NEXT_REGEX = /^\/demo$/;

function sanitizeCrcPairNext(raw) {
  if (typeof raw !== "string") return null;
  // Single decode; reject if a second decode would still differ.
  let decoded;
  try { decoded = decodeURIComponent(raw); } catch { return null; }
  // Catch double-encoded payloads.
  if (decoded !== raw && /%/.test(decoded)) return null;
  if (!PAIR_NEXT_REGEX.test(decoded) && !REMOTE_CONTROL_NEXT_REGEX.test(decoded) && !DEMO_NEXT_REGEX.test(decoded)) return null;
  return decoded;
}

// POST /api/qr-login ... create a QR login session
async function handleQrLoginStart(req, res) {
  cleanupExpiredChallenges();
  const body = await readBody(req).catch(() => ({}));
  const handle = ((body && body.handle) || "").trim().toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 30);
  const mode = ((body && body.mode) || "register") === "signin" ? "signin" : "register";
  // Validate `next` strictly. Invalid next is silently dropped, not
  // 400'd, so legacy callers still work.
  //
  // Only /pair/<CODE> next triggers pair-mode (C6 strip on desktop
  // status, C8 desktop-no-redirect, the "phone is the actor" model).
  // /codex-remote-control/<UUID> and /demo are normal post-login
  // continuations: desktop status returns the full login response
  // (apiKey, handle, next) so the desktop poll can authenticate and
  // redirect on its own. The phone also gets next via approve, so both
  // ends can act.
  const next = sanitizeCrcPairNext(body && body.next);
  const purpose = (next && PAIR_NEXT_REGEX.test(next)) ? "pair" : null;
  const sessionId = randomUUID();
  const loginUrl = ISSUER_URL + "/login?s=" + sessionId + "&m=" + mode + (handle ? "&h=" + encodeURIComponent(handle) : "");
  const qrBuffer = await QRCode.toBuffer(loginUrl, { type: "png", width: 400, margin: 2 });
  qrLoginSessions[sessionId] = {
    qrBuffer,
    status: "pending",
    agentId: null,
    apiKey: null,
    handle: handle || null,
    expires: Date.now() + QR_LOGIN_EXPIRY_MS,
    purpose,           // "pair" | null
    next: next || null, // sanitized `/pair/<CODE>`, `/codex-remote-control/<UUID>`, `/demo`, or null
  };
  console.log("QR login: created session " + sessionId.slice(0, 8) + "..." + (purpose === "pair" ? " (pair-mode)" : ""));
  json(res, 200, { sessionId, qrUrl: "/api/qr-login/qr?s=" + sessionId });
}

// GET /api/qr-login/qr?s=XXX ... serve QR code PNG
function handleQrLoginQR(req, res) {
  const url = parseUrl(req.url);
  const s = url.searchParams.get("s");
  const entry = qrLoginSessions[s];
  if (!entry || Date.now() > entry.expires) {
    json(res, 404, { error: "Session not found or expired" });
    return;
  }
  res.writeHead(200, { "Content-Type": "image/png", "Content-Length": entry.qrBuffer.length });
  res.end(entry.qrBuffer);
}

// GET /api/qr-login/status?s=XXX ... poll for completion
//
// Response shape depends on `purpose`:
//   - Pair-mode (purpose === "pair"): {status, agentId} only on approved.
//     NEVER returns apiKey or next to the desktop. Phone receives next via
//     /api/qr-login/approve. Per plan C6 round 4.
//   - Legacy login mode: {status, agentId, apiKey} on approved (unchanged).
function handleQrLoginStatus(req, res) {
  const url = parseUrl(req.url);
  const s = url.searchParams.get("s");
  const entry = qrLoginSessions[s];
  if (!entry || Date.now() > entry.expires) {
    json(res, 404, { error: "Session not found or expired" });
    return;
  }
  if (entry.status === "approved") {
    if (entry.purpose === "pair") {
      // Pair-mode (purpose === "pair", next === /pair/<CODE>):
      // desktop gets ONLY a display label. No apiKey. No next. Plan
      // C6 round 4. Desktop never becomes the pairing authority.
      json(res, 200, { status: "approved", agentId: entry.agentId });
    } else {
      // Legacy login mode OR standard login continuation
      // (purpose === null). Desktop gets full identity to render the
      // welcome view OR redirect to next on its own poll.
      // credentialLabel matches the saved-passkey label (see
      // register-verify / auth-verify). next is included only if a
      // sanitized non-pair-mode next was set on the session
      // (/codex-remote-control/<UUID> or /demo); legacy login sessions
      // without next get next === null.
      json(res, 200, {
        status: "approved",
        agentId: entry.agentId,
        tenantId: entry.tenantId || null,
        apiKey: entry.apiKey,
        credentialLabel: entry.credentialLabel || null,
        next: entry.next || null,
      });
    }
    delete qrLoginSessions[s]; // one-time use
  } else {
    json(res, 200, { status: "pending" });
  }
}

// POST /api/qr-login/approve ... phone calls after passkey created
//
// In pair-mode, the response includes the sanitized `next` so the phone
// can location.replace(next) into /pair/<CODE>. Legacy login mode returns
// {ok: true} unchanged.
function handleQrLoginApprove(req, res) {
  readBody(req).then(function(body) {
    const { sessionId, agentId, apiKey, tenantId, credentialLabel } = body || {};
    const entry = qrLoginSessions[sessionId];
    if (!entry || Date.now() > entry.expires) {
      json(res, 404, { error: "Session not found or expired" });
      return;
    }
    if (entry.status === "approved") {
      json(res, 400, { error: "Already approved" });
      return;
    }
    entry.status = "approved";
    entry.agentId = agentId;
    entry.apiKey = apiKey;
    const verifiedIdentity = identityForApiKey(apiKey);
    entry.tenantId = verifiedIdentity?.tenantId || (isInternalTenantId(tenantId) ? tenantId : null);
    // Phone-side passes the label it received from register-verify /
    // auth-verify so the desktop can show the same string the user
    // just saved on their phone. Optional for back-compat.
    entry.credentialLabel = (typeof credentialLabel === "string" && credentialLabel.length <= 64) ? credentialLabel : null;
    console.log("QR login: approved session " + sessionId.slice(0, 8) + "... for '" + agentId + "'" + (entry.purpose === "pair" ? " (pair-mode)" : (entry.next ? " (next=" + entry.next + ")" : "")));
    // Phone receives next on approve regardless of purpose, so the
    // phone can redirect to /pair/<CODE> (pair-mode, phone is the
    // actor) or a standard continuation such as
    // /codex-remote-control/<UUID> or /demo. Desktop's separate
    // behavior (strip vs full response) is handled in
    // handleQrLoginStatus.
    if (entry.next) {
      json(res, 200, { ok: true, next: entry.next });
    } else {
      json(res, 200, { ok: true });
    }
  }).catch(function() {
    json(res, 400, { error: "Invalid request" });
  });
}

// ---------- Demo API handlers ----------

// ── Wallet tracking (per agent) ──
const IMAGE_COST_CENTS = 1; // $0.01, launch onboarding image-generation step
const INITIAL_BALANCE_CENTS = 1000; // $10.00

// JSON fallback for wallets
const WALLET_FILE = join(dirname(fileURLToPath(import.meta.url)), "wallets.json");
const DEMO_WALLET_RESET_MARKER_FILE = join(dirname(fileURLToPath(import.meta.url)), ".demo-wallet-reset-v0-4-87.json");
function loadWalletsFromFile() { try { return JSON.parse(readFileSync(WALLET_FILE, "utf8")); } catch { return {}; } }
function saveWalletsToFile(w) { try { writeFileSync(WALLET_FILE, JSON.stringify(w, null, 2) + "\n"); } catch {} }

function walletUserIdForAgent(agentId) {
  return typeof agentId === "string" && agentId.startsWith("acct:") ? agentId.slice("acct:".length) : agentId;
}

function resetAndNormalizeWalletFileEntries(wallets) {
  const normalizedWallets = {};
  let resetCount = 0;
  for (const agentId of Object.keys(wallets)) {
    normalizedWallets[walletUserIdForAgent(agentId)] = INITIAL_BALANCE_CENTS;
    resetCount += 1;
  }
  return { wallets: normalizedWallets, count: resetCount };
}

async function resetExistingDemoWalletsToStarterBalanceOnce() {
  if (existsSync(DEMO_WALLET_RESET_MARKER_FILE)) return;
  let prismaResetCount = 0;
  let jsonResetCount = 0;
  if (usePrisma) {
    try {
      const result = await prisma.wallet.updateMany({ data: { balance: INITIAL_BALANCE_CENTS } });
      prismaResetCount = result.count || 0;
    } catch (err) {
      console.error("Demo wallet reset migration error:", err.message);
    }
  }
  const normalizedWalletFile = resetAndNormalizeWalletFileEntries(loadWalletsFromFile());
  jsonResetCount = normalizedWalletFile.count;
  saveWalletsToFile(normalizedWalletFile.wallets);
  try {
    writeFileSync(DEMO_WALLET_RESET_MARKER_FILE, JSON.stringify({
      resetAt: new Date().toISOString(),
      balance: INITIAL_BALANCE_CENTS,
      prismaCount: prismaResetCount,
      jsonCount: jsonResetCount,
    }, null, 2) + "\n");
  } catch (err) {
    console.error("Demo wallet reset marker write error:", err.message);
  }
  console.log("Demo wallet reset migration: set " + (prismaResetCount + jsonResetCount) + " existing wallet balance(s) to " + formatCents(INITIAL_BALANCE_CENTS));
}

async function getBalance(agentId) {
  const walletUserId = walletUserIdForAgent(agentId);
  if (usePrisma) {
    try {
      const wallet = await prisma.wallet.findFirst({ where: { userId: walletUserId } });
      return wallet ? wallet.balance : INITIAL_BALANCE_CENTS;
    } catch {}
  }
  const w = loadWalletsFromFile();
  return w[walletUserId] !== undefined ? w[walletUserId] : INITIAL_BALANCE_CENTS;
}

async function deductBalance(agentId, cents) {
  const walletUserId = walletUserIdForAgent(agentId);
  if (usePrisma) {
    try {
      let wallet = await prisma.wallet.findFirst({ where: { userId: walletUserId } });
      if (!wallet) {
        wallet = await prisma.wallet.create({
          data: { userId: walletUserId, balance: INITIAL_BALANCE_CENTS },
        });
      }
      const newBalance = Math.max(0, wallet.balance - cents);
      await prisma.wallet.update({ where: { id: wallet.id }, data: { balance: newBalance } });
      return newBalance;
    } catch (err) {
      console.error("Prisma deductBalance error:", err.message);
    }
  }
  // JSON fallback
  const w = loadWalletsFromFile();
  if (w[walletUserId] === undefined) w[walletUserId] = INITIAL_BALANCE_CENTS;
  w[walletUserId] = Math.max(0, w[walletUserId] - cents);
  saveWalletsToFile(w);
  return w[walletUserId];
}
function formatCents(c) { return "$" + (c / 100).toFixed(2); }

await resetExistingDemoWalletsToStarterBalanceOnce();

const LIVE_WALL_FILE = process.env.KALEIDOSCOPE_LIVE_WALL_FILE || join(__dirname, "kaleidoscope-live-wall.json");
const LIVE_WALL_MEDIA_ROUTE = "/media/kaleidoscope/generated/";
const LIVE_WALL_DEFAULT_MEDIA_DIR = DEV_MODE
  ? join(__dirname, "media", "kaleidoscope", "generated")
  : "/var/www/wip.computer/public_html/media/kaleidoscope/generated";
const LIVE_WALL_MEDIA_DIR = process.env.KALEIDOSCOPE_LIVE_WALL_MEDIA_DIR || LIVE_WALL_DEFAULT_MEDIA_DIR;
const LIVE_WALL_MAX_IMAGE_BYTES = Math.max(1, parseInt(process.env.KALEIDOSCOPE_LIVE_WALL_MAX_IMAGE_BYTES || String(10 * 1024 * 1024), 10));
const LIVE_WALL_FETCH_TIMEOUT_MS = Math.max(1_000, parseInt(process.env.KALEIDOSCOPE_LIVE_WALL_FETCH_TIMEOUT_MS || "15000", 10));
const LIVE_WALL_LIMIT = 240;
const KALEIDOSCOPE_PUBLIC_STATS_BASELINE = Object.freeze({
  timezone: "America/Los_Angeles",
  date: "2026-05-21",
  startsAt: "2026-05-21T07:00:00.000Z",
  counts: Object.freeze({
    keysCreated: 3,
    genericKaleidoscopes: 11,
    imageKaleidoscopes: 3,
  }),
});
const LIVE_WALL_SEED_SOURCES = [
  {
    sourceUrl: "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-bd814982-276f-438d-bc3c-2ca817982aae.jpeg",
    createdAt: "2026-05-20T00:00:00.000Z",
    kind: "generic",
  },
  {
    sourceUrl: "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-226e18a9-7721-4f6c-9ef2-3c26c0ff1293.jpeg",
    createdAt: "2026-05-20T00:00:01.000Z",
    kind: "generic",
  },
  {
    sourceUrl: "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-b1b398b5-4982-4ed8-b583-170a4ae4e811.jpeg",
    createdAt: "2026-05-20T00:00:02.000Z",
    kind: "generic",
  },
  {
    sourceUrl: "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-5505496e-c436-4047-ab81-630a22ec75ea.jpeg",
    createdAt: "2026-05-20T00:00:03.000Z",
    kind: "generic",
  },
];
let liveWallSeedBackfillAttempted = false;

function ensureLiveWallRuntimeStorage() {
  try {
    mkdirSync(dirname(LIVE_WALL_FILE), { recursive: true });
    mkdirSync(LIVE_WALL_MEDIA_DIR, { recursive: true });
    accessSync(dirname(LIVE_WALL_FILE), fsConstants.W_OK);
    accessSync(LIVE_WALL_MEDIA_DIR, fsConstants.W_OK);
  } catch (err) {
    console.error("FATAL: Kaleidoscope live wall storage is not writable:", err.message);
    process.exit(1);
  }
}

ensureLiveWallRuntimeStorage();

const LIVE_WALL_GENERIC_PROMPT = "Create an abstract kaleidoscope image with mirrored radial symmetry, analog film grain, warm color bleed, soft exposure, organic imperfections, and no text.";
const LIVE_WALL_PHOTO_PROMPT = "Create an abstract kaleidoscope image from the colors, light, and shapes in the user's photo. Use mirrored radial symmetry, analog film grain, warm color bleed, soft exposure, organic imperfections, and no text.";
const LIVE_WALL_IMAGE_PROMPT_PREFIX = "Create an abstract kaleidoscope image from these visual details in the user's photo: ";
const LIVE_WALL_IMAGE_PROMPT_SUFFIX = ". Use mirrored radial symmetry, analog film grain, warm color bleed, soft exposure, organic imperfections, and no text.";

function classifyLiveWallPrompt(prompt) {
  if (prompt === LIVE_WALL_GENERIC_PROMPT) return "generic";
  if (prompt === LIVE_WALL_PHOTO_PROMPT) return "image";
  if (typeof prompt === "string"
    && prompt.startsWith(LIVE_WALL_IMAGE_PROMPT_PREFIX)
    && prompt.endsWith(LIVE_WALL_IMAGE_PROMPT_SUFFIX)) {
    return "image";
  }
  return null;
}

function parseTimestampMs(value) {
  if (typeof value !== "string" || !value.trim()) return null;
  const ms = Date.parse(value);
  return Number.isFinite(ms) ? ms : null;
}

function createdAtSinceBaseline(item) {
  const baselineMs = Date.parse(KALEIDOSCOPE_PUBLIC_STATS_BASELINE.startsAt);
  const createdAtMs = parseTimestampMs(item?.createdAt);
  return createdAtMs !== null && createdAtMs >= baselineMs;
}

function isWipTestHandle(handle) {
  return typeof handle === "string" && handle.trim().toLowerCase().startsWith("wiptest-");
}

function publicKeyCreatedSinceBaseline(entry) {
  return createdAtSinceBaseline(entry) && !isWipTestHandle(entry?.handle);
}

function latestCreatedAt(items) {
  let latestMs = null;
  let latest = null;
  for (const item of Array.isArray(items) ? items : []) {
    const ms = parseTimestampMs(item?.createdAt);
    if (ms === null) continue;
    if (latestMs === null || ms > latestMs) {
      latestMs = ms;
      latest = new Date(ms).toISOString();
    }
  }
  return latest;
}

function countCreatedInLast24Hours(items, now = new Date()) {
  const nowMs = now.getTime();
  const windowStartMs = nowMs - (24 * 60 * 60 * 1000);
  return (Array.isArray(items) ? items : []).filter(item => {
    const ms = parseTimestampMs(item?.createdAt);
    return ms !== null && ms >= windowStartMs && ms <= nowMs;
  }).length;
}

function deriveKaleidoscopePublicStats({ images, passkeyEntries, now = new Date() }) {
  const safeImages = Array.isArray(images) ? images : [];
  const safePasskeys = Array.isArray(passkeyEntries) ? passkeyEntries : [];
  const postBaselineGeneric = safeImages
    .filter(item => item && isPublicWallImageUrl(item.url) && item.kind !== "image" && createdAtSinceBaseline(item))
    .length;
  const postBaselineImage = safeImages
    .filter(item => item && isPublicWallImageUrl(item.url) && item.kind === "image" && createdAtSinceBaseline(item))
    .length;
  const publicPasskeys = safePasskeys.filter(item => !isWipTestHandle(item?.handle));
  const postBaselineKeys = publicPasskeys.filter(createdAtSinceBaseline).length;
  const newestCreatedAt = latestCreatedAt([...safeImages, ...publicPasskeys]);

  return {
    genericKaleidoscopes: KALEIDOSCOPE_PUBLIC_STATS_BASELINE.counts.genericKaleidoscopes + postBaselineGeneric,
    imageKaleidoscopes: KALEIDOSCOPE_PUBLIC_STATS_BASELINE.counts.imageKaleidoscopes + postBaselineImage,
    keysCreated: KALEIDOSCOPE_PUBLIC_STATS_BASELINE.counts.keysCreated + postBaselineKeys,
    publicWallImages: safeImages.filter(item => item && isPublicWallImageUrl(item.url)).length,
    baseline: KALEIDOSCOPE_PUBLIC_STATS_BASELINE,
    newSinceBaseline: {
      genericKaleidoscopes: postBaselineGeneric,
      imageKaleidoscopes: postBaselineImage,
      keysCreated: postBaselineKeys,
      total: postBaselineGeneric + postBaselineImage + postBaselineKeys,
    },
    last24Hours: {
      wallImages: countCreatedInLast24Hours(safeImages, now),
      keysCreated: countCreatedInLast24Hours(publicPasskeys, now),
    },
    lastCreated: newestCreatedAt,
  };
}

function loadLiveWallState() {
  try {
    const parsed = JSON.parse(readFileSync(LIVE_WALL_FILE, "utf8"));
    const saved = Array.isArray(parsed?.images) ? parsed.images : [];
    return {
      images: saved,
    };
  } catch {
    return {
      images: [],
    };
  }
}

function saveLiveWallState(state) {
  try {
    mkdirSync(dirname(LIVE_WALL_FILE), { recursive: true });
    writeFileSync(LIVE_WALL_FILE, JSON.stringify({
      images: Array.isArray(state?.images) ? state.images : [],
    }, null, 2) + "\n");
  } catch (err) {
    console.error("Kaleidoscope live wall save error:", err.message);
  }
}

function liveWallSourceHash(value) {
  return createHash("sha256").update(value).digest("hex");
}

function publicLiveWallMediaUrl(filename) {
  return ISSUER_URL + LIVE_WALL_MEDIA_ROUTE + filename;
}

function liveWallMediaFilenameFromUrl(value) {
  try {
    const url = new URL(value, ISSUER_URL);
    if (url.origin !== ISSUER_URL || !url.pathname.startsWith(LIVE_WALL_MEDIA_ROUTE)) return null;
    const filename = url.pathname.slice(LIVE_WALL_MEDIA_ROUTE.length);
    return /^[a-f0-9]{64}\.(jpg|png|webp)$/.test(filename) ? filename : null;
  } catch {
    return null;
  }
}

function liveWallMediaFileExists(value) {
  const filename = liveWallMediaFilenameFromUrl(value);
  return Boolean(filename && existsSync(join(LIVE_WALL_MEDIA_DIR, filename)));
}

function liveWallContentTypeForFilename(filename) {
  if (filename.endsWith(".jpg")) return "image/jpeg";
  if (filename.endsWith(".png")) return "image/png";
  if (filename.endsWith(".webp")) return "image/webp";
  return null;
}

function serveKaleidoscopeGeneratedMedia(path, res) {
  const filename = path.slice(LIVE_WALL_MEDIA_ROUTE.length);
  if (!/^[a-f0-9]{64}\.(jpg|png|webp)$/.test(filename)) {
    json(res, 404, { error: "Not found" });
    return;
  }
  try {
    const content = readFileSync(join(LIVE_WALL_MEDIA_DIR, filename));
    const contentType = liveWallContentTypeForFilename(filename) || "application/octet-stream";
    res.writeHead(200, {
      "Content-Type": contentType,
      "Content-Length": content.length,
      "Cache-Control": "public, max-age=31536000, immutable",
    });
    res.end(content);
  } catch {
    json(res, 404, { error: "Not found" });
  }
}

function isLiveWallMediaUrl(value) {
  if (typeof value !== "string" || value.length > 2048) return false;
  try {
    const url = new URL(value, ISSUER_URL);
    return url.origin === ISSUER_URL && url.pathname.startsWith(LIVE_WALL_MEDIA_ROUTE);
  } catch {
    return false;
  }
}

function isAllowedLiveWallSourceUrl(value) {
  if (typeof value !== "string" || value.length > 2048) return false;
  if (value.startsWith("data:")) return false;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && url.hostname === "imgen.x.ai" && url.pathname.startsWith("/xai-imgen/");
  } catch {
    return false;
  }
}

function isPublicWallImageUrl(value) {
  return isLiveWallMediaUrl(value) || isAllowedLiveWallSourceUrl(value);
}

function normalizeLiveWallContentType(value) {
  const type = String(value || "").split(";")[0].trim().toLowerCase();
  if (type === "image/jpg") return "image/jpeg";
  return type;
}

function liveWallExtensionForContentType(contentType) {
  if (contentType === "image/jpeg") return "jpg";
  if (contentType === "image/png") return "png";
  if (contentType === "image/webp") return "webp";
  return null;
}

function liveWallBufferMatchesContentType(buffer, contentType) {
  if (!Buffer.isBuffer(buffer) || buffer.length < 12) return false;
  if (contentType === "image/jpeg") {
    return buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff;
  }
  if (contentType === "image/png") {
    return buffer[0] === 0x89 && buffer[1] === 0x50 && buffer[2] === 0x4e && buffer[3] === 0x47
      && buffer[4] === 0x0d && buffer[5] === 0x0a && buffer[6] === 0x1a && buffer[7] === 0x0a;
  }
  if (contentType === "image/webp") {
    return buffer.subarray(0, 4).toString("ascii") === "RIFF"
      && buffer.subarray(8, 12).toString("ascii") === "WEBP";
  }
  return false;
}

async function readLiveWallImageResponseBody(response) {
  if (!response.body || typeof response.body.getReader !== "function") {
    throw new Error("source image response body is not readable");
  }
  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (!value) continue;
      total += value.byteLength;
      if (total > LIVE_WALL_MAX_IMAGE_BYTES) {
        throw new Error("source image exceeds max byte size");
      }
      chunks.push(Buffer.from(value));
    }
  } finally {
    try { reader.releaseLock(); } catch {}
  }

  if (total < 1) throw new Error("source image byte size is invalid");
  return Buffer.concat(chunks, total);
}

async function archiveKaleidoscopeGeneratedImage(sourceUrl) {
  if (!isAllowedLiveWallSourceUrl(sourceUrl)) throw new Error("source image URL is not an allowed HTTPS image source");
  const source = new URL(sourceUrl);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), LIVE_WALL_FETCH_TIMEOUT_MS);
  if (typeof timeout.unref === "function") timeout.unref();
  let imageRes;
  try {
    imageRes = await fetch(source.href, { redirect: "follow", signal: controller.signal });
    if (!imageRes.ok) throw new Error("source image fetch failed with HTTP " + imageRes.status);
    const finalUrl = new URL(imageRes.url || source.href);
    if (!isAllowedLiveWallSourceUrl(finalUrl.href)) throw new Error("source image redirected away from allowed image source");

    const contentType = normalizeLiveWallContentType(imageRes.headers.get("content-type"));
    const ext = liveWallExtensionForContentType(contentType);
    if (!ext) throw new Error("source image content type is not an allowed raster image");

    const contentLength = Number.parseInt(imageRes.headers.get("content-length") || "0", 10);
    if (Number.isFinite(contentLength) && contentLength > LIVE_WALL_MAX_IMAGE_BYTES) {
      throw new Error("source image exceeds max byte size");
    }

    const buffer = await readLiveWallImageResponseBody(imageRes);
    if (!liveWallBufferMatchesContentType(buffer, contentType)) {
      throw new Error("source image bytes do not match content type");
    }

    const contentHash = createHash("sha256").update(buffer).digest("hex");
    const sourceUrlHash = liveWallSourceHash(source.href);
    const filename = contentHash + "." + ext;
    mkdirSync(LIVE_WALL_MEDIA_DIR, { recursive: true });
    const filePath = join(LIVE_WALL_MEDIA_DIR, filename);
    if (!existsSync(filePath)) writeFileSync(filePath, buffer);

    return {
      url: publicLiveWallMediaUrl(filename),
      sourceProvider: "xai",
      sourceUrlHash,
      contentHash,
      contentType,
      byteLength: buffer.length,
      archivedAt: new Date().toISOString(),
    };
  } catch (err) {
    if (err?.name === "AbortError") throw new Error("source image fetch timed out");
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

function liveWallEntryFromArchived({ archived, createdAt, kind, id }) {
  return {
    id: id || randomUUID(),
    url: archived.url,
    createdAt: createdAt || new Date().toISOString(),
    kind: kind === "image" ? "image" : "generic",
    sourceProvider: archived.sourceProvider,
    sourceUrlHash: archived.sourceUrlHash,
    contentHash: archived.contentHash,
    contentType: archived.contentType,
    byteLength: archived.byteLength,
    archivedAt: archived.archivedAt,
  };
}

function liveWallEntrySourceHash(item) {
  if (!item || typeof item !== "object") return null;
  if (typeof item.sourceUrlHash === "string" && item.sourceUrlHash) return item.sourceUrlHash;
  if (isAllowedLiveWallSourceUrl(item.url)) return liveWallSourceHash(item.url);
  return null;
}

async function ensureLiveWallSeedImages() {
  if (liveWallSeedBackfillAttempted) return;
  liveWallSeedBackfillAttempted = true;

  const state = loadLiveWallState();
  const images = [];
  const existingSourceHashes = new Set();
  const existingUrls = new Set(images.map(item => item.url).filter(Boolean));
  let changed = false;

  for (const item of state.images) {
    if (!item || typeof item.url !== "string") {
      changed = true;
      continue;
    }
    if (isLiveWallMediaUrl(item.url) && liveWallMediaFileExists(item.url)) {
      images.push(item);
      if (item.sourceUrlHash) existingSourceHashes.add(item.sourceUrlHash);
      existingUrls.add(item.url);
      continue;
    }
    if (isAllowedLiveWallSourceUrl(item.url)) {
      try {
        const archived = await archiveKaleidoscopeGeneratedImage(item.url);
        if (!existingUrls.has(archived.url)) {
          images.push(liveWallEntryFromArchived({
            archived,
            createdAt: item.createdAt,
            kind: item.kind,
            id: item.id,
          }));
          existingUrls.add(archived.url);
        }
        existingSourceHashes.add(archived.sourceUrlHash);
        changed = true;
      } catch (err) {
        images.push(item);
        console.error("Kaleidoscope live wall registry image migration failed:", JSON.stringify({
          sourceUrlHash: liveWallSourceHash(item.url),
          message: err.message,
        }));
      }
      continue;
    }
    changed = true;
  }

  for (const seed of LIVE_WALL_SEED_SOURCES) {
    const sourceUrlHash = liveWallSourceHash(seed.sourceUrl);
    if (existingSourceHashes.has(sourceUrlHash)) continue;
    try {
      const archived = await archiveKaleidoscopeGeneratedImage(seed.sourceUrl);
      if (existingUrls.has(archived.url)) continue;
      images.push(liveWallEntryFromArchived({
        archived,
        createdAt: seed.createdAt,
        kind: seed.kind,
      }));
      existingSourceHashes.add(sourceUrlHash);
      existingUrls.add(archived.url);
      changed = true;
    } catch (err) {
      console.error("Kaleidoscope live wall seed archive failed:", JSON.stringify({
        sourceUrlHash,
        message: err.message,
      }));
    }
  }

  if (changed) saveLiveWallState({ images: images.slice(0, LIVE_WALL_LIMIT) });
}

async function registerKaleidoscopeLiveWallEvent({ kind, imageUrl }) {
  if (kind !== "generic" && kind !== "image") return;
  let archived;
  try {
    archived = await archiveKaleidoscopeGeneratedImage(imageUrl);
  } catch (err) {
    console.error("Kaleidoscope live wall archive failed:", JSON.stringify({
      kind,
      message: err.message,
    }));
    return;
  }

  const state = loadLiveWallState();
  const mediaImages = state.images
    .filter(item => item && isLiveWallMediaUrl(item.url) && liveWallMediaFileExists(item.url))
    .filter(item => item.url !== archived.url && item.sourceUrlHash !== archived.sourceUrlHash);
  const rawImages = state.images
    .filter(item => item && isAllowedLiveWallSourceUrl(item.url))
    .filter(item => liveWallEntrySourceHash(item) !== archived.sourceUrlHash);
  const images = [
    liveWallEntryFromArchived({
      archived,
      createdAt: new Date().toISOString(),
      kind,
    }),
    ...mediaImages,
    ...rawImages,
  ];
  saveLiveWallState({ images: images.slice(0, LIVE_WALL_LIMIT) });
  return archived.url;
}

async function handleKaleidoscopeLiveWall(req, res) {
  await ensureLiveWallSeedImages();
  const state = loadLiveWallState();
  const images = state.images
    .filter(item => item && isLiveWallMediaUrl(item.url) && liveWallMediaFileExists(item.url))
    .slice(0, LIVE_WALL_LIMIT);
  const stats = deriveKaleidoscopePublicStats({ images, passkeyEntries: passkeys });
  res.setHeader("Cache-Control", "no-store");
  json(res, 200, {
    count: images.length,
    stats,
    images: images.map(item => ({ url: item.url, createdAt: item.createdAt || null })),
  });
}

// POST /demo/api/analyze-photo
// Sends a base64 image to OpenAI GPT-4o vision to extract colors/mood.
async function handleDemoAnalyzePhoto(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }

  try {
    const body = await readBody(req);
    const image = body?.image;
    if (!image || typeof image !== "string" || !image.startsWith("data:image/")) {
      json(res, 400, { error: "Missing or invalid base64 image" });
      return;
    }

    const OPENAI_KEY = process.env.OPENAI_API_KEY || "";
    if (!OPENAI_KEY) {
      json(res, 503, { error: "Vision analysis not configured" });
      return;
    }

    const oaiRes = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_KEY,
      },
      body: JSON.stringify({
        model: "gpt-4o",
        max_tokens: 80,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: "List only the 5 most dominant COLOR NAMES in this image, separated by commas. Example: warm amber, deep brown, soft cream, golden yellow, muted gray. Do NOT describe objects, people, faces, or shapes. ONLY color names. Nothing else.",
              },
              {
                type: "image_url",
                image_url: { url: image },
              },
            ],
          },
        ],
      }),
    });

    const oaiData = await oaiRes.json();
    const description = oaiData.choices?.[0]?.message?.content?.trim();

    if (!description) {
      console.error("Vision analysis: no description returned", oaiData.error || "");
      json(res, 502, { error: "Vision analysis returned no description" });
      return;
    }

    console.log("Demo: vision analysis for agent '" + identity.agentId + "': " + description);
    json(res, 200, { description });
  } catch (err) {
    console.error("Demo analyze-photo error:", err.message);
    json(res, 500, { error: "Internal error" });
  }
}

// POST /demo/api/imagine
async function handleDemoImagine(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }

  try {
    const body = await readBody(req);
    const prompt = body?.prompt || "kaleidoscope";
    const liveWallKind = classifyLiveWallPrompt(prompt);

    const XAI_KEY = process.env.XAI_API_KEY || "";
    if (!XAI_KEY) {
      json(res, 503, { error: "Image generation not configured" });
      return;
    }

    const imageModel = process.env.XAI_IMAGE_MODEL || "grok-imagine-image-quality";
    const imageRequestBody = {
      model: imageModel,
      prompt: prompt,
    };
    const grokRes = await fetch("https://api.x.ai/v1/images/generations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + XAI_KEY,
      },
      body: JSON.stringify(imageRequestBody),
    });

    const grokText = await grokRes.text();
    let grokData;
    try {
      grokData = grokText ? JSON.parse(grokText) : {};
    } catch {
      grokData = { error: { message: "Non-JSON image API response" } };
    }

    if (!grokRes.ok || grokData.error) {
      const message = grokData.error?.message || grokRes.statusText || "Image generation failed";
      console.error("Demo imagine upstream error:", JSON.stringify({
        status: grokRes.status,
        model: imageModel,
        message,
        type: grokData.error?.type || null,
        code: grokData.error?.code || null,
        param: grokData.error?.param || null,
      }));
      json(res, 502, { error: message });
      return;
    }

    const imageUrl = grokData.data?.[0]?.url;
    if (!imageUrl) {
      console.error("Demo imagine upstream returned no image URL:", JSON.stringify({
        status: grokRes.status,
        model: imageModel,
        responseKeys: Object.keys(grokData || {}),
      }));
      json(res, 502, { error: "No image returned" });
      return;
    }

    const newBalance = await deductBalance(identity.agentId, IMAGE_COST_CENTS);
    const archivedImageUrl = await registerKaleidoscopeLiveWallEvent({ kind: liveWallKind, imageUrl });
    console.log("Demo: generated image for agent '" + identity.agentId + "' using " + imageModel + " (balance: " + formatCents(newBalance) + ")");
    json(res, 200, { url: archivedImageUrl || imageUrl, prompt: prompt, cost: formatCents(IMAGE_COST_CENTS), balance: formatCents(newBalance) });
  } catch (err) {
    console.error("Demo imagine error:", err.message);
    json(res, 500, { error: "Internal error" });
  }
}

// ---------- MCP handlers ----------

async function handlePost(req, res, identity) {
  const sid = req.headers["mcp-session-id"];
  let body;
  try { body = await readBody(req); } catch { rpcError(res, 400, -32700, "Parse error"); return; }

  if (sid && sessions[sid]) {
    touchSession(sid);
    await sessions[sid].transport.handleRequest(req, res, body);
    return;
  }

  if (!sid && isInitializeRequest(body)) {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (id) => {
        sessions[id] = { transport, server: mcpServer, identity, lastActivity: Date.now() };
        console.log("Session created: " + id + " (agent: " + identity.agentId + ")");
      },
    });
    transport.onclose = () => {
      const id = transport.sessionId;
      if (id && sessions[id]) { console.log("Session closed: " + id); delete sessions[id]; }
    };
    const mcpServer = new McpServer({ name: SERVER_NAME, version: SERVER_VERSION });
    registerTools(mcpServer, () => identity);
    await mcpServer.connect(transport);
    await transport.handleRequest(req, res, body);
    return;
  }

  rpcError(res, 400, -32000, "Bad request: missing or invalid session");
}

async function handleGetOrDelete(req, res) {
  const sid = req.headers["mcp-session-id"];
  if (!sid || !sessions[sid]) { rpcError(res, 400, -32000, "Invalid or missing session ID"); return; }
  touchSession(sid);
  await sessions[sid].transport.handleRequest(req, res);
}

// ---------- HTTP server ----------

// ── Device Pairing (Bridge Phase A) ─────────────────────────────────
//
// Flow:
//   1. CLI runs `ldm pair`, calls POST /api/pair/request with a code
//   2. Server stores the pending pairing (code -> device info)
//   3. User goes to kaleidoscope.wip.computer/pair, signs in with passkey
//   4. User enters the code, calls POST /api/pair/approve
//   5. Server matches code, generates a device token, marks as approved
//   6. CLI polls GET /api/pair/status?code=X, gets the token
//   7. CLI stores token at ~/.ldm/auth/kaleidoscope.json
//
// Codes expire after 120 seconds. Approved tokens persist on the server
// in a device registry (paired-devices.json).

const PAIR_CODE_EXPIRY_MS = 120_000;
const PAIRED_DEVICES_FILE = join(__dirname, "paired-devices.json");

// In-memory pending pairings: code -> { deviceName, agentId, createdAt, approved, token, userId, userName }
const pendingPairings = new Map();

// Load persisted device registry
function loadPairedDevices() {
  try { return JSON.parse(readFileSync(PAIRED_DEVICES_FILE, "utf8")); } catch { return []; }
}
function savePairedDevices(devices) {
  writeFileSync(PAIRED_DEVICES_FILE, JSON.stringify(devices, null, 2) + "\n");
}

// Word lists for human-readable codes
const PAIR_WORDS = [
  "BLUE", "RED", "GREEN", "GOLD", "GRAY", "PINK", "DARK", "WARM", "COLD", "WILD",
  "FISH", "BIRD", "WOLF", "BEAR", "DEER", "HAWK", "FROG", "LYNX", "DOVE", "CROW",
  "OAK", "ELM", "ASH", "FIG", "IVY", "YEW", "BAY", "FIR", "RYE", "RUM",
];

function generatePairCode() {
  const w1 = PAIR_WORDS[Math.floor(Math.random() * 10)];       // color
  const w2 = PAIR_WORDS[10 + Math.floor(Math.random() * 10)];  // animal
  const num = String(Math.floor(1000 + Math.random() * 9000)); // 4 digits
  return `${w1}-${w2}-${num}`;
}

// Clean expired pairings every 30s
setInterval(() => {
  const now = Date.now();
  for (const [code, p] of pendingPairings) {
    if (now - p.createdAt > PAIR_CODE_EXPIRY_MS && !p.approved) {
      pendingPairings.delete(code);
    }
  }
}, 30_000);

async function handlePairRequest(req, res) {
  const body = await readBody(req);
  const { code, deviceName, agentId } = body || {};

  if (!code || typeof code !== "string") {
    json(res, 400, { error: "Missing code" });
    return;
  }

  // Store as pending
  pendingPairings.set(code.toUpperCase(), {
    deviceName: deviceName || "unknown",
    agentId: agentId || "cc-mini",
    createdAt: Date.now(),
    approved: false,
    token: null,
    userId: null,
    userName: null,
  });

  json(res, 200, { ok: true, code: code.toUpperCase(), expiresIn: PAIR_CODE_EXPIRY_MS / 1000 });
}

async function handlePairApprove(req, res) {
  const body = await readBody(req);
  const { code, userId, userName } = body || {};

  if (!code || typeof code !== "string") {
    json(res, 400, { error: "Missing code" });
    return;
  }

  const upper = code.toUpperCase();
  const pending = pendingPairings.get(upper);

  if (!pending) {
    json(res, 404, { error: "Code not found or expired. Run ldm pair again." });
    return;
  }

  if (Date.now() - pending.createdAt > PAIR_CODE_EXPIRY_MS) {
    pendingPairings.delete(upper);
    json(res, 410, { error: "Code expired. Run ldm pair again." });
    return;
  }

  // Generate device token
  const token = "dk-" + randomBytes(32).toString("hex");

  // Mark as approved
  pending.approved = true;
  pending.token = token;
  pending.userId = userId || "unknown";
  pending.userName = userName || "User";

  // Persist to device registry
  if (usePrisma) {
    try {
      await prisma.device.create({
        data: {
          token,
          deviceName: pending.deviceName,
          agentId: pending.agentId,
          userId: pending.userId,
          pairedAt: new Date(),
        },
      });
    } catch (err) {
      console.error("Prisma device save error:", err.message);
    }
  }
  // JSON backup
  try {
    const devices = loadPairedDevices();
    devices.push({
      token,
      deviceName: pending.deviceName,
      agentId: pending.agentId,
      userId: pending.userId,
      userName: pending.userName,
      pairedAt: new Date().toISOString(),
    });
    savePairedDevices(devices);
  } catch {}

  json(res, 200, {
    paired: true,
    deviceName: pending.deviceName,
    token, // returned to the approve page so it can confirm
  });
}

function handlePairStatus(req, res, url) {
  const code = (url.searchParams?.get("code") || url.query?.code || "").toUpperCase();

  if (!code) {
    json(res, 400, { error: "Missing code parameter" });
    return;
  }

  const pending = pendingPairings.get(code);

  if (!pending) {
    json(res, 404, { error: "Code not found or expired" });
    return;
  }

  if (!pending.approved) {
    json(res, 202, { status: "pending", message: "Waiting for approval..." });
    return;
  }

  // Approved. Return token. Clean up.
  pendingPairings.delete(code);
  json(res, 200, {
    status: "approved",
    token: pending.token,
    userId: pending.userId,
    userName: pending.userName,
  });
}

const httpServer = createServer(async (req, res) => {
  cors(res);
  if (req.method === "OPTIONS") { res.writeHead(204); res.end(); return; }

  const url = parseUrl(req.url);
  const path = url.pathname;

  // Health check
  if (req.method === "GET" && path === "/health") {
    json(res, 200, {
      ok: true, server: SERVER_NAME, version: SERVER_VERSION,
      database: usePrisma ? "postgres" : "json",
      sessions: Object.keys(sessions).length,
      passkeys: passkeys.length,
      uptime: process.uptime(),
    });
    return;
  }

  // --- Shared assets (Kaleidoscope template system) ---

  if (req.method === "GET" && path.startsWith(LIVE_WALL_MEDIA_ROUTE)) {
    serveKaleidoscopeGeneratedMedia(path, res);
    return;
  }

  if (req.method === "GET" && path.startsWith("/shared/")) {
    const filePath = join(__dirname, path);
    try {
      const content = readFileSync(filePath, "utf8");
      const ext = path.split(".").pop();
      const mimeTypes = { css: "text/css", js: "text/javascript", html: "text/html" };
      res.writeHead(200, { "Content-Type": (mimeTypes[ext] || "text/plain") + "; charset=utf-8" });
      res.end(content);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  // --- Static pages ---

  if (req.method === "GET" && path === "/signup") {
    handleSignupPage(req, res);
    return;
  }

  if (req.method === "GET" && (path === "/login" || path === "/login/")) {
    // Production /login owns its own file at app/kaleidoscope-login.html.
    //
    // Earlier this route served demo/login.html, which made production
    // auth depend on a file under demo/. That coupling is wrong: demo/
    // is the demo site's domain, not production. The canonical
    // Kaleidoscope login HTML now lives under app/, where production
    // owns it.
    //
    // Fallback chain (defense in depth):
    //   1. app/kaleidoscope-login.html  ... canonical production file.
    //   2. demo/login.html               ... legacy fallback during the
    //      transition; will be removed in a follow-up once the
    //      production file is verified live.
    //   3. handleLoginPage               ... server-rendered last resort.
    //
    // /login/app continues to serve the developed app/login.html flow
    // (see the next handler).
    try {
      const html = readFileSync(join(__dirname, "app", "kaleidoscope-login.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    } catch {
      try {
        const legacy = readFileSync(join(__dirname, "demo", "login.html"), "utf8");
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(legacy);
      } catch {
        handleLoginPage(req, res);
      }
    }
    return;
  }

  if (req.method === "GET" && (path === "/login/app" || path === "/login/app/")) {
    // Explicit non-primary route for the app/login.html flow (the
    // newer two-path "this device or QR-from-phone" copy). This
    // exists so the developed flow stays reachable without hijacking
    // /login. If app/login.html is not present, return 404 rather
    // than silently falling back to the canonical /login page.
    try {
      const loginHtml = readFileSync(join(__dirname, "app", "login.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(loginHtml);
    } catch {
      json(res, 404, { error: "Not found" });
    }
    return;
  }

  // --- Legal pages ---

  if (req.method === "GET" && path === "/legal/legal.css") {
    try {
      const css = readFileSync(join(__dirname, "legal", "legal.css"), "utf8");
      res.writeHead(200, { "Content-Type": "text/css; charset=utf-8" });
      res.end(css);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  if (req.method === "GET" && path === "/legal/legal-footer.js") {
    try {
      const js = readFileSync(join(__dirname, "legal", "legal-footer.js"), "utf8");
      res.writeHead(200, { "Content-Type": "text/javascript; charset=utf-8" });
      res.end(js);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  if (req.method === "GET" && (path === "/legal/privacy/" || path === "/legal/privacy")) {
    try {
      const html = readFileSync(join(__dirname, "legal", "privacy", "index.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  if (req.method === "GET" && (path === "/legal/privacy/en-ww/" || path === "/legal/privacy/en-ww")) {
    try {
      const html = readFileSync(join(__dirname, "legal", "privacy", "en-ww", "index.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  if (req.method === "GET" && path === "/legal/internet-services/terms/site.html") {
    try {
      const html = readFileSync(join(__dirname, "legal", "internet-services", "terms", "site.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  if (req.method === "GET" && (path === "/legal/internet-services/kaleidoscope/" || path === "/legal/internet-services/kaleidoscope")) {
    try {
      const html = readFileSync(join(__dirname, "legal", "internet-services", "kaleidoscope", "index.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
    } catch { json(res, 404, { error: "Not found" }); }
    return;
  }

  // --- WebAuthn API ---

  if (req.method === "POST" && path === "/webauthn/register-options") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleRegisterOptions(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/register-verify") {
    if (!applyRateLimit(req, res, "validate")) return;
    await handleRegisterVerify(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/auth-options") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleAuthOptions(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/auth-verify") {
    if (!applyRateLimit(req, res, "validate")) return;
    await handleAuthVerify(req, res);
    return;
  }

  // --- OAuth 2.0 / Well-Known ---

  if (req.method === "GET" && path === "/.well-known/oauth-authorization-server") {
    handleOAuthDiscovery(req, res);
    return;
  }

  if (req.method === "GET" && path === "/.well-known/oauth-protected-resource") {
    handleProtectedResource(req, res);
    return;
  }

  if (req.method === "POST" && path === "/oauth/register") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleOAuthRegister(req, res);
    return;
  }

  if (req.method === "GET" && path === "/oauth/authorize") {
    handleOAuthAuthorize(req, res);
    return;
  }

  if (req.method === "POST" && path === "/oauth/authorize/submit") {
    if (!applyRateLimit(req, res, "validate")) return;
    await handleOAuthAuthorizeSubmit(req, res);
    return;
  }

  if (req.method === "POST" && path === "/oauth/token") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleOAuthToken(req, res);
    return;
  }

  // --- Agent QR Auth ---

  if (req.method === "GET" && path === "/demo/api/agent-auth") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleAgentAuthStart(req, res);
    return;
  }

  if (req.method === "GET" && path === "/demo/api/agent-auth/qr") {
    if (!applyRateLimit(req, res, "status")) return;
    handleAgentAuthQR(req, res);
    return;
  }

  if (req.method === "GET" && path === "/demo/api/agent-auth/status") {
    if (!applyRateLimit(req, res, "status")) return;
    handleAgentAuthStatus(req, res);
    return;
  }

  if (req.method === "POST" && path === "/demo/api/agent-auth/approve") {
    if (!applyRateLimit(req, res, "validate")) return;
    handleAgentAuthApprove(req, res);
    return;
  }

  if (req.method === "GET" && path === "/approve") {
    handleApprovePage(req, res);
    return;
  }

  // --- Generic QR generator (encode any same-origin URL) ---

  if (req.method === "GET" && path === "/api/qr") {
    const target = url.searchParams.get("url");
    if (!target) { json(res, 400, { error: "missing url" }); return; }
    if (target.length > 2048) { json(res, 400, { error: "url too long" }); return; }
    QRCode.toBuffer(target, { type: "png", width: 320, margin: 2 })
      .then((buffer) => {
        res.writeHead(200, {
          "Content-Type": "image/png",
          "Content-Length": buffer.length,
          "Cache-Control": "no-store",
        });
        res.end(buffer);
      })
      .catch(() => json(res, 500, { error: "QR generation failed" }));
    return;
  }

  // --- QR Login (Chrome fallback) ---

  if (req.method === "POST" && path === "/api/qr-login") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleQrLoginStart(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/qr-login/qr") {
    if (!applyRateLimit(req, res, "status")) return;
    handleQrLoginQR(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/qr-login/status") {
    if (!applyRateLimit(req, res, "status")) return;
    handleQrLoginStatus(req, res);
    return;
  }

  if (req.method === "POST" && path === "/api/qr-login/approve") {
    if (!applyRateLimit(req, res, "validate")) return;
    handleQrLoginApprove(req, res);
    return;
  }

  // --- Demo API ---

  if (req.method === "GET" && path === "/demo/api/wallet") {
    const identity = authenticate(req);
    if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
    json(res, 200, { balance: formatCents(await getBalance(identity.agentId)), cost: formatCents(IMAGE_COST_CENTS) });
    return;
  }

  if (req.method === "GET" && path === "/demo/api/kaleidoscope-live-wall") {
    if (!applyRateLimit(req, res, "status")) return;
    await handleKaleidoscopeLiveWall(req, res);
    return;
  }

  if (req.method === "POST" && path === "/demo/api/analyze-photo") {
    await handleDemoAnalyzePhoto(req, res);
    return;
  }

  if (req.method === "POST" && path === "/demo/api/imagine") {
    await handleDemoImagine(req, res);
    return;
  }

  // --- MCP ---

  if (path === "/mcp") {
    const identity = authenticate(req);
    if (!identity && req.method === "POST") {
      json(res, 401, { error: "Unauthorized. Provide Bearer ck-... token." });
      return;
    }
    try {
      if (req.method === "POST") await handlePost(req, res, identity);
      else if (req.method === "GET" || req.method === "DELETE") await handleGetOrDelete(req, res);
      else rpcError(res, 405, -32000, "Method not allowed");
    } catch (err) {
      console.error("MCP error:", err);
      if (!res.headersSent) rpcError(res, 500, -32603, "Internal server error");
    }
    return;
  }

  // --- Device Pairing API (Bridge Phase A) ---

  if (req.method === "POST" && path === "/api/pair/request") {
    await handlePairRequest(req, res);
    return;
  }

  if (req.method === "POST" && path === "/api/pair/approve") {
    await handlePairApprove(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/pair/status") {
    handlePairStatus(req, res, url);
    return;
  }

  // --- Codex Relay (codex-daemon ↔ phone) ---

  if (req.method === "POST" && path === "/api/codex-relay/pair-init") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleCodexPairInit(req, res);
    return;
  }

  if (req.method === "GET" && path.startsWith("/api/codex-relay/pair-status/")) {
    if (!applyRateLimit(req, res, "status")) return;
    handleCodexPairStatus(req, res, path.slice("/api/codex-relay/pair-status/".length));
    return;
  }

  if (req.method === "POST" && path === "/api/codex-relay/pair-complete") {
    if (!applyRateLimit(req, res, "validate")) return;
    await handleCodexPairComplete(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/codex-relay/state") {
    if (!applyRateLimit(req, res, "status")) return;
    handleCodexRelayState(req, res);
    return;
  }

  if (req.method === "GET" && path.startsWith("/api/codex-relay/bootstrap/")) {
    if (!applyRateLimit(req, res, "mint")) return;
    const tid = decodeURIComponent(path.slice("/api/codex-relay/bootstrap/".length));
    handleCodexBootstrap(req, res, tid);
    return;
  }

  if (req.method === "POST" && path === "/api/codex-relay/ws-ticket") {
    if (!applyRateLimit(req, res, "mint")) return;
    await handleCodexWsTicket(req, res);
    return;
  }

  // --- Codex Remote Control pages (Phase 2c/2e, post-/demo) ---

  if (req.method === "GET" && (path === "/pair" || path === "/pair/")) {
    serveAppFile(res, "pair.html");
    return;
  }

  // /pair/<CODE> ... URL-first pair flow. Per plan C1 + round 5: real daemon
  // alphabet [ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}, length 6, L IS included.
  if (req.method === "GET" && /^\/pair\/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/.test(path)) {
    serveAppFile(res, "pair.html");
    return;
  }

  // /:handle/codex-remote-control/:threadId
  const remoteControlMatch = path.match(/^\/([^/]+)\/codex-remote-control\/([^/]+)\/?$/);
  if (req.method === "GET" && remoteControlMatch) {
    serveAppFile(res, "codex-remote-control/index.html");
    return;
  }

  if (req.method === "GET" && path.startsWith("/app/")) {
    const rel = path.slice("/app/".length);
    if (rel.includes("..")) { json(res, 400, { error: "bad path" }); return; }
    serveAppFile(res, rel);
    return;
  }

  json(res, 404, { error: "Not found" });
});

// ---------- Codex Relay (codex-daemon ↔ phone) ----------
//
// In-memory state. Pairing codes: 6-char, 5-min TTL. Daemons indexed by
// immutable tenant id (one daemon per tenant; new daemon kicks the old one). Web clients
// indexed by `tenantId:threadId`. The server is a transport relay between
// the daemon and matching web client(s). The relay injects the route thread
// into the E2EE handshake, and the daemon enforces that bound route after
// decrypting session commands.

const CODEX_PAIR_EXPIRY_MS = 5 * 60 * 1000;
const CODEX_PAIR_PRESENCE_TTL_MS = 2 * 60 * 1000;
const CODEX_PAIR_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const codexPairings = {};       // pairing_id -> { code, status, expires, poll_token, poll_token_used?, daemon_info, apiKey?, agentId?, handle?, daemon_public_key?, crypto_versions? }
const codexPairingByCode = {};  // code -> pairing_id (only while pending)
const codexPairPresenceTokens = new Map(); // token -> { agentId, expires, used }
const codexDaemons = new Map(); // agentId -> ws
const codexWebClients = new Map(); // `${agentId}:${threadId}` -> Set<ws>
const codexE2eeSessionRoutes = new Map(); // `${agentId}:${e2eeSession}` -> { threadId, webKey, ws }

// E2EE substrate (Phase 2.5).
//
// codexDaemonPubkeyRegistry: per tenant id, the most recently paired daemon's
//   public key (P-256 SPKI base64url) + supported crypto versions +
//   registration timestamp. This is what the browser fetches via
//   bootstrap before opening an encrypted session.
//
// codexRelayTickets: short-lived single-use tickets that replace
//   ?token=ck-... in the browser WebSocket URL. Bound to a specific
//   (agentId, threadId) so a leaked ticket cannot drive a different
//   route, even by the same authenticated user.
const codexRelayTickets = new Map();    // ticket -> { agentId, threadId, expires, used }
const CODEX_RELAY_TICKET_TTL_MS = 60 * 1000; // 60s; browser must connect immediately

const codexDaemonPubkeyRegistry = createCodexDaemonPubkeyRegistry({
  usePrisma,
  prisma,
  devMode: DEV_MODE,
  logger: console,
});

await codexDaemonPubkeyRegistry.loadFromDb();

function codexRelayKey(agentId, id) {
  return agentId + ":" + id;
}

function isCodexE2eeEnvelope(envelope) {
  return !!(envelope && typeof envelope.type === "string" && envelope.type.startsWith("e2ee."));
}

function registerCodexE2eeSessionRoute(agentId, e2eeSession, threadId, ws) {
  if (typeof e2eeSession !== "string" || !e2eeSession) return;
  if (typeof threadId !== "string" || !threadId) return;
  const webKey = codexRelayKey(agentId, threadId);
  codexE2eeSessionRoutes.set(codexRelayKey(agentId, e2eeSession), { threadId, webKey, ws });
}

function addCodexWebClient(webKey, ws) {
  let clients = codexWebClients.get(webKey);
  if (!clients) {
    clients = new Set();
    codexWebClients.set(webKey, clients);
  }
  clients.add(ws);
  return clients.size;
}

function removeCodexWebClient(webKey, ws) {
  const clients = codexWebClients.get(webKey);
  if (!clients) return 0;
  clients.delete(ws);
  if (clients.size === 0) {
    codexWebClients.delete(webKey);
    return 0;
  }
  return clients.size;
}

function openCodexWebClientsForKey(webKey) {
  const clients = codexWebClients.get(webKey);
  if (!clients) return [];
  return [...clients].filter((webWs) => webWs.readyState === webWs.OPEN);
}

function resolveCodexWebClientsForDaemonFrame(agentId, routeId) {
  const routed = codexE2eeSessionRoutes.get(codexRelayKey(agentId, routeId));
  if (routed && routed.ws && routed.ws.readyState === routed.ws.OPEN) return [routed.ws];
  return openCodexWebClientsForKey(codexRelayKey(agentId, routeId));
}

function removeCodexE2eeRoutesForWeb(agentId, threadId, ws) {
  const webKey = codexRelayKey(agentId, threadId);
  for (const [routeKey, route] of codexE2eeSessionRoutes) {
    if (route.webKey === webKey && (!ws || route.ws === ws)) {
      codexE2eeSessionRoutes.delete(routeKey);
    }
  }
}

function invalidateCodexBrowserSessionsForAgent(agentId, reason) {
  const prefix = agentId + ":";
  let closed = 0;
  for (const routeKey of [...codexE2eeSessionRoutes.keys()]) {
    if (routeKey.startsWith(prefix)) codexE2eeSessionRoutes.delete(routeKey);
  }
  for (const [webKey, clients] of [...codexWebClients]) {
    if (!webKey.startsWith(prefix)) continue;
    for (const webWs of clients) {
      if (webWs.readyState === webWs.OPEN) {
        closed += 1;
        try { webWs.close(4001, reason); } catch {}
      }
    }
    codexWebClients.delete(webKey);
  }
  return closed;
}

function logCodexWsLimit({ agentId, threadId, connectionId, reason }) {
  console.warn(formatCodexWsLimitLog({ agentId, threadId, connectionId, reason }));
}

function closeCodexWsForLimit(ws, { agentId, threadId, connectionId }, decision) {
  logCodexWsLimit({ agentId, threadId, connectionId, reason: decision.reason });
  try { ws.close(decision.code, decision.reason); } catch {}
}

function generateCodexPairingCode() {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    let code = "";
    const bytes = randomBytes(6);
    for (let i = 0; i < 6; i += 1) {
      code += CODEX_PAIR_ALPHABET[bytes[i] % CODEX_PAIR_ALPHABET.length];
    }
    if (!codexPairingByCode[code]) return code;
  }
  throw new Error("Could not generate unique codex-relay pairing code");
}

function generateCodexPairPollToken() {
  return "ppt_" + randomBytes(32).toString("base64url");
}

function cleanupCodexPairPresenceTokens() {
  const now = Date.now();
  for (const [token, entry] of codexPairPresenceTokens) {
    if (!entry || entry.used || now > entry.expires) codexPairPresenceTokens.delete(token);
  }
}

function generateCodexPairPresenceToken(agentId) {
  cleanupCodexPairPresenceTokens();
  if (typeof agentId !== "string" || !agentId) return null;
  const token = "cpt_" + randomBytes(32).toString("base64url");
  codexPairPresenceTokens.set(token, {
    agentId,
    expires: Date.now() + CODEX_PAIR_PRESENCE_TTL_MS,
    used: false,
  });
  return token;
}

function consumeCodexPairPresenceToken(token, agentId) {
  cleanupCodexPairPresenceTokens();
  const entry = codexPairPresenceTokens.get(token);
  if (!entry || entry.used || entry.agentId !== agentId || Date.now() > entry.expires) return false;
  entry.used = true;
  codexPairPresenceTokens.delete(token);
  return true;
}

function getBearerToken(req) {
  const auth = req.headers["authorization"];
  if (typeof auth !== "string" || !auth.startsWith("Bearer ")) return null;
  const token = auth.slice(7).trim();
  return token || null;
}

async function handleCodexPairInit(req, res) {
  let body = {};
  try { body = (await readBody(req)) || {}; } catch {}
  const code = generateCodexPairingCode();
  const pairingId = randomUUID();
  const pollToken = generateCodexPairPollToken();
  const expires = Date.now() + CODEX_PAIR_EXPIRY_MS;
  codexPairings[pairingId] = {
    code,
    status: "pending",
    expires,
    poll_token: pollToken,
    poll_token_used: false,
    daemon_info: {
      hostname: typeof body.hostname === "string" ? body.hostname.slice(0, 64) : null,
      platform: typeof body.platform === "string" ? body.platform.slice(0, 32) : null,
      arch: typeof body.arch === "string" ? body.arch.slice(0, 16) : null,
    },
    // Phase 2.5: daemon publishes its E2EE identity pubkey + supported
    // crypto versions on pair-init. The browser later fetches these via
    // /api/codex-relay/bootstrap/:threadId before opening an encrypted
    // session. Both fields are optional for back-compat with pre-E2EE
    // daemons; absent pubkey means "no E2EE on this pair, legacy only."
    daemon_public_key: typeof body.daemon_public_key === "string" ? body.daemon_public_key.slice(0, 1024) : null,
    crypto_versions: Array.isArray(body.crypto_versions)
      ? body.crypto_versions.filter((v) => typeof v === "string" && v.length <= 32).slice(0, 8)
      : null,
  };
  codexPairingByCode[code] = pairingId;
  // Per plan: web_url goes through /login first so the existing Kaleidoscope
  // QR + phone-passkey ceremony handles auth. After phone passkey, phone
  // (not desktop) redirects to /pair/<CODE> and completes pair-complete.
  json(res, 200, {
    code,
    pairing_id: pairingId,
    pair_poll_token: pollToken,
    web_url: ISSUER_URL + "/login?next=" + encodeURIComponent("/pair/" + code),
    expires_at: new Date(expires).toISOString(),
  });
}

function handleCodexPairStatus(req, res, pairingId) {
  const p = codexPairings[pairingId];
  if (!p) { json(res, 404, { error: "pairing not found" }); return; }
  if (Date.now() > p.expires) {
    p.status = "expired";
    if (codexPairingByCode[p.code] === pairingId) delete codexPairingByCode[p.code];
    json(res, 401, { error: "pair_poll_token_expired" });
    return;
  }
  const pollToken = getBearerToken(req);
  if (!pollToken || pollToken !== p.poll_token || p.poll_token_used) {
    json(res, 401, { error: "invalid_pair_poll_token" });
    return;
  }
  if (p.status === "completed") {
    p.poll_token_used = true;
    json(res, 200, {
      status: "completed",
      api_key: p.apiKey,
      handle: p.handle || p.agentId,
      replaced_daemon_key: !!p.replaced_daemon_key,
    });
  } else {
    json(res, 200, { status: p.status });
  }
}

async function handleCodexPairComplete(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
  let body;
  try { body = await readBody(req); } catch { json(res, 400, { error: "bad request" }); return; }
  const code = (body && typeof body.code === "string") ? body.code.trim().toUpperCase() : "";
  if (!code) { json(res, 400, { error: "missing code" }); return; }
  // Defensive: reject codes that don't match the daemon's alphabet up front,
  // before the map lookup, so probe attempts get one uniform reject path
  // instead of leaking timing/shape info between "wrong-alphabet" and "valid
  // shape but unknown code." Per plan C3 + round 5.
  if (!/^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/.test(code)) {
    json(res, 404, { error: "invalid or already-used code" });
    return;
  }
  const pairingId = codexPairingByCode[code];
  if (!pairingId) { json(res, 404, { error: "invalid or already-used code" }); return; }
  const p = codexPairings[pairingId];
  if (!p || p.status !== "pending" || Date.now() > p.expires) {
    json(res, 410, { error: "code expired or already used" });
    return;
  }
  const pairPresenceToken = body && typeof body.codex_pair_presence_token === "string"
    ? body.codex_pair_presence_token
    : "";
  if (p.daemon_public_key && !consumeCodexPairPresenceToken(pairPresenceToken, identity.agentId)) {
    json(res, 403, {
      error: "fresh_presence_required",
      error_description: "Pairing this daemon requires a fresh passkey confirmation. Sign in again from the pair page.",
    });
    return;
  }
  // Phase 2.5: register the daemon's E2EE public key against the
  // authenticated immutable tenant id. The display handle is returned
  // as metadata only.
  let daemonKeyResult = null;
  if (p.daemon_public_key) {
    daemonKeyResult = await codexDaemonPubkeyRegistry.register(identity.agentId, p.daemon_public_key, p.crypto_versions, "pair-complete");
    if (daemonKeyResult?.replaced) {
      const closed = invalidateCodexBrowserSessionsForAgent(identity.agentId, "daemon key replaced");
      console.log(
        "codex-relay: replaced daemon E2EE key for tenant " + identity.agentId
        + " old=" + daemonKeyResult.old_fingerprint
        + " new=" + daemonKeyResult.new_fingerprint
        + " closed_browser_sessions=" + closed
      );
    }
  }
  p.status = "completed";
  p.apiKey = identity.apiKey;
  p.agentId = identity.agentId;
  p.handle = identity.handle;
  p.replaced_daemon_key = !!daemonKeyResult?.replaced;
  delete codexPairingByCode[code];
  console.log("codex-relay: paired daemon for tenant " + identity.agentId + " handle " + identity.handle);
  json(res, 200, {
    ok: true,
    handle: identity.handle,
    replaced_daemon_key: !!daemonKeyResult?.replaced,
  });
}

function handleCodexRelayState(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
  json(res, 200, {
    handle: identity.handle,
    daemon_online: codexDaemons.has(identity.agentId),
  });
}

// GET /api/codex-relay/bootstrap/:threadId
// Browser calls this after passkey auth + before opening the encrypted
// WebSocket. Returns enough metadata for the browser to know whether
// E2EE is available with this daemon and which crypto version to use.
function handleCodexBootstrap(req, res, threadId) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
  if (!threadId) { json(res, 400, { error: "missing threadId" }); return; }
  const daemonOnline = codexDaemons.has(identity.agentId);
  const daemonKey = codexDaemonPubkeyRegistry.get(identity.agentId);
  json(res, 200, buildCodexBootstrapPayload({ identity, threadId, daemonOnline, daemonKey }));
}

// POST /api/codex-relay/ws-ticket
// Browser exchanges its long-lived ck- key for a short-lived single-use
// relay ticket bound to a specific (agentId, threadId). The browser then
// connects to /api/codex-relay/web/:threadId?ticket=... instead of
// putting ck- in the URL.
async function handleCodexWsTicket(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
  let body;
  try { body = (await readBody(req)) || {}; } catch { body = {}; }
  const threadId = (body && typeof body.thread_id === "string") ? body.thread_id.trim() : "";
  if (!threadId) { json(res, 400, { error: "missing thread_id" }); return; }
  if (threadId.length > 256) { json(res, 400, { error: "thread_id too long" }); return; }
  const ticket = "rt_" + randomBytes(24).toString("base64url");
  const expires = Date.now() + CODEX_RELAY_TICKET_TTL_MS;
  codexRelayTickets.set(ticket, {
    agentId: identity.agentId,
    handle: identity.handle,
    threadId,
    expires,
    used: false,
  });
  // Lazy cleanup: schedule eviction after TTL.
  setTimeout(() => {
    const t = codexRelayTickets.get(ticket);
    if (t && t.expires <= Date.now()) codexRelayTickets.delete(ticket);
  }, CODEX_RELAY_TICKET_TTL_MS + 5_000);
  json(res, 200, {
    ticket,
    expires_at: new Date(expires).toISOString(),
    ttl_seconds: Math.floor(CODEX_RELAY_TICKET_TTL_MS / 1000),
  });
}

function consumeCodexRelayTicket(ticket, threadId) {
  if (typeof ticket !== "string" || !ticket) return null;
  const entry = codexRelayTickets.get(ticket);
  if (!entry) return null;
  if (entry.used) return null;
  if (Date.now() > entry.expires) { codexRelayTickets.delete(ticket); return null; }
  if (entry.threadId !== threadId) return null; // bound to specific route
  entry.used = true;
  return { agentId: entry.agentId, handle: entry.handle || entry.agentId };
}

function serveAppFile(res, relPath) {
  const filePath = join(__dirname, "app", relPath);
  try {
    const content = readFileSync(filePath);
    const ext = (relPath.split(".").pop() || "").toLowerCase();
    const mimeTypes = {
      html: "text/html",
      css: "text/css",
      js: "text/javascript",
      svg: "image/svg+xml",
      png: "image/png",
      json: "application/json",
      ico: "image/x-icon",
    };
    const mime = mimeTypes[ext] || "application/octet-stream";
    const charset = (ext === "html" || ext === "css" || ext === "js" || ext === "svg" || ext === "json") ? "; charset=utf-8" : "";
    res.writeHead(200, { "Content-Type": mime + charset });
    res.end(content);
  } catch {
    json(res, 404, { error: "Not found" });
  }
}

// authenticateWs verifies a WS upgrade request against the API_KEYS
// map. Default behavior is HEADER ONLY: Authorization: Bearer ck-...
// is accepted; ?token=ck-... in the URL is ignored.
//
// Set { allowQueryToken: true } only on the explicit web-side
// back-compat branch that runs inside ALLOW_WS_URL_TOKEN. Daemon
// connections never enable this; CLI clients can always set
// Authorization, and a daemon accepting URL-token would be a needless
// attack surface (URL leaks via referrer / log scrape are not relevant
// for daemons, but the asymmetry of "header-only on the daemon path"
// keeps the policy clean and auditable).
function authenticateWs(req, { allowQueryToken = false } = {}) {
  const auth = req.headers["authorization"];
  if (auth && auth.startsWith("Bearer ")) {
    const key = auth.slice(7).trim();
    const identity = identityForApiKey(key);
    if (identity) return identity;
  }
  if (!allowQueryToken) return null;

  // Web back-compat path only. Browsers cannot set Authorization on a
  // WebSocket() handshake, so legacy clients put ck- in the URL.
  // parseUrl returns a WHATWG URL, which has no .query getter (only
  // .search/.searchParams). Strip the leading "?" off .search and
  // parse with querystring so the array/string handling below works.
  const u = parseUrl(req.url);
  const qs = u.search ? parseUrlQs(u.search.slice(1)) : {};
  const tokenParam = Array.isArray(qs.token) ? qs.token[0] : qs.token;
  if (typeof tokenParam === "string") {
    return identityForApiKey(tokenParam);
  }
  return null;
}

// F-001: subprotocol-based WS auth for the codex-relay surface. The web
// client sends Sec-WebSocket-Protocol: ldm-codex-relay.v1, ticket.<v>.
// Server echoes only the protocol name (not the ticket-bearing entry).
// Daemon connections do not use a subprotocol, so empty Sets pass.
const codexRelayWss = new WebSocketServer({
  noServer: true,
  handleProtocols: (protocols /*, request */) => {
    if (!protocols || protocols.size === 0) return undefined;
    if (protocols.has("ldm-codex-relay.v1")) return "ldm-codex-relay.v1";
    return false;
  },
});

function getTicketFromSubprotocol(req) {
  const header = req.headers["sec-websocket-protocol"];
  if (!header) return null;
  const tokens = header.split(",").map(s => s.trim()).filter(Boolean);
  for (const t of tokens) {
    if (t.startsWith("ticket.")) {
      return t.slice("ticket.".length);
    }
  }
  return null;
}

httpServer.on("upgrade", (req, socket, head) => {
  const u = parseUrl(req.url);
  const path = u.pathname || "";
  const isDaemon = path === "/api/codex-relay/daemon";
  const isWeb = path.startsWith("/api/codex-relay/web/");
  if (!isDaemon && !isWeb) return; // let other listeners (or default) handle it

  // F-003: enforce Origin allowlist for browser-borne web upgrades.
  // Runs BEFORE ticket consumption / authenticateWs so a request from
  // a disallowed origin cannot burn a valid one-time ticket or trigger
  // an auth check side effect. Daemon path is exempt because CLI
  // clients do not send a browser Origin header. Requires nginx to
  // pass the Origin header through unchanged on the upgrade hop;
  // verified in Lane B B2 of the audit doc.
  if (isWeb) {
    const origin = req.headers["origin"];
    if (!isWsOriginAllowed(origin)) {
      console.warn("WS upgrade rejected: bad origin (" + (origin || "<none>") + ") for " + path);
      socket.write("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n");
      socket.destroy();
      return;
    }
  }

  // Daemon side keeps the existing Bearer ck- token auth.
  // Web side: prefer ticket via Sec-WebSocket-Protocol (F-001), fall
  // back to ?ticket= query string. The legacy ?token=ck- URL fallback
  // is gated behind LDM_HOSTED_MCP_ALLOW_WS_URL_TOKEN=1; production
  // does not accept it.
  let identity = null;
  if (isDaemon) {
    // Daemon connections must use Authorization: Bearer ck-. URL-token
    // is never accepted on the daemon path (allowQueryToken: false).
    identity = authenticateWs(req, { allowQueryToken: false });
  } else {
    const threadId = decodeURIComponent(path.slice("/api/codex-relay/web/".length));

    // Preferred path: ticket carried in Sec-WebSocket-Protocol. Avoids
    // URL/log/referrer exposure of the ticket value.
    const subTicket = getTicketFromSubprotocol(req);
    if (subTicket) {
      const consumed = consumeCodexRelayTicket(subTicket, threadId);
      if (consumed) identity = { agentId: consumed.agentId, handle: consumed.handle, viaTicket: true };
    }

    // Back-compat: ?ticket= query string. Same single-use binding.
    if (!identity) {
      // parseUrl returns a WHATWG URL with .search/.searchParams, no
      // .query. Strip the leading "?" off .search and parse with
      // querystring so the array/string handling below still works.
      const qs = u.search ? parseUrlQs(u.search.slice(1)) : {};
      const ticketParam = Array.isArray(qs.ticket) ? qs.ticket[0] : qs.ticket;
      if (typeof ticketParam === "string" && ticketParam) {
        const consumed = consumeCodexRelayTicket(ticketParam, threadId);
        if (consumed) identity = { agentId: consumed.agentId, handle: consumed.handle, viaTicket: true };
      }
    }

    // Legacy ?token=ck- URL fallback: dev/back-compat only. Production
    // refuses long-lived bearer in WS URLs (gate condition 2). The
    // URL-token branch in authenticateWs is gated by allowQueryToken,
    // and we only set it true here, only when ALLOW_WS_URL_TOKEN is on.
    if (!identity && ALLOW_WS_URL_TOKEN) {
      identity = authenticateWs(req, { allowQueryToken: true });
    }
  }

  if (!identity) {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
    return;
  }

  if (isDaemon) {
    codexRelayWss.handleUpgrade(req, socket, head, (ws) => {
      let daemonIdentityAccepted = false;
      function activateCodexDaemonWs() {
        const previous = codexDaemons.get(identity.agentId);
        if (previous && previous !== ws && previous.readyState === previous.OPEN) {
          console.warn("codex-relay: rejected duplicate daemon reconnect for online tenant " + identity.agentId);
          try { ws.close(4004, "daemon already online"); } catch {}
          return false;
        }
        if (previous && previous !== ws) try { previous.close(4000, "replaced"); } catch {}
        codexDaemons.set(identity.agentId, ws);
        console.log("codex-relay: daemon online for " + identity.agentId);
        return true;
      }
      // F-001 per-thread isolation. Daemon -> web routing must NOT
      // fan out every frame to every same-agent web socket; that
      // breaks isolation when one user has multiple threads open.
      // Parse the OUTER envelope only to read the routing field
      // (session/sessionId). The encrypted ciphertext (or any inner
      // session.* payload) is never inspected, so gate 3a still
      // holds: the relay sees only routing metadata on the envelope.
      // No-session frames are an explicit allowlist (control/presence
      // types) or are dropped with a redacted warning. We never
      // broadcast unknown frames.
      const BROADCAST_TYPES = new Set([
        "presence",
        "presence.web",
        "presence.daemon",
        "daemon.online",
        "daemon.offline",
      ]);
      ws.on("message", (data) => {
        const text = data.toString();
        let envelope = null;
        try { envelope = JSON.parse(text); } catch {}
        if (envelope?.type === "daemon.identity") {
          const reconnectPolicy = evaluateCodexDaemonReconnectPubkey(
            codexDaemonPubkeyRegistry.get(identity.agentId),
            envelope.daemon_public_key,
          );
          if (!reconnectPolicy.allowed) {
            console.warn(
              "codex-relay: rejected daemon reconnect E2EE key for tenant " + identity.agentId
              + " reason=" + reconnectPolicy.reason
              + " old=" + (reconnectPolicy.old_fingerprint || "<none>")
              + " new=" + (reconnectPolicy.new_fingerprint || codexDaemonPubkeyFingerprint(envelope.daemon_public_key) || "<none>"),
            );
            const closeReason = reconnectPolicy.replaced
              ? "daemon key change requires fresh pair"
              : "invalid daemon identity";
            try { ws.close(reconnectPolicy.replaced ? 4003 : 1008, closeReason); } catch {}
            return;
          }
          void codexDaemonPubkeyRegistry.register(
            identity.agentId,
            envelope.daemon_public_key,
            envelope.crypto_versions,
            "daemon-reconnect",
          ).then((result) => {
            if (!result?.registered) {
              try { ws.close(1011, "daemon identity persistence failed"); } catch {}
              return;
            }
            daemonIdentityAccepted = activateCodexDaemonWs();
          }).catch(() => {
            try { ws.close(1011, "daemon identity persistence failed"); } catch {}
          });
          return;
        }
        if (!daemonIdentityAccepted) {
          try { ws.close(1008, "daemon identity required"); } catch {}
          return;
        }
        const sessionId = envelope?.session || envelope?.sessionId || envelope?.threadId;
        if (sessionId) {
          const targets = resolveCodexWebClientsForDaemonFrame(identity.agentId, sessionId);
          for (const target of targets) {
            target.send(text);
          }
          // No matching web client: drop silently. Daemon-emitted
          // frames for a thread the user has not opened in any browser
          // are not interesting to fan out elsewhere.
          return;
        }
        const type = envelope?.type;
        if (type && BROADCAST_TYPES.has(type)) {
          // Allowlisted agent-level frame (presence, online status).
          // Fan out within agent, never across agents.
          const prefix = identity.agentId + ":";
          for (const [key, webClients] of codexWebClients) {
            if (key.startsWith(prefix)) {
              for (const webWs of webClients) {
                if (webWs.readyState === webWs.OPEN) webWs.send(text);
              }
            }
          }
          return;
        }
        // Parse failed, missing session, or unknown type: drop. Log a
        // redacted notice so the operator can see if a daemon is
        // emitting unrouteable frames. We never log envelope/payload
        // bytes; only the agent and the type (or "no-type").
        const typeMarker = type ? String(type).slice(0, 32) : "no-type";
        console.warn("codex-relay: dropped unroutable daemon frame for " + identity.agentId + " (type=" + typeMarker + ")");
      });
      ws.on("close", () => {
        if (codexDaemons.get(identity.agentId) === ws) {
          codexDaemons.delete(identity.agentId);
          console.log("codex-relay: daemon offline for " + identity.agentId);
        }
      });
      ws.on("error", (err) => {
        console.error("codex-relay daemon ws error:", err.message);
      });
    });
    return;
  }

  // Web side: /api/codex-relay/web/<threadId>
  const threadId = decodeURIComponent(path.slice("/api/codex-relay/web/".length));
  if (!threadId || threadId.includes("/")) {
    socket.write("HTTP/1.1 400 Bad Request\r\n\r\n");
    socket.destroy();
    return;
  }
  const webKey = codexRelayKey(identity.agentId, threadId);
  if (isCodexWsAgentDisabled(CODEX_WS_ABUSE_LIMITS, identity.agentId)) {
    console.warn(formatCodexWsLimitLog({
      agentId: identity.agentId,
      threadId,
      connectionId: "upgrade",
      reason: "operator disabled",
    }));
    socket.write("HTTP/1.1 503 Service Unavailable\r\nConnection: close\r\n\r\n");
    socket.destroy();
    return;
  }
  const openBrowserSockets = openCodexWebClientsForKey(webKey).length;
  if (openBrowserSockets >= CODEX_WS_ABUSE_LIMITS.maxBrowserSocketsPerThread) {
    console.warn(formatCodexWsLimitLog({
      agentId: identity.agentId,
      threadId,
      connectionId: "upgrade",
      reason: "too many browser sockets",
    }));
    socket.write("HTTP/1.1 429 Too Many Requests\r\nConnection: close\r\n\r\n");
    socket.destroy();
    return;
  }
  codexRelayWss.handleUpgrade(req, socket, head, (ws) => {
    const connectionId = randomUUID();
    const guard = createCodexWsConnectionGuard({
      config: CODEX_WS_ABUSE_LIMITS,
      agentId: identity.agentId,
    });
    const guardContext = { agentId: identity.agentId, threadId, connectionId };
    const idleIntervalMs = Math.max(1000, Math.min(60_000, Math.floor(CODEX_WS_ABUSE_LIMITS.idleTtlMs / 2)));
    const idleTimer = setInterval(() => {
      const decision = guard.observeIdle();
      if (!decision.ok && ws.readyState === ws.OPEN) {
        closeCodexWsForLimit(ws, guardContext, decision);
      }
    }, idleIntervalMs);
    const clientCount = addCodexWebClient(webKey, ws);
    console.log("codex-relay: web online " + webKey + " clients=" + clientCount + " conn=" + connectionId);
    ws.on("message", (data) => {
      const frameDecision = guard.observeFrame(codexWsFrameByteLength(data));
      if (!frameDecision.ok) {
        closeCodexWsForLimit(ws, guardContext, frameDecision);
        return;
      }
      let text = data.toString();
      let envelope = null;
      try { envelope = JSON.parse(text); } catch {}
      if (!envelope || typeof envelope !== "object" || Array.isArray(envelope)) {
        const malformedDecision = guard.observeMalformed();
        if (!malformedDecision.ok) {
          closeCodexWsForLimit(ws, guardContext, malformedDecision);
        }
        return;
      }
      if (isCodexE2eeEnvelope(envelope) && envelope.session) {
        // The browser cannot be allowed to choose this value. The relay
        // owns the route because it consumed the ticket for this URL
        // thread. The daemon uses this metadata to bind the encrypted
        // session before it decrypts any session.* command.
        envelope.route_thread_id = threadId;
        text = JSON.stringify(envelope);
        registerCodexE2eeSessionRoute(identity.agentId, envelope.session, threadId, ws);
      }
      const daemonWs = codexDaemons.get(identity.agentId);
      if (daemonWs && daemonWs.readyState === daemonWs.OPEN) {
        const pendingDecision = guard.observePendingBytes(daemonWs.bufferedAmount || 0);
        if (!pendingDecision.ok) {
          closeCodexWsForLimit(ws, guardContext, pendingDecision);
          return;
        }
        daemonWs.send(text);
      } else {
        try { ws.send(JSON.stringify({ type: "error", message: "daemon offline" })); } catch {}
      }
    });
    ws.on("close", () => {
      clearInterval(idleTimer);
      removeCodexE2eeRoutesForWeb(identity.agentId, threadId, ws);
      removeCodexWebClient(webKey, ws);
    });
    ws.on("error", (err) => {
      console.error("codex-relay web ws error:", err.message);
    });
  });
});

httpServer.listen(PORT, SERVER_BIND, () => {
  console.log(SERVER_NAME + " v" + SERVER_VERSION + " listening on " + SERVER_BIND + ":" + PORT);
  console.log("WS origin allowlist: " + WS_ORIGIN_ALLOWLIST.join(", "));
  console.log("Health:        http://localhost:" + PORT + "/health");
  console.log("MCP:           http://localhost:" + PORT + "/mcp");
  console.log("OAuth:         http://localhost:" + PORT + "/.well-known/oauth-authorization-server");
  console.log("Signup:        http://localhost:" + PORT + "/signup");
  console.log("Login:         http://localhost:" + PORT + "/login");
  console.log("Pair (codex):  http://localhost:" + PORT + "/pair");
  console.log("Demo (legacy): http://localhost:" + PORT + "/demo/");
  console.log("Passkeys stored: " + passkeys.length);
  console.log("Session timeout: " + (SESSION_TIMEOUT_MS / 60000) + " min");
});

async function shutdown() {
  console.log("Shutting down...");
  clearInterval(cleanupTimer);
  for (const sid of Object.keys(sessions)) {
    try { await sessions[sid].transport.close(); } catch {}
    delete sessions[sid];
  }
  httpServer.close();
  process.exit(0);
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
