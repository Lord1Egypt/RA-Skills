import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { readFile, writeFile, rename } from 'fs/promises';
import { join } from 'path';
import { config } from './config.js';
import { acquireLockSync, releaseLockSync, initWalStorage, logWriteOp } from './storage_lock.js';
import { logOp, readWal, closeWal } from './wal.js';
import {
  getCurrentTeam,
  filterByTeamAndScope,
  normalizeScope,
  getCurrentAgentId,
} from './scope.js';
import { getTransactionManager } from './transaction-manager.js';

// v4 StorageGateway proxy (unified backend for sqlite mode)
let _v4Gw = null;
async function getV4Gw() {
  if (!_v4Gw) {
    const { StorageGateway } = await import('./v4/storage-gateway.js');
    _v4Gw = new StorageGateway();
    await _v4Gw.init();
  }
  return _v4Gw;
}

// ===== Storage Mode Selection =====
const STORAGE_MODE = process.env.STORAGE_MODE || 'json';

// Lazy-load SQLite backend (only when STORAGE_MODE=sqlite)
let _sqliteBackend = null;
async function getSqliteBackend() {
  if (_sqliteBackend) return _sqliteBackend;
  try {
    _sqliteBackend = await import('./storage_sqlite.js');
    return _sqliteBackend;
  } catch (e) {
    console.warn('[storage] SQLite backend unavailable:', e.message);
    return null;
  }
}

/**
 * Check if SQLite backend is active
 */
function isSqliteMode() {
  return STORAGE_MODE === 'sqlite';
}

// Lazy import to avoid circular deps and to handle missing Ollama gracefully
let _vectorMem = null;
async function getVectorMem() {
  if (!_vectorMem) {
    try {
      const { VectorMemory } = await import('./vector_lancedb.js');
      _vectorMem = new VectorMemory();
      await _vectorMem.initialize();
    } catch (e) {
      console.warn('[storage] VectorMemory init failed:', e.message);
      return null;
    }
  }
  return _vectorMem;
}

/**
 * @typedef {import('./types.js').Memory} Memory
 */

/** @type {Map<string, Memory[]>} */
const memoryCache = new Map();
let cacheDirty = false;

// ─── Write-Behind Buffer (P0-3) ──────────────────────────────────────────────
const WRITE_BEHIND_DELAY_MS = 500;
let _writeTimer = null;
let _pendingMemories = null;

/**
 * Flush any pending write immediately (called by timer or on shutdown)
 */
async function _flushPendingWrite() {
  if (!_pendingMemories) return;
  const memories = _pendingMemories;
  _pendingMemories = null;
  _writeTimer = null;
  // Direct write for JSON mode (no debounce timer, immediate flush)
  const lockPath = config.memoryFile;
  acquireLockSync(lockPath);
  try {
    if (global._walInit) {
      logWriteOp({ type: 'save', count: memories.length });
    }
    const data = JSON.stringify(memories, null, 2);
    const tmpPath = `${lockPath}.tmp.${process.pid}.${Date.now()}`;
    
    // 使用 fsync 保证数据持久化
    await writeFile(tmpPath, data, 'utf8');
    
    // 确保数据写入磁盘
    const fs = await import('fs');
    const fd = await fs.promises.open(tmpPath, 'r+');
    try {
      await fd.sync();
    } finally {
      await fd.close();
    }
    
    // 原子性重命名
    await rename(tmpPath, lockPath);
    
    // 确保目标文件也同步到磁盘
    const targetFd = await fs.promises.open(lockPath, 'r+');
    try {
      await targetFd.sync();
    } finally {
      await targetFd.close();
    }
    
  } catch (err) {
    console.error('[storage] Write-behind flush failed:', err.message);
  } finally {
    try { releaseLockSync(lockPath); } catch { /* ignore */ }
  }
  memoryCache.set('all', memories);
  cacheDirty = false;
}

/**
 * Actual save logic (async, multi-process safe via rename)
 */
async function _doSaveMemories(memories) {
  const lockPath = config.memoryFile;
  // Multi-process safe: use flock lock + atomic rename
  acquireLockSync(lockPath);
  let released = false;
  try {
    if (global._walInit) {
      logWriteOp({ type: 'save', count: memories.length });
    }
    const data = JSON.stringify(memories, null, 2);
    // Atomic write: temp file + rename (crash-safe, no partial files)
    const tmpPath = `${lockPath}.tmp.${process.pid}.${Date.now()}`;
    await writeFile(tmpPath, data, 'utf8');
    await rename(tmpPath, lockPath);
  } catch (err) {
    console.error('[storage] Write-behind flush failed:', err.message);
  } finally {
    try { releaseLockSync(lockPath); } catch { /* ignore */ }
  }
  memoryCache.set('all', memories);
  cacheDirty = false;
}

/**
 * @returns {Memory[]}
 */
export async function loadMemories() {
  // Clear any pending write-behind writes before reading from disk.
  // If a crash occurred, the pending write is lost and we reload from disk.
  if (_writeTimer) { clearTimeout(_writeTimer); _writeTimer = null; }
  _pendingMemories = null;
  // SQLite backend path
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    const mems = await gw.getMemories({ limit: 100000 });
    memoryCache.set('all', mems);
    return mems;
  }

  // JSON backend (default)
  if (!existsSync(config.memoryFile)) {
    return [];
  }
  try {
    const data = JSON.parse(readFileSync(config.memoryFile, 'utf8'));
    return Array.isArray(data) ? data : (data.memories || []);
  } catch {
    return [];
  }
}

/**
 * Save memories to disk (write-behind: queues write and flushes after debounce)
 * @param {Memory[]} memories
 */
export async function saveMemories(memories) {
  // SQLite backend
  if (isSqliteMode()) {
    // writeMemory handles WAL internally; no need to call gw multiple times
    // For bulk save, just return (memories already in DB via addMemory/updateMemory)
    return;
  }

  // Initialize WAL on first call
  if (!global._walInit) {
    try {
      initWalStorage();
      global._walInit = true;
    } catch { /* WAL init failure is non-fatal */ }
  }

  memoryCache.set('all', memories);
  cacheDirty = false;

  // Write-behind: debounce 500ms to reduce I/O under load
  _pendingMemories = memories;
  if (_writeTimer) clearTimeout(_writeTimer);
  _writeTimer = setTimeout(() => {
    _flushPendingWrite().catch(err => console.error('[storage] flush error:', err.message));
  }, WRITE_BEHIND_DELAY_MS);
}

/**
 * Force immediate flush of pending writes (call before shutdown or critical ops)
 */
export async function flushPendingWrites() {
  if (_writeTimer) {
    clearTimeout(_writeTimer);
    _writeTimer = null;
  }
  if (_pendingMemories) {
    await _flushPendingWrite();
  }
}

/**
 * Get all memories (with caching)
 * Optionally filter by team+scope context.
 * @param {object} opts
 * @param {string} [opts.scope='GLOBAL']  - Scope level for filtering
 * @param {boolean} [opts.applyTeamFilter=true] - Whether to apply current team context
 * @returns {Memory[]}
 */
// Normalized memory cache (survives across calls)
let _normalizedCache = null;

export async function getAllMemories(opts = {}) {
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    return gw.getMemories({ ...opts, limit: opts.limit || 10000 });
  }
  const { scope = 'GLOBAL', applyTeamFilter = false } = opts;
  if (!memoryCache.has('all')) {
    memoryCache.set('all', await loadMemories());
    _normalizedCache = null; // reset normalized cache on reload
  }
  // Normalize: support both 'content' (import format) and 'text' field
  // Cache normalized result to avoid re-mapping on every call
  if (!_normalizedCache) {
    _normalizedCache = memoryCache.get('all').map((m) => ({
      ...m,
      text: m.text || m.content || '',
      created_at: m.created_at || (m.timestamp ? new Date(m.timestamp).getTime() : Date.now()),
    }));
  }
  let memories = _normalizedCache;

  // Apply team+scope filtering when requested
  if (applyTeamFilter) {
    const teamId = getCurrentTeam();
    memories = filterByTeamAndScope(memories, scope);
  }

  return memories;
}

// Sync access to raw (non-normalized) memories - for internal use only
export function getAllMemoriesRaw() {
  return memoryCache.get('all') || [];
}

/**
 * Invalidate cache
 */
export function invalidateCache() {
  memoryCache.delete('all');
}

/**
 * Add a new memory
 * @param {Omit<Memory, 'id' | 'created_at' | 'updated_at' | 'access_count' | 'last_access'>} mem
 * @returns {Memory}
 */
export async function addMemory(mem) {
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    return gw.writeMemory({
      text: mem.text,
      category: mem.category || 'general',
      importance: mem.importance || 0.5,
      scope: mem.scope,
      scopeId: mem.scopeId,
      tags: mem.tags,
    });
  }

  const now = Date.now();

  // v3.2: Auto-tag with agent_id if in AGENT scope
  const scope = mem.scope || 'USER';
  const agentId = scope === 'AGENT' ? mem.agent_id || getCurrentAgentId() : null;

  /** @type {Memory} */
  const newMem = {
    id: `mem_${now}_${Math.random().toString(36).slice(2, 8)}`,
    text: mem.text,
    category: mem.category || 'general',
    importance: mem.importance || 0.5,
    tags: mem.tags || [],
    scope,
    ...(agentId ? { agent_id: agentId } : {}),
    created_at: now,
    updated_at: now,
    access_count: 0,
    last_access: now,
  };

  // JSON backend
  const memories = await getAllMemories();
  memories.push(newMem);

  // WAL: log individual add op before save (crash recovery = replay add)
  if (global._walInit) {
    logWriteOp({ type: 'add', memory: newMem });
  }

  // 使用原子事务管理器保证双写一致性
  const txManager = getTransactionManager();
  const transactionId = await txManager.beginTransaction();
  
  try {
    // 阶段1：准备 JSON 写入
    await txManager.prepareJsonWrite(transactionId, newMem);
    
    // 阶段2：准备向量写入（如果有 embedding）
    const vectorMem = await getVectorMem();
    if (vectorMem && mem.embedding) {
      await txManager.prepareVectorWrite(transactionId, newMem, mem.embedding);
    }
    
    // 阶段3：提交事务 - 原子性写入两个存储
    await saveMemories(memories);
    
    // 阶段4：执行向量写入（在事务保护下）
    if (vectorMem && mem.embedding) {
      try {
        await vectorMem.upsert({
          id: newMem.id,
          text: newMem.text,
          embedding: mem.embedding,
          created_at: now,
        });
      } catch (vectorError) {
        console.error(`[storage] Vector upsert failed for memory ${newMem.id}:`, vectorError.message);
        // 向量写入失败，需要回滚 JSON 写入
        const currentMemories = await getAllMemories();
        const updatedMemories = currentMemories.filter(m => m.id !== newMem.id);
        await saveMemories(updatedMemories);
        throw new Error(`Vector store write failed: ${vectorError.message}`);
      }
    }
    
    // 阶段5：提交事务
    await txManager.commitTransaction(transactionId);
    
  } catch (error) {
    // 事务失败，回滚
    console.error(`[storage] Atomic write failed for memory ${newMem.id}:`, error.message);
    
    // 从内存缓存中移除（如果已添加）
    const currentMemories = await getAllMemories();
    const updatedMemories = currentMemories.filter(m => m.id !== newMem.id);
    await saveMemories(updatedMemories);
    
    // 回滚事务
    await txManager.rollbackTransaction(transactionId, error);
    
    throw new Error(`Failed to write memory atomically: ${error.message}`);
  }

  return newMem;
}

/**
 * Delete a memory by id
 * @param {string} id
 * @returns {boolean}
 */
export async function deleteMemory(id) {
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    return gw.deleteMemory(id);
  }

  // JSON backend
  const memories = await getAllMemories();
  const idx = memories.findIndex((m) => m.id === id);
  if (idx === -1) return false;
  memories.splice(idx, 1);

  // WAL: log individual delete op before save
  if (global._walInit) {
    logWriteOp({ type: 'delete', memory_id: id });
  }

  await saveMemories(memories);

  // Sync delete to LanceDB vector store
  getVectorMem().then(vm => {
    if (vm) vm.delete(id).catch(e => console.warn('[storage→LanceDB] delete failed:', e.message));
  }).catch(() => {});

  return true;
}

/**
 * Permanently forget a memory (for lifecycle/forgetting mechanism).
 * Triggers when significance < 0.05.
 * - Removes from memory store
 * - Removes from vector index cache (by text hash)
 * - Logs WAL "FORGET" operation
 * @param {string} memoryId
 * @returns {boolean}
 */
export function forget(memoryId) {
  const memories = getAllMemoriesRaw();
  const mem = memories.find((m) => m.id === memoryId);
  if (!mem) return false;

  // Remove from vector cache if text is available
  if (mem.text) {
    try {
      const hash = hashTextForCache(mem.text);
      const cacheFile = join(config.vectorCacheDir, `${hash}.json`);
      if (existsSync(cacheFile)) {
        unlinkSync(cacheFile);
      }
    } catch { /* ignore cache cleanup errors */ }
  }

  // Remove from in-memory memories list
  const idx = memories.findIndex((m) => m.id === memoryId);
  if (idx !== -1) memories.splice(idx, 1);

  // WAL: log FORGET op (significance = importance field)
  if (global._walInit) {
    logWriteOp({ type: 'FORGET', memory_id: memoryId, significance: mem.importance });
  }

  saveMemories(memories);
  return true;
}

/**
 * Hash text to match vector cache key format (same as vector.js getEmbeddingCached)
 * @param {string} text
 * @returns {string}
 */
function hashTextForCache(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    const char = text.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}

/**
 * Get a memory by id
 * @param {string} id
 * @returns {Memory|undefined}
 */
export async function getMemory(id) {
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    return gw.getMemory(id);
  }
  const memories = await getAllMemories();
  return memories.find((m) => m.id === id);
}

/**
 * Update access stats
 * @param {string} id
 */
export async function updateMemory(updatedMem) {
  if (isSqliteMode()) {
    const gw = await getV4Gw();
    const existing = await gw.getMemory(updatedMem.id);
    if (!existing) return false;
    // StorageGateway.writeMemory acts as upsert
    return gw.writeMemory({
      text: updatedMem.text ?? existing.text,
      category: updatedMem.category ?? existing.category,
      importance: updatedMem.importance ?? existing.importance,
      scope: updatedMem.scope ?? existing.scope_type,
      scopeId: updatedMem.scopeId ?? existing.scope_id,
      tags: updatedMem.tags ?? existing.tags,
      id: updatedMem.id,
    });
  }
  const memories = await getAllMemories();
  const idx = memories.findIndex((m) => m.id === updatedMem.id);
  if (idx === -1) return false;
  const oldMemory = { ...memories[idx] }; // 保存旧版本用于创建 diff
  memories[idx] = { ...memories[idx], ...updatedMem };
  await saveMemories(memories);
  // v2.7.0: 每次更新自动创建版本记录
  createMemoryVersion(updatedMem.id, memories[idx], oldMemory, 'update');

  // P1-6: Sync text changes to vector store (old embedding is cleaned up by upsert's delete)
  if (updatedMem.text !== undefined) {
    getVectorMem().then(vm => {
      if (vm) vm.upsert({
        id: updatedMem.id,
        text: updatedMem.text,
        category: memories[idx].category,
        scope: memories[idx].scope,
        importance: memories[idx].importance,
        created_at: memories[idx].created_at,
      }).catch(e => console.warn('[storage→LanceDB] update upsert failed:', e.message));
    }).catch(() => {});
  }
  return true;
}

export function touchMemory(id) {
  if (isSqliteMode()) {
    const backend = _sqliteBackend || null;
    if (backend) {
      backend.touchMemoryById(id);
      return;
    }
  }
  const memories = getAllMemoriesRaw();
  const mem = memories.find((m) => m.id === id);
  if (mem) {
    mem.access_count = (mem.access_count || 0) + 1;
    mem.last_access = Date.now();
    // WAL: log access op (for quality scoring / access tracking in recovery)
    if (global._walInit) {
      logWriteOp({ type: 'access', memory_id: id });
    }
    saveMemories(memories);
  }
}

// ============================================================
// v3.4: PIN 记忆系统 — 重要记忆永不丢失
// ============================================================

const PIN_REASON_MAX = 200; // reason 最大长度

/**
 * 锁定一条记忆（不被压缩/删除）
 * @param {string} id
 * @param {string} reason 锁定原因
 * @returns {boolean}
 */
export function pinMemory(id, reason = '') {
  if (isSqliteMode()) {
    const backend = _sqliteBackend || null;
    if (backend) {
      const pinned = backend.pinMemoryById(id, reason);
      if (pinned) { getAllMemories().then(data => { memoryCache.set('all', data); _normalizedCache = null; }); }
      return pinned;
    }
  }
  const memories = getAllMemoriesRaw();
  const mem = memories.find(m => m.id === id);
  if (!mem) return false;
  mem.pinned = true;
  mem.pinnedAt = Date.now();
  mem.pinnedReason = String(reason).slice(0, PIN_REASON_MAX);
  if (global._walInit) {
    logWriteOp({ type: 'pin', memory_id: id, reason: mem.pinnedReason });
  }
  saveMemories(memories);
  return true;
}

/**
 * 解锁一条记忆
 * @param {string} id
 * @returns {boolean}
 */
export function unpinMemory(id) {
  if (isSqliteMode()) {
    const backend = _sqliteBackend || null;
    if (backend) {
      const unpinned = backend.unpinMemoryById(id);
      if (unpinned) { getAllMemories().then(data => { memoryCache.set('all', data); _normalizedCache = null; }); }
      return unpinned;
    }
  }
  const memories = getAllMemoriesRaw();
  const mem = memories.find(m => m.id === id);
  if (!mem) return false;
  mem.pinned = false;
  mem.pinnedAt = null;
  mem.pinnedReason = null;
  if (global._walInit) {
    logWriteOp({ type: 'unpin', memory_id: id });
  }
  saveMemories(memories);
  return true;
}

/**
 * 获取所有 PIN 记忆
 * @returns {Array}
 */
export function getPinnedMemories() {
  if (isSqliteMode()) {
    const backend = _sqliteBackend || null;
    if (backend) return backend.getPinnedMemories();
  }
  return getAllMemoriesRaw().filter(m => m.pinned);
}

// ============================================================
// v2.7.0: 完整修订历史 (Version History) — 增量 diff 存储
// ============================================================
// 注意：readFileSync/writeFileSync/existsSync/mkdirSync 已在上方导入

const WORKSPACE = process.env.OPENCLAW_WORKSPACE_DIR ?? join(process.env.HOME ?? '/root', '.openclaw', 'workspace');
const VERSIONS_FILE = join(WORKSPACE, 'memory', 'memory_versions.json');
const MAX_VERSIONS = 10; // 保留最近 10 个版本
const VERSIONS_WRITE_DELAY_MS = 500;
let _versionsTimer = null;
let _pendingVersionStore = null;

/** 加载版本存储 */
export function loadVersionStore() {
  // Clear any pending version store write before reading
  if (_versionsTimer) { clearTimeout(_versionsTimer); _versionsTimer = null; }
  _pendingVersionStore = null;
  if (!existsSync(VERSIONS_FILE)) {
    return {};
  }
  try {
    return JSON.parse(readFileSync(VERSIONS_FILE, 'utf8'));
  } catch (err) {
    console.error('[storage:versions] Load error:', err.message);
    return {};
  }
}

/** 持久化版本存储 (write-behind, debounced) */
function persistVersionStore(store) {
  _pendingVersionStore = store;
  if (_versionsTimer) clearTimeout(_versionsTimer);
  _versionsTimer = setTimeout(() => {
    _flushVersionStore().catch(err => console.error('[storage:versions] flush error:', err.message));
  }, VERSIONS_WRITE_DELAY_MS);
}

async function _flushVersionStore() {
  if (!_pendingVersionStore) return;
  const store = _pendingVersionStore;
  _pendingVersionStore = null;
  _versionsTimer = null;
  try {
    const dir = join(WORKSPACE, 'memory');
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    const tmpPath = `${VERSIONS_FILE}.tmp.${process.pid}.${Date.now()}`;
    await writeFile(tmpPath, JSON.stringify(store, null, 2), 'utf8');
    await rename(tmpPath, VERSIONS_FILE);
  } catch (err) {
    console.error('[storage:versions] Persist error:', err.message);
  }
}

/** Flush pending version store writes */
export async function flushVersionStore() {
  if (_versionsTimer) { clearTimeout(_versionsTimer); _versionsTimer = null; }
  if (_pendingVersionStore) await _flushVersionStore();
}

/** 生成版本 ID */
function genVersionId() {
  return `v_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
}

/**
 * 计算两个内容的增量 diff（行级 diff，无外部依赖）
 * @param {any} oldContent
 * @param {any} newContent
 * @returns {{ added: string[], removed: string[], addedCount: number, removedCount: number }}
 */
function computeDiff(oldContent, newContent) {
  const oldText = typeof oldContent === 'string' ? oldContent : JSON.stringify(oldContent, null, 2);
  const newText = typeof newContent === 'string' ? newContent : JSON.stringify(newContent, null, 2);

  const oldLines = oldText.split('\n');
  const newLines = newText.split('\n');

  const oldSet = new Set(oldLines);
  const newSet = new Set(newLines);

  const diff = { added: [], removed: [] };
  for (const line of newLines) {
    if (!oldSet.has(line)) diff.added.push(line);
  }
  for (const line of oldLines) {
    if (!newSet.has(line)) diff.removed.push(line);
  }
  diff.addedCount = diff.added.length;
  diff.removedCount = diff.removed.length;
  return diff;
}

/**
 * 创建记忆版本的快照（完整内容，用于最终重建）
 * @param {string} memoryId
 * @param {object} newMemory 更新后的完整记忆
 * @param {object|null} oldMemory 更新前的完整记忆（可选）
 * @param {'update'|'create'|'restore'} changeType
 */
function createMemoryVersion(memoryId, newMemory, oldMemory = null, changeType = 'update') {
  const store = loadVersionStore();

  if (!store[memoryId]) {
    store[memoryId] = { versions: [] };
  }

  const versions = store[memoryId].versions;
  const latest = versions[versions.length - 1];

  // 计算与上一个版本的增量 diff
  let diffFromPrev = null;
  if (latest && oldMemory) {
    diffFromPrev = computeDiff(latest.content, newMemory);
  } else if (!latest && newMemory) {
    diffFromPrev = computeDiff({}, newMemory);
  }

  const version = {
    versionId: genVersionId(),
    content: { ...newMemory }, // 完整快照（简化实现，不依赖 jsondiffpatch）
    timestamp: Date.now(),
    changeType,
    diffFromPrev,
  };

  versions.push(version);

  // 保留最近 MAX_VERSIONS 个版本
  if (versions.length > MAX_VERSIONS) {
    versions.splice(0, versions.length - MAX_VERSIONS);
  }

  persistVersionStore(store);
  return version;
}

/**
 * 获取记忆的所有版本历史（摘要列表）
 * @param {string} memoryId
 * @returns {Array<{versionId: string, timestamp: number, changeType: string, diffFromPrev: object|null}>}
 */
export function getMemoryVersions(memoryId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data) return [];
  return data.versions.map((v) => ({
    versionId: v.versionId,
    timestamp: v.timestamp,
    changeType: v.changeType,
    diffFromPrev: v.diffFromPrev
      ? { addedCount: v.diffFromPrev.addedCount, removedCount: v.diffFromPrev.removedCount }
      : null,
  }));
}

/**
 * 获取指定版本详情
 * @param {string} memoryId
 * @param {string} versionId
 * @returns {object|null}
 */
export function getMemoryVersion(memoryId, versionId) {
  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data) return null;
  return data.versions.find((v) => v.versionId === versionId) || null;
}

/**
 * 恢复到指定版本
 * @param {string} memoryId
 * @param {string} versionId
 * @returns {{ success: boolean, restoredTo?: object, error?: string }}
 */
export function restoreMemoryVersion(memoryId, versionId) {
  const memories = getAllMemoriesRaw();
  const memIdx = memories.findIndex((m) => m.id === memoryId);
  if (memIdx === -1) {
    return { success: false, error: `Memory ${memoryId} not found` };
  }

  const store = loadVersionStore();
  const data = store[memoryId];
  if (!data) {
    return { success: false, error: `No version history for ${memoryId}` };
  }

  const version = data.versions.find((v) => v.versionId === versionId);
  if (!version) {
    return { success: false, error: `Version ${versionId} not found` };
  }

  const oldMemory = { ...memories[memIdx] };

  // 用旧版本内容覆盖当前记忆
  const restoredMemory = {
    ...memories[memIdx],
    ...version.content,
    updated_at: Date.now(),
  };
  memories[memIdx] = restoredMemory;
  saveMemories(memories);

  // 在版本历史中记录本次恢复操作
  createMemoryVersion(memoryId, restoredMemory, oldMemory, 'restore');

  return {
    success: true,
    restoredTo: { versionId: version.versionId, timestamp: version.timestamp },
    changeType: version.changeType,
  };
}

/**
 * 获取版本统计
 * @returns {{ totalVersions: number, totalMemories: number, memoryCounts: object }}
 */
export function getVersionStats() {
  const store = loadVersionStore();
  let totalVersions = 0;
  const counts = {};
  for (const [memoryId, data] of Object.entries(store)) {
    counts[memoryId] = data.versions.length;
    totalVersions += data.versions.length;
  }
  return {
    totalVersions,
    totalMemories: Object.keys(store).length,
    memoryCounts: counts,
  };
}

/**
 * 比较两个版本的差异
 * @param {string} memoryId
 * @param {string} versionId1
 * @param {string} versionId2
 * @returns {object}
 */
export function compareMemoryVersions(memoryId, versionId1, versionId2) {
  const v1 = getMemoryVersion(memoryId, versionId1);
  const v2 = getMemoryVersion(memoryId, versionId2);
  if (!v1 || !v2) {
    throw new Error('One or both versions not found');
  }
  const diff = computeDiff(v1.content, v2.content);
  return {
    memoryId,
    fromVersion: { versionId: v1.versionId, timestamp: v1.timestamp },
    toVersion: { versionId: v2.versionId, timestamp: v2.timestamp },
    diff,
  };
}

/**
 * 获取版本总数
 * @param {string} memoryId
 * @returns {number}
 */
export function getMemoryVersionCount(memoryId) {
  const store = loadVersionStore();
  return store[memoryId]?.versions.length || 0;
}

export default {
  loadMemories,
  saveMemories,
  getAllMemories,
  invalidateCache,
  addMemory,
  deleteMemory,
  forget,
  getMemory,
  updateMemory,
  touchMemory,
  // v2.7.0 版本历史
  getMemoryVersions,
  getMemoryVersion,
  restoreMemoryVersion,
  getVersionStats,
  compareMemoryVersions,
  getMemoryVersionCount,
  loadVersionStore,
};
