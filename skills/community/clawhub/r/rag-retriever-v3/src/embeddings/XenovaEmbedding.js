/**
 * Xenova/Transformers 本地嵌入模型
 * 使用 @xenova/transformers 在本地运行嵌入模型，无需 API Key
 */

import { EmbeddingProvider } from './EmbeddingProvider.js';
import { pipeline, env } from '@xenova/transformers';

// 配置 transformers.js
env.allowLocalModels = true;
env.allowRemoteModels = true;

export class XenovaEmbedding extends EmbeddingProvider {
  constructor(options = {}) {
    super(options);
    this.modelName = options.modelName || 'Xenova/all-MiniLM-L6-v2';
    this.name = 'xenova';
    this.pipeline = null;
    
    // 模型维度映射
    this.dimensionMap = {
      'Xenova/all-MiniLM-L6-v2': 384,
      'Xenova/bge-small-en-v1.5': 384,
      'Xenova/bge-base-en-v1.5': 768,
      'Xenova/bge-large-en-v1.5': 1024,
      'Xenova/bge-small-zh-v1.5': 512,
      'Xenova/bge-base-zh-v1.5': 768,
      'Xenova/bge-large-zh-v1.5': 1024,
      'Xenova/gte-small': 384,
      'Xenova/gte-base': 768,
      'Xenova/multilingual-e5-small': 384,
      'Xenova/multilingual-e5-base': 768,
      'Xenova/multilingual-e5-large': 1024
    };
    
    // 自动设置维度
    if (this.dimensionMap[this.modelName]) {
      this.dimensions = this.dimensionMap[this.modelName];
    }
  }

  /**
   * 初始化嵌入管道
   */
  async initialize() {
    if (this.initialized) return;

    console.log(`[XenovaEmbedding] 加载模型: ${this.modelName}`);
    
    try {
      // 创建特征提取管道
      this.pipeline = await pipeline(
        'feature-extraction',
        this.modelName,
        {
          quantized: true, // 使用量化模型以减少内存占用
          revision: 'main',
          progress_callback: (progress) => {
            if (progress.status === 'progress') {
              const percent = ((progress.loaded / progress.total) * 100).toFixed(1);
              process.stdout.write(`\r[XenovaEmbedding] 加载进度: ${percent}%`);
            }
          }
        }
      );
      
      console.log('\n[XenovaEmbedding] ✅ 模型加载完成');
      this.initialized = true;
    } catch (error) {
      console.error('[XenovaEmbedding] ❌ 模型加载失败:', error.message);
      throw error;
    }
  }

  /**
   * 生成单个文本的嵌入向量
   */
  async embed(text) {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!text || typeof text !== 'string') {
      throw new Error('输入必须是有效的字符串');
    }

    try {
      // 截断长文本（大多数模型有最大长度限制）
      const maxLength = 512;
      const truncatedText = text.length > maxLength * 3 
        ? text.slice(0, maxLength * 3) 
        : text;

      // 生成嵌入
      const output = await this.pipeline(truncatedText, {
        pooling: 'mean',
        normalize: true
      });

      // 转换为数组
      const embedding = Array.from(output.data);
      
      return embedding;
    } catch (error) {
      console.error('[XenovaEmbedding] 嵌入生成失败:', error.message);
      throw error;
    }
  }

  /**
   * 批量生成嵌入（优化版本）
   */
  async embedBatch(texts, batchSize = 8) {
    if (!this.initialized) {
      await this.initialize();
    }

    const results = [];
    
    // 分批处理以避免内存问题
    for (let i = 0; i < texts.length; i += batchSize) {
      const batch = texts.slice(i, i + batchSize);
      const batchPromises = batch.map(text => this.embed(text));
      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
      
      if (i + batchSize < texts.length) {
        process.stdout.write(`\r[XenovaEmbedding] 处理进度: ${Math.min(i + batchSize, texts.length)}/${texts.length}`);
      }
    }
    
    console.log(`\r[XenovaEmbedding] 完成: ${texts.length} 个文本的嵌入生成`);
    return results;
  }

  /**
   * 获取支持的模型列表
   */
  static getSupportedModels() {
    return [
      { name: 'Xenova/all-MiniLM-L6-v2', dimensions: 384, description: '轻量级英文模型' },
      { name: 'Xenova/bge-small-en-v1.5', dimensions: 384, description: 'BGE 英文小模型' },
      { name: 'Xenova/bge-base-en-v1.5', dimensions: 768, description: 'BGE 英文基础模型' },
      { name: 'Xenova/bge-large-en-v1.5', dimensions: 1024, description: 'BGE 英文大模型' },
      { name: 'Xenova/bge-small-zh-v1.5', dimensions: 512, description: 'BGE 中文小模型' },
      { name: 'Xenova/bge-base-zh-v1.5', dimensions: 768, description: 'BGE 中文基础模型' },
      { name: 'Xenova/bge-large-zh-v1.5', dimensions: 1024, description: 'BGE 中文大模型' },
      { name: 'Xenova/gte-small', dimensions: 384, description: 'GTE 小模型' },
      { name: 'Xenova/gte-base', dimensions: 768, description: 'GTE 基础模型' },
      { name: 'Xenova/multilingual-e5-small', dimensions: 384, description: '多语言 E5 小模型' },
      { name: 'Xenova/multilingual-e5-base', dimensions: 768, description: '多语言 E5 基础模型' },
      { name: 'Xenova/multilingual-e5-large', dimensions: 1024, description: '多语言 E5 大模型' }
    ];
  }

  getInfo() {
    return {
      ...super.getInfo(),
      modelName: this.modelName,
      type: 'local'
    };
  }
}

export default XenovaEmbedding;
