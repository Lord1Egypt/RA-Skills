// memory-crystal/search-pipeline.ts — Deep search pipeline.
// Orchestrates query expansion, multi-path search, RRF fusion, LLM re-ranking,
// and position-aware score blending. Ported from QMD (MIT License, Tobi Lutke).

import type { Crystal, SearchResult } from './core.js';
import { expandQuery, rerankResults, detectProvider } from './llm.js';

// Strong signal detection thresholds (from QMD)
const STRONG_SIGNAL_MIN_SCORE = 0.85;
const STRONG_SIGNAL_MIN_GAP = 0.15;
const DEFAULT_CANDIDATE_LIMIT = 40;

export interface DeepSearchOptions {
  limit?: number;
  candidateLimit?: number;
  intent?: string;
  filter?: { agent_id?: string; source_type?: string; since?: string; until?: string };
  explain?: boolean;
}

export interface ExplainTrace {
  fts_score?: number;
  vec_score?: number;
  rrf_rank: number;
  rrf_score: number;
  rerank_score: number;
  recency_weight: number;
  final_score: number;
}

export interface DeepSearchResult extends SearchResult {
  explain?: ExplainTrace;
}

/**
 * Deep search pipeline: expand query, multi-path search, RRF fusion, rerank, blend.
 * Falls back to standard search if no LLM provider is available.
 */
export async function deepSearch(crystal: Crystal, query: string, options: DeepSearchOptions = {}): Promise<DeepSearchResult[]> {
  const limit = options.limit || 5;
  const candidateLimit = options.candidateLimit || DEFAULT_CANDIDATE_LIMIT;
  const intent = options.intent;
  const filter = options.filter;
  const explain = options.explain || false;

  // Check if we have an LLM provider
  const provider = await detectProvider();
  if (provider.provider === 'none') {
    // No LLM available, fall back to standard search
    return crystal.search(query, limit, filter);
  }

  // Access internal methods via the crystal instance
  const db = (crystal as any).sqliteDb;
  if (!db) return crystal.search(query, limit, filter);

  const sinceDate = filter?.since ? (crystal as any).parseSince(filter.since) : undefined;
  const untilDate = filter?.until ? (crystal as any).parseSince(filter.until) : undefined;
  const internalFilter = { ...filter, sinceDate, untilDate };

  // Step 1: BM25 probe for strong signal detection
  const initialFts = (crystal as any).searchFTS(query, 20, internalFilter) as SearchResult[];
  const topScore = initialFts[0]?.score ?? 0;
  const secondScore = initialFts[1]?.score ?? 0;
  // Disable strong-signal bypass when intent is present (keyword match might not be what caller wants)
  const hasStrongSignal = !intent && initialFts.length > 0
    && topScore >= STRONG_SIGNAL_MIN_SCORE
    && (topScore - secondScore) >= STRONG_SIGNAL_MIN_GAP;

  // Step 2: Expand query (skip if strong signal)
  const expanded = hasStrongSignal ? [] : await expandQuery(query, intent);

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
      const [embedding] = await (crystal as any).embed([variation.text]);
      const vecResults = (crystal as any).searchVec(embedding, 20, internalFilter) as SearchResult[];
      if (vecResults.length > 0) allResultLists.push(vecResults);
    }
  }

  // Step 4: RRF fusion with tiered weights
  const weights = allResultLists.map((_, i) => i < 2 ? 2.0 : 1.0);
  const fused = (crystal as any).reciprocalRankFusion(allResultLists, weights) as SearchResult[];
  const candidates = fused.slice(0, candidateLimit);

  if (candidates.length === 0) return [];

  // Build FTS/vec score maps for explain mode
  const ftsScoreMap = new Map<string, number>();
  const vecScoreMap = new Map<string, number>();
  if (explain) {
    for (const r of initialFts) ftsScoreMap.set(r.text.slice(0, 200), r.score);
    for (const r of originalVec) vecScoreMap.set(r.text.slice(0, 200), r.score);
  }

  // Step 5: LLM re-ranking
  const passages = candidates.map(c => c.text.slice(0, 500));
  const rerankQuery = intent ? `${intent}: ${query}` : query;
  const reranked = await rerankResults(rerankQuery, passages);

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

    const ageDays = candidate.created_at ? (now - new Date(candidate.created_at).getTime()) / 86400000 : 0;
    const recency = candidate.created_at ? (crystal as any).recencyWeight(ageDays) : 1;
    const finalScore = blendedScore * recency;

    const freshness = candidate.created_at ? (crystal as any).freshnessLabel(ageDays) : undefined;

    const result: DeepSearchResult = {
      ...candidate,
      score: finalScore,
      freshness,
    };

    if (explain) {
      const dedup = candidate.text.slice(0, 200);
      result.explain = {
        fts_score: ftsScoreMap.get(dedup),
        vec_score: vecScoreMap.get(dedup),
        rrf_rank: rrfRank,
        rrf_score: rrfScore,
        rerank_score: r.score,
        recency_weight: recency,
        final_score: finalScore,
      };
    }

    return result;
  }).filter((r): r is DeepSearchResult => r !== null);

  // Sort by final score, normalize so top = 0.95 and others relative
  const sorted = blended.sort((a, b) => b.score - a.score).slice(0, limit);
  const topNormScore = sorted[0]?.score || 1;
  return sorted.map(r => ({ ...r, score: Math.min(r.score / topNormScore * 0.95, 0.95) }));
}
