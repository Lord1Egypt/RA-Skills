// RAG 2.0 - 向量嵌入模块
// 支持 OpenAI Embeddings 和本地 MiniLM

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * OpenAI Embedding 提供者
 */
export class OpenAIEmbedding {
  constructor(options = {}) {
    this.apiKey = options.apiKey || process.env.OPENAI_API_KEY;
    this.model = options.model || 'text-embedding-3-small';
    this.dimensions = options.dimensions || 1536;
    this.batchSize = options.batchSize || 100;
    this.cachePath = options.cachePath || join(__dirname, '../data/embedding-cache.json');
    this.cache = this.loadCache();
  }

  loadCache() {
    if (existsSync(this.cachePath)) {
      try {
        return JSON.parse(readFileSync(this.cachePath, 'utf-8'));
      } catch {
        return {};
      }
    }
    return {};
  }

  saveCache() {
    const dir = dirname(this.cachePath);
    if (!existsSync(dir)) {
      import('fs').then(fs => fs.mkdirSync(dir, { recursive: true }));
    }
    writeFileSync(this.cachePath, JSON.stringify(this.cache, null, 2));
  }

  async getCacheKey(text) {
    const crypto = await import('crypto');
    return crypto.createHash('md5').update(text).digest('hex');
  }

  /**
   * 生成单个文本的嵌入向量
   */
  async embed(text) {
    const cacheKey = await this.getCacheKey(text);
    if (this.cache[cacheKey]) {
      return this.cache[cacheKey];
    }

    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        input: text,
        model: this.model,
        dimensions: this.dimensions
      })
    });

    if (!response.ok) {
      throw new Error(`OpenAI Embedding API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    const embedding = data.data[0].embedding;
    
    // 缓存结果
    this.cache[cacheKey] = embedding;
    
    return embedding;
  }

  /**
   * 批量生成嵌入向量
   */
  async embedBatch(texts) {
    const results = [];
    const toProcess = [];
    const toProcessIndices = [];

    // 检查缓存
    for (let i = 0; i < texts.length; i++) {
      const cacheKey = await this.getCacheKey(texts[i]);
      if (this.cache[cacheKey]) {
        results[i] = this.cache[cacheKey];
      } else {
        toProcess.push(texts[i]);
        toProcessIndices.push(i);
      }
    }

    // 批量处理未缓存的
    if (toProcess.length > 0) {
      for (let i = 0; i < toProcess.length; i += this.batchSize) {
        const batch = toProcess.slice(i, i + this.batchSize);
        
        const response = await fetch('https://api.openai.com/v1/embeddings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiKey}`
          },
          body: JSON.stringify({
            input: batch,
            model: this.model,
            dimensions: this.dimensions
          })
        });

        if (!response.ok) {
          throw new Error(`OpenAI Embedding API error: ${response.status}`);
        }

        const data = await response.json();
        
        for (let j = 0; j < data.data.length; j++) {
          const idx = toProcessIndices[i + j];
          const embedding = data.data[j].embedding;
          results[idx] = embedding;
          
          // 缓存
          const cacheKey = await this.getCacheKey(toProcess[i + j]);
          this.cache[cacheKey] = embedding;
        }
      }
    }

    this.saveCache();
    return results;
  }
}

/**
 * 简单本地嵌入（基于词频向量，用于测试和降级）
 */
export class SimpleEmbedding {
  constructor(options = {}) {
    this.dimensions = options.dimensions || 384;
  }

  /**
   * 生成简单的词频向量
   */
  async embed(text) {
    const words = text.toLowerCase()
      .replace(/[^\w\s\u4e00-\u9fff]/g, '')
      .split(/\s+/)
      .filter(w => w.length > 0);
    
    const vector = new Array(this.dimensions).fill(0);
    
    for (const word of words) {
      const hash = this.hashWord(word);
      const idx = Math.abs(hash) % this.dimensions;
      vector[idx] += 1;
    }

    // 归一化
    const magnitude = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
    if (magnitude > 0) {
      for (let i = 0; i < vector.length; i++) {
        vector[i] /= magnitude;
      }
    }

    return vector;
  }

  async embedBatch(texts) {
    return Promise.all(texts.map(t => this.embed(t)));
  }

  hashWord(word) {
    let hash = 0;
    for (let i = 0; i < word.length; i++) {
      const char = word.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash;
  }
}

/**
 * 嵌入提供者工厂
 */
export function createEmbeddingProvider(type = 'simple', options = {}) {
  switch (type) {
    case 'openai':
      return new OpenAIEmbedding(options);
    case 'simple':
    default:
      return new SimpleEmbedding(options);
  }
}
