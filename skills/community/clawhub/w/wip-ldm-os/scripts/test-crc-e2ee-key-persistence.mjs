import { readFileSync } from "node:fs";
import {
  buildCodexBootstrapPayload,
  createCodexDaemonPubkeyRegistry,
} from "../src/hosted-mcp/codex-relay-e2ee-registry.mjs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");
const registrySource = readFileSync("src/hosted-mcp/codex-relay-e2ee-registry.mjs", "utf8");
const deployScript = readFileSync("src/hosted-mcp/deploy.sh", "utf8");

function assertContains(haystack, needle, label) {
  if (!haystack.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertBefore(haystack, first, second, label) {
  const firstIndex = haystack.indexOf(first);
  const secondIndex = haystack.indexOf(second);
  if (firstIndex === -1 || secondIndex === -1 || firstIndex >= secondIndex) {
    throw new Error(`${label} expected "${first}" before "${second}"`);
  }
}

function assert(condition, label, detail = "") {
  if (!condition) throw new Error(`${label}${detail ? ": " + detail : ""}`);
}

function bootstrapPayloadFor(registry, identity, threadId, daemonOnline = true) {
  return buildCodexBootstrapPayload({
    identity,
    threadId,
    daemonOnline,
    daemonKey: registry.get(identity.agentId),
  });
}

function createFakePrisma() {
  const rows = new Map();
  return {
    rows,
    async $executeRawUnsafe(sql, tenantId, pubkey, cryptoVersionsJson) {
      if (/CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_keys/.test(sql)) return;
      if (/CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_key_audit/.test(sql)) return;
      if (/INSERT INTO codex_daemon_e2ee_keys/.test(sql)) {
        rows.set(tenantId, {
          tenant_id: tenantId,
          pubkey,
          crypto_versions_json: cryptoVersionsJson,
          registered_at: new Date("2026-05-11T17:37:18.000Z"),
        });
        return;
      }
      if (/INSERT INTO codex_daemon_e2ee_key_audit/.test(sql)) return;
      throw new Error("unexpected fake prisma execute: " + sql);
    },
    async $queryRawUnsafe(sql) {
      if (/FROM codex_daemon_e2ee_keys/.test(sql)) return [...rows.values()];
      throw new Error("unexpected fake prisma query: " + sql);
    },
  };
}

function createSilentLogger() {
  return { log() {}, error() {} };
}

assertContains(registrySource, "CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_keys", "persistent key table");
assertContains(registrySource, "async function loadFromDb()", "boot load helper");
assertContains(registrySource, "async function persist(agentId, pubkey, cryptoVersions)", "persist helper");
assertContains(registrySource, "function register(agentId, pubkey, cryptoVersions, source)", "registration helper");
assertContains(registrySource, "pubkeys.set(agentId, {", "registration updates in-memory bootstrap cache");
assertContains(registrySource, "return persist(agentId, pubkey, normalizedVersions)", "registration persists after cache update");
assertContains(server, "await codexDaemonPubkeyRegistry.loadFromDb();", "server boot load call");
assertContains(server, "await codexDaemonPubkeyRegistry.register(identity.agentId, p.daemon_public_key, p.crypto_versions, \"pair-complete\");", "pair-complete persists key");
assertContains(server, "if (envelope?.type === \"daemon.identity\") {", "daemon reconnect identity frame");
assertContains(server, "codexDaemonPubkeyRegistry.register(", "daemon reconnect register call");
assertContains(server, "buildCodexBootstrapPayload({ identity, threadId, daemonOnline, daemonKey })", "bootstrap uses shared payload builder");
assertContains(deployScript, "codex-relay-e2ee-registry.mjs", "hosted deploy copies registry module");
assertBefore(
  server,
  "await codexDaemonPubkeyRegistry.loadFromDb();",
  "function handleCodexBootstrap(req, res, threadId)",
  "persisted keys load before bootstrap handler",
);

const identity = {
  agentId: "acct:test-user-a",
  tenantId: "acct:test-user-a",
  handle: "Parker smoke test",
  apiKey: "ck-test",
};
const threadId = "019dfa1e-0c3d-7f01-86b9-9a22cd452bde";

const fakePrisma = createFakePrisma();
const registryBeforeRestart = createCodexDaemonPubkeyRegistry({
  usePrisma: true,
  prisma: fakePrisma,
  devMode: false,
  logger: createSilentLogger(),
});
await registryBeforeRestart.register(identity.agentId, "spki-key-before-restart", ["e2ee-v1"], "pair-complete");

const beforeRestartBootstrap = bootstrapPayloadFor(registryBeforeRestart, identity, threadId);
assert(beforeRestartBootstrap.e2ee_available === true, "bootstrap reports e2ee before restart");
assert(beforeRestartBootstrap.daemon_public_key === "spki-key-before-restart", "bootstrap returns registered daemon key before restart");

const registryAfterRestart = createCodexDaemonPubkeyRegistry({
  usePrisma: true,
  prisma: fakePrisma,
  devMode: false,
  logger: createSilentLogger(),
});
await registryAfterRestart.loadFromDb();

const afterRestartBootstrap = bootstrapPayloadFor(registryAfterRestart, identity, threadId);
assert(afterRestartBootstrap.e2ee_available === true, "bootstrap reports e2ee after restart from persisted key");
assert(afterRestartBootstrap.daemon_public_key === "spki-key-before-restart", "bootstrap restores persisted daemon key after restart");
assert(afterRestartBootstrap.daemon_crypto_versions?.[0] === "e2ee-v1", "bootstrap restores crypto versions after restart");

const emptyFakePrisma = createFakePrisma();
const registryBeforeReconnect = createCodexDaemonPubkeyRegistry({
  usePrisma: true,
  prisma: emptyFakePrisma,
  devMode: false,
  logger: createSilentLogger(),
});
await registryBeforeReconnect.loadFromDb();
const beforeReconnectBootstrap = bootstrapPayloadFor(registryBeforeReconnect, identity, threadId);
assert(beforeReconnectBootstrap.e2ee_available === false, "bootstrap is not e2ee available before daemon reconnect when no key exists");
assert(beforeReconnectBootstrap.daemon_public_key === null, "bootstrap has no daemon key before daemon reconnect");

await registryBeforeReconnect.register(identity.agentId, "spki-key-from-daemon-reconnect", [], "daemon-reconnect");
const afterReconnectBootstrap = bootstrapPayloadFor(registryBeforeReconnect, identity, threadId);
assert(afterReconnectBootstrap.e2ee_available === true, "bootstrap reports e2ee after daemon reconnect self-heal");
assert(afterReconnectBootstrap.daemon_public_key === "spki-key-from-daemon-reconnect", "bootstrap returns daemon reconnect key");
assert(afterReconnectBootstrap.daemon_crypto_versions?.[0] === "e2ee-v1", "daemon reconnect defaults crypto version");

const registryAfterReconnectRestart = createCodexDaemonPubkeyRegistry({
  usePrisma: true,
  prisma: emptyFakePrisma,
  devMode: false,
  logger: createSilentLogger(),
});
await registryAfterReconnectRestart.loadFromDb();
const afterReconnectRestartBootstrap = bootstrapPayloadFor(registryAfterReconnectRestart, identity, threadId);
assert(afterReconnectRestartBootstrap.e2ee_available === true, "daemon reconnect key is persisted for the next restart");
assert(afterReconnectRestartBootstrap.daemon_public_key === "spki-key-from-daemon-reconnect", "daemon reconnect key survives restart");

console.log("crc e2ee key persistence restart regression checks passed");
