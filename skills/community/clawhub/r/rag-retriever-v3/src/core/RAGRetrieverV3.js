/**
 * RAG 3.0 检索器主类
 * 集成语义嵌入、混合检索、重排序和来源引用
 */

import { connect } from '@lancedb/lancedb';
import { createHash } from 'crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import { createEmbeddingProvider } from '../embeddings/index.js';
import { BM25Search } from '../search/BM25Search.js';
import { RRFFusion } from '../search/RRFFusion.js';
import { CrossEncoderReranker } from '../rerank/CrossEncoderReranker.js';
import { ChunkingStrategy } from './ChunkingStrategy.js';
import { CitationManager } from './CitationManager.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export class RAGRetrieverV3 {
  constructor(options = {}) {
    // 基础配置
    this.dbPath = options.dbPath || join(process.cwd(), 'data', 'lancedb-v3');
    this.collectionName = options.collectionName || 'documents';
    
    // 嵌入配置
    this.embeddingProvider = options.embeddingProvider || 'auto';
    this.embeddingOptions = options.embeddingOptions || {};
    this.embedding = null;
    
    // 分块配置
    this.chunkingOptions = options.chunking || {
      chunkSize: 500,
      overlap: 50,
      strategy: 'recursive'
    };
    this.chunking = new ChunkingStrategy(this.chunkingOptions);
    
    // BM25 配置
    this.bm25Options = options.bm25 || {
      k1: 1.5,
      b: 0.75
    };
    this.bm25 = new BM25Search(this.bm25Options);
    
    // RRF 配置
    this.rrfOptions = options.rrf || {
      k: 60,
      weights: { 0: 1.0, 1: 1.0 }  // 向量搜索和关键词搜索的权重
    };
    this.rrf = new RRFFusion(this.rrfOptions);
    
    // 重排序配置
    this.rerankOptions = options.rerank || {
      enabled: true,
      model: 'Xenova/ms-marco-MiniLM-L-6-v2',
      topK: 20  // 重排序前 K 个结果
    };
    this.reranker = null;
    
    // 引用配置
    this.citationOptions = options.citation || {
      format: 'numbered',
      includeMetadata: true
    };
    this.citationManager = new CitationManager(this.citationOptions);
    
    // 状态
    this.db = null;
    this.collection = null;
    this.initialized = false;
    this.documentCount = 0;
  }

  /**
   * 初始化检索器
   */
  async initialize() {
    if (this.initialized) return;

    console.log('[RAG V3] 初始化 RAG 3.0 检索器...');

    // 确保数据目录存在
    if (!existsSync(dirname(this.dbPath))) {
      mkdirSync(dirname(this.dbPath), { recursive: true });
    }

    // 初始化嵌入模型
    console.log(`[RAG V3] 初始化嵌入模型: ${this.embeddingProvider}`);
    this.embedding = createEmbeddingProvider(this.embeddingProvider, this.embeddingOptions);
    await this.embedding.initialize();
    console.log('[RAG V3] ✅ 嵌入模型初始化完成');

    // 初始化重排序器
    if (this.rerankOptions.enabled) {
      console.log('[RAG V3] 初始化重排序器...');
      this.reranker = new CrossEncoderReranker({
        modelName: this.rerankOptions.model
      });
    }

    // 连接 LanceDB
    console.log(`[RAG V3] 连接 LanceDB: ${this.dbPath}`);
    this.db = await connect(this.dbPath);

    // 尝试打开集合
    try {
      this.collection = await this.db.openTable(this.collectionName);
      this.documentCount = await this.collection.countRows();
      console.log(`[RAG V3] 打开集合: ${this.collectionName} (${this.documentCount} 文档)`);
    } catch (error) {
      this.collection = null;
      console.log(`[RAG V3] 集合不存在: ${this.collectionName}，需要创建`);
    }

    this.initialized = true;
    console.log('[RAG V3] ✅ 初始化完成');
  }

  /**
   * 添加文档
   */
  async addDocument(text, metadata = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    // 分块
    const chunks = this.chunking.chunk(text, metadata);
    console.log(`[RAG V3] 文档分块: ${chunks.length} 块`);

    // 生成嵌入
    const embeddings = await this.embedding.embedBatch(chunks.map(c => c.content));

    // 准备数据
    const data = chunks.map((chunk, index) => ({
      id: chunk.id,
      content: chunk.content,
      vector: embeddings[index],
      metadata: JSON.stringify(chunk.metadata)
    }));

    // 添加到 BM25 索引
    await this.bm25.addDocuments(chunks.map(c => ({
      id: c.id,
      content: c.content,
      metadata: c.metadata
    })));

    // 创建或添加到集合
    if (!this.collection) {
      this.collection = await this.db.createTable(this.collectionName, data);
      console.log(`[RAG V3] 创建集合并添加: ${data.length} 条`);
    } else {
      await this.collection.add(data);
      console.log(`[RAG V3] 添加到集合: ${data.length} 条`);
    }

    this.documentCount += chunks.length;

    return {
      chunks: chunks.length,
      ids: chunks.map(c => c.id),
      stats: this.chunking.getStats(chunks)
    };
  }

  /**
   * 向量搜索
   */
  async vectorSearch(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.collection) {
      throw new Error('集合不存在，请先添加文档');
    }

    const limit = options.limit || 20;

    // 生成查询嵌入
    const queryVector = await this.embedding.embed(query);

    // 执行向量搜索
    const searchResults = await this.collection
      .search(queryVector)
      .limit(limit)
      .execute();

    // 解析结果
    const results = await this.parseSearchResults(searchResults);
    
    // 添加排名
    return results.map((r, i) => ({ ...r, rank: i + 1, searchType: 'vector' }));
  }

  /**
   * 关键词搜索（BM25）
   */
  async keywordSearch(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    const limit = options.limit || 20;

    // 执行 BM25 搜索
    const results = await this.bm25.search(query, { limit });
    
    // 添加搜索类型
    return results.map(r => ({ ...r, searchType: 'keyword' }));
  }

  /**
   * 混合搜索（向量 + 关键词 + RRF 融合）
   */
  async hybridSearch(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    const vectorLimit = options.vectorLimit || 20;
    const keywordLimit = options.keywordLimit || 20;
    const fusionLimit = options.limit || 10;

    console.log(`[RAG V3] 执行混合搜索: "${query}"`);

    // 并行执行两种搜索
    const [vectorResults, keywordResults] = await Promise.all([
      this.vectorSearch(query, { limit: vectorLimit }),
      this.keywordSearch(query, { limit: keywordLimit })
    ]);

    console.log(`[RAG V3] 向量搜索: ${vectorResults.length} 条, 关键词搜索: ${keywordResults.length} 条`);

    // RRF 融合
    const fusedResults = this.rrf.fuseTwo(vectorResults, keywordResults, { limit: fusionLimit });

    console.log(`[RAG V3] 融合后: ${fusedResults.length} 条`);

    return fusedResults;
  }

  /**
   * 重排序
   */
  async rerank(query, results, options = {}) {
    if (!this.reranker || !this.rerankOptions.enabled) {
      return results;
    }

    const limit = options.limit || this.rerankOptions.topK || results.length;

    console.log(`[RAG V3] 执行重排序: ${results.length} 条`);

    // 重排序
    const rerankedResults = await this.reranker.rerank(query, results, { limit });

    console.log(`[RAG V3] 重排序完成: ${rerankedResults.length} 条`);

    return rerankedResults;
  }

  /**
   * 完整检索流程（混合搜索 + 重排序 + 引用）
   */
  async retrieve(query, options = {}) {
    const {
      limit = 5,
      rerank = true,
      addCitations = true,
      hybrid = true
    } = options;

    // 步骤 1: 搜索
    let results;
    if (hybrid) {
      results = await this.hybridSearch(query, { limit: limit * 3 });
    } else {
      results = await this.vectorSearch(query, { limit: limit * 3 });
    }

    // 步骤 2: 重排序
    if (rerank && this.rerankOptions.enabled && results.length > 0) {
      results = await this.rerank(query, results, { limit: limit * 2 });
    }

    // 步骤 3: 截取前 N 个
    results = results.slice(0, limit);

    // 步骤 4: 添加引用
    if (addCitations) {
      results = this.citationManager.addCitations(results);
    }

    return results;
  }

  /**
   * RAG 查询（生成带引用的上下文）
   */
  async retrieveForRAG(query, options = {}) {
    const results = await this.retrieve(query, { ...options, addCitations: true });
    
    // 生成 RAG 提示词
    const ragResult = this.citationManager.generateRAGPrompt(query, results, options);

    return {
      query,
      results,
      ...ragResult
    };
  }

  /**
   * 解析 LanceDB 搜索结果
   */
  async parseSearchResults(searchResults) {
    const results = [];

    if (searchResults && searchResults.constructor?.name === 'RecordBatchIterator') {
      // LanceDB RecordBatchIterator
      let batch;
      while ((batch = await searchResults.next()) && !batch.done) {
        const value = batch.value;
        if (value && typeof value.toArray === 'function') {
          const array = value.toArray();
          for (let i = 0; i < array.length; i++) {
            results.push({
              id: array[i].id,
              content: array[i].content,
              metadata: JSON.parse(array[i].metadata),
              score: array[i]._distance || 0
            });
          }
        }
      }
    } else if (searchResults && typeof searchResults.toArray === 'function') {
      // Arrow Table 格式
      const array = searchResults.toArray();
      for (let i = 0; i < array.length; i++) {
        results.push({
          id: array[i].id,
          content: array[i].content,
          metadata: JSON.parse(array[i].metadata),
          score: array[i]._distance || 0
        });
      }
    } else if (Array.isArray(searchResults)) {
      // 数组格式
      return searchResults.map(row => ({
        id: row.id,
        content: row.content,
        metadata: JSON.parse(row.metadata),
        score: row._distance || row.score || 0
      }));
    }

    return results;
  }

  /**
   * 获取统计信息
   */
  async getStats() {
    const embeddingInfo = this.embedding ? this.embedding.getInfo() : null;
    const bm25Stats = this.bm25.getStats();

    return {
      collection: this.collectionName,
      documentCount: this.documentCount,
      initialized: this.initialized,
      embedding: embeddingInfo,
      bm25: bm25Stats,
      rerank: this.reranker ? this.reranker.getInfo() : null
    };
  }

  /**
   * 列出所有集合
   */
  async listCollections() {
    if (!this.db) {
      await this.initialize();
    }
    return await this.db.tableNames();
  }

  /**
   * 删除集合
   */
  async dropCollection(name) {
    if (!this.db) {
      await this.initialize();
    }
    await this.db.dropTable(name);
    console.log(`[RAG V3] 删除集合: ${name}`);
  }

  /**
   * 关闭连接
   */
  async close() {
    if (this.db) {
      await this.db.close();
      console.log('[RAG V3] 连接已关闭');
    }
    this.initialized = false;
  }
}

export default RAGRetrieverV3;