/**
 * Trace Analyzer v1.0 - Memory Replay Debugger (Feature #8)
 * 
 * Analyze retrieval patterns across all traces.
 * - Find: most common failing patterns (high recall low precision etc)
 * - Detect: systematic biases (always misses certain categories, etc)
 * - Suggest: tuning parameters based on trace analysis
 */

import { getAllTraces, getMemoryIndexStats, clearAllTraces } from './retrieval_tracer.js';

/**
 * Analyze all traces and return retrieval quality statistics
 * @param {number} limit - number of recent traces to analyze (default 200)
 * @returns {object}
 */
export function analyzeRetrievalPatterns(limit = 200) {
  const traces = getAllTraces(limit);
  
  if (traces.length === 0) {
    return {
      success: true,
      message: 'No traces available. Enable traceRetrieval in config.',
      stats: null,
    };
  }
  
  // Basic stats
  const totalTraces = traces.length;
  const durations = traces.map(t => t.durationMs).filter(d => d != null);
  const avgDuration = durations.length > 0 
    ? durations.reduce((a, b) => a + b, 0) / durations.length 
    : 0;
  
  // Analyze each trace for patterns
  let totalResults = 0;
  let queriesWithNoResults = 0;
  const stepFailureCounts = {};
  const categoryMissCounts = {};  // category → miss count
  const categoryTotalCounts = {}; // category → total count
  const stepDurations = {};       // stepName → [durations]
  
  for (const trace of traces) {
    const resultCount = trace.finalRanking?.length || 0;
    totalResults += resultCount;
    
    if (resultCount === 0) {
      queriesWithNoResults++;
    }
    
    // Analyze pipeline steps
    for (const step of trace.pipelineSteps || []) {
      const name = step.stepName;
      
      // Track step durations
      if (!stepDurations[name]) stepDurations[name] = [];
      if (step.durationMs) {
        stepDurations[name].push(step.durationMs);
      }
      
      // Track failures (low scores, no results)
      if (step.score === 0 || step.output?.count === 0) {
        stepFailureCounts[name] = (stepFailureCounts[name] || 0) + 1;
      }
    }
    
    // Analyze final ranking for category bias
    for (const entry of trace.finalRanking || []) {
      const cat = entry.category || 'unknown';
      categoryTotalCounts[cat] = (categoryTotalCounts[cat] || 0) + 1;
    }
  }
  
  // Calculate failure rates per step
  const stepFailureRates = {};
  for (const [name, count] of Object.entries(stepFailureCounts)) {
    const totalStepOccurrences = traces.filter(t => 
      t.pipelineSteps?.some(s => s.stepName === name)
    ).length;
    stepFailureRates[name] = totalStepOccurrences > 0 
      ? Math.round((count / totalStepOccurrences) * 100) 
      : 0;
  }
  
  // Find systematic biases
  const biases = detectBiases(traces, categoryTotalCounts);
  
  // Find failing patterns
  const failingPatterns = detectFailingPatterns(traces);
  
  // Generate tuning suggestions
  const suggestions = generateTuningSuggestions(traces, stepFailureRates, biases);
  
  return {
    success: true,
    stats: {
      overview: {
        totalTraces,
        avgDurationMs: Math.round(avgDuration * 100) / 100,
        minDurationMs: Math.min(...durations),
        maxDurationMs: Math.max(...durations),
        totalResults,
        avgResultsPerQuery: Math.round((totalResults / totalTraces) * 100) / 100,
        zeroResultQueries: queriesWithNoResults,
        zeroResultRate: Math.round((queriesWithNoResults / totalTraces) * 100),
      },
      stepDurations: Object.fromEntries(
        Object.entries(stepDurations).map(([name, durs]) => {
          const avg = durs.length > 0 ? durs.reduce((a, b) => a + b, 0) / durs.length : 0;
          return [name, { avgMs: Math.round(avg * 100) / 100, count: durs.length }];
        })
      ),
      stepFailureRates,
      categoryDistribution: categoryTotalCounts,
      biases,
      failingPatterns,
      suggestions,
    },
  };
}

/**
 * Detect systematic biases in retrieval
 * @param {Array} traces
 * @param {object} categoryCounts
 * @returns {Array}
 */
function detectBiases(traces, categoryCounts) {
  const biases = [];
  
  // Category bias: certain categories appear much more than others
  const totalCat = Object.values(categoryCounts).reduce((a, b) => a + b, 0);
  if (totalCat > 0) {
    for (const [cat, count] of Object.entries(categoryCounts)) {
      const pct = (count / totalCat) * 100;
      if (pct > 60) {
        biases.push({
          type: 'category_dominance',
          description: `Category "${cat}" dominates ${pct.toFixed(1)}% of results`,
          severity: pct > 80 ? 'high' : 'medium',
          suggestion: `Consider boosting underrepresented categories or adjusting category weights`,
        });
      }
    }
  }
  
  // Position bias: top-3 results are always from similar sources
  // Check if certain memory IDs always appear in top-3
  const topMemoryFreq = {};
  for (const trace of traces) {
    const top3 = (trace.finalRanking || []).slice(0, 3).map(e => e.memoryId);
    for (const mid of top3) {
      topMemoryFreq[mid] = (topMemoryFreq[mid] || 0) + 1;
    }
  }
  for (const [mid, freq] of Object.entries(topMemoryFreq)) {
    const rate = (freq / traces.length) * 100;
    if (rate > 50) {
      biases.push({
        type: 'position_bias',
        description: `Memory ${mid.slice(0, 8)} appears in top-3 for ${rate.toFixed(1)}% of queries`,
        severity: rate > 80 ? 'high' : 'medium',
        suggestion: 'Consider applying diversity boost or MMR to reduce position bias',
      });
    }
  }
  
  return biases;
}

/**
 * Detect failing patterns
 * @param {Array} traces
 * @returns {Array}
 */
function detectFailingPatterns(traces) {
  const patterns = [];
  
  // High recall, low precision: many candidates but final results are poor
  for (const trace of traces) {
    const bm25Step = trace.pipelineSteps?.find(s => s.stepName === 'bm25_search');
    const vectorStep = trace.pipelineSteps?.find(s => s.stepName === 'vector_search');
    const finalCount = trace.finalRanking?.length || 0;
    
    const bm25Candidates = bm25Step?.output?.totalCandidates || 0;
    const vectorCandidates = vectorStep?.output?.totalCandidates || 0;
    
    // Pattern: many candidates but zero results
    if ((bm25Candidates > 10 || vectorCandidates > 10) && finalCount === 0) {
      patterns.push({
        type: 'high_recall_zero_precision',
        queryId: trace.queryId,
        query: trace.query,
        description: `${bm25Candidates} BM25 + ${vectorCandidates} vector candidates but 0 final results`,
        likelyCause: 'MMR or reranking may be too aggressive, or decay killed all candidates',
      });
    }
    
    // Pattern: BM25 has results but vector doesn't
    if (bm25Candidates > 0 && vectorCandidates === 0 && finalCount > 0) {
      patterns.push({
        type: 'bm25_only',
        queryId: trace.queryId,
        query: trace.query,
        description: 'Query only matched via BM25, vector search returned nothing',
        likelyCause: 'No semantic overlap with indexed memories',
      });
    }
  }
  
  // Return top 5 most significant patterns
  return patterns.slice(0, 5);
}

/**
 * Generate tuning suggestions based on analysis
 * @param {Array} traces
 * @param {object} stepFailureRates
 * @param {Array} biases
 * @returns {Array}
 */
function generateTuningSuggestions(traces, stepFailureRates, biases) {
  const suggestions = [];
  
  // Suggestion based on step failure rates
  if (stepFailureRates['bm25_search'] > 20) {
    suggestions.push({
      parameter: 'bm25.k1',
      currentIssue: `BM25 failure rate is ${stepFailureRates['bm25_search']}%`,
      suggestion: 'Consider increasing BM25 k1 parameter or checking index freshness',
      priority: 'medium',
    });
  }
  
  if (stepFailureRates['rerank'] > 30) {
    suggestions.push({
      parameter: 'rerank.enabled',
      currentIssue: `Rerank has ${stepFailureRates['rerank']}% failure rate`,
      suggestion: 'Consider disabling LLM rerank or switching to keyword rerank',
      priority: 'high',
    });
  }
  
  // Suggestion based on biases
  for (const bias of biases) {
    if (bias.type === 'category_dominance') {
      suggestions.push({
        parameter: 'categoryWeights',
        currentIssue: bias.description,
        suggestion: bias.suggestion,
        priority: bias.severity === 'high' ? 'high' : 'medium',
      });
    }
  }
  
  // General suggestion if avg results per query is low
  const avgResults = traces.reduce((sum, t) => sum + (t.finalRanking?.length || 0), 0) / Math.max(traces.length, 1);
  if (avgResults < 2) {
    suggestions.push({
      parameter: 'fetchK',
      currentIssue: `Average ${avgResults.toFixed(1)} results per query`,
      suggestion: 'Consider increasing fetchK or relaxing MMR lambda for more candidate diversity',
      priority: 'medium',
    });
  }
  
  return suggestions;
}

/**
 * Get retrieval quality score (0-100)
 * @param {number} limit
 * @returns {number}
 */
export function getRetrievalQualityScore(limit = 100) {
  const analysis = analyzeRetrievalPatterns(limit);
  if (!analysis.stats) return 0;
  
  const { overview, failingPatterns, biases } = analysis.stats;
  
  // Simple scoring: 100 - penalties
  let score = 100;
  
  // Penalty for zero-result rate
  score -= overview.zeroResultRate * 0.5;
  
  // Penalty for failing patterns
  score -= failingPatterns.length * 5;
  
  // Penalty for high-severity biases
  score -= biases.filter(b => b.severity === 'high').length * 10;
  score -= biases.filter(b => b.severity === 'medium').length * 3;
  
  return Math.max(0, Math.round(score));
}
