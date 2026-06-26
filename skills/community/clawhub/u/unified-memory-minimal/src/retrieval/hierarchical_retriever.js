/**
 * 层级检索器 - Hierarchical Retriever
 * 借鉴 OpenViking 的层级检索机制
 */

import { logger } from '../utils/logger.js';
import { VikingURI } from '../core/viking_uri.js';

/**
 * 匹配的上下文
 */
export class MatchedContext {
  constructor(options) {
    this.uri = options.uri;
    this.contextType = options.contextType;
    this.isLeaf = options.isLeaf;
    this.abstract = options.abstract;
    this.overview = options.overview;
    this.score = options.score;
    this.relations = options.relations || [];
    this.metadata = options.metadata || {};
  }
  
  toJSON() {
    return {
      uri: this.uri,
      contextType: this.contextType,
      isLeaf: this.isLeaf,
      abstract: this.abstract,
      overview: this.overview,
      score: this.score,
      relations: this.relations,
      metadata: this.metadata
    };
  }
}

/**
 * 检索结果
 */
export class FindResult {
  constructor(options) {
    this.memories = options.memories || [];
    this.resources = options.resources || [];
    this.skills = options.skills || [];
    this.queryPlan = options.queryPlan || null;
    this.total = options.total || 0;
  }
  
  toJSON() {
    return {
      memories: this.memories.map(m => m.toJSON()),
      resources: this.resources.map(r => r.toJSON()),
      skills: this.skills.map(s => s.toJSON()),
      queryPlan: this.queryPlan ? this.queryPlan.toJSON() : null,
      total: this.total
    };
  }
}

/**
 * 优先队列项
 */
class PriorityQueueItem {
  constructor(uri, score) {
    this.uri = uri;
    this.score = score;
  }
}

/**
 * 优先队列（最小堆）
 */
class PriorityQueue {
  constructor() {
    this.heap = [];
  }
  
  push(item) {
    this.heap.push(item);
    this.bubbleUp(this.heap.length - 1);
  }
  
  pop() {
    if (this.heap.length === 0) return null;
    
    const min = this.heap[0];
    const last = this.heap.pop();
    
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.bubbleDown(0);
    }
    
    return min;
  }
  
  get length() {
    return this.heap.length;
  }
  
  bubbleUp(index) {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      
      if (this.heap[parentIndex].score <= this.heap[index].score) {
        break;
      }
      
      [this.heap[parentIndex], this.heap[index]] = 
        [this.heap[index], this.heap[parentIndex]];
      index = parentIndex;
    }
  }
  
  bubbleDown(index) {
    const length = this.heap.length;
    
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let smallest = index;
      
      if (leftChild < length && this.heap[leftChild].score < this.heap[smallest].score) {
        smallest = leftChild;
      }
      
      if (rightChild < length && this.heap[rightChild].score < this.heap[smallest].score) {
        smallest = rightChild;
      }
      
      if (smallest === index) break;
      
      [this.heap[index], this.heap[smallest]] = 
        [this.heap[smallest], this.heap[index]];
      index = smallest;
    }
  }
}

/**
 * 层级检索器
 */
export class HierarchicalRetriever {
  constructor(options = {}) {
    this.vectorStore = options.vectorStore;
    this.reranker = options.reranker;
    this.storage = options.storage;
    
    // 检索参数
    this.scorePropagationAlpha = options.scorePropagationAlpha || 0.5;
    this.maxConvergenceRounds = options.maxConvergenceRounds || 3;
    this.globalSearchTopK = options.globalSearchTopK || 3;
    this.maxRelations = options.maxRelations || 5;
    this.defaultThreshold = options.defaultThreshold || 0.5;
    
    // 统计
    this.stats = {
      totalSearches: 0,
      totalResults: 0,
      avgSearchTime: 0,
      avgResultsPerSearch: 0
    };
  }
  
  /**
   * 检索
   */
  async retrieve(typedQueries, options = {}) {
    const startTime = Date.now();
    
    logger.info(`[HierarchicalRetriever] 开始检索，${typedQueries.length} 个类型化查询`);
    
    const allResults = [];
    
    for (const typedQuery of typedQueries) {
      // 1. 确定根目录
      const rootUris = this.getRootUris(typedQuery.contextType, options);
      
      // 2. 全局搜索定位起始点
      const startPoints = await this.globalSearch(typedQuery.query, rootUris);
      
      // 3. 递归搜索
      const results = await this.recursiveSearch(
        startPoints, 
        typedQuery, 
        options.threshold || this.defaultThreshold
      );
      
      allResults.push(...results);
    }
    
    // 4. 去重
    const dedupedResults = this.deduplicateResults(allResults);
    
    // 5. 重排序
    let finalResults = dedupedResults;
    
    if (this.reranker && options.useRerank !== false) {
      finalResults = await this.reranker.rerank(
        typedQueries[0]?.query || '', 
        dedupedResults
      );
    }
    
    // 6. 分类结果
    const findResult = this.classifyResults(finalResults);
    
    // 更新统计
    const searchTime = Date.now() - startTime;
    this.stats.totalSearches++;
    this.stats.totalResults += finalResults.length;
    this.stats.avgSearchTime = 
      (this.stats.avgSearchTime * (this.stats.totalSearches - 1) + searchTime) / 
      this.stats.totalSearches;
    this.stats.avgResultsPerSearch = 
      this.stats.totalResults / this.stats.totalSearches;
    
    logger.info(`[HierarchicalRetriever] 检索完成，返回 ${finalResults.length} 个结果，耗时 ${searchTime}ms`);
    
    return findResult;
  }
  
  /**
   * 获取根目录
   */
  getRootUris(contextType, options) {
    const userId = options.userId;
    const agentId = options.agentId;
    
    switch (contextType) {
      case 'MEMORY':
        return [
          `viking://user/${userId}/memories/`,
          `viking://agent/${agentId}/memories/`
        ].filter(Boolean);
      
      case 'RESOURCE':
        return ['viking://resources/'];
      
      case 'SKILL':
        return [`viking://agent/${agentId}/skills/`].filter(Boolean);
      
      default:
        return [
          `viking://user/${userId}/memories/`,
          `viking://agent/${agentId}/memories/`,
          'viking://resources/',
          `viking://agent/${agentId}/skills/`
        ].filter(Boolean);
    }
  }
  
  /**
   * 全局搜索
   */
  async globalSearch(query, rootUris) {
    if (!this.vectorStore) {
      logger.warn('[HierarchicalRetriever] 向量存储未配置，返回根目录');
      return rootUris.map(uri => ({ uri, score: 1.0 }));
    }
    
    const startPoints = [];
    
    for (const rootUri of rootUris) {
      try {
        const results = await this.vectorStore.search(query, {
          filter: { uriPrefix: rootUri },
          limit: this.globalSearchTopK
        });
        
        for (const result of results) {
          startPoints.push({
            uri: result.uri,
            score: result.score
          });
        }
      } catch (error) {
        logger.error(`[HierarchicalRetriever] 全局搜索失败: ${rootUri}`, error);
      }
    }
    
    // 如果没有结果，返回根目录
    if (startPoints.length === 0) {
      return rootUris.map(uri => ({ uri, score: 1.0 }));
    }
    
    return startPoints;
  }
  
  /**
   * 递归搜索
   */
  async recursiveSearch(startPoints, typedQuery, threshold) {
    const queue = new PriorityQueue();
    const collected = [];
    const visited = new Set();
    let unchangedRounds = 0;
    let lastTopK = [];
    
    // 初始化队列
    for (const point of startPoints) {
      queue.push(new PriorityQueueItem(point.uri, point.score));
    }
    
    while (queue.length > 0 && unchangedRounds < this.maxConvergenceRounds) {
      const current = queue.pop();
      
      if (!current || visited.has(current.uri)) {
        continue;
      }
      
      visited.add(current.uri);
      
      // 搜索子项
      const children = await this.searchChildren(current.uri, typedQuery.query);
      
      for (const child of children) {
        if (visited.has(child.uri)) {
          continue;
        }
        
        // 分数传播
        const finalScore = 
          this.scorePropagationAlpha * child.score + 
          this.scorePropagationAlpha * current.score;
        
        if (finalScore >= threshold) {
          collected.push(new MatchedContext({
            uri: child.uri,
            contextType: typedQuery.contextType,
            isLeaf: child.isFile,
            abstract: child.abstract || '',
            overview: child.overview || '',
            score: finalScore,
            metadata: child.metadata || {}
          }));
          
          // 如果是目录，继续递归
          if (!child.isFile) {
            queue.push(new PriorityQueueItem(child.uri, finalScore));
          }
        }
      }
      
      // 收敛检测
      const currentTopK = collected
        .sort((a, b) => b.score - a.score)
        .slice(0, 10)
        .map(r => r.uri);
      
      if (JSON.stringify(currentTopK) === JSON.stringify(lastTopK)) {
        unchangedRounds++;
      } else {
        unchangedRounds = 0;
      }
      
      lastTopK = currentTopK;
    }
    
    return collected;
  }
  
  /**
   * 搜索子项
   */
  async searchChildren(parentUri, query) {
    if (!this.storage) {
      logger.warn('[HierarchicalRetriever] 存储未配置');
      return [];
    }
    
    try {
      // 列出子项
      const children = await this.storage.ls(parentUri);
      
      // 向量搜索
      if (this.vectorStore) {
        const results = await this.vectorStore.search(query, {
          filter: { uriPrefix: parentUri },
          limit: 20
        });
        
        // 合并结果
        const childMap = new Map();
        
        for (const child of children) {
          childMap.set(child.uri, {
            ...child,
            score: 0
          });
        }
        
        for (const result of results) {
          if (childMap.has(result.uri)) {
            childMap.get(result.uri).score = result.score;
          } else {
            childMap.set(result.uri, result);
          }
        }
        
        return Array.from(childMap.values());
      }
      
      return children;
      
    } catch (error) {
      logger.error(`[HierarchicalRetriever] 搜索子项失败: ${parentUri}`, error);
      return [];
    }
  }
  
  /**
   * 去重结果
   */
  deduplicateResults(results) {
    const seen = new Map();
    
    for (const result of results) {
      if (!seen.has(result.uri)) {
        seen.set(result.uri, result);
      } else {
        // 保留分数更高的
        const existing = seen.get(result.uri);
        if (result.score > existing.score) {
          seen.set(result.uri, result);
        }
      }
    }
    
    return Array.from(seen.values());
  }
  
  /**
   * 分类结果
   */
  classifyResults(results) {
    const memories = [];
    const resources = [];
    const skills = [];
    
    for (const result of results) {
      const uri = new VikingURI(result.uri);
      
      if (uri.scope === 'user' || uri.scope === 'agent' && uri.path.includes('memories')) {
        memories.push(result);
      } else if (uri.scope === 'resources') {
        resources.push(result);
      } else if (uri.scope === 'agent' && uri.path.includes('skills')) {
        skills.push(result);
      }
    }
    
    return new FindResult({
      memories,
      resources,
      skills,
      total: results.length
    });
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return { ...this.stats };
  }
}

/**
 * 获取层级检索器实例
 */
let defaultRetriever = null;

export function getHierarchicalRetriever(options = {}) {
  if (!defaultRetriever) {
    defaultRetriever = new HierarchicalRetriever(options);
  }
  return defaultRetriever;
}

export default HierarchicalRetriever;
