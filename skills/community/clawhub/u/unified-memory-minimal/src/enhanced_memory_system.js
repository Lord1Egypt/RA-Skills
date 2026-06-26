/**
 * Enhanced Memory System - 增强版记忆系统
 * 整合所有 OpenViking 风格的组件
 */

import { logger } from './logger.js';
import { MemoryPipeline } from './memory_pipeline.js';
import { getMemoryTypeRegistry } from './memory_types/registry.js';
import { getMemoryQueue } from './queue/memory_queue.js';
import { getSmartDeduplicator } from './deduplication/smart_deduplicator.js';
import { getMemoryRecallOptimizer } from './recall/memory_recall_optimizer.js';
import { getMemoryCompressor } from './compression/memory_compressor.js';
import { getLayeredCompressor } from './compression/layered_compressor.js';
import { getMemoryLifecycleManager } from './lifecycle/memory_lifecycle_manager.js';
import { storage } from './storage.js';
import { vector_lancedb } from './vector_lancedb.js';

// Claude-Mem 风格功能
import { 
  createClaudeMemFeatures,
  MemoryEditor,
  PrivacyManager,
  MemoryQuality,
  MemoryIndex 
} from './claudemem_features/index.js';

export class EnhancedMemorySystem {
  constructor(options = {}) {
    this.options = {
      enablePipeline: options.enablePipeline !== false,
      enableQueue: options.enableQueue !== false,
      enableDedup: options.enableDedup !== false,
      enableTypeSystem: options.enableTypeSystem !== false,
      enableRecallOptimization: options.enableRecallOptimization !== false,
      enableCompression: options.enableCompression !== false,
      enableLayeredCompression: options.enableLayeredCompression !== false,  // 新增：分层压缩
      enableLifecycle: options.enableLifecycle !== false,
      asyncProcessing: options.asyncProcessing !== false,
      // Claude-Mem 功能选项
      enableClaudeMem: options.enableClaudeMem !== false,
      enableMemoryEditor: options.enableMemoryEditor !== false,
      enablePrivacyManager: options.enablePrivacyManager !== false,
      enableMemoryQuality: options.enableMemoryQuality !== false,
      enableMemoryIndex: options.enableMemoryIndex !== false,
      ...options
    };
    
    // 初始化组件
    this.pipeline = null;
    this.typeRegistry = null;
    this.queue = null;
    this.deduplicator = null;
    this.recallOptimizer = null;
    this.compressor = null;
    this.layeredCompressor = null;  // 新增：分层压缩器
    this.lifecycleManager = null;
    
    // Claude-Mem 功能组件
    this.memoryEditor = null;
    this.privacyManager = null;
    this.memoryQuality = null;
    this.memoryIndex = null;
    
    // 存储后端
    this.storage = storage;
    this.vectorStore = vector_lancedb;
    
    // 初始化标志
    this.initialized = false;
    
    logger.info('[EnhancedMemorySystem] 增强版记忆系统创建');
  }
  
  /**
   * 初始化系统
   */
  async initialize() {
    if (this.initialized) {
      return;
    }
    
    logger.info('[EnhancedMemorySystem] 开始初始化...');
    
    try {
      // 1. 初始化类型注册系统
      if (this.options.enableTypeSystem) {
        this.typeRegistry = getMemoryTypeRegistry();
        logger.info('[EnhancedMemorySystem] 类型注册系统已初始化');
      }
      
      // 2. 初始化队列系统
      if (this.options.enableQueue) {
        this.queue = getMemoryQueue(this.options.queueOptions);
        this.registerQueueProcessors();
        logger.info('[EnhancedMemorySystem] 队列系统已初始化');
      }
      
      // 3. 初始化去重系统
      if (this.options.enableDedup) {
        this.deduplicator = getSmartDeduplicator(this.options.dedupOptions);
        logger.info('[EnhancedMemorySystem] 去重系统已初始化');
      }
      
      // 4. 初始化处理管道
      if (this.options.enablePipeline) {
        this.pipeline = new MemoryPipeline({
          enableL0: true,
          enableL1: true,
          enableL2: true,
          enableL3: true,
          asyncProcessing: this.options.asyncProcessing,
          ...this.options.pipelineOptions
        });
        logger.info('[EnhancedMemorySystem] 处理管道已初始化');
      }
      
      // 5. 初始化召回优化器
      if (this.options.enableRecallOptimization) {
        this.recallOptimizer = getMemoryRecallOptimizer(this.options.recallOptions);
        logger.info('[EnhancedMemorySystem] 召回优化器已初始化');
      }
      
      // 6. 初始化压缩器
      if (this.options.enableCompression) {
        this.compressor = getMemoryCompressor(this.options.compressionOptions);
        logger.info('[EnhancedMemorySystem] 压缩器已初始化');
      }
      
      // 6.5 初始化分层压缩器（借鉴 OpenViking）
      if (this.options.enableLayeredCompression) {
        this.layeredCompressor = getLayeredCompressor(this.options.layeredCompressionOptions);
        logger.info('[EnhancedMemorySystem] 分层压缩器已初始化（L0/L1/L2）');
      }
      
      // 7. 初始化生命周期管理器
      if (this.options.enableLifecycle) {
        this.lifecycleManager = getMemoryLifecycleManager(this.options.lifecycleOptions);
        // 启动自动管理
        this.lifecycleManager.startAutoManagement(this.storage, this.vectorStore);
        logger.info('[EnhancedMemorySystem] 生命周期管理器已初始化');
      }
      
      // 8. 初始化 Claude-Mem 风格功能
      if (this.options.enableClaudeMem) {
        await this.initializeClaudeMemFeatures();
        logger.info('[EnhancedMemorySystem] Claude-Mem 功能已初始化');
      }
      
      this.initialized = true;
      
      logger.info('[EnhancedMemorySystem] 初始化完成');
      
    } catch (error) {
      logger.error('[EnhancedMemorySystem] 初始化失败:', error);
      throw error;
    }
  }
  
  /**
   * 注册队列处理器
   */
  registerQueueProcessors() {
    // Embedding 处理器
    this.queue.registerProcessor('embedding', async (task) => {
      logger.debug(`[QueueProcessor] 处理 embedding 任务: ${task.id}`);
      
      // 调用向量存储生成 embedding
      if (this.vectorStore && this.vectorStore.embed) {
        return await this.vectorStore.embed(task.text);
      }
      
      return { embedding: null, status: 'skipped' };
    });
    
    // 语义分析处理器
    this.queue.registerProcessor('semantic', async (task) => {
      logger.debug(`[QueueProcessor] 处理语义分析任务: ${task.id}`);
      
      if (this.typeRegistry) {
        const detected = await this.typeRegistry.detectMemoryType(task.text);
        const processed = await this.typeRegistry.processMemory(
          task.text,
          detected.type,
          task.context
        );
        
        return processed;
      }
      
      return { status: 'skipped' };
    });
    
    // 去重处理器
    this.queue.registerProcessor('deduplication', async (task) => {
      logger.debug(`[QueueProcessor] 处理去重任务: ${task.id}`);
      
      if (this.deduplicator) {
        const result = await this.deduplicator.checkDuplicate(
          task.memory,
          task.existingMemories
        );
        
        return result;
      }
      
      return { isDuplicate: false };
    });
    
    // 归档处理器
    this.queue.registerProcessor('archiving', async (task) => {
      logger.debug(`[QueueProcessor] 处理归档任务: ${task.id}`);
      
      if (this.storage && this.storage.archive) {
        return await this.storage.archive(task.memory);
      }
      
      return { status: 'archived' };
    });
    
    // 索引处理器
    this.queue.registerProcessor('indexing', async (task) => {
      logger.debug(`[QueueProcessor] 处理索引任务: ${task.id}`);
      
      if (this.vectorStore && this.vectorStore.add) {
        return await this.vectorStore.add(task.memory);
      }
      
      return { status: 'indexed' };
    });
  }
  
  /**
   * 存储记忆（增强版）
   */
  async remember(text, context = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    logger.info(`[EnhancedMemorySystem] 存储记忆: ${text.substring(0, 50)}...`);
    
    try {
      // 1. 检测记忆类型
      let memoryType = 'facts';
      let processedMemory = null;
      
      if (this.typeRegistry) {
        const detected = await this.typeRegistry.detectMemoryType(text, context);
        memoryType = detected.type;
        
        logger.debug(`[EnhancedMemorySystem] 检测到记忆类型: ${memoryType} (置信度: ${detected.confidence})`);
        
        // 2. 根据类型处理记忆
        processedMemory = await this.typeRegistry.processMemory(text, memoryType, context);
      } else {
        // 简单处理
        processedMemory = {
          id: `mem_${Date.now()}`,
          text: text,
          type: memoryType,
          timestamp: Date.now(),
          metadata: context
        };
      }
      
      // 3. 去重检查
      if (this.deduplicator && context.skipDedup !== true) {
        const existingMemories = await this.getRecentMemories(100);
        const dupResult = await this.deduplicator.checkDuplicate(
          processedMemory,
          existingMemories
        );
        
        if (dupResult.isDuplicate) {
          logger.info(`[EnhancedMemorySystem] 检测到重复记忆 (${dupResult.duplicateType}), 动作: ${dupResult.action}`);
          
          if (dupResult.action === 'skip') {
            return {
              status: 'duplicate_skipped',
              duplicateOf: dupResult.similarMemories[0]?.memory.id
            };
          }
          
          if (dupResult.action === 'merge' && dupResult.similarMemories.length > 0) {
            const merged = await this.deduplicator.mergeMemories(
              processedMemory,
              dupResult.similarMemories[0].memory
            );
            processedMemory = merged;
          }
        }
      }
      
      // 4. 存储到后端
      await this.storage.save(processedMemory);
      
      // 5. 异步处理（队列）
      if (this.queue && this.options.asyncProcessing) {
        // Embedding 任务
        this.queue.enqueue('embedding', {
          id: processedMemory.id,
          text: processedMemory.text
        });
        
        // 索引任务
        this.queue.enqueue('indexing', {
          memory: processedMemory
        });
      }
      
      logger.info(`[EnhancedMemorySystem] 记忆已存储: ${processedMemory.id}`);
      
      return {
        status: 'success',
        memory: processedMemory,
        type: memoryType
      };
      
    } catch (error) {
      logger.error('[EnhancedMemorySystem] 存储记忆失败:', error);
      throw error;
    }
  }
  
  /**
   * 回忆记忆（增强版）
   */
  async recall(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    logger.info(`[EnhancedMemorySystem] 回忆记忆: ${query}`);
    
    try {
      // 1. 检测查询类型
      let queryType = 'general';
      
      if (this.typeRegistry && options.detectType !== false) {
        const detected = await this.typeRegistry.detectMemoryType(query);
        queryType = detected.type;
        
        logger.debug(`[EnhancedMemorySystem] 查询类型: ${queryType}`);
      }
      
      // 2. 向量搜索
      let vectorResults = [];
      
      if (this.vectorStore && options.useVector !== false) {
        vectorResults = await this.vectorStore.search(query, {
          limit: options.limit || 20,
          threshold: options.threshold || 0.6
        });
      }
      
      // 3. 文本搜索
      let textResults = [];
      
      if (this.storage && options.useTextSearch !== false) {
        textResults = await this.storage.search(query, {
          limit: options.limit || 20,
          type: options.type || queryType
        });
      }
      
      // 4. 合并结果
      const mergedResults = this.mergeSearchResults(vectorResults, textResults);
      
      // 5. 召回优化
      let finalResults = mergedResults;
      
      if (this.recallOptimizer && options.optimizeRecall !== false) {
        const optimized = await this.recallOptimizer.optimizeRecall(
          query,
          mergedResults,
          {
            userId: options.userId,
            sessionId: options.sessionId,
            type: queryType,
            timestamp: Date.now()
          }
        );
        
        finalResults = optimized.memories;
      }
      
      // 6. 压缩记忆（如果需要）
      let compressedText = null;
      
      // 6.5 分层压缩（借鉴 OpenViking）
      if (this.layeredCompressor && options.useLayeredCompression) {
        const layeredResult = this.layeredCompressor.selectLayer(
          finalResults,
          query,
          {
            maxTokens: options.maxTokens || 4000,
            strategy: options.layerStrategy || 'adaptive'
          }
        );
        
        finalResults = layeredResult.memories;
        compressedText = finalResults.map(m => m.text).join('\n\n');
        
        logger.info(`[EnhancedMemorySystem] 分层压缩: ${layeredResult.stats.l0Filtered} → ${layeredResult.stats.l1Used} 条记忆, ${layeredResult.totalTokens} tokens`);
        
      } else if (this.compressor && options.compress !== false) {
        const compressed = await this.compressor.compress(finalResults, {
          userId: options.userId,
          format: options.format || 'structured'
        });
        
        compressedText = compressed.text;
      }
      
      logger.info(`[EnhancedMemorySystem] 找到 ${finalResults.length} 条记忆`);
      
      return {
        status: 'success',
        query: query,
        queryType: queryType,
        results: finalResults,
        compressedText: compressedText,
        stats: {
          vectorResults: vectorResults.length,
          textResults: textResults.length,
          finalResults: finalResults.length
        }
      };
      
    } catch (error) {
      logger.error('[EnhancedMemorySystem] 回忆记忆失败:', error);
      throw error;
    }
  }
  
  /**
   * 获取最近的记忆
   */
  async getRecentMemories(limit = 100) {
    if (!this.storage) {
      return [];
    }
    
    try {
      const memories = await this.storage.list({
        limit: limit,
        sort: 'timestamp',
        order: 'desc'
      });
      
      return memories || [];
    } catch (error) {
      logger.error('[EnhancedMemorySystem] 获取最近记忆失败:', error);
      return [];
    }
  }
  
  /**
   * 合并搜索结果
   */
  mergeSearchResults(vectorResults, textResults) {
    const merged = [];
    const seen = new Set();
    
    // 添加向量搜索结果
    for (const result of vectorResults) {
      const key = result.id || result.text;
      if (!seen.has(key)) {
        seen.add(key);
        merged.push({
          ...result,
          source: 'vector'
        });
      }
    }
    
    // 添加文本搜索结果
    for (const result of textResults) {
      const key = result.id || result.text;
      if (!seen.has(key)) {
        seen.add(key);
        merged.push({
          ...result,
          source: 'text'
        });
      } else {
        // 如果已存在，标记为双重匹配
        const existing = merged.find(m => (m.id || m.text) === key);
        if (existing) {
          existing.source = 'both';
          existing.textScore = result.score;
        }
      }
    }
    
    // 排序（双重匹配优先，然后按分数）
    merged.sort((a, b) => {
      if (a.source === 'both' && b.source !== 'both') return -1;
      if (a.source !== 'both' && b.source === 'both') return 1;
      return (b.score || 0) - (a.score || 0);
    });
    
    return merged;
  }
  
  /**
   * 处理对话（管道模式）
   */
  async processConversation(conversationData, context = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    if (!this.pipeline) {
      throw new Error('处理管道未启用');
    }
    
    logger.info('[EnhancedMemorySystem] 处理对话');
    
    const taskId = await this.pipeline.processConversation(conversationData, context);
    
    return {
      taskId: taskId,
      status: 'processing',
      message: '对话正在后台处理'
    };
  }
  
  /**
   * 获取系统状态
   */
  getStatus() {
    const status = {
      initialized: this.initialized,
      components: {
        pipeline: this.pipeline ? this.pipeline.getStatus() : null,
        queue: this.queue ? this.queue.healthCheck() : null,
        deduplicator: this.deduplicator ? this.deduplicator.getStats() : null,
        recallOptimizer: this.recallOptimizer ? this.recallOptimizer.getStats() : null,
        compressor: this.compressor ? this.compressor.getStats() : null,
        layeredCompressor: this.layeredCompressor ? this.layeredCompressor.getStats() : null,  // 新增
        lifecycleManager: this.lifecycleManager ? this.lifecycleManager.getLifecycleStats() : null,
        typeRegistry: this.typeRegistry ? {
          typesCount: this.typeRegistry.types.size,
          types: Object.keys(this.typeRegistry.getAllTypes())
        } : null
      }
    };
    
    return status;
  }
  
  /**
   * 健康检查
   */
  healthCheck() {
    const health = {
      status: 'healthy',
      components: {}
    };
    
    // 检查各个组件
    if (this.pipeline) {
      const pipelineStatus = this.pipeline.getStatus();
      health.components.pipeline = {
        status: pipelineStatus.isProcessing ? 'processing' : 'idle',
        queueLength: pipelineStatus.queueLength
      };
    }
    
    if (this.queue) {
      const queueHealth = this.queue.healthCheck();
      health.components.queue = {
        status: queueHealth.status,
        activeTasks: queueHealth.activeTasks
      };
      
      if (queueHealth.status !== 'healthy') {
        health.status = 'degraded';
      }
    }
    
    if (this.deduplicator) {
      const dedupStats = this.deduplicator.getStats();
      health.components.deduplicator = {
        status: 'healthy',
        totalChecked: dedupStats.totalChecked,
        duplicatesFound: dedupStats.duplicatesFound
      };
    }
    
    if (this.typeRegistry) {
      health.components.typeRegistry = {
        status: 'healthy',
        typesCount: this.typeRegistry.types.size
      };
    }
    
    if (this.recallOptimizer) {
      health.components.recallOptimizer = {
        status: 'healthy',
        totalRecalls: this.recallOptimizer.getStats().totalRecalls
      };
    }
    
    if (this.compressor) {
      health.components.compressor = {
        status: 'healthy',
        compressionRatio: this.compressor.getStats().avgCompressionRatio
      };
    }
    
    if (this.layeredCompressor) {
      health.components.layeredCompressor = {
        status: 'healthy',
        totalTokensSaved: this.layeredCompressor.getStats().totalTokensSaved,
        avgCompressionRatio: this.layeredCompressor.getStats().compressionRatio
      };
    }
    
    if (this.lifecycleManager) {
      health.components.lifecycleManager = {
        status: 'healthy',
        ...this.lifecycleManager.getLifecycleStats()
      };
    }
    
    // Claude-Mem 功能状态
    if (this.options.enableClaudeMem) {
      health.components.claudeMem = {
        status: 'healthy',
        features: {
          memoryEditor: !!this.memoryEditor,
          privacyManager: !!this.privacyManager,
          memoryQuality: !!this.memoryQuality,
          memoryIndex: !!this.memoryIndex
        }
      };
    }
    
    return health;
  }
  
  /**
   * 初始化 Claude-Mem 风格功能
   */
  async initializeClaudeMemFeatures() {
    try {
      // 初始化记忆编辑系统
      if (this.options.enableMemoryEditor) {
        this.memoryEditor = new MemoryEditor(this.storage, this.vectorStore);
        logger.info('[EnhancedMemorySystem] 记忆编辑系统已初始化');
      }
      
      // 初始化隐私管理系统
      if (this.options.enablePrivacyManager) {
        this.privacyManager = new PrivacyManager(this.storage, this.memoryEditor);
        logger.info('[EnhancedMemorySystem] 隐私管理系统已初始化');
      }
      
      // 初始化记忆质量评估系统
      if (this.options.enableMemoryQuality) {
        this.memoryQuality = new MemoryQuality(this.storage, this.vectorStore);
        logger.info('[EnhancedMemorySystem] 记忆质量评估系统已初始化');
      }
      
      // 初始化记忆索引系统
      if (this.options.enableMemoryIndex) {
        this.memoryIndex = new MemoryIndex(this.storage, this.vectorStore);
        logger.info('[EnhancedMemorySystem] 记忆索引系统已初始化');
      }
      
      // 批量索引现有记忆（可选）
      if (this.options.enableMemoryIndex && this.options.autoIndexExisting) {
        logger.info('[EnhancedMemorySystem] 开始自动索引现有记忆...');
        // 这里可以添加批量索引逻辑
      }
      
      return true;
      
    } catch (error) {
      logger.error('[EnhancedMemorySystem] Claude-Mem 功能初始化失败:', error);
      throw error;
    }
  }
  
  /**
   * 获取 Claude-Mem 功能
   */
  getClaudeMemFeatures() {
    return {
      memoryEditor: this.memoryEditor,
      privacyManager: this.privacyManager,
      memoryQuality: this.memoryQuality,
      memoryIndex: this.memoryIndex
    };
  }
  
  /**
   * 关闭系统
   */
  async shutdown() {
    logger.info('[EnhancedMemorySystem] 关闭系统...');
    
    // 停止生命周期管理
    if (this.lifecycleManager) {
      this.lifecycleManager.stopAutoManagement();
    }
    
    // 停止队列处理
    if (this.queue) {
      this.queue.stopProcessing();
    }
    
    // 停止管道处理
    if (this.pipeline) {
      this.pipeline.stop();
    }
    
    this.initialized = false;
    
    logger.info('[EnhancedMemorySystem] 系统已关闭');
  }
}

// 导出单例
let systemInstance = null;

export function getEnhancedMemorySystem(options = {}) {
  if (!systemInstance) {
    systemInstance = new EnhancedMemorySystem(options);
  }
  return systemInstance;
}

export default EnhancedMemorySystem;