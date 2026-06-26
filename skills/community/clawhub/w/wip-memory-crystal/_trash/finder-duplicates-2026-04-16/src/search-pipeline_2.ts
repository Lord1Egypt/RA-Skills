// memory-crystal/search-pipeline.ts — Deep search pipeline.
// Orchestrates query expansion, multi-path search, RRF fusion, LLM re-ranking,
// and position-aware score blending. Ported from QMD (MIT License, Tobi Lutke).

import type { Crystal, SearchResult } from './core.js';
import { expandQuery, rerankResults, detectProvider } from './llm.js';

// Strong signal detection thresholds (from QMD)
const STRONG_SIGNAL_MIN_SCORE = 0.85;
const STRONG_SIGNAL_MIN_GAP = 0.15;
const RERANK_CANDIDATE_LIMIT = 40;

export interface DeepSearchOptions {
  limit?: number;
  filter?: { agent_id?: string; source_type?: string; since?: string };
}

/**
 * Deep search pipeline: expand query, multi-path search, RRF fusion, rerank, blend.
 * Falls back to standard search if no LLM provider is available.
 */
export async function deepSearch(crystal: Crystal, query: string, options: DeepSearchOptions = {}): Promise<SearchResult[]> {
  const limit = options.limit || 5;
  const filter = options.filter;

  // Check if we have an LLM provider
  const provider = await detectProvider();
  if (provider.provider === 'none') {
    // No LLM available, fall back to standard search
    return crystal.search(query, limit, filter);
  }

  // Access internal methods via the crystal instance
  // We need the raw search functions, not the public search() which already applies recency
  const db = (crystal as any).sqliteDb;
  if (!db) return crystal.search(query, limit, filter);

  const sinceDate = filter?.since ? (crystal as any).parseSince(filter.since) : undefined;
  const internalFilter = { ...filter, sinceDate };

  // Step 1: BM25 probe for strong signal detection
  const initialFts = (crystal as any).searchFTS(query, 20, internalFilter) as SearchResult[];
  const topScore = initialFts[0]?.score ?? 0;
  const secondScore = initialFts[1]?.score ?? 0;
  const hasStrongSignal = initialFts.length > 0
    && topScore >= STRONG_SIGNAL_MIN_SCORE
    && (topScore - secondScore) >= STRONG_SIGNAL_MIN_GAP;

  // Step 2: Expand query (skip if strong signal)
  const expanded = hasStrongSignal ? [] : await expandQuery(query);

  // Step 3: Run searches for each variation
  const allResultLists: SearchResult[][] = [];

  // Always include original FTS results
  if (initialFts.length > 0) allResultLists.push(initialFts);

  // Run original vector search
  const [queryEmbedding] = await (crystal as any).embed([query]);
  const originalVec = (crystal as any).searchVec(queryEmbedding, 30, internalFilter) as SearchResult[];
  if (originalVec.length > 0) allResultLists.push(originalVec);

  // Run expanded queries
  for (const variation of expanded) {
    if (variation.type === 'lex') {
      const ftsResults = (crystal as any).searchFTS(variation.text, 20, internalFilter) as SearchResult[];
      if (ftsResults.length > 0) allResultLists.push(ftsResults);
    } else {
      // vec and hyde get embedded and searched
      const [embedding] = await (crystal as any).embed([variation.text]);
      const vecResults = (crystal as any).searchVec(embedding, 20, internalFilter) as SearchResult[];
      if (vecResults.length > 0) allResultLists.push(vecResults);
    }
  }

  // Step 4: RRF fusion with tiered weights
  // First 2 lists (original FTS + original vec) get 2x weight
  const weights = allResultLists.map((_, i) => i < 2 ? 2.0 : 1.0);
  const fused = (crystal as any).reciprocalRankFusion(allResultLists, weights) as SearchResult[];
  const candidates = fused.slice(0, RERANK_CANDIDATE_LIMIT);

  if (candidates.length === 0) return [];

  // Step 5: LLM re-ranking
  const passages = candidates.map(c => c.text.slice(0, 500));
  const reranked = await rerankResults(query, passages);

  // Step 6: Position-aware score blending
  const now = Date.now();
  const blended = reranked.map(r => {
    const candidate = candidates[r.index];
    if (!candidate) return null;

    const rrfRank = r.index + 1;
    let rrfWeight: number;
    if (rrfRank <= 3) rrfWeight = 0.75;
    else if (rrfRank <= 10) rrfWeight = 0.60;
    else rrfWeight = 0.40;

    const rrfScore = 1 / rrfRank;
    const blendedScore = rrfWeight * rrfScore + (1 - rrfWeight) * r.score;

    // Apply recency weighting
    const ageDays = candidate.created_at ? (now - new Date(candidate.created_at).getTime()) / 86400000 : 0;
    const recency = candidate.created_at ? (crystal as any).recencyWeight(ageDays) : 1;
    const finalScore = Math.min(blendedScore * recency * 8, 1.0);

    const freshness = candidate.created_at ? (crystal as any).freshnessLabel(ageDays) : undefined;

    return {
      ...candidate,
      score: finalScore,
      freshness,
    } as SearchResult;
  }).filter((r): r is SearchResult => r !== null);

  // Sort by final score and return
  return blended.sort((a, b) => b.score - a.score).slice(0, limit);
}
