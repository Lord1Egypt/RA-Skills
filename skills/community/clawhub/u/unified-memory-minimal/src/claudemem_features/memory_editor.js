/**
 * 记忆编辑系统 - Claude-Mem 风格
 * 
 * 功能：
 * 1. 查看所有记忆
 * 2. 编辑、删除、修改记忆
 * 3. 标记记忆为重要/不重要
 * 4. 合并相似记忆
 * 5. 批量操作
 */

import { logger } from '../utils/logger.js';

export class MemoryEditor {
  constructor(storage, vectorStore) {
    this.storage = storage;
    this.vectorStore = vectorStore;
    this.logger = logger.child({ module: 'memory_editor' });
  }

  /**
   * 列出用户的所有记忆
   * @param {string} userId - 用户 ID
   * @param {Object} options - 选项
   * @param {number} options.limit - 限制数量
   * @param {number} options.offset - 偏移量
   * @param {string} options.category - 分类过滤
   * @param {string} options.search - 搜索关键词
   * @param {boolean} options.importantOnly - 仅重要记忆
   * @returns {Promise<Array>} 记忆列表
   */
  async listMemories(userId, options = {}) {
    const {
      limit = 50,
      offset = 0,
      category = null,
      search = null,
      importantOnly = false,
      sortBy = 'createdAt',
      sortOrder = 'desc'
    } = options;

    try {
      // 构建查询条件
      const conditions = { userId };
      
      if (category) {
        conditions.category = category;
      }
      
      if (importantOnly) {
        conditions.important = true;
      }
      
      // 搜索关键词
      let memories = [];
      if (search) {
        // 使用向量搜索
        const searchResults = await this.vectorStore.search(search, {
          userId,
          limit: 100, // 搜索更多结果
          filter: category ? { category } : undefined
        });
        
        const memoryIds = searchResults.map(r => r.memoryId);
        if (memoryIds.length > 0) {
          conditions._id = { $in: memoryIds };
        }
      }
      
      // 查询记忆
      memories = await this.storage.find('memories', conditions, {
        limit,
        skip: offset,
        sort: { [sortBy]: sortOrder === 'desc' ? -1 : 1 }
      });
      
      // 添加元数据
      const enhancedMemories = await Promise.all(
        memories.map(async (memory) => {
          const usage = await this.getMemoryUsage(memory._id);
          return {
            ...memory,
            usageCount: usage.totalUses,
            lastUsed: usage.lastUsed,
            successRate: usage.successRate,
            qualityScore: await this.calculateQualityScore(memory)
          };
        })
      );
      
      // 如果搜索关键词，按相关性排序
      if (search) {
        enhancedMemories.sort((a, b) => {
          const aScore = a.relevanceScore || 0;
          const bScore = b.relevanceScore || 0;
          return bScore - aScore;
        });
      }
      
      this.logger.info('Listed memories', { 
        userId, 
        count: enhancedMemories.length,
        options 
      });
      
      return enhancedMemories;
      
    } catch (error) {
      this.logger.error('Failed to list memories', { error, userId, options });
      throw error;
    }
  }

  /**
   * 获取记忆详情
   * @param {string} memoryId - 记忆 ID
   * @returns {Promise<Object>} 记忆详情
   */
  async getMemory(memoryId) {
    try {
      const memory = await this.storage.findOne('memories', { _id: memoryId });
      
      if (!memory) {
        throw new Error(`Memory not found: ${memoryId}`);
      }
      
      // 获取使用统计
      const usage = await this.getMemoryUsage(memoryId);
      const qualityScore = await this.calculateQualityScore(memory);
      
      // 获取相关记忆
      const related = await this.getRelatedMemories(memoryId);
      
      return {
        ...memory,
        usage,
        qualityScore,
        relatedMemories: related
      };
      
    } catch (error) {
      this.logger.error('Failed to get memory', { error, memoryId });
      throw error;
    }
  }

  /**
   * 编辑记忆
   * @param {string} memoryId - 记忆 ID
   * @param {Object} updates - 更新内容
   * @param {string} updates.content - 新内容
   * @param {string} updates.category - 新分类
   * @param {Array} updates.tags - 新标签
   * @param {boolean} updates.important - 是否重要
   * @returns {Promise<Object>} 更新后的记忆
   */
  async editMemory(memoryId, updates) {
    try {
      const memory = await this.storage.findOne('memories', { _id: memoryId });
      
      if (!memory) {
        throw new Error(`Memory not found: ${memoryId}`);
      }
      
      // 验证更新字段
      const allowedFields = ['content', 'summary', 'category', 'tags', 'important', 'metadata'];
      const validUpdates = {};
      
      for (const [key, value] of Object.entries(updates)) {
        if (allowedFields.includes(key)) {
          validUpdates[key] = value;
        }
      }
      
      // 添加更新时间
      validUpdates.updatedAt = new Date();
      
      // 更新记忆
      const updatedMemory = await this.storage.updateOne(
        'memories',
        { _id: memoryId },
        { $set: validUpdates }
      );
      
      // 如果内容改变，更新向量存储
      if (updates.content && updates.content !== memory.content) {
        await this.vectorStore.update(memoryId, {
          text: updates.content,
          metadata: {
            ...memory.metadata,
            ...(updates.metadata || {}),
            updatedAt: new Date()
          }
        });
      }
      
      this.logger.info('Memory edited', { memoryId, updates: Object.keys(updates) });
      
      return updatedMemory;
      
    } catch (error) {
      this.logger.error('Failed to edit memory', { error, memoryId, updates });
      throw error;
    }
  }

  /**
   * 删除记忆
   * @param {string} memoryId - 记忆 ID
   * @returns {Promise<boolean>} 是否成功
   */
  async deleteMemory(memoryId) {
    try {
      // 检查记忆是否存在
      const memory = await this.storage.findOne('memories', { _id: memoryId });
      
      if (!memory) {
        throw new Error(`Memory not found: ${memoryId}`);
      }
      
      // 从向量存储中删除
      await this.vectorStore.delete(memoryId);
      
      // 从关系存储中删除
      await this.storage.deleteMany('memory_relations', {
        $or: [
          { sourceMemoryId: memoryId },
          { targetMemoryId: memoryId }
        ]
      });
      
      // 从主存储中删除
      await this.storage.deleteOne('memories', { _id: memoryId });
      
      // 删除使用记录
      await this.storage.deleteMany('memory_usage', { memoryId });
      
      this.logger.info('Memory deleted', { memoryId, userId: memory.userId });
      
      return true;
      
    } catch (error) {
      this.logger.error('Failed to delete memory', { error, memoryId });
      throw error;
    }
  }

  /**
   * 合并相似记忆
   * @param {Array<string>} memoryIds - 要合并的记忆 ID 列表
   * @param {Object} options - 选项
   * @param {string} options.strategy - 合并策略: 'merge', 'keep_latest', 'keep_most_used'
   * @returns {Promise<Object>} 合并结果
   */
  async mergeMemories(memoryIds, options = {}) {
    const { strategy = 'merge' } = options;
    
    try {
      // 获取所有记忆
      const memories = await this.storage.find('memories', {
        _id: { $in: memoryIds }
      });
      
      if (memories.length < 2) {
        throw new Error('Need at least 2 memories to merge');
      }
      
      // 检查是否属于同一用户
      const userIds = [...new Set(memories.map(m => m.userId))];
      if (userIds.length > 1) {
        throw new Error('Cannot merge memories from different users');
      }
      
      const userId = userIds[0];
      
      // 根据策略选择主记忆
      let mainMemory;
      const otherMemories = [];
      
      switch (strategy) {
        case 'keep_latest':
          memories.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
          mainMemory = memories[0];
          otherMemories.push(...memories.slice(1));
          break;
          
        case 'keep_most_used':
          const usageStats = await Promise.all(
            memories.map(async (m) => ({
              memory: m,
              usage: await this.getMemoryUsage(m._id)
            }))
          );
          usageStats.sort((a, b) => b.usage.totalUses - a.usage.totalUses);
          mainMemory = usageStats[0].memory;
          otherMemories.push(...usageStats.slice(1).map(s => s.memory));
          break;
          
        case 'merge':
        default:
          // 选择内容最长的作为主记忆
          memories.sort((a, b) => b.content.length - a.content.length);
          mainMemory = memories[0];
          otherMemories.push(...memories.slice(1));
          break;
      }
      
      // 合并内容
      const mergedContent = await this.mergeContent(
        mainMemory.content,
        otherMemories.map(m => m.content)
      );
      
      // 合并元数据
      const mergedMetadata = {
        ...mainMemory.metadata,
        mergedFrom: memoryIds,
        mergedAt: new Date(),
        originalCategories: memories.map(m => m.category),
        originalTags: [...new Set(memories.flatMap(m => m.tags || []))]
      };
      
      // 更新主记忆
      const updatedMemory = await this.editMemory(mainMemory._id, {
        content: mergedContent,
        metadata: mergedMetadata,
        tags: mergedMetadata.originalTags,
        important: memories.some(m => m.important) // 如果任意一个重要，则合并后重要
      });
      
      // 删除其他记忆
      for (const memory of otherMemories) {
        await this.deleteMemory(memory._id);
      }
      
      this.logger.info('Memories merged', {
        memoryIds,
        mainMemoryId: mainMemory._id,
        strategy,
        mergedCount: memories.length
      });
      
      return {
        success: true,
        mainMemoryId: mainMemory._id,
        mergedCount: memories.length,
        deletedMemoryIds: otherMemories.map(m => m._id),
        memory: updatedMemory
      };
      
    } catch (error) {
      this.logger.error('Failed to merge memories', { error, memoryIds, strategy });
      throw error;
    }
  }

  /**
   * 标记记忆为重要/不重要
   * @param {string} memoryId - 记忆 ID
   * @param {boolean} important - 是否重要
   * @returns {Promise<Object>} 更新后的记忆
   */
  async markImportant(memoryId, important = true) {
    return this.editMemory(memoryId, { important });
  }

  /**
   * 批量操作
   * @param {Array<string>} memoryIds - 记忆 ID 列表
   * @param {string} action - 操作: 'delete', 'mark_important', 'mark_unimportant', 'change_category'
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 批量操作结果
   */
  async batchOperation(memoryIds, action, options = {}) {
    try {
      const results = {
        success: [],
        failed: []
      };
      
      for (const memoryId of memoryIds) {
        try {
          let result;
          
          switch (action) {
            case 'delete':
              await this.deleteMemory(memoryId);
              result = { memoryId, action: 'deleted' };
              break;
              
            case 'mark_important':
              result = await this.markImportant(memoryId, true);
              break;
              
            case 'mark_unimportant':
              result = await this.markImportant(memoryId, false);
              break;
              
            case 'change_category':
              result = await this.editMemory(memoryId, { category: options.category });
              break;
              
            case 'add_tag':
              const memory = await this.getMemory(memoryId);
              const newTags = [...new Set([...(memory.tags || []), ...(options.tags || [])])];
              result = await this.editMemory(memoryId, { tags: newTags });
              break;
              
            default:
              throw new Error(`Unknown action: ${action}`);
          }
          
          results.success.push({ memoryId, result });
          
        } catch (error) {
          results.failed.push({ memoryId, error: error.message });
        }
      }
      
      this.logger.info('Batch operation completed', {
        action,
        total: memoryIds.length,
        success: results.success.length,
        failed: results.failed.length
      });
      
      return results;
      
    } catch (error) {
      this.logger.error('Batch operation failed', { error, memoryIds, action, options });
      throw error;
    }
  }

  /**
   * 获取记忆使用统计
   * @param {string} memoryId - 记忆 ID
   * @returns {Promise<Object>} 使用统计
   */
  async getMemoryUsage(memoryId) {
    try {
      const usageRecords = await this.storage.find('memory_usage', { memoryId });
      
      const totalUses = usageRecords.length;
      const successfulUses = usageRecords.filter(r => r.success).length;
      const successRate = totalUses > 0 ? successfulUses / totalUses : 0;
      const lastUsed = usageRecords.length > 0 
        ? Math.max(...usageRecords.map(r => r.timestamp))
        : null;
      
      return {
        totalUses,
        successfulUses,
        successRate,
        lastUsed,
        usageRecords: usageRecords.slice(0, 10) // 返回最近10条记录
      };
      
    } catch (error) {
      this.logger.error('Failed to get memory usage', { error, memoryId });
      return {
        totalUses: 0,
        successfulUses: 0,
        successRate: 0,
        lastUsed: null,
        usageRecords: []
      };
    }
  }

  /**
   * 计算记忆质量分数
   * @param {Object} memory - 记忆对象
   * @returns {Promise<number>} 质量分数 0-100
   */
  async calculateQualityScore(memory) {
    try {
      let score = 50; // 基础分
      
      // 内容长度加分
      if (memory.content && memory.content.length > 100) {
        score += Math.min(20, memory.content.length / 50);
      }
      
      // 摘要存在加分
      if (memory.summary && memory.summary.length > 20) {
        score += 10;
      }
      
      // 分类明确加分
      if (memory.category && memory.category !== 'unknown') {
        score += 5;
      }
      
      // 标签数量加分
      if (memory.tags && memory.tags.length > 0) {
        score += Math.min(10, memory.tags.length * 2);
      }
      
      // 使用频率加分
      const usage = await this.getMemoryUsage(memory._id);
      if (usage.totalUses > 0) {
        score += Math.min(15, usage.totalUses * 3);
        score += Math.min(10, usage.successRate * 10);
      }
      
      // 重要标记加分
      if (memory.important) {
        score += 10;
      }
      
      return Math.min(100, Math.max(0, Math.round(score)));
      
    } catch (error) {
      this.logger.error('Failed to calculate quality score', { error, memoryId: memory._id });
      return 50; // 默认分数
    }
  }

  /**
   * 获取相关记忆
   * @param {string} memoryId - 记忆 ID
   * @param {number} limit - 限制数量
   * @returns {Promise<Array>} 相关记忆
   */
  async getRelatedMemories(memoryId, limit = 5) {
    try {
      const memory = await this.getMemory(memoryId);
      
      // 向量搜索相似记忆
      const similar = await this.vectorStore.search(memory.content, {
        userId: memory.userId,
        limit: limit + 1, // 多查一个，排除自己
        minScore: 0.7
      });
      
      // 过滤掉自己
      const related = similar
        .filter(r => r.memoryId !== memoryId)
        .slice(0, limit)
        .map(r => ({
          memoryId: r.memoryId,
          score: r.score,
          content: r.text?.substring(0, 100) + '...'
        }));
      
      return related;
      
    } catch (error) {
      this.logger.error('Failed to get related memories', { error, memoryId });
      return [];
    }
  }

  /**
   * 合并内容（使用 LLM）
   * @param {string} mainContent - 主内容
   * @param {Array<string>} otherContents - 其他内容
   * @returns {Promise<string>} 合并后的内容
   */
  async mergeContent(mainContent, otherContents) {
    // 简单实现：连接所有内容
    // 实际应该使用 LLM 智能合并
    const allContents = [mainContent, ...otherContents];
    return allContents.join('\n\n---\n\n');
  }
}

export default MemoryEditor;