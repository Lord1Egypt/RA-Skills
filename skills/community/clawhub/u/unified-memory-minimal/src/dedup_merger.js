/**
 * dedup_merger.js - Memory Merge Strategies
 *
 * Implements three merge strategies based on semantic similarity:
 *   ABSORB  (>0.95): Keep older, discard newer
 *   MERGE   (0.85–0.95): Combine unique details from both
 *   KEEP_BOTH (<0.85): No action needed
 *
 * Merge algorithm:
 *   - union of tags
 *   - concatenate text snippets (deduplicated)
 *   - max of importances
 *   - earliest created_at
 *   - merged updated_at = now
 *
 * All merge operations are logged to dedup_log.json.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from './config.js';
import { saveMemories, getAllMemories, deleteMemory } from './storage.js';
import { appendDedupLog, ABSORB_THRESHOLD, MERGE_THRESHOLD } from './semantic_dedup.js';

export const DEDUP_LOG_PATH = join(config.memoryDir, 'dedup_log.json');

// ─── Strategy constants ─────────────────────────────────────────────────────
export const STRATEGY_ABSORB = 'absorb';
export const STRATEGY_MERGE = 'merge';
export const STRATEGY_KEEP_BOTH = 'keep_both';

/**
 * Classify similarity into a merge strategy.
 * @param {number} similarity
 * @returns {string}
 */
export function classifyStrategy(similarity) {
  if (similarity > ABSORB_THRESHOLD) return STRATEGY_ABSORB;
  if (similarity >= MERGE_THRESHOLD) return STRATEGY_MERGE;
  return STRATEGY_KEEP_BOTH;
}

/**
 * Decide which memory to keep when merging (always prefer older).
 * @param {object} memA
 * @param {object} memB
 * @returns {{ keeper: object, discarded: object }}
 */
function pickKeeper(memA, memB) {
  const aTime = memA.created_at || 0;
  const bTime = memB.created_at || 0;
  if (aTime <= bTime) {
    return { keeper: memA, discarded: memB };
  }
  return { keeper: memB, discarded: memA };
}

/**
 * Merge tags: union of both sets, no duplicates.
 * @param {string[]} tagsA
 * @param {string[]} tagsB
 * @returns {string[]}
 */
function mergeTags(tagsA = [], tagsB = []) {
  const combined = new Set([...tagsA, ...tagsB]);
  return Array.from(combined);
}

/**
 * Merge text snippets: combine unique sentences.
 * @param {string} textA
 * @param {string} textB
 * @returns {string}
 */
function mergeText(textA, textB) {
  // Split into sentences (crude split on . ! ? or newline)
  const split = (t) =>
    String(t || '')
      .split(/(?<=[.!?])\s+|\n+/)
      .map(s => s.trim())
      .filter(s => s.length > 2);

  const sentencesA = split(textA);
  const sentencesB = split(textB);
  const seen = new Set(sentencesA.map(s => s.toLowerCase()));
  const unique = [...sentencesA];

  for (const s of sentencesB) {
    if (!seen.has(s.toLowerCase())) {
      seen.add(s.toLowerCase());
      unique.push(s);
    }
  }

  return unique.join(' ');
}

/**
 * Absorb strategy: keep older memory, discard newer one silently.
 * No changes to the kept memory, just delete the newer one.
 *
 * @param {object} olderMem
 * @param {object} newerMem
 * @param {number} similarity
 * @returns {{ action: 'absorbed', kept: string, discarded: string }}
 */
export function absorbMemory(olderMem, newerMem, similarity) {
  const { discarded } = pickKeeper(olderMem, newerMem);

  // Delete the discarded memory
  const deleted = deleteMemory(discarded.id);

  appendDedupLog('absorb', {
    strategy: STRATEGY_ABSORB,
    similarity,
    keptId: discarded.id === newerMem.id ? olderMem.id : newerMem.id,
    absorbedId: discarded.id,
    reason: `Absorbed: similarity=${(similarity * 100).toFixed(2)}% > ${(ABSORB_THRESHOLD * 100).toFixed(0)}%`,
  });

  return {
    action: 'absorbed',
    kept: discarded.id === newerMem.id ? olderMem.id : newerMem.id,
    discarded: discarded.id,
    deleted,
  };
}

/**
 * Merge strategy: combine unique details from both memories into keeper.
 * The keeper is the older memory; its fields are updated in place.
 *
 * @param {object} memA
 * @param {object} memB
 * @param {number} similarity
 * @returns {{ action: 'merged', mergedId: string, discardedId: string, changes: object }}
 */
export function mergeMemory(memA, memB, similarity) {
  const { keeper, discarded } = pickKeeper(memA, memB);

  const changes = {
    tagsBefore: [...(keeper.tags || [])],
    tagsAfter: mergeTags(keeper.tags, discarded.tags),
    textBefore: keeper.text,
    textAfter: mergeText(keeper.text, discarded.text),
    importanceBefore: keeper.importance,
    importanceAfter: Math.max(keeper.importance || 0, discarded.importance || 0),
    importanceMax: true,
  };

  // Update keeper
  keeper.tags = changes.tagsAfter;
  keeper.text = changes.textAfter;
  keeper.importance = changes.importanceAfter;
  keeper.updated_at = Date.now();

  // If discarded has category different from keeper, note it
  if (discarded.category && discarded.category !== keeper.category) {
    keeper.tags = [...(keeper.tags || []), `merged_category:${discarded.category}`];
  }

  // Persist the merged keeper and delete the discarded one
  const memories = getAllMemories();
  const idx = memories.findIndex(m => m.id === keeper.id);
  if (idx !== -1) {
    memories[idx] = keeper;
  }
  saveMemories(memories);
  deleteMemory(discarded.id);

  appendDedupLog('merge', {
    strategy: STRATEGY_MERGE,
    similarity,
    mergedId: keeper.id,
    discardedId: discarded.id,
    changes,
    reason: `Merged: similarity=${(similarity * 100).toFixed(2)}% in [${(MERGE_THRESHOLD * 100).toFixed(0)}%–${(ABSORB_THRESHOLD * 100).toFixed(0)}%]`,
  });

  return {
    action: 'merged',
    mergedId: keeper.id,
    discardedId: discarded.id,
    changes,
  };
}

/**
 * Automatically apply a merge decision based on similarity and autoMerge setting.
 * If autoMerge=false (default), only returns the suggestion without applying.
 *
 * @param {object} memA
 * @param {object} memB
 * @param {number} similarity
 * @param {boolean} autoMerge - If true, apply the merge; if false, return suggestion
 * @returns {object} result with action, strategy, and optionally applied changes
 */
export function applyDedup(memA, memB, similarity, autoMerge = false) {
  const strategy = classifyStrategy(similarity);

  if (strategy === STRATEGY_KEEP_BOTH) {
    return {
      action: 'kept_both',
      strategy,
      similarity,
      memA: { id: memA.id, text: memA.text.slice(0, 80) },
      memB: { id: memB.id, text: memB.text.slice(0, 80) },
      autoApplied: false,
    };
  }

  if (strategy === STRATEGY_ABSORB) {
    if (autoMerge) {
      const result = absorbMemory(memA, memB, similarity);
      return { ...result, strategy, similarity, autoApplied: true };
    }
    // Return absorb suggestion
    const { keeper, discarded } = pickKeeper(memA, memB);
    return {
      action: 'suggest_absorb',
      strategy,
      similarity,
      suggestion: {
        keep: { id: keeper.id, text: keeper.text.slice(0, 80) },
        absorb: { id: discarded.id, text: discarded.text.slice(0, 80) },
      },
      autoApplied: false,
      message: `Similarity ${(similarity * 100).toFixed(1)}% > ${(ABSORB_THRESHOLD * 100).toFixed(0)}%. Suggest absorbing newer into older. Set autoMerge=true to apply.`,
    };
  }

  // STRATEGY_MERGE
  if (autoMerge) {
    const result = mergeMemory(memA, memB, similarity);
    return { ...result, strategy, similarity, autoApplied: true };
  }
  const { keeper, discarded } = pickKeeper(memA, memB);
  return {
    action: 'suggest_merge',
    strategy,
    similarity,
    suggestion: {
      keeper: { id: keeper.id, text: keeper.text.slice(0, 80) },
      toMerge: { id: discarded.id, text: discarded.text.slice(0, 80) },
    },
    autoApplied: false,
    message: `Similarity ${(similarity * 100).toFixed(1)}% in [${(MERGE_THRESHOLD * 100).toFixed(0)}%–${(ABSORB_THRESHOLD * 100).toFixed(0)}%]. Suggest merging. Set autoMerge=true to apply.`,
  };
}

export default { applyDedup, mergeMemory, absorbMemory, classifyStrategy };
