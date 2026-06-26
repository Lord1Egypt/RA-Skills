/**
 * OpenAI API 嵌入模型
 * 使用 OpenAI API 生成嵌入向量
 * 
 * 注意：openai 是可选依赖，如果未安装会抛出友好错误
 */

import { EmbeddingProvider } from './EmbeddingProvider.js';

// 动态导入 openai，使其成为可选依赖
let OpenAI = null;
let openaiAvailable = false;

try {
  const openaiModule = await import('openai');
  OpenAI = openaiModule.default;
  openaiAvailable = true;
} catch (error) {
  openaiAvailable = false;
}

export class OpenAIEmbedding extends EmbeddingProvider {
  constructor(options = {}) {
    super(options);
    this.apiKey = options.apiKey || process.env.OPENAI_API_KEY;
    this.modelName = options.modelName || 'text-embedding-3-small';
    this.baseURL = options.baseURL || 'https://api.openai.com/v1';
    this.name = 'openai';
    this.client = null;
    
    // OpenAI 模型维度映射
    this.dimensionMap = {
      'text-embedding-ada-002': 1536,
      'text-embedding-3-small': 1536,
      'text-embedding-3-large': 3072
    };
    
    // 自动设置维度
    if (this.dimensionMap[this.modelName]) {
      this.dimensions = this.dimensionMap[this.modelName];
    }
  }

  /**
   * 初始化 OpenAI 客户端
   */
  async initialize() {
    if (this.initialized) return;

    // 检查 openai 模块是否可用
    if (!openaiAvailable) {
      throw new Error(
        'OpenAI 模块未安装。请运行: npm install openai\n' +
        '或者使用本地模型: createEmbeddingProvider("xenova")'
      );
    }

    if (!this.apiKey) {
      throw new Error('OpenAI API Key 未设置。请设置 OPENAI_API_KEY 环境变量或在选项中提供 apiKey');
    }

    console.log(`[OpenAIEmbedding] 初始化 OpenAI 客户端，模型: ${this.modelName}`);
    
    try {
      this.client = new OpenAI({
        apiKey: this.apiKey,
        baseURL: this.baseURL
      });
      
      this.initialized = true;
      console.log('[OpenAIEmbedding] ✅ 初始化完成');
    } catch (error) {
      console.error('[OpenAIEmbedding] ❌ 初始化失败:', error.message);
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
      const response = await this.client.embeddings.create({
        model: this.modelName,
        input: text,
        encoding_format: 'float'
      });

      return response.data[0].embedding;
    } catch (error) {
      console.error('[OpenAIEmbedding] 嵌入生成失败:', error.message);
      throw error;
    }
  }

  /**
   * 批量生成嵌入向量
   */
  async embedBatch(texts, batchSize = 100) {
    if (!this.initialized) {
      await this.initialize();
    }

    const results = [];
    
    // OpenAI API 限制：每次最多 2048 个输入
    const effectiveBatchSize = Math.min(batchSize, 100);
    
    for (let i = 0; i < texts.length; i += effectiveBatchSize) {
      const batch = texts.slice(i, i + effectiveBatchSize);
      
      try {
        const response = await this.client.embeddings.create({
          model: this.modelName,
          input: batch,
          encoding_format: 'float'
        });

        // 按索引排序结果
        const embeddings = response.data
          .sort((a, b) => a.index - b.index)
          .map(item => item.embedding);
        
        results.push(...embeddings);
        
        if (i + effectiveBatchSize < texts.length) {
          process.stdout.write(`\r[OpenAIEmbedding] 处理进度: ${Math.min(i + effectiveBatchSize, texts.length)}/${texts.length}`);
        }
      } catch (error) {
        console.error('[OpenAIEmbedding] 批量嵌入失败:', error.message);
        throw error;
      }
    }
    
    console.log(`\r[OpenAIEmbedding] 完成: ${texts.length} 个文本的嵌入生成`);
    return results;
  }

  /**
   * 获取支持的模型列表
   */
  static getSupportedModels() {
    return [
      { name: 'text-embedding-3-small', dimensions: 1536, description: 'OpenAI 小型嵌入模型，性价比高' },
      { name: 'text-embedding-3-large', dimensions: 3072, description: 'OpenAI 大型嵌入模型，精度更高' },
      { name: 'text-embedding-ada-002', dimensions: 1536, description: 'OpenAI 旧版嵌入模型' }
    ];
  }

  /**
   * 估算 token 使用量
   */
  estimateTokens(texts) {
    // 粗略估算：英文约 1 token/字符，中文约 2 tokens/字符
    let totalTokens = 0;
    for (const text of texts) {
      const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
      const otherChars = text.length - chineseChars;
      totalTokens += chineseChars * 2 + otherChars;
    }
    return totalTokens;
  }

  getInfo() {
    return {
      ...super.getInfo(),
      modelName: this.modelName,
      baseURL: this.baseURL,
      type: 'api'
    };
  }
}

export default OpenAIEmbedding;
