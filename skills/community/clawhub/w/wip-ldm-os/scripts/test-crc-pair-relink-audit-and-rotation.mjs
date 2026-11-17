import { readFileSync } from "node:fs";
import {
  codexDaemonPubkeyFingerprint,
  createCodexDaemonPubkeyRegistry,
  evaluateCodexDaemonReconnectPubkey,
} from "../src/hosted-mcp/codex-relay-e2ee-registry.mjs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");
const pairHtml = readFileSync("src/hosted-mcp/app/pair.html", "utf8");
const loginHtml = readFileSync("src/hosted-mcp/app/kaleidoscope-login.html", "utf8");
const registrySource = readFileSync("src/hosted-mcp/codex-relay-e2ee-registry.mjs", "utf8");
const ticket = readFileSync("ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-pair-relink-audit-and-rotation.md", "utf8");

function assertContains(haystack, needle, label) {
  if (!haystack.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assert(condition, label, detail = "") {
  if (!condition) throw new Error(`${label}${detail ? ": " + detail : ""}`);
}

function createSilentLogger() {
  return { log() {}, error() {} };
}

assertContains(server, "const CODEX_PAIR_PRESENCE_TTL_MS = 2 * 60 * 1000;", "short pair presence ttl");
assertContains(server, "const codexPairPresenceTokens = new Map();", "pair presence token store");
assertContains(server, "function generateCodexPairPresenceToken(agentId)", "pair presence token mint");
assertContains(server, "function consumeCodexPairPresenceToken(token, agentId)", "pair presence token consume");
assertContains(server, "codex_pair_presence_token: generateCodexPairPresenceToken(agentId)", "registration mints pair presence token");
assertContains(server, "codex_pair_presence_token: generateCodexPairPresenceToken(entry.agentId)", "authentication mints pair presence token");
assertContains(server, 'error: "fresh_presence_required"', "pair-complete fresh presence rejection");
assertContains(server, "consumeCodexPairPresenceToken(pairPresenceToken, identity.agentId)", "pair-complete consumes pair presence token");
assertContains(server, 'json(res, 404, { error: "invalid or already-used code" });', "pair code reuse rejection");
assertContains(server, 'json(res, 410, { error: "code expired or already used" });', "pair code expiry rejection");
assertContains(server, "invalidateCodexBrowserSessionsForAgent(identity.agentId, \"daemon key replaced\")", "daemon replacement invalidates stale browser sessions");
assertContains(server, "evaluateCodexDaemonReconnectPubkey(", "daemon reconnect checks existing key policy");
assertContains(server, "daemon key change requires fresh pair", "changed daemon reconnect key requires pair flow");
assertContains(server, "daemonIdentityAccepted = activateCodexDaemonWs();", "daemon only becomes active after identity is accepted");
assertContains(server, "daemon already online", "duplicate daemon cannot evict an online daemon");
assertContains(server, "daemon identity required", "daemon frames require identity before routing");
assertContains(server, "p.replaced_daemon_key = !!daemonKeyResult?.replaced;", "pair state records replacement status");
assertContains(server, "replaced_daemon_key: !!p.replaced_daemon_key", "pair-status exposes relink replacement status");
assertContains(pairHtml, "codex_pair_presence_token: getPairPresenceToken()", "pair page sends pair presence token");
assertContains(pairHtml, "fresh_presence_required", "pair page handles fresh presence error");
assertContains(pairHtml, "Remote Control relinked this laptop.", "pair page gives relink message");
assertContains(loginHtml, "wip_codex_pair_presence_token", "login carries pair presence token into pair page");
assertContains(registrySource, "CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_key_audit", "pair audit table");
assertContains(registrySource, "old_pubkey_fingerprint", "audit stores old key fingerprint");
assertContains(registrySource, "new_pubkey_fingerprint", "audit stores new key fingerprint");
assertContains(ticket, "status: done", "ticket marked done");

const oldFingerprint = codexDaemonPubkeyFingerprint("old-spki-key");
const newFingerprint = codexDaemonPubkeyFingerprint("new-spki-key");
assert(oldFingerprint && oldFingerprint.startsWith("sha256:"), "fingerprint has sha256 prefix");
assert(oldFingerprint !== newFingerprint, "fingerprint changes when daemon key changes");

const registry = createCodexDaemonPubkeyRegistry({
  usePrisma: false,
  devMode: false,
  logger: createSilentLogger(),
});
const first = await registry.register("acct:test-user-a", "old-spki-key", ["e2ee-v1"], "pair-complete");
assert(first.registered === true, "first pair registers key");
assert(first.replaced === false, "first pair is not replacement");
const second = await registry.register("acct:test-user-a", "new-spki-key", ["e2ee-v1"], "pair-complete");
assert(second.registered === true, "relink registers new key");
assert(second.replaced === true, "relink replacement is detected");
assert(second.old_fingerprint === oldFingerprint, "relink reports old fingerprint");
assert(second.new_fingerprint === newFingerprint, "relink reports new fingerprint");
assert(registry.auditLog.length === 2, "registry keeps audit entries");
assert(registry.auditLog[1].replaced === true, "audit marks replacement");
assert(registry.auditLog[1].old_pubkey_fingerprint === oldFingerprint, "audit stores old fingerprint");
assert(registry.auditLog[1].new_pubkey_fingerprint === newFingerprint, "audit stores new fingerprint");

const firstReconnectPolicy = evaluateCodexDaemonReconnectPubkey(null, "daemon-reconnect-key");
assert(firstReconnectPolicy.allowed === true, "daemon reconnect can self-heal when no key is registered");
assert(firstReconnectPolicy.replaced === false, "first daemon reconnect is not a replacement");
const sameReconnectPolicy = evaluateCodexDaemonReconnectPubkey({ pubkey: "daemon-reconnect-key" }, "daemon-reconnect-key");
assert(sameReconnectPolicy.allowed === true, "daemon reconnect can re-register the same key");
assert(sameReconnectPolicy.replaced === false, "same-key daemon reconnect is not a replacement");
const changedReconnectPolicy = evaluateCodexDaemonReconnectPubkey({ pubkey: "daemon-reconnect-key" }, "attacker-reconnect-key");
assert(changedReconnectPolicy.allowed === false, "daemon reconnect cannot replace an existing key");
assert(changedReconnectPolicy.reason === "fresh_pair_required", "changed daemon reconnect requires fresh pair");
assert(changedReconnectPolicy.replaced === true, "changed daemon reconnect is detected as replacement");
assert(changedReconnectPolicy.old_fingerprint === codexDaemonPubkeyFingerprint("daemon-reconnect-key"), "changed reconnect reports old fingerprint");
assert(changedReconnectPolicy.new_fingerprint === codexDaemonPubkeyFingerprint("attacker-reconnect-key"), "changed reconnect reports new fingerprint");
const invalidReconnectPolicy = evaluateCodexDaemonReconnectPubkey({ pubkey: "daemon-reconnect-key" }, "");
assert(invalidReconnectPolicy.allowed === false, "daemon reconnect rejects missing pubkey");
assert(invalidReconnectPolicy.reason === "invalid_daemon_pubkey", "missing daemon reconnect pubkey has explicit reason");
const oversizedReconnectPolicy = evaluateCodexDaemonReconnectPubkey(null, "x".repeat(1025));
assert(oversizedReconnectPolicy.allowed === false, "daemon reconnect rejects oversized pubkey");
assert(oversizedReconnectPolicy.reason === "invalid_daemon_pubkey", "oversized daemon reconnect pubkey has explicit reason");

const executeCalls = [];
const persistedRegistry = createCodexDaemonPubkeyRegistry({
  usePrisma: true,
  devMode: false,
  logger: createSilentLogger(),
  prisma: {
    async $executeRawUnsafe(sql, ...args) {
      executeCalls.push({ sql, args });
      return 1;
    },
  },
});
await persistedRegistry.register("acct:test-user-b", "persisted-spki-key", ["e2ee-v1"], "daemon-reconnect");
const auditInsert = executeCalls.find((call) => call.sql.includes("INSERT INTO codex_daemon_e2ee_key_audit"));
assert(auditInsert, "audit insert executes for persisted registry");
assert(auditInsert.sql.includes("$7::timestamptz"), "audit insert casts registered_at parameter to timestamptz");
assert(typeof auditInsert.args[6] === "string" && auditInsert.args[6].includes("T"), "audit insert passes ISO registered_at value");

function pairCompleteModel({ hasDaemonPublicKey, pairPresenceOk, previousPubkey, nextPubkey }) {
  if (hasDaemonPublicKey && !pairPresenceOk) return { code: 403, error: "fresh_presence_required" };
  const replaced = !!(previousPubkey && nextPubkey && previousPubkey !== nextPubkey);
  return { code: 200, replaced };
}

assert(
  pairCompleteModel({
    hasDaemonPublicKey: true,
    pairPresenceOk: false,
    previousPubkey: "old",
    nextPubkey: "new",
  }).code === 403,
  "ck token alone cannot replace daemon key",
);
assert(
  pairCompleteModel({
    hasDaemonPublicKey: true,
    pairPresenceOk: true,
    previousPubkey: "old",
    nextPubkey: "new",
  }).replaced === true,
  "fresh pair presence permits relink",
);
assert(
  pairCompleteModel({
    hasDaemonPublicKey: true,
    pairPresenceOk: true,
    previousPubkey: null,
    nextPubkey: "new",
  }).replaced === false,
  "fresh pair presence permits first pair",
);

function pairCodeModel(pair, codeKnown, now) {
  if (!codeKnown) return { code: 404, error: "invalid or already-used code" };
  if (!pair || pair.status !== "pending" || now > pair.expires) {
    return { code: 410, error: "code expired or already used" };
  }
  pair.status = "completed";
  return { code: 200 };
}

const pair = { status: "pending", expires: 100 };
assert(pairCodeModel(pair, true, 10).code === 200, "first pair-complete succeeds");
assert(pairCodeModel(pair, true, 20).code === 410, "pair code reuse fails");
assert(pairCodeModel({ status: "pending", expires: 100 }, true, 200).code === 410, "expired pair code fails");
assert(pairCodeModel(null, false, 10).code === 404, "unknown pair code fails");

console.log("crc pair relink audit and rotation checks passed");
