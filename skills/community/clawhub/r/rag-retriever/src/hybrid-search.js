// RAG 2.0 - 混合搜索模块
// Reciprocal Rank Fusion (RRF) 融合向量搜索和 BM25 搜索

import { BM25Search } from './bm25.js';

/**
 * Reciprocal Rank Fusion (RRF) 算法
 */
export function reciprocalRankFusion(rankings, k = 60) {
  const scores = new Map();

  for (const ranking of rankings) {
    for (let rank = 0; rank < ranking.length; rank++) {
      const item = ranking[rank];
      const id = item.id || item;
      const rrfScore = 1 / (k + rank + 1);
      scores.set(id, (scores.get(id) || 0) + rrfScore);
    }
  }

  return Array.from(scores.entries())
    .sort((a, b) => b[1] - a[1])
    .map(([id, score]) => ({ id, score }));
}

/**
 * 混合搜索引擎
 */
export class HybridSearch {
  constructor(options = {}) {
    this.bm25 = new BM25Search(options.bm25);
    this.embeddingProvider = options.embeddingProvider;
    this.documents = new Map();
    this.embeddings = new Map();
    this.vectorWeight = options.vectorWeight || 0.7;
    this.bm25Weight = options.bm25Weight || 0.3;
    this.rrfK = options.rrfK || 60;
  }

  /**
   * 添加文档
   */
  async addDocument(doc) {
    const { id, content, metadata = {} } = doc;
    
    // 添加到 BM25 索引
    this.bm25.addDocument(id, content, metadata);
    
    // 存储文档
    this.documents.set(id, { id, content, metadata });

    // 生成向量嵌入
    if (this.embeddingProvider) {
      try {
        const embedding = await this.embeddingProvider.embed(content);
        this.embeddings.set(id, embedding);
      } catch (err) {
        console.warn(`Failed to generate embedding for doc ${id}:`, err.message);
      }
    }
  }

  /**
   * 批量添加文档
   */
  async addDocuments(docs) {
    for (const doc of docs) {
      await this.addDocument(doc);
    }
  }

  /**
   * 余弦相似度计算
   */
  cosineSimilarity(vecA, vecB) {
    if (!vecA || !vecB || vecA.length !== vecB.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < vecA.length; i++) {
      dotProduct += vecA[i] * vecB[i];
      normA += vecA[i] * vecA[i];
      normB += vecB[i] * vecB[i];
    }
    
    const denominator = Math.sqrt(normA) * Math.sqrt(normB);
    return denominator === 0 ? 0 : dotProduct / denominator;
  }

  /**
   * 向量搜索
   */
  async vectorSearch(query, topK = 10) {
    if (!this.embeddingProvider) return [];

    const queryEmbedding = await this.embeddingProvider.embed(query);
    const scores = [];

    for (const [docId, docEmbedding] of this.embeddings) {
      const similarity = this.cosineSimilarity(queryEmbedding, docEmbedding);
      scores.push({
        id: docId,
        score: similarity,
        content: this.documents.get(docId).content,
        metadata: this.documents.get(docId).metadata
      });
    }

    return scores
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  /**
   * BM25 搜索
   */
  bm25Search(query, topK = 10) {
    return this.bm25.search(query, topK);
  }

  /**
   * 混合搜索（RRF 融合）
   */
  async hybridSearch(query, topK = 10) {
    const vectorResults = await this.vectorSearch(query, topK * 2);
    const bm25Results = this.bm25Search(query, topK * 2);

    // RRF 融合
    const vectorIds = vectorResults.map(r => r.id);
    const bm25Ids = bm25Results.map(r => r.id);
    
    const fused = reciprocalRankFusion([vectorIds, bm25Ids], this.rrfK);

    // 合并详细信息
    const results = fused.slice(0, topK).map(item => {
      const doc = this.documents.get(item.id);
      const vectorResult = vectorResults.find(r => r.id === item.id);
      const bm25Result = bm25Results.find(r => r.id === item.id);

      return {
        id: item.id,
        score: item.score,
        vectorScore: vectorResult?.score || 0,
        bm25Score: bm25Result?.score || 0,
        content: doc?.content || '',
        metadata: doc?.metadata || {},
        citation: this.generateCitation(doc)
      };
    });

    return results;
  }

  /**
   * 加权融合搜索（简单版重排序）
   */
  async weightedSearch(query, topK = 10) {
    const vectorResults = await this.vectorSearch(query, topK * 2);
    const bm25Results = this.bm25Search(query, topK * 2);

    // 归一化分数
    const maxVectorScore = Math.max(...vectorResults.map(r => r.score), 0.001);
    const maxBm25Score = Math.max(...bm25Results.map(r => r.score), 0.001);

    const scores = new Map();

    for (const result of vectorResults) {
      const normalizedScore = result.score / maxVectorScore;
      scores.set(result.id, {
        id: result.id,
        vectorScore: normalizedScore,
        bm25Score: 0,
        content: result.content,
        metadata: result.metadata
      });
    }

    for (const result of bm25Results) {
      const normalizedScore = result.score / maxBm25Score;
      const existing = scores.get(result.id);
      if (existing) {
        existing.bm25Score = normalizedScore;
      } else {
        scores.set(result.id, {
          id: result.id,
          vectorScore: 0,
          bm25Score: normalizedScore,
          content: result.content,
          metadata: result.metadata
        });
      }
    }

    // 加权融合
    const results = Array.from(scores.values()).map(item => ({
      ...item,
      score: item.vectorScore * this.vectorWeight + item.bm25Score * this.bm25Weight,
      citation: this.generateCitation(this.documents.get(item.id))
    }));

    return results
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  /**
   * 生成引用
   */
  generateCitation(doc) {
    if (!doc) return null;
    
    const { metadata } = doc;
    return {
      source: metadata.source || metadata.filename || 'unknown',
      title: metadata.title || '',
      url: metadata.url || '',
      chunkIndex: metadata.chunkIndex ?? null,
      totalChunks: metadata.totalChunks ?? null,
      charStart: metadata.charStart ?? null,
      charEnd: metadata.charEnd ?? null
    };
  }

  /**
   * 搜索并返回带引用的结果
   */
  async searchWithCitations(query, topK = 5, method = 'hybrid') {
    let results;
    
    switch (method) {
      case 'vector':
        results = await this.vectorSearch(query, topK);
        break;
      case 'bm25':
        results = this.bm25Search(query, topK);
        break;
      case 'weighted':
        results = await this.weightedSearch(query, topK);
        break;
      case 'hybrid':
      default:
        results = await this.hybridSearch(query, topK);
    }

    // 添加引用编号
    return results.map((result, index) => ({
      ...result,
      reference: `[${index + 1}]`
    }));
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      totalDocuments: this.documents.size,
      totalEmbeddings: this.embeddings.size,
      bm25: this.bm25.getStats(),
      hasEmbeddingProvider: !!this.embeddingProvider
    };
  }

  /**
   * 清空索引
   */
  clear() {
    this.bm25.clear();
    this.documents.clear();
    this.embeddings.clear();
  }
}
