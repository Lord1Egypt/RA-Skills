/**
 * Core Search Pipeline v3.1
 * Full integration: Adaptive skip → Intent routing → BM25 → Vector → Rerank → MMR → Decay → Category weighting → Scope
 * 
 * Complete retrieval chain:
 * 1. shouldSkipRetrieval() - skip meaningless queries (adaptive.js)
 * 2. routeSearch() - intent analysis, returns null = skip (intent.js)
 * 3. Scope filter + category filter based on intent weights
 * 4. BM25 search - fast keyword match
 * 5. Vector search - semantic similarity (LanceDB)
 * 6. LLM/keyword rerank - cross-encoder re-scoring
 * 7. MMR - diversity deduplication
 * 8. Weibull decay - time-weighted boosting
 * 9. Category weights from intent signal
 * 10. RRF fusion - merge BM25 + vector ranked lists
 */

import { shouldSkipRetrieval } from './adaptive.js';
import { routeSearch, getCategoryWeights } from './intent.js';
import { embedCache, EmbedCache } from './embed_cache.js';
import { bm25Search } from './bm25.js';
import { vectorSearch } from './vector.js';
import { keywordRerank, LlmReranker } from './rerank.js';
import { mmrSelect } from './mmr.js';
import { applyDecayBoost } from './decay.js';
import { filterByScope, getScopeOrder } from './scope.js';
import { filterByQuality } from './noise.js';
import { qualityScore } from './quality.js';
import { config } from './config.js';
import { loadMemories } from './storage.js';
import { MemoryAssociation } from './core/association.js';

// Intent patterns that trigger knowledge-graph association search
const ASSOCIATION_PATTERNS = [
  /^(what|哪些|什么).*(relat|关联|相关|联系)/i,
  /(relat|关联|相关|联系).*(to|到|于)/i,
  /^tell\s+me\s+about/i,
  /^(who\s+is|what\s+is|explain|describe)\s+.{0,30}$/i,
  /(remember|recall|earlier|before|曾|记得|之前).*related/i,
  /^(关联|相关记忆|相关联系)/i,
];

function isAssociationQuery(query) {
  const q = String(query || '').trim();
  // Check explicit patterns
  for (const p of ASSOCIATION_PATTERNS) {
    if (p.test(q)) return true;
  }
  // Also trigger for entity-type queries (tell me about X, who is X)
  const intent = routeSearch(q);
  if (intent && intent.intent === 'entity') return true;
  return false;
}

/**
 * Knowledge graph association search via MemoryAssociation
 * Uses vector similarity, co-occurrence, and tag correlation
 * @param {string} query
 * @param {number} topK
 * @returns {Promise<Array>}
 */
export async function knowledgeGraphSearch(query, topK = 5) {
  try {
    const association = new MemoryAssociation();
    const results = await association.relatedToQuery(query, topK);
    return results.map((r, i) => ({
      memory: r.memory,
      score: r.score,
      reasons: r.reasons,
      rank: i + 1,
      highlight: (r.memory.text || '').slice(0, 150),
      source: 'knowledge_graph',
    }));
  } catch (err) {
    // Graceful fallback - return empty on error
    console.error('[knowledgeGraphSearch] error:', err.message);
    return [];
  }
}

// Global embedding cache instance (shared across calls)
const embedCacheInstance = new EmbedCache(256, 30);
let llmReranker = null;

function getReranker() {
  if (!llmReranker) {
    llmReranker = new LlmReranker();
  }
  return llmReranker;
}

/**
 * Apply category weights to candidates based on intent signal
 * @param {Array} candidates 
 * @param {Map} categoryWeights 
 * @returns {Array}
 */
function applyCategoryWeights(candidates, categoryWeights) {
  if (!categoryWeights || categoryWeights.size === 0) return candidates;

  return candidates.map(c => {
    const cat = c.memory?.category || 'other';
    const weight = categoryWeights.get(cat) ?? 0.2;
    return {
      ...c,
      categoryWeight: weight,
      score: (c.score ?? (c.bm25Score ?? 0) + (c.vectorScore ?? 0)) * weight,
    };
  });
}

/**
 * Apply reflection/insightful boost to candidates.
 * Memories that have been reflected (insightful flag or reflection_count > 0)
 * receive a multiplicative score boost, stacking with existing relevance scores.
 *
 * @param {Array} candidates
 * @param {number} [boostFactor=0.15] - max boost multiplier added to score
 * @returns {Array}
 */
function applyReflectionBoost(candidates, boostFactor = 0.15) {
  return candidates.map(c => {
    const reflectionCount = c.memory?.reflection_count || 0;
    const insightful = c.memory?.insightful === true;
    if (!insightful && reflectionCount === 0) return c;

    // Cap boost at reflectionCount=3 (max boost reached)
    const boost = Math.min(reflectionCount, 3) * (boostFactor / 3);
    const originalScore = c.score ?? (c.bm25Score ?? 0) + (c.vectorScore ?? 0);
    return {
      ...c,
      reflectionBoost: boost,
      score: originalScore + boost,
    };
  });
}

/**
 * Main search pipeline v3.2
 * @param {string} query
 * @param {object} options
 * @param {number} options.topK - final results to return (default 10)
 * @param {string} options.scope - AGENT|USER|TEAM|GLOBAL (default GLOBAL)
 * @param {boolean} options.enableRerank - use LLM rerank (default true)
 * @param {boolean} options.enableMMR - use MMR diversity (default true)
 * @param {boolean} options.enableDecay - apply Weibull time decay (default true)
 * @param {boolean} options.reflectedBoost - boost reflected/insightful memories (default true)
 * @param {number} options.fetchK - candidates to fetch before MMR (default 20)
 * @param {string} options.mode - 'hybrid'|'bm25'|'vector' (default hybrid)
 * @returns {Promise<Array>}
 */
export async function search(query, options = {}) {
  const {
    topK = 10,
    scope = 'global',
    enableRerank = true,
    enableMMR = true,
    enableDecay = true,
    fetchK = 20,
    mode = 'hybrid',
    reflectedBoost = true,
  } = options;

  // === 1. Adaptive Skip ===
  if (shouldSkipRetrieval(query)) {
    return [];
  }

  // === 2. Intent Routing ===
  const intent = routeSearch(query);
  if (!intent) {
    return [];  // Query classified as skip (l0, non-specific)
  }

  // === 2b. Knowledge Graph Association Search (optional path for entity/relation queries) ===
  let kgResults = [];
  if (isAssociationQuery(query)) {
    try {
      kgResults = await knowledgeGraphSearch(query, fetchK);
      // Touch KG results so they count as accessed
      for (const r of kgResults) {
        if (r.memory?.id) {
          // Mark as touched via storage
          const { touchMemory } = await import('./storage.js');
          touchMemory(r.memory.id);
        }
      }
    } catch (err) {
      console.warn('[search] KG path failed, falling back to standard search:', err.message);
    }
  }

  // === 3. Load memories + Scope filter ===
  const allMemories = loadMemories();
  
  // Apply scope filter
  const scopeOrder = getScopeOrder(scope);
  let memories = [];
  for (const s of scopeOrder) {
    const filtered = filterByScope(allMemories, s);
    memories.push(...filtered);
  }

  // Apply noise filter (remove low-quality entries)
  memories = filterByQuality(memories);

  // Deduplicate by id
  const seen = new Set();
  memories = memories.filter(m => {
    if (seen.has(m.id)) return false;
    seen.add(m.id);
    return true;
  });

  if (memories.length === 0) return [];

  // === 4. BM25 Search (returns scored results) ===
  const bm25Results = bm25Search(query, fetchK * 2);

  // === 5. Vector Search ===
  const vectorResults = await vectorSearch(query, fetchK * 2);

  // === 6. Merge candidates ===
  const candidateMap = new Map();
  for (const r of bm25Results) {
    candidateMap.set(r.memory.id, { memory: r.memory, bm25Score: r.score ?? 0, vectorScore: 0, _bm25Rank: bm25Results.indexOf(r) });
  }
  for (const r of vectorResults) {
    const existing = candidateMap.get(r.memory.id);
    if (existing) {
      existing.vectorScore = r.score ?? 0;
    } else {
      candidateMap.set(r.memory.id, { memory: r.memory, bm25Score: 0, vectorScore: r.score ?? 0, _vectorRank: vectorResults.indexOf(r) });
    }
  }

  let candidates = Array.from(candidateMap.values());

  // === 6b. Inject KG association results into candidate pool ===
  if (kgResults.length > 0) {
    for (const kg of kgResults) {
      const existing = candidateMap.get(kg.memory.id);
      if (existing) {
        // Boost existing candidate with KG signal
        existing.score = (existing.score ?? 0) + (kg.score ?? 0) * 0.4;
        existing.kgScore = kg.score ?? 0;
        existing.kgReasons = kg.reasons ?? [];
      } else {
        // New candidate discovered via KG path only
        candidateMap.set(kg.memory.id, {
          memory: kg.memory,
          bm25Score: 0,
          vectorScore: 0,
          score: kg.score ?? 0,
          kgScore: kg.score ?? 0,
          kgReasons: kg.reasons ?? [],
          source: 'knowledge_graph',
        });
      }
    }
    candidates = Array.from(candidateMap.values());
  }

  // === 7. Rerank (optional) ===
  if (enableRerank) {
    try {
      const reranker = getReranker();
      candidates = await reranker.rerank(query, candidates, fetchK);
    } catch {
      candidates = keywordRerank(query, candidates, fetchK);
    }
  }

  // === 8. MMR Diversity (optional) ===
  if (enableMMR) {
    candidates = await mmrSelect(candidates, query, 0.5, fetchK, topK * 2);
  } else {
    candidates.sort((a, b) => ((b.bm25Score + b.vectorScore) - (a.bm25Score + a.vectorScore)));
    candidates = candidates.slice(0, fetchK);
  }

  // === 9. Weibull Time Decay (optional) ===
  if (enableDecay) {
    candidates = applyDecayBoost(candidates, 30, 0.3);
  }

  // === 10. Apply category weights from intent ===
  const categoryWeights = getCategoryWeights(intent);
  candidates = applyCategoryWeights(candidates, categoryWeights);

  // === 10b. Reflection / Insightful Boost ===
  // Memories that have been reflected (marked as insightful) get a relevance boost
  if (options.reflectedBoost !== false) {
    candidates = applyReflectionBoost(candidates);
  }

  // === 11. Build final results with RRF-like score ===
  const finalResults = candidates.slice(0, topK).map((c, i) => ({
    memory: c.memory,
    score: c.score ?? (c.bm25Score ?? 0) + (c.vectorScore ?? 0),
    bm25Score: c.bm25Score,
    vectorScore: c.vectorScore,
    fusionScore: c.fusionScore,
    rerankScore: c.rerankScore,
    decay: c.decay,
    categoryWeight: c.categoryWeight,
    reflectionBoost: c.reflectionBoost || 0,
    intentLabel: intent.label,
    ageDays: c.ageDays,
    rank: i + 1,
    highlight: c.highlight || c.memory.text?.slice(0, 150),
  }));

  return finalResults;
}

/**
 * Quick BM25-only search (no vector)
 */
export async function searchBm25(query, options = {}) {
  if (shouldSkipRetrieval(query)) return [];
  const intent = routeSearch(query);
  if (!intent) return [];

  const { topK = 10, scope = 'global' } = options;
  const allMemories = await loadMemories();
  const scopeOrder = getScopeOrder(scope);
  let memories = [];
  for (const s of scopeOrder) {
    memories.push(...filterByScope(allMemories, s));
  }
  memories = filterByQuality(memories);

  const results = bm25Search(query, topK);
  return results.slice(0, topK).map((r, i) => ({
    memory: r.memory,
    score: r.score,
    bm25Score: r.score,
    rank: i + 1,
    highlight: r.highlight,
  }));
}

/**
 * Get embedding cache stats
 */
export function getCacheStats() {
  return embedCache.getStats();
}
