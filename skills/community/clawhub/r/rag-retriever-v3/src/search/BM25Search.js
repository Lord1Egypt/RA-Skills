/**
 * BM25 关键词搜索实现
 * 支持中英文混合搜索，使用 jieba 进行中文分词
 */

import { createRequire } from 'module';

export class BM25Search {
  constructor(options = {}) {
    this.k1 = options.k1 || 1.5;  // BM25 参数 k1
    this.b = options.b || 0.75;   // BM25 参数 b
    this.documents = [];          // 文档列表
    this.tokenizedDocs = [];      // 分词后的文档
    this.docFreqs = new Map();    // 文档频率
    this.docLengths = [];         // 文档长度
    this.avgDocLength = 0;        // 平均文档长度
    this.totalDocs = 0;           // 文档总数
    this.jieba = null;            // 中文分词器
    this.stopWords = new Set();   // 停用词
    
    // 初始化停用词
    this.initStopWords();
    
    // 延迟加载 jieba
    this.initJieba();
  }

  /**
   * 初始化停用词
   */
  initStopWords() {
    // 中英文停用词
    const stopWordsList = [
      '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也',
      '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
      'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
      'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'and', 'or', 'but'
    ];
    stopWordsList.forEach(word => this.stopWords.add(word));
  }

  /**
   * 初始化 jieba 分词器
   */
  async initJieba() {
    try {
      // 动态导入 @node-rs/jieba
      const jiebaModule = await import('@node-rs/jieba');
      this.jieba = new jiebaModule.Jieba();
      console.log('[BM25Search] ✅ jieba 分词器已加载');
    } catch (error) {
      console.warn('[BM25Search] ⚠️ jieba 加载失败，将使用简单分词:', error.message);
      this.jieba = null;
    }
  }

  /**
   * 分词（支持中英文）
   */
  async tokenize(text) {
    if (!text || typeof text !== 'string') {
      return [];
    }

    // 确保 jieba 已加载
    if (!this.jieba) {
      await this.initJieba();
    }

    const hasChinese = /[\u4e00-\u9fa5]/.test(text);
    let tokens = [];

    if (hasChinese && this.jieba) {
      // 使用 jieba 进行中文分词
      try {
        const cutResult = this.jieba.cut(text);
        tokens = Array.from(cutResult)
          .map(w => w.trim().toLowerCase())
          .filter(w => w.length > 0 && !this.stopWords.has(w));
      } catch (error) {
        // 降级到简单分词
        tokens = this.simpleTokenize(text);
      }
    } else {
      // 英文分词
      tokens = this.simpleTokenize(text);
    }

    return tokens;
  }

  /**
   * 简单分词（降级方案）
   */
  simpleTokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 1 && !this.stopWords.has(w));
  }

  /**
   * 添加文档到索引
   */
  async addDocument(doc) {
    const { id, content, metadata = {} } = doc;
    
    if (!content) {
      console.warn('[BM25Search] 跳过空文档:', id);
      return;
    }

    // 分词
    const tokens = await this.tokenize(content);
    
    // 统计词频
    const termFreqs = new Map();
    for (const token of tokens) {
      termFreqs.set(token, (termFreqs.get(token) || 0) + 1);
    }

    // 更新文档频率
    for (const term of termFreqs.keys()) {
      this.docFreqs.set(term, (this.docFreqs.get(term) || 0) + 1);
    }

    // 存储文档
    this.documents.push({ id, content, metadata });
    this.tokenizedDocs.push({
      id,
      tokens,
      termFreqs,
      length: tokens.length
    });
    this.docLengths.push(tokens.length);
    this.totalDocs++;

    // 更新平均文档长度
    this.avgDocLength = this.docLengths.reduce((a, b) => a + b, 0) / this.totalDocs;
  }

  /**
   * 批量添加文档
   */
  async addDocuments(docs) {
    for (const doc of docs) {
      await this.addDocument(doc);
    }
    console.log(`[BM25Search] 已索引 ${this.totalDocs} 个文档`);
  }

  /**
   * 计算 BM25 分数
   */
  calculateBM25Score(term, docIndex) {
    const doc = this.tokenizedDocs[docIndex];
    const termFreq = doc.termFreqs.get(term) || 0;
    
    if (termFreq === 0) return 0;

    // 文档频率
    const df = this.docFreqs.get(term) || 0;
    
    // IDF 计算
    const idf = Math.log((this.totalDocs - df + 0.5) / (df + 0.5) + 1);
    
    // 词频归一化
    const docLength = this.docLengths[docIndex];
    const normalizedTf = termFreq / (termFreq + this.k1 * (1 - this.b + this.b * docLength / this.avgDocLength));
    
    return idf * normalizedTf;
  }

  /**
   * 搜索文档
   */
  async search(query, options = {}) {
    const limit = options.limit || 10;
    
    if (this.totalDocs === 0) {
      return [];
    }

    // 对查询进行分词
    const queryTokens = await this.tokenize(query);
    
    if (queryTokens.length === 0) {
      return [];
    }

    // 计算每个文档的 BM25 分数
    const scores = [];
    
    for (let i = 0; i < this.totalDocs; i++) {
      let score = 0;
      
      for (const term of queryTokens) {
        score += this.calculateBM25Score(term, i);
      }
      
      if (score > 0) {
        scores.push({
          index: i,
          score,
          document: this.documents[i]
        });
      }
    }

    // 按分数排序
    scores.sort((a, b) => b.score - a.score);

    // 返回结果
    return scores.slice(0, limit).map((item, rank) => ({
      id: item.document.id,
      content: item.document.content,
      metadata: item.document.metadata,
      score: item.score,
      rank: rank + 1
    }));
  }

  /**
   * 获取索引统计信息
   */
  getStats() {
    return {
      totalDocs: this.totalDocs,
      avgDocLength: this.avgDocLength,
      vocabularySize: this.docFreqs.size,
      parameters: {
        k1: this.k1,
        b: this.b
      }
    };
  }

  /**
   * 清空索引
   */
  clear() {
    this.documents = [];
    this.tokenizedDocs = [];
    this.docFreqs.clear();
    this.docLengths = [];
    this.avgDocLength = 0;
    this.totalDocs = 0;
  }
}

export default BM25Search;
