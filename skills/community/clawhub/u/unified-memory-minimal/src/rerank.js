/**
 * Reranker - Multi-signal reranking for memory retrieval
 * 
 * v3.1: Adds multi-signal rule-based rerank to complement the existing LlmReranker.
 * Multi-signal rerank uses: keyword overlap, entity match, recency, importance, scope, category.
 * 
 * Original LlmReranker (LLM-based cross-encoder) is preserved alongside.
 */

import { config } from './config.js';

// ============ LlmReranker (original - preserved) ============

function getLlmProvider() {
  const providers = config.llmProviders || [];
  return providers.find(p => p.name === 'ollama') || providers[0] || {
    baseURL: process.env.OLLAMA_HOST || 'http://localhost:11434',
    model: 'qwen2.5:7b',
    apiKey: null,
  };
}

export class LlmReranker {
  constructor(llmUrl = null, model = null) {
    const defaultProvider = getLlmProvider();
    this.llmUrl = llmUrl || defaultProvider.baseURL;
    this.model = model || defaultProvider.model;
    this.initialized = true;
  }

  async rerank(query, documents, topK = 5) {
    if (!documents || documents.length === 0) return [];
    if (documents.length === 1) return documents.slice(0, topK);

    const scored = await Promise.all(documents.map(async (doc) => {
      const text = doc.memory?.text || doc.memory?.content || '';
      if (!text) return { ...doc, rerankScore: doc.score || 0 };
      
      const prompt = `Query: ${query}\nDocument: ${text.slice(0, 500)}\nScore 1-10 how relevant is this document to the query. Reply only with the number:`;
      
      let rerankScore = doc.score || 0;
      try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 3000);
        const res = await fetch(`${this.llmUrl}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: this.model, prompt, stream: false, options: { num_predict: 8 } }),
          signal: controller.signal,
        });
        clearTimeout(timer);
        if (res.ok) {
          const json = await res.json();
          const match = json.response?.match(/\d+/);
          if (match) rerankScore = parseInt(match[0]) / 10;
        }
      } catch { /* fallback */ }
      
      return { ...doc, rerankScore };
    }));

    return scored
      .sort((a, b) => b.rerankScore - a.rerankScore)
      .slice(0, topK);
  }
}

export function keywordRerank(query, documents, topK = 5) {
  const queryWords = query.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  if (queryWords.length === 0) return documents.slice(0, topK);

  return documents
    .map(doc => {
      const text = (doc.memory?.text || doc.memory?.content || '').toLowerCase();
      const matches = queryWords.filter(w => text.includes(w)).length;
      return { ...doc, rerankScore: (doc.score || 0) + matches * 0.1 };
    })
    .sort((a, b) => b.rerankScore - a.rerankScore)
    .slice(0, topK);
}

// ============ Multi-Signal Rerank (v3.1 new) ============

const RERANK_CONFIG = {
  topK: 5,
  keywordWeight: 0.25,
  entityWeight: 0.20,
  importanceWeight: 0.15,
  recencyWeight: 0.15,
  scopeWeight: 0.15,
  categoryWeight: 0.10,
  recencyDays: 7,
};

const CATEGORY_PRIORITY = {
  identity: 5, preference: 4, decision: 3, skill: 3, goal: 3,
  reflection: 2, entity: 2, fact: 1, general: 0, conversation: -1,
};

const SCOPE_PRIORITY = { USER: 4, TEAM: 3, AGENT: 2, GLOBAL: 1, '': 4 };

function tokenize(text) {
  if (!text) return new Set();
  return new Set(text.toLowerCase().split(/[\s,.!?;:()\[\]{}'"-]+/).filter(t => t.length >= 2));
}

function overlapFraction(setA, setB) {
  if (!setA.size || !setB.size) return 0;
  return [...setA].filter(x => setB.has(x)).length / setA.size;
}

function detectEntities(text) {
  if (!text) return [];
  const entities = [];
  const patterns = [
    /\b(Claude|OpenAI|GPT|MiniMax|DeepSeek|Ollama|LanceDB|BM25|Elasticsearch)\b/gi,
    /\b(飞书|Lark|钉钉|微信|Discord|Telegram|Slack|Signal)\b/gi,
    /\b(MCP|API|REST|GraphQL|gRPC|WebSocket|SSE)\b/gi,
    /\b(macOS|Linux|Windows|Docker|Kubernetes)\b/gi,
    /\b(ou_[a-z0-9]+|oc_[a-z0-9]+|mem_[^\s,]+)\b/gi,
  ];
  for (const p of patterns) { let m; while ((m = p.exec(text)) !== null) entities.push(m[1] || m[0]); }
  return [...new Set(entities)];
}

function recencyScore(mem) {
  const ts = mem.updated_at || mem.created_at;
  if (!ts) return 0.0;
  const updatedAt = typeof ts === 'string' ? new Date(ts).getTime() : ts;
  if (isNaN(updatedAt)) return 0.0;
  const daysDiff = (Date.now() - updatedAt) / (1000 * 60 * 60 * 24);
  return daysDiff <= RERANK_CONFIG.recencyDays ? 1.0 : Math.max(0, 1 - (daysDiff / 365));
}

function temporalValidity(mem) {
  if (!mem.valid_to) return 1.0;
  const vt = typeof mem.valid_to === 'string' ? new Date(mem.valid_to).getTime() : mem.valid_to;
  return Date.now() <= vt ? 1.0 : 0.0;
}

/**
 * Multi-signal rule-based reranking
 * Combines: keyword overlap, entity match, recency, importance, scope, category
 * 
 * @param {string} query
 * @param {Array} candidates - {memory, fusionScore?, bm25Score?, vectorScore?}[]
 * @param {object} options - {topK}
 * @returns {Array} reranked results
 */
export function rerank(query, candidates, options = {}) {
  const { topK = RERANK_CONFIG.topK } = options;
  
  if (!candidates || candidates.length === 0) return [];
  if (candidates.length === 1) {
    return [{ ...candidates[0], rerankScore: candidates[0].fusionScore || candidates[0].vectorScore || 0 }];
  }

  const queryTokens = tokenize(query);
  const queryEntities = detectEntities(query);

  const reranked = candidates.map(candidate => {
    const mem = candidate.memory;
    const text = mem.text || '';
    const contentTokens = tokenize(text);
    const contentEntities = detectEntities(text);

    const keywordScore = overlapFraction(queryTokens, contentTokens);
    const entityScore = overlapFraction(new Set(queryEntities), new Set(contentEntities));
    const importanceScore = mem.importance || 0.5;
    const recency = recencyScore(mem);
    const temporal = temporalValidity(mem);
    const categoryPriority = (CATEGORY_PRIORITY[mem.category] ?? 0) / 5;
    const scopePriority = (SCOPE_PRIORITY[mem.scope || ''] ?? 4) / 4;
    const vectorScore = candidate.vectorScore || candidate.score || 0;
    const bm25Score = candidate.bm25Score ? Math.min(1, candidate.bm25Score / 10) : 0;

    const rerankScore = (
      keywordScore * RERANK_CONFIG.keywordWeight +
      entityScore * RERANK_CONFIG.entityWeight +
      importanceScore * RERANK_CONFIG.importanceWeight +
      recency * RERANK_CONFIG.recencyWeight +
      categoryPriority * RERANK_CONFIG.categoryWeight +
      scopePriority * RERANK_CONFIG.scopeWeight +
      vectorScore * 0.5 +
      bm25Score * 0.3 +
      temporal * 0.05
    );

    return {
      ...candidate,
      rerankScore: Math.min(1, Math.max(0, rerankScore)),
      signals: { keywordScore, entityScore, importanceScore, recency, categoryPriority, scopePriority },
    };
  });

  reranked.sort((a, b) => {
    if (b.rerankScore !== a.rerankScore) return b.rerankScore - a.rerankScore;
    return (b.memory.importance || 0.5) - (a.memory.importance || 0.5);
  });

  return reranked.slice(0, topK);
}
