/**
 * OpenViking 集成系统 - OpenViking Integrated System
 * 整合所有借鉴自 OpenViking 的功能
 */

import { logger } from './utils/logger.js';

// 核心组件
import { VikingURI, URI_TEMPLATES, URIParser } from './core/viking_uri.js';

// 检索组件
import { IntentAnalyzer, TypedQuery, QueryPlan, getIntentAnalyzer } from './retrieval/intent_analyzer.js';
import { HierarchicalRetriever, MatchedContext, FindResult, getHierarchicalRetriever } from './retrieval/hierarchical_retriever.js';
import { getReranker, VolcengineReranker, CohereReranker, JinaReranker, LocalReranker } from './retrieval/reranker.js';

// Session 组件
import { SessionManager, Session, Message, TextPart, ContextPart, ToolPart, getSessionManager } from './session/session_manager.js';

// 提取组件
import { MemoryExtractor, CandidateMemory, DedupDecision, MEMORY_CATEGORIES, getMemoryExtractor } from './extraction/memory_extractor.js';

// 存储组件
import { FileSystemInterface, getFileSystem } from './storage/filesystem.js';

// 解析组件
import { ParserRegistry, getParserRegistry } from './parsing/document_parser.js';

// 关系组件
import { RelationManager, Relation, RELATION_TYPES, getRelationManager } from './relations/relation_manager.js';

// 现有组件
import { getLayeredCompressor } from './compression/layered_compressor.js';
import { getSmartDeduplicator } from './deduplication/smart_deduplicator.js';
import { getMemoryQueue } from './queue/memory_queue.js';

/**
 * OpenViking 集成系统配置
 */
export const DEFAULT_CONFIG = {
  // Viking URI
  enableVikingURI: true,
  
  // 意图分析
  enableIntentAnalysis: true,
  intentAnalyzer: {
    maxQueries: 5,
    enableCache: true
  },
  
  // 层级检索
  enableHierarchicalRetrieval: true,
  hierarchicalRetriever: {
    scorePropagationAlpha: 0.5,
    maxConvergenceRounds: 3,
    globalSearchTopK: 3
  },
  
  // 重排序
  enableRerank: true,
  reranker: {
    provider: 'local',  // 'volcengine' | 'cohere' | 'jina' | 'local'
    topN: 20
  },
  
  // Session 管理
  enableSessionManagement: true,
  sessionManager: {
    maxMessagesBeforeArchive: 20,
    enableAutoArchive: true,
    enableMemoryExtraction: true
  },
  
  // 记忆提取
  enableMemoryExtraction: true,
  memoryExtractor: {
    similarityThreshold: 0.85,
    maxSimilarMemories: 5,
    enableLLMDedup: true
  },
  
  // 文件系统
  enableFileSystem: true,
  fileSystem: {
    cacheMaxSize: 1000
  },
  
  // 文档解析
  enableDocumentParsing: true,
  
  // 关系管理
  enableRelationManagement: true,
  relationManager: {
    maxRelations: 100
  },
  
  // 分层压缩
  enableLayeredCompression: true,
  layeredCompressor: {
    l0TokenLimit: 100,
    l1TokenLimit: 2000,
    l2TokenLimit: null
  },
  
  // 去重
  enableDedup: true,
  
  // 队列
  enableQueue: true
};

/**
 * OpenViking 集成系统
 */
export class OpenVikingSystem {
  constructor(options = {}) {
    this.options = { ...DEFAULT_CONFIG, ...options };
    this.initialized = false;
    
    // 组件
    this.intentAnalyzer = null;
    this.hierarchicalRetriever = null;
    this.reranker = null;
    this.sessionManager = null;
    this.memoryExtractor = null;
    this.fileSystem = null;
    this.parserRegistry = null;
    this.relationManager = null;
    this.layeredCompressor = null;
    this.deduplicator = null;
    this.queue = null;
    
    // 存储
    this.storage = options.storage;
    this.vectorStore = options.vectorStore;
    this.llmClient = options.llmClient;
    
    // 统计
    this.stats = {
      totalSearches: 0,
      totalSessions: 0,
      totalMemoriesExtracted: 0,
      avgSearchTime: 0
    };
  }
  
  /**
   * 初始化系统
   */
  async initialize() {
    if (this.initialized) {
      return;
    }
    
    logger.info('[OpenVikingSystem] 初始化系统...');
    
    // 1. 初始化意图分析器
    if (this.options.enableIntentAnalysis) {
      this.intentAnalyzer = getIntentAnalyzer({
        llmClient: this.llmClient,
        ...this.options.intentAnalyzer
      });
      logger.info('[OpenVikingSystem] 意图分析器已初始化');
    }
    
    // 2. 初始化重排序器
    if (this.options.enableRerank) {
      this.reranker = getReranker({
        ...this.options.reranker,
        client: this.options.rerankClient
      });
      logger.info('[OpenVikingSystem] 重排序器已初始化');
    }
    
    // 3. 初始化层级检索器
    if (this.options.enableHierarchicalRetrieval) {
      this.hierarchicalRetriever = getHierarchicalRetriever({
        vectorStore: this.vectorStore,
        reranker: this.reranker,
        storage: this.storage,
        ...this.options.hierarchicalRetriever
      });
      logger.info('[OpenVikingSystem] 层级检索器已初始化');
    }
    
    // 4. 初始化记忆提取器
    if (this.options.enableMemoryExtraction) {
      this.memoryExtractor = getMemoryExtractor({
        llmClient: this.llmClient,
        vectorStore: this.vectorStore,
        storage: this.storage,
        ...this.options.memoryExtractor
      });
      logger.info('[OpenVikingSystem] 记忆提取器已初始化');
    }
    
    // 5. 初始化 Session 管理器
    if (this.options.enableSessionManagement) {
      this.sessionManager = getSessionManager({
        storage: this.storage,
        memoryExtractor: this.memoryExtractor,
        ...this.options.sessionManager
      });
      logger.info('[OpenVikingSystem] Session 管理器已初始化');
    }
    
    // 6. 初始化文件系统
    if (this.options.enableFileSystem) {
      this.fileSystem = getFileSystem({
        storage: this.storage,
        vectorStore: this.vectorStore,
        ...this.options.fileSystem
      });
      logger.info('[OpenVikingSystem] 文件系统已初始化');
    }
    
    // 7. 初始化解析器
    if (this.options.enableDocumentParsing) {
      this.parserRegistry = getParserRegistry();
      logger.info('[OpenVikingSystem] 文档解析器已初始化');
    }
    
    // 8. 初始化关系管理器
    if (this.options.enableRelationManagement) {
      this.relationManager = getRelationManager({
        storage: this.storage,
        ...this.options.relationManager
      });
      logger.info('[OpenVikingSystem] 关系管理器已初始化');
    }
    
    // 9. 初始化分层压缩器
    if (this.options.enableLayeredCompression) {
      this.layeredCompressor = getLayeredCompressor({
        ...this.options.layeredCompressor
      });
      logger.info('[OpenVikingSystem] 分层压缩器已初始化');
    }
    
    // 10. 初始化去重器
    if (this.options.enableDedup) {
      this.deduplicator = getSmartDeduplicator();
      logger.info('[OpenVikingSystem] 去重器已初始化');
    }
    
    // 11. 初始化队列
    if (this.options.enableQueue) {
      this.queue = getMemoryQueue();
      logger.info('[OpenVikingSystem] 队列已初始化');
    }
    
    this.initialized = true;
    
    logger.info('[OpenVikingSystem] 系统初始化完成');
  }
  
  /**
   * 搜索（find - 简单查询）
   */
  async find(query, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const startTime = Date.now();
    
    logger.info(`[OpenVikingSystem] find: ${query}`);
    
    // 直接向量搜索
    if (this.vectorStore) {
      const results = await this.vectorStore.search(query, {
        filter: options.filter,
        limit: options.limit || 20
      });
      
      // 重排序
      if (this.reranker && options.useRerank !== false) {
        const reranked = await this.reranker.rerank(query, results);
        
        // 更新统计
        const searchTime = Date.now() - startTime;
        this.stats.totalSearches++;
        this.stats.avgSearchTime = 
          (this.stats.avgSearchTime * (this.stats.totalSearches - 1) + searchTime) / 
          this.stats.totalSearches;
        
        return new FindResult({
          memories: reranked.filter(r => r.uri.includes('memories')),
          resources: reranked.filter(r => r.uri.includes('resources')),
          skills: reranked.filter(r => r.uri.includes('skills')),
          total: reranked.length
        });
      }
      
      return new FindResult({
        memories: results.filter(r => r.uri.includes('memories')),
        resources: results.filter(r => r.uri.includes('resources')),
        skills: results.filter(r => r.uri.includes('skills')),
        total: results.length
      });
    }
    
    return new FindResult();
  }
  
  /**
   * 搜索（search - 复杂查询）
   */
  async search(query, sessionContext, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const startTime = Date.now();
    
    logger.info(`[OpenVikingSystem] search: ${query}`);
    
    // 1. 意图分析
    let queryPlan = null;
    
    if (this.intentAnalyzer) {
      queryPlan = await this.intentAnalyzer.analyze(query, sessionContext);
      
      logger.debug(`[OpenVikingSystem] 生成 ${queryPlan.typedQueries.length} 个类型化查询`);
    }
    
    // 2. 层级检索
    let results;
    
    if (this.hierarchicalRetriever && queryPlan) {
      results = await this.hierarchicalRetriever.retrieve(
        queryPlan.typedQueries,
        {
          userId: options.userId,
          agentId: options.agentId,
          threshold: options.threshold,
          useRerank: options.useRerank
        }
      );
      
      results.queryPlan = queryPlan;
    } else {
      // 回退到简单搜索
      results = await this.find(query, options);
    }
    
    // 3. 分层压缩
    if (this.layeredCompressor && options.useLayeredCompression !== false) {
      const allResults = [
        ...results.memories,
        ...results.resources,
        ...results.skills
      ];
      
      const compressed = this.layeredCompressor.selectLayer(
        allResults,
        query,
        {
          maxTokens: options.maxTokens || 4000,
          strategy: options.layerStrategy || 'adaptive'
        }
      );
      
      results.memories = compressed.memories.filter(m => m.uri.includes('memories'));
      results.resources = compressed.memories.filter(m => m.uri.includes('resources'));
      results.skills = compressed.memories.filter(m => m.uri.includes('skills'));
      results.totalTokens = compressed.totalTokens;
    }
    
    // 更新统计
    const searchTime = Date.now() - startTime;
    this.stats.totalSearches++;
    this.stats.avgSearchTime = 
      (this.stats.avgSearchTime * (this.stats.totalSearches - 1) + searchTime) / 
      this.stats.totalSearches;
    
    logger.info(`[OpenVikingSystem] search 完成，返回 ${results.total} 个结果，耗时 ${searchTime}ms`);
    
    return results;
  }
  
  /**
   * 获取 Session
   */
  async getSession(sessionId, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    if (!this.sessionManager) {
      throw new Error('Session 管理未启用');
    }
    
    return this.sessionManager.getSession(sessionId, options);
  }
  
  /**
   * 添加消息
   */
  async addMessage(sessionId, role, parts) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    if (!this.sessionManager) {
      throw new Error('Session 管理未启用');
    }
    
    return this.sessionManager.addMessage(sessionId, role, parts);
  }
  
  /**
   * 提交 Session
   */
  async commitSession(sessionId) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    if (!this.sessionManager) {
      throw new Error('Session 管理未启用');
    }
    
    const result = await this.sessionManager.commit(sessionId);
    
    if (result.taskId) {
      this.stats.totalMemoriesExtracted++;
    }
    
    return result;
  }
  
  /**
   * 添加资源
   */
  async addResource(url, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    logger.info(`[OpenVikingSystem] 添加资源: ${url}`);
    
    // 1. 解析文档
    let parseResult;
    
    if (this.parserRegistry) {
      parseResult = await this.parserRegistry.parse(url, {
        uri: url,
        ...options
      });
    }
    
    // 2. 存储内容
    if (this.storage && parseResult) {
      const uri = options.targetUri || `viking://resources/${options.project || 'default'}/${options.filename || 'resource'}`;
      
      await this.storage.write(uri, parseResult.content);
      
      // 3. 向量化
      if (this.vectorStore) {
        await this.vectorStore.index({
          uri: uri,
          text: parseResult.content,
          metadata: {
            format: parseResult.format,
            tokens: parseResult.tokens,
            ...parseResult.metadata
          }
        });
      }
      
      return { uri, parseResult };
    }
    
    return null;
  }
  
  /**
   * 添加技能
   */
  async addSkill(skill, options = {}) {
    if (!this.initialized) {
      await this.initialize();
    }
    
    logger.info(`[OpenVikingSystem] 添加技能: ${skill.name}`);
    
    const uri = `viking://agent/${options.agentId || 'default'}/skills/${skill.name}/`;
    
    // 存储
    if (this.storage) {
      await this.storage.write(uri + 'SKILL.md', skill.content);
      
      // 向量化
      if (this.vectorStore) {
        await this.vectorStore.index({
          uri: uri,
          text: skill.description || skill.content,
          metadata: {
            type: 'skill',
            name: skill.name
          }
        });
      }
    }
    
    return { uri };
  }
  
  /**
   * 文件系统操作
   */
  get fs() {
    if (!this.initialized) {
      throw new Error('系统未初始化');
    }
    
    return this.fileSystem;
  }
  
  /**
   * 关系管理操作
   */
  get relations() {
    if (!this.initialized) {
      throw new Error('系统未初始化');
    }
    
    return this.relationManager;
  }
  
  /**
   * 获取系统状态
   */
  getStatus() {
    const status = {
      initialized: this.initialized,
      components: {
        intentAnalyzer: this.intentAnalyzer ? this.intentAnalyzer.getStats() : null,
        hierarchicalRetriever: this.hierarchicalRetriever ? this.hierarchicalRetriever.getStats() : null,
        reranker: this.reranker ? this.reranker.getStats() : null,
        sessionManager: this.sessionManager ? this.sessionManager.getStats() : null,
        memoryExtractor: this.memoryExtractor ? this.memoryExtractor.getStats() : null,
        fileSystem: this.fileSystem ? this.fileSystem.getCacheStats() : null,
        relationManager: this.relationManager ? this.relationManager.getStats() : null,
        layeredCompressor: this.layeredCompressor ? this.layeredCompressor.getStats() : null
      },
      stats: this.stats
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
    
    const components = [
      { name: 'intentAnalyzer', instance: this.intentAnalyzer },
      { name: 'hierarchicalRetriever', instance: this.hierarchicalRetriever },
      { name: 'reranker', instance: this.reranker },
      { name: 'sessionManager', instance: this.sessionManager },
      { name: 'memoryExtractor', instance: this.memoryExtractor },
      { name: 'fileSystem', instance: this.fileSystem },
      { name: 'relationManager', instance: this.relationManager },
      { name: 'layeredCompressor', instance: this.layeredCompressor }
    ];
    
    for (const component of components) {
      health.components[component.name] = {
        status: component.instance ? 'healthy' : 'disabled'
      };
    }
    
    return health;
  }
  
  /**
   * 关闭系统
   */
  async shutdown() {
    logger.info('[OpenVikingSystem] 关闭系统...');
    
    // 清理资源
    if (this.fileSystem) {
      this.fileSystem.clearCache();
    }
    
    if (this.relationManager) {
      this.relationManager.clear();
    }
    
    this.initialized = false;
    
    logger.info('[OpenVikingSystem] 系统已关闭');
  }
}

/**
 * 创建 OpenViking 系统实例
 */
export function createOpenVikingSystem(options = {}) {
  return new OpenVikingSystem(options);
}

/**
 * 获取默认实例
 */
let defaultSystem = null;

export function getOpenVikingSystem(options = {}) {
  if (!defaultSystem) {
    defaultSystem = new OpenVikingSystem(options);
  }
  return defaultSystem;
}

// 导出所有组件
export {
  // URI
  VikingURI,
  URI_TEMPLATES,
  URIParser,
  
  // 检索
  IntentAnalyzer,
  TypedQuery,
  QueryPlan,
  HierarchicalRetriever,
  MatchedContext,
  FindResult,
  
  // Rerank
  VolcengineReranker,
  CohereReranker,
  JinaReranker,
  LocalReranker,
  
  // Session
  SessionManager,
  Session,
  Message,
  TextPart,
  ContextPart,
  ToolPart,
  
  // Extraction
  MemoryExtractor,
  CandidateMemory,
  DedupDecision,
  MEMORY_CATEGORIES,
  
  // Storage
  FileSystemInterface,
  
  // Parsing
  ParserRegistry,
  
  // Relations
  RelationManager,
  Relation,
  RELATION_TYPES
};

export default OpenVikingSystem;
