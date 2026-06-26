/**
 * Graph Search - Knowledge Graph expanded search
 * Given a query, expands it with related entities from the knowledge graph,
 * then runs the expanded query through the normal search pipeline.
 *
 * @module tools/graph_search
 */

import { loadGraph } from '../graph/graph_store.js';
import { extractEntitiesRuleBased } from '../graph/entity.js';

/**
 * Expand a query by adding related entity names.
 * Finds entities in the query, then adds their neighbors' names.
 *
 * @param {string} query
 * @param {number} [maxExpand=5] - max entities to expand
 * @returns {{ expandedQuery: string, entities: Array, expanded: boolean }}
 */
export function expandQueryWithGraph(query, maxExpand = 5) {
  // 1. Extract entities from the query using rule-based extraction
  const queryEntities = extractEntitiesRuleBased(query);

  if (queryEntities.length === 0) {
    return { expandedQuery: query, entities: [], expanded: false };
  }

  // 2. Load the knowledge graph
  let graph;
  try {
    graph = loadGraph();
  } catch {
    return { expandedQuery: query, entities: queryEntities, expanded: false };
  }

  if (!graph || !graph.entities || graph.entities.length === 0) {
    return { expandedQuery: query, entities: queryEntities, expanded: false };
  }

  // 3. For each query entity, find neighbors and expand
  /** @type {string[]} */
  const expansionTerms = [];
  const processedEntities = [];

  for (const qe of queryEntities.slice(0, maxExpand)) {
    // Find entity in graph by name
    const graphEntity = graph.entities.find(
      e => e.name === qe.name && e.type === qe.type
    );

    if (!graphEntity) continue;

    processedEntities.push({
      ...qe,
      graphId: graphEntity.id,
      memory_ids: graphEntity.memory_ids || [],
    });

    // Get neighbors (related entities)
    const neighbors = [];
    for (const r of graph.relations || []) {
      if (r.from === graphEntity.id) {
        const neighbor = graph.entities.find(e => e.id === r.to);
        if (neighbor) neighbors.push({ entity: neighbor, relation: r.relation });
      }
      if (r.to === graphEntity.id && (r.relation === 'worked_with' || r.relation === 'related_to')) {
        const neighbor = graph.entities.find(e => e.id === r.from);
        if (neighbor) neighbors.push({ entity: neighbor, relation: r.relation });
      }
    }

    // Add neighbor names to expansion terms
    for (const { entity, relation } of neighbors.slice(0, 3)) {
      // Include the relation type as a hint
      if (relation === 'worked_with' || relation === 'related_to') {
        expansionTerms.push(entity.name);
      }
    }
  }

  // 4. Build expanded query
  const uniqueTerms = [...new Set(expansionTerms)];
  const expandedQuery = uniqueTerms.length > 0
    ? `${query} ${uniqueTerms.join(' ')}`
    : query;

  return {
    expandedQuery,
    entities: processedEntities,
    expanded: uniqueTerms.length > 0,
  };
}

/**
 * Get graph-enhanced search results.
 * First expands query via graph, then searches.
 *
 * @param {string} query
 * @param {object} options
 * @param {number} options.topK
 * @param {string} options.scope
 * @param {boolean} options.enableRerank
 * @param {boolean} options.enableMMR
 * @param {boolean} options.enableDecay
 * @param {number} options.fetchK
 * @param {boolean} options.enableGraphBoost
 * @returns {Promise<{ results: Array, expandedQuery: string, graphEntities: Array, expanded: boolean }>}
 */
export async function graphEnhancedSearch(query, options = {}) {
  const {
    topK = 10,
    scope = 'global',
    enableRerank = true,
    enableMMR = true,
    enableDecay = true,
    fetchK = 20,
    enableGraphBoost = true,
  } = options;

  // Step 1: Expand query with graph
  const { expandedQuery, entities: graphEntities, expanded } = expandQueryWithGraph(query, 5);

  // Step 2: Import and run the normal search pipeline
  const { search } = await import('../search.js');

  const results = await search(expandedQuery, {
    topK,
    scope,
    enableRerank,
    enableMMR,
    enableDecay,
    fetchK,
    reflectedBoost: true,
    // Pass graph-specific options
    enableGraphBoost,
    graphEntities: graphEntities.map(e => e.name),
  });

  return {
    results,
    expandedQuery,
    graphEntities,
    expanded,
  };
}

/**
 * MCP tool handler for memory_graph_search
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function memoryGraphSearchTool(args) {
  const {
    query,
    topK = 5,
    scope = 'global',
    enableRerank = true,
    enableMMR = true,
    enableDecay = true,
    fetchK = 20,
  } = args;

  try {
    const { results, expandedQuery, graphEntities, expanded } = await graphEnhancedSearch(query, {
      topK,
      scope,
      enableRerank,
      enableMMR,
      enableDecay,
      fetchK,
      enableGraphBoost: true,
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          query,
          expandedQuery: expanded ? expandedQuery : null,
          graphExpanded: expanded,
          graphEntitiesFound: graphEntities.map(e => ({
            name: e.name,
            type: e.type,
            relatedMemories: e.memory_ids?.length || 0,
          })),
          count: results.length,
          results: results.map(r => ({
            id: r.memory.id,
            text: r.memory.text,
            category: r.memory.category,
            importance: r.memory.importance,
            score: Math.round(r.score * 1000) / 1000,
            graphBoost: r.graphBoost || 0,
            highlight: r.highlight,
            created_at: new Date(r.memory.created_at).toISOString(),
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return {
      content: [{ type: 'text', text: `Graph search error: ${err.message}` }],
      isError: true,
    };
  }
}
