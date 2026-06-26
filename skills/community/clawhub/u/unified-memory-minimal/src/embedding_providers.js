/**
 * Embedding Multi-Provider Client v1.0
 * 自动遍历可用provider，Ollama挂了切OpenAI，OpenAI挂了切Jina...
 */

import { config } from './config.js';
import { log } from './config.js';

export class EmbeddingClient {
  constructor() {
    this.providers = config.embedProviders; // already configured in config.js
    this.cache = new Map();
    this._availableProviders = null; // 缓存可用providers
    this._cacheCheckMs = 60 * 1000; // 每分钟重新检测一次provider可用性
    this._lastCheck = 0;
  }

  /**
   * 检查某个provider是否可用（health check）
   * @param {object} provider
   * @returns {Promise<boolean>}
   */
  async healthCheck(provider) {
    if (!provider.apiKey && provider.name !== 'ollama') {
      // 需要key但没有配置，跳过
      return false;
    }
    try {
      if (provider.name === 'ollama') {
        // Ollama: 访问 /api/tags 或者直接用 /api/embeddings 做健康检查
        const response = await fetch(`${provider.baseURL}/api/tags`, {
          method: 'GET',
          signal: AbortSignal.timeout(3000),
        });
        return response.ok;
      } else {
        // OpenAI/Jina/SiliconFlow: 用 /embeddings 做轻量健康检查
        const body = provider.name === 'openai'
          ? { model: provider.model, input: 'health_check' }
          : { model: provider.model, input: 'health_check' };

        const headers = { 'Content-Type': 'application/json' };
        if (provider.apiKey) headers['Authorization'] = `Bearer ${provider.apiKey}`;

        const response = await fetch(`${provider.baseURL}/embeddings`, {
          method: 'POST',
          headers,
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(5000),
        });
        return response.ok;
      }
    } catch (e) {
      log('WARN', `[EmbeddingClient] healthCheck failed for ${provider.name}: ${e.message}`);
      return false;
    }
  }

  /**
   * 获取可用provider列表（按优先级，过滤不可用的）
   * @returns {Promise<Array>}
   */
  async getAvailableProviders() {
    const now = Date.now();
    if (this._availableProviders && (now - this._lastCheck) < this._cacheCheckMs) {
      return this._availableProviders;
    }

    const available = [];
    for (const provider of this.providers) {
      // 无apiKey且非ollama的provider视为不可用（未配置）
      if (!provider.apiKey && provider.name !== 'ollama') {
        log('WARN', `[EmbeddingClient] Provider ${provider.name} skipped: no API key configured`);
        continue;
      }
      const ok = await this.healthCheck(provider);
      if (ok) {
        available.push(provider);
        log('INFO', `[EmbeddingClient] Provider ${provider.name} is available`);
      } else {
        log('WARN', `[EmbeddingClient] Provider ${provider.name} is NOT available`);
      }
    }

    this._availableProviders = available;
    this._lastCheck = now;
    return available;
  }

  /**
   * 生成文本的hash用于缓存key
   * @param {string} text
   * @returns {string}
   */
  _hashText(text) {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(36);
  }

  /**
   * 核心：自动切换的embed
   * @param {string} text
   * @param {object} options
   * @returns {Promise<number[]|null>}
   */
  async embed(text, options = {}) {
    const cacheKey = this._hashText(text);
    const maxLen = options.maxLength || 2000;
    const truncated = text.slice(0, maxLen);

    // 1. 先查内存缓存
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // 2. 获取可用providers
    const available = await this.getAvailableProviders();
    if (available.length === 0) {
      log('ERROR', '[EmbeddingClient] No embedding providers available');
      return null;
    }

    // 3. 按优先级遍历providers
    for (const provider of available) {
      try {
        const embedding = await this._embedWithProvider(provider, truncated);
        if (embedding) {
          // 成功则缓存
          this.cache.set(cacheKey, embedding);
          log('INFO', `[EmbeddingClient] Embedding succeeded with provider: ${provider.name}`);
          return embedding;
        }
      } catch (e) {
        log('WARN', `[EmbeddingClient] Provider ${provider.name} failed: ${e.message}, trying next...`);
      }
    }

    // 4. 全部失败返回null
    log('ERROR', '[EmbeddingClient] All embedding providers failed');
    return null;
  }

  /**
   * 使用指定provider生成embedding
   * @param {object} provider
   * @param {string} text
   * @returns {Promise<number[]|null>}
   */
  async _embedWithProvider(provider, text) {
    const headers = { 'Content-Type': 'application/json' };
    if (provider.apiKey) {
      headers['Authorization'] = `Bearer ${provider.apiKey}`;
    }

    let body;
    let embeddingsPath;
    if (provider.name === 'ollama') {
      // Ollama 使用 /api/embeddings，字段为 prompt
      body = { model: provider.model, prompt: text };
      embeddingsPath = '/api/embeddings';
    } else {
      // OpenAI/Jina/SiliconFlow 使用 /embeddings，字段为 input
      body = { model: provider.model, input: text };
      embeddingsPath = '/embeddings';
    }

    const response = await fetch(`${provider.baseURL}${embeddingsPath}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(30000),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // 解析不同provider的响应格式
    if (provider.name === 'ollama') {
      return data.embedding || null;
    } else {
      // OpenAI/Jina/SiliconFlow: { data: [{ embedding: [...] }] }
      if (data.data && data.data[0] && data.data[0].embedding) {
        return data.data[0].embedding;
      }
      // 兼容 { embedding: [...] } 格式
      if (data.embedding) return data.embedding;
      return null;
    }
  }

  /**
   * 批量embed（支持并行请求）
   * @param {string[]} texts
   * @param {object} options
   * @returns {Promise<Array<number[]>|null>}
   */
  async embedBatch(texts, options = {}) {
    if (!texts || texts.length === 0) return [];

    // 并行执行所有text的embed，但限制并发数
    const concurrency = options.concurrency || 3;
    const results = [];

    for (let i = 0; i < texts.length; i += concurrency) {
      const batch = texts.slice(i, i + concurrency);
      const batchResults = await Promise.all(
        batch.map(text => this.embed(text, options))
      );
      results.push(...batchResults);
    }

    // 如果有任何失败，返回null
    if (results.some(r => r === null)) {
      log('WARN', '[EmbeddingClient] Some embeddings failed in batch');
      return null;
    }

    return results;
  }

  /**
   * 清除内存缓存
   */
  clearCache() {
    this.cache.clear();
  }

  /**
   * 强制重新检测providers（下次embed时生效）
   */
  refreshProviders() {
    this._availableProviders = null;
    this._lastCheck = 0;
  }
}

// Convenience function: createEmbedding(text) → returns embedding array
let _client;
function getClient() {
  if (!_client) _client = new EmbeddingClient();
  return _client;
}
export async function createEmbedding(text) {
  const client = getClient();
  return await client.embed(text);
}
