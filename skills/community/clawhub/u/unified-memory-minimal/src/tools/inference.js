/**
 * Memory Inference - 关联推理增强
 * 
 * 功能:
 * - 向量搜索 + 图谱路径扩展的联合推理
 * - 实体上下文链获取
 * - 智能缓存优化
 * 
 * Ported from memory_inference.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const ONTOLOGY_DIR = join(MEMORY_DIR, 'ontology');
const GRAPH_FILE = join(ONTOLOGY_DIR, 'graph.jsonl');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';
const CACHE_TTL = 300; // seconds

// Relation weights
const RELATION_WEIGHTS = {
  'participates_in': 1.0,
  'owns': 1.0,
  'depends_on': 0.9,
  'related_to': 0.8,
  'uses': 0.8,
  'prefers': 0.9,
  'works_on': 0.9,
  'manages': 0.9,
  'created': 0.85,
  'completed': 0.85,
  'updated': 0.7,
  'mentioned_in': 0.6
};

// Entity type priority
const ENTITY_PRIORITY = {
  'project': 1.0,
  'task': 0.95,
  'person': 0.9,
  'decision': 0.9,
  'preference': 0.85,
  'event': 0.8,
  'tool': 0.75,
  'fact': 0.7
};

// ============================================================
// CacheManager
// ============================================================

class CacheManager {
  constructor(ttlSeconds = 300) {
    this.cache = new Map();
    this.ttl = ttlSeconds * 1000;
  }

  _makeKey(...args) {
    return JSON.stringify({ args, time: Date.now() });
  }

  get(...args) {
    const key = this._makeKey(...args.slice(0, -1));
    if (this.cache.has(key)) {
      const entry = this.cache.get(key);
      if (Date.now() - entry.time < this.ttl) {
        return entry.data;
      }
      this.cache.delete(key);
    }
    return null;
  }

  set(data, ...args) {
    const key = this._makeKey(...args);
    this.cache.set(key, { data, time: Date.now() });
  }

  clear() {
    this.cache.clear();
  }

  stats() {
    const now = Date.now();
    let valid = 0;
    for (const entry of this.cache.values()) {
      if (now - entry.time < this.ttl) valid++;
    }
    return { total: this.cache.size, valid, expired: this.cache.size - valid };
  }
}

// ============================================================
// SimpleOntologyGraph
// ============================================================

class SimpleOntologyGraph {
  constructor(graphFile) {
    this.graphFile = graphFile;
    /** @type {Map<string, object>} */
    this.entities = new Map();
    /** @type {Array<object>} */
    this.relations = [];
    this._load();
  }

  _load() {
    if (!existsSync(this.graphFile)) return;
    try {
      const content = readFileSync(this.graphFile, 'utf-8');
      const lines = content.split('\n').filter(Boolean);
      for (const line of lines) {
        try {
          const data = JSON.parse(line);
          if (data.op === 'create') {
            const entity = data.entity || {};
            this.entities.set(entity.id, entity);
          } else if (data.op === 'relate') {
            this.relations.push({
              from: data.from,
              rel: data.rel,
              to: data.to,
              created: data.created
            });
          }
        } catch { /* skip */ }
      }
    } catch { /* ignore */ }
  }

  getEntity(entityId) {
    return this.entities.get(entityId) || null;
  }

  getRelationsFrom(entityId) {
    return this.relations.filter(r => r.from === entityId);
  }

  getRelationsTo(entityId) {
    return this.relations.filter(r => r.to === entityId);
  }

  traverse(startId, depth = 2) {
    const result = {
      center: this.entities.get(startId) || null,
      nodes: [],
      edges: []
    };

    if (!this.entities.has(startId)) return result;

    const visited = new Set([startId]);
    let frontier = [startId];

    for (let d = 0; d < depth; d++) {
      const newFrontier = [];
      for (const nodeId of frontier) {
        // Outgoing
        for (const rel of this.getRelationsFrom(nodeId)) {
          result.edges.push({ from: nodeId, rel: rel.rel, to: rel.to });
          if (this.entities.has(rel.to) && !visited.has(rel.to)) {
            visited.add(rel.to);
            newFrontier.push(rel.to);
            result.nodes.push(this.entities.get(rel.to));
          }
        }
        // Incoming
        for (const rel of this.getRelationsTo(nodeId)) {
          result.edges.push({ from: rel.from, rel: rel.rel, to: nodeId });
          if (this.entities.has(rel.from) && !visited.has(rel.from)) {
            visited.add(rel.from);
            newFrontier.push(rel.from);
            result.nodes.push(this.entities.get(rel.from));
          }
        }
      }
      frontier = newFrontier;
    }

    return result;
  }
}

// ============================================================
// MemoryInference
// ============================================================

export class MemoryInference {
  constructor(cacheTtl = 300) {
    this.cache = new CacheManager(cacheTtl);
    this.graph = new SimpleOntologyGraph(GRAPH_FILE);
    this.memories = this._loadMemories();
  }

  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      return getAllMemories();
    } catch {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          return Array.isArray(data) ? data : (data.memories || []);
        } catch { /* ignore */ }
      }
      return [];
    }
  }

  async _getEmbedding(text) {
    try {
      const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }),
        signal: AbortSignal.timeout(10000)
      });
      if (response.ok) {
        const data = await response.json();
        return data.embedding || null;
      }
    } catch { /* ignore */ }
    return null;
  }

  async inferRelated(query, topK = 5, maxDepth = 2) {
    const cached = this.cache.get('inferRelated', query, topK, maxDepth);
    if (cached) return cached;

    const startTime = Date.now();

    // 1. Vector search (fallback to keyword)
    const vectorResults = this._vectorSearch(query, topK * 2);

    // 2. Graph expansion
    const graphExpansion = [];
    const seenEntityIds = new Set();
    for (const result of vectorResults) {
      const entityId = result.entityId ||
        (this.graph.entities.size > 0 ? this._findEntityId(result.text || '') : null);
      if (entityId && !seenEntityIds.has(entityId)) {
        seenEntityIds.add(entityId);
        const paths = this._expandFromEntity(entityId, maxDepth);
        graphExpansion.push(...paths);
      }
    }

    // 3. Merge results
    const merged = this._mergeResults(vectorResults, graphExpansion, topK);

    const result = {
      vector_results: vectorResults.slice(0, topK),
      graph_expansion: graphExpansion.slice(0, topK),
      merged,
      stats: {
        vector_count: vectorResults.length,
        expansion_count: graphExpansion.length,
        merged_count: merged.length,
        time_ms: Date.now() - startTime
      }
    };

    this.cache.set(result, 'inferRelated', query, topK, maxDepth);
    return result;
  }

  _vectorSearch(query, limit = 10) {
    const results = [];
    const queryLower = query.toLowerCase();
    const queryWords = new Set(queryLower.split(/\s+/));

    for (const mem of this.memories) {
      const text = mem.text || '';
      let score = 0;
      if (text.toLowerCase().includes(queryLower)) {
        score = 1.0;
      } else {
        const textWords = new Set(text.toLowerCase().split(/\s+/));
        const overlap = [...queryWords].filter(w => textWords.has(w)).length;
        score = overlap / Math.max(queryWords.size, 1);
      }
      if (score > 0.1) {
        results.push({
          id: mem.id,
          text,
          category: mem.category || 'unknown',
          importance: mem.importance || 0.5,
          score,
          source: 'keyword',
          entityId: null
        });
      }
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }

  _findEntityId(text) {
    if (!this.graph.entities.size) return null;
    const textLower = text.toLowerCase();
    for (const [id, entity] of this.graph.entities) {
      const props = entity.properties || {};
      const name = props.name || '';
      if (name && name.toLowerCase().includes(textLower.slice(0, 10))) {
        return id;
      }
    }
    return null;
  }

  _expandFromEntity(entityId, maxDepth = 2) {
    if (!this.graph.entities.size) return [];
    try {
      const result = this.graph.traverse(entityId, maxDepth);
      return (result.nodes || []).map(node => ({
        entity_id: node.id,
        type: node.type || 'unknown',
        name: (node.properties || {}).name || node.id,
        text: (node.properties || {}).description || '',
        weight: ENTITY_PRIORITY[node.type] || 0.5,
        source: 'graph_expansion',
        relation_depth: 1
      }));
    } catch {
      return [];
    }
  }

  _mergeResults(vectorResults, graphExpansion, topK) {
    const mergedMap = new Map();

    for (const r of vectorResults) {
      const key = r.text || '';
      mergedMap.set(key, {
        text: r.text,
        entity_id: r.entityId,
        category: r.category || 'unknown',
        importance: r.importance || 0.5,
        vector_score: r.score,
        graph_weight: 0,
        sources: ['vector']
      });
    }

    for (const r of graphExpansion) {
      const key = r.text || r.name || '';
      if (mergedMap.has(key)) {
        mergedMap.get(key).graph_weight = r.weight;
        mergedMap.get(key).sources.push('graph');
      } else {
        mergedMap.set(key, {
          text: r.text || r.name || '',
          entity_id: r.entity_id,
          type: r.type,
          category: r.type || 'unknown',
          importance: r.weight || 0.5,
          vector_score: 0,
          graph_weight: r.weight || 0.5,
          sources: ['graph']
        });
      }
    }

    const scored = [];
    for (const item of mergedMap.values()) {
      const vectorScore = Math.min(item.vector_score, 1);
      const combinedScore =
        vectorScore * 0.4 +
        item.graph_weight * 0.4 +
        item.importance * 0.2;
      scored.push({
        ...item,
        combined_score: Math.round(combinedScore * 1000) / 1000
      });
    }

    scored.sort((a, b) => b.combined_score - a.combined_score);
    return scored.slice(0, topK);
  }

  getContextChain(entityId, entityType = null) {
    const cached = this.cache.get('contextChain', entityId, entityType);
    if (cached) return cached;

    if (!this.graph.entities.size) return [];

    let entity = this.graph.getEntity(entityId);
    if (!entity) {
      entity = this._findEntityByName(entityId);
      if (entity) entityId = entity.id;
    }

    if (!entity) return [];

    const type = entityType || entity.type || 'unknown';
    let chain = [];

    if (type === 'project') chain = this._getProjectContext(entityId);
    else if (type === 'person') chain = this._getPersonContext(entityId);
    else if (type === 'task') chain = this._getTaskContext(entityId);
    else chain = this._getGenericContext(entityId);

    this.cache.set(chain, 'contextChain', entityId, entityType);
    return chain;
  }

  _findEntityByName(name) {
    if (!this.graph.entities.size) return null;
    const nameLower = name.toLowerCase();
    for (const entity of this.graph.entities.values()) {
      const props = entity.properties || {};
      const entityName = props.name || '';
      if (entityName.toLowerCase() === nameLower) return entity;
    }
    return null;
  }

  _getProjectContext(projectId) {
    const context = [];
    const project = this.graph.getEntity(projectId);
    if (project) {
      context.push({
        type: 'project',
        role: 'center',
        name: (project.properties || {}).name || projectId,
        status: (project.properties || {}).status || 'unknown'
      });
    }
    for (const rel of this.graph.getRelationsFrom(projectId)) {
      const person = this.graph.getEntity(rel.rel_to);
      if (person) {
        context.push({
          type: 'person',
          role: rel.rel || 'participant',
          name: (person.properties || {}).name || rel.rel_to
        });
      }
    }
    return context;
  }

  _getPersonContext(personId) {
    const context = [];
    const person = this.graph.getEntity(personId);
    if (person) {
      context.push({
        type: 'person',
        role: 'center',
        name: (person.properties || {}).name || personId
      });
    }
    for (const rel of this.graph.getRelationsFrom(personId)) {
      const target = this.graph.getEntity(rel.to);
      if (target) {
        context.push({
          type: target.type || 'unknown',
          role: rel.rel,
          name: (target.properties || {}).name || rel.to
        });
      }
    }
    return context;
  }

  _getTaskContext(taskId) {
    const context = [];
    const task = this.graph.getEntity(taskId);
    if (task) {
      context.push({
        type: 'task',
        role: 'center',
        name: (task.properties || {}).name || taskId,
        status: (task.properties || {}).status || 'unknown'
      });
    }
    return context;
  }

  _getGenericContext(entityId) {
    const context = [];
    const entity = this.graph.getEntity(entityId);
    if (entity) {
      context.push({
        type: entity.type || 'unknown',
        role: 'center',
        name: (entity.properties || {}).name || entityId
      });
    }
    return context;
  }

  getStats() {
    return {
      cache: this.cache.stats(),
      graph_entities: this.graph.entities.size,
      graph_relations: this.graph.relations.length,
      memories_loaded: this.memories.length
    };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdInference(command, args) {
  const inference = new MemoryInference(parseInt(args.cacheTtl) || 300);

  switch (command) {
    case 'search': {
      if (!args.query) return { error: '请提供查询内容' };
      const result = await inference.inferRelated(
        args.query,
        parseInt(args.limit) || 10,
        parseInt(args.depth) || 2
      );
      if (args.json) return { type: 'json', data: result };
      const lines = [
        `🔍 联合推理搜索: "${args.query}"`,
        `   向量结果: ${result.stats.vector_count} 条`,
        `   图谱扩展: ${result.stats.expansion_count} 条`,
        `   合并结果: ${result.stats.merged_count} 条`,
        `   耗时: ${result.stats.time_ms} ms\n`,
        `📊 Top 合并结果:`
      ];
      for (let i = 0; i < Math.min(5, result.merged.length); i++) {
        const item = result.merged[i];
        const sources = (item.sources || []).join('+');
        lines.push(`   ${i + 1}. [${sources}] ${(item.text || '').slice(0, 60)}... (score: ${item.combined_score.toFixed(3)})`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'context':
    case 'chain': {
      if (!args.query) return { error: '请提供实体ID' };
      const chain = inference.getContextChain(args.query, args.type);
      if (args.json) return { type: 'json', data: chain };
      if (!chain.length) return { type: 'text', text: '未找到上下文信息' };
      const lines = [`📋 实体上下文链: ${args.query}\n`];
      const center = chain.find(c => c.role === 'center');
      if (center) {
        lines.push(`🎯 ${(center.type || 'Entity').toUpperCase()}: ${center.name}`);
        if (center.status) lines.push(`   状态: ${center.status}`);
        lines.push('');
      }
      const related = chain.filter(c => c.role !== 'center');
      if (related.length) {
        lines.push('🔗 关联信息:');
        for (const item of related) {
          lines.push(`   - [${item.type}/${item.role}] ${item.name}${item.status ? ` [${item.status}]` : ''}`);
        }
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'related': {
      if (!args.query) return { error: '请提供查询内容' };
      const chain = inference.getContextChain(args.query, args.type);
      if (args.json) return { type: 'json', data: chain };
      return { type: 'text', text: JSON.stringify(chain, null, 2) };
    }

    case 'stats': {
      const stats = inference.getStats();
      if (args.json) return { type: 'json', data: stats };
      return {
        type: 'text',
        text: `📊 Memory Inference 引擎统计\n` +
          `   缓存: ${stats.cache.valid} 有效 / ${stats.cache.total} 总计\n` +
          `   图谱实体: ${stats.graph_entities}\n` +
          `   图谱关系: ${stats.graph_relations}\n` +
          `   加载记忆: ${stats.memories_loaded}`
      };
    }

    case 'cache-clear': {
      inference.cache.clear();
      return { type: 'text', text: '✅ 缓存已清空' };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { MemoryInference, cmdInference };
