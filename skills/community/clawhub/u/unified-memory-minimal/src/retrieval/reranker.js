/**
 * 重排序器 - Reranker
 * 借鉴 OpenViking 的重排序机制
 */

import { logger } from '../utils/logger.js';

/**
 * 重排序结果
 */
export class RerankResult {
  constructor(options) {
    this.uri = options.uri;
    this.text = options.text;
    this.vectorScore = options.vectorScore;
    this.rerankScore = options.rerankScore;
    this.finalScore = options.finalScore;
    this.metadata = options.metadata || {};
  }
  
  toJSON() {
    return {
      uri: this.uri,
      text: this.text,
      vectorScore: this.vectorScore,
      rerankScore: this.rerankScore,
      finalScore: this.finalScore,
      metadata: this.metadata
    };
  }
}

/**
 * 重排序器基类
 */
export class BaseReranker {
  constructor(options = {}) {
    this.options = options;
    this.stats = {
      totalReranked: 0,
      avgRerankTime: 0,
      errors: 0
    };
  }
  
  async rerank(query, documents) {
    throw new Error('Subclass must implement rerank()');
  }
  
  getStats() {
    return { ...this.stats };
  }
}

/**
 * Volcengine Reranker
 */
export class VolcengineReranker extends BaseReranker {
  constructor(options = {}) {
    super(options);
    this.client = options.client;
    this.model = options.model || 'doubao-seed-rerank';
    this.topN = options.topN || 20;
  }
  
  async rerank(query, documents) {
    const startTime = Date.now();
    
    if (!this.client) {
      logger.warn('[VolcengineReranker] 客户端未配置，回退到向量分数');
      return this.fallbackToVectorScore(documents);
    }
    
    try {
      logger.debug(`[VolcengineReranker] 重排序 ${documents.length} 个文档`);
      
      const response = await this.client.rerank({
        model: this.model,
        query: query,
        documents: documents.map(d => d.text),
        top_n: Math.min(this.topN, documents.length)
      });
      
      const results = response.results.map((r, i) => {
        const doc = documents[r.index] || documents[i];
        return new RerankResult({
          uri: doc.uri || doc.id,
          text: doc.text,
          vectorScore: doc.score || 0,
          rerankScore: r.relevance_score,
          finalScore: r.relevance_score,
          metadata: doc.metadata || {}
        });
      });
      
      // 更新统计
      const rerankTime = Date.now() - startTime;
      this.stats.totalReranked += documents.length;
      this.stats.avgRerankTime = 
        (this.stats.avgRerankTime * (this.stats.totalReranked - documents.length) + rerankTime) / 
        this.stats.totalReranked;
      
      logger.debug(`[VolcengineReranker] 重排序完成，耗时 ${rerankTime}ms`);
      
      return results;
      
    } catch (error) {
      this.stats.errors++;
      logger.error('[VolcengineReranker] 重排序失败:', error);
      return this.fallbackToVectorScore(documents);
    }
  }
  
  fallbackToVectorScore(documents) {
    return documents.map(d => new RerankResult({
      uri: d.uri || d.id,
      text: d.text,
      vectorScore: d.score || 0,
      rerankScore: null,
      finalScore: d.score || 0,
      metadata: d.metadata || {}
    }));
  }
}

/**
 * Cohere Reranker
 */
export class CohereReranker extends BaseReranker {
  constructor(options = {}) {
    super(options);
    this.apiKey = options.apiKey;
    this.model = options.model || 'rerank-english-v2.0';
    this.topN = options.topN || 20;
    this.apiUrl = options.apiUrl || 'https://api.cohere.ai/v1/rerank';
  }
  
  async rerank(query, documents) {
    const startTime = Date.now();
    
    if (!this.apiKey) {
      logger.warn('[CohereReranker] API Key 未配置，回退到向量分数');
      return this.fallbackToVectorScore(documents);
    }
    
    try {
      logger.debug(`[CohereReranker] 重排序 ${documents.length} 个文档`);
      
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.model,
          query: query,
          documents: documents.map(d => d.text),
          top_n: Math.min(this.topN, documents.length)
        })
      });
      
      if (!response.ok) {
        throw new Error(`Cohere API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const results = data.results.map(r => {
        const doc = documents[r.index];
        return new RerankResult({
          uri: doc.uri || doc.id,
          text: doc.text,
          vectorScore: doc.score || 0,
          rerankScore: r.relevance_score,
          finalScore: r.relevance_score,
          metadata: doc.metadata || {}
        });
      });
      
      // 更新统计
      const rerankTime = Date.now() - startTime;
      this.stats.totalReranked += documents.length;
      this.stats.avgRerankTime = 
        (this.stats.avgRerankTime * (this.stats.totalReranked - documents.length) + rerankTime) / 
        this.stats.totalReranked;
      
      logger.debug(`[CohereReranker] 重排序完成，耗时 ${rerankTime}ms`);
      
      return results;
      
    } catch (error) {
      this.stats.errors++;
      logger.error('[CohereReranker] 重排序失败:', error);
      return this.fallbackToVectorScore(documents);
    }
  }
  
  fallbackToVectorScore(documents) {
    return documents.map(d => new RerankResult({
      uri: d.uri || d.id,
      text: d.text,
      vectorScore: d.score || 0,
      rerankScore: null,
      finalScore: d.score || 0,
      metadata: d.metadata || {}
    }));
  }
}

/**
 * Jina Reranker
 */
export class JinaReranker extends BaseReranker {
  constructor(options = {}) {
    super(options);
    this.apiKey = options.apiKey;
    this.model = options.model || 'jina-reranker-v2-base-multilingual';
    this.topN = options.topN || 20;
    this.apiUrl = options.apiUrl || 'https://api.jina.ai/v1/rerank';
  }
  
  async rerank(query, documents) {
    const startTime = Date.now();
    
    if (!this.apiKey) {
      logger.warn('[JinaReranker] API Key 未配置，回退到向量分数');
      return this.fallbackToVectorScore(documents);
    }
    
    try {
      logger.debug(`[JinaReranker] 重排序 ${documents.length} 个文档`);
      
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.model,
          query: query,
          documents: documents.map(d => d.text),
          top_n: Math.min(this.topN, documents.length)
        })
      });
      
      if (!response.ok) {
        throw new Error(`Jina API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      const results = data.results.map(r => {
        const doc = documents[r.index];
        return new RerankResult({
          uri: doc.uri || doc.id,
          text: doc.text,
          vectorScore: doc.score || 0,
          rerankScore: r.relevance_score,
          finalScore: r.relevance_score,
          metadata: doc.metadata || {}
        });
      });
      
      // 更新统计
      const rerankTime = Date.now() - startTime;
      this.stats.totalReranked += documents.length;
      this.stats.avgRerankTime = 
        (this.stats.avgRerankTime * (this.stats.totalReranked - documents.length) + rerankTime) / 
        this.stats.totalReranked;
      
      logger.debug(`[JinaReranker] 重排序完成，耗时 ${rerankTime}ms`);
      
      return results;
      
    } catch (error) {
      this.stats.errors++;
      logger.error('[JinaReranker] 重排序失败:', error);
      return this.fallbackToVectorScore(documents);
    }
  }
  
  fallbackToVectorScore(documents) {
    return documents.map(d => new RerankResult({
      uri: d.uri || d.id,
      text: d.text,
      vectorScore: d.score || 0,
      rerankScore: null,
      finalScore: d.score || 0,
      metadata: d.metadata || {}
    }));
  }
}

/**
 * 本地重排序器（基于关键词匹配）
 */
export class LocalReranker extends BaseReranker {
  constructor(options = {}) {
    super(options);
    this.weights = {
      exactMatch: 0.3,
      partialMatch: 0.2,
      tfidf: 0.3,
      position: 0.2
    };
  }
  
  async rerank(query, documents) {
    const startTime = Date.now();
    
    logger.debug(`[LocalReranker] 重排序 ${documents.length} 个文档`);
    
    const queryTerms = this.tokenize(query.toLowerCase());
    
    const results = documents.map(doc => {
      const text = doc.text.toLowerCase();
      const docTerms = this.tokenize(text);
      
      // 精确匹配分数
      const exactMatchScore = this.calculateExactMatch(queryTerms, docTerms);
      
      // 部分匹配分数
      const partialMatchScore = this.calculatePartialMatch(queryTerms, docTerms);
      
      // TF-IDF 分数
      const tfidfScore = this.calculateTFIDF(queryTerms, docTerms, documents);
      
      // 位置分数
      const positionScore = this.calculatePositionScore(queryTerms, text);
      
      // 综合分数
      const rerankScore = 
        this.weights.exactMatch * exactMatchScore +
        this.weights.partialMatch * partialMatchScore +
        this.weights.tfidf * tfidfScore +
        this.weights.position * positionScore;
      
      return new RerankResult({
        uri: doc.uri || doc.id,
        text: doc.text,
        vectorScore: doc.score || 0,
        rerankScore: rerankScore,
        finalScore: rerankScore,
        metadata: doc.metadata || {}
      });
    });
    
    // 按分数排序
    results.sort((a, b) => b.finalScore - a.finalScore);
    
    // 更新统计
    const rerankTime = Date.now() - startTime;
    this.stats.totalReranked += documents.length;
    this.stats.avgRerankTime = 
      (this.stats.avgRerankTime * (this.stats.totalReranked - documents.length) + rerankTime) / 
      this.stats.totalReranked;
    
    logger.debug(`[LocalReranker] 重排序完成，耗时 ${rerankTime}ms`);
    
    return results;
  }
  
  tokenize(text) {
    return text.split(/\s+/).filter(t => t.length > 0);
  }
  
  calculateExactMatch(queryTerms, docTerms) {
    const querySet = new Set(queryTerms);
    const docSet = new Set(docTerms);
    
    let matchCount = 0;
    for (const term of querySet) {
      if (docSet.has(term)) {
        matchCount++;
      }
    }
    
    return matchCount / querySet.size;
  }
  
  calculatePartialMatch(queryTerms, docTerms) {
    let matchCount = 0;
    
    for (const qTerm of queryTerms) {
      for (const dTerm of docTerms) {
        if (dTerm.includes(qTerm) || qTerm.includes(dTerm)) {
          matchCount++;
          break;
        }
      }
    }
    
    return matchCount / queryTerms.length;
  }
  
  calculateTFIDF(queryTerms, docTerms, allDocs) {
    const tf = {};
    for (const term of docTerms) {
      tf[term] = (tf[term] || 0) + 1;
    }
    
    const df = {};
    for (const term of queryTerms) {
      df[term] = 0;
      for (const doc of allDocs) {
        if (doc.text.toLowerCase().includes(term)) {
          df[term]++;
        }
      }
    }
    
    let score = 0;
    for (const term of queryTerms) {
      const termFreq = tf[term] || 0;
      const docFreq = df[term] || 1;
      const idf = Math.log(allDocs.length / docFreq);
      score += termFreq * idf;
    }
    
    return Math.min(score / queryTerms.length, 1);
  }
  
  calculatePositionScore(queryTerms, text) {
    const positions = [];
    
    for (const term of queryTerms) {
      const idx = text.indexOf(term);
      if (idx >= 0) {
        positions.push(idx);
      }
    }
    
    if (positions.length === 0) return 0;
    
    const avgPosition = positions.reduce((a, b) => a + b, 0) / positions.length;
    const maxPosition = text.length;
    
    return 1 - (avgPosition / maxPosition);
  }
}

/**
 * 重排序器工厂
 */
export function getReranker(options = {}) {
  const provider = options.provider || 'local';
  
  switch (provider) {
    case 'volcengine':
      return new VolcengineReranker(options);
    case 'cohere':
      return new CohereReranker(options);
    case 'jina':
      return new JinaReranker(options);
    case 'local':
    default:
      return new LocalReranker(options);
  }
}

export default getReranker;
