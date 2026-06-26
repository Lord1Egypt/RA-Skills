// RAG 2.0 - BM25 关键词搜索模块
// 基于 Okapi BM25 算法

/**
 * BM25 搜索引擎
 */
export class BM25Search {
  constructor(options = {}) {
    this.k1 = options.k1 || 1.5;  // 词频饱和参数
    this.b = options.b || 0.75;   // 长度归一化参数
    this.index = new Map();       // 倒排索引: term -> [{docId, freq}]
    this.docs = new Map();        // 文档存储: docId -> {content, metadata}
    this.docLengths = new Map();  // 文档长度
    this.avgDocLength = 0;
    this.totalDocs = 0;
  }

  /**
   * 中文分词（简单实现）
   */
  tokenize(text) {
    // 简单的中文字符级分词 + 英文词级分词
    const tokens = [];
    const chineseChars = text.match(/[\u4e00-\u9fff]/g) || [];
    const englishWords = text.toLowerCase()
      .replace(/[\u4e00-\u9fff]/g, ' ')
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 1);

    tokens.push(...chineseChars);
    tokens.push(...englishWords);
    
    return tokens;
  }

  /**
   * 添加文档到索引
   */
  addDocument(docId, content, metadata = {}) {
    const tokens = this.tokenize(content);
    const termFreq = new Map();

    // 统计词频
    for (const token of tokens) {
      termFreq.set(token, (termFreq.get(token) || 0) + 1);
    }

    // 存储文档
    this.docs.set(docId, { content, metadata });
    this.docLengths.set(docId, tokens.length);

    // 更新倒排索引
    for (const [term, freq] of termFreq) {
      if (!this.index.has(term)) {
        this.index.set(term, []);
      }
      this.index.get(term).push({ docId, freq });
    }

    // 更新统计
    this.totalDocs++;
    this.updateAvgDocLength();
  }

  /**
   * 批量添加文档
   */
  addDocuments(documents) {
    for (const doc of documents) {
      this.addDocument(doc.id, doc.content, doc.metadata);
    }
  }

  updateAvgDocLength() {
    let totalLength = 0;
    for (const length of this.docLengths.values()) {
      totalLength += length;
    }
    this.avgDocLength = totalLength / this.totalDocs || 1;
  }

  /**
   * 计算 IDF（逆文档频率）
   */
  idf(term) {
    const docsWithTerm = this.index.get(term)?.length || 0;
    if (docsWithTerm === 0) return 0;
    return Math.log((this.totalDocs - docsWithTerm + 0.5) / (docsWithTerm + 0.5) + 1);
  }

  /**
   * 搜索文档
   */
  search(query, topK = 10) {
    const queryTokens = this.tokenize(query);
    const scores = new Map();

    for (const term of queryTokens) {
      const postings = this.index.get(term);
      if (!postings) continue;

      const termIdf = this.idf(term);

      for (const { docId, freq } of postings) {
        const docLength = this.docLengths.get(docId);
        const tf = (freq * (this.k1 + 1)) / 
                   (freq + this.k1 * (1 - this.b + this.b * (docLength / this.avgDocLength)));
        
        const score = tf * termIdf;
        scores.set(docId, (scores.get(docId) || 0) + score);
      }
    }

    // 排序并返回 topK
    const results = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, topK)
      .map(([docId, score]) => ({
        id: docId,
        score,
        content: this.docs.get(docId).content,
        metadata: this.docs.get(docId).metadata
      }));

    return results;
  }

  /**
   * 清空索引
   */
  clear() {
    this.index.clear();
    this.docs.clear();
    this.docLengths.clear();
    this.totalDocs = 0;
    this.avgDocLength = 0;
  }

  /**
   * 获取索引统计
   */
  getStats() {
    return {
      totalDocs: this.totalDocs,
      totalTerms: this.index.size,
      avgDocLength: this.avgDocLength
    };
  }
}
