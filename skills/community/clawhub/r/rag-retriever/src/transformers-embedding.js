// RAG 2.0 - Transformers.js 本地嵌入提供者
// 使用 all-MiniLM-L6-v2 模型，无需 API key

/**
 * Transformers.js 嵌入提供者
 * 基于 Hugging Face Transformers.js，本地运行，无需 API
 */
export class TransformersEmbedding {
  constructor(options = {}) {
    this.modelId = options.modelId || 'Xenova/all-MiniLM-L6-v2';
    this.dimensions = options.dimensions || 384;
    this.cachePath = options.cachePath || './data/transformers-cache';
    this.pipeline = null;
    this.initialized = false;
  }

  /**
   * 初始化模型（懒加载）
   */
  async init() {
    if (this.initialized) return;

    try {
      const { pipeline, env } = await import('@huggingface/transformers');
      
      // 配置 HuggingFace 镜像（国内访问）
      env.HF_HUB_BASE_URL = 'https://hf-mirror.com';
      env.HF_ENDPOINT = 'https://hf-mirror.com';
      
      this.pipeline = await pipeline('feature-extraction', this.modelId, {
        cache_dir: this.cachePath,
        quantized: true  // 使用量化模型，更快更小
      });

      this.initialized = true;
      console.log(`[TransformersEmbedding] 模型 ${this.modelId} 加载完成`);
    } catch (err) {
      console.error(`[TransformersEmbedding] 模型加载失败:`, err.message);
      throw err;
    }
  }

  /**
   * 生成单个文本的嵌入向量
   */
  async embed(text) {
    await this.init();

    const output = await this.pipeline(text, {
      pooling: 'mean',
      normalize: true
    });

    // 转换为普通数组
    return Array.from(output.data);
  }

  /**
   * 批量生成嵌入向量
   */
  async embedBatch(texts, batchSize = 32) {
    await this.init();

    const results = [];

    for (let i = 0; i < texts.length; i += batchSize) {
      const batch = texts.slice(i, i + batchSize);
      
      const output = await this.pipeline(batch, {
        pooling: 'mean',
        normalize: true
      });

      // 处理批量输出
      if (batch.length === 1) {
        results.push(Array.from(output.data));
      } else {
        // 批量输出是 3D 张量 [batch, tokens, dims]
        const batchData = output.tolist();
        results.push(...batchData);
      }
    }

    return results;
  }

  /**
   * 计算两个向量的余弦相似度
   */
  similarity(vecA, vecB) {
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
   * 获取模型信息
   */
  getInfo() {
    return {
      modelId: this.modelId,
      dimensions: this.dimensions,
      initialized: this.initialized,
      type: 'transformers.js'
    };
  }
}

/**
 * Cross-Encoder 重排序提供者
 */
export class CrossEncoderReranker {
  constructor(options = {}) {
    this.modelId = options.modelId || 'Xenova/ms-marco-MiniLM-L-6-v2';
    this.cachePath = options.cachePath || './data/transformers-cache';
    this.pipeline = null;
    this.initialized = false;
  }

  async init() {
    if (this.initialized) return;

    try {
      const { pipeline, env } = await import('@huggingface/transformers');
      
      // 配置 HuggingFace 镜像（国内访问）
      env.HF_HUB_BASE_URL = 'https://hf-mirror.com';
      env.HF_ENDPOINT = 'https://hf-mirror.com';
      
      this.pipeline = await pipeline('text-classification', this.modelId, {
        cache_dir: this.cachePath,
        quantized: true
      });

      this.initialized = true;
      console.log(`[CrossEncoderReranker] 模型 ${this.modelId} 加载完成`);
    } catch (err) {
      console.error(`[CrossEncoderReranker] 模型加载失败:`, err.message);
      throw err;
    }
  }

  /**
   * 重排序文档
   * @param {string} query - 查询文本
   * @param {Array} documents - 文档列表 [{id, content, metadata}]
   * @param {number} topK - 返回 topK 结果
   */
  async rerank(query, documents, topK = 10) {
    await this.init();

    const pairs = documents.map(doc => ({
      text: `${query} [SEP] ${doc.content}`,
      doc
    }));

    const scores = [];

    for (const pair of pairs) {
      try {
        const output = await this.pipeline(pair.text);
        scores.push({
          doc: pair.doc,
          score: output[0].score
        });
      } catch (err) {
        // 如果单个处理失败，给一个默认分数
        scores.push({
          doc: pair.doc,
          score: 0
        });
      }
    }

    // 排序并返回 topK
    return scores
      .sort((a, b) => b.score - a.score)
      .slice(0, topK)
      .map((item, idx) => ({
        ...item.doc,
        rerankScore: item.score,
        rerankRank: idx + 1
      }));
  }

  getInfo() {
    return {
      modelId: this.modelId,
      initialized: this.initialized,
      type: 'cross-encoder'
    };
  }
}

export default TransformersEmbedding;
