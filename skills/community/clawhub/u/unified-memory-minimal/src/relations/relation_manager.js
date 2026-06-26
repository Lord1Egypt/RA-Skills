/**
 * 关系管理器 - Relation Manager
 * 借鉴 OpenViking 的关系管理机制
 */

import { logger } from '../utils/logger.js';
import { VikingURI } from '../core/viking_uri.js';

/**
 * 关系类型
 */
export const RELATION_TYPES = {
  RELATED_TO: 'related_to',
  DEPENDS_ON: 'depends_on',
  REFERENCES: 'references',
  EXTENDS: 'extends',
  IMPLEMENTS: 'implements',
  USES: 'uses',
  CONTAINS: 'contains',
  BELONGS_TO: 'belongs_to'
};

/**
 * 关系
 */
export class Relation {
  constructor(options) {
    this.id = options.id || `rel_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.source = options.source;
    this.target = options.target;
    this.type = options.type;
    this.weight = options.weight || 1.0;
    this.metadata = options.metadata || {};
    this.createdAt = Date.now();
  }
  
  toJSON() {
    return {
      id: this.id,
      source: this.source,
      target: this.target,
      type: this.type,
      weight: this.weight,
      metadata: this.metadata,
      createdAt: this.createdAt
    };
  }
}

/**
 * 关系管理器
 */
export class RelationManager {
  constructor(options = {}) {
    this.storage = options.storage;
    this.maxRelations = options.maxRelations || 100;
    
    // 关系索引
    this.relationsBySource = new Map();
    this.relationsByTarget = new Map();
    this.relationsByType = new Map();
    
    // 统计
    this.stats = {
      totalRelations: 0,
      totalLinks: 0,
      totalUnlinks: 0
    };
  }
  
  /**
   * 添加关系
   */
  async link(source, target, type = RELATION_TYPES.RELATED_TO, options = {}) {
    logger.debug(`[RelationManager] 添加关系: ${source} -> ${target} (${type})`);
    
    const relation = new Relation({
      source: source,
      target: target,
      type: type,
      weight: options.weight || 1.0,
      metadata: options.metadata || {}
    });
    
    // 添加到索引
    this.addToIndex(relation);
    
    // 持久化
    if (this.storage) {
      await this.persistRelation(relation);
    }
    
    this.stats.totalRelations++;
    this.stats.totalLinks++;
    
    return relation;
  }
  
  /**
   * 删除关系
   */
  async unlink(source, target, type) {
    logger.debug(`[RelationManager] 删除关系: ${source} -> ${target} (${type})`);
    
    // 查找关系
    const relations = this.findRelations({ source, target, type });
    
    for (const relation of relations) {
      this.removeFromIndex(relation);
      
      // 从存储删除
      if (this.storage) {
        await this.deleteRelation(relation);
      }
      
      this.stats.totalRelations--;
    }
    
    this.stats.totalUnlinks++;
    
    return relations.length;
  }
  
  /**
   * 查询关系
   */
  async relations(uri, options = {}) {
    const direction = options.direction || 'both';  // 'outgoing' | 'incoming' | 'both'
    const type = options.type;
    
    const results = [];
    
    // 出向关系
    if (direction === 'outgoing' || direction === 'both') {
      const outgoing = this.relationsBySource.get(uri) || [];
      
      for (const relation of outgoing) {
        if (!type || relation.type === type) {
          results.push({
            ...relation.toJSON(),
            direction: 'outgoing'
          });
        }
      }
    }
    
    // 入向关系
    if (direction === 'incoming' || direction === 'both') {
      const incoming = this.relationsByTarget.get(uri) || [];
      
      for (const relation of incoming) {
        if (!type || relation.type === type) {
          results.push({
            ...relation.toJSON(),
            direction: 'incoming'
          });
        }
      }
    }
    
    // 限制数量
    const limit = options.limit || this.maxRelations;
    
    return results.slice(0, limit);
  }
  
  /**
   * 查找关系
   */
  findRelations(query) {
    const results = [];
    
    if (query.source) {
      const relations = this.relationsBySource.get(query.source) || [];
      
      for (const relation of relations) {
        if (this.matchesQuery(relation, query)) {
          results.push(relation);
        }
      }
    } else if (query.target) {
      const relations = this.relationsByTarget.get(query.target) || [];
      
      for (const relation of relations) {
        if (this.matchesQuery(relation, query)) {
          results.push(relation);
        }
      }
    } else if (query.type) {
      const relations = this.relationsByType.get(query.type) || [];
      
      for (const relation of relations) {
        if (this.matchesQuery(relation, query)) {
          results.push(relation);
        }
      }
    }
    
    return results;
  }
  
  /**
   * 匹配查询
   */
  matchesQuery(relation, query) {
    if (query.source && relation.source !== query.source) return false;
    if (query.target && relation.target !== query.target) return false;
    if (query.type && relation.type !== query.type) return false;
    return true;
  }
  
  /**
   * 添加到索引
   */
  addToIndex(relation) {
    // 按源索引
    if (!this.relationsBySource.has(relation.source)) {
      this.relationsBySource.set(relation.source, []);
    }
    this.relationsBySource.get(relation.source).push(relation);
    
    // 按目标索引
    if (!this.relationsByTarget.has(relation.target)) {
      this.relationsByTarget.set(relation.target, []);
    }
    this.relationsByTarget.get(relation.target).push(relation);
    
    // 按类型索引
    if (!this.relationsByType.has(relation.type)) {
      this.relationsByType.set(relation.type, []);
    }
    this.relationsByType.get(relation.type).push(relation);
  }
  
  /**
   * 从索引删除
   */
  removeFromIndex(relation) {
    // 从源索引删除
    const sourceRelations = this.relationsBySource.get(relation.source);
    if (sourceRelations) {
      const idx = sourceRelations.findIndex(r => r.id === relation.id);
      if (idx >= 0) {
        sourceRelations.splice(idx, 1);
      }
    }
    
    // 从目标索引删除
    const targetRelations = this.relationsByTarget.get(relation.target);
    if (targetRelations) {
      const idx = targetRelations.findIndex(r => r.id === relation.id);
      if (idx >= 0) {
        targetRelations.splice(idx, 1);
      }
    }
    
    // 从类型索引删除
    const typeRelations = this.relationsByType.get(relation.type);
    if (typeRelations) {
      const idx = typeRelations.findIndex(r => r.id === relation.id);
      if (idx >= 0) {
        typeRelations.splice(idx, 1);
      }
    }
  }
  
  /**
   * 持久化关系
   */
  async persistRelation(relation) {
    if (!this.storage) return;
    
    try {
      const sourceUri = new VikingURI(relation.source);
      const relationsFile = sourceUri.parent.join('.relations.json');
      
      // 读取现有关系
      let relations = [];
      try {
        const data = await this.storage.read(relationsFile.uri);
        relations = JSON.parse(data);
      } catch (error) {
        // 文件不存在
      }
      
      // 添加新关系
      relations.push(relation.toJSON());
      
      // 写入
      await this.storage.write(relationsFile.uri, JSON.stringify(relations, null, 2));
      
    } catch (error) {
      logger.error('[RelationManager] 持久化关系失败:', error);
    }
  }
  
  /**
   * 删除关系
   */
  async deleteRelation(relation) {
    if (!this.storage) return;
    
    try {
      const sourceUri = new VikingURI(relation.source);
      const relationsFile = sourceUri.parent.join('.relations.json');
      
      // 读取现有关系
      let relations = [];
      try {
        const data = await this.storage.read(relationsFile.uri);
        relations = JSON.parse(data);
      } catch (error) {
        return;
      }
      
      // 删除关系
      relations = relations.filter(r => r.id !== relation.id);
      
      // 写入
      await this.storage.write(relationsFile.uri, JSON.stringify(relations, null, 2));
      
    } catch (error) {
      logger.error('[RelationManager] 删除关系失败:', error);
    }
  }
  
  /**
   * 加载关系
   */
  async loadRelations(uri) {
    if (!this.storage) return;
    
    try {
      const vikingUri = new VikingURI(uri);
      const relationsFile = vikingUri.join('.relations.json');
      
      const data = await this.storage.read(relationsFile.uri);
      const relations = JSON.parse(data);
      
      for (const r of relations) {
        const relation = new Relation(r);
        this.addToIndex(relation);
        this.stats.totalRelations++;
      }
      
    } catch (error) {
      // 文件不存在，忽略
    }
  }
  
  /**
   * 获取相关上下文
   */
  async getRelatedContexts(uri, options = {}) {
    const relations = await this.relations(uri, options);
    
    const contexts = [];
    
    for (const relation of relations) {
      const relatedUri = relation.direction === 'outgoing' ? 
        relation.target : relation.source;
      
      contexts.push({
        uri: relatedUri,
        relation: relation.type,
        weight: relation.weight,
        direction: relation.direction
      });
    }
    
    return contexts;
  }
  
  /**
   * 批量添加关系
   */
  async batchLink(links) {
    const results = [];
    
    for (const link of links) {
      const relation = await this.link(
        link.source,
        link.target,
        link.type,
        link.options
      );
      
      results.push(relation);
    }
    
    return results;
  }
  
  /**
   * 清除所有关系
   */
  clear() {
    this.relationsBySource.clear();
    this.relationsByTarget.clear();
    this.relationsByType.clear();
    this.stats.totalRelations = 0;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      uniqueSources: this.relationsBySource.size,
      uniqueTargets: this.relationsByTarget.size,
      relationTypes: this.relationsByType.size
    };
  }
}

/**
 * 获取关系管理器实例
 */
let defaultManager = null;

export function getRelationManager(options = {}) {
  if (!defaultManager) {
    defaultManager = new RelationManager(options);
  }
  return defaultManager;
}

export default RelationManager;
