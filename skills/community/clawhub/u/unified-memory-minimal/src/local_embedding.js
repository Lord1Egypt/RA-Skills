/**
 * local_embedding.js — 本地 Embedding 服务
 * 
 * 移植自 memory-tencentdb 的 LocalEmbeddingService
 * 使用 node-llama-cpp + GGUF 模型实现完全离线的向量嵌入
 * 
 * 特性:
 * - 完全离线，无需任何 API
 * - 默认使用 embeddinggemma-300m (300MB, 768 维)
 * - 后台预热，不阻塞主线程
 * - 自动截断超长文本
 * - L2 归一化输出
 */

import { log } from './logger.js';

// ─── 常量 ───────────────────────────────────────────────────────────────────

/** 默认模型: Google embeddinggemma-300m Q8_0 量化 (~300MB) */
const DEFAULT_LOCAL_MODEL = 'hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf';

/** embeddinggemma-300m 输出 768 维向量 */
const LOCAL_DIMENSIONS = 768;

/** 最大输入字符数 (embeddinggemma-300m 有 256 token 限制) */
const LOCAL_MAX_INPUT_CHARS = 512;

// ─── 错误类 ─────────────────────────────────────────────────────────────────

/**
 * 本地 Embedding 模型未就绪错误
 */
export class EmbeddingNotReadyError extends Error {
  constructor(message) {
    super(message || 'Local embedding model is not ready yet (still downloading or loading)');
    this.name = 'EmbeddingNotReadyError';
  }
}

// ─── 工具函数 ───────────────────────────────────────────────────────────────

/**
 * 清理 NaN/Inf 值并进行 L2 归一化
 */
function sanitizeAndNormalize(vec) {
  const arr = Array.from(vec).map(v => (Number.isFinite(v) ? v : 0));
  const magnitude = Math.sqrt(arr.reduce((sum, v) => sum + v * v, 0));
  if (magnitude < 1e-10) {
    return new Float32Array(arr);
  }
  return new Float32Array(arr.map(v => v / magnitude));
}

// ─── 本地 Embedding 服务类 ─────────────────────────────────────────────────

/**
 * 本地 Embedding 服务 (node-llama-cpp)
 * 
 * 初始化状态机:
 * - idle: 未启动
 * - initializing: 模型下载/加载中
 * - ready: 模型已加载，可以服务请求
 * - failed: 初始化失败
 */
export class LocalEmbeddingService {
  constructor(config = {}, logger) {
    this.modelPath = config.modelPath?.trim() || DEFAULT_LOCAL_MODEL;
    this.modelCacheDir = config.modelCacheDir?.trim() || undefined;
    this.logger = logger || { info: console.log, warn: console.warn, error: console.error, debug: () => {} };
    
    // 初始化状态
    this.initState = 'idle';
    this.initPromise = null;
    this.initError = null;
    this.embeddingContext = null;
    
    // 统计
    this.stats = {
      totalEmbeddings: 0,
      totalTexts: 0,
      errors: 0,
    };
  }
  
  /**
   * 获取向量维度
   */
  getDimensions() {
    return LOCAL_DIMENSIONS;
  }
  
  /**
   * 获取 Provider 信息
   */
  getProviderInfo() {
    return { provider: 'local', model: this.modelPath };
  }
  
  /**
   * 模型是否就绪
   */
  isReady() {
    return this.initState === 'ready' && this.embeddingContext !== null;
  }
  
  /**
   * 获取状态
   */
  getStatus() {
    return {
      state: this.initState,
      model: this.modelPath,
      dimensions: LOCAL_DIMENSIONS,
      ready: this.isReady(),
      error: this.initError?.message || null,
      stats: this.stats,
    };
  }
  
  /**
   * 启动后台预热: 下载模型（如需要）并加载到内存
   * 不阻塞调用者，立即返回
   * 可以安全多次调用（幂等）
   */
  startWarmup() {
    if (this.initState === 'initializing' || this.initState === 'ready') {
      return; // 已在进行中或已完成
    }
    
    log.info(`[LocalEmbedding] Starting background warmup for model: ${this.modelPath}`);
    this.initState = 'initializing';
    this.initError = null;
    
    this.initPromise = this._doInitialize()
      .then(() => {
        this.initState = 'ready';
        log.info('[LocalEmbedding] Background warmup complete — local embedding ready');
      })
      .catch(err => {
        this.initState = 'failed';
        this.initError = err instanceof Error ? err : new Error(String(err));
        log.error(`[LocalEmbedding] Background warmup failed: ${this.initError.message}`);
      });
  }
  
  /**
   * 获取单个文本的 Embedding
   * @throws {EmbeddingNotReadyError} 如果模型未就绪
   */
  async embed(text) {
    this._assertReady();
    const truncated = this._truncateInput(text);
    
    try {
      const embedding = await this.embeddingContext.getEmbeddingFor(truncated);
      this.stats.totalEmbeddings += 1;
      this.stats.totalTexts += 1;
      return sanitizeAndNormalize(embedding.vector);
    } catch (err) {
      this.stats.errors += 1;
      throw err;
    }
  }
  
  /**
   * 批量获取 Embedding
   * @throws {EmbeddingNotReadyError} 如果模型未就绪
   */
  async embedBatch(texts) {
    if (texts.length === 0) return [];
    this._assertReady();
    
    const results = [];
    for (const text of texts) {
      const truncated = this._truncateInput(text);
      const embedding = await this.embeddingContext.getEmbeddingFor(truncated);
      results.push(sanitizeAndNormalize(embedding.vector));
    }
    
    this.stats.totalEmbeddings += 1;
    this.stats.totalTexts += texts.length;
    
    return results;
  }
  
  /**
   * 释放资源
   */
  close() {
    if (this.embeddingContext) {
      try {
        const ctx = this.embeddingContext;
        if (typeof ctx.dispose === 'function') {
          ctx.dispose();
        }
      } catch {
        // 尽力清理
      }
      this.embeddingContext = null;
      this.initPromise = null;
      this.initState = 'idle';
      this.initError = null;
      log.info('[LocalEmbedding] Resources released');
    }
  }
  
  /**
   * 等待预热完成
   */
  async waitForReady() {
    if (this.initPromise) {
      await this.initPromise;
    }
  }
  
  // ─── 内部方法 ─────────────────────────────────────────────────────────────
  
  /**
   * 断言模型已就绪
   */
  _assertReady() {
    if (this.initState === 'ready' && this.embeddingContext) {
      return;
    }
    
    if (this.initState === 'failed') {
      throw new EmbeddingNotReadyError(
        `Local embedding model initialization failed: ${this.initError?.message || 'unknown error'}. Call startWarmup() to retry.`
      );
    }
    
    if (this.initState === 'initializing') {
      throw new EmbeddingNotReadyError(
        'Local embedding model is still loading (download/initialization in progress). Please try again later.'
      );
    }
    
    // "idle" — startWarmup() 从未被调用
    throw new EmbeddingNotReadyError(
      'Local embedding model warmup has not been started. Call startWarmup() first.'
    );
  }
  
  /**
   * 截断输入文本以适应模型上下文窗口
   */
  _truncateInput(text) {
    if (text.length <= LOCAL_MAX_INPUT_CHARS) return text;
    log.debug(`[LocalEmbedding] Input truncated from ${text.length} to ${LOCAL_MAX_INPUT_CHARS} chars`);
    return text.slice(0, LOCAL_MAX_INPUT_CHARS);
  }
  
  /**
   * 内部: 执行实际的模型下载 + 加载
   */
  async _doInitialize() {
    let model = undefined;
    
    try {
      log.debug('[LocalEmbedding] Loading node-llama-cpp...');
      
      // 动态导入 — node-llama-cpp 是可选依赖
      const { getLlama, resolveModelFile, LlamaLogLevel } = await import('node-llama-cpp').catch(() => {
        throw new Error('node-llama-cpp is not installed. Run: npm install node-llama-cpp');
      });
      
      const llama = await getLlama({ logLevel: LlamaLogLevel.error });
      log.debug('[LocalEmbedding] Llama instance created');
      
      const resolvedPath = await resolveModelFile(this.modelPath, this.modelCacheDir);
      log.debug(`[LocalEmbedding] Model resolved: ${resolvedPath}`);
      
      model = await llama.loadModel({ modelPath: resolvedPath });
      log.debug('[LocalEmbedding] Model loaded, creating embedding context...');
      
      this.embeddingContext = await model.createEmbeddingContext();
      log.info(`[LocalEmbedding] Ready (model=${this.modelPath}, dims=${LOCAL_DIMENSIONS})`);
      
    } catch (err) {
      // 清理部分初始化的资源
      if (model?.dispose) {
        try { model.dispose(); } catch { /* 尽力清理 */ }
      }
      this.embeddingContext = null;
      throw err;
    }
  }
}

// ─── 单例实例 ─────────────────────────────────────────────────────────────

let localEmbeddingInstance = null;

/**
 * 获取本地 Embedding 服务实例
 */
export function getLocalEmbedding(config, logger) {
  if (!localEmbeddingInstance) {
    localEmbeddingInstance = new LocalEmbeddingService(config, logger);
  }
  return localEmbeddingInstance;
}

/**
 * 初始化本地 Embedding 服务
 */
export function initLocalEmbedding(config, logger) {
  if (localEmbeddingInstance) {
    localEmbeddingInstance.close();
  }
  localEmbeddingInstance = new LocalEmbeddingService(config, logger);
  return localEmbeddingInstance;
}

/**
 * 检查 node-llama-cpp 是否可用
 */
export async function isLocalEmbeddingAvailable() {
  try {
    await import('node-llama-cpp');
    return true;
  } catch {
    return false;
  }
}

export default {
  LocalEmbeddingService,
  EmbeddingNotReadyError,
  getLocalEmbedding,
  initLocalEmbedding,
  isLocalEmbeddingAvailable,
};
