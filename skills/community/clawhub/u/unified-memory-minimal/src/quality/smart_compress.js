/**
 * Smart Compression - 智能压缩
 * 
 * 核心概念：
 * - 不是固定压缩率
 * - 而是保留"关键信息"
 * - 关键实体 + 关键关系 + 可溯源
 * 
 * Ported from memory_smart_compress.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

// Entity patterns
const ENTITY_PATTERNS = {
  person: [
    /[\u4e00-\u9fa5]{2,4}(?:先生|女士|总|经理|总监|工程师|设计师|产品经理|CEO|CTO|CFO)/g,
    /(?:刘总|张总|王总|李总)/g
  ],
  project: [
    /项目[：:][^\n]+/g,
    /【[^\]]+】/g,
    /(?:电商|社交|金融|医疗|教育)[网站系统平台]/g
  ],
  tool: [
    /使用[^\s]+(?:框架|库|工具|服务)/g,
    /(?:Python|Java|JS|React|Vue|Node)[^\s]*/g
  ],
  decision: [
    /决定[^\n]+/g,
    /采用[^\n]+/g,
    /选择[^\n]+/g,
    /应该[^\n]+/g
  ],
  metric: [
    /\d+(?:%|倍|次|个|条)/g
  ]
};

// ============================================================
// SmartCompressor
// ============================================================

export class SmartCompressor {
  constructor() {
    this.entityPatterns = ENTITY_PATTERNS;
  }

  /**
   * Extract entities from text
   * @param {string} text
   * @returns {object}
   */
  extractEntities(text) {
    const entities = {};

    for (const [entityType, patterns] of Object.entries(this.entityPatterns)) {
      const found = [];
      for (const pattern of patterns) {
        const matches = text.match(pattern) || [];
        found.push(...matches);
      }
      if (found.length > 0) {
        entities[entityType] = [...new Set(found)].slice(0, 5);
      }
    }

    return entities;
  }

  /**
   * Extract relations from text
   * @param {string} text
   * @returns {string[]}
   */
  extractRelations(text) {
    const relations = [];
    const patterns = [
      /([\u4e00-\u9fa5]+)使用([\u4e00-\u9fa5]+)/g,
      /([\u4e00-\u9fa5]+)决定([\u4e00-\u9fa5]+)/g,
      /([\u4e00-\u9fa5]+)创建([\u4e00-\u9fa5]+)/g,
      /([\u4e00-\u9fa5]+)完成([\u4e00-\u9fa5]+)/g
    ];

    for (const pattern of patterns) {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        relations.push(`${match[1]} -> ${match[2]}`);
      }
    }

    return [...new Set(relations)].slice(0, 10);
  }

  /**
   * Compress memories intelligently
   * @param {Array<object>} memories
   * @param {number} targetSize
   * @returns {object}
   */
  compress(memories, targetSize = 4000) {
    if (!memories || memories.length === 0) {
      return { summary: '', sources: [] };
    }

    // Sort by time (newest first)
    const sorted = [...memories].sort((a, b) => {
      const ta = a.timestamp || a.created_at || '';
      const tb = b.timestamp || b.created_at || '';
      return tb.localeCompare(ta);
    });

    /** @type {Map<string, string[]>} */
    const allEntities = {};
    /** @type {Set<string>} */
    const allRelationsSet = new Set();
    /** @type {Array} */
    const sources = [];

    for (const mem of sorted) {
      const text = mem.text || '';

      // Extract entities
      const entities = this.extractEntities(text);
      for (const [et, ents] of Object.entries(entities)) {
        if (!allEntities[et]) allEntities[et] = [];
        allEntities[et].push(...ents);
      }

      // Extract relations
      const relations = this.extractRelations(text);
      for (const rel of relations) allRelationsSet.add(rel);

      // Record source
      sources.push({
        id: mem.id || '',
        text: text.slice(0, 100),
        category: mem.category || 'unknown',
        timestamp: mem.timestamp || mem.created_at || ''
      });
    }

    // Dedupe
    for (const et of Object.keys(allEntities)) {
      allEntities[et] = [...new Set(allEntities[et])].slice(0, 5);
    }
    const allRelations = [...allRelationsSet].slice(0, 10);

    /** @type {string[]} */
    const parts = [];

    // 1. Key entities
    if (Object.keys(allEntities).length > 0) {
      const entityParts = [];
      for (const [et, ents] of Object.entries(allEntities)) {
        if (ents.length > 0) {
          entityParts.push(`${et}: ${ents.join(', ')}`);
        }
      }
      if (entityParts.length > 0) {
        parts.push('【关键实体】\n' + entityParts.join('\n'));
      }
    }

    // 2. Key relations
    if (allRelations.length > 0) {
      parts.push('【关键关系】\n' + allRelations.slice(0, 5).join('\n'));
    }

    // 3. Recent memories
    const recent = sorted.slice(0, 5);
    if (recent.length > 0) {
      const recentText = recent.map(m =>
        `- [${m.category || '?'}] ${(m.text || '').slice(0, 60)}...`
      ).join('\n');
      parts.push('【最新进展】\n' + recentText);
    }

    // 4. Decisions
    const decisions = sorted.filter(m => (m.category || '') === 'decision');
    if (decisions.length > 0) {
      const decText = decisions.slice(0, 3).map(d =>
        `- ${(d.text || '').slice(0, 60)}...`
      ).join('\n');
      parts.push('【决策记录】\n' + decText);
    }

    let summary = parts.join('\n\n');

    // Truncate if too long
    if (summary.length > targetSize * 4) {
      summary = summary.slice(0, targetSize * 4);
    }

    return {
      summary,
      entities: allEntities,
      relations: allRelations,
      sources: sources.slice(0, 20)
    };
  }

  /**
   * Compress for context (returns string)
   * @param {Array<object>} memories
   * @param {number} maxTokens
   * @returns {string}
   */
  compressForContext(memories, maxTokens = 4000) {
    const result = this.compress(memories, maxTokens);
    return result.summary;
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdSmartCompress(command, args) {
  const compressor = new SmartCompressor();

  switch (command) {
    case 'extract': {
      if (!args.text) return { error: '请提供 --text' };
      const entities = compressor.extractEntities(args.text);
      const relations = compressor.extractRelations(args.text);
      if (args.json) {
        return { type: 'json', data: { entities, relations } };
      }
      return {
        type: 'text',
        text: `📦 实体:\n${JSON.stringify(entities, null, 2)}\n\n🔗 关系:\n${relations.join('\n')}`
      };
    }

    case 'compress': {
      if (!args.text && !args.memories) {
        return { error: '请提供 --text 或 --memories' };
      }
      const result = compressor.compress(args.memories || [{ text: args.text }]);
      if (args.json) {
        return { type: 'json', data: result };
      }
      return {
        type: 'text',
        text: `📝 压缩摘要:\n\n${result.summary}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { SmartCompressor, cmdSmartCompress };
