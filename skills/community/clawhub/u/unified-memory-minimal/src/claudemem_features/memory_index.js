/**
 * 记忆索引系统 - Claude-Mem 风格
 * 
 * 功能：
 * 1. 多维度索引
 * 2. 自动标签
 * 3. 分类管理
 * 4. 搜索优化
 */

import { logger } from '../utils/logger.js';

export class MemoryIndex {
  constructor(storage, vectorStore) {
    this.storage = storage;
    this.vectorStore = vectorStore;
    this.logger = logger.child({ module: 'memory_index' });
    
    // 内置分类
    this.categories = {
      personal: '个人信息',
      work: '工作相关',
      project: '项目相关',
      idea: '想法点子',
      fact: '客观事实',
      preference: '偏好设置',
      relationship: '人际关系',
      event: '事件记录',
      learning: '学习笔记',
      other: '其他'
    };
    
    // 内置标签
    this.commonTags = [
      '重要', '紧急', '待办', '已完成', '进行中',
      '想法', '决定', '承诺', '问题', '解决方案',
      '反馈', '建议', '批评', '表扬', '学习',
      '成长', '目标', '成就', '失败', '教训'
    ];
  }

  /**
   * 为记忆创建索引
   * @param {string} memoryId - 记忆 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 索引结果
   */
  async indexMemory(memoryId, options = {}) {
    try {
      const memory = await this.storage.findOne('memories', { _id: memoryId });
      
      if (!memory) {
        throw new Error(`Memory not found: ${memoryId}`);
      }
      
      const indexes = {
        category: null,
        tags: [],
        keywords: [],
        entities: [],
        topics: []
      };
      
      // 1. 自动分类
      if (!memory.category || memory.category === 'unknown') {
        indexes.category = await this.suggestCategory(memory.content);
      } else {
        indexes.category = memory.category;
      }
      
      // 2. 自动标签
      if (!memory.tags || memory.tags.length === 0) {
        indexes.tags = await this.suggestTags(memory.content);
      } else {
        indexes.tags = memory.tags;
      }
      
      // 3. 关键词提取
      indexes.keywords = this.extractKeywords(memory.content);
      
      // 4. 实体识别
      indexes.entities = await this.extractEntities(memory.content);
      
      // 5. 主题识别
      indexes.topics = await this.extractTopics(memory.content);
      
      // 更新记忆
      await this.storage.updateOne(
        'memories',
        { _id: memoryId },
        {
          $set: {
            category: indexes.category,
            tags: indexes.tags,
            'metadata.indexes': indexes,
            'metadata.indexedAt': new Date()
          }
        }
      );
      
      this.logger.info('Memory indexed', { memoryId, indexes });
      
      return {
        memoryId,
        indexes,
        indexedAt: new Date()
      };
      
    } catch (error) {
      this.logger.error('Failed to index memory', { error, memoryId });
      throw error;
    }
  }

  /**
   * 批量索引记忆
   * @param {string} userId - 用户 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 批量索引结果
   */
  async batchIndex(userId, options = {}) {
    const { onlyUnindexed = true, limit = 100 } = options;
    
    try {
      const conditions = { userId };
      
      if (onlyUnindexed) {
        conditions.$or = [
          { category: { $exists: false } },
          { category: null },
          { category: 'unknown' },
          { 'metadata.indexedAt': { $exists: false } }
        ];
      }
      
      const memories = await this.storage.find('memories', conditions, { limit });
      
      const results = {
        success: 0,
        failed: 0,
        errors: []
      };
      
      for (const memory of memories) {
        try {
          await this.indexMemory(memory._id);
          results.success++;
        } catch (error) {
          results.failed++;
          results.errors.push({
            memoryId: memory._id,
            error: error.message
          });
        }
      }
      
      this.logger.info('Batch indexing completed', { 
        userId, 
        total: memories.length,
        success: results.success,
        failed: results.failed
      });
      
      return results;
      
    } catch (error) {
      this.logger.error('Batch indexing failed', { error, userId });
      throw error;
    }
  }

  /**
   * 建议分类
   * @param {string} content - 内容
   * @returns {Promise<string>} 建议的分类
   */
  async suggestCategory(content) {
    // 基于关键词的简单分类
    const categoryKeywords = {
      personal: ['我', '我的', '自己', '感觉', '觉得', '想要', '希望', '喜欢', '不喜欢'],
      work: ['工作', '任务', '项目', '会议', '同事', '老板', '客户', ' deadline', '需求'],
      project: ['开发', '代码', '设计', '功能', '测试', '部署', 'bug', '优化', '重构'],
      idea: ['想法', '创意', '建议', '也许', '可能', '考虑', '觉得可以', '突发奇想'],
      fact: ['事实', '是真的', '确认', '验证', '数据', '统计', '研究', '发现'],
      preference: ['偏好', '喜欢', '不喜欢', '倾向', '宁愿', '首选', '习惯'],
      relationship: ['朋友', '家人', '认识', '了解', '关系', '交流', '沟通', '约定'],
      event: ['发生', '去了', '见了', '参加', '会议', '活动', '事件', '那天'],
      learning: ['学习', '了解', '知道', '学会', '掌握', '知识', '技能', '经验']
    };
    
    // 统计各类关键词出现次数
    const scores = {};
    
    for (const [category, keywords] of Object.entries(categoryKeywords)) {
      scores[category] = 0;
      for (const keyword of keywords) {
        if (content.includes(keyword)) {
          scores[category]++;
        }
      }
    }
    
    // 找出得分最高的分类
    let maxScore = 0;
    let suggestedCategory = 'other';
    
    for (const [category, score] of Object.entries(scores)) {
      if (score > maxScore) {
        maxScore = score;
        suggestedCategory = category;
      }
    }
    
    return suggestedCategory;
  }

  /**
   * 建议标签
   * @param {string} content - 内容
   * @returns {Promise<Array>} 建议的标签
   */
  async suggestTags(content) {
    const tags = [];
    
    // 检查内置标签
    for (const tag of this.commonTags) {
      if (content.includes(tag)) {
        tags.push(tag);
      }
    }
    
    // 基于内容的自动标签
    const contentPatterns = [
      { pattern: /\d+[时分秒分钟小时天周月年]/g, tag: '时间相关' },
      { pattern: /[是否]|有没有|能不能/g, tag: '疑问' },
      { pattern: /!{2,}|太棒了|太好了|开心/g, tag: '正面情绪' },
      { pattern: /怎么办|如何|怎么/g, tag: '求助' },
      { pattern: /因为|所以|因此|于是/g, tag: '因果关系' },
      { pattern: /如果|假如|要是/g, tag: '假设' },
      { pattern: /但是|然而|不过/g, tag: '转折' },
      { pattern: /首先|然后|最后|接着/g, tag: '步骤' }
    ];
    
    for (const { pattern, tag } of contentPatterns) {
      if (pattern.test(content)) {
        if (!tags.includes(tag)) {
          tags.push(tag);
        }
      }
    }
    
    // 如果没有找到标签，返回默认
    if (tags.length === 0) {
      tags.push('未分类');
    }
    
    // 限制标签数量
    return tags.slice(0, 5);
  }

  /**
   * 提取关键词
   * @param {string} content - 内容
   * @returns {Array} 关键词列表
   */
  extractKeywords(content) {
    // 简单的关键词提取
    const words = content
      .replace(/[^\w\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length >= 2);
    
    // 统计词频
    const wordCount = {};
    for (const word of words) {
      const lower = word.toLowerCase();
      wordCount[lower] = (wordCount[lower] || 0) + 1;
    }
    
    // 排序并返回前10个
    const sorted = Object.entries(wordCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
    
    return sorted;
  }

  /**
   * 提取实体（简单实现）
   * @param {string} content - 内容
   * @returns {Promise<Array>} 实体列表
   */
  async extractEntities(content) {
    const entities = [];
    
    // 提取邮箱
    const emails = content.match(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g);
    if (emails) {
      entities.push(...emails.map(e => ({ type: 'email', value: e })));
    }
    
    // 提取URL
    const urls = content.match(/https?:\/\/[^\s]+/g);
    if (urls) {
      entities.push(...urls.map(u => ({ type: 'url', value: u })));
    }
    
    // 提取电话号码
    const phones = content.match(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g);
    if (phones) {
      entities.push(...phones.map(p => ({ type: 'phone', value: p })));
    }
    
    return entities;
  }

  /**
   * 提取主题
   * @param {string} content - 内容
   * @returns {Promise<Array>} 主题列表
   */
  async extractTopics(content) {
    // 基于关键词的主题识别
    const topicKeywords = {
      '技术': ['代码', '开发', '编程', '软件', '系统', 'API', '数据库', '服务器'],
      '产品': ['功能', '需求', '用户', '体验', '界面', '设计', '交互'],
      '商业': ['公司', '业务', '市场', '客户', '销售', '收入', '增长'],
      '学习': ['学习', '读书', '课程', '培训', '知识', '技能'],
      '生活': ['生活', '家庭', '朋友', '旅行', '娱乐', '爱好'],
      '健康': ['健康', '运动', '饮食', '睡眠', '锻炼', '身体']
    };
    
    const topics = [];
    
    for (const [topic, keywords] of Object.entries(topicKeywords)) {
      const count = keywords.filter(k => content.includes(k)).length;
      if (count >= 2) {
        topics.push({
          topic,
          confidence: Math.min(1, count / keywords.length)
        });
      }
    }
    
    // 按置信度排序
    topics.sort((a, b) => b.confidence - a.confidence);
    
    return topics.slice(0, 3);
  }

  /**
   * 搜索记忆（多维度）
   * @param {string} userId - 用户 ID
   * @param {Object} query - 搜索查询
   * @returns {Promise<Array>} 搜索结果
   */
  async search(userId, query = {}) {
    const {
      text = '',
      category = null,
      tags = [],
      topics = [],
      dateRange = null,
      importance = null,
      limit = 20
    } = query;
    
    try {
      let results = [];
      
      // 1. 向量搜索（如果提供了文本）
      if (text) {
        const vectorResults = await this.vectorStore.search(text, {
          userId,
          limit: 100,
          filter: category ? { category } : undefined
        });
        
        results = vectorResults.map(r => ({
          ...r,
          relevanceScore: r.score
        }));
      } else {
        // 如果没有文本搜索，获取所有记忆
        const memories = await this.storage.find('memories', { userId }, { limit: 100 });
        results = memories.map(m => ({
          memoryId: m._id,
          ...m,
          relevanceScore: 1
        }));
      }
      
      // 2. 分类过滤
      if (category) {
        results = results.filter(r => r.category === category);
      }
      
      // 3. 标签过滤
      if (tags && tags.length > 0) {
        results = results.filter(r => {
          const memoryTags = r.tags || [];
          return tags.some(tag => memoryTags.includes(tag));
        });
      }
      
      // 4. 主题过滤
      if (topics && topics.length > 0) {
        results = results.filter(r => {
          const memoryTopics = r.metadata?.indexes?.topics || [];
          return topics.some(topic => 
            memoryTopics.some(mt => mt.topic === topic)
          );
        });
      }
      
      // 5. 日期范围过滤
      if (dateRange) {
        const { start, end } = dateRange;
        results = results.filter(r => {
          const createdAt = new Date(r.createdAt);
          if (start && createdAt < new Date(start)) return false;
          if (end && createdAt > new Date(end)) return false;
          return true;
        });
      }
      
      // 6. 重要性过滤
      if (importance !== null) {
        results = results.filter(r => r.important === importance);
      }
      
      // 7. 限制结果数量
      results = results.slice(0, limit);
      
      return results;
      
    } catch (error) {
      this.logger.error('Search failed', { error, userId, query });
      throw error;
    }
  }

  /**
   * 获取用户的所有分类
   * @param {string} userId - 用户 ID
   * @returns {Promise<Object>} 分类统计
   */
  async getCategoryStats(userId) {
    try {
      const memories = await this.storage.find('memories', { userId });
      
      const stats = {
        total: memories.length,
        categories: {}
      };
      
      for (const memory of memories) {
        const category = memory.category || 'unknown';
        if (!stats.categories[category]) {
          stats.categories[category] = {
            count: 0,
            percentage: 0,
            examples: []
          };
        }
        
        stats.categories[category].count++;
        
        // 保存几个示例
        if (stats.categories[category].examples.length < 3) {
          stats.categories[category].examples.push({
            id: memory._id,
            content: memory.content.substring(0, 50) + '...'
          });
        }
      }
      
      // 计算百分比
      for (const category of Object.keys(stats.categories)) {
        stats.categories[category].percentage = 
          Math.round((stats.categories[category].count / stats.total) * 100);
      }
      
      return stats;
      
    } catch (error) {
      this.logger.error('Failed to get category stats', { error, userId });
      throw error;
    }
  }

  /**
   * 获取用户的标签统计
   * @param {string} userId - 用户 ID
   * @returns {Promise<Object>} 标签统计
   */
  async getTagStats(userId) {
    try {
      const memories = await this.storage.find('memories', { userId });
      
      const tagCount = {};
      
      for (const memory of memories) {
        const tags = memory.tags || [];
        for (const tag of tags) {
          tagCount[tag] = (tagCount[tag] || 0) + 1;
        }
      }
      
      // 排序
      const sorted = Object.entries(tagCount)
        .sort((a, b) => b[1] - a[1])
        .reduce((obj, [tag, count]) => {
          obj[tag] = { count, percentage: 0 };
          return obj;
        }, {});
      
      // 计算百分比
      const total = Object.values(sorted).reduce((sum, item) => sum + item.count, 0);
      for (const tag of Object.keys(sorted)) {
        sorted[tag].percentage = Math.round((sorted[tag].count / total) * 100);
      }
      
      return {
        totalTags: Object.keys(sorted).length,
        totalUsages: total,
        tags: sorted
      };
      
    } catch (error) {
      this.logger.error('Failed to get tag stats', { error, userId });
      throw error;
    }
  }

  /**
   * 重建索引
   * @param {string} userId - 用户 ID
   * @returns {Promise<Object>} 重建结果
   */
  async rebuildIndex(userId) {
    try {
      this.logger.info('Starting index rebuild', { userId });
      
      // 1. 清除旧索引
      await this.storage.updateMany(
        'memories',
        { userId },
        {
          $set: {
            'metadata.indexedAt': null
          }
        }
      );
      
      // 2. 批量重新索引
      const batchResult = await this.batchIndex(userId, {
        onlyUnindexed: true,
        limit: 1000
      });
      
      this.logger.info('Index rebuild completed', { userId, result: batchResult });
      
      return {
        success: true,
        indexed: batchResult.success,
        failed: batchResult.failed,
        completedAt: new Date()
      };
      
    } catch (error) {
      this.logger.error('Index rebuild failed', { error, userId });
      throw error;
    }
  }
}

export default MemoryIndex;