// RAG Retriever - 检索增强生成系统
// 基于 LanceDB 实现向量检索

import { connect } from '@lancedb/lancedb';
import { createHash } from 'crypto';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * 文档分块策略
 */
export class ChunkingStrategy {
  constructor(options = {}) {
    this.chunkSize = options.chunkSize || 500; // 每块字符数
    this.overlap = options.overlap || 50; // 重叠字符数
    this.separator = options.separator || '\n'; // 分隔符
  }

  /**
   * 将文本分块
   */
  chunk(text, metadata = {}) {
    const chunks = [];
    
    // 如果文本小于 chunkSize，直接返回
    if (text.length <= this.chunkSize) {
      chunks.push({
        id: this.generateId(text),
        content: text,
        metadata: {
          ...metadata,
          chunkIndex: 0,
          totalChunks: 1,
          charStart: 0,
          charEnd: text.length
        }
      });
      return chunks;
    }

    // 按分隔符分割
    let start = 0;
    let chunkIndex = 0;

    while (start < text.length) {
      let end = start + this.chunkSize;
      
      // 如果不是最后一块，在分隔符处切断
      if (end < text.length) {
        const separatorIndex = text.lastIndexOf(this.separator, end);
        if (separatorIndex > start) {
          end = separatorIndex + this.separator.length;
        }
      }

      const chunkContent = text.slice(start, end);
      
      chunks.push({
        id: this.generateId(chunkContent + chunkIndex),
        content: chunkContent.trim(),
        metadata: {
          ...metadata,
          chunkIndex,
          charStart: start,
          charEnd: end
        }
      });

      // 移动起始位置（减去重叠部分）
      start = end - this.overlap;
      if (start < 0) start = end;
      
      chunkIndex++;
    }

    // 更新总块数
    chunks.forEach(chunk => {
      chunk.metadata.totalChunks = chunks.length;
    });

    return chunks;
  }

  /**
   * 生成唯一 ID
   */
  generateId(content) {
    return createHash('sha256').update(content).digest('hex').slice(0, 16);
  }
}

/**
 * 简单文本嵌入（基于词频 + 长度归一化）
 * 生产环境应使用真正的嵌入模型（如 OpenAI embeddings, Cohere 等）
 */
export class SimpleTextEmbedding {
  constructor(dimensions = 384) {
    this.dimensions = dimensions;
    this.vocabulary = new Map();
    this.vocabSize = 0;
    this.jieba = null;
    
    // 尝试加载 @node-rs/jieba 用于中文分词
    import('@node-rs/jieba')
      .then(module => {
        this.jieba = new module.Jieba();
        console.log('[Embedding] ✅ @node-rs/jieba 分词库已加载');
      })
      .catch(err => {
        console.log('[Embedding] ⚠️ jieba 加载失败:', err.message);
      });
  }

  /**
   * 构建词汇表（异步）
   */
  async buildVocabulary(texts) {
    const wordFreq = new Map();
    
    for (const text of texts) {
      const words = await this.tokenize(text);
      for (const word of words) {
        wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
      }
    }

    // 选择最高频的词汇
    const sorted = Array.from(wordFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, this.dimensions);

    sorted.forEach(([word, _], index) => {
      this.vocabulary.set(word, index);
    });

    this.vocabSize = sorted.length;
    console.log(`[Embedding] 词汇表大小：${this.vocabSize}/${this.dimensions}`);
  }

  /**
   * 分词（支持中英文）
   */
  async tokenize(text) {
    // 检测是否包含中文
    const hasChinese = /[\u4e00-\u9fa5]/.test(text);
    
    if (hasChinese && this.jieba) {
      // 使用 @node-rs/jieba 中文分词
      const words = this.jieba.cut(text);
      return Array.from(words)
        .map(w => w.trim().toLowerCase())
        .filter(w => w.length > 0 && /[^\s]/.test(w));
    } else {
      // 英文分词
      return text
        .toLowerCase()
        .replace(/[^\w\s]/g, '')
        .split(/\s+/)
        .filter(w => w.length > 1);
    }
  }

  /**
   * 生成嵌入向量（异步）
   */
  async embed(text) {
    const vector = new Array(this.dimensions).fill(0);
    const words = await this.tokenize(text);
    
    // 词频统计
    const wordFreq = new Map();
    for (const word of words) {
      wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
    }

    // 生成向量
    wordFreq.forEach((freq, word) => {
      const index = this.vocabulary.get(word);
      if (index !== undefined) {
        vector[index] = freq;
      }
    });

    // 归一化
    const magnitude = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
    if (magnitude > 0) {
      return vector.map(v => v / magnitude);
    }
    
    return vector;
  }

  /**
   * 批量嵌入（异步）
   */
  async embedBatch(texts) {
    const results = [];
    for (const text of texts) {
      results.push(await this.embed(text));
    }
    return results;
  }

  /**
   * 保存词汇表
   */
  save(path) {
    const data = {
      dimensions: this.dimensions,
      vocabulary: Array.from(this.vocabulary.entries())
    };
    writeFileSync(path, JSON.stringify(data));
  }

  /**
   * 加载词汇表
   */
  load(path) {
    if (!existsSync(path)) {
      return false;
    }
    const data = JSON.parse(readFileSync(path, 'utf-8'));
    this.dimensions = data.dimensions;
    this.vocabulary = new Map(data.vocabulary);
    this.vocabSize = this.vocabulary.size;
    return true;
  }
}

/**
 * RAG 检索器主类
 */
export class RAGRetriever {
  constructor(options = {}) {
    this.dbPath = options.dbPath || join(__dirname, '../data/lancedb');
    this.embedding = new SimpleTextEmbedding(options.dimensions || 384);
    this.chunking = new ChunkingStrategy(options.chunking || {});
    this.db = null;
    this.collection = null;
    this.initialized = false;
  }

  /**
   * 初始化连接
   */
  async initialize(collectionName = 'documents') {
    console.log(`[RAG] 初始化 LanceDB: ${this.dbPath}`);
    
    this.db = await connect(this.dbPath);
    this.collectionName = collectionName;
    
    // 尝试加载现有词汇表
    const vocabPath = join(this.dbPath, 'vocabulary.json');
    if (this.embedding.load(vocabPath)) {
      console.log('[RAG] 词汇表已加载');
    }

    // 尝试打开集合
    try {
      this.collection = await this.db.openTable(collectionName);
      console.log(`[RAG] 打开集合：${collectionName}`);
    } catch (error) {
      this.collection = null;
      console.log(`[RAG] 集合不存在：${collectionName}`);
    }

    this.initialized = true;
    console.log('[RAG] ✅ 初始化完成');
  }

  /**
   * 获取或创建集合
   */
  async getCollection(name) {
    if (!this.initialized) {
      await this.initialize(name);
    }

    try {
      this.collection = await this.db.openTable(name);
      console.log(`[RAG] 打开集合：${name}`);
    } catch (error) {
      // 集合不存在，需要创建
      this.collection = null;
    }

    return this.collection;
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
    console.log(`[RAG] 文档分块：${chunks.length} 块`);

    // 如果没有词汇表，先构建
    if (this.embedding.vocabSize === 0) {
      console.log('[RAG] 构建词汇表...');
      await this.embedding.buildVocabulary(chunks.map(c => c.content));
      
      // 保存词汇表
      const vocabPath = join(this.dbPath, 'vocabulary.json');
      this.embedding.save(vocabPath);
    }

    // 生成嵌入
    const embeddings = await this.embedding.embedBatch(chunks.map(c => c.content));

    // 准备数据
    const data = chunks.map((chunk, index) => ({
      id: chunk.id,
      content: chunk.content,
      vector: embeddings[index],
      metadata: JSON.stringify(chunk.metadata)
    }));

    // 创建或添加到集合
    if (!this.collection) {
      this.collection = await this.db.createTable(this.collectionName, data);
      console.log(`[RAG] 创建集合：${this.collectionName}`);
    } else {
      await this.collection.add(data);
      console.log(`[RAG] 添加到集合：${data.length} 条`);
    }

    return {
      chunks: chunks.length,
      ids: chunks.map(c => c.id)
    };
  }

  /**
   * 添加多个文档
   */
  async addDocuments(documents) {
    const results = [];
    
    for (const doc of documents) {
      const result = await this.addDocument(doc.text, doc.metadata || {});
      results.push(result);
    }

    return results;
  }

  /**
   * 检索相关文档
   */
  async retrieve(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.collection) {
      throw new Error('集合不存在，请先添加文档');
    }

    const limit = options.limit || 5;
    
    // 生成查询嵌入
    const queryVector = await this.embedding.embed(query);
    console.log(`[RAG] 查询向量：${queryVector.length} 维，非零：${queryVector.filter(v => v !== 0).length}`);

    // 执行向量搜索（LanceDB API）
    try {
      const searchResults = await this.collection
        .search(queryVector)
        .limit(limit)
        .execute();

      console.log(`[RAG] 搜索结果类型：${typeof searchResults}`, searchResults?.constructor?.name);

      // 解析结果（处理 RecordBatchIterator 格式）
      const results = [];
      
      if (searchResults && searchResults.constructor?.name === 'RecordBatchIterator') {
        // LanceDB RecordBatchIterator - 需要迭代读取
        console.log('[RAG] 处理 RecordBatchIterator...');
        
        let batch;
        while ((batch = await searchResults.next()) && !batch.done) {
          const value = batch.value;
          if (value && typeof value.toArray === 'function') {
            const array = value.toArray();
            console.log(`[RAG] 批次大小：${array?.length || 0}`);
            if (array && array.length > 0) {
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
        }
      } else if (searchResults && typeof searchResults.toArray === 'function') {
        // Arrow Table 格式
        const array = searchResults.toArray();
        console.log(`[RAG] Arrow 数组长度：${array.length}`);
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
          score: row._distance || 0
        }));
      }

      console.log(`[RAG] 最终结果数：${results.length}`);
      return results;
    } catch (error) {
      console.error('[RAG] 搜索失败:', error.message);
      throw error;
    }
  }

  /**
   * 检索并格式化（用于 RAG）
   */
  async retrieveForRAG(query, options = {}) {
    const results = await this.retrieve(query, options);
    
    // 格式化上下文
    const context = results
      .map((r, i) => `[${i + 1}] ${r.content}`)
      .join('\n\n');

    return {
      query,
      context,
      results,
      resultCount: results.length
    };
  }

  /**
   * 查询统计
   */
  async getStats() {
    if (!this.collection) {
      return {
        collection: this.collectionName,
        documentCount: 0
      };
    }

    // LanceDB 统计
    const count = await this.collection.countRows();
    
    return {
      collection: this.collectionName,
      documentCount: count,
      vocabularySize: this.embedding.vocabSize,
      dimensions: this.embedding.dimensions
    };
  }

  /**
   * 删除集合
   */
  async dropCollection(name) {
    await this.db.dropTable(name);
    console.log(`[RAG] 删除集合：${name}`);
  }

  /**
   * 列出所有集合
   */
  async listCollections() {
    return await this.db.tableNames();
  }

  /**
   * 关闭连接
   */
  async close() {
    if (this.db) {
      await this.db.close();
      console.log('[RAG] 连接已关闭');
    }
  }
}

// 导出默认实例
export const ragRetriever = new RAGRetriever();
