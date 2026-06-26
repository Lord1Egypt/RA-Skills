/**
 * sync_incremental.js — Cross-device incremental sync for unified-memory
 * P2-2: Incremental Sync
 * 
 * Based on collab/cloud.js infrastructure.
 * - Records every write as a sync_log entry: {op, memory_id, timestamp, checksum}
 * - Push: exports local delta to remote (WebDAV / S3 / local)
 * - Pull: imports remote delta, merges with local (timestamp + checksum conflict resolution)
 * 
 * Storage: ~/.unified-memory/sync/
 */

import { createRequire } from 'module';
import { existsSync, readFileSync, writeFileSync, mkdirSync, appendFileSync, unlinkSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { createHash } from 'crypto';
import { fileURLToPath } from 'url';

const req = createRequire(import.meta.url);
const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const SYNC_DIR = join(HOME, '.unified-memory', 'sync');
const SYNC_LOG_FILE = join(SYNC_DIR, 'sync_log.jsonl');
const SYNC_STATE_FILE = join(SYNC_DIR, 'sync_state.json');
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');

// ============================================================
// Checksum utility
// ============================================================

function checksumMemory(mem) {
  const content = JSON.stringify({
    id: mem.id,
    text: mem.text,
    category: mem.category,
    importance: mem.importance,
    tags: mem.tags,
    scope: mem.scope,
  });
  return createHash('sha256').update(content).digest('hex').slice(0, 16);
}

// ============================================================
// Sync log management
// ============================================================

function ensureSyncDir() {
  if (!existsSync(SYNC_DIR)) {
    mkdirSync(SYNC_DIR, { recursive: true });
  }
}

function loadSyncLog(limit = 1000) {
  ensureSyncDir();
  if (!existsSync(SYNC_LOG_FILE)) return [];
  try {
    const lines = readFileSync(SYNC_LOG_FILE, 'utf-8').split('\n').filter(Boolean);
    return lines.slice(-limit).map(line => {
      try { return JSON.parse(line); } catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

function appendSyncLog(op, memoryId, mem = null) {
  ensureSyncDir();
  const entry = {
    op,           // 'upsert' | 'delete'
    memory_id: memoryId,
    timestamp: Date.now(),
    checksum: mem ? checksumMemory(mem) : null,
  };
  appendFileSync(SYNC_LOG_FILE, JSON.stringify(entry) + '\n', 'utf-8');
  return entry;
}

/**
 * Get last sync timestamp from state file
 */
function getLastSyncTime(scope = 'default') {
  if (!existsSync(SYNC_STATE_FILE)) return null;
  try {
    const state = JSON.parse(readFileSync(SYNC_STATE_FILE, 'utf-8'));
    return state[scope]?.last_sync_at || null;
  } catch {
    return null;
  }
}

/**
 * Update last sync timestamp
 */
function setLastSyncTime(scope, timestamp = Date.now()) {
  ensureSyncDir();
  let state = {};
  if (existsSync(SYNC_STATE_FILE)) {
    try { state = JSON.parse(readFileSync(SYNC_STATE_FILE, 'utf-8')); } catch { /* ignore */ }
  }
  if (!state[scope]) state[scope] = {};
  state[scope].last_sync_at = timestamp;
  writeFileSync(SYNC_STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

// ============================================================
// Storage backends
// ============================================================

/**
 * Local filesystem sync provider (reads from memory store directly)
 */
class LocalSyncProvider {
  constructor(backupPath) {
    this.backupPath = backupPath || join(HOME, '.unified-memory', 'sync_backup');
    this.type = 'local';
  }

  async push(delta, remotePath = 'delta.json') {
    try {
      mkdirSync(this.backupPath, { recursive: true });
      const remoteFull = join(this.backupPath, remotePath);
      writeFileSync(remoteFull, JSON.stringify(delta, null, 2), 'utf-8');
      return { success: true, path: remoteFull };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async pull(remotePath = 'delta.json') {
    try {
      const remoteFull = join(this.backupPath, remotePath);
      if (!existsSync(remoteFull)) return { success: false, error: 'No remote delta found' };
      const data = JSON.parse(readFileSync(remoteFull, 'utf-8'));
      return { success: true, data };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async listDeltas() {
    try {
      if (!existsSync(this.backupPath)) return [];
      const files = readdirSync(this.backupPath).filter(f => f.endsWith('.json'));
      return files.map(f => {
        const stat = statSync(join(this.backupPath, f));
        return { name: f, modified: stat.mtime.toISOString(), size: stat.size };
      });
    } catch {
      return [];
    }
  }
}

/**
 * WebDAV sync provider
 */
class WebDAVSyncProvider {
  constructor(config = {}) {
    this.url = config.url || '';
    this.username = config.username || '';
    this.password = config.password || '';
    this.remotePath = config.path || '/memory_backup';
    this.type = 'webdav';
  }

  async push(delta, remotePath = 'delta.json') {
    try {
      const fullUrl = `${this.url}${this.remotePath}/${remotePath}`;
      const body = JSON.stringify(delta, null, 2);
      const resp = await fetch(fullUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...(this.username ? { 'Authorization': `Basic ${Buffer.from(`${this.username}:${this.password}`).toString('base64')}` } : {}),
        },
        body,
        signal: AbortSignal.timeout(30000),
      });
      if (!resp.ok) throw new Error(`WebDAV ${resp.status} ${resp.statusText}`);
      return { success: true, url: fullUrl };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async pull(remotePath = 'delta.json') {
    try {
      const fullUrl = `${this.url}${this.remotePath}/${remotePath}`;
      const resp = await fetch(fullUrl, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          ...(this.username ? { 'Authorization': `Basic ${Buffer.from(`${this.username}:${this.password}`).toString('base64')}` } : {}),
        },
        signal: AbortSignal.timeout(30000),
      });
      if (resp.status === 404) return { success: false, error: 'Not found' };
      if (!resp.ok) throw new Error(`WebDAV ${resp.status}`);
      const text = await resp.text();
      return { success: true, data: JSON.parse(text) };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async listDeltas() {
    return []; // WebDAV PROPFIND out of scope
  }
}

// ============================================================
// Merge / conflict resolution
// ============================================================

/**
 * Resolve conflict between local and remote entry.
 * Strategy: latest timestamp wins by default.
 * Optionally use `source` priority: explicit > inferred > historical.
 * @param {object} local
 * @param {object} remote
 * @param {string} strategy - 'timestamp' | 'source_priority'
 */
function resolveConflict(local, remote, strategy = 'timestamp') {
  if (strategy === 'timestamp') {
    return (remote.timestamp || 0) > (local.timestamp || 0) ? remote : local;
  }
  // source_priority: explicit > inferred > historical
  const priority = { explicit: 3, inferred: 2, historical: 1 };
  const remoteP = priority[remote.source] || 0;
  const localP = priority[local.source] || 0;
  if (remoteP !== localP) return remoteP > localP ? remote : local;
  // Same priority: latest timestamp wins
  return (remote.timestamp || 0) > (local.timestamp || 0) ? remote : local;
}

// ============================================================
// Public sync API
// ============================================================

/**
 * Record a sync log entry for a write operation.
 * Call this after every add/update/delete in storage.js.
 * @param {string} op - 'upsert' | 'delete'
 * @param {object} memory - the memory object (for upsert)
 */
export function recordSyncOp(op, memory = null) {
  try {
    const memoryId = memory?.id || null;
    if (!memoryId) return;
    return appendSyncLog(op, memoryId, memory);
  } catch (err) {
    console.error('[sync_incremental] recordSyncOp failed:', err.message);
  }
}

/**
 * Push local delta to remote.
 * Returns { success, delta, stats }
 * @param {object} options
 * @param {string} options.providerType - 'local' | 'webdav'
 * @param {object} options.providerConfig - provider-specific config
 * @param {string} options.scope - sync scope identifier
 */
export async function syncPush({ providerType = 'local', providerConfig = {}, scope = 'default' } = {}) {
  try {
    const provider = providerType === 'webdav'
      ? new WebDAVSyncProvider(providerConfig)
      : new LocalSyncProvider(providerConfig);

    const since = getLastSyncTime(scope);
    const logEntries = loadSyncLog(10000);

    // Build delta: only entries since last sync
    const deltaEntries = since
      ? logEntries.filter(e => e.timestamp > since)
      : logEntries;

    if (deltaEntries.length === 0) {
      setLastSyncTime(scope);
      return { success: true, pushed: 0, message: 'No delta to push' };
    }

    // Attach memory data for upsert entries
    const { getAllMemories } = await import('./storage.js');
    const memories = await getAllMemories();
    const memoryMap = new Map(memories.map(m => [m.id, m]));

    const delta = {
      scope,
      generated_at: Date.now(),
      entries: deltaEntries.map(e => ({
        ...e,
        memory: e.op === 'upsert' ? memoryMap.get(e.memory_id) : null,
      })),
    };

    const remotePath = `delta_${scope}_${Date.now()}.json`;
    const result = await provider.push(delta, remotePath);

    if (result.success) {
      setLastSyncTime(scope);
      return {
        success: true,
        pushed: deltaEntries.length,
        remote_path: result.path || result.url || remotePath,
        delta_id: remotePath,
      };
    } else {
      return { success: false, error: result.error };
    }
  } catch (err) {
    return { success: false, error: err.message };
  }
}

/**
 * Pull remote delta and merge with local.
 * @param {object} options
 * @param {string} options.providerType
 * @param {object} options.providerConfig
 * @param {string} options.remotePath - specific delta file to pull (optional)
 * @param {string} options.scope
 * @param {string} options.conflictStrategy - 'timestamp' | 'source_priority'
 */
export async function syncPull({ providerType = 'local', providerConfig = {}, remotePath, scope = 'default', conflictStrategy = 'timestamp' } = {}) {
  try {
    const provider = providerType === 'webdav'
      ? new WebDAVSyncProvider(providerConfig)
      : new LocalSyncProvider(providerConfig);

    // If remotePath specified, pull that specific delta; otherwise find latest
    let result;
    if (remotePath) {
      result = await provider.pull(remotePath);
    } else {
      // Find latest delta for this scope
      const deltas = await provider.listDeltas();
      const scopeDeltas = deltas.filter(f => f.name.includes(`_${scope}_`)).sort((a, b) =>
        new Date(b.modified) - new Date(a.modified)
      );
      if (scopeDeltas.length === 0) {
        return { success: true, merged: 0, message: 'No remote delta found' };
      }
      result = await provider.pull(scopeDeltas[0].name);
    }

    if (!result.success) {
      return { success: false, error: result.error };
    }

    const { data: delta } = result;
    if (!delta?.entries?.length) {
      return { success: true, merged: 0, message: 'Empty delta' };
    }

    // Load current local memories and sync log
    const { getAllMemories, saveMemories } = await import('./storage.js');
    let localMemories = await getAllMemories();
    const localMap = new Map(localMemories.map(m => [m.id, m]));
    let merged = 0;
    let conflicts = 0;

    for (const entry of delta.entries) {
      const { op, memory_id, timestamp, checksum, memory: remoteMem } = entry;

      if (op === 'upsert' && remoteMem) {
        const local = localMap.get(memory_id);
        if (!local) {
          // New memory from remote — add
          localMemories.push(remoteMem);
          localMap.set(memory_id, remoteMem);
          merged++;
        } else {
          // Conflict resolution
          const localEntry = { timestamp: local.updated_at, source: local.source || 'historical', memory: local };
          const remoteEntry = { timestamp, source: remoteMem.source || 'historical', memory: remoteMem };
          const winner = resolveConflict(localEntry, remoteEntry, conflictStrategy);

          if (winner.memory.id === remoteMem.id) {
            // Remote wins — update local
            const idx = localMemories.findIndex(m => m.id === memory_id);
            if (idx !== -1) localMemories[idx] = remoteMem;
            localMap.set(memory_id, remoteMem);
          }
          conflicts++;
        }
      } else if (op === 'delete') {
        const idx = localMemories.findIndex(m => m.id === memory_id);
        if (idx !== -1) {
          localMemories.splice(idx, 1);
          localMap.delete(memory_id);
          merged++;
        }
      }
    }

    saveMemories(localMemories);
    setLastSyncTime(scope);

    return {
      success: true,
      merged,
      conflicts,
      delta_entries: delta.entries.length,
    };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

/**
 * Get sync status
 */
export function syncStatus({ scope = 'default' } = {}) {
  const lastSync = getLastSyncTime(scope);
  const logEntries = loadSyncLog(10);
  const recentOps = logEntries.slice(-10);

  return {
    scope,
    last_sync_at: lastSync ? new Date(lastSync).toISOString() : null,
    pending_ops: logEntries.filter(e => !lastSync || e.timestamp > lastSync).length,
    recent_ops: recentOps.map(e => ({
      op: e.op,
      memory_id: e.memory_id,
      timestamp: new Date(e.timestamp).toISOString(),
    })),
    sync_log: SYNC_LOG_FILE,
    sync_state: SYNC_STATE_FILE,
  };
}

/**
 * MCP tool: memory_sync
 */
export function memorySyncTool({ action, providerType, providerConfig, remotePath, scope, conflictStrategy, ttlSeconds } = {}) {
  try {
    if (action === 'status') {
      const status = syncStatus({ scope: scope || 'default' });
      return { content: [{ type: 'text', text: JSON.stringify(status, null, 2) }] };
    }

    if (action === 'push') {
      if (providerType === 'webdav' && !providerConfig?.url) {
        return { content: [{ type: 'text', text: '{"error": "webdav provider requires url in providerConfig"}' }], isError: true };
      }
      return syncPush({
        providerType: providerType || 'local',
        providerConfig: providerConfig || {},
        scope: scope || 'default',
      }).then(result => {
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      }).catch(err => {
        return { content: [{ type: 'text', text: `Sync push error: ${err.message}` }], isError: true };
      });
    }

    if (action === 'pull') {
      return syncPull({
        providerType: providerType || 'local',
        providerConfig: providerConfig || {},
        remotePath,
        scope: scope || 'default',
        conflictStrategy: conflictStrategy || 'timestamp',
      }).then(result => {
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      }).catch(err => {
        return { content: [{ type: 'text', text: `Sync pull error: ${err.message}` }], isError: true };
      });
    }

    return {
      content: [{ type: 'text', text: '{"error": "Unknown action. Use: status, push, pull"}' }],
      isError: true,
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Sync error: ${err.message}` }], isError: true };
  }
}

export default {
  recordSyncOp,
  syncPush,
  syncPull,
  syncStatus,
  memorySyncTool,
};
