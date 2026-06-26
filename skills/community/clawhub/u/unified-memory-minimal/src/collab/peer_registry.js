/**
 * peer_registry.js - Peer Node Registry for Distributed Sync
 * 
 * Maintains a list of known peer nodes (local file paths or remote URLs).
 * Provides CRUD operations, health checks, and persistence.
 * 
 * Storage: ~/.openclaw/workspace/memory/shared/peers.json
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, statSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw/workspace/memory');
const SHARED_DIR = join(MEMORY_DIR, 'shared');
const PEERS_FILE = join(SHARED_DIR, 'peers.json');

const DEFAULT_PEER = {
  type: 'local',      // 'local' | 'remote'
  status: 'unknown',   // 'unknown' | 'online' | 'offline' | 'error'
  last_ping: null,
  last_sync: null,
  version: 0,
  priority: 1,
  enabled: true
};

function ensureSharedDir() {
  if (!existsSync(SHARED_DIR)) mkdirSync(SHARED_DIR, { recursive: true });
}

function loadPeers() {
  ensureSharedDir();
  try {
    if (existsSync(PEERS_FILE)) {
      const data = JSON.parse(readFileSync(PEERS_FILE, 'utf-8'));
      if (data && typeof data === 'object' && data.peers) return data;
    }
  } catch { /* ignore */ }
  return { peers: {}, schema: 'peer-registry-v1', last_updated: new Date().toISOString() };
}

function savePeers(registry) {
  registry.last_updated = new Date().toISOString();
  writeFileSync(PEERS_FILE, JSON.stringify(registry, null, 2), 'utf-8');
}

/**
 * Add a peer node
 * @param {string} peerId - Unique peer identifier
 * @param {string} pathOrUrl - File path (local) or URL (remote)
 * @param {object} options - { type: 'local'|'remote', priority: number }
 * @returns {object}
 */
export function addPeer(peerId, pathOrUrl, options = {}) {
  const registry = loadPeers();
  const type = options.type || (pathOrUrl.startsWith('http') ? 'remote' : 'local');

  if (registry.peers[peerId]) {
    return { success: false, reason: 'already exists', peer_id: peerId };
  }

  registry.peers[peerId] = {
    ...DEFAULT_PEER,
    peer_id: peerId,
    path: pathOrUrl,
    type,
    priority: options.priority || 1,
    added_at: new Date().toISOString(),
    enabled: options.enabled !== false
  };

  savePeers(registry);
  return { success: true, peer_id: peerId, type };
}

/**
 * Remove a peer node
 * @param {string} peerId
 * @returns {object}
 */
export function removePeer(peerId) {
  const registry = loadPeers();
  if (!registry.peers[peerId]) {
    return { success: false, reason: 'not found' };
  }
  delete registry.peers[peerId];
  savePeers(registry);
  return { success: true, peer_id: peerId };
}

/**
 * Update a peer
 * @param {string} peerId
 * @param {object} updates
 * @returns {object}
 */
export function updatePeer(peerId, updates) {
  const registry = loadPeers();
  if (!registry.peers[peerId]) {
    return { success: false, reason: 'not found' };
  }
  const allowed = ['path', 'type', 'priority', 'enabled', 'status', 'last_ping', 'last_sync', 'version'];
  for (const key of allowed) {
    if (key in updates) registry.peers[peerId][key] = updates[key];
  }
  savePeers(registry);
  return { success: true, peer_id: peerId };
}

/**
 * List all peers
 * @param {object} filters - { type, status, enabled }
 * @returns {Array<object>}
 */
export function listPeers(filters = {}) {
  const registry = loadPeers();
  let peers = Object.values(registry.peers);
  if (filters.type) peers = peers.filter(p => p.type === filters.type);
  if (filters.status) peers = peers.filter(p => p.status === filters.status);
  if (filters.enabled !== undefined) peers = peers.filter(p => p.enabled === filters.enabled);
  return peers;
}

/**
 * Get a single peer
 * @param {string} peerId
 * @returns {object|null}
 */
export function getPeer(peerId) {
  const registry = loadPeers();
  return registry.peers[peerId] || null;
}

/**
 * Health check - ping a peer
 * For local peers: check if file exists
 * For remote peers: HEAD request with timeout
 * @param {string} peerId
 * @returns {Promise<object>}
 */
export async function pingPeer(peerId) {
  const registry = loadPeers();
  const peer = registry.peers[peerId];
  if (!peer) return { success: false, reason: 'not found' };

  let online = false;
  let latency_ms = null;

  try {
    if (peer.type === 'local') {
      const exists = existsSync(peer.path);
      online = exists;
      if (exists) {
        const stat = statSync(peer.path);
        latency_ms = 0;
        peer.status = 'online';
      } else {
        peer.status = 'offline';
      }
    } else if (peer.type === 'remote') {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);
      try {
        const start = Date.now();
        const res = await fetch(peer.path, { method: 'HEAD', signal: controller.signal });
        latency_ms = Date.now() - start;
        online = res.ok;
        peer.status = online ? 'online' : 'error';
      } catch { peer.status = 'offline'; }
      clearTimeout(timeout);
    }
  } catch (err) {
    peer.status = 'error';
  }

  peer.last_ping = new Date().toISOString();
  savePeers(registry);

  return { success: online, latency_ms, status: peer.status };
}

/**
 * Health check all peers
 * @returns {Promise<object>}
 */
export async function pingAllPeers() {
  const peers = listPeers();
  const results = [];
  for (const peer of peers) {
    const r = await pingPeer(peer.peer_id);
    results.push({ peer_id: peer.peer_id, ...r });
  }
  const online = results.filter(r => r.success).length;
  return { total: peers.length, online, results };
}

export default { addPeer, removePeer, updatePeer, listPeers, getPeer, pingPeer, pingAllPeers };
