import { createHash, randomUUID } from "node:crypto";

export function normalizeCodexCryptoVersions(versions) {
  const out = Array.isArray(versions)
    ? versions.filter((v) => typeof v === "string" && v.length > 0 && v.length <= 32).slice(0, 8)
    : [];
  return out.length ? out : ["e2ee-v1"];
}

export function codexDaemonPubkeyFingerprint(pubkey) {
  if (typeof pubkey !== "string" || !pubkey) return null;
  return "sha256:" + createHash("sha256").update(pubkey).digest("base64url").slice(0, 16);
}

export function evaluateCodexDaemonReconnectPubkey(existingKey, incomingPubkey) {
  const existingPubkey = typeof existingKey?.pubkey === "string" && existingKey.pubkey ? existingKey.pubkey : null;
  const nextPubkey = typeof incomingPubkey === "string" && incomingPubkey && incomingPubkey.length <= 1024 ? incomingPubkey : null;
  const oldFingerprint = codexDaemonPubkeyFingerprint(existingPubkey);
  const newFingerprint = codexDaemonPubkeyFingerprint(nextPubkey);

  if (!nextPubkey) {
    return {
      allowed: false,
      reason: "invalid_daemon_pubkey",
      replaced: false,
      old_fingerprint: oldFingerprint,
      new_fingerprint: newFingerprint,
    };
  }
  if (!existingPubkey || existingPubkey === nextPubkey) {
    return {
      allowed: true,
      reason: null,
      replaced: false,
      old_fingerprint: oldFingerprint,
      new_fingerprint: newFingerprint,
    };
  }
  return {
    allowed: false,
    reason: "fresh_pair_required",
    replaced: true,
    old_fingerprint: oldFingerprint,
    new_fingerprint: newFingerprint,
  };
}

export function buildCodexBootstrapPayload({ identity, threadId, daemonOnline, daemonKey }) {
  return {
    handle: identity.handle,
    thread_id: threadId,
    daemon_online: daemonOnline,
    daemon_public_key: daemonKey ? daemonKey.pubkey : null,
    daemon_crypto_versions: daemonKey ? daemonKey.crypto_versions : null,
    supported_crypto_versions: ["e2ee-v1"],
    e2ee_available: !!daemonKey,
  };
}

export function createCodexDaemonPubkeyRegistry({
  usePrisma,
  prisma,
  devMode = false,
  logger = console,
} = {}) {
  const pubkeys = new Map();
  const auditLog = [];

  async function ensureStore() {
    if (!usePrisma) return;
    await prisma.$executeRawUnsafe(`
      CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_keys (
        tenant_id TEXT PRIMARY KEY,
        pubkey TEXT NOT NULL,
        crypto_versions_json TEXT NOT NULL,
        registered_at TIMESTAMPTZ NOT NULL DEFAULT now()
      )
    `);
  }

  async function ensureAuditStore() {
    if (!usePrisma) return;
    await prisma.$executeRawUnsafe(`
      CREATE TABLE IF NOT EXISTS codex_daemon_e2ee_key_audit (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        source TEXT NOT NULL,
        old_pubkey_fingerprint TEXT,
        new_pubkey_fingerprint TEXT,
        replaced BOOLEAN NOT NULL,
        registered_at TIMESTAMPTZ NOT NULL DEFAULT now()
      )
    `);
  }

  async function loadFromDb() {
    if (!usePrisma) return;
    try {
      await ensureStore();
      const rows = await prisma.$queryRawUnsafe(`
        SELECT tenant_id, pubkey, crypto_versions_json, registered_at
        FROM codex_daemon_e2ee_keys
      `);
      for (const row of rows) {
        let cryptoVersions = ["e2ee-v1"];
        try { cryptoVersions = normalizeCodexCryptoVersions(JSON.parse(row.crypto_versions_json)); } catch {}
        pubkeys.set(row.tenant_id, {
          pubkey: row.pubkey,
          crypto_versions: cryptoVersions,
          registered_at: row.registered_at instanceof Date ? row.registered_at.toISOString() : String(row.registered_at),
        });
      }
      logger.log("codex-relay: loaded " + rows.length + " persisted E2EE daemon pubkey(s)");
    } catch (err) {
      logger.error("codex-relay: failed to load persisted E2EE daemon pubkeys:", err.message);
      if (!devMode) process.exit(1);
    }
  }

  async function persist(agentId, pubkey, cryptoVersions) {
    if (!usePrisma) return;
    await ensureStore();
    await prisma.$executeRawUnsafe(
      `INSERT INTO codex_daemon_e2ee_keys
        (tenant_id, pubkey, crypto_versions_json, registered_at)
       VALUES ($1, $2, $3, now())
       ON CONFLICT (tenant_id)
       DO UPDATE SET
        pubkey = EXCLUDED.pubkey,
        crypto_versions_json = EXCLUDED.crypto_versions_json,
        registered_at = EXCLUDED.registered_at`,
      agentId,
      pubkey,
      JSON.stringify(cryptoVersions),
    );
  }

  async function recordAudit(agentId, previousPubkey, nextPubkey, source, registeredAt) {
    const oldFingerprint = codexDaemonPubkeyFingerprint(previousPubkey);
    const newFingerprint = codexDaemonPubkeyFingerprint(nextPubkey);
    const replaced = !!(previousPubkey && previousPubkey !== nextPubkey);
    const entry = {
      tenant_id: agentId,
      source,
      old_pubkey_fingerprint: oldFingerprint,
      new_pubkey_fingerprint: newFingerprint,
      replaced,
      registered_at: registeredAt,
    };
    auditLog.push(entry);
    if (!usePrisma) return;
    await ensureAuditStore();
    await prisma.$executeRawUnsafe(
      `INSERT INTO codex_daemon_e2ee_key_audit
        (id, tenant_id, source, old_pubkey_fingerprint, new_pubkey_fingerprint, replaced, registered_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7::timestamptz)`,
      randomUUID(),
      agentId,
      source,
      oldFingerprint,
      newFingerprint,
      replaced,
      registeredAt,
    );
  }

  function register(agentId, pubkey, cryptoVersions, source) {
    if (typeof agentId !== "string" || !agentId) return Promise.resolve(false);
    if (typeof pubkey !== "string" || !pubkey || pubkey.length > 1024) return Promise.resolve(false);
    const previous = pubkeys.get(agentId) || null;
    const normalizedVersions = normalizeCodexCryptoVersions(cryptoVersions);
    const registeredAt = new Date().toISOString();
    pubkeys.set(agentId, {
      pubkey,
      crypto_versions: normalizedVersions,
      registered_at: registeredAt,
    });
    logger.log("codex-relay: registered E2EE pubkey for " + agentId + " via " + source);
    return persist(agentId, pubkey, normalizedVersions)
      .then(() => recordAudit(agentId, previous?.pubkey || null, pubkey, source, registeredAt))
      .then(() => ({
        registered: true,
        replaced: !!(previous?.pubkey && previous.pubkey !== pubkey),
        old_fingerprint: codexDaemonPubkeyFingerprint(previous?.pubkey || null),
        new_fingerprint: codexDaemonPubkeyFingerprint(pubkey),
      }))
      .catch((err) => {
        logger.error("codex-relay: failed to persist E2EE pubkey for " + agentId + ":", err.message);
        if (!devMode) throw err;
        return false;
      });
  }

  return {
    pubkeys,
    auditLog,
    ensureStore,
    ensureAuditStore,
    loadFromDb,
    register,
    get(agentId) {
      return pubkeys.get(agentId) || null;
    },
    clearMemoryForTest() {
      pubkeys.clear();
    },
  };
}
