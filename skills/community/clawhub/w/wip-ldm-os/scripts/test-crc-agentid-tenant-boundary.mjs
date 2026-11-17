import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");

function assertContains(needle, label) {
  if (!server.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertNotContains(needle, label) {
  if (server.includes(needle)) {
    throw new Error(`${label} still contains forbidden text: ${needle}`);
  }
}

assertContains('const ACCOUNT_TENANT_PREFIX = "acct:";', "account tenant prefix");
assertContains('const LEGACY_API_KEY_TENANT_PREFIX = "key:";', "legacy key tenant prefix");
assertContains('function accountTenantIdForUserId(userId)', "account tenant helper");
assertContains('function identityForApiKey(key)', "api key identity helper");
assertContains('return identityForApiKey(key);', "http auth uses identity helper");
assertContains("const agentId = accountTenantIdForUserId(stored.userId);", "registration uses immutable account tenant");
assertContains("function sanitizeDisplayLabel(raw)", "display label sanitizer");
assertContains('replace(/[\\u0000-\\u001f\\u007f]/g, "").replace(/\\s+/g, " ").trim().slice(0, 64)', "display label sanitizer preserves label semantics");
assertContains("const displayLabel = sanitizeDisplayLabel(body?.displayName || body?.username);", "registration treats entered name as display label");
assertContains("displayLabel,", "registration challenge stores display label");
assertContains("await saveApiKey(apiKey, agentId, { handle: credentialLabel });", "registration stores handle separately");
assertContains("p.handle = identity.handle;", "pair stores display handle separately");
assertContains("handle: identity.handle,", "relay metadata returns display handle");
assertContains("codexDaemons.has(identity.agentId)", "daemon presence uses tenant id");
assertContains("codexDaemonPubkeyRegistry.get(identity.agentId)", "daemon pubkey uses tenant id");
assertContains("agentId: identity.agentId,", "relay tickets bind tenant id");
assertContains("handle: identity.handle,", "relay tickets preserve display handle");
assertContains("codexDaemons.set(identity.agentId, ws);", "daemon ws keyed by tenant id");
assertContains("const webKey = codexRelayKey(identity.agentId, threadId);", "web ws keyed by tenant id");
assertContains("const daemonWs = codexDaemons.get(identity.agentId);", "web sends to tenant daemon");
assertNotContains("const agentId = stored.username || (\"passkey-\"", "registration must not use chosen handle as tenant");
assertNotContains("const existingKey = Object.entries(API_KEYS).find(([k, v]) => v === agentId);", "oauth must not reuse chosen handle as tenant");
assertNotContains("function isUsernameTaken", "display labels must not be globally unique usernames");
assertNotContains("function sanitizeUsername", "display labels must not be modeled as usernames");
assertNotContains('json(res, 409, { error: "reserved_handle"', "display labels must not be blocked as reserved security handles");
assertNotContains('json(res, 409, { error: "handle_taken"', "duplicate display labels must be allowed");

function legacyTenantIdForApiKey(key) {
  return "key:" + createHash("sha256").update(key).digest("base64url").slice(0, 32);
}

function accountTenantIdForUserId(userId) {
  return "acct:" + userId;
}

const chosenHandle = "parker-smoke-test";
const sharedDisplayLabel = "Parker";
const accountA = accountTenantIdForUserId("user-a");
const accountB = accountTenantIdForUserId("user-b");
const threadId = "thread-019dfa";
if (accountA === accountB) {
  throw new Error("different user ids collapsed to one account tenant");
}
if (`${sharedDisplayLabel}:${threadId}` === `${accountA}:${threadId}` || `${sharedDisplayLabel}:${threadId}` === `${accountB}:${threadId}`) {
  throw new Error("display label was used as a relay route key");
}

const legacyA = legacyTenantIdForApiKey("ck-a");
const legacyB = legacyTenantIdForApiKey("ck-b");
if (legacyA === legacyB) {
  throw new Error("legacy API-key tenants collided");
}

const webKeyA = `${accountA}:${threadId}`;
const webKeyB = `${accountB}:${threadId}`;
if (webKeyA === webKeyB) {
  throw new Error("same display handle can still collide across account tenants");
}
if (`${chosenHandle}:${threadId}` === webKeyA || `${chosenHandle}:${threadId}` === webKeyB) {
  throw new Error("model still keys relay routes by display handle");
}

console.log("crc agentId tenant boundary checks passed");
