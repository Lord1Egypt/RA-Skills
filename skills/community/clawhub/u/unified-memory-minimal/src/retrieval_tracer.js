/**
 * Retrieval Tracer v1.0 - Memory Replay Debugger (Feature #8)
 * 
 * Records every step of the search pipeline for each query.
 * Like `git blame` for memory retrieval - trace exactly how a memory was retrieved.
 * 
 * Data logged per query:
 *   { queryId, query, timestamp, pipelineSteps[], results[], finalRanking[], durationMs }
 * 
 * Each step record:
 *   { stepName, input, output, score, reasoning }
 * 
 * Storage: ~/.openclaw/workspace/memory/retrieval_traces.json (rolling window, last 1000)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from './config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TRACES_FILE = join(config.memoryDir, 'retrieval_traces.json');

// In-memory cache for ultra-fast reads during replay
let _traceCache = null;
let _cacheExpiry = 0;
const CACHE_TTL_MS = 5000; // 5 second cache

// Per-memory index: memoryId → [{ queryId, rank, score, timestamp }]
let _memoryIndex = new Map();

// Global query counter for IDs
let _queryCounter = 0;

/**
 * Load all traces from disk (with caching)
 * @returns {Array}
 */
function loadTraces() {
  const now = Date.now();
  if (_traceCache && now < _cacheExpiry) {
    return _traceCache;
  }
  
  if (!existsSync(TRACES_FILE)) {
    _traceCache = [];
    _cacheExpiry = now + CACHE_TTL_MS;
    return [];
  }
  
  try {
    const raw = readFileSync(TRACES_FILE, 'utf-8');
    _traceCache = JSON.parse(raw);
    _cacheExpiry = now + CACHE_TTL_MS;
    return _traceCache;
  } catch {
    _traceCache = [];
    _cacheExpiry = now + CACHE_TTL_MS;
    return [];
  }
}

/**
 * Persist traces to disk
 * @param {Array} traces
 */
function saveTraces(traces) {
  try {
    const dir = dirname(TRACES_FILE);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    // Rolling window: keep only last maxTraces
    const trimmed = traces.slice(-config.maxTraces);
    writeFileSync(TRACES_FILE, JSON.stringify(trimmed, null, 2), 'utf-8');
    _traceCache = trimmed;
    _cacheExpiry = 0; // invalidate cache
  } catch (err) {
    console.error('[retrieval_tracer] saveTraces failed:', err.message);
  }
}

/**
 * Generate a unique query trace ID
 * @returns {string}
 */
export function generateQueryId() {
  _queryCounter++;
  return `qt-${Date.now().toString(36)}-${_queryCounter.toString(36).padStart(4, '0')}`;
}

/**
 * Start a new retrieval trace session
 * @param {string} query 
 * @param {object} options - { scope, mode, topK, enableRerank, enableMMR, enableDecay }
 * @returns {object} - trace context
 */
export function startRetrievalTrace(query, options = {}) {
  if (!config.traceRetrieval) {
    return null;
  }
  
  const queryId = generateQueryId();
  const startTime = Date.now();
  
  return {
    queryId,
    query,
    timestamp: new Date().toISOString(),
    options: { ...options },
    pipelineSteps: [],
    startTime,
    _active: true,
  };
}

/**
 * Record a pipeline step
 * @param {object} traceCtx - trace context from startRetrievalTrace
 * @param {string} stepName - e.g., 'bm25_search', 'vector_search', 'mmr', 'rerank'
 * @param {object} input - what went into this step
 * @param {object} output - what came out
 * @param {number} score - score if applicable
 * @param {string} reasoning - why this step did what it did
 */
export function recordPipelineStep(traceCtx, stepName, input, output, score = null, reasoning = '') {
  if (!traceCtx || !traceCtx._active) return;
  
  const step = {
    stepName,
    input: sanitizeForTrace(input),
    output: sanitizeForTrace(output),
    score,
    reasoning,
    timestamp: Date.now(),
    durationMs: Date.now() - traceCtx.startTime,
  };
  
  traceCtx.pipelineSteps.push(step);
}

/**
 * Record BM25 step
 * @param {object} traceCtx
 * @param {string} query
 * @param {Array} candidates - BM25 results
 * @param {number} topK
 */
export function traceBm25Step(traceCtx, query, candidates, topK) {
  const topResults = candidates.slice(0, topK);
  recordPipelineStep(traceCtx, 'bm25_search', 
    { query, topK, totalCandidates: candidates.length },
    { 
      results: topResults.map((r, i) => ({
        memoryId: r.memory?.id,
        text: r.memory?.text?.slice(0, 80),
        score: r.score,
        rank: i + 1,
      })),
      count: topResults.length,
    },
    topResults[0]?.score,
    `BM25 keyword matching: found ${candidates.length} candidates, returned top ${topResults.length}`
  );
}

/**
 * Record Vector search step
 * @param {object} traceCtx
 * @param {string} query
 * @param {Array} candidates
 * @param {number} topK
 */
export function traceVectorStep(traceCtx, query, candidates, topK) {
  const topResults = candidates.slice(0, topK);
  recordPipelineStep(traceCtx, 'vector_search',
    { query, topK, totalCandidates: candidates.length },
    {
      results: topResults.map((r, i) => ({
        memoryId: r.memory?.id,
        text: r.memory?.text?.slice(0, 80),
        score: r.score,
        rank: i + 1,
      })),
      count: topResults.length,
    },
    topResults[0]?.score,
    `Vector similarity search: found ${candidates.length} candidates, returned top ${topResults.length}`
  );
}

/**
 * Record merge/fusion step
 * @param {object} traceCtx
 * @param {Array} candidates - merged candidates
 * @param {string} mode - 'hybrid', 'bm25', 'vector'
 */
export function traceMergeStep(traceCtx, candidates, mode = 'hybrid') {
  recordPipelineStep(traceCtx, 'merge_candidates',
    { mode, candidateCount: candidates.length },
    {
      candidates: candidates.slice(0, 10).map((c, i) => ({
        memoryId: c.memory?.id,
        bm25Score: c.bm25Score,
        vectorScore: c.vectorScore,
        score: c.score,
        rank: i + 1,
      })),
    },
    candidates[0]?.score,
    `Merged BM25 + vector candidates using ${mode} mode`
  );
}

/**
 * Record rerank step
 * @param {object} traceCtx
 * @param {Array} before - before reranking
 * @param {Array} after - after reranking
 * @param {string} method - 'keyword', 'llm', 'cross-encoder'
 */
export function traceRerankStep(traceCtx, before, after, method = 'keyword') {
  const topChanges = [];
  for (let i = 0; i < Math.min(5, after.length); i++) {
    const newId = after[i]?.memory?.id;
    const oldRank = before.findIndex(b => b.memory?.id === newId);
    topChanges.push({
      memoryId: newId,
      text: after[i]?.memory?.text?.slice(0, 60),
      oldRank: oldRank >= 0 ? oldRank + 1 : 'new',
      newRank: i + 1,
      score: after[i]?.score,
    });
  }
  
  recordPipelineStep(traceCtx, 'rerank',
    { method, inputCount: before.length },
    { 
      topChanges,
      outputCount: after.length,
    },
    after[0]?.score,
    `Reranked using ${method}: top result ${before[0]?.memory?.id === after[0]?.memory?.id ? 'unchanged' : 'changed'}`
  );
}

/**
 * Record MMR/diversity step
 * @param {object} traceCtx
 * @param {Array} before
 * @param {Array} after
 * @param {number} lambda
 */
export function traceMmrStep(traceCtx, before, after, lambda = 0.5) {
  const removed = before.filter(b => !after.find(a => a.memory?.id === b.memory?.id));
  recordPipelineStep(traceCtx, 'mmr_diversity',
    { lambda, inputCount: before.length, outputCount: after.length },
    {
      selected: after.slice(0, 5).map((a, i) => ({
        memoryId: a.memory?.id,
        text: a.memory?.text?.slice(0, 60),
        rank: i + 1,
      })),
      removed: removed.slice(0, 3).map(r => ({
        memoryId: r.memory?.id,
        text: r.memory?.text?.slice(0, 60),
        reason: 'diversity deduplication',
      })),
    },
    after[0]?.score,
    `MMR diversity (λ=${lambda}): selected ${after.length} from ${before.length}, removed ${removed.length} for diversity`
  );
}

/**
 * Record decay step
 * @param {object} traceCtx
 * @param {Array} before
 * @param {Array} after
 * @param {number} halfLifeDays
 * @param {number} maxBoost
 */
export function traceDecayStep(traceCtx, before, after, halfLifeDays = 30, maxBoost = 0.3) {
  const boosted = after.filter(a => (a.decay ?? 1) > 1);
  recordPipelineStep(traceCtx, 'time_decay',
    { halfLifeDays, maxBoost, inputCount: before.length },
    {
      boosted: boosted.slice(0, 5).map(b => ({
        memoryId: b.memory?.id,
        ageDays: b.ageDays,
        decayFactor: b.decay,
        scoreBefore: before.find(p => p.memory?.id === b.memory?.id)?.score,
        scoreAfter: b.score,
      })),
    },
    after[0]?.score,
    `Weibull time decay (halfLife=${halfLifeDays}d): ${boosted.length} memories boosted for recency`
  );
}

/**
 * Record entity/graph boost step
 * @param {object} traceCtx
 * @param {Array} before
 * @param {Array} after
 * @param {Array} entityNames
 */
export function traceEntityBoostStep(traceCtx, before, after, entityNames = []) {
  const boosted = after.filter(a => (a.graphBoost ?? 1) > 1);
  recordPipelineStep(traceCtx, 'entity_boost',
    { entities: entityNames, inputCount: before.length },
    {
      boosted: boosted.slice(0, 5).map(b => ({
        memoryId: b.memory?.id,
        graphBoost: b.graphBoost,
        scoreBefore: before.find(p => p.memory?.id === b.memory?.id)?.score,
        scoreAfter: b.score,
      })),
    },
    after[0]?.score,
    `Entity boost for [${entityNames.join(', ')}]: ${boosted.length} memories boosted`
  );
}

/**
 * Record importance boost step
 * @param {object} traceCtx
 * @param {Array} before
 * @param {Array} after
 */
export function traceImportanceBoostStep(traceCtx, before, after) {
  const boosted = after.filter(a => (a.importanceBoost ?? 0) > 0);
  recordPipelineStep(traceCtx, 'importance_boost',
    { inputCount: before.length },
    {
      boosted: boosted.slice(0, 5).map(b => ({
        memoryId: b.memory?.id,
        importanceBoost: b.importanceBoost,
        dynamicImportance: b.dynamicImportance,
        scoreBefore: before.find(p => p.memory?.id === b.memory?.id)?.score,
        scoreAfter: b.score,
      })),
    },
    after[0]?.score,
    `Importance boost: ${boosted.length} memories boosted based on usage patterns`
  );
}

/**
 * Record final ranking
 * @param {object} traceCtx
 * @param {Array} results
 */
export function recordFinalRanking(traceCtx, results) {
  if (!traceCtx || !traceCtx._active) return;
  
  const durationMs = Date.now() - traceCtx.startTime;
  
  recordPipelineStep(traceCtx, 'final_ranking',
    { resultCount: results.length },
    {
      ranking: results.slice(0, 10).map((r, i) => ({
        memoryId: r.memory?.id,
        text: r.memory?.text?.slice(0, 80),
        score: r.score,
        bm25Score: r.bm25Score,
        vectorScore: r.vectorScore,
        rank: i + 1,
        category: r.memory?.category,
      })),
    },
    results[0]?.score,
    `Final ranking complete: ${results.length} results in ${durationMs}ms`
  );
  
  traceCtx.finalRanking = results.slice(0, 20).map((r, i) => ({
    memoryId: r.memory?.id,
    text: r.memory?.text?.slice(0, 80),
    score: r.score,
    rank: i + 1,
  }));
  traceCtx.durationMs = durationMs;
  traceCtx._active = false;
}

/**
 * Finalize and persist a trace
 * @param {object} traceCtx
 */
export function finalizeTrace(traceCtx) {
  if (!traceCtx) return;
  
  // Mark as inactive
  traceCtx._active = false;
  
  if (!config.traceRetrieval) return;
  
  const traces = loadTraces();
  traces.push({
    queryId: traceCtx.queryId,
    query: traceCtx.query,
    timestamp: traceCtx.timestamp,
    options: traceCtx.options,
    pipelineSteps: traceCtx.pipelineSteps,
    finalRanking: traceCtx.finalRanking || [],
    durationMs: traceCtx.durationMs || Date.now() - traceCtx.startTime,
  });
  
  // Update per-memory index
  if (traceCtx.finalRanking) {
    for (const item of traceCtx.finalRanking) {
      if (!item.memoryId) continue;
      const idx = _memoryIndex.get(item.memoryId) || [];
      idx.push({
        queryId: traceCtx.queryId,
        rank: item.rank,
        score: item.score,
        timestamp: traceCtx.timestamp,
      });
      _memoryIndex.set(item.memoryId, idx);
    }
  }
  
  saveTraces(traces);
}

/**
 * Get all traces
 * @param {number} limit
 * @returns {Array}
 */
export function getAllTraces(limit = 100) {
  const traces = loadTraces();
  return traces.slice(-limit);
}

/**
 * Get a specific trace by query ID
 * @param {string} queryId
 * @returns {object|null}
 */
export function getTraceById(queryId) {
  const traces = loadTraces();
  return traces.find(t => t.queryId === queryId) || null;
}

/**
 * Get retrieval history for a specific memory
 * @param {string} memoryId
 * @returns {Array}
 */
export function getMemoryRetrievalHistory(memoryId) {
  const traces = loadTraces();
  const history = [];
  
  for (const trace of traces) {
    if (!trace.finalRanking) continue;
    const entry = trace.finalRanking.find(r => r.memoryId === memoryId);
    if (entry) {
      history.push({
        queryId: trace.queryId,
        query: trace.query,
        timestamp: trace.timestamp,
        rank: entry.rank,
        score: entry.score,
        durationMs: trace.durationMs,
      });
    }
  }
  
  return history.sort((a, b) => b.timestamp.localeCompare(a.timestamp));
}

/**
 * Get memory index stats
 * @returns {object}
 */
export function getMemoryIndexStats() {
  const traces = loadTraces();
  return {
    totalTraces: traces.length,
    indexedMemories: _memoryIndex.size,
    oldestTrace: traces[0]?.timestamp || null,
    newestTrace: traces[traces.length - 1]?.timestamp || null,
  };
}

/**
 * Sanitize data for tracing (avoid serializing circular refs, too-large data)
 * @param {any} data
 * @returns {any}
 */
function sanitizeForTrace(data) {
  if (data === null || data === undefined) return null;
  if (typeof data === 'string') return data.slice(0, 500);
  if (typeof data === 'number' || typeof data === 'boolean') return data;
  if (Array.isArray(data)) {
    return data.slice(0, 50).map(sanitizeForTrace);
  }
  if (typeof data === 'object') {
    const safe = {};
    for (const [k, v] of Object.entries(data)) {
      if (k === 'memory' && v && typeof v === 'object') {
        safe[k] = { id: v.id, text: String(v.text || '').slice(0, 100), category: v.category };
      } else {
        safe[k] = sanitizeForTrace(v);
      }
    }
    return safe;
  }
  return String(data).slice(0, 200);
}

/**
 * Clear all traces
 */
export function clearAllTraces() {
  _traceCache = [];
  _memoryIndex.clear();
  try {
    if (existsSync(TRACES_FILE)) {
      writeFileSync(TRACES_FILE, '[]', 'utf-8');
    }
  } catch (err) {
    console.error('[retrieval_tracer] clearAllTraces failed:', err.message);
  }
}

/**
 * Get traces matching a query substring
 * @param {string} querySubstr
 * @returns {Array}
 */
export function searchTraces(querySubstr) {
  const traces = loadTraces();
  const q = querySubstr.toLowerCase();
  return traces.filter(t => t.query.toLowerCase().includes(q));
}
