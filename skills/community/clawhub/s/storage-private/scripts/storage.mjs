#!/usr/bin/env node
/**
 * 🔐 Storage Private — Encrypted Multi-Node Agent Storage
 * 
 * Zero-dependency Node.js CLI for encrypted agent data storage.
 * Replicates across diverse backends: memory stores, FilStream CDN, local disk.
 * Client-side ChaCha20-Poly1305 encryption — data is ciphertext before it leaves.
 * 
 * Usage:
 *   node storage.mjs put <key> [--data "..."] [--file path] [--namespace ns] [--anchor]
 *   node storage.mjs get <key> [--namespace ns] [--version N] [--output path]
 *   node storage.mjs list [--namespace ns] [--prefix "..."]
 *   node storage.mjs delete <key> [--namespace ns]
 *   node storage.mjs status
 *   node storage.mjs sync [--namespace ns]         — ensure all nodes have all data
 * 
 * Environment:
 *   STORAGE_PRIVATE_KEY    — Hex key or ETH private key for KEK derivation
 *   STORAGE_NAMESPACE      — Default namespace (default: "default")
 * 
 * Created: 2026-03-03
 * Author: Rick 🦞 (Cortex Protocol)
 */

import { createCipheriv, createDecipheriv, randomBytes, createHash, hkdfSync } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { resolve, basename, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

// ── Paths ──
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_DIR = resolve(__dirname, '..');
const CONFIG_PATH = resolve(SKILL_DIR, 'config.json');
const LOCAL_INDEX_DIR = resolve(homedir(), '.openclaw', 'workspace', '.storage-private');
const SECRETS_DIR = resolve(homedir(), '.openclaw', 'workspace', '.secrets');
const DEFAULT_NAMESPACE = process.env.STORAGE_NAMESPACE || 'default';

// ── Load Config ──
function loadConfig() {
  if (existsSync(CONFIG_PATH)) {
    return JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
  }
  // Fallback: single-node config
  return {
    version: 1,
    replication: { min_replicas: 1, write_quorum: 1, read_strategy: 'first-success' },
    nodes: [{
      id: 'default',
      type: 'memory-store',
      url: 'http://[2a05:a00:2::10:11]:8081',
      location: 'Default',
      priority: 1,
      enabled: true,
    }],
  };
}

const CONFIG = loadConfig();
const ENABLED_NODES = CONFIG.nodes.filter(n => n.enabled).sort((a, b) => a.priority - b.priority);

// ── Crypto Layer ──

function deriveKEK(secretHex) {
  const secret = Buffer.from(secretHex.replace(/^0x/, ''), 'hex');
  const salt = Buffer.from('cortex-storage-private-v1', 'utf8');
  const info = Buffer.from('storage-private-kek', 'utf8');
  return Buffer.from(hkdfSync('sha256', secret, salt, info, 32));
}

function encrypt(plaintext, kek) {
  const dek = randomBytes(32);
  const nonce = randomBytes(12);
  const cipher = createCipheriv('chacha20-poly1305', dek, nonce, { authTagLength: 16 });
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  const dekNonce = randomBytes(12);
  const dekCipher = createCipheriv('chacha20-poly1305', kek, dekNonce, { authTagLength: 16 });
  const wrappedDek = Buffer.concat([dekCipher.update(dek), dekCipher.final()]);
  const dekTag = dekCipher.getAuthTag();
  return {
    version: 1, algorithm: 'chacha20-poly1305',
    nonce: nonce.toString('hex'), ciphertext: encrypted.toString('hex'),
    tag: tag.toString('hex'), wrappedDek: wrappedDek.toString('hex'),
    dekNonce: dekNonce.toString('hex'), dekTag: dekTag.toString('hex'),
  };
}

function decrypt(envelope, kek) {
  if (envelope.version !== 1) throw new Error(`Unsupported envelope version: ${envelope.version}`);
  const dekDecipher = createDecipheriv('chacha20-poly1305', kek,
    Buffer.from(envelope.dekNonce, 'hex'), { authTagLength: 16 });
  dekDecipher.setAuthTag(Buffer.from(envelope.dekTag, 'hex'));
  const dek = Buffer.concat([dekDecipher.update(Buffer.from(envelope.wrappedDek, 'hex')), dekDecipher.final()]);
  const decipher = createDecipheriv('chacha20-poly1305', dek,
    Buffer.from(envelope.nonce, 'hex'), { authTagLength: 16 });
  decipher.setAuthTag(Buffer.from(envelope.tag, 'hex'));
  return Buffer.concat([decipher.update(Buffer.from(envelope.ciphertext, 'hex')), decipher.final()]);
}

function contentHash(data) { return createHash('sha256').update(data).digest('hex'); }

// ── HTTP helpers ──

async function httpJson(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const resp = await fetch(url, { ...options, signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...options.headers } });
    const text = await resp.text();
    try { return { status: resp.status, ok: resp.ok, data: JSON.parse(text) }; }
    catch { return { status: resp.status, ok: resp.ok, data: text }; }
  } catch (e) {
    return { status: 0, ok: false, data: { error: e.message } };
  } finally { clearTimeout(timeout); }
}

// ── Backend Drivers ──

/**
 * Each backend implements: write(nodeConfig, agentId, cid, envelopeBytes), 
 *                          read(nodeConfig, agentId, cid) → Buffer|null,
 *                          health(nodeConfig) → { status, ... }
 */
const backends = {
  // ── Memory Store (HTTP KV) ──
  'memory-store': {
    async write(node, agentId, cid, envelopeBytes, metadata) {
      const r = await httpJson(`${node.url}/api/v1/agent/${agentId}/memory`, {
        method: 'PUT',
        body: JSON.stringify({
          content: Buffer.from(envelopeBytes).toString('base64'),
          type: 'encrypted-blob',
          filename: `${metadata.key}.encrypted`,
          timestamp: Math.floor(Date.now() / 1000),
        }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}: ${JSON.stringify(r.data)}`);
      return { cid: r.data.cid, nodeId: node.id };
    },
    async read(node, agentId, cid) {
      const r = await httpJson(`${node.url}/api/v1/agent/${agentId}/memory/${cid}`);
      if (!r.ok) return null;
      // The blob may be raw JSON or base64-encoded
      if (typeof r.data === 'object' && r.data.version && r.data.algorithm) return r.data;
      if (typeof r.data === 'string') {
        try { return JSON.parse(Buffer.from(r.data, 'base64').toString()); } catch {}
        try { return JSON.parse(r.data); } catch {}
      }
      return r.data;
    },
    async health(node) {
      const r = await httpJson(`${node.url}/health`);
      const stats = await httpJson(`${node.url}/api/v1/stats`).catch(() => ({ data: {} }));
      return { status: r.ok ? 'ok' : 'down', ...r.data, stats: stats.data || {} };
    },
  },

  // ── FilStream Network (content-addressed, distributed via seeders) ──
  'filstream': {
    async write(node, agentId, cid, envelopeBytes, metadata) {
      // Upload encrypted blob to FilStream index → automatically distributed to seeders
      const boundary = '----StoragePrivate' + Date.now();
      const filename = `${agentId}/${metadata.key}.encrypted`;
      const title = `[encrypted] ${metadata.key}`;
      
      const bodyParts = [
        `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: application/octet-stream\r\n\r\n`,
        envelopeBytes,
        `\r\n--${boundary}\r\nContent-Disposition: form-data; name="title"\r\n\r\n${title}`,
        `\r\n--${boundary}--\r\n`,
      ];
      
      const body = Buffer.concat(bodyParts.map(p => typeof p === 'string' ? Buffer.from(p) : p));
      
      const resp = await fetch(`${node.index_url}/api/upload`, {
        method: 'POST',
        headers: { 'Content-Type': `multipart/form-data; boundary=${boundary}` },
        body,
      });
      const result = await resp.json();
      if (!resp.ok) throw new Error(`FilStream upload failed: ${JSON.stringify(result)}`);
      return { cid: result.cid, fsCid: result.cid, nodeId: node.id };
    },
    async read(node, agentId, cid) {
      // Try seeder first (cached/distributed), fall back to index
      for (const baseUrl of [node.seeder_url, node.index_url]) {
        if (!baseUrl) continue;
        try {
          const port = new URL(baseUrl).port;
          const url = port === '4001' || port === '4002'
            ? `${baseUrl}/content/${cid}`
            : `${baseUrl}/api/content/${cid}/stream`;
          const resp = await fetch(url, { signal: AbortSignal.timeout(10000) });
          if (resp.ok) {
            const text = await resp.text();
            try { return JSON.parse(text); } catch { return text; }
          }
        } catch {}
      }
      return null;
    },
    async health(node) {
      const checks = {};
      try {
        const r = await httpJson(`${node.index_url}/api/content`);
        checks.index = { status: 'ok', items: r.data?.content?.length || '?' };
      } catch (e) { checks.index = { status: 'down', error: e.message }; }
      try {
        const r = await httpJson(`${node.seeder_url || ''}/health`);
        checks.seeder = { status: r.ok ? 'ok' : 'down', ...r.data };
      } catch (e) { checks.seeder = { status: 'down', error: e.message }; }
      const allOk = Object.values(checks).some(c => c.status === 'ok');
      return { status: allOk ? 'ok' : 'down', ...checks };
    },
  },

  // ── Local Filesystem (geographic diversity, fastest reads) ──
  'local': {
    async write(node, agentId, cid, envelopeBytes, metadata) {
      const blobDir = resolve(node.path.replace('~', homedir()), agentId.replace(/[^a-zA-Z0-9_:-]/g, '_'));
      mkdirSync(blobDir, { recursive: true });
      const blobPath = resolve(blobDir, `${cid}.json`);
      writeFileSync(blobPath, envelopeBytes);
      return { cid, nodeId: node.id, path: blobPath };
    },
    async read(node, agentId, cid) {
      const blobDir = resolve(node.path.replace('~', homedir()), agentId.replace(/[^a-zA-Z0-9_:-]/g, '_'));
      const blobPath = resolve(blobDir, `${cid}.json`);
      if (!existsSync(blobPath)) return null;
      const raw = readFileSync(blobPath, 'utf8');
      try { return JSON.parse(raw); } catch { return raw; }
    },
    async health(node) {
      const dir = node.path.replace('~', homedir());
      try {
        mkdirSync(dir, { recursive: true });
        const testFile = resolve(dir, '.health-check');
        writeFileSync(testFile, 'ok');
        let totalBytes = 0;
        let blobCount = 0;
        if (existsSync(dir)) {
          const walk = (d) => {
            for (const f of readdirSync(d, { withFileTypes: true })) {
              if (f.isDirectory()) walk(resolve(d, f.name));
              else if (f.name.endsWith('.json') && f.name !== '.health-check') {
                blobCount++;
                totalBytes += statSync(resolve(d, f.name)).size;
              }
            }
          };
          walk(dir);
        }
        return { status: 'ok', path: dir, blobs: blobCount, bytes: totalBytes,
                 bytes_human: `${(totalBytes / 1024).toFixed(1)} KB` };
      } catch (e) { return { status: 'error', error: e.message }; }
    },
  },
};

// ── Local Index ──

function loadLocalIndexSync(namespace) {
  try {
    const path = resolve(LOCAL_INDEX_DIR, namespace.replace(/[^a-zA-Z0-9_-]/g, '_'), 'index.json');
    if (existsSync(path)) return JSON.parse(readFileSync(path, 'utf8'));
  } catch {}
  return { namespace, entries: {}, created: new Date().toISOString() };
}

function saveLocalIndexSync(namespace, index) {
  const dir = resolve(LOCAL_INDEX_DIR, namespace.replace(/[^a-zA-Z0-9_-]/g, '_'));
  mkdirSync(dir, { recursive: true });
  writeFileSync(resolve(dir, 'index.json'), JSON.stringify(index, null, 2));
}

// ── Commands ──

async function cmdPut(key, opts) {
  const kek = getKEK();
  const namespace = opts.namespace || DEFAULT_NAMESPACE;
  
  // Get plaintext
  let plaintext;
  if (opts.file) { plaintext = readFileSync(resolve(opts.file)); }
  else if (opts.data) { plaintext = Buffer.from(opts.data, 'utf8'); }
  else { const chunks = []; for await (const chunk of process.stdin) chunks.push(chunk); plaintext = Buffer.concat(chunks); }
  
  const hash = contentHash(plaintext);
  const envelope = encrypt(plaintext, kek);
  const envelopeJson = JSON.stringify(envelope);
  const envelopeBytes = Buffer.from(envelopeJson);
  const agentId = `storage-private:${namespace}`;
  
  // CID for local index (content-addressed)
  const cid = 'bafymem' + createHash('sha256').update(envelopeBytes).digest('hex').slice(0, 24);
  
  // Write to ALL enabled nodes in parallel
  const results = await Promise.allSettled(
    ENABLED_NODES.map(async (node) => {
      const driver = backends[node.type];
      if (!driver) throw new Error(`Unknown backend type: ${node.type}`);
      return await driver.write(node, agentId, cid, envelopeBytes, { key });
    })
  );
  
  const successes = [];
  const failures = [];
  results.forEach((r, i) => {
    const node = ENABLED_NODES[i];
    if (r.status === 'fulfilled') {
      successes.push({ nodeId: node.id, type: node.type, location: node.location, ...r.value });
    } else {
      failures.push({ nodeId: node.id, type: node.type, location: node.location, error: r.reason?.message });
    }
  });
  
  if (successes.length === 0) {
    console.error(`❌ All ${ENABLED_NODES.length} nodes failed:`);
    failures.forEach(f => console.error(`   ${f.nodeId} (${f.type}): ${f.error}`));
    process.exit(1);
  }
  
  if (failures.length > 0) {
    failures.forEach(f => console.error(`⚠️  ${f.nodeId} (${f.location}): ${f.error}`));
  }
  
  // Update local index
  const index = loadLocalIndexSync(namespace);
  const entry = {
    key, cid,
    version: ((index.entries[key]?.current?.version) || 0) + 1,
    size_plain: plaintext.length,
    size_encrypted: envelopeBytes.length,
    content_hash: hash,
    algorithm: 'chacha20-poly1305',
    created: new Date().toISOString(),
    previous_cid: index.entries[key]?.cid || null,
    // Track where replicas live
    replicas: successes.map(s => ({ nodeId: s.nodeId, type: s.type, cid: s.cid || s.fsCid || cid })),
    // Track FilStream CID separately (different hash scheme)
    filstream_cid: successes.find(s => s.fsCid)?.fsCid || null,
  };
  
  if (!index.entries[key]) {
    index.entries[key] = { current: entry, history: [] };
  } else {
    index.entries[key].history.push(index.entries[key].current);
    index.entries[key].current = entry;
  }
  index.updated = new Date().toISOString();
  saveLocalIndexSync(namespace, index);
  
  // Optional on-chain anchor
  if (opts.anchor) {
    console.error(`⛓️  On-chain anchoring: ${cid} (TODO: SignalAnchor v2)`);
  }
  
  console.log(JSON.stringify({
    status: 'ok', key, cid,
    version: entry.version,
    size_plain: plaintext.length,
    size_encrypted: envelopeBytes.length,
    content_hash: hash,
    replicas: successes.length,
    total_nodes: ENABLED_NODES.length,
    distribution: successes.map(s => `${s.nodeId} (${s.type})`),
    filstream_cid: entry.filstream_cid,
  }, null, 2));
}

async function cmdGet(key, opts) {
  const kek = getKEK();
  const namespace = opts.namespace || DEFAULT_NAMESPACE;
  const index = loadLocalIndexSync(namespace);
  const entryRecord = index.entries[key];
  
  if (!entryRecord) { console.error(`❌ Key "${key}" not found in namespace "${namespace}"`); process.exit(1); }
  
  let entry;
  if (opts.version && entryRecord.history) {
    entry = entryRecord.history.find(e => e.version === parseInt(opts.version));
    if (!entry && entryRecord.current.version === parseInt(opts.version)) entry = entryRecord.current;
  } else {
    entry = entryRecord.current;
  }
  if (!entry) { console.error(`❌ Version ${opts.version} not found`); process.exit(1); }
  
  // Try each node in priority order (local first = fastest)
  const agentId = `storage-private:${namespace}`;
  let envelope = null;
  let sourceNode = null;
  
  for (const node of ENABLED_NODES) {
    const driver = backends[node.type];
    if (!driver) continue;
    try {
      // Use the node-specific CID if available (FilStream has different CID scheme)
      const replicaInfo = entry.replicas?.find(r => r.nodeId === node.id);
      const cidToFetch = replicaInfo?.cid || entry.cid;
      const result = await driver.read(node, agentId, cidToFetch);
      if (result && typeof result === 'object' && result.version && result.algorithm) {
        envelope = result;
        sourceNode = node.id;
        break;
      }
    } catch (e) {
      console.error(`⚠️  ${node.id}: ${e.message}`);
    }
  }
  
  if (!envelope) { console.error(`❌ Could not fetch from any of ${ENABLED_NODES.length} nodes`); process.exit(1); }
  
  const plaintext = decrypt(envelope, kek);
  const hash = contentHash(plaintext);
  if (entry.content_hash && hash !== entry.content_hash) {
    console.error(`⚠️  Integrity check FAILED! Expected ${entry.content_hash}, got ${hash}`);
    process.exit(1);
  }
  
  if (opts.output) {
    writeFileSync(resolve(opts.output), plaintext);
    console.error(`✅ Decrypted ${plaintext.length} bytes → ${opts.output} (from ${sourceNode})`);
  } else {
    process.stdout.write(plaintext);
  }
}

async function cmdList(opts) {
  const namespace = opts.namespace || DEFAULT_NAMESPACE;
  const index = loadLocalIndexSync(namespace);
  const entries = Object.entries(index.entries);
  
  const keys = entries
    .filter(([k, v]) => (!opts.prefix || k.startsWith(opts.prefix)) && !v.current.tombstoned)
    .map(([k, v]) => ({
      key: k,
      version: v.current.version,
      size: v.current.size_plain,
      hash: v.current.content_hash?.slice(0, 16) + '...',
      created: v.current.created,
      versions: (v.history?.length || 0) + 1,
      replicas: v.current.replicas?.length || 0,
      nodes: v.current.replicas?.map(r => r.nodeId) || [],
    }));
  
  console.log(JSON.stringify({ namespace, count: keys.length, keys }, null, 2));
}

async function cmdDelete(key, opts) {
  const namespace = opts.namespace || DEFAULT_NAMESPACE;
  const index = loadLocalIndexSync(namespace);
  if (!index.entries[key]) { console.error(`❌ Key "${key}" not found`); process.exit(1); }
  index.entries[key].tombstoned = new Date().toISOString();
  index.entries[key].current.tombstoned = true;
  index.updated = new Date().toISOString();
  saveLocalIndexSync(namespace, index);
  console.log(JSON.stringify({ status: 'tombstoned', key, namespace }, null, 2));
}

async function cmdStatus() {
  const results = { nodes: [], replication: null, local_index: null, encryption: null };
  
  for (const node of ENABLED_NODES) {
    const driver = backends[node.type];
    if (!driver) { results.nodes.push({ id: node.id, type: node.type, status: 'unknown-type' }); continue; }
    try {
      const health = await driver.health(node);
      results.nodes.push({ id: node.id, type: node.type, location: node.location, ...health });
    } catch (e) {
      results.nodes.push({ id: node.id, type: node.type, location: node.location, status: 'error', error: e.message });
    }
  }
  
  const healthy = results.nodes.filter(n => n.status === 'ok').length;
  results.replication = {
    total_nodes: ENABLED_NODES.length,
    healthy,
    min_replicas: CONFIG.replication.min_replicas,
    status: healthy >= CONFIG.replication.min_replicas ? 'ok' : 'degraded',
  };
  
  results.local_index = { status: 'ok', path: LOCAL_INDEX_DIR };
  
  try { getKEK(); results.encryption = { status: 'ok', algorithm: 'chacha20-poly1305', key_source: 'eth-wallet' }; }
  catch (e) { results.encryption = { status: 'error', error: e.message }; }
  
  console.log(JSON.stringify(results, null, 2));
}

async function cmdSync(opts) {
  const namespace = opts.namespace || DEFAULT_NAMESPACE;
  const index = loadLocalIndexSync(namespace);
  const entries = Object.entries(index.entries).filter(([_, v]) => !v.current.tombstoned);
  const agentId = `storage-private:${namespace}`;
  
  console.error(`🔄 Syncing ${entries.length} keys in namespace "${namespace}" across ${ENABLED_NODES.length} nodes...`);
  
  let synced = 0;
  let failed = 0;
  
  for (const [key, record] of entries) {
    const entry = record.current;
    const existingNodeIds = new Set(entry.replicas?.map(r => r.nodeId) || []);
    const missingNodes = ENABLED_NODES.filter(n => !existingNodeIds.has(n.id));
    
    if (missingNodes.length === 0) continue;
    
    // Read the blob from any available node (try ALL nodes, not just known replicas)
    let envelopeBytes = null;
    let sourceNodeId = null;
    for (const node of ENABLED_NODES) {
      const driver = backends[node.type];
      if (!driver) continue;
      try {
        const replicaInfo = entry.replicas?.find(r => r.nodeId === node.id);
        const cidToFetch = replicaInfo?.cid || entry.cid;
        const result = await driver.read(node, agentId, cidToFetch);
        if (result && typeof result === 'object' && result.version && result.algorithm) {
          envelopeBytes = Buffer.from(JSON.stringify(result));
          sourceNodeId = node.id;
          existingNodeIds.add(node.id);
          break;
        }
      } catch {}
    }
    
    if (!envelopeBytes) {
      console.error(`⚠️  ${key}: could not read from any node`);
      failed++;
      continue;
    }
    
    // Recalculate missing nodes now that we know the source
    const actualMissingNodes = ENABLED_NODES.filter(n => !existingNodeIds.has(n.id));
    if (actualMissingNodes.length === 0) { synced++; continue; }
    
    // Write to missing nodes
    const newReplicas = [...(entry.replicas || [])];
    // Add source node to replicas if not already tracked
    if (sourceNodeId && !newReplicas.find(r => r.nodeId === sourceNodeId)) {
      const srcNode = ENABLED_NODES.find(n => n.id === sourceNodeId);
      if (srcNode) newReplicas.push({ nodeId: srcNode.id, type: srcNode.type, cid: entry.cid });
    }
    for (const node of actualMissingNodes) {
      const driver = backends[node.type];
      if (!driver) continue;
      try {
        const result = await driver.write(node, agentId, entry.cid, envelopeBytes, { key });
        newReplicas.push({ nodeId: node.id, type: node.type, cid: result.cid || result.fsCid || entry.cid });
        synced++;
      } catch (e) {
        console.error(`⚠️  ${key} → ${node.id}: ${e.message}`);
        failed++;
      }
    }
    
    // Update index with new replica info
    entry.replicas = newReplicas;
    entry.filstream_cid = newReplicas.find(r => r.type === 'filstream')?.cid || entry.filstream_cid;
  }
  
  // Save updated index
  index.updated = new Date().toISOString();
  saveLocalIndexSync(namespace, index);
  
  console.log(JSON.stringify({
    status: 'ok',
    namespace,
    total_keys: entries.length,
    synced_writes: synced,
    failed_writes: failed,
    nodes: ENABLED_NODES.map(n => n.id),
  }, null, 2));
}

// ── Discovery ──

async function cmdDiscover(opts) {
  // Shell out to discover.mjs for clean separation
  const { execSync } = await import('node:child_process');
  const discoverPath = resolve(__dirname, 'discover.mjs');
  const args = ['--update-config'];
  if (opts.maxNodes) args.push('--max-nodes', opts.maxNodes);
  try {
    const output = execSync(`node "${discoverPath}" ${args.join(' ')}`, { encoding: 'utf8', timeout: 30000 });
    console.log(output);
    // Reload config
    console.error('✅ Config updated. Run `status` to see new nodes.');
  } catch (e) {
    console.error(`❌ Discovery failed: ${e.message}`);
    process.exit(1);
  }
}

// ── Key Management ──

function getKEK() {
  let secret = process.env.STORAGE_PRIVATE_KEY;
  if (!secret) {
    const walletEnv = resolve(SECRETS_DIR, 'eth-wallet.env');
    if (existsSync(walletEnv)) {
      const content = readFileSync(walletEnv, 'utf8');
      const match = content.match(/PRIVATE_KEY=([0-9a-fA-Fx]+)/);
      if (match) secret = match[1];
    }
  }
  if (!secret) throw new Error('No encryption key. Set STORAGE_PRIVATE_KEY or ensure .secrets/eth-wallet.env exists.');
  return deriveKEK(secret);
}

// ── CLI ──

function parseArgs(argv) {
  const args = argv.slice(2);
  const cmd = args[0];
  const positional = [];
  const flags = {};
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) { flags[key] = next; i++; }
      else flags[key] = true;
    } else positional.push(args[i]);
  }
  return { cmd, positional, flags };
}

async function main() {
  const { cmd, positional, flags } = parseArgs(process.argv);
  const opts = {
    namespace: flags.namespace || flags.ns || DEFAULT_NAMESPACE,
    file: flags.file || flags.f,
    data: flags.data || flags.d,
    output: flags.output || flags.o,
    version: flags.version || flags.v,
    prefix: flags.prefix || flags.p,
    anchor: flags.anchor || false,
  };
  
  switch (cmd) {
    case 'put':
      if (!positional[0]) { console.error('Usage: storage.mjs put <key> [--data "..." | --file path]'); process.exit(1); }
      await cmdPut(positional[0], opts); break;
    case 'get':
      if (!positional[0]) { console.error('Usage: storage.mjs get <key> [--output path]'); process.exit(1); }
      await cmdGet(positional[0], opts); break;
    case 'list': case 'ls':
      await cmdList(opts); break;
    case 'delete': case 'rm':
      if (!positional[0]) { console.error('Usage: storage.mjs delete <key>'); process.exit(1); }
      await cmdDelete(positional[0], opts); break;
    case 'status':
      await cmdStatus(); break;
    case 'sync':
      await cmdSync(opts); break;
    case 'discover':
      await cmdDiscover(opts); break;
    default:
      console.log(`🔐 Storage Private — Encrypted Multi-Node Agent Storage

Commands:
  put <key> [--data "..." | --file path]   Encrypt & replicate to all nodes
  get <key> [--output path]                Retrieve & decrypt (failover reads)
  list [--prefix "..."]                    List stored keys  
  delete <key>                             Tombstone a key
  status                                   Health check all nodes
  sync                                     Ensure all nodes have all data

Options:
  --namespace, --ns    Storage namespace (default: ${DEFAULT_NAMESPACE})
  --anchor             Anchor CID on-chain after storing
  --version, --v       Retrieve specific version
  --output, --o        Write decrypted output to file

Nodes (${ENABLED_NODES.length} configured):
${ENABLED_NODES.map(n => `  ${n.id} (${n.type}) — ${n.location}`).join('\n')}`);
  }
}

main().catch(e => { console.error(`❌ ${e.message}`); process.exit(1); });
