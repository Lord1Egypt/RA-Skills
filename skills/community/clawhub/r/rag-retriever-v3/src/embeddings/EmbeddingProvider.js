/**
 * 嵌入模型提供者基类
 * 定义所有嵌入模型的通用接口
 */

export class EmbeddingProvider {
  constructor(options = {}) {
    this.dimensions = options.dimensions || 384;
    this.name = 'base';
    this.initialized = false;
  }

  /**
   * 初始化模型
   */
  async initialize() {
    throw new Error('子类必须实现 initialize 方法');
  }

  /**
   * 生成单个文本的嵌入向量
   * @param {string} text - 输入文本
   * @returns {Promise<number[]>} - 嵌入向量
   */
  async embed(text) {
    throw new Error('子类必须实现 embed 方法');
  }

  /**
   * 批量生成嵌入向量
   * @param {string[]} texts - 文本数组
   * @returns {Promise<number[][]>} - 嵌入向量数组
   */
  async embedBatch(texts) {
    const results = [];
    for (const text of texts) {
      results.push(await this.embed(text));
    }
    return results;
  }

  /**
   * 获取模型信息
   */
  getInfo() {
    return {
      name: this.name,
      dimensions: this.dimensions,
      initialized: this.initialized
    };
  }
}

export default EmbeddingProvider;
