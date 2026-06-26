/**
 * Memory V2 - 记忆管理模块
 * 负责记忆优先级评分、自动遗忘、压缩归档
 */

import { EventEmitter } from 'events';

/**
 * 记忆管理器类
 */
export class MemoryManager extends EventEmitter {
  /**
   * @param {Object} config
   * @param {VectorStore} config.vectorStore - 向量存储实例
   * @param {GraphStore} config.graphStore - 图存储实例
   * @param {Object} config.llm - LLM 接口（用于摘要）
   * @param {number} config.forgetThreshold - 遗忘阈值
   */
  constructor(config = {}) {
    super();
    this.vectorStore = config.vectorStore;
    this.graphStore = config.graphStore;
    this.llm = config.llm;
    this.forgetThreshold = config.forgetThreshold || 0.2;
    
    // 访问计数
    this.accessCounts = new Map();
  }

  /**
   * 计算记忆优先级评分
   * @param {Object} memory - 记忆对象
   * @returns {number} - 优先级评分（0-1）
   */
  calculateScore(memory) {
    const metadata = memory.metadata || {};
    const createdAt = new Date(metadata.createdAt || Date.now());
    const daysSinceCreated = (Date.now() - createdAt.getTime()) / (1000 * 60 * 60 * 24);
    
    // 1. 时间衰减（指数衰减）
    const halfLife = 30; // 半衰期 30 天
    const recency = Math.exp(-Math.log(2) * daysSinceCreated / halfLife);
    
    // 2. 访问频率
    const accessCount = this.accessCounts.get(memory.id) || 0;
    const maxAccessCount = Math.max(...this.accessCounts.values(), 1);
    const frequency = accessCount / maxAccessCount;
    
    // 3. 重要性标记
    const importance = metadata.importance || 0.5;
    
    // 加权评分
    const score = 0.4 * recency + 0.3 * frequency + 0.3 * importance;
    
    return Math.max(0, Math.min(1, score));
  }

  /**
   * 记录访问
   * @param {string} memoryId - 记忆 ID
   */
  recordAccess(memoryId) {
    const count = this.accessCounts.get(memoryId) || 0;
    this.accessCounts.set(memoryId, count + 1);
  }

  /**
   * 自动遗忘低优先级记忆
   * @returns {Promise<Object>} - 遗忘统计
   */
  async forgetLowPriorityMemories() {
    this.emit('forgetting-started');
    
    const stats = {
      totalMemories: 0,
      compressed: 0,
      archived: 0
    };
    
    // 获取所有记忆
    const allMemories = await this.vectorStore.search('', 10000); // 搜索所有
    stats.totalMemories = allMemories.length;
    
    const lowPriority = allMemories.filter(memory => 
      this.calculateScore(memory) < this.forgetThreshold
    );
    
    console.log(`[MemoryManager] Found ${lowPriority.length} low-priority memories`);
    
    // 压缩并归档
    for (const memory of lowPriority) {
      try {
        // 压缩（生成摘要）
        if (this.llm && memory.content.length > 100) {
          const summary = await this.compressMemory(memory.content);
          await this.vectorStore.updateMemory(memory.id, {
            content: summary,
            metadata: {
              originalLength: memory.content.length,
              compressedAt: new Date().toISOString(),
              isCompressed: true
            }
          });
          stats.compressed++;
        }
        
        // 标记为归档
        await this.vectorStore.updateMemory(memory.id, {
          metadata: {
            status: 'archived',
            archivedAt: new Date().toISOString()
          }
        });
        stats.archived++;
        
      } catch (e) {
        console.error(`[MemoryManager] Failed to forget memory ${memory.id}:`, e);
      }
    }
    
    this.emit('forgetting-completed', stats);
    return stats;
  }

  /**
   * 压缩记忆（生成摘要）
   * @param {string} content - 原始内容
   * @returns {Promise<string>} - 摘要
   */
  async compressMemory(content) {
    if (!this.llm) {
      // 简单摘要：取前 100 字
      return content.slice(0, 100) + '...';
    }
    
    const prompt = `请用一句话总结以下内容，保留核心信息：\n\n${content}`;
    const response = await this.llm.generate(prompt);
    return response.text.trim();
  }

  /**
   * 获取记忆统计
   * @returns {Promise<Object>}
   */
  async getStats() {
    const vectorStats = await this.vectorStore.getStats();
    const graphStats = this.graphStore.getStats();
    
    const allMemories = await this.vectorStore.search('', 10000);
    const scores = allMemories.map(m => this.calculateScore(m));
    
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length || 0;
    const lowPriorityCount = scores.filter(s => s < this.forgetThreshold).length;
    
    return {
      vector: vectorStats,
      graph: graphStats,
      memory: {
        total: allMemories.length,
        avgScore: avgScore.toFixed(3),
        lowPriorityCount,
        accessTracked: this.accessCounts.size
      }
    };
  }

  /**
   * 清理访问计数（定期调用）
   */
  cleanupAccessCounts(maxSize = 1000) {
    if (this.accessCounts.size <= maxSize) {
      return;
    }
    
    // 保留最近访问的前 maxSize 个
    const sorted = Array.from(this.accessCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, maxSize);
    
    this.accessCounts = new Map(sorted);
  }
}

export default MemoryManager;
