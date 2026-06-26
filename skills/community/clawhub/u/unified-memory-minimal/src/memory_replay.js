/**
 * Memory Replay Engine v1.0 - Memory Replay Debugger (Feature #8)
 * 
 * Replay historical queries and explain memory retrieval decisions.
 * 
 * Methods:
 *   replayQuery(queryId)      - rerun a historical query and return full pipeline trace
 *   replayMemory(memoryId)     - show all queries that retrieved this memory and how it ranked
 *   diffQueries(q1, q2)       - compare two query retrieval paths side by side
 *   explainMemoryRetrieval(memoryId) - why was this memory retrieved? show contributing factors
 */

import { getTraceById, getAllTraces, getMemoryRetrievalHistory, searchTraces } from './retrieval_tracer.js';
import { search } from './search.js';

/**
 * Replay a historical query and return its full pipeline trace
 * Reruns the exact same search pipeline and returns step-by-step breakdown
 * 
 * @param {string} queryId - the trace query ID (qt-xxx)
 * @returns {Promise<object>} full replay result with current results + historical trace
 */
export async function replayQuery(queryId) {
  const historicalTrace = getTraceById(queryId);
  
  if (!historicalTrace) {
    return {
      success: false,
      error: `Trace not found: ${queryId}`,
      hint: 'Traces expire after maxTraces (1000) queries. Use searchTraces() to find query IDs.',
    };
  }
  
  // Rerun the search with the same options
  const { query, options } = historicalTrace;
  const startTime = Date.now();
  
  let currentResults;
  try {
    currentResults = await search(query, {
      topK: options.topK || 10,
      scope: options.scope || 'global',
      mode: options.mode || 'hybrid',
      enableRerank: options.enableRerank !== false,
      enableMMR: options.enableMMR !== false,
      enableDecay: options.enableDecay !== false,
      enableGraphBoost: options.enableGraphBoost !== false,
      enableImportanceBoost: options.enableImportanceBoost !== false,
    });
  } catch (err) {
    currentResults = { error: err.message };
  }
  
  const replayDurationMs = Date.now() - startTime;
  
  // Compare current vs historical results
  const historicalIds = (historicalTrace.finalRanking || []).map(r => r.memoryId);
  const currentIds = currentResults.map ? currentResults.map(r => r.memory?.id) : [];
  
  const rankingChanges = [];
  for (let i = 0; i < Math.min(historicalIds.length, currentIds.length); i++) {
    const oldId = historicalIds[i];
    const newId = currentIds[i];
    const newRank = currentIds.indexOf(oldId);
    rankingChanges.push({
      rank: i + 1,
      historicalId: oldId,
      currentId: newRank >= 0 ? newId : null,
      change: newRank >= 0 ? (newRank - i) : 'dropped',
    });
  }
  
  return {
    success: true,
    queryId,
    query,
    historical: {
      timestamp: historicalTrace.timestamp,
      durationMs: historicalTrace.durationMs,
      finalRanking: historicalTrace.finalRanking,
      pipelineSteps: historicalTrace.pipelineSteps,
    },
    current: {
      timestamp: new Date().toISOString(),
      durationMs: replayDurationMs,
      results: currentResults.map ? currentResults.slice(0, 10).map((r, i) => ({
        memoryId: r.memory?.id,
        text: r.memory?.text?.slice(0, 80),
        score: r.score,
        rank: i + 1,
      })) : null,
      error: currentResults.error || null,
    },
    comparison: {
      rankingChanges,
      resultCountChange: (currentResults.length || 0) - historicalTrace.finalRanking?.length,
      durationChange: replayDurationMs - historicalTrace.durationMs,
    },
  };
}

/**
 * Show all queries that retrieved a specific memory and how it ranked
 * @param {string} memoryId
 * @returns {object}
 */
export function replayMemory(memoryId) {
  const history = getMemoryRetrievalHistory(memoryId);
  
  if (history.length === 0) {
    return {
      success: true,
      memoryId,
      retrieved: false,
      message: `Memory ${memoryId} was never retrieved in any traced query.`,
    };
  }
  
  // Categorize retrieval performance
  const topRank = history.filter(h => h.rank <= 3);
  const midRank = history.filter(h => h.rank > 3 && h.rank <= 10);
  const lowRank = history.filter(h => h.rank > 10);
  
  // Score trend
  const scores = history.map(h => h.score).filter(s => s != null);
  const avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
  
  return {
    success: true,
    memoryId,
    retrieved: true,
    totalRetrievals: history.length,
    performance: {
      topRankCount: topRank.length,      // rank 1-3: highly visible
      midRankCount: midRank.length,       // rank 4-10: visible
      lowRankCount: lowRank.length,      // rank 10+: rarely seen
    },
    scoreStats: {
      avgScore: Math.round(avgScore * 1000) / 1000,
      maxScore: Math.max(...scores),
      minScore: Math.min(...scores),
    },
    retrievalHistory: history.map(h => ({
      queryId: h.queryId,
      query: h.query,
      timestamp: h.timestamp,
      rank: h.rank,
      score: h.score,
      durationMs: h.durationMs,
    })),
  };
}

/**
 * Compare two query retrieval paths side by side
 * @param {string} queryId1
 * @param {string} queryId2
 * @returns {object}
 */
export async function diffQueries(queryId1, queryId2) {
  const trace1 = getTraceById(queryId1);
  const trace2 = getTraceById(queryId2);
  
  if (!trace1 && !trace2) {
    return { success: false, error: `Neither trace found: ${queryId1}, ${queryId2}` };
  }
  if (!trace1) {
    return { success: false, error: `Trace not found: ${queryId1}` };
  }
  if (!trace2) {
    return { success: false, error: `Trace not found: ${queryId2}` };
  }
  
  // Build step comparison
  const steps1 = trace1.pipelineSteps || [];
  const steps2 = trace2.pipelineSteps || [];
  const maxSteps = Math.max(steps1.length, steps2.length);
  
  const stepComparison = [];
  for (let i = 0; i < maxSteps; i++) {
    const s1 = steps1[i];
    const s2 = steps2[i];
    stepComparison.push({
      index: i,
      step1: s1 ? { name: s1.stepName, score: s1.score, reasoning: s1.reasoning } : null,
      step2: s2 ? { name: s2.stepName, score: s2.score, reasoning: s2.reasoning } : null,
      different: !s1 || !s2 || s1.stepName !== s2.stepName || s1.score !== s2.score,
    });
  }
  
  // Result comparison
  const ids1 = new Set((trace1.finalRanking || []).map(r => r.memoryId));
  const ids2 = new Set((trace2.finalRanking || []).map(r => r.memoryId));
  
  const onlyIn1 = [...ids1].filter(id => !ids2.has(id));
  const onlyIn2 = [...ids2].filter(id => !ids1.has(id));
  const inBoth = [...ids1].filter(id => ids2.has(id));
  
  return {
    success: true,
    query1: { queryId: queryId1, query: trace1.query, timestamp: trace1.timestamp, durationMs: trace1.durationMs },
    query2: { queryId: queryId2, query: trace2.query, timestamp: trace2.timestamp, durationMs: trace2.durationMs },
    stepComparison,
    resultComparison: {
      sharedCount: inBoth.length,
      onlyInQuery1Count: onlyIn1.length,
      onlyInQuery2Count: onlyIn2.length,
      sharedMemoryIds: inBoth,
      onlyInQuery1: onlyIn1.slice(0, 10),
      onlyInQuery2: onlyIn2.slice(0, 10),
    },
  };
}

/**
 * Explain why a memory was retrieved - show all contributing factors
 * @param {string} memoryId
 * @returns {object}
 */
export function explainMemoryRetrieval(memoryId) {
  const history = getMemoryRetrievalHistory(memoryId);
  
  if (history.length === 0) {
    return {
      success: false,
      memoryId,
      error: 'Memory was never retrieved in any traced query. Cannot explain.',
      hint: 'This memory may never have appeared in search results, or tracing may be disabled.',
    };
  }
  
  // Get the most recent retrieval trace
  const latest = history[0];
  const trace = getTraceById(latest.queryId);
  
  if (!trace) {
    return { success: false, memoryId, error: 'Trace data no longer available.' };
  }
  
  // Find this memory's data in each pipeline step
  const stepAnalysis = [];
  for (const step of trace.pipelineSteps || []) {
    if (!step.output) continue;
    
    let memoryEntry = null;
    
    // Check if memory appears in this step's output
    const results = step.output.results || step.output.candidates || step.output.ranking || [];
    memoryEntry = results.find(r => {
      if (r.memoryId === memoryId) return true;
      if (r.memory?.id === memoryId) return true;
      return false;
    });
    
    if (memoryEntry) {
      stepAnalysis.push({
        stepName: step.stepName,
        reasoning: step.reasoning,
        score: memoryEntry.score,
        rank: memoryEntry.rank,
        input: step.input,
      });
    }
  }
  
  // Calculate attribution breakdown
  const attribution = {
    bm25: null,
    vector: null,
    rerank: null,
    mmr: null,
    decay: null,
    entityBoost: null,
    importanceBoost: null,
  };
  
  for (const step of stepAnalysis) {
    const name = step.stepName;
    if (name === 'bm25_search') attribution.bm25 = step.score;
    else if (name === 'vector_search') attribution.vector = step.score;
    else if (name === 'rerank') attribution.rerank = step.score;
    else if (name === 'mmr_diversity') attribution.mmr = step.rank;
    else if (name === 'time_decay') attribution.decay = step.score;
    else if (name === 'entity_boost') attribution.entityBoost = step.score;
    else if (name === 'importance_boost') attribution.importanceBoost = step.score;
  }
  
  return {
    success: true,
    memoryId,
    latestRetrieval: {
      queryId: latest.queryId,
      query: latest.query,
      timestamp: latest.timestamp,
      rank: latest.rank,
      score: latest.score,
    },
    totalRetrievals: history.length,
    pipelineAppearance: stepAnalysis,
    attribution,
    summary: buildAttributionSummary(attribution, stepAnalysis),
  };
}

/**
 * Build human-readable attribution summary
 * @param {object} attribution
 * @param {Array} stepAnalysis
 * @returns {string}
 */
function buildAttributionSummary(attribution, stepAnalysis) {
  const parts = [];
  
  if (attribution.bm25 != null) {
    parts.push(`BM25 keyword match contributed score ${(attribution.bm25 * 100).toFixed(1)}`);
  }
  if (attribution.vector != null) {
    parts.push(`vector similarity contributed score ${(attribution.vector * 100).toFixed(1)}`);
  }
  if (attribution.entityBoost != null) {
    parts.push(`entity boost increased score by ${((attribution.entityBoost - 1) * 100).toFixed(1)}%`);
  }
  if (attribution.importanceBoost != null) {
    parts.push(`importance boost added ${(attribution.importanceBoost * 100).toFixed(1)}%`);
  }
  if (attribution.mmr != null) {
    const survived = attribution.mmr <= 10 ? 'survived' : 'was removed by';
    parts.push(`MMR diversity: rank ${attribution.mmr}, ${survived} deduplication`);
  }
  
  if (parts.length === 0) return 'No specific factors identified.';
  return parts.join('; ') + '.';
}

/**
 * Search traces by query text
 * @param {string} querySubstr
 * @returns {Array}
 */
export function findTracesByQuery(querySubstr) {
  return searchTraces(querySubstr);
}
