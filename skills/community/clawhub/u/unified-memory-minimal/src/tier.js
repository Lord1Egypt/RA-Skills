/**
 * Tier Manager - HOT(7d) / WARM(7-30d) / COLD(>30d) 三层架构
 * Automatic tier assignment and redistribution
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from './config.js';
import { getAllMemories, saveMemories, forget as storageForget } from './storage.js';

export const TIER_CONFIG = {
  HOT: { maxAgeDays: 7, compress: false, priority: 3 },
  WARM: { maxAgeDays: 30, compress: false, priority: 2 },
  COLD: { maxAgeDays: Infinity, compress: true, priority: 1 },
};

const DAY_MS = 86400000;

function parseTimestamp(memory) {
  const raw = memory.timestamp || memory.created_at || memory.createdAt || Date.now();
  // Handle ISO string format from Python
  if (typeof raw === 'string') return new Date(raw).getTime();
  return raw;
}

function getTier(memory, now = Date.now()) {
  const ts = parseTimestamp(memory);
  const age = now - ts;
  const ageDays = age / DAY_MS;
  if (ageDays <= TIER_CONFIG.HOT.maxAgeDays) return 'HOT';
  if (ageDays <= TIER_CONFIG.WARM.maxAgeDays) return 'WARM';
  return 'COLD';
}

/**
 * Assign tier to each memory
 * @param {Array} memories
 * @returns {Array} memories with .tier field added
 */
export function assignTiers(memories, now = Date.now()) {
  return memories.map(m => ({ ...m, tier: getTier(m, now) }));
}

/**
 * Partition memories by tier
 * @param {Array} memories
 * @returns {{ HOT: Array, WARM: Array, COLD: Array }}
 */
export function partitionByTier(memories) {
  const tiers = { HOT: [], WARM: [], COLD: [] };
  for (const m of assignTiers(memories)) {
    tiers[m.tier].push(m);
  }
  return tiers;
}

/**
 * Redistribute all memories across tiers (full re-tier)
 * @param {Array} memories
 * @returns {Array}
 */
export function redistributeTiers(memories) {
  return assignTiers(memories);
}

/**
 * Compress cold tier memories (summarize / drop details)
 * Uses summarization to reduce storage while keeping essential meaning.
 * @param {Array} coldMemories
 * @returns {Array}
 */
export function compressColdTier(coldMemories) {
  return coldMemories.map(m => {
    // Pinned memories — skip compression entirely
    if (m.pinned) return m;
    // Already compressed — skip
    if (m.compressed) return m;

    const text = m.text || '';
    // Keep first 200 chars as rough summary
    const summary = text.length > 200 ? text.slice(0, 200) : text;

    return {
      ...m,
      compressed: true,
      original_length: text.length,
      // Keep essential fields
      id: m.id,
      text: summary,
      category: m.category,
      importance: m.importance,
      tags: m.tags || [],
      scope: m.scope,
      timestamp: m.timestamp,
      created_at: m.created_at,
      tier: 'COLD',
      // Drop heavy fields to save space
      embedding: undefined,
      last_access: undefined,
    };
  });
}

/**
 * Automatic tier migration based on access frequency and importance.
 * Heuristics:
 * - HOT → WARM: not accessed in 3+ days and importance < 0.5
 * - HOT → COLD: not accessed in 7+ days and importance < 0.3
 * - WARM → HOT: accessed in last 2 days and importance >= 0.5
 * - WARM → COLD: not accessed in 14+ days
 * - COLD → WARM: accessed in last 7 days and importance >= 0.4
 * - COLD → HOT: accessed in last 2 days and importance >= 0.7
 *
 * @param {Array} memories - All memories
 * @param {{ dryRun?: boolean }} options
 * @returns {{ memories: Array, changes: Array }}
 */
export function autoMigrateTiers(memories, { dryRun = false } = {}) {
  const now = Date.now();
  const DAY_MS = 86400000;
  const changes = [];

  // Work on a copy
  const updated = memories.map(m => ({ ...m }));
  const tierMap = new Map(updated.map(m => [m.id, getTier(m, now)]));

  for (const mem of updated) {
    const currentTier = tierMap.get(mem.id);
    const lastAcc = mem.last_access || mem.lastAccess || mem.timestamp || mem.created_at || mem.createdAt || now;
    const lastAccTs = typeof lastAcc === 'string' ? new Date(lastAcc).getTime() : lastAcc;
    const daysSinceAccess = (now - lastAccTs) / DAY_MS;
    const importance = mem.importance || 0.5;
    let newTier = currentTier;

    // Pinned memories: always stay in HOT, never demote
    if (mem.pinned) newTier = 'HOT';

    if (currentTier === 'HOT') {
      // Demote HOT → WARM or HOT → COLD
      if (daysSinceAccess >= 7 && importance < 0.3) {
        newTier = 'COLD';
      } else if (daysSinceAccess >= 3 && importance < 0.5) {
        newTier = 'WARM';
      }
    } else if (currentTier === 'WARM') {
      // Promote WARM → HOT or demote WARM → COLD
      if (daysSinceAccess <= 2 && importance >= 0.5) {
        newTier = 'HOT';
      } else if (daysSinceAccess >= 14) {
        newTier = 'COLD';
      }
    } else if (currentTier === 'COLD') {
      // Promote COLD → WARM or COLD → HOT
      if (daysSinceAccess <= 2 && importance >= 0.7) {
        newTier = 'HOT';
      } else if (daysSinceAccess <= 7 && importance >= 0.4) {
        newTier = 'WARM';
      }
    }

    if (newTier !== currentTier) {
      const reason = `${currentTier} → ${newTier}: daysSinceAccess=${Math.round(daysSinceAccess * 10) / 10}, importance=${importance}`;
      changes.push({ id: mem.id, fromTier: currentTier, toTier: newTier, reason, memory: mem });
      tierMap.set(mem.id, newTier);
      mem.tier = newTier;
    }
  }

  return { memories: updated, changes };
}

/**
 * Get tier stats
 * @param {Array} memories
 * @returns {{ HOT: number, WARM: number, COLD: number, total: number }}
 */
export function getTierStats(memories) {
  const tiers = partitionByTier(memories);
  return {
    HOT: tiers.HOT.length,
    WARM: tiers.WARM.length,
    COLD: tiers.COLD.length,
    total: memories.length,
  };
}

/**
 * Run lifecycle management — called by proactive_manager every 100 operations.
 * Handles:
 * 1. Archiving COLD memories older than 90 days (export summary to archive/)
 * 2. Forgetting COLD memories with significance < 0.05
 * 3. Forgetting WARM memories with significance < 0.05
 * 4. Natural decay: 30-day inactive memories get significance *= 0.95
 * @returns {{ archived: number, forgotten: number, decayed: number }}
 */
export function runLifecycle() {
  const ARCHIVE_DIR = join(config.memoryDir || process.env.HOME + '/.unified-memory', 'archive');
  const DAY_MS = 86400000;
  const now = Date.now();

  // Ensure archive directory exists
  if (!existsSync(ARCHIVE_DIR)) {
    mkdirSync(ARCHIVE_DIR, { recursive: true });
  }

  const memories = getAllMemories();
  const tiers = partitionByTier(memories);

  let archived = 0;
  let forgotten = 0;
  let decayed = 0;

  // ── 1. Archive + forget COLD memories > 90 days old ──
  const ninetyDaysMs = 90 * DAY_MS;
  for (const mem of tiers.COLD) {
    const created = mem.created_at || mem.timestamp || now;
    if (now - created > ninetyDaysMs) {
      // Archive: save summary to archive directory
      try {
        const archiveFile = join(ARCHIVE_DIR, `${mem.id}.json`);
        const summary = {
          id: mem.id,
          text: mem.text || '',
          summary: mem.text ? mem.text.slice(0, 200) : '',
          category: mem.category,
          importance: mem.importance || 0.5,
          created_at: created,
          archived_at: now,
        };
        writeFileSync(archiveFile, JSON.stringify(summary, null, 2), 'utf8');
        archived++;
      } catch (e) {
        log('WARN', `[runLifecycle] archive failed for ${mem.id}: ${e.message}`);
      }
      // Forget: remove from store + vector cache
      storageForget(mem.id);
      forgotten++;
    }
  }

  // ── 2. Forget COLD memories with significance < 0.05 ──
  for (const mem of tiers.COLD) {
    const created = mem.created_at || mem.timestamp || now;
    if (now - created <= ninetyDaysMs && (mem.importance || 0.5) < 0.05) {
      storageForget(mem.id);
      forgotten++;
    }
  }

  // ── 3. Forget WARM memories with significance < 0.05 ──
  for (const mem of tiers.WARM) {
    if ((mem.importance || 0.5) < 0.05) {
      storageForget(mem.id);
      forgotten++;
    }
  }

  // ── 4. Natural decay: memories not accessed in 30+ days get significance *= 0.95 ──
  const thirtyDaysMs = 30 * DAY_MS;
  for (const mem of memories) {
    const lastAccess = mem.last_access || mem.updated_at || mem.created_at || now;
    if (now - lastAccess > thirtyDaysMs) {
      const currentImportance = mem.importance || 0.5;
      mem.importance = Math.max(0, currentImportance * 0.95);
      decayed++;
    }
  }

  if (decayed > 0) {
    saveMemories(memories);
  }

  log('INFO', `[runLifecycle] archived=${archived} forgotten=${forgotten} decayed=${decayed}`);
  return { archived, forgotten, decayed };
}

export default { TIER_CONFIG, getTier, assignTiers, partitionByTier, redistributeTiers, compressColdTier, getTierStats, runLifecycle, autoMigrateTiers };
