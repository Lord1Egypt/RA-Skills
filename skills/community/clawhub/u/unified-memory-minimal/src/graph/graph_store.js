/**
 * Graph Store - 知识图谱的持久化存储
 * 文件：~/.openclaw/workspace/memory/knowledge_graph.json
 *
 * @module graph/graph_store
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';
import { buildAdjacencyList, getNeighbors as relationGetNeighbors, queryGraphPaths } from './relation.js';

const GRAPH_FILE = join(config.memoryDir, 'knowledge_graph.json');

// Ensure memory dir exists
if (!existsSync(config.memoryDir)) {
  mkdirSync(config.memoryDir, { recursive: true });
}

/**
 * @typedef {Object} GraphEntity
 * @property {string} id
 * @property {string} name
 * @property {string} type
 * @property {string} [description]
 * @property {string[]} [memory_ids]
 * @property {number} [count]
 * @property {string} created_at
 * @property {string} updated_at
 */

/**
 * @typedef {Object} GraphRelation
 * @property {string} id
 * @property {string} from
 * @property {string} to
 * @property {string} relation
 * @property {number} confidence
 * @property {string} [source]
 * @property {string} created_at
 */

/**
 * @typedef {Object} KnowledgeGraph
 * @property {GraphEntity[]} entities
 * @property {GraphRelation[]} relations
 * @property {string} built_at
 * @property {number} version
 */

/**
 * Load the graph from disk.
 * @returns {KnowledgeGraph}
 */
export function loadGraph() {
  if (!existsSync(GRAPH_FILE)) {
    return {
      entities: [],
      relations: [],
      built_at: new Date().toISOString(),
      version: 1,
    };
  }
  try {
    return JSON.parse(readFileSync(GRAPH_FILE, 'utf8'));
  } catch {
    return {
      entities: [],
      relations: [],
      built_at: new Date().toISOString(),
      version: 1,
    };
  }
}

/**
 * Save the graph to disk.
 * @param {KnowledgeGraph} graph
 */
export function saveGraph(graph) {
  graph.built_at = new Date().toISOString();
  graph.version = (graph.version || 0) + 1;
  writeFileSync(GRAPH_FILE, JSON.stringify(graph, null, 2), 'utf8');
}

/**
 * Add or update an entity in the graph.
 * @param {Partial<GraphEntity> & { name: string, type: string }} entity
 * @returns {GraphEntity}
 */
export function addEntity(entity) {
  const graph = loadGraph();
  const now = new Date().toISOString();

  // Check if entity with same name+type already exists
  const existingIdx = graph.entities.findIndex(
    e => e.name === entity.name && e.type === entity.type
  );

  if (existingIdx !== -1) {
    // Update existing: increment count, add memory_id
    const existing = graph.entities[existingIdx];
    const memory_ids = [...new Set([...(existing.memory_ids || []), ...(entity.memory_ids || [])])];
    graph.entities[existingIdx] = {
      ...existing,
      count: (existing.count || 1) + 1,
      memory_ids,
      description: entity.description || existing.description,
      updated_at: now,
    };
    saveGraph(graph);
    return graph.entities[existingIdx];
  }

  // Create new entity
  const newEntity = {
    id: entity.id || `ent_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
    name: entity.name,
    type: entity.type,
    description: entity.description || null,
    memory_ids: entity.memory_ids || [],
    count: 1,
    created_at: now,
    updated_at: now,
  };

  graph.entities.push(newEntity);
  saveGraph(graph);
  return newEntity;
}

/**
 * Add a relation to the graph (skip duplicates).
 * @param {Partial<GraphRelation> & { from: string, to: string, relation: string }} relation
 * @returns {GraphRelation}
 */
export function addRelation(relation) {
  const graph = loadGraph();
  const now = new Date().toISOString();

  // Check for duplicate
  const exists = graph.relations.some(
    r => r.from === relation.from && r.to === relation.to && r.relation === relation.relation
  );

  if (exists) {
    return graph.relations.find(
      r => r.from === relation.from && r.to === relation.to && r.relation === relation.relation
    );
  }

  const newRelation = {
    id: relation.id || `rel_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
    from: relation.from,
    to: relation.to,
    relation: relation.relation,
    confidence: relation.confidence || 0.5,
    source: relation.source || null,
    created_at: now,
  };

  graph.relations.push(newRelation);
  saveGraph(graph);
  return newRelation;
}

/**
 * Find an entity by name and/or type.
 * @param {string} name
 * @param {string} [type]
 * @returns {GraphEntity|null}
 */
export function findEntity(name, type) {
  const graph = loadGraph();
  return graph.entities.find(
    e => e.name === name && (!type || e.type === type)
  ) || null;
}

/**
 * Find entity by ID.
 * @param {string} id
 * @returns {GraphEntity|null}
 */
export function findEntityById(id) {
  const graph = loadGraph();
  return graph.entities.find(e => e.id === id) || null;
}

/**
 * Get all relations for an entity.
 * @param {string} entityId
 * @returns {Array<{ relation: GraphRelation, direction: 'outgoing' | 'incoming' }>}
 */
export function getEntityRelations(entityId) {
  const graph = loadGraph();
  const results = [];

  for (const r of graph.relations) {
    if (r.from === entityId) {
      results.push({ relation: r, direction: 'outgoing' });
    }
    if (r.to === entityId) {
      results.push({ relation: r, direction: 'incoming' });
    }
  }

  return results;
}

/**
 * Get neighbors of an entity (direct graph traversal).
 * @param {string} entityId
 * @param {string} [relationType]
 * @returns {Array<{ entity: GraphEntity, relation: string, weight: number }>}
 */
export function getNeighbors(entityId, relationType = null) {
  const graph = loadGraph();
  const results = [];

  for (const r of graph.relations) {
    if (r.from === entityId) {
      if (relationType && r.relation !== relationType) continue;
      const entity = graph.entities.find(e => e.id === r.to);
      if (entity) {
        results.push({ entity, relation: r.relation, weight: r.confidence || 1.0 });
      }
    }
    // For symmetric relations, include reverse
    if (r.to === entityId && (r.relation === 'worked_with' || r.relation === 'related_to')) {
      if (relationType && r.relation !== relationType) continue;
      const entity = graph.entities.find(e => e.id === r.from);
      if (entity) {
        results.push({ entity, relation: r.relation, weight: r.confidence || 1.0 });
      }
    }
  }

  return results;
}

/**
 * Query the graph with depth-first traversal.
 * @param {string} startEntity - Entity name or ID
 * @param {string|null} relationType - Filter by relation type
 * @param {number} depth - Traversal depth (default 1)
 * @returns {{ entity: GraphEntity, paths: Array<{ path: string[], relations: string[], weight: number }> }}
 */
export function queryGraph(startEntity, relationType = null, depth = 1) {
  const graph = loadGraph();

  // Resolve startEntity to ID
  let startId = startEntity;
  const startEntityObj = graph.entities.find(
    e => e.id === startEntity || e.name === startEntity
  );
  if (!startEntityObj) {
    return null;
  }
  startId = startEntityObj.id;

  const paths = queryGraphPaths(startId, graph.relations, depth, relationType);

  return {
    entity: startEntityObj,
    paths,
  };
}

/**
 * Build the full adjacency list for the graph.
 * @returns {Map<string, Array<{ neighbor: string, relation: string, weight: number }>>}
 */
export function buildGraphAdjacency() {
  const graph = loadGraph();
  return buildAdjacencyList(graph.relations);
}

/**
 * Get graph statistics.
 * @returns {{
 *   entities: number,
 *   relations: number,
 *   entityTypes: Record<string, number>,
 *   relationTypes: Record<string, number>,
 *   density: number
 * }}
 */
export function getGraphStats() {
  const graph = loadGraph();

  /** @type {Record<string, number>} */
  const entityTypes = {};
  /** @type {Record<string, number>} */
  const relationTypes = {};

  for (const e of graph.entities) {
    entityTypes[e.type] = (entityTypes[e.type] || 0) + 1;
  }

  for (const r of graph.relations) {
    relationTypes[r.relation] = (relationTypes[r.relation] || 0) + 1;
  }

  const n = graph.entities.length;
  const maxEdges = n * (n - 1);
  const density = maxEdges > 0 ? graph.relations.length / maxEdges : 0;

  return {
    entities: n,
    relations: graph.relations.length,
    entityTypes,
    relationTypes,
    density: Math.round(density * 1000) / 1000,
    built_at: graph.built_at,
    version: graph.version,
  };
}

/**
 * Clear all entities and relations (reset graph).
 */
export function clearGraph() {
  writeFileSync(GRAPH_FILE, JSON.stringify({
    entities: [],
    relations: [],
    built_at: new Date().toISOString(),
    version: 1,
  }, null, 2), 'utf8');
}

/**
 * Merge new entities and relations into the graph.
 * @param {GraphEntity[]} newEntities
 * @param {GraphRelation[]} newRelations
 */
export function mergeIntoGraph(newEntities, newRelations) {
  for (const e of newEntities) {
    addEntity(e);
  }
  for (const r of newRelations) {
    addRelation(r);
  }
}
