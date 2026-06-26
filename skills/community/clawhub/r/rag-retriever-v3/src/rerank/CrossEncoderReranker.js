/**
 * Cross-Encoder 重排序器
 * 使用 @xenova/transformers 在本地运行 Cross-Encoder 模型
 * 对检索结果进行精确重排序
 */

import { pipeline, env } from '@xenova/transformers';

// 配置 transformers.js
env.allowLocalModels = true;
env.allowRemoteModels = true;

export class CrossEncoderReranker {
  constructor(options = {}) {
    this.modelName = options.modelName || 'Xenova/ms-marco-MiniLM-L-6-v2';
    this.name = 'cross-encoder';
    this.pipeline = null;
    this.initialized = false;
    this.batchSize = options.batchSize || 16;
    this.maxLength = options.maxLength || 512;
    
    // 支持的模型列表
    this.supportedModels = [
      { name: 'Xenova/ms-marco-MiniLM-L-6-v2', description: 'MS MARCO MiniLM，适合重排序' },
      { name: 'Xenova/ms-marco-MiniLM-L-12-v2', description: 'MS MARCO MiniLM 大版本' },
      { name: 'Xenova/ms-marco-MiniLM-L-4-v2', description: 'MS MARCO MiniLM 小版本' },
      { name: 'Xenova/ms-marco-TinyBERT-L-2-v2', description: 'MS MARCO TinyBERT，更快' },
      { name: 'Xenova/cross-encoder-ms-marco-MiniLM-L-6-v2', description: 'Cross-Encoder MS MARCO' }
    ];
  }

  /**
   * 初始化 Cross-Encoder 模型
   */
  async initialize() {
    if (this.initialized) return;

    console.log(`[CrossEncoderReranker] 加载模型: ${this.modelName}`);
    
    try {
      // 创建文本分类管道（Cross-Encoder 使用分类方式）
      this.pipeline = await pipeline(
        'text-classification',
        this.modelName,
        {
          revision: 'main',
          progress_callback: (progress) => {
            if (progress.status === 'progress') {
              const percent = ((progress.loaded / progress.total) * 100).toFixed(1);
              process.stdout.write(`\r[CrossEncoderReranker] 加载进度: ${percent}%`);
            }
          }
        }
      );
      
      console.log('\n[CrossEncoderReranker] ✅ 模型加载完成');
      this.initialized = true;
    } catch (error) {
      console.error('[CrossEncoderReranker] ❌ 模型加载失败:', error.message);
      throw error;
    }
  }

  /**
   * 计算查询和文档的相关性分数
   * @param {string} query - 查询文本
   * @param {string} document - 文档文本
   * @returns {Promise<number>} - 相关性分数
   */
  async score(query, document) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!query || !document) {
      return 0;
    }

    try {
      // 截断文档
      const truncatedDoc = document.length > this.maxLength * 3 
        ? document.slice(0, this.maxLength * 3) + '...'
        : document;

      // Cross-Encoder 输入格式：[query, document]
      const result = await this.pipeline(
        [[query, truncatedDoc]],
        { 
          truncation: true,
          max_length: this.maxLength
        }
      );

      // 提取分数
      // MS MARCO 模型输出的是相关性分数
      const score = result[0]?.score || 0;
      
      // 有些模型输出的是标签，需要转换
      if (result[0]?.label !== undefined) {
        // 如果是标签形式，根据标签返回分数
        const label = result[0].label;
        if (typeof label === 'string') {
          // 标签可能是 'LABEL_0', 'LABEL_1' 等
          const labelNum = parseInt(label.replace('LABEL_', ''));
          return isNaN(labelNum) ? score : labelNum;
        }
        return label;
      }

      return score;
    } catch (error) {
      console.error('[CrossEncoderReranker] 评分失败:', error.message);
      return 0;
    }
  }

  /**
   * 批量评分
   * @param {string} query - 查询文本
   * @param {Array} documents - 文档列表，每个文档包含 content 或 text
   * @returns {Promise<Array>} - 带分数的文档列表
   */
  async scoreBatch(query, documents) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!query || !documents || documents.length === 0) {
      return [];
    }

    const results = [];
    
    // 分批处理
    for (let i = 0; i < documents.length; i += this.batchSize) {
      const batch = documents.slice(i, i + this.batchSize);
      
      // 准备输入
      const inputs = batch.map(doc => {
        const content = doc.content || doc.text || doc.document || '';
        const truncated = content.length > this.maxLength * 3 
          ? content.slice(0, this.maxLength * 3) + '...'
          : content;
        return [query, truncated];
      });

      try {
        const batchResults = await this.pipeline(inputs, {
          truncation: true,
          max_length: this.maxLength
        });

        // 处理结果
        batch.forEach((doc, index) => {
          const result = batchResults[index];
          let score = 0;
          
          if (result) {
            if (result.score !== undefined) {
              score = result.score;
            } else if (result.label !== undefined) {
              const label = result.label;
              if (typeof label === 'string') {
                const labelNum = parseInt(label.replace('LABEL_', ''));
                score = isNaN(labelNum) ? 0 : labelNum;
              } else {
                score = label;
              }
            }
          }

          results.push({
            ...doc,
            rerankScore: score,
            originalScore: doc.score || doc.rrfScore || 0
          });
        });

        if (i + this.batchSize < documents.length) {
          process.stdout.write(`\r[CrossEncoderReranker] 处理进度: ${Math.min(i + this.batchSize, documents.length)}/${documents.length}`);
        }
      } catch (error) {
        console.error('[CrossEncoderReranker] 批量评分失败:', error.message);
        // 为失败的批次添加默认分数
        batch.forEach(doc => {
          results.push({
            ...doc,
            rerankScore: 0,
            originalScore: doc.score || doc.rrfScore || 0
          });
        });
      }
    }

    console.log(`\r[CrossEncoderReranker] 完成: ${documents.length} 个文档的重排序`);
    return results;
  }

  /**
   * 重排序检索结果
   * @param {string} query - 查询文本
   * @param {Array} results - 检索结果列表
   * @param {Object} options - 配置选项
   * @returns {Promise<Array>} - 重排序后的结果
   */
  async rerank(query, results, options = {}) {
    const limit = options.limit || results.length;
    
    if (!results || results.length === 0) {
      return [];
    }

    // 获取分数
    const scoredResults = await this.scoreBatch(query, results);

    // 按重排序分数排序
    scoredResults.sort((a, b) => b.rerankScore - a.rerankScore);

    // 添加排名信息
    return scoredResults.slice(0, limit).map((item, index) => ({
      ...item,
      rerankRank: index + 1,
      finalScore: item.rerankScore
    }));
  }

  /**
   * 组合重排序（融合分数 + Cross-Encoder）
   * @param {string} query - 查询文本
   * @param {Array} results - 融合后的检索结果
   * @param {Object} options - 配置选项
   * @returns {Promise<Array>} - 最终排序结果
   */
  async rerankHybrid(query, results, options = {}) {
    const limit = options.limit || results.length;
    const rrfWeight = options.rrfWeight || 0.3;  // RRF 分数权重
    const ceWeight = options.ceWeight || 0.7;    // Cross-Encoder 分数权重

    if (!results || results.length === 0) {
      return [];
    }

    // 获取 Cross-Encoder 分数
    const scoredResults = await this.scoreBatch(query, results);

    // 归一化分数并组合
    const maxRRF = Math.max(...scoredResults.map(r => r.rrfScore || 0), 1);
    const maxCE = Math.max(...scoredResults.map(r => r.rerankScore || 0), 1);

    const combinedResults = scoredResults.map(item => {
      const normalizedRRF = (item.rrfScore || 0) / maxRRF;
      const normalizedCE = (item.rerankScore || 0) / maxCE;
      const combinedScore = normalizedRRF * rrfWeight + normalizedCE * ceWeight;

      return {
        ...item,
        normalizedRRF,
        normalizedCE,
        combinedScore,
        finalScore: combinedScore
      };
    });

    // 按组合分数排序
    combinedResults.sort((a, b) => b.combinedScore - a.combinedScore);

    // 添加排名信息
    return combinedResults.slice(0, limit).map((item, index) => ({
      ...item,
      finalRank: index + 1
    }));
  }

  /**
   * 获取支持的模型列表
   */
  static getSupportedModels() {
    return [
      { name: 'Xenova/ms-marco-MiniLM-L-6-v2', description: 'MS MARCO MiniLM，适合重排序' },
      { name: 'Xenova/ms-marco-MiniLM-L-12-v2', description: 'MS MARCO MiniLM 大版本' },
      { name: 'Xenova/ms-marco-MiniLM-L-4-v2', description: 'MS MARCO MiniLM 小版本' },
      { name: 'Xenova/ms-marco-TinyBERT-L-2-v2', description: 'MS MARCO TinyBERT，更快' }
    ];
  }

  getInfo() {
    return {
      name: this.name,
      modelName: this.modelName,
      initialized: this.initialized,
      batchSize: this.batchSize,
      maxLength: this.maxLength
    };
  }
}

export default CrossEncoderReranker;