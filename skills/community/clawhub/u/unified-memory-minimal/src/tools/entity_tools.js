/**
 * Entity Tools - MCP tools for knowledge graph entity operations
 *
 * P0-2: Exposes entity graph operations as MCP tools
 *
 * Tools:
 * - memory_entity_extract: Extract entities from text (rule-based)
 * - memory_entity_link: Create a relation between two entities
 * - memory_entity_neighbors: Get neighbor entities of a given entity
 * - memory_entity_search: Graph-expanded search
 *
 * @module tools/entity_tools
 */

import { extractEntitiesRuleBased } from '../graph/entity.js';
import { loadGraph, addEntity, addRelation, getNeighbors, findEntityById, findEntity, getGraphStats } from '../graph/graph_store.js';
import { expandQueryWithGraph } from './graph_search.js';

/**
 * Extract entities from text using rule-based extraction.
 *
 * @param {string} text - Text to extract entities from
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export function memoryEntityExtractTool({ text }) {
  try {
    if (!text || !text.trim()) {
      return { content: [{ type: 'text', text: JSON.stringify({ count: 0, entities: [] }, null, 2) }] };
    }

    const entities = extractEntitiesRuleBased(text);

    // Add each entity to the graph store
    for (const e of entities) {
      addEntity({ name: e.name, type: e.type, description: null, memory_ids: [] });
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          count: entities.length,
          entities: entities.map(e => ({
            name: e.name,
            type: e.type,
            method: e.method,
          })),
          graph_stats: getGraphStats(),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Entity extract error: ${err.message}` }], isError: true };
  }
}

/**
 * Create a relation between two entities.
 *
 * @param {object} params
 * @param {string} params.from - Source entity name or ID
 * @param {string} params.to - Target entity name or ID
 * @param {string} params.relation - Relation type (worked_with, related_to, etc.)
 * @param {number} [params.strength] - Relation strength/confidence 0-1 (default 0.8)
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export function memoryEntityLinkTool({ from, to, relation, strength = 0.8 }) {
  try {
    if (!from || !to || !relation) {
      return { content: [{ type: 'text', text: 'Error: from, to, and relation are required' }], isError: true };
    }

    const graph = loadGraph();

    // Resolve from entity
    let fromEntity = graph.entities.find(e => e.id === from || e.name === from);
    if (!fromEntity) {
      // Auto-create the entity if it doesn't exist
      fromEntity = addEntity({ name: from, type: 'other', description: null, memory_ids: [] });
    }

    // Resolve to entity
    let toEntity = graph.entities.find(e => e.id === to || e.name === to);
    if (!toEntity) {
      toEntity = addEntity({ name: to, type: 'other', description: null, memory_ids: [] });
    }

    // Add the relation
    const rel = addRelation({
      from: fromEntity.id,
      to: toEntity.id,
      relation,
      confidence: Math.min(1, Math.max(0, strength)),
      source: 'manual',
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          relation: {
            id: rel.id,
            from: fromEntity.name,
            to: toEntity.name,
            relation: rel.relation,
            confidence: rel.confidence,
          },
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Entity link error: ${err.message}` }], isError: true };
  }
}

/**
 * Get neighbor entities of a given entity.
 *
 * @param {object} params
 * @param {string} params.entity - Entity name or ID
 * @param {string} [params.relationType] - Filter by relation type
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export function memoryEntityNeighborsTool({ entity, relationType }) {
  try {
    if (!entity) {
      return { content: [{ type: 'text', text: 'Error: entity is required' }], isError: true };
    }

    const graph = loadGraph();

    // Resolve entity
    let entityObj = graph.entities.find(e => e.id === entity || e.name === entity);
    if (!entityObj) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            error: `Entity not found: ${entity}`,
            available_entities: graph.entities.slice(0, 20).map(e => ({ id: e.id, name: e.name, type: e.type })),
          }, null, 2),
        }],
      };
    }

    const neighbors = getNeighbors(entityObj.id, relationType || null);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          entity: { id: entityObj.id, name: entityObj.name, type: entityObj.type, count: entityObj.count },
          neighbors: neighbors.map(n => ({
            id: n.entity.id,
            name: n.entity.name,
            type: n.entity.type,
            relation: n.relation,
            weight: n.weight,
          })),
          graph_stats: getGraphStats(),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Entity neighbors error: ${err.message}` }], isError: true };
  }
}

/**
 * Search using graph-expanded query (graph-enhanced search).
 *
 * @param {object} params
 * @param {string} params.query - Search query
 * @param {number} [params.topK] - Number of results (default 5)
 * @param {string} [params.scope] - Scope filter
 * @returns {{ content: Array<{type: 'text', text: string}> }}
 */
export async function memoryEntitySearchTool({ query, topK = 5, scope }) {
  try {
    if (!query) {
      return { content: [{ type: 'text', text: 'Error: query is required' }], isError: true };
    }

    // Expand query with graph
    const { expandedQuery, entities, expanded } = expandQueryWithGraph(query, 5);

    // Import the search pipeline
    const { hybridSearch } = await import('../fusion.js');
    const results = await hybridSearch(query, topK, 'hybrid', scope || null);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          original_query: query,
          expanded_query: expanded ? expandedQuery : null,
          graph_expanded: expanded,
          graph_entities: entities.map(e => ({ name: e.name, type: e.type, graph_id: e.graphId })),
          count: results.length,
          results: results.map(r => ({
            id: r.memory.id,
            text: r.memory.text,
            category: r.memory.category,
            importance: r.memory.importance,
            score: Math.round(r.fusionScore * 1000) / 1000,
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Entity search error: ${err.message}` }], isError: true };
  }
}
