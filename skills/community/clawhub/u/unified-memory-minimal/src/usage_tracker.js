/**
 * usage_tracker.js - Track memory retrieval and usage for dynamic importance scoring
 *
 * Stores per-memory usage statistics in:
 *   ~/.openclaw/workspace/memory/usage_stats.json
 *
 * Data structure per memory:
 *   {
 *     memoryId: string,
 *     retrievalCount: number,   // times this memory appeared in search results
 *     usageCount: number,      // times this memory was actually used (selected by user / in final response)
 *     lastRetrieved: number,   // timestamp ms
 *     lastUsed: number,        // timestamp ms
 *     utilityScore: number,     // usageCount / retrievalCount (0-1)
 *     manualBoost: number,      // manual boost applied via memory_boost tool (0-1)
 *     createdAt: number,        // timestamp ms when stats were first created
 *   }
 *
 * Utility score formula: usageCount / retrievalCount (0-1 range)
 *   - Higher ratio = memory is consistently useful when retrieved
 *   - 0 = retrieved many times but never used (might be noise)
 *   - 1 = always used when retrieved (high-value memory)
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { setTimeout as sleep } from 'timers/promises';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const USAGE_STATS_FILE = join(MEMORY_DIR, 'usage_stats.json');

/** @type {Map<string, object>} In-memory cache of usage stats */
const statsCache = new Map();

/** @type {Map<string, number>} Dirty keys pending write (debounce) */
const dirtyKeys = new Set();

/** @type {NodeJS.Timeout|null} Debounce flush timer */
let flushTimer = null;

/** Debounce flush interval in ms */
const FLUSH_INTERVAL_MS = 2000;

// ─── File I/O ───────────────────────────────────────────────────────────────

/**
 * Load all usage stats from disk into memory cache.
 * Returns a Map of memoryId -> stats object.
 * @returns {Map<string, object>}
 */
function loadAll() {
  if (!existsSync(USAGE_STATS_FILE)) {
    return new Map();
  }
  try {
    const raw = readFileSync(USAGE_STATS_FILE, 'utf-8');
    const arr = JSON.parse(raw);
    if (!Array.isArray(arr)) return new Map();
    const map = new Map();
    for (const entry of arr) {
      if (entry && entry.memoryId) {
        map.set(entry.memoryId, entry);
      }
    }
    return map;
  } catch {
    return new Map();
  }
}

/**
 * Save all current in-memory stats to disk.
 * Called on debounced flush.
 */
function saveAll() {
  try {
    const arr = Array.from(statsCache.values());
    writeFileSync(USAGE_STATS_FILE, JSON.stringify(arr, null, 2), 'utf-8');
  } catch {
    // Non-fatal - log would be noisy
  }
}

// ─── Public API ─────────────────────────────────────────────────────────────

/**
 * Initialize usage stats for a newly stored memory.
 * Called by storage.addMemory().
 * @param {string} memoryId
 */
export function initUsageStats(memoryId) {
  if (statsCache.size === 0) {
    // Lazy-load on first call
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }

  if (statsCache.has(memoryId)) {
    return; // Already initialized
  }

  const now = Date.now();
  /** @type {object} */
  const entry = {
    memoryId,
    retrievalCount: 0,
    usageCount: 0,
    lastRetrieved: null,
    lastUsed: null,
    utilityScore: 0,
    manualBoost: 0,
    createdAt: now,
  };

  statsCache.set(memoryId, entry);
  dirtyKeys.add(memoryId);
  scheduleFlush();
}

/**
 * Mark a memory as retrieved (appeared in search results).
 * Called by search pipeline after RRF fusion.
 * @param {string} memoryId
 */
export function markRetrieved(memoryId) {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }

  let entry = statsCache.get(memoryId);
  if (!entry) {
    // Memory not in stats (e.g., loaded from old file) — init silently
    entry = {
      memoryId,
      retrievalCount: 0,
      usageCount: 0,
      lastRetrieved: null,
      lastUsed: null,
      utilityScore: 0,
      manualBoost: 0,
      createdAt: Date.now(),
    };
    statsCache.set(memoryId, entry);
  }

  entry.retrievalCount += 1;
  entry.lastRetrieved = Date.now();
  entry.utilityScore = entry.usageCount / entry.retrievalCount;

  dirtyKeys.add(memoryId);
  scheduleFlush();
}

/**
 * Mark a memory as used (selected by user / appeared in final response).
 * Called when user gives positive feedback (thumbs up / confirms).
 * Also called automatically when memory appears in final search results
 * that are returned to the user.
 * @param {string} memoryId
 */
export function markUsed(memoryId) {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }

  let entry = statsCache.get(memoryId);
  if (!entry) {
    entry = {
      memoryId,
      retrievalCount: 0,
      usageCount: 0,
      lastRetrieved: null,
      lastUsed: null,
      utilityScore: 0,
      manualBoost: 0,
      createdAt: Date.now(),
    };
    statsCache.set(memoryId, entry);
  }

  entry.usageCount += 1;
  entry.lastUsed = Date.now();
  // Recalculate utility score: usage / retrieval
  // Handle case where retrievalCount might be 0
  entry.utilityScore = entry.retrievalCount > 0
    ? entry.usageCount / entry.retrievalCount
    : (entry.usageCount > 0 ? 1 : 0);

  dirtyKeys.add(memoryId);
  scheduleFlush();
}

/**
 * Set a manual boost for a memory (via memory_boost tool).
 * @param {string} memoryId
 * @param {number} boost - boost value 0-1
 */
export function setManualBoost(memoryId, boost) {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }

  let entry = statsCache.get(memoryId);
  if (!entry) {
    entry = {
      memoryId,
      retrievalCount: 0,
      usageCount: 0,
      lastRetrieved: null,
      lastUsed: null,
      utilityScore: 0,
      manualBoost: 0,
      createdAt: Date.now(),
    };
    statsCache.set(memoryId, entry);
  }

  entry.manualBoost = Math.max(0, Math.min(1, boost));
  dirtyKeys.add(memoryId);
  scheduleFlush();
}

/**
 * Get usage stats for a specific memory.
 * @param {string} memoryId
 * @returns {object|null}
 */
export function getUsageStats(memoryId) {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }
  return statsCache.get(memoryId) || null;
}

/**
 * Get all usage stats as an array.
 * @returns {object[]}
 */
export function getAllUsageStats() {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }
  return Array.from(statsCache.values());
}

/**
 * Get usage stats for multiple memory IDs (bulk lookup for search pipeline).
 * @param {string[]} memoryIds
 * @returns {Map<string, object>}
 */
export function getUsageStatsBulk(memoryIds) {
  if (statsCache.size === 0) {
    const loaded = loadAll();
    for (const [id, stats] of loaded) {
      statsCache.set(id, stats);
    }
  }
  const result = new Map();
  for (const id of memoryIds) {
    if (statsCache.has(id)) {
      result.set(id, statsCache.get(id));
    }
  }
  return result;
}

/**
 * Flush any pending writes to disk synchronously.
 * Call on critical paths (e.g., process exit).
 */
export function flushUsageStatsSync() {
  if (flushTimer) {
    clearTimeout(flushTimer);
    flushTimer = null;
  }
  saveAll();
  dirtyKeys.clear();
}

/**
 * Delete usage stats for a memory (called when memory is deleted).
 * @param {string} memoryId
 */
export function deleteUsageStats(memoryId) {
  statsCache.delete(memoryId);
  dirtyKeys.add(memoryId); // mark for removal on next flush
  // Rewrite without this memory
  try {
    const arr = Array.from(statsCache.values()).filter(e => e.memoryId !== memoryId);
    writeFileSync(USAGE_STATS_FILE, JSON.stringify(arr, null, 2), 'utf-8');
  } catch {
    // Non-fatal
  }
}

// ─── Debounce Logic ─────────────────────────────────────────────────────────

/**
 * Schedule a debounced flush of dirty stats to disk.
 * Multiple dirty keys within FLUSH_INTERVAL_MS only trigger one write.
 */
function scheduleFlush() {
  if (flushTimer !== null) {
    return; // Already scheduled
  }
  flushTimer = setTimeout(async () => {
    flushTimer = null;
    const dirty = Array.from(dirtyKeys);
    dirtyKeys.clear();
    if (dirty.length === 0) return;

    // Re-read current file state to avoid overwrites from concurrent processes
    let currentStats = new Map();
    try {
      if (existsSync(USAGE_STATS_FILE)) {
        const raw = readFileSync(USAGE_STATS_FILE, 'utf-8');
        const arr = JSON.parse(raw);
        for (const e of arr) {
          if (e && e.memoryId) currentStats.set(e.memoryId, e);
        }
      }
    } catch {
      // Start fresh
    }

    // Merge: update dirty entries with current cache values
    for (const key of dirty) {
      const entry = statsCache.get(key);
      if (entry) {
        currentStats.set(key, entry);
      } else {
        // Memory was deleted - remove from file
        currentStats.delete(key);
      }
    }

    try {
      writeFileSync(USAGE_STATS_FILE, JSON.stringify(Array.from(currentStats.values()), null, 2), 'utf-8');
    } catch {
      // Non-fatal, stats will be re-flushed on next change
    }
  }, FLUSH_INTERVAL_MS);
}
