/**
 * 向量存储抽象层 - 支持多种向量数据库后端
 * 解决 LanceDB WHERE 子句损坏问题，提供可迁移架构
 */

export class VectorStore {
  constructor(config) {
    this.config = config;
    this.backend = null;
    this.initialized = false;
  }

  /**
   * 初始化向量存储
   */
  async initialize() {
    if (this.initialized) return;
    
    const backendType = this.config.backend || 'lancedb';
    
    try {
      switch (backendType) {
        case 'lancedb':
          const { LanceDBVectorStore } = await import('./vector-lancedb-backend.js');
          this.backend = new LanceDBVectorStore(this.config);
          break;
          
        case 'chromadb':
          const { ChromaDBVectorStore } = await import('./vector-chromadb-backend.js');
          this.backend = new ChromaDBVectorStore(this.config);
          break;
          
        case 'qdrant':
          const { QdrantVectorStore } = await import('./vector-qdrant-backend.js');
          this.backend = new QdrantVectorStore(this.config);
          break;
          
        case 'weaviate':
          const { WeaviateVectorStore } = await import('./vector-weaviate-backend.js');
          this.backend = new WeaviateVectorStore(this.config);
          break;
          
        default:
          throw new Error(`Unsupported vector backend: ${backendType}`);
      }
      
      await this.backend.initialize();
      this.initialized = true;
      
      console.log(`[VectorStore] Initialized with backend: ${backendType}`);
      
    } catch (error) {
      console.error(`[VectorStore] Failed to initialize backend ${backendType}:`, error.message);
      throw error;
    }
  }

  /**
   * 插入或更新向量
   */
  async upsert(vector) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.upsert(vector);
    } catch (error) {
      console.error(`[VectorStore] Upsert failed for vector ${vector.id}:`, error.message);
      throw error;
    }
  }

  /**
   * 批量插入或更新向量
   */
  async batchUpsert(vectors) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.batchUpsert(vectors);
    } catch (error) {
      console.error(`[VectorStore] Batch upsert failed:`, error.message);
      throw error;
    }
  }

  /**
   * 相似性搜索
   */
  async search(query, options = {}) {
    if (!this.initialized) await this.initialize();
    
    const defaultOptions = {
      limit: 10,
      minScore: 0.0,
      filter: null,
      includeMetadata: true
    };
    
    const searchOptions = { ...defaultOptions, ...options };
    
    try {
      return await this.backend.search(query, searchOptions);
    } catch (error) {
      console.error(`[VectorStore] Search failed for query: ${query}`, error.message);
      throw error;
    }
  }

  /**
   * 删除向量
   */
  async delete(id) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.delete(id);
    } catch (error) {
      console.error(`[VectorStore] Delete failed for id ${id}:`, error.message);
      throw error;
    }
  }

  /**
   * 批量删除向量
   */
  async batchDelete(ids) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.batchDelete(ids);
    } catch (error) {
      console.error(`[VectorStore] Batch delete failed:`, error.message);
      throw error;
    }
  }

  /**
   * 获取向量统计信息
   */
  async getStats() {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.getStats();
    } catch (error) {
      console.error(`[VectorStore] Get stats failed:`, error.message);
      throw error;
    }
  }

  /**
   * 清理过期向量
   */
  async cleanup(options = {}) {
    if (!this.initialized) await this.initialize();
    
    const defaultOptions = {
      maxAgeDays: 30,
      minAccessCount: 0
    };
    
    const cleanupOptions = { ...defaultOptions, ...options };
    
    try {
      return await this.backend.cleanup(cleanupOptions);
    } catch (error) {
      console.error(`[VectorStore] Cleanup failed:`, error.message);
      throw error;
    }
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.healthCheck();
    } catch (error) {
      console.error(`[VectorStore] Health check failed:`, error.message);
      return { healthy: false, error: error.message };
    }
  }

  /**
   * 备份向量数据
   */
  async backup(backupPath) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.backup(backupPath);
    } catch (error) {
      console.error(`[VectorStore] Backup failed:`, error.message);
      throw error;
    }
  }

  /**
   * 恢复向量数据
   */
  async restore(backupPath) {
    if (!this.initialized) await this.initialize();
    
    try {
      return await this.backend.restore(backupPath);
    } catch (error) {
      console.error(`[VectorStore] Restore failed:`, error.message);
      throw error;
    }
  }

  /**
   * 迁移到另一个后端
   */
  async migrateTo(targetBackend, targetConfig) {
    if (!this.initialized) await this.initialize();
    
    console.log(`[VectorStore] Starting migration from ${this.config.backend} to ${targetBackend}`);
    
    try {
      // 1. 创建目标后端实例
      let targetStore;
      switch (targetBackend) {
        case 'chromadb':
          const { ChromaDBVectorStore } = await import('./vector-chromadb-backend.js');
          targetStore = new ChromaDBVectorStore(targetConfig);
          break;
          
        case 'qdrant':
          const { QdrantVectorStore } = await import('./vector-qdrant-backend.js');
          targetStore = new QdrantVectorStore(targetConfig);
          break;
          
        case 'weaviate':
          const { WeaviateVectorStore } = await import('./vector-weaviate-backend.js');
          targetStore = new WeaviateVectorStore(targetConfig);
          break;
          
        default:
          throw new Error(`Unsupported target backend: ${targetBackend}`);
      }
      
      await targetStore.initialize();
      
      // 2. 分批导出和导入数据
      const batchSize = 100;
      let totalMigrated = 0;
      let offset = 0;
      
      while (true) {
        // 从源后端获取一批数据
        const batch = await this.backend.exportBatch(offset, batchSize);
        
        if (!batch || batch.length === 0) {
          break;
        }
        
        // 导入到目标后端
        await targetStore.batchUpsert(batch);
        
        totalMigrated += batch.length;
        offset += batchSize;
        
        console.log(`[VectorStore] Migrated ${totalMigrated} vectors...`);
        
        // 小延迟避免过载
        if (batch.length === batchSize) {
          await new Promise(resolve => setTimeout(resolve, 100));
        }
      }
      
      console.log(`[VectorStore] Migration completed: ${totalMigrated} vectors migrated`);
      
      // 3. 验证数据一致性
      const sourceStats = await this.getStats();
      const targetStats = await targetStore.getStats();
      
      if (sourceStats.totalVectors !== targetStats.totalVectors) {
        throw new Error(`Data inconsistency: source has ${sourceStats.totalVectors}, target has ${targetStats.totalVectors}`);
      }
      
      // 4. 更新配置（实际应用中需要持久化新配置）
      this.config.backend = targetBackend;
      this.config = { ...this.config, ...targetConfig };
      this.backend = targetStore;
      
      console.log(`[VectorStore] Successfully migrated to ${targetBackend}`);
      
      return {
        success: true,
        totalMigrated,
        sourceStats,
        targetStats
      };
      
    } catch (error) {
      console.error(`[VectorStore] Migration failed:`, error.message);
      throw error;
    }
  }

  /**
   * 获取当前后端类型
   */
  getBackendType() {
    return this.config.backend || 'lancedb';
  }

  /**
   * 获取支持的迁移目标
   */
  getSupportedMigrationTargets() {
    const current = this.getBackendType();
    const allBackends = ['lancedb', 'chromadb', 'qdrant', 'weaviate'];
    return allBackends.filter(backend => backend !== current);
  }
}

// 单例实例
let _instance = null;

export function getVectorStore(config = {}) {
  if (!_instance) {
    _instance = new VectorStore(config);
  }
  return _instance;
}

export default VectorStore;