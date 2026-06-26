/**
 * Memory Graph - Knowledge Graph from Memories
 * 
 * Builds a knowledge graph by extracting entities and relationships from memories.
 * Node types: person, project, tool, time, action
 * Graph stored as JSON: { nodes: [], edges: [] }
 * 
 * @module graph/graph
 */

import { getAllMemories, getMemory } from '../storage.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';
import { dirname } from 'path';
import { extractEntities } from './entity.js';
import { extractRelations, buildAdjacencyList } from './relation.js';
import {
  loadGraph,
  saveGraph as storeGraph,
  addEntity as gsAddEntity,
  addRelation as gsAddRelation,
  findEntity,
  findEntityById,
  getNeighbors as gsGetNeighbors,
  queryGraph,
  getGraphStats,
  mergeIntoGraph,
  clearGraph as gsClearGraph,
  getGraphStats as gsGetStats,
} from './graph_store.js';

// Use configurable entity types from entity_config.js
import { loadEntityConfig, DEFAULT_ENTITY_TYPES } from './entity_config.js';

/** @type {Record<string, string>} */
let ENTITY_COLORS = {};

/** @type {Map<string, EntityType>} */
let ENTITY_TYPES = {};

/**
 * Initialize entity types from config (lazy load)
 */
function initEntityTypes() {
  if (Object.keys(ENTITY_TYPES).length === 0) {
    try {
      const config = loadEntityConfig();
      // Build ENTITY_TYPES.map from config.keywords
      for (const [type, def] of Object.entries(config)) {
        if (!ENTITY_TYPES[type]) ENTITY_TYPES[type] = [];
        if (def.keywords) ENTITY_TYPES[type].push(...def.keywords);
        ENTITY_COLORS[type] = def.color || '#94a3b8';
      }
    } catch {
      // Fallback to defaults
      ENTITY_COLORS = {
        person: '#667eea',
        project: '#10b981',
        tool: '#f59e0b',
        time: '#ef4444',
        action: '#8b5cf6',
      };
      ENTITY_TYPES = {
        person: ['用户', '刘总', '我', '你', '他', '她'],
        project: ['项目', '龙宫', '官网', '重构', '开发'],
        tool: ['飞书', '微信', 'QQ', '钉钉', 'Slack'],
        time: ['今天', '明天', '下周', '月', '日'],
        action: ['喜欢', '使用', '决定', '创建', '完成'],
      };
    }
  }
  return { ENTITY_TYPES, ENTITY_COLORS };
}

/**
 * @typedef {Object} Entity
 * @property {string} name
 * @property {string} type
 * @property {string} text
 * @property {string} [memory_id]
 */

/**
 * @typedef {Object} Relation
 * @property {string} source
 * @property {string} target
 * @property {string} relation
 * @property {string} memory_id
 */

/**
 * @typedef {Object} KnowledgeGraph
 * @property {number} memories_count
 * @property {Entity[]} entities
 * @property {number} entities_count
 * @property {Record<string, number>} entity_types
 * @property {Relation[]} relations
 * @property {number} relations_count
 * @property {string} built_at
 */

/**
 * @typedef {Object} VisNode
 * @property {string} id
 * @property {string} label
 * @property {string} type
 * @property {string} color
 */

/**
 * @typedef {Object} VisEdge
 * @property {string} from
 * @property {string} to
 * @property {string} label
 */

/**
 * Extract entities from a single memory text.
 * Uses configurable entity types from entity_config.js
 * @param {string} text
 * @returns {Entity[]}
 */
export function extractEntitiesFromText(text) {
  /** @type {Entity[]} */
  const entities = [];
  const { ENTITY_TYPES: etypes, ENTITY_COLORS: ecolors } = initEntityTypes();

  for (const [entityType, keywords] of Object.entries(etypes)) {
    for (const keyword of keywords) {
      if (text.includes(keyword)) {
        entities.push({ name: keyword, type: entityType, text, color: ecolors[entityType] });
      }
    }
  }

  return entities;
}

/**
 * Extract entities using the new hybrid (rule + LLM) entity extractor.
 * @param {string} text
 * @param {object} options
 * @returns {Promise<Array<{ id: string, name: string, type: string, method: string }>>}
 */
export async function extractEntitiesHybrid(text, options = {}) {
  return extractEntities(text, options);
}

/**
 * Extract relations from a list of memories.
 * Supports: "喜欢", "使用", "决定" relations.
 * @param {Array<{id: string, text: string}>} memories
 * @returns {Relation[]}
 */
export function extractRelationsFromMemories(memories) {
  /** @type {Relation[]} */
  const relations = [];

  for (const m of memories) {
    const text = m.text || '';

    // "喜欢" relation
    if (text.includes('喜欢') || text.includes('偏好') || text.includes('爱用')) {
      const entities = extractEntitiesFromText(text);
      const person = entities.find((e) => e.type === 'person');
      const tool = entities.find((e) => e.type === 'tool');

      if (person && tool) {
        relations.push({
          source: person.name,
          target: tool.name,
          relation: '喜欢',
          memory_id: m.id,
        });
      }
    }

    // "使用" relation
    if (text.includes('使用') || text.includes('用')) {
      const entities = extractEntitiesFromText(text);
      const person = entities.find((e) => e.type === 'person');
      const tool = entities.find((e) => e.type === 'tool');
      const project = entities.find((e) => e.type === 'project');

      if (person) {
        const target = tool || project;
        if (target) {
          relations.push({
            source: person.name,
            target: target.name,
            relation: '使用',
            memory_id: m.id,
          });
        }
      }
    }

    // "决定" relation
    if (text.includes('决定') || text.includes('确定') || text.includes('选择')) {
      const entities = extractEntitiesFromText(text);
      const person = entities.find((e) => e.type === 'person');
      const project = entities.find((e) => e.type === 'project');
      const tool = entities.find((e) => e.type === 'tool');

      if (person) {
        const target = project || tool;
        if (target) {
          relations.push({
            source: person.name,
            target: target.name,
            relation: '决定',
            memory_id: m.id,
          });
        }
      }
    }
  }

  return relations;
}

/**
 * Search for context relevant to a query.
 * Finds memories matching keywords and extracts their entities and relations.
 * @param {string} query
 * @param {number} [limit=5]
 * @returns {{
 *   query: string,
 *   memories_count: number,
 *   entities: Entity[],
 *   relations: Relation[]
 * }}
 */
export function searchContext(query, limit = 5) {
  const memories = getAllMemories();
  const queryLower = query.toLowerCase();
  const queryTerms = queryLower.split(/\s+/).filter(Boolean);

  // Find relevant memories
  const relevantMemories = memories.filter((m) => {
    const textLower = (m.text || '').toLowerCase();
    return queryTerms.some((kw) => textLower.includes(kw));
  });

  // Extract entities from relevant memories
  /** @type {Entity[]} */
  const allEntities = [];
  for (const m of relevantMemories.slice(0, limit)) {
    const entities = extractEntitiesFromText(m.text || '');
    for (const e of entities) {
      allEntities.push({ ...e, memory_id: m.id, text: (m.text || '').slice(0, 100) });
    }
  }

  // Deduplicate by name
  /** @type {Entity[]} */
  const uniqueEntities = [];
  /** @type {Set<string>} */
  const seen = new Set();
  for (const e of allEntities) {
    if (e.name && !seen.has(e.name)) {
      seen.add(e.name);
      uniqueEntities.push(e);
    }
  }

  // Extract relations from relevant memories
  const relations = extractRelationsFromMemories(relevantMemories);

  return {
    query,
    memories_count: relevantMemories.length,
    entities: uniqueEntities.slice(0, limit * 2),
    relations: relations.slice(0, limit),
  };
}

/**
 * Build the full knowledge graph from all memories.
 * @returns {KnowledgeGraph}
 */
export function buildGraph() {
  const memories = getAllMemories();

  // Extract all entities
  /** @type {Entity[]} */
  const allEntities = [];
  for (const m of memories) {
    const entities = extractEntitiesFromText(m.text || '');
    for (const e of entities) {
      allEntities.push({ ...e, memory_id: m.id });
    }
  }

  // Extract relations
  const relations = extractRelationsFromMemories(memories);

  // Count by type
  /** @type {Record<string, number>} */
  const entityTypes = {};
  for (const e of allEntities) {
    const t = e.type || 'unknown';
    entityTypes[t] = (entityTypes[t] || 0) + 1;
  }

  return {
    memories_count: memories.length,
    entities: allEntities,
    entities_count: allEntities.length,
    entity_types: entityTypes,
    relations,
    relations_count: relations.length,
    built_at: new Date().toISOString(),
  };
}

/**
 * Save the graph to disk.
 * @param {KnowledgeGraph} graph
 */
export function saveGraphToFile(graph) {
  const dir = join(config.memoryDir);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  const graphFile = join(dir, 'graph.json');
  writeFileSync(graphFile, JSON.stringify(graph, null, 2), 'utf8');
}

/**
 * Load the graph from disk (if it exists).
 * @returns {KnowledgeGraph|null}
 */
export function loadGraphFromFile() {
  const graphFile = join(config.memoryDir, 'graph.json');
  if (!existsSync(graphFile)) return null;
  try {
    return JSON.parse(readFileSync(graphFile, 'utf8'));
  } catch {
    return null;
  }
}

/**
 * Build and save the graph.
 * @returns {KnowledgeGraph}
 */
export function buildAndSaveGraph() {
  const graph = buildGraph();
  saveGraphToFile(graph);
  return graph;
}

/**
 * Build the new knowledge graph using hybrid entity + relation extraction.
 * Stores in knowledge_graph.json via graph_store.js
 * @param {object} options
 * @returns {Promise<{ entities: number, relations: number, stats: object }>}
 */
export async function buildKnowledgeGraph(options = {}) {
  const { useLLM = false } = options; // LLM extraction off by default for speed
  const memories = getAllMemories();

  /** @type {Array<{ id: string, name: string, type: string, method: string, memory_ids: string[] }>} */
  const allNewEntities = [];

  for (const m of memories) {
    const text = m.text || '';
    if (!text.trim()) continue;

    try {
      const entities = await extractEntities(text, { useLLM });
      for (const e of entities) {
        const existing = allNewEntities.find(n => n.name === e.name && n.type === e.type);
        if (existing) {
          existing.memory_ids.push(m.id);
        } else {
          allNewEntities.push({ ...e, memory_ids: [m.id] });
        }
      }
    } catch {
      // Skip on error
    }
  }

  // Add entities to store
  for (const e of allNewEntities) {
    gsAddEntity(e);
  }

  // Extract relations using entity IDs
  for (const m of memories) {
    const text = m.text || '';
    if (!text.trim()) continue;

    try {
      // Build entity list with IDs for this memory
      const memoryEntities = await extractEntities(text, { useLLM });
      const relations = await extractRelations(text, memoryEntities, {});
      for (const r of relations) {
        gsAddRelation(r);
      }
    } catch {
      // Skip on error
    }
  }

  const stats = gsGetStats();
  return {
    entities: allNewEntities.length,
    relations: 0,
    stats,
  };
}

/**
 * Export the graph as HTML visualization using vis-network.
 * @param {KnowledgeGraph} graph
 * @returns {string}
 */
export function exportHtml(graph) {
  /** @type {Record<string, VisNode>} */
  const nodes = {};

  for (const e of graph.entities || []) {
    const name = e.name;
    if (name && !nodes[name]) {
      nodes[name] = {
        id: name,
        label: name,
        type: e.type || 'unknown',
        color: ENTITY_COLORS[e.type] || '#94a3b8',
      };
    }
  }

  /** @type {VisEdge[]} */
  const edges = [];
  for (const r of graph.relations || []) {
    edges.push({ from: r.source, to: r.target, label: r.relation });
  }

  const nodesJson = JSON.stringify(Object.values(nodes));
  const edgesJson = JSON.stringify(edges);
  const nodeCount = Object.keys(nodes).length;
  const edgeCount = edges.length;
  const memCount = graph.memories_count || 0;

  return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Memory Graph - 知识图谱</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { margin: 0; font-family: sans-serif; background: #1e1e1e; }
        #mynetwork { width: 100%; height: 100vh; }
        .header {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 100;
        }
        .header h1 { margin: 0; font-size: 18px; }
        .header p { margin: 5px 0 0 0; font-size: 14px; color: #aaa; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Memory Graph</h1>
        <p>实体: ${nodeCount} | 关系: ${edgeCount} | 记忆: ${memCount}</p>
    </div>
    <div id="mynetwork"></div>
    <script>
        const nodes = new vis.DataSet(${nodesJson});
        const edges = new vis.DataSet(${edgesJson});
        const container = document.getElementById('mynetwork');
        const data = { nodes: nodes, edges: edges };
        const options = {
            nodes: {
                shape: 'dot',
                size: 20,
                font: { size: 14, color: '#fff' },
                borderWidth: 2
            },
            edges: {
                width: 2,
                color: { color: '#848484' },
                arrows: { to: { enabled: true, scaleFactor: 0.5 } },
                font: { size: 12, color: '#ccc', align: 'middle' }
            },
            physics: {
                forceAtlas2Based: {
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                },
                maxVelocity: 50,
                solver: 'forceAtlas2Based',
                timestep: 0.35,
                stabilization: { iterations: 150 }
            }
        };
        new vis.Network(container, data, options);
    </script>
</body>
</html>`;
}

/**
 * Export the graph as JSON string.
 * @param {KnowledgeGraph} graph
 * @returns {string}
 */
export function getGraphStatsFromFile() {
  const graph = loadGraphFromFile();
  const nodes = graph?.nodes || [];
  const edges = graph?.edges || [];
  const entities = nodes.filter(n => n.type === 'entity').length;
  const concepts = nodes.filter(n => n.type === 'concept').length;
  return {
    total_nodes: nodes.length,
    total_edges: edges.length,
    entities,
    concepts,
    categories: [...new Set(nodes.map(n => n.category).filter(Boolean))]
  };
}

export function exportJson(graph) {
  return JSON.stringify(graph, null, 2);
}

// Re-export graph_store functions for convenience
export {
  loadGraph,
  storeGraph,
  gsAddEntity as addEntityToGraph,
  gsAddRelation as addRelationToGraph,
  findEntity,
  findEntityById,
  gsGetNeighbors,
  queryGraph,
  getGraphStats,
  mergeIntoGraph,
  gsClearGraph,
  gsGetStats,
};
