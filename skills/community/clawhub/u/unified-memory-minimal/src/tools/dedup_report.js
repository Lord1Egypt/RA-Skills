/**
 * dedup_report.js - Dedup Report & Manual Merge Tools
 *
 * Tools:
 *   memory_dedup_full_scan → Scan all memories for semantic duplicates
 *   memory_dedup_merge     → Manually merge a pair of memories
 */

import { z } from 'zod';
import { findAllDuplicatePairs, loadDedupLog } from '../semantic_dedup.js';
import { applyDedup, STRATEGY_ABSORB, STRATEGY_MERGE, STRATEGY_KEEP_BOTH } from '../dedup_merger.js';
import { getMemory } from '../storage.js';

const dedupFullScanSchema = z.object({
  threshold: z.number().optional().default(0.85).describe('Minimum similarity threshold (0–1)'),
  topK: z.number().optional().default(50).describe('Maximum number of duplicate pairs to return'),
});

const dedupMergeSchema = z.object({
  memoryIdA: z.string().describe('ID of first memory'),
  memoryIdB: z.string().describe('ID of second memory'),
  similarity: z.number().optional().describe('Pre-computed similarity (if known, skips computation)'),
  autoMerge: z.boolean().optional().default(false).describe('If true, auto-apply the merge; if false, return suggestion'),
});

/**
 * memory_dedup_full_scan tool
 * Scans ALL memories for semantic duplicate pairs.
 */
export async function memoryDeduFullScan(args) {
  const parsed = dedupFullScanSchema.safeParse(args);
  if (!parsed.success) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ error: 'Invalid args', details: parsed.error.format() }),
      }],
      isError: true,
    };
  }

  const { threshold, topK } = parsed.data;

  let result;
  try {
    result = await findAllDuplicatePairs({ threshold, maxPairs: topK });
  } catch (err) {
    return {
      content: [{ type: 'text', text: JSON.stringify({ error: `Scan failed: ${err.message}` }) }],
      isError: true,
    };
  }

  // Group by strategy
  const absorbPairs = result.pairs.filter(p => p.strategy === STRATEGY_ABSORB);
  const mergePairs = result.pairs.filter(p => p.strategy === STRATEGY_MERGE);
  const keepPairs = result.pairs.filter(p => p.strategy === STRATEGY_KEEP_BOTH);

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        scan: 'full semantic dedup scan',
        stats: result.stats,
        summary: {
          absorbCandidates: absorbPairs.length,
          mergeCandidates: mergePairs.length,
          differentAspectPairs: keepPairs.length,
        },
        absorbPairs: absorbPairs.slice(0, 20),
        mergePairs: mergePairs.slice(0, 20),
        // don't show keep_both pairs in report — they're not actionable
        totalPairsShown: Math.min(result.pairs.length, topK),
        threshold,
      }, null, 2),
    }],
  };
}

/**
 * memory_dedup_merge tool
 * Manually merges two memories. If similarity not provided, computes it.
 */
export async function memoryDeduMerge(args) {
  const parsed = dedupMergeSchema.safeParse(args);
  if (!parsed.success) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ error: 'Invalid args', details: parsed.error.format() }),
      }],
      isError: true,
    };
  }

  const { memoryIdA, memoryIdB, similarity, autoMerge } = parsed.data;

  const memA = getMemory(memoryIdA);
  const memB = getMemory(memoryIdB);

  if (!memA || !memB) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          error: 'Memory not found',
          found: { A: !!memA, B: !!memB },
          ids: { memoryIdA, memoryIdB },
        }),
      }],
      isError: true,
    };
  }

  // Compute similarity if not provided
  let sim = similarity;
  if (sim === undefined || sim === null) {
    const { cosineSimilarity } = await import('../semantic_dedup.js');
    const { getEmbeddingCached } = await import('../vector.js');
    try {
      const embA = await getEmbeddingCached(memA.text);
      const embB = await getEmbeddingCached(memB.text);
      if (embA && embB) {
        sim = cosineSimilarity(embA, embB);
      } else {
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ error: 'Could not compute embeddings for one or both memories' }),
          }],
          isError: true,
        };
      }
    } catch (err) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ error: `Embedding failed: ${err.message}` }) }],
        isError: true,
      };
    }
  }

  const result = applyDedup(memA, memB, sim, autoMerge);

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        memoryIdA,
        memoryIdB,
        similarity: sim,
        ...result,
      }, null, 2),
    }],
  };
}

/**
 * memory_dedup_log tool
 * Returns the dedup merge history log.
 */
export async function memoryDeduLog() {
  try {
    const log = loadDedupLog();
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          merges: log.merges.slice(-50).reverse(),
          scans: log.scans.slice(-20).reverse(),
          totalMerges: log.merges.length,
          totalScans: log.scans.length,
        }, null, 2),
      }],
    };
  } catch (err) {
    return {
      content: [{ type: 'text', text: JSON.stringify({ error: `Failed to load log: ${err.message}` }) }],
      isError: true,
    };
  }
}

export default { memoryDeduFullScan, memoryDeduMerge, memoryDeduLog };
