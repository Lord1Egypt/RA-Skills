/**
 * 意图分析器 - Intent Analyzer
 * 借鉴 OpenViking 的意图分析机制
 */

import { getLayeredCompressor } from '../compression/layered_compressor.js';
import { logger } from '../utils/logger.js';

/**
 * 类型化查询
 */
export class TypedQuery {
  constructor(options) {
    this.query = options.query;              // 重写的查询
    this.contextType = options.contextType;  // MEMORY/RESOURCE/SKILL
    this.intent = options.intent;            // 查询目的
    this.priority = options.priority || 3;   // 1-5 优先级
    this.metadata = options.metadata || {};  // 额外元数据
  }
  
  toJSON() {
    return {
      query: this.query,
      contextType: this.contextType,
      intent: this.intent,
      priority: this.priority,
      metadata: this.metadata
    };
  }
}

/**
 * 查询计划
 */
export class QueryPlan {
  constructor(options) {
    this.originalQuery = options.originalQuery;
    this.typedQueries = options.typedQueries || [];
    this.sessionContext = options.sessionContext || null;
    this.createdAt = Date.now();
  }
  
  addTypedQuery(typedQuery) {
    this.typedQueries.push(typedQuery);
    this.typedQueries.sort((a, b) => b.priority - a.priority);
  }
  
  toJSON() {
    return {
      originalQuery: this.originalQuery,
      typedQueries: this.typedQueries.map(q => q.toJSON()),
      createdAt: this.createdAt
    };
  }
}

/**
 * 意图分析器
 */
export class IntentAnalyzer {
  constructor(options = {}) {
    this.llmClient = options.llmClient || null;
    this.maxQueries = options.maxQueries || 5;
    this.enableCache = options.enableCache !== false;
    this.cache = new Map();
    this.cacheMaxSize = options.cacheMaxSize || 100;
    
    // 统计
    this.stats = {
      totalAnalyzed: 0,
      cacheHits: 0,
      avgQueriesGenerated: 0,
      avgAnalysisTime: 0
    };
  }
  
  /**
   * 分析查询意图
   */
  async analyze(query, sessionContext = null) {
    const startTime = Date.now();
    
    logger.info(`[IntentAnalyzer] 分析查询: ${query.substring(0, 50)}...`);
    
    // 检查缓存
    if (this.enableCache) {
      const cacheKey = this.getCacheKey(query, sessionContext);
      const cached = this.cache.get(cacheKey);
      
      if (cached) {
        this.stats.cacheHits++;
        logger.debug('[IntentAnalyzer] 使用缓存结果');
        return cached;
      }
    }
    
    // 分析意图
    let queryPlan;
    
    if (this.llmClient) {
      queryPlan = await this.analyzeWithLLM(query, sessionContext);
    } else {
      queryPlan = await this.analyzeWithRules(query, sessionContext);
    }
    
    // 更新统计
    const analysisTime = Date.now() - startTime;
    this.stats.totalAnalyzed++;
    this.stats.avgAnalysisTime = 
      (this.stats.avgAnalysisTime * (this.stats.totalAnalyzed - 1) + analysisTime) / 
      this.stats.totalAnalyzed;
    this.stats.avgQueriesGenerated = 
      (this.stats.avgQueriesGenerated * (this.stats.totalAnalyzed - 1) + queryPlan.typedQueries.length) / 
      this.stats.totalAnalyzed;
    
    // 缓存结果
    if (this.enableCache) {
      const cacheKey = this.getCacheKey(query, sessionContext);
      this.cache.set(cacheKey, queryPlan);
      
      // 限制缓存大小
      if (this.cache.size > this.cacheMaxSize) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
    }
    
    logger.info(`[IntentAnalyzer] 生成 ${queryPlan.typedQueries.length} 个类型化查询，耗时 ${analysisTime}ms`);
    
    return queryPlan;
  }
  
  /**
   * 使用 LLM 分析意图
   */
  async analyzeWithLLM(query, sessionContext) {
    const prompt = this.buildAnalysisPrompt(query, sessionContext);
    
    try {
      const response = await this.llmClient.chat({
        messages: [
          {
            role: 'system',
            content: `你是一个查询意图分析器。分析用户的查询，生成 0-5 个类型化查询。

输出 JSON 格式：
{
  "queries": [
    {
      "query": "重写的查询",
      "contextType": "MEMORY|RESOURCE|SKILL",
      "intent": "查询目的",
      "priority": 1-5
    }
  ]
}

规则：
1. MEMORY: 查询用户的记忆、偏好、历史
2. RESOURCE: 查询文档、知识库、外部资源
3. SKILL: 查询可执行的技能、工具

优先级：
- 5: 必须查询
- 4: 重要查询
- 3: 一般查询
- 2: 可选查询
- 1: 补充查询

如果是闲聊、问候，返回空数组。`
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        response_format: { type: 'json_object' }
      });
      
      const result = JSON.parse(response.choices[0].message.content);
      
      const queryPlan = new QueryPlan({
        originalQuery: query,
        sessionContext: sessionContext
      });
      
      for (const q of result.queries || []) {
        queryPlan.addTypedQuery(new TypedQuery({
          query: q.query,
          contextType: q.contextType,
          intent: q.intent,
          priority: q.priority
        }));
      }
      
      return queryPlan;
      
    } catch (error) {
      logger.error('[IntentAnalyzer] LLM 分析失败，回退到规则分析:', error);
      return this.analyzeWithRules(query, sessionContext);
    }
  }
  
  /**
   * 使用规则分析意图
   */
  async analyzeWithRules(query, sessionContext) {
    const queryPlan = new QueryPlan({
      originalQuery: query,
      sessionContext: sessionContext
    });
    
    const lowerQuery = query.toLowerCase();
    
    // 检测技能查询（动词开头）
    const skillPatterns = [
      /^(创建|生成|删除|修改|更新|执行|运行|调用|使用|帮我|请)/i,
      /^(create|generate|delete|modify|update|execute|run|call|use|help)/i
    ];
    
    if (skillPatterns.some(p => p.test(query))) {
      queryPlan.addTypedQuery(new TypedQuery({
        query: query,
        contextType: 'SKILL',
        intent: '执行任务',
        priority: 5
      }));
    }
    
    // 检测资源查询（名词短语）
    const resourcePatterns = [
      /(文档|手册|指南|教程|模板|示例|代码|api)/i,
      /(document|manual|guide|tutorial|template|example|code|api)/i
    ];
    
    if (resourcePatterns.some(p => p.test(query))) {
      queryPlan.addTypedQuery(new TypedQuery({
        query: query,
        contextType: 'RESOURCE',
        intent: '查找资源',
        priority: 4
      }));
    }
    
    // 检测记忆查询
    const memoryPatterns = [
      /(我的|用户|偏好|设置|历史|之前|上次)/i,
      /(my|user|preference|setting|history|before|last)/i
    ];
    
    if (memoryPatterns.some(p => p.test(query))) {
      queryPlan.addTypedQuery(new TypedQuery({
        query: query,
        contextType: 'MEMORY',
        intent: '查询记忆',
        priority: 4
      }));
    }
    
    // 如果没有匹配任何模式，添加通用查询
    if (queryPlan.typedQueries.length === 0) {
      queryPlan.addTypedQuery(new TypedQuery({
        query: query,
        contextType: 'MEMORY',
        intent: '通用查询',
        priority: 3
      }));
    }
    
    return queryPlan;
  }
  
  /**
   * 构建分析提示
   */
  buildAnalysisPrompt(query, sessionContext) {
    let prompt = `用户查询: "${query}"\n\n`;
    
    if (sessionContext) {
      prompt += `会话上下文:\n`;
      
      if (sessionContext.summary) {
        prompt += `- 摘要: ${sessionContext.summary}\n`;
      }
      
      if (sessionContext.lastMessages && sessionContext.lastMessages.length > 0) {
        prompt += `- 最近消息:\n`;
        sessionContext.lastMessages.slice(-3).forEach(msg => {
          prompt += `  ${msg.role}: ${msg.text.substring(0, 100)}...\n`;
        });
      }
    }
    
    return prompt;
  }
  
  /**
   * 获取缓存键
   */
  getCacheKey(query, sessionContext) {
    const contextHash = sessionContext ? 
      JSON.stringify(sessionContext.summary || '') : 
      '';
    return `${query}:${contextHash}`;
  }
  
  /**
   * 清除缓存
   */
  clearCache() {
    this.cache.clear();
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: this.cache.size,
      cacheHitRate: this.stats.totalAnalyzed > 0 ? 
        this.stats.cacheHits / this.stats.totalAnalyzed : 0
    };
  }
}

/**
 * 获取意图分析器实例
 */
let defaultAnalyzer = null;

export function getIntentAnalyzer(options = {}) {
  if (!defaultAnalyzer) {
    defaultAnalyzer = new IntentAnalyzer(options);
  }
  return defaultAnalyzer;
}

export default IntentAnalyzer;
