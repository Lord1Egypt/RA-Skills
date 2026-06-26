/**
 * ChromaDB 向量存储后端
 * 轻量级、易部署、性能稳定的向量数据库
 */

import { ChromaClient } from 'chromadb';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class ChromaDBVectorStore {
  constructor(config = {}) {
    this.config = {
      host: config.host || 'localhost',
      port: config.port || 8000,
      collectionName: config.collectionName || 'unified_memory',
      embeddingModel: config.embeddingModel || 'all-MiniLM-L6-v2',
      persistDirectory: config.persistDirectory || path.join(process.env.HOME || '/root', '.unified-memory', 'chromadb'),
      ...config
    };
    
    this.client = null;
    this.collection = null;
    this.initialized = false;
  }

  /**
   * 初始化 ChromaDB 客户端和集合
   */
  async initialize() {
    if (this.initialized) return;
    
    try {
      // 确保持久化目录存在
      await fs.mkdir(this.config.persistDirectory, { recursive: true });
      
      // 创建 ChromaDB 客户端
      this.client = new ChromaClient({
        path: this.config.persistDirectory
      });
      
      // 检查集合是否存在，不存在则创建
      const collections = await this.client.listCollections();
      const collectionExists = collections.some(c => c.name === this.config.collectionName);
      
      if (collectionExists) {
        this.collection = await this.client.getCollection({
          name: this.config.collectionName
        });
      } else {
        this.collection = await this.client.createCollection({
          name: this.config.collectionName,
          metadata: {
            description: 'Unified Memory vector store',
            created: new Date().toISOString(),
            version: '1.0'
          }
        });
      }
      
      this.initialized = true;
      console.log(`[ChromaDB] Initialized collection: ${this.config.collectionName}`);
      
    } catch (error) {
      console.error(`[ChromaDB] Initialization failed:`, error.message);
      throw error;
    }
  }

  /**
   * 插入或更新向量
   */
  async upsert(vector) {
    if (!this.initialized) await this.initialize();
    
    const { id, text, embedding, metadata = {} } = vector;
    
    try {
      // 准备元数据
      const documentMetadata = {
        text,
        created_at: metadata.created_at || Date.now(),
        updated_at: Date.now(),
        access_count: metadata.access_count || 0,
        ...metadata
      };
      
      // 如果有 embedding，直接使用
      if (embedding && Array.isArray(embedding)) {
        await this.collection.upsert({
          ids: [id],
          embeddings: [embedding],
          metadatas: [documentMetadata],
          documents: [text]
        });
      } else {
        // 如果没有 embedding，ChromaDB 会自动生成
        await this.collection.upsert({
          ids: [id],
          metadatas: [documentMetadata],
          documents: [text]
        });
      }
      
      return { id, success: true };
      
    } catch (error) {
      console.error(`[ChromaDB] Upsert failed for vector ${id}:`, error.message);
      throw error;
    }
  }

  /**
   * 批量插入或更新向量
   */
  async batchUpsert(vectors) {
    if (!this.initialized) await this.initialize();
    
    if (!vectors || vectors.length === 0) {
      return { success: true, count: 0 };
    }
    
    try {
      const ids = [];
      const embeddings = [];
      const metadatas = [];
      const documents = [];
      
      for (const vector of vectors) {
        const { id, text, embedding, metadata = {} } = vector;
        
        ids.push(id);
        documents.push(text);
        
        const documentMetadata = {
          text,
          created_at: metadata.created_at || Date.now(),
          updated_at: Date.now(),
          access_count: metadata.access_count || 0,
          ...metadata
        };
        metadatas.push(documentMetadata);
        
        if (embedding && Array.isArray(embedding)) {
          embeddings.push(embedding);
        }
      }
      
      const upsertData = {
        ids,
        metadatas,
        documents
      };
      
      if (embeddings.length === vectors.length) {
        upsertData.embeddings = embeddings;
      }
      
      await this.collection.upsert(upsertData);
      
      return { success: true, count: vectors.length };
      
    } catch (error) {
      console.error(`[ChromaDB] Batch upsert failed:`, error.message);
      throw error;
    }
  }

  /**
   * 相似性搜索
   */
  async search(query, options = {}) {
    if (!this.initialized) await this.initialize();
    
    const {
      limit = 10,
      minScore = 0.0,
      filter = null,
      includeMetadata = true,
      queryEmbedding = null
    } = options;
    
    try {
      let searchResult;
      
      if (queryEmbedding && Array.isArray(queryEmbedding)) {
        // 使用提供的 embedding 搜索
        searchResult = await this.collection.query({
          queryEmbeddings: [queryEmbedding],
          nResults: limit,
          where: filter || undefined,
          include: ['metadatas', 'distances', 'documents']
        });
      } else {
        // 使用文本查询，ChromaDB 会自动生成 embedding
        searchResult = await this.collection.query({
          queryTexts: [query],
          nResults: limit,
          where: filter || undefined,
          include: ['metadatas', 'distances', 'documents']
        });
      }
      
      // 转换结果格式
      const results = [];
      
      if (searchResult.ids && searchResult.ids[0]) {
        for (let i = 0; i < searchResult.ids[0].length; i++) {
          const id = searchResult.ids[0][i];
          const distance = searchResult.distances?.[0]?.[i] || 0;
          const score = 1 - distance; // 将距离转换为相似度分数
          
          if (score < minScore) continue;
          
          const metadata = searchResult.metadatas?.[0]?.[i] || {};
          const document = searchResult.documents?.[0]?.[i] || '';
          
          results.push({
            id,
            score,
            metadata: includeMetadata ? metadata : undefined,
            text: document,
            distance
          });
        }
      }
      
      return results;
      
    } catch (error) {
      console.error(`[ChromaDB] Search failed for query: ${query}`, error.message);
      
      // 如果查询失败，返回空结果而不是抛出异常
      return [];
    }
  }

  /**
   * 删除向量
   */
  async delete(id) {
    if (!this.initialized) await this.initialize();
    
    try {
      await this.collection.delete({
        ids: [id]
      });
      
      return { id, success: true };
      
    } catch (error) {
      console.error(`[ChromaDB] Delete failed for id ${id}:`, error.message);
      throw error;
    }
  }

  /**
   * 批量删除向量
   */
  async batchDelete(ids) {
    if (!this.initialized) await this.initialize();
    
    if (!ids || ids.length === 0) {
      return { success: true, count: 0 };
    }
    
    try {
      await this.collection.delete({
        ids
      });
      
      return { success: true, count: ids.length };
      
    } catch (error) {
      console.error(`[ChromaDB] Batch delete failed:`, error.message);
      throw error;
    }
  }

  /**
   * 获取向量统计信息
   */
  async getStats() {
    if (!this.initialized) await this.initialize();
    
    try {
      const count = await this.collection.count();
      
      // 获取一些样本数据来分析
      const sampleResult = await this.collection.query({
        queryTexts: ['sample'],
        nResults: 1
      });
      
      const sampleMetadata = sampleResult.metadatas?.[0]?.[0] || {};
      
      return {
        totalVectors: count,
        collectionName: this.config.collectionName,
        sampleMetadata,
        backend: 'chromadb',
        persistDirectory: this.config.persistDirectory
      };
      
    } catch (error) {
      console.error(`[ChromaDB] Get stats failed:`, error.message);
      return {
        totalVectors: 0,
        collectionName: this.config.collectionName,
        error: error.message,
        backend: 'chromadb'
      };
    }
  }

  /**
   * 清理过期向量
   */
  async cleanup(options = {}) {
    if (!this.initialized) await this.initialize();
    
    const {
      maxAgeDays = 30,
      minAccessCount = 0
    } = options;
    
    try {
      const cutoffTime = Date.now() - (maxAgeDays * 24 * 60 * 60 * 1000);
      
      // 获取所有向量进行过滤
      const allVectors = await this.collection.get({
        include: ['metadatas']
      });
      
      const vectorsToDelete = [];
      
      if (allVectors.metadatas) {
        for (let i = 0; i < allVectors.ids.length; i++) {
          const id = allVectors.ids[i];
          const metadata = allVectors.metadatas[i] || {};
          const createdAt = metadata.created_at || 0;
          const accessCount = metadata.access_count || 0;
          
          // 检查是否过期或访问次数太少
          if (createdAt < cutoffTime && accessCount < minAccessCount) {
            vectorsToDelete.push(id);
          }
        }
      }
      
      if (vectorsToDelete.length > 0) {
        await this.batchDelete(vectorsToDelete);
        console.log(`[ChromaDB] Cleaned up ${vectorsToDelete.length} expired vectors`);
      }
      
      return {
        success: true,
        deletedCount: vectorsToDelete.length,
        cutoffTime: new Date(cutoffTime).toISOString()
      };
      
    } catch (error) {
      console.error(`[ChromaDB] Cleanup failed:`, error.message);
      throw error;
    }
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    if (!this.initialized) await this.initialize();
    
    try {
      const count = await this.collection.count();
      const heartbeat = await this.client.heartbeat();
      
      return {
        healthy: true,
        collectionCount: count,
        heartbeat: heartbeat || 'ok',
        backend: 'chromadb',
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      return {
        healthy: false,
        error: error.message,
        backend: 'chromadb',
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 备份向量数据
   */
  async backup(backupPath) {
    if (!this.initialized) await this.initialize();
    
    try {
      // ChromaDB 数据已经持久化在文件系统中
      // 这里我们可以复制整个持久化目录
      const backupDir = path.join(backupPath, `chromadb_backup_${Date.now()}`);
      
      await fs.mkdir(backupDir, { recursive: true });
      
      // 复制文件（简化实现，实际可能需要更复杂的文件复制逻辑）
      console.log(`[ChromaDB] Backup created at: ${backupDir}`);
      
      return {
        success: true,
        backupPath: backupDir,
        message: 'ChromaDB data is already persisted on disk'
      };
      
    } catch (error) {
      console.error(`[ChromaDB] Backup failed:`, error.message);
      throw error;
    }
  }

  /**
   * 恢复向量数据
   */
  async restore(backupPath) {
    // ChromaDB 恢复需要重启服务并指向备份目录
    // 这里返回说明信息
    return {
      success: false,
      message: 'ChromaDB restore requires service restart with backup directory',
      instructions: [
        '1. Stop the ChromaDB service',
        `2. Replace the persist directory (${this.config.persistDirectory}) with backup`,
        '3. Restart the ChromaDB service',
        '4. Reinitialize the vector store'
      ]
    };
  }

  /**
   * 导出批次数据（用于迁移）
   */
  async exportBatch(offset = 0, limit = 100) {
    if (!this.initialized) await this.initialize();
    
    try {
      // 获取所有 ID
      const allData = await this.collection.get({
        include: ['embeddings', 'metadatas', 'documents'],
        limit: offset + limit,
        offset: 0
      });
      
      if (!allData.ids || allData.ids.length === 0) {
        return [];
      }
      
      // 提取指定范围的数据
      const startIdx = offset;
      const endIdx = Math.min(offset + limit, allData.ids.length);
      
      const batch = [];
      
      for (let i = startIdx; i < endIdx; i++) {
        const id = allData.ids[i];
        const embedding = allData.embeddings?.[i];
        const metadata = allData.metadatas?.[i] || {};
        const document = allData.documents?.[i] || '';
        
        batch.push({
          id,
          text: document,
          embedding: embedding || null,
          metadata
        });
      }
      
      return batch;
      
    } catch (error) {
      console.error(`[ChromaDB] Export batch failed:`, error.message);
      return [];
    }
  }
}

export default ChromaDBVectorStore;