/**
 * working_memory_injector.js - Context Injection for Search
 * 
 * When memory_search is called, inject active working memories as priority context.
 * Working memory context is prepended to query context with boost scoring.
 * 
 * Boost formula: boostedScore = baseScore * (1 + workingMemoryRelevance * 0.5)
 */

import { getActive, get as getWorkingMemory } from './working_memory_manager.js';
import { config } from './config.js';

// Boost weight for working memory relevance
const WORKING_MEMORY_BOOST_WEIGHT = 0.5;

// ============================================================================
// Context Injection
// ============================================================================

/**
 * Get working memory context to inject into search
 * @returns {{context: string, memories: object[], count: number}}
 */
export function getWorkingMemoryContext() {
  const { active, held } = getActive();
  const all = [...active, ...held];

  if (all.length === 0) {
    return { context: '', memories: [], count: 0 };
  }

  const lines = ['## Active Working Memories (Task Context)'];
  
  for (const wm of all) {
    const statusLabel = wm.status === 'HELD' ? '[HELD]' : '[ACTIVE]';
    lines.push(`\n${statusLabel} Task: ${wm.description}`);
    if (wm.contextWindow) {
      lines.push(`  Context: ${wm.contextWindow}`);
    }
    lines.push(`  Created: ${wm.createdAt} | Expires: ${wm.expiresAt}`);
    if (wm.episodeId) {
      lines.push(`  Episode: ${wm.episodeId}`);
    }
  }

  return {
    context: lines.join('\n'),
    memories: all,
    count: all.length,
  };
}

/**
 * Calculate relevance score between a working memory and a search query
 * 
 * @param {object} wm - Working memory (formatted)
 * @param {string} query - Search query
 * @returns {number} Relevance score 0-1
 */
export function calculateWorkingMemoryRelevance(wm, query) {
  const queryLower = query.toLowerCase();
  const queryTerms = queryLower.split(/\s+/).filter(t => t.length > 2);

  if (queryTerms.length === 0) return 0;

  // Score based on description match
  const descLower = (wm.description || '').toLowerCase();
  let score = 0;

  // Exact phrase match (highest weight)
  if (descLower.includes(queryLower)) {
    score += 0.6;
  }

  // Individual term matches
  for (const term of queryTerms) {
    if (descLower.includes(term)) {
      score += 0.1;
    }
  }

  // Context window match
  const ctxLower = (wm.contextWindow || '').toLowerCase();
  for (const term of queryTerms) {
    if (ctxLower.includes(term)) {
      score += 0.05;
    }
  }

  // Normalize to 0-1
  return Math.min(1, score);
}

/**
 * Boost search results based on working memory relevance
 * 
 * @param {Array<{memory: object, score: number}>} results - Search results
 * @param {string} query - Original search query
 * @returns {Array<{memory: object, score: number, boostedScore: number, workingMemoryBoost: number}>}
 */
export function boostResultsWithWorkingMemory(results, query) {
  const { memories: workingMemories } = getWorkingMemoryContext();

  if (workingMemories.length === 0) {
    return results.map(r => ({
      ...r,
      boostedScore: r.score,
      workingMemoryBoost: 0,
    }));
  }

  return results.map(result => {
    let maxRelevance = 0;

    for (const wm of workingMemories) {
      const relevance = calculateWorkingMemoryRelevance(wm, query);
      if (relevance > maxRelevance) {
        maxRelevance = relevance;
      }
    }

    // Boost formula: boostedScore = baseScore * (1 + workingMemoryRelevance * 0.5)
    const boostFactor = 1 + maxRelevance * WORKING_MEMORY_BOOST_WEIGHT;
    const boostedScore = result.score * boostFactor;

    return {
      ...result,
      boostedScore,
      workingMemoryBoost: maxRelevance,
    };
  });
}

/**
 * Re-rank results putting working-memory-relevant items first
 * 
 * @param {Array} results - Boosted results
 * @returns {Array}
 */
export function rerankWithWorkingMemory(results) {
  return [...results].sort((a, b) => {
    // First sort by boosted score (descending)
    const scoreDiff = (b.boostedScore || b.score) - (a.boostedScore || a.score);
    if (scoreDiff !== 0) return scoreDiff;

    // Fall back to original score
    return (b.score || 0) - (a.score || 0);
  });
}

/**
 * Inject working memory context into hybrid search call
 * This is called before the actual search to prepend context
 * 
 * @param {string} query - Original query
 * @param {object} searchOptions - Search options
 * @returns {{modifiedQuery: string, workingMemoryContext: object, injected: boolean}}
 */
export function injectWorkingMemoryContext(query, searchOptions = {}) {
  const wmContext = getWorkingMemoryContext();

  if (wmContext.count === 0) {
    return {
      modifiedQuery: query,
      workingMemoryContext: wmContext,
      injected: false,
    };
  }

  // Prepend working memory context to query as pseudo-context
  const prefix = wmContext.context + '\n\n';
  
  return {
    modifiedQuery: query,
    workingMemoryContext: wmContext,
    injected: true,
    prefix,
  };
}

/**
 * Post-process search results: apply working memory boost
 * 
 * @param {Array} results - Raw search results
 * @param {string} query - Original search query
 * @returns {{results: Array, workingMemoryContext: object, boosted: boolean}}
 */
export function processSearchResults(results, query) {
  const wmContext = getWorkingMemoryContext();

  if (wmContext.count === 0 || !results || results.length === 0) {
    return { results, workingMemoryContext: wmContext, boosted: false };
  }

  const boosted = boostResultsWithWorkingMemory(results, query);
  const reranked = rerankWithWorkingMemory(boosted);

  return {
    results: reranked,
    workingMemoryContext: wmContext,
    boosted: true,
  };
}

// ============================================================================
// Standalone Query Enhancement
// ============================================================================

/**
 * Enhance a query with working memory context (for LLM prompts)
 * @param {string} query
 * @returns {{enhancedQuery: string, hasWorkingMemory: boolean}}
 */
export function enhanceQuery(query) {
  const { context, count } = getWorkingMemoryContext();

  if (count === 0) {
    return { enhancedQuery: query, hasWorkingMemory: false };
  }

  const enhanced = `${context}\n\n---\n\nQuery: ${query}`;
  return { enhancedQuery: enhanced, hasWorkingMemory: true };
}
