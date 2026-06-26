/**
 * 记忆提取器 - Memory Extractor
 * 借鉴 OpenViking 的 8 类记忆提取机制
 */

import { logger } from '../utils/logger.js';
import { VikingURI, URI_TEMPLATES } from '../core/viking_uri.js';

/**
 * 8 类记忆分类
 */
export const MEMORY_CATEGORIES = {
  // 用户记忆
  PROFILE: 'profile',           // 用户身份/属性
  PREFERENCES: 'preferences',   // 用户偏好
  ENTITIES: 'entities',         // 实体（人/项目）
  EVENTS: 'events',             // 事件/决策
  
  // Agent 记忆
  CASES: 'cases',              // 问题 + 解决方案
  PATTERNS: 'patterns',        // 可复用模式
  TOOLS: 'tools',              // 工具使用知识
  SKILLS: 'skills'             // 技能执行知识
};

/**
 * 记忆分类配置
 */
export const CATEGORY_CONFIG = {
  [MEMORY_CATEGORIES.PROFILE]: {
    belongsTo: 'user',
    description: '用户身份/属性',
    mergeable: true,
    priority: 5
  },
  [MEMORY_CATEGORIES.PREFERENCES]: {
    belongsTo: 'user',
    description: '用户偏好',
    mergeable: true,
    priority: 4
  },
  [MEMORY_CATEGORIES.ENTITIES]: {
    belongsTo: 'user',
    description: '实体（人/项目）',
    mergeable: true,
    priority: 3
  },
  [MEMORY_CATEGORIES.EVENTS]: {
    belongsTo: 'user',
    description: '事件/决策',
    mergeable: false,
    priority: 3
  },
  [MEMORY_CATEGORIES.CASES]: {
    belongsTo: 'agent',
    description: '问题 + 解决方案',
    mergeable: false,
    priority: 4
  },
  [MEMORY_CATEGORIES.PATTERNS]: {
    belongsTo: 'agent',
    description: '可复用模式',
    mergeable: true,
    priority: 3
  },
  [MEMORY_CATEGORIES.TOOLS]: {
    belongsTo: 'agent',
    description: '工具使用知识',
    mergeable: true,
    priority: 3
  },
  [MEMORY_CATEGORIES.SKILLS]: {
    belongsTo: 'agent',
    description: '技能执行知识',
    mergeable: true,
    priority: 4
  }
};

/**
 * 候选记忆
 */
export class CandidateMemory {
  constructor(options) {
    this.id = options.id || `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.category = options.category;
    this.content = options.content;
    this.importance = options.importance || 0.5;
    this.confidence = options.confidence || 0.8;
    this.source = options.source || 'session';
    this.timestamp = Date.now();
    this.metadata = options.metadata || {};
  }
  
  toJSON() {
    return {
      id: this.id,
      category: this.category,
      content: this.content,
      importance: this.importance,
      confidence: this.confidence,
      source: this.source,
      timestamp: this.timestamp,
      metadata: this.metadata
    };
  }
}

/**
 * 去重决策
 */
export class DedupDecision {
  constructor(options) {
    this.candidateDecision = options.candidateDecision;  // 'skip' | 'create' | 'none'
    this.itemDecisions = options.itemDecisions || [];   // [{memoryId, action: 'merge' | 'delete'}]
    this.reason = options.reason || '';
  }
  
  toJSON() {
    return {
      candidateDecision: this.candidateDecision,
      itemDecisions: this.itemDecisions,
      reason: this.reason
    };
  }
}

/**
 * 记忆提取器
 */
export class MemoryExtractor {
  constructor(options = {}) {
    this.llmClient = options.llmClient;
    this.vectorStore = options.vectorStore;
    this.storage = options.storage;
    
    // 配置
    this.similarityThreshold = options.similarityThreshold || 0.85;
    this.maxSimilarMemories = options.maxSimilarMemories || 5;
    this.enableLLMDedup = options.enableLLMDedup !== false;
    
    // 统计
    this.stats = {
      totalExtractions: 0,
      totalMemoriesExtracted: 0,
      totalSkipped: 0,
      totalMerged: 0,
      totalCreated: 0,
      avgExtractionTime: 0
    };
  }
  
  /**
   * 从 Session 提取记忆
   */
  async extract(session) {
    const startTime = Date.now();
    
    logger.info(`[MemoryExtractor] 开始从 Session ${session.id} 提取记忆`);
    
    // 1. LLM 提取候选记忆
    const candidates = await this.extractCandidates(session);
    
    logger.debug(`[MemoryExtractor] 提取到 ${candidates.length} 个候选记忆`);
    
    // 2. 向量预过滤
    const filtered = await this.vectorPrefilter(candidates);
    
    // 3. LLM 去重决策
    const decisions = await this.deduplication(filtered);
    
    // 4. 写入记忆
    const memories = await this.writeMemories(decisions, session);
    
    // 更新统计
    const extractionTime = Date.now() - startTime;
    this.stats.totalExtractions++;
    this.stats.totalMemoriesExtracted += memories.length;
    this.stats.avgExtractionTime = 
      (this.stats.avgExtractionTime * (this.stats.totalExtractions - 1) + extractionTime) / 
      this.stats.totalExtractions;
    
    logger.info(`[MemoryExtractor] 提取完成，写入 ${memories.length} 条记忆，耗时 ${extractionTime}ms`);
    
    return memories;
  }
  
  /**
   * 提取候选记忆
   */
  async extractCandidates(session) {
    if (!this.llmClient) {
      logger.warn('[MemoryExtractor] LLM 客户端未配置，使用规则提取');
      return this.extractWithRules(session);
    }
    
    try {
      const messages = session.messages.map(m => {
        const text = m.parts
          .filter(p => p.type === 'text')
          .map(p => p.text)
          .join(' ');
        
        return `${m.role}: ${text}`;
      }).join('\n');
      
      const prompt = `从以下对话中提取记忆。输出 JSON 格式：

{
  "memories": [
    {
      "category": "profile|preferences|entities|events|cases|patterns|tools|skills",
      "content": "记忆内容",
      "importance": 0.0-1.0,
      "confidence": 0.0-1.0
    }
  ]
}

分类规则：
- profile: 用户身份、姓名、职位、联系方式等
- preferences: 用户偏好、习惯、风格等
- entities: 提到的人、项目、组织等
- events: 重要事件、决策、里程碑等
- cases: 遇到的问题和解决方案
- patterns: 可复用的模式、最佳实践
- tools: 工具使用知识、技巧
- skills: 技能执行知识、工作流

对话内容：
${messages}`;
      
      const response = await this.llmClient.chat({
        messages: [
          {
            role: 'system',
            content: '你是一个记忆提取专家。从对话中提取有价值的长期记忆。'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        response_format: { type: 'json_object' }
      });
      
      const result = JSON.parse(response.choices[0].message.content);
      
      return (result.memories || []).map(m => new CandidateMemory({
        category: m.category,
        content: m.content,
        importance: m.importance,
        confidence: m.confidence,
        source: `session:${session.id}`
      }));
      
    } catch (error) {
      logger.error('[MemoryExtractor] LLM 提取失败，回退到规则提取:', error);
      return this.extractWithRules(session);
    }
  }
  
  /**
   * 使用规则提取
   */
  extractWithRules(session) {
    const candidates = [];
    
    for (const message of session.messages) {
      const text = message.parts
        .filter(p => p.type === 'text')
        .map(p => p.text)
        .join(' ');
      
      // 检测偏好
      if (/我(喜欢|偏好|习惯|通常)/.test(text)) {
        candidates.push(new CandidateMemory({
          category: MEMORY_CATEGORIES.PREFERENCES,
          content: text,
          importance: 0.6,
          confidence: 0.7,
          source: `session:${session.id}`
        }));
      }
      
      // 检测实体
      if (/(项目|公司|团队|同事|朋友)/.test(text)) {
        candidates.push(new CandidateMemory({
          category: MEMORY_CATEGORIES.ENTITIES,
          content: text,
          importance: 0.5,
          confidence: 0.6,
          source: `session:${session.id}`
        }));
      }
      
      // 检测事件
      if (/(决定|完成|发布|上线|修复)/.test(text)) {
        candidates.push(new CandidateMemory({
          category: MEMORY_CATEGORIES.EVENTS,
          content: text,
          importance: 0.7,
          confidence: 0.8,
          source: `session:${session.id}`
        }));
      }
      
      // 检测案例
      if (/(问题|错误|bug|解决|修复)/.test(text)) {
        candidates.push(new CandidateMemory({
          category: MEMORY_CATEGORIES.CASES,
          content: text,
          importance: 0.7,
          confidence: 0.7,
          source: `session:${session.id}`
        }));
      }
    }
    
    return candidates;
  }
  
  /**
   * 向量预过滤
   */
  async vectorPrefilter(candidates) {
    if (!this.vectorStore) {
      return candidates.map(c => ({ candidate: c, similar: [] }));
    }
    
    const filtered = [];
    
    for (const candidate of candidates) {
      try {
        // 搜索相似记忆
        const similar = await this.vectorStore.search(candidate.content, {
          filter: { category: candidate.category },
          limit: this.maxSimilarMemories,
          threshold: this.similarityThreshold
        });
        
        filtered.push({
          candidate: candidate,
          similar: similar
        });
        
      } catch (error) {
        logger.error('[MemoryExtractor] 向量搜索失败:', error);
        filtered.push({ candidate: candidate, similar: [] });
      }
    }
    
    return filtered;
  }
  
  /**
   * LLM 去重决策
   */
  async deduplication(filtered) {
    const decisions = [];
    
    for (const item of filtered) {
      const { candidate, similar } = item;
      
      // 如果没有相似记忆，直接创建
      if (similar.length === 0) {
        decisions.push({
          candidate: candidate,
          decision: new DedupDecision({
            candidateDecision: 'create',
            reason: '没有相似记忆'
          })
        });
        this.stats.totalCreated++;
        continue;
      }
      
      // 使用 LLM 决策
      if (this.enableLLMDedup && this.llmClient) {
        const decision = await this.llmDedupDecision(candidate, similar);
        decisions.push({ candidate, decision });
        
        if (decision.candidateDecision === 'skip') {
          this.stats.totalSkipped++;
        } else if (decision.candidateDecision === 'create') {
          this.stats.totalCreated++;
        } else {
          this.stats.totalMerged++;
        }
        
      } else {
        // 简单决策：如果相似度很高，跳过
        const maxSimilarity = Math.max(...similar.map(s => s.score || 0));
        
        if (maxSimilarity > 0.95) {
          decisions.push({
            candidate: candidate,
            decision: new DedupDecision({
              candidateDecision: 'skip',
              reason: `相似度过高: ${maxSimilarity}`
            })
          });
          this.stats.totalSkipped++;
        } else {
          decisions.push({
            candidate: candidate,
            decision: new DedupDecision({
              candidateDecision: 'create',
              reason: '相似度适中'
            })
          });
          this.stats.totalCreated++;
        }
      }
    }
    
    return decisions;
  }
  
  /**
   * LLM 去重决策
   */
  async llmDedupDecision(candidate, similar) {
    try {
      const prompt = `候选记忆：
分类: ${candidate.category}
内容: ${candidate.content}
重要性: ${candidate.importance}

相似记忆：
${similar.map((s, i) => `${i + 1}. ${s.text} (相似度: ${s.score})`).join('\n')}

判断候选记忆是否应该：
1. skip: 与现有记忆重复，跳过
2. create: 创建新记忆
3. none: 不创建候选，合并到现有记忆

输出 JSON：
{
  "candidateDecision": "skip|create|none",
  "itemDecisions": [
    {"memoryId": "xxx", "action": "merge|delete"}
  ],
  "reason": "原因"
}`;
      
      const response = await this.llmClient.chat({
        messages: [
          {
            role: 'system',
            content: '你是一个记忆去重专家。判断候选记忆是否与现有记忆重复。'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        response_format: { type: 'json_object' }
      });
      
      const result = JSON.parse(response.choices[0].message.content);
      
      return new DedupDecision({
        candidateDecision: result.candidateDecision,
        itemDecisions: result.itemDecisions || [],
        reason: result.reason
      });
      
    } catch (error) {
      logger.error('[MemoryExtractor] LLM 去重决策失败:', error);
      
      // 回退到简单决策
      return new DedupDecision({
        candidateDecision: 'create',
        reason: 'LLM 决策失败，默认创建'
      });
    }
  }
  
  /**
   * 写入记忆
   */
  async writeMemories(decisions, session) {
    const memories = [];
    
    for (const item of decisions) {
      const { candidate, decision } = item;
      
      if (decision.candidateDecision === 'skip') {
        continue;
      }
      
      // 确定存储 URI
      const config = CATEGORY_CONFIG[candidate.category];
      const baseUri = config.belongsTo === 'user' ?
        URI_TEMPLATES.USER_MEMORIES(session.userId) :
        URI_TEMPLATES.AGENT_MEMORIES(session.agentId);
      
      const memoryUri = `${baseUri}${candidate.category}/${candidate.id}.md`;
      
      // 写入记忆
      if (this.storage) {
        try {
          await this.storage.write(memoryUri, candidate.content);
          
          // 向量化
          if (this.vectorStore) {
            await this.vectorStore.index({
              uri: memoryUri,
              text: candidate.content,
              metadata: {
                category: candidate.category,
                importance: candidate.importance,
                confidence: candidate.confidence,
                source: candidate.source,
                timestamp: candidate.timestamp
              }
            });
          }
          
          memories.push({
            uri: memoryUri,
            ...candidate.toJSON()
          });
          
        } catch (error) {
          logger.error(`[MemoryExtractor] 写入记忆失败: ${memoryUri}`, error);
        }
      } else {
        memories.push({
          uri: memoryUri,
          ...candidate.toJSON()
        });
      }
    }
    
    return memories;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return { ...this.stats };
  }
}

/**
 * 获取记忆提取器实例
 */
let defaultExtractor = null;

export function getMemoryExtractor(options = {}) {
  if (!defaultExtractor) {
    defaultExtractor = new MemoryExtractor(options);
  }
  return defaultExtractor;
}

export default MemoryExtractor;
