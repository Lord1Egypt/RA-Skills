/**
 * Memory Lifecycle Manager - 记忆生命周期管理器
 * 
 * 核心目标：自动管理记忆的生命周期，归档旧记忆，清理过期记忆
 */

import { logger } from '../logger.js';

export class MemoryLifecycleManager {
  constructor(options = {}) {
    this.options = {
      // 生命周期配置
      lifecycles: {
        facts: { retention: 9999, archive: 365, priority: 'high' },
        patterns: { retention: 180, archive: 90, priority: 'medium' },
        skills: { retention: 365, archive: 180, priority: 'high' },
        cases: { retention: 365, archive: 180, priority: 'medium' },
        events: { retention: 90, archive: 30, priority: 'low' },
        preferences: { retention: 9999, archive: 365, priority: 'high' },
        general: { retention: 90, archive: 30, priority: 'low' }
      },
      
      // 清理配置
      enableAutoArchive: options.enableAutoArchive !== false,
      enableAutoCleanup: options.enableAutoCleanup !== false,
      archiveInterval: options.archiveInterval || 24 * 60 * 60 * 1000, // 24小时
      cleanupInterval: options.cleanupInterval || 7 * 24 * 60 * 60 * 1000, // 7天
      
      // 归档配置
      archiveThreshold: options.archiveThreshold || 0.3, // 重要性低于此值归档
      keepHighImportance: options.keepHighImportance !== false, // 高重要性记忆永久保留
      
      ...options
    };
    
    // 统计
    this.stats = {
      totalArchived: 0,
      totalCleaned: 0,
      totalKept: 0,
      lastArchiveTime: null,
      lastCleanupTime: null
    };
    
    // 定时器
    this.archiveTimer = null;
    this.cleanupTimer = null;
    
    logger.info('[MemoryLifecycleManager] 生命周期管理器初始化完成');
  }
  
  /**
   * 启动自动管理
   */
  startAutoManagement(storage, vectorStore) {
    logger.info('[MemoryLifecycleManager] 启动自动管理');
    
    // 启动归档定时器
    if (this.options.enableAutoArchive) {
      this.archiveTimer = setInterval(() => {
        this.runArchive(storage, vectorStore);
      }, this.options.archiveInterval);
      
      // 立即执行一次
      this.runArchive(storage, vectorStore);
    }
    
    // 启动清理定时器
    if (this.options.enableAutoCleanup) {
      this.cleanupTimer = setInterval(() => {
        this.runCleanup(storage, vectorStore);
      }, this.options.cleanupInterval);
    }
  }
  
  /**
   * 停止自动管理
   */
  stopAutoManagement() {
    logger.info('[MemoryLifecycleManager] 停止自动管理');
    
    if (this.archiveTimer) {
      clearInterval(this.archiveTimer);
      this.archiveTimer = null;
    }
    
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
  }
  
  /**
   * 执行归档
   */
  async runArchive(storage, vectorStore) {
    logger.info('[MemoryLifecycleManager] 开始归档检查');
    
    const now = Date.now();
    const archived = [];
    const kept = [];
    
    try {
      // 获取所有记忆
      const memories = await storage.list({ limit: 10000 });
      
      for (const memory of memories) {
        const type = memory.type || 'general';
        const lifecycle = this.options.lifecycles[type] || this.options.lifecycles.general;
        
        const age = now - (memory.timestamp || now);
        const daysAge = age / (1000 * 60 * 60 * 24);
        
        // 检查是否需要归档
        const shouldArchive = this.shouldArchive(memory, daysAge, lifecycle);
        
        if (shouldArchive) {
          // 归档记忆
          await this.archiveMemory(memory, storage, vectorStore);
          archived.push(memory.id);
        } else {
          kept.push(memory.id);
        }
      }
      
      // 更新统计
      this.stats.totalArchived += archived.length;
      this.stats.totalKept += kept.length;
      this.stats.lastArchiveTime = now;
      
      logger.info(`[MemoryLifecycleManager] 归档完成: ${archived.length} 条归档, ${kept.length} 条保留`);
      
      return {
        archived: archived.length,
        kept: kept.length,
        memories: archived
      };
      
    } catch (error) {
      logger.error('[MemoryLifecycleManager] 归档失败:', error);
      throw error;
    }
  }
  
  /**
   * 判断是否应该归档
   */
  shouldArchive(memory, daysAge, lifecycle) {
    // 高重要性记忆不归档
    if (this.options.keepHighImportance && memory.importance >= 0.8) {
      return false;
    }
    
    // 检查归档阈值
    if (daysAge < lifecycle.archive) {
      return false;
    }
    
    // 检查重要性
    if (memory.importance < this.options.archiveThreshold) {
      return true;
    }
    
    // 检查访问频率（如果有）
    if (memory.accessCount && memory.accessCount < 2) {
      return true;
    }
    
    return false;
  }
  
  /**
   * 归档单条记忆
   */
  async archiveMemory(memory, storage, vectorStore) {
    try {
      // 标记为已归档
      memory.archived = true;
      memory.archivedAt = Date.now();
      
      // 从主存储移到归档存储
      if (storage.archive) {
        await storage.archive(memory);
      }
      
      // 从向量索引移除（可选）
      if (vectorStore && vectorStore.remove) {
        await vectorStore.remove(memory.id);
      }
      
      logger.debug(`[MemoryLifecycleManager] 已归档: ${memory.id}`);
      
    } catch (error) {
      logger.error(`[MemoryLifecycleManager] 归档失败: ${memory.id}`, error);
      throw error;
    }
  }
  
  /**
   * 执行清理
   */
  async runCleanup(storage, vectorStore) {
    logger.info('[MemoryLifecycleManager] 开始清理检查');
    
    const now = Date.now();
    const cleaned = [];
    
    try {
      // 获取已归档的记忆
      const archivedMemories = await storage.listArchived ? 
        await storage.listArchived({ limit: 10000 }) : [];
      
      for (const memory of archivedMemories) {
        const type = memory.type || 'general';
        const lifecycle = this.options.lifecycles[type] || this.options.lifecycles.general;
        
        const age = now - (memory.timestamp || now);
        const daysAge = age / (1000 * 60 * 60 * 24);
        
        // 检查是否需要清理
        if (daysAge > lifecycle.retention) {
          await this.cleanMemory(memory, storage, vectorStore);
          cleaned.push(memory.id);
        }
      }
      
      // 更新统计
      this.stats.totalCleaned += cleaned.length;
      this.stats.lastCleanupTime = now;
      
      logger.info(`[MemoryLifecycleManager] 清理完成: ${cleaned.length} 条已删除`);
      
      return {
        cleaned: cleaned.length,
        memories: cleaned
      };
      
    } catch (error) {
      logger.error('[MemoryLifecycleManager] 清理失败:', error);
      throw error;
    }
  }
  
  /**
   * 清理单条记忆
   */
  async cleanMemory(memory, storage, vectorStore) {
    try {
      // 从存储删除
      if (storage.delete) {
        await storage.delete(memory.id);
      }
      
      // 从向量索引删除
      if (vectorStore && vectorStore.remove) {
        await vectorStore.remove(memory.id);
      }
      
      logger.debug(`[MemoryLifecycleManager] 已清理: ${memory.id}`);
      
    } catch (error) {
      logger.error(`[MemoryLifecycleManager] 清理失败: ${memory.id}`, error);
      throw error;
    }
  }
  
  /**
   * 手动归档
   */
  async archive(memoryId, storage, vectorStore) {
    const memory = await storage.get(memoryId);
    
    if (!memory) {
      throw new Error(`记忆不存在: ${memoryId}`);
    }
    
    await this.archiveMemory(memory, storage, vectorStore);
    
    this.stats.totalArchived++;
    
    return { archived: true, memoryId };
  }
  
  /**
   * 手动清理
   */
  async clean(memoryId, storage, vectorStore) {
    const memory = await storage.get(memoryId);
    
    if (!memory) {
      throw new Error(`记忆不存在: ${memoryId}`);
    }
    
    await this.cleanMemory(memory, storage, vectorStore);
    
    this.stats.totalCleaned++;
    
    return { cleaned: true, memoryId };
  }
  
  /**
   * 恢复归档记忆
   */
  async restore(memoryId, storage, vectorStore) {
    try {
      const memory = await storage.getArchived ? 
        await storage.getArchived(memoryId) : null;
      
      if (!memory) {
        throw new Error(`归档记忆不存在: ${memoryId}`);
      }
      
      // 恢复记忆
      memory.archived = false;
      memory.restoredAt = Date.now();
      
      // 保存回主存储
      await storage.save(memory);
      
      // 重新索引
      if (vectorStore && vectorStore.add) {
        await vectorStore.add(memory);
      }
      
      logger.info(`[MemoryLifecycleManager] 已恢复: ${memoryId}`);
      
      return { restored: true, memoryId };
      
    } catch (error) {
      logger.error(`[MemoryLifecycleManager] 恢复失败: ${memoryId}`, error);
      throw error;
    }
  }
  
  /**
   * 获取生命周期状态
   */
  getLifecycleStats() {
    return {
      ...this.stats,
      config: this.options.lifecycles,
      autoArchiveEnabled: this.options.enableAutoArchive && this.archiveTimer !== null,
      autoCleanupEnabled: this.options.enableAutoCleanup && this.cleanupTimer !== null
    };
  }
  
  /**
   * 更新生命周期配置
   */
  updateLifecycle(type, config) {
    if (!this.options.lifecycles[type]) {
      this.options.lifecycles[type] = {};
    }
    
    this.options.lifecycles[type] = {
      ...this.options.lifecycles[type],
      ...config
    };
    
    logger.info(`[MemoryLifecycleManager] 更新生命周期配置: ${type}`, config);
    
    return this.options.lifecycles[type];
  }
  
  /**
   * 预览归档
   */
  async previewArchive(storage) {
    const now = Date.now();
    const preview = {
      toArchive: [],
      toKeep: [],
      stats: {
        total: 0,
        archive: 0,
        keep: 0
      }
    };
    
    try {
      const memories = await storage.list({ limit: 10000 });
      preview.stats.total = memories.length;
      
      for (const memory of memories) {
        const type = memory.type || 'general';
        const lifecycle = this.options.lifecycles[type] || this.options.lifecycles.general;
        
        const age = now - (memory.timestamp || now);
        const daysAge = age / (1000 * 60 * 60 * 24);
        
        const shouldArchive = this.shouldArchive(memory, daysAge, lifecycle);
        
        if (shouldArchive) {
          preview.toArchive.push({
            id: memory.id,
            type: type,
            daysAge: Math.floor(daysAge),
            importance: memory.importance
          });
          preview.stats.archive++;
        } else {
          preview.toKeep.push(memory.id);
          preview.stats.keep++;
        }
      }
      
      return preview;
      
    } catch (error) {
      logger.error('[MemoryLifecycleManager] 预览归档失败:', error);
      throw error;
    }
  }
}

// 导出单例
let lifecycleInstance = null;

export function getMemoryLifecycleManager(options = {}) {
  if (!lifecycleInstance) {
    lifecycleInstance = new MemoryLifecycleManager(options);
  }
  return lifecycleInstance;
}

export default MemoryLifecycleManager;
