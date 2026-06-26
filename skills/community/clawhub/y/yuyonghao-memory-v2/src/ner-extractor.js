/**
 * Memory V2 - 实体提取模块
 * 基于 Transformers.js 的中文命名实体识别（NER）
 */

import { pipeline } from '@xenova/transformers';
import { EventEmitter } from 'events';

/**
 * 实体提取器类
 */
export class NERExtractor extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.model - NER 模型名称
   */
  constructor(config = {}) {
    super();
    this.modelName = config.model || 'Xenova/bert-base-chinese-ner';
    this.ner = null;
    this.initialized = false;
    
    // 实体类型映射
    this.entityTypes = {
      'B-PER': 'PERSON',
      'I-PER': 'PERSON',
      'B-LOC': 'LOCATION',
      'I-LOC': 'LOCATION',
      'B-ORG': 'ORGANIZATION',
      'I-ORG': 'ORGANIZATION',
      'B-MISC': 'MISC',
      'I-MISC': 'MISC'
    };
  }

  /**
   * 初始化 NER 模型
   */
  async initialize() {
    if (this.initialized) {
      return;
    }

    this.emit('initializing');
    console.log(`[NERExtractor] Loading NER model: ${this.modelName}`);
    
    this.ner = await pipeline('token-classification', this.modelName);
    
    console.log('[NERExtractor] NER model loaded');
    this.initialized = true;
    this.emit('initialized');
  }

  /**
   * 提取实体
   * @param {string} text - 输入文本
   * @returns {Promise<Array<Object>>} - 实体列表
   */
  async extract(text) {
    if (!this.initialized) {
      await this.initialize();
    }

    const result = await this.ner(text);
    
    // 合并连续的 token（同一实体）
    const entities = this.mergeTokens(result);
    
    this.emit('entities-extracted', { count: entities.length });
    return entities;
  }

  /**
   * 合并连续的 token
   */
  mergeTokens(tokens) {
    if (tokens.length === 0) {
      return [];
    }

    const entities = [];
    let currentEntity = null;

    for (const token of tokens) {
      const entityType = this.entityTypes[token.entity];
      
      if (!entityType) {
        // 非实体 token，结束当前实体
        if (currentEntity) {
          entities.push(currentEntity);
          currentEntity = null;
        }
        continue;
      }

      if (token.entity.startsWith('B-')) {
        // 新实体开始
        if (currentEntity) {
          entities.push(currentEntity);
        }
        currentEntity = {
          text: token.word,
          type: entityType,
          score: token.score,
          start: token.start,
          end: token.end
        };
      } else if (token.entity.startsWith('I-') && currentEntity) {
        // 继续当前实体
        currentEntity.text += token.word;
        currentEntity.end = token.end;
        currentEntity.score = (currentEntity.score + token.score) / 2;
      }
    }

    // 添加最后一个实体
    if (currentEntity) {
      entities.push(currentEntity);
    }

    return entities;
  }

  /**
   * 批量提取实体
   * @param {Array<string>} texts - 文本数组
   * @returns {Promise<Array<Array<Object>>>} - 实体列表数组
   */
  async extractBatch(texts) {
    return Promise.all(texts.map(text => this.extract(text)));
  }

  /**
   * 提取并链接到图谱
   * @param {string} text - 输入文本
   * @param {GraphStore} graphStore - 图存储实例
   * @returns {Promise<Array<Object>>} - 链接后的实体
   */
  async extractAndLink(text, graphStore) {
    const entities = await this.extract(text);
    const linkedEntities = [];

    for (const entity of entities) {
      // 在图谱中搜索匹配节点
      const matches = graphStore.searchNodes({
        type: entity.type,
        text: entity.text
      });

      if (matches.length > 0) {
        // 找到匹配，链接到现有节点
        entity.linkedId = matches[0].id;
        entity.isNew = false;
      } else {
        // 未找到，创建新节点
        const nodeId = `entity_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        graphStore.addNode(nodeId, entity.type, {
          name: entity.text,
          source: 'ner-extraction',
          extractedAt: new Date().toISOString()
        });
        
        entity.linkedId = nodeId;
        entity.isNew = true;
      }

      linkedEntities.push(entity);
    }

    return linkedEntities;
  }
}

export default NERExtractor;
