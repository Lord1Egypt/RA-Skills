// server.mjs: Hosted MCP server for wip.computer
// MCP Streamable HTTP transport at /mcp, health check at /health.
// Auth: Bearer ck-... API key maps to an agent ID.
// OAuth 2.0: Minimal flow for Claude iOS custom connector.
// WebAuthn: Passkey-based signup/login (replaces agent name text form).

import { randomUUID, randomBytes, createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
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

// ── Settings ─────────────────────────────────────────────────────────

const PORT = parseInt(process.env.MCP_PORT || "18800", 10);
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
// Primary: Postgres via Prisma (production).
// Fallback: JSON files (if DATABASE_URL is not set, e.g. local dev without Postgres).
//
// The demo and all API endpoints use the db.* functions below.
// They try Prisma first, fall back to JSON if Prisma isn't available.

const __dirname = dirname(fileURLToPath(import.meta.url));
const TOKEN_FILE = join(__dirname, "tokens.json");
const PASSKEY_FILE = join(__dirname, "passkeys.json");
const WALLET_FILE_LEGACY = join(__dirname, "wallets.json");

// Initialize Prisma (may fail if DATABASE_URL not set)
let prisma = null;
let usePrisma = false;
try {
  prisma = new PrismaClient();
  await prisma.$connect();
  usePrisma = true;
  console.log("Database: Postgres via Prisma");
} catch (err) {
  console.log("Database: JSON files (Prisma not available: " + err.message + ")");
}

// ── API Keys ────────────────────────────────────────────────────────

// Hardcoded defaults (always available, even without DB)
const DEFAULT_API_KEYS = {
  "ck-test-001": "test-agent",
  "ck-e04df46877aa3672e21c4e33149bacc4": "cc-mini",
  "ck-f1986e957e21cbb40dc100bc05dc78ec": "lesa",
  "ck-c2849eef903407c877bc6e79bf8794aa": "parker",
};

// In-memory cache (populated from DB or JSON on boot)
const API_KEYS = { ...DEFAULT_API_KEYS };

// Load from JSON (fallback)
function loadTokensFromFile() {
  try { return JSON.parse(readFileSync(TOKEN_FILE, "utf8")); } catch { return {}; }
}
Object.assign(API_KEYS, loadTokensFromFile());

async function saveApiKey(key, agentId) {
  API_KEYS[key] = agentId;
  if (usePrisma) {
    try {
      await prisma.apiKey.upsert({
        where: { key },
        update: { agentId },
        create: { key, agentId },
      });
    } catch (err) {
      console.error("Prisma saveApiKey error:", err.message);
    }
  }
  // Always write JSON as backup
  try { writeFileSync(TOKEN_FILE, JSON.stringify(API_KEYS, null, 2) + "\n"); } catch {}
}

// ── Passkeys ────────────────────────────────────────────────────────

// In-memory array (populated from DB or JSON on boot)
let passkeys = [];

function loadPasskeysFromFile() {
  try { return JSON.parse(readFileSync(PASSKEY_FILE, "utf8")); } catch { return []; }
}

async function loadPasskeysFromDb() {
  if (!usePrisma) return loadPasskeysFromFile();
  try {
    const creds = await prisma.credential.findMany({ include: { user: true } });
    return creds.map(c => ({
      credentialId: c.id,
      publicKey: Buffer.from(c.publicKey).toString("base64url"),
      counter: c.counter,
      userId: c.userId,
      agentId: c.user?.name ? "passkey-" + c.user.name.slice(0, 12) : "unknown",
      createdAt: c.createdAt.toISOString(),
      transports: c.transports || [],
    }));
  } catch (err) {
    console.error("Prisma loadPasskeys error:", err.message);
    return loadPasskeysFromFile();
  }
}

async function savePasskey(entry) {
  passkeys.push(entry);
  if (usePrisma) {
    try {
      // Ensure user exists
      let user = await prisma.user.findUnique({ where: { id: entry.userId } });
      if (!user) {
        user = await prisma.user.create({
          data: { id: entry.userId, name: entry.agentId || "user" },
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
    }
  }
  // Always write JSON as backup
  try { writeFileSync(PASSKEY_FILE, JSON.stringify(passkeys, null, 2) + "\n"); } catch {}
}

async function updatePasskeyCounter(credentialId, newCounter) {
  const entry = passkeys.find(p => p.credentialId === credentialId);
  if (entry) entry.counter = newCounter;
  if (usePrisma) {
    try {
      await prisma.credential.update({
        where: { id: credentialId },
        data: { counter: newCounter },
      });
    } catch (err) {
      console.error("Prisma updateCounter error:", err.message);
    }
  }
  try { writeFileSync(PASSKEY_FILE, JSON.stringify(passkeys, null, 2) + "\n"); } catch {}
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
  return API_KEYS[key] ? { agentId: API_KEYS[key], apiKey: key } : null;
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

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function sanitizeUsername(raw) {
  if (!raw || typeof raw !== "string") return null;
  const cleaned = raw.toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 30);
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

  // Accept optional username from request body
  const username = sanitizeUsername(body?.username);

  const userId = randomBytes(16);
  const userIdB64 = userId.toString("base64url");

  const userName = username || ("user-" + userIdB64.slice(0, 8));
  const displayName = username || "Memory Crystal User";

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
    username: username,
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

  // Use provided username as agentId, or fall back to passkey-<id>
  const agentId = stored.username || ("passkey-" + stored.userId.slice(0, 12));
  const apiKey = generateApiKey();

  const entry = {
    credentialId: cred.id,
    publicKey: Buffer.from(cred.publicKey).toString("base64url"),
    counter: cred.counter,
    userId: stored.userId,
    agentId,
    apiKey,
    deviceType: credentialDeviceType,
    backedUp: credentialBackedUp,
    transports: credential.response?.transports || [],
    createdAt: new Date().toISOString(),
  };
  await savePasskey(entry);
  await saveApiKey(apiKey, agentId);

  console.log("WebAuthn: registered passkey for agent '" + agentId + "' (credId: " + cred.id.slice(0, 16) + "...)");

  json(res, 200, { success: true, agentId, apiKey });
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

  entry.counter = verification.authenticationInfo.newCounter;
  await updatePasskeyCounter(entry.credentialId, entry.counter);

  console.log("WebAuthn: authenticated agent '" + entry.agentId + "'");

  json(res, 200, { success: true, agentId: entry.agentId, apiKey: entry.apiKey });
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

  // Check if agent already has an API key (from passkey registration)
  const agentId = stored.agent_name || "oauth-user";
  let apiKey;

  const existingKey = Object.entries(API_KEYS).find(([k, v]) => v === agentId);
  if (existingKey) {
    apiKey = existingKey[0];
  } else {
    apiKey = generateApiKey();
    await saveApiKey(apiKey, agentId);
  }

  console.log("OAuth: issued token for agent '" + agentId + "' (key: " + apiKey.slice(0, 10) + "...)");

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

// POST /api/qr-login ... create a QR login session
async function handleQrLoginStart(req, res) {
  cleanupExpiredChallenges();
  const body = await readBody(req).catch(() => ({}));
  const handle = ((body && body.handle) || "").trim().toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 30);
  const mode = ((body && body.mode) || "register") === "signin" ? "signin" : "register";
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
  };
  console.log("QR login: created session " + sessionId.slice(0, 8) + "...");
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
function handleQrLoginStatus(req, res) {
  const url = parseUrl(req.url);
  const s = url.searchParams.get("s");
  const entry = qrLoginSessions[s];
  if (!entry || Date.now() > entry.expires) {
    json(res, 404, { error: "Session not found or expired" });
    return;
  }
  if (entry.status === "approved") {
    json(res, 200, { status: "approved", agentId: entry.agentId, apiKey: entry.apiKey });
    delete qrLoginSessions[s]; // one-time use
  } else {
    json(res, 200, { status: "pending" });
  }
}

// POST /api/qr-login/approve ... phone calls after passkey created
function handleQrLoginApprove(req, res) {
  readBody(req).then(function(body) {
    const { sessionId, agentId, apiKey } = body || {};
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
    console.log("QR login: approved session " + sessionId.slice(0, 8) + "... for '" + agentId + "'");
    json(res, 200, { ok: true });
  }).catch(function() {
    json(res, 400, { error: "Invalid request" });
  });
}

// ---------- Demo API handlers ----------

// ── Wallet tracking (per agent) ──
const IMAGE_COST_CENTS = 1; // $0.01
const INITIAL_BALANCE_CENTS = 500; // $5.00

// JSON fallback for wallets
const WALLET_FILE = join(dirname(fileURLToPath(import.meta.url)), "wallets.json");
function loadWalletsFromFile() { try { return JSON.parse(readFileSync(WALLET_FILE, "utf8")); } catch { return {}; } }
function saveWalletsToFile(w) { try { writeFileSync(WALLET_FILE, JSON.stringify(w, null, 2) + "\n"); } catch {} }

async function getBalance(agentId) {
  if (usePrisma) {
    try {
      const wallet = await prisma.wallet.findFirst({ where: { userId: agentId } });
      return wallet ? wallet.balance : INITIAL_BALANCE_CENTS;
    } catch {}
  }
  const w = loadWalletsFromFile();
  return w[agentId] !== undefined ? w[agentId] : INITIAL_BALANCE_CENTS;
}

async function deductBalance(agentId, cents) {
  if (usePrisma) {
    try {
      let wallet = await prisma.wallet.findFirst({ where: { userId: agentId } });
      if (!wallet) {
        wallet = await prisma.wallet.create({
          data: { userId: agentId, balance: INITIAL_BALANCE_CENTS },
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
  if (w[agentId] === undefined) w[agentId] = INITIAL_BALANCE_CENTS;
  w[agentId] = Math.max(0, w[agentId] - cents);
  saveWalletsToFile(w);
  return w[agentId];
}
function formatCents(c) { return "$" + (c / 100).toFixed(2); }

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

    const XAI_KEY = process.env.XAI_API_KEY || "";
    if (!XAI_KEY) {
      json(res, 503, { error: "Image generation not configured" });
      return;
    }

    const grokRes = await fetch("https://api.x.ai/v1/images/generations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + XAI_KEY,
      },
      body: JSON.stringify({
        model: "grok-imagine-image",
        prompt: prompt,
        n: 1,
      }),
    });

    const grokData = await grokRes.json();
    if (grokData.error) {
      json(res, 502, { error: grokData.error.message || "Image generation failed" });
      return;
    }

    const imageUrl = grokData.data?.[0]?.url;
    if (!imageUrl) {
      json(res, 502, { error: "No image returned" });
      return;
    }

    const newBalance = await deductBalance(identity.agentId, IMAGE_COST_CENTS);
    console.log("Demo: generated image for agent '" + identity.agentId + "' (balance: " + formatCents(newBalance) + ")");
    json(res, 200, { url: imageUrl, prompt: prompt, cost: formatCents(IMAGE_COST_CENTS), balance: formatCents(newBalance) });
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
    // Serve the new app/ login (two-path: this device or QR-from-phone).
    try {
      const loginHtml = readFileSync(join(__dirname, "app", "login.html"), "utf8");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(loginHtml);
    } catch {
      // Fallback to legacy demo login, then server-rendered.
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

  // --- Legal pages ---

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

  // --- WebAuthn API ---

  if (req.method === "POST" && path === "/webauthn/register-options") {
    await handleRegisterOptions(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/register-verify") {
    await handleRegisterVerify(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/auth-options") {
    await handleAuthOptions(req, res);
    return;
  }

  if (req.method === "POST" && path === "/webauthn/auth-verify") {
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
    await handleOAuthRegister(req, res);
    return;
  }

  if (req.method === "GET" && path === "/oauth/authorize") {
    handleOAuthAuthorize(req, res);
    return;
  }

  if (req.method === "POST" && path === "/oauth/authorize/submit") {
    await handleOAuthAuthorizeSubmit(req, res);
    return;
  }

  if (req.method === "POST" && path === "/oauth/token") {
    await handleOAuthToken(req, res);
    return;
  }

  // --- Agent QR Auth ---

  if (req.method === "GET" && path === "/demo/api/agent-auth") {
    await handleAgentAuthStart(req, res);
    return;
  }

  if (req.method === "GET" && path === "/demo/api/agent-auth/qr") {
    handleAgentAuthQR(req, res);
    return;
  }

  if (req.method === "GET" && path === "/demo/api/agent-auth/status") {
    handleAgentAuthStatus(req, res);
    return;
  }

  if (req.method === "POST" && path === "/demo/api/agent-auth/approve") {
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
    await handleQrLoginStart(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/qr-login/qr") {
    handleQrLoginQR(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/qr-login/status") {
    handleQrLoginStatus(req, res);
    return;
  }

  if (req.method === "POST" && path === "/api/qr-login/approve") {
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
    await handleCodexPairInit(req, res);
    return;
  }

  if (req.method === "GET" && path.startsWith("/api/codex-relay/pair-status/")) {
    handleCodexPairStatus(req, res, path.slice("/api/codex-relay/pair-status/".length));
    return;
  }

  if (req.method === "POST" && path === "/api/codex-relay/pair-complete") {
    await handleCodexPairComplete(req, res);
    return;
  }

  if (req.method === "GET" && path === "/api/codex-relay/state") {
    handleCodexRelayState(req, res);
    return;
  }

  if (req.method === "GET" && path.startsWith("/api/codex-relay/bootstrap/")) {
    const tid = decodeURIComponent(path.slice("/api/codex-relay/bootstrap/".length));
    handleCodexBootstrap(req, res, tid);
    return;
  }

  if (req.method === "POST" && path === "/api/codex-relay/ws-ticket") {
    await handleCodexWsTicket(req, res);
    return;
  }

  // --- Codex Remote Control pages (Phase 2c/2e, post-/demo) ---

  if (req.method === "GET" && (path === "/pair" || path === "/pair/")) {
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
// agentId (one daemon per agentId; new daemon kicks the old one). Web clients
// indexed by `agentId:threadId`. Server is a transparent passthrough between
// the daemon and the matching web client(s); thread routing is enforced
// purely client-side via session.send/sessionId payloads.

const CODEX_PAIR_EXPIRY_MS = 5 * 60 * 1000;
const CODEX_PAIR_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const codexPairings = {};       // pairing_id -> { code, status, expires, daemon_info, apiKey?, agentId?, daemon_public_key?, crypto_versions? }
const codexPairingByCode = {};  // code -> pairing_id (only while pending)
const codexDaemons = new Map(); // agentId -> ws
const codexWebClients = new Map(); // `${agentId}:${threadId}` -> ws

// E2EE substrate (Phase 2.5).
//
// codexDaemonPubkeys: per agentId, the most recently paired daemon's
//   public key (P-256 SPKI base64url) + supported crypto versions +
//   registration timestamp. This is what the browser fetches via
//   bootstrap before opening an encrypted session.
//
// codexRelayTickets: short-lived single-use tickets that replace
//   ?token=ck-... in the browser WebSocket URL. Bound to a specific
//   (agentId, threadId) so a leaked ticket cannot drive a different
//   route, even by the same authenticated user.
const codexDaemonPubkeys = new Map();   // agentId -> { pubkey, crypto_versions, registered_at }
const codexRelayTickets = new Map();    // ticket -> { agentId, threadId, expires, used }
const CODEX_RELAY_TICKET_TTL_MS = 60 * 1000; // 60s; browser must connect immediately

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

async function handleCodexPairInit(req, res) {
  let body = {};
  try { body = (await readBody(req)) || {}; } catch {}
  const code = generateCodexPairingCode();
  const pairingId = randomUUID();
  const expires = Date.now() + CODEX_PAIR_EXPIRY_MS;
  codexPairings[pairingId] = {
    code,
    status: "pending",
    expires,
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
  json(res, 200, {
    code,
    pairing_id: pairingId,
    web_url: ISSUER_URL + "/pair",
    expires_at: new Date(expires).toISOString(),
  });
}

function handleCodexPairStatus(req, res, pairingId) {
  const p = codexPairings[pairingId];
  if (!p) { json(res, 404, { error: "pairing not found" }); return; }
  if (p.status === "pending" && Date.now() > p.expires) {
    p.status = "expired";
    if (codexPairingByCode[p.code] === pairingId) delete codexPairingByCode[p.code];
  }
  if (p.status === "completed") {
    json(res, 200, { status: "completed", api_key: p.apiKey, handle: p.agentId });
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
  const pairingId = codexPairingByCode[code];
  if (!pairingId) { json(res, 404, { error: "invalid or already-used code" }); return; }
  const p = codexPairings[pairingId];
  if (!p || p.status !== "pending" || Date.now() > p.expires) {
    json(res, 410, { error: "code expired or already used" });
    return;
  }
  p.status = "completed";
  p.apiKey = identity.apiKey;
  p.agentId = identity.agentId;
  // Phase 2.5: register the daemon's E2EE public key against the
  // authenticated handle. Replaces any previous key for this handle
  // (rotate-key implicitly happens here on a re-pair).
  if (p.daemon_public_key) {
    codexDaemonPubkeys.set(identity.agentId, {
      pubkey: p.daemon_public_key,
      crypto_versions: p.crypto_versions && p.crypto_versions.length ? p.crypto_versions : ["e2ee-v1"],
      registered_at: new Date().toISOString(),
    });
    console.log("codex-relay: registered E2EE pubkey for " + identity.agentId);
  }
  delete codexPairingByCode[code];
  console.log("codex-relay: paired daemon for " + identity.agentId);
  json(res, 200, { ok: true, handle: identity.agentId });
}

function handleCodexRelayState(req, res) {
  const identity = authenticate(req);
  if (!identity) { json(res, 401, { error: "Unauthorized" }); return; }
  json(res, 200, {
    handle: identity.agentId,
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
  const daemonKey = codexDaemonPubkeys.get(identity.agentId) || null;
  json(res, 200, {
    handle: identity.agentId,
    thread_id: threadId,
    daemon_online: daemonOnline,
    daemon_public_key: daemonKey ? daemonKey.pubkey : null,
    daemon_crypto_versions: daemonKey ? daemonKey.crypto_versions : null,
    supported_crypto_versions: ["e2ee-v1"],
    e2ee_available: !!daemonKey,
  });
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
  return { agentId: entry.agentId };
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

function authenticateWs(req) {
  const auth = req.headers["authorization"];
  if (auth && auth.startsWith("Bearer ")) {
    const key = auth.slice(7).trim();
    if (API_KEYS[key]) return { agentId: API_KEYS[key], apiKey: key };
  }
  // Browsers can't set Authorization on WebSocket(): accept ?token= fallback.
  const u = parseUrl(req.url);
  const qs = u.query ? parseUrlQs(u.query) : {};
  const tokenParam = Array.isArray(qs.token) ? qs.token[0] : qs.token;
  if (typeof tokenParam === "string" && API_KEYS[tokenParam]) {
    return { agentId: API_KEYS[tokenParam], apiKey: tokenParam };
  }
  return null;
}

const codexRelayWss = new WebSocketServer({ noServer: true });

httpServer.on("upgrade", (req, socket, head) => {
  const u = parseUrl(req.url);
  const path = u.pathname || "";
  const isDaemon = path === "/api/codex-relay/daemon";
  const isWeb = path.startsWith("/api/codex-relay/web/");
  if (!isDaemon && !isWeb) return; // let other listeners (or default) handle it

  // Daemon side keeps the existing Bearer ck- token auth.
  // Web side: prefer single-use ?ticket= bound to the route; fall back
  // to ?token=ck- for back-compat with the pre-2.5 alpha.
  let identity = null;
  if (isDaemon) {
    identity = authenticateWs(req);
  } else {
    const threadId = decodeURIComponent(path.slice("/api/codex-relay/web/".length));
    const qs = u.query ? parseUrlQs(u.query) : {};
    const ticketParam = Array.isArray(qs.ticket) ? qs.ticket[0] : qs.ticket;
    if (typeof ticketParam === "string" && ticketParam) {
      const consumed = consumeCodexRelayTicket(ticketParam, threadId);
      if (consumed) identity = { agentId: consumed.agentId, viaTicket: true };
    }
    if (!identity) identity = authenticateWs(req);
  }

  if (!identity) {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
    return;
  }

  if (isDaemon) {
    codexRelayWss.handleUpgrade(req, socket, head, (ws) => {
      const previous = codexDaemons.get(identity.agentId);
      if (previous && previous !== ws) try { previous.close(4000, "replaced"); } catch {}
      codexDaemons.set(identity.agentId, ws);
      console.log("codex-relay: daemon online for " + identity.agentId);
      ws.on("message", (data) => {
        const text = data.toString();
        const prefix = identity.agentId + ":";
        for (const [key, webWs] of codexWebClients) {
          if (key.startsWith(prefix) && webWs.readyState === webWs.OPEN) {
            webWs.send(text);
          }
        }
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
  codexRelayWss.handleUpgrade(req, socket, head, (ws) => {
    const key = identity.agentId + ":" + threadId;
    const previous = codexWebClients.get(key);
    if (previous && previous !== ws) try { previous.close(4000, "replaced"); } catch {}
    codexWebClients.set(key, ws);
    console.log("codex-relay: web online " + key);
    ws.on("message", (data) => {
      const daemonWs = codexDaemons.get(identity.agentId);
      if (daemonWs && daemonWs.readyState === daemonWs.OPEN) {
        daemonWs.send(data.toString());
      } else {
        try { ws.send(JSON.stringify({ type: "error", message: "daemon offline" })); } catch {}
      }
    });
    ws.on("close", () => {
      if (codexWebClients.get(key) === ws) codexWebClients.delete(key);
    });
    ws.on("error", (err) => {
      console.error("codex-relay web ws error:", err.message);
    });
  });
});

httpServer.listen(PORT, SERVER_BIND, () => {
  console.log(SERVER_NAME + " v" + SERVER_VERSION + " listening on " + SERVER_BIND + ":" + PORT);
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
