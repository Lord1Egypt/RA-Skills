/**
 * importance_scorer.js - Dynamic importance scoring based on multiple signals
 *
 * Combines multiple signals into a final importance score (0-1):
 *   - Static importance (user-provided at store time)
 *   - Utility score (usageCount / retrievalCount — how often memory is actually used)
 *   - Recency boost (memories from last 7 days get +0.1)
 *   - Reference boost (memories frequently cited by other memories get +0.1)
 *   - Category weight boost (PREFERENCE=0.2, FACT=0.15, DECISION=0.25, others=0.1)
 *
 * Formula:
 *   finalImportance =
 *     (static * 0.3) +
 *     (utility * 0.4) +
 *     (recency * 0.1) +
 *     (reference * 0.1) +
 *     (categoryWeight * 0.1)
 *
 * All components are 0-1 range; final clamped to [0, 1].
 */

import { config } from './config.js';
import { getUsageStats, getUsageStatsBulk } from './usage_tracker.js';

// ─── Default weights (can be overridden via config) ───────────────────────────

const DEFAULT_WEIGHTS = {
  static: 0.3,
  utility: 0.4,
  recency: 0.1,
  reference: 0.1,
  category: 0.1,
};

// ─── Category base weights ───────────────────────────────────────────────────

const CATEGORY_BASE_WEIGHTS = {
  preference: 0.2,
  decision: 0.25,
  fact: 0.15,
  entity: 0.1,
  reflection: 0.1,
  other: 0.1,
};

// ─── Recency window in ms (7 days) ─────────────────────────────────────────
const RECENCY_WINDOW_MS = 7 * 24 * 60 * 60 * 1000;

// ─── Reference counting (cross-memory citations) ─────────────────────────────
// We track how many other memories reference each memory via a simple
// in-memory map. Updated by storage.js when memories are stored/linked.

/** @type {Map<string, number>} memoryId -> reference count */
const referenceCounts = new Map();

/**
 * Increment the reference count for a target memory.
 * Called when one memory references another (e.g., in reflection/lessons).
 * @param {string} memoryId
 * @param {number} [delta=1]
 */
export function incrementReference(memoryId, delta = 1) {
  const current = referenceCounts.get(memoryId) || 0;
  referenceCounts.set(memoryId, current + delta);
}

/**
 * Get the reference count for a memory.
 * @param {string} memoryId
 * @returns {number}
 */
export function getReferenceCount(memoryId) {
  return referenceCounts.get(memoryId) || 0;
}

// ─── Component calculators ─────────────────────────────────────────────────

/**
 * Get the recency signal for a memory.
 * @param {object} memory - Memory object with created_at field
 * @returns {number} 0-1; 1 if created within last 7 days, 0 otherwise
 */
function getRecencySignal(memory) {
  const age = Date.now() - (memory.created_at || memory.timestamp || Date.now());
  return age <= RECENCY_WINDOW_MS ? 1 : 0;
}

/**
 * Get the reference signal for a memory.
 * Reference boost is 1 if memory has been cited by >= 2 other memories.
 * @param {string} memoryId
 * @returns {number} 0-1
 */
function getReferenceSignal(memoryId) {
  const count = referenceCounts.get(memoryId) || 0;
  return count >= 2 ? 1 : (count >= 1 ? 0.5 : 0);
}

/**
 * Get the category weight signal.
 * @param {string} category
 * @returns {number} 0-1
 */
function getCategorySignal(category) {
  const base = CATEGORY_BASE_WEIGHTS[category?.toLowerCase()] ?? CATEGORY_BASE_WEIGHTS.other;
  return base; // Already 0-1 scaled
}

/**
 * Get the utility score from usage stats.
 * @param {object|null} usageStats
 * @returns {number} 0-1
 */
function getUtilitySignal(usageStats) {
  if (!usageStats) return 0;
  // utilityScore is precomputed as usageCount/retrievalCount
  return typeof usageStats.utilityScore === 'number'
    ? usageStats.utilityScore
    : 0;
}

/**
 * Get the manual boost signal.
 * @param {object|null} usageStats
 * @returns {number} 0-1
 */
function getManualBoostSignal(usageStats) {
  if (!usageStats) return 0;
  return typeof usageStats.manualBoost === 'number' ? usageStats.manualBoost : 0;
}

// ─── Main scorer ────────────────────────────────────────────────────────────

/**
 * Get the dynamic importance score for a single memory.
 *
 * @param {object} memory - Memory object with: id, importance (static), category, created_at
 * @param {object} [usageStats] - Optional pre-fetched usage stats
 * @returns {{ finalImportance: number, breakdown: object }}
 */
export function scoreMemory(memory, usageStats = null) {
  const weights = config.importanceWeights || DEFAULT_WEIGHTS;

  // 1. Static importance (user-provided at store time)
  const staticImportance = typeof memory.importance === 'number'
    ? Math.max(0, Math.min(1, memory.importance))
    : 0.5;

  // 2. Utility signal (from usage tracker)
  const stats = usageStats !== null ? usageStats : getUsageStats(memory.id);
  const utility = getUtilitySignal(stats);

  // 3. Recency signal
  const recency = getRecencySignal(memory);

  // 4. Reference signal
  const reference = getReferenceSignal(memory.id);

  // 5. Category weight signal
  const categoryWeight = getCategorySignal(memory.category);

  // 6. Manual boost (override/additive)
  const manualBoost = getManualBoostSignal(stats);

  // Final formula
  const raw = (
    (staticImportance * weights.static) +
    (utility * weights.utility) +
    (recency * weights.recency) +
    (reference * weights.reference) +
    (categoryWeight * weights.category)
  );

  // Apply manual boost additively after formula, then clamp
  const withBoost = Math.max(0, Math.min(1, raw + manualBoost * 0.1));

  return {
    finalImportance: withBoost,
    breakdown: {
      static: {
        value: staticImportance,
        weight: weights.static,
        contribution: staticImportance * weights.static,
      },
      utility: {
        value: utility,
        weight: weights.utility,
        contribution: utility * weights.utility,
        retrievalCount: stats?.retrievalCount || 0,
        usageCount: stats?.usageCount || 0,
      },
      recency: {
        value: recency,
        weight: weights.recency,
        contribution: recency * weights.recency,
        ageDays: memory.created_at
          ? Math.round((Date.now() - memory.created_at) / (24 * 60 * 60 * 1000))
          : null,
      },
      reference: {
        value: reference,
        weight: weights.reference,
        contribution: reference * weights.reference,
        referenceCount: referenceCounts.get(memory.id) || 0,
      },
      category: {
        value: categoryWeight,
        weight: weights.category,
        contribution: categoryWeight * weights.category,
        category: memory.category,
      },
      manualBoost: {
        value: manualBoost,
        contribution: manualBoost * 0.1,
      },
      rawScore: Math.round(raw * 1000) / 1000,
      finalScore: Math.round(withBoost * 1000) / 1000,
    },
  };
}

/**
 * Score multiple memories efficiently (batch).
 * @param {object[]} memories - Array of memory objects
 * @returns {Map<string, { finalImportance: number, breakdown: object }>}
 */
export function scoreMemories(memories) {
  const memoryIds = memories.map(m => m.id);
  const statsMap = getUsageStatsBulk(memoryIds);
  const weights = config.importanceWeights || DEFAULT_WEIGHTS;

  const results = new Map();
  for (const memory of memories) {
    const stats = statsMap.get(memory.id) || null;
    results.set(memory.id, scoreMemory(memory, stats));
  }
  return results;
}

/**
 * Get importance boost factor for search pipeline.
 * Returns: (dynamicImportance - 0.5) * 0.4
 * This is used to boost RRF scores: boostedScore = rrfScore * (1 + importanceBoost)
 *
 * @param {string} memoryId
 * @param {number} [staticImportance=0.5]
 * @param {string} [category='other']
 * @param {number} [createdAt]
 * @returns {number} boost factor (can be negative)
 */
export function getImportanceBoost(memoryId, staticImportance = 0.5, category = 'other', createdAt = null) {
  const stats = getUsageStats(memoryId);
  const { finalImportance } = scoreMemory(
    { id: memoryId, importance: staticImportance, category, created_at: createdAt },
    stats
  );
  const boost = (finalImportance - 0.5) * 0.4;
  return boost;
}

/**
 * Explain why a memory has its current importance score.
 * Returns a human-readable breakdown.
 *
 * @param {object} memory - Memory object
 * @returns {object} breakdown object
 */
export function explainImportance(memory) {
  const stats = getUsageStats(memory.id);
  const { finalImportance, breakdown } = scoreMemory(memory, stats);
  return {
    memoryId: memory.id,
    finalImportance: Math.round(finalImportance * 1000) / 1000,
    breakdown,
    usageStats: stats ? {
      retrievalCount: stats.retrievalCount,
      usageCount: stats.usageCount,
      utilityScore: Math.round((stats.utilityScore || 0) * 1000) / 1000,
      lastRetrieved: stats.lastRetrieved ? new Date(stats.lastRetrieved).toISOString() : null,
      lastUsed: stats.lastUsed ? new Date(stats.lastUsed).toISOString() : null,
    } : null,
  };
}
