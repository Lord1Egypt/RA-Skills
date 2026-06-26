/**
 * Memory Attribution v1.0 - Memory Replay Debugger (Feature #8)
 * 
 * For any memory in final results, attribute its score to specific factors:
 *   - BM25 keyword match contribution
 *   - Vector similarity contribution
 *   - Entity boost contribution
 *   - Importance score contribution
 *   - Recency/decay contribution
 *   - Scope match contribution
 * 
 * Output: pie chart data or structured breakdown
 */

import { getTraceById, getAllTraces } from './retrieval_tracer.js';

/**
 * Attribute a memory's retrieval score to contributing factors
 * 
 * @param {string} memoryId
 * @param {string} queryId - optional, uses most recent if not provided
 * @returns {object} - structured attribution breakdown
 */
export function attributeMemoryScore(memoryId, queryId = null) {
  // Get traces and find the relevant one
  const traces = getAllTraces(1000);
  
  let trace = null;
  if (queryId) {
    trace = traces.find(t => t.queryId === queryId);
  } else {
    // Find most recent trace that includes this memory
    for (let i = traces.length - 1; i >= 0; i--) {
      if (traces[i].finalRanking?.some(r => r.memoryId === memoryId)) {
        trace = traces[i];
        break;
      }
    }
  }
  
  if (!trace) {
    return {
      success: false,
      memoryId,
      error: 'No trace found for this memory. Tracing may be disabled or memory was never retrieved.',
    };
  }
  
  // Extract score contributions from pipeline steps
  const contributions = {
    bm25: { score: 0, weight: 0, label: 'BM25 Keyword Match' },
    vector: { score: 0, weight: 0, label: 'Vector Similarity' },
    entityBoost: { score: 0, weight: 0, label: 'Entity Boost' },
    importanceBoost: { score: 0, weight: 0, label: 'Importance Boost' },
    recencyDecay: { score: 0, weight: 0, label: 'Recency Decay Boost' },
    categoryWeight: { score: 0, weight: 0, label: 'Category Weight' },
    fusionScore: { score: 0, weight: 0, label: 'RRF Fusion Score' },
    rerankScore: { score: 0, weight: 0, label: 'Rerank Score' },
  };
  
  let finalScore = 0;
  let foundInRanking = false;
  
  for (const step of trace.pipelineSteps || []) {
    const output = step.output || {};
    const results = output.results || output.candidates || output.ranking || [];
    
    // Find this memory in step results
    const entry = results.find(r => 
      r.memoryId === memoryId || r.memory?.id === memoryId
    );
    
    if (!entry) continue;
    
    const score = entry.score ?? 0;
    
    if (step.stepName === 'bm25_search') {
      contributions.bm25.score = score;
      contributions.bm25.weight = score > 0 ? Math.abs(score) : 0;
    } else if (step.stepName === 'vector_search') {
      contributions.vector.score = score;
      contributions.vector.weight = score > 0 ? Math.abs(score) : 0;
    } else if (step.stepName === 'entity_boost') {
      // Entity boost is multiplicative: show the boost factor
      const beforeScore = step.input?._beforeScore || score;
      contributions.entityBoost.score = score;
      contributions.entityBoost.weight = score - beforeScore;
    } else if (step.stepName === 'importance_boost') {
      const beforeImp = step.input?._beforeScore || score;
      contributions.importanceBoost.score = score;
      contributions.importanceBoost.weight = score - beforeImp;
    } else if (step.stepName === 'time_decay') {
      contributions.recencyDecay.score = score;
      contributions.recencyDecay.weight = Math.max(0, score - (step.input?._beforeScore || score));
    } else if (step.stepName === 'rerank') {
      contributions.rerankScore.score = score;
      contributions.rerankScore.weight = score;
    }
    
    if (step.stepName === 'final_ranking') {
      finalScore = score;
      foundInRanking = true;
      // Parse rank info
      if (entry.rank !== undefined) {
        contributions._rank = entry.rank;
      }
    }
  }
  
  // Build pie chart data
  const totalPositiveWeight = Object.values(contributions)
    .filter(c => typeof c.weight === 'number' && c.weight > 0)
    .reduce((sum, c) => sum + c.weight, 0);
  
  const pieData = Object.entries(contributions)
    .filter(([key]) => !key.startsWith('_'))
    .map(([key, c]) => {
      const value = totalPositiveWeight > 0 
        ? Math.round((c.weight / totalPositiveWeight) * 10000) / 100  // percentage
        : 0;
      return {
        factor: key,
        label: c.label,
        rawScore: c.score,
        weight: c.weight,
        percentage: value,
      };
    })
    .filter(d => d.percentage > 0)
    .sort((a, b) => b.percentage - a.percentage);
  
  // Structured breakdown
  const breakdown = {
    memoryId,
    queryId: trace.queryId,
    query: trace.query,
    timestamp: trace.timestamp,
    finalScore: Math.round(finalScore * 1000) / 1000,
    rank: contributions._rank || null,
    pieChart: pieData,
    breakdown: pieData.map(d => ({
      factor: d.factor,
      description: d.label,
      contribution: d.percentage > 0 
        ? `${d.percentage.toFixed(1)}% (raw score: ${d.rawScore.toFixed(4)})`
        : 'N/A',
    })),
  };
  
  return {
    success: true,
    ...breakdown,
  };
}

/**
 * Generate pie chart data for score attribution
 * @param {string} memoryId
 * @param {string} queryId
 * @returns {object}
 */
export function getAttributionPieChart(memoryId, queryId = null) {
  const result = attributeMemoryScore(memoryId, queryId);
  if (!result.success) return result;
  
  return {
    success: true,
    memoryId,
    queryId: result.queryId,
    pieChart: result.pieChart,
    // Simple ASCII bar chart
    asciiChart: result.pieChart.map(p => {
      const barLen = Math.round(p.percentage / 2);
      const bar = '█'.repeat(barLen);
      return `${p.label.padEnd(20)} ${bar} ${p.percentage.toFixed(1)}%`;
    }).join('\n'),
  };
}

/**
 * Get score breakdown for multiple memories in a single query
 * @param {string} queryId
 * @returns {object}
 */
export function attributeQueryResults(queryId) {
  const trace = getTraceById(queryId);
  if (!trace) {
    return { success: false, error: `Trace not found: ${queryId}` };
  }
  
  const ranking = trace.finalRanking || [];
  const results = [];
  
  for (const entry of ranking) {
    if (!entry.memoryId) continue;
    const attr = attributeMemoryScore(entry.memoryId, queryId);
    results.push({
      rank: entry.rank,
      memoryId: entry.memoryId,
      text: entry.text?.slice(0, 60),
      finalScore: entry.score,
      topFactor: attr.pieChart?.[0]?.label || 'unknown',
      topFactorPct: attr.pieChart?.[0]?.percentage || 0,
    });
  }
  
  return {
    success: true,
    queryId,
    query: trace.query,
    timestamp: trace.timestamp,
    attributionSummary: results,
    totalResults: results.length,
  };
}
