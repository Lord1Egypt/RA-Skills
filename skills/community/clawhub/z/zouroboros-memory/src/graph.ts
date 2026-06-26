/**
 * Graph-boosted search v2
 *
 * Builds an implicit entity graph from facts and episodes,
 * then uses graph traversal to boost search results for
 * entities that are closely related to the query context.
 */

import { getDatabase } from './database.js';
import type { GraphNode, GraphEdge, MemoryEntry, MemorySearchResult } from './types.js';

/** Cached graph with TTL to avoid rebuilding on every search */
let _graphCache: { nodes: GraphNode[]; edges: GraphEdge[]; builtAt: number } | null = null;
const GRAPH_CACHE_TTL_MS = 60_000; // 1 minute

/**
 * Invalidate the graph cache. Call after mutations (fact store/delete, episode create).
 */
export function invalidateGraphCache(): void {
  _graphCache = null;
}

/**
 * Build a graph of entity co-occurrences from episodes.
 * Two entities are connected if they appear in the same episode.
 * Results are cached with a 60-second TTL.
 */
export function buildEntityGraph(): { nodes: GraphNode[]; edges: GraphEdge[] } {
  if (_graphCache && Date.now() - _graphCache.builtAt < GRAPH_CACHE_TTL_MS) {
    return { nodes: _graphCache.nodes, edges: _graphCache.edges };
  }
  const db = getDatabase();

  // Get all entities that appear in episodes
  const entityRows = db.query(
    'SELECT DISTINCT entity FROM episode_entities'
  ).all() as { entity: string }[];

  const nodes: GraphNode[] = entityRows.map(r => ({
    id: r.entity,
    type: 'entity',
    label: r.entity,
    properties: {},
  }));

  // Build edges from co-occurrence in episodes
  const edgeMap = new Map<string, number>();

  const episodes = db.query(
    'SELECT id FROM episodes'
  ).all() as { id: string }[];

  // For each episode, get all entities and create edges between them
  const stmt = db.query(
    'SELECT entity FROM episode_entities WHERE episode_id = ?'
  );

  for (const ep of episodes) {
    const entities = (stmt.all(ep.id) as { entity: string }[]).map(r => r.entity);
    for (let i = 0; i < entities.length; i++) {
      for (let j = i + 1; j < entities.length; j++) {
        const key = [entities[i], entities[j]].sort().join('||');
        edgeMap.set(key, (edgeMap.get(key) ?? 0) + 1);
      }
    }
  }

  // Also build edges from facts sharing the same entity
  const factEntities = db.query(
    'SELECT DISTINCT entity FROM facts'
  ).all() as { entity: string }[];

  for (const fe of factEntities) {
    const existing = nodes.find(n => n.id === fe.entity);
    if (!existing) {
      nodes.push({
        id: fe.entity,
        type: 'entity',
        label: fe.entity,
        properties: {},
      });
    }
  }

  const edges: GraphEdge[] = Array.from(edgeMap.entries()).map(([key, weight]) => {
    const [source, target] = key.split('||');
    return { source, target, relation: 'co-occurs', weight };
  });

  _graphCache = { nodes, edges, builtAt: Date.now() };
  return { nodes, edges };
}

/**
 * Get entities related to a given entity via graph traversal.
 * Returns entities within `depth` hops, scored by connection strength.
 */
export function getRelatedEntities(
  entity: string,
  options: { depth?: number; limit?: number } = {}
): { entity: string; score: number }[] {
  const { depth = 2, limit = 20 } = options;
  const { edges } = buildEntityGraph();

  // BFS with decay
  const visited = new Map<string, number>(); // entity → score
  const queue: { entity: string; score: number; hop: number }[] = [
    { entity, score: 1.0, hop: 0 },
  ];
  visited.set(entity, 1.0);

  while (queue.length > 0) {
    const current = queue.shift()!;
    if (current.hop >= depth) continue;

    // Find connected entities
    for (const edge of edges) {
      let neighbor: string | null = null;
      if (edge.source === current.entity) neighbor = edge.target;
      else if (edge.target === current.entity) neighbor = edge.source;

      if (neighbor && !visited.has(neighbor)) {
        const decayFactor = 1 / (current.hop + 2); // decay with distance
        const score = current.score * decayFactor * Math.min(edge.weight, 5) / 5;
        visited.set(neighbor, score);
        queue.push({ entity: neighbor, score, hop: current.hop + 1 });
      }
    }
  }

  // Remove self, sort by score
  visited.delete(entity);
  return Array.from(visited.entries())
    .map(([entity, score]) => ({ entity, score }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

/**
 * Graph-boosted search: augments keyword/vector results with
 * graph-adjacent facts from related entities.
 *
 * Uses RRF fusion across three signals:
 * 1. Exact/keyword matches (weight: exactWeight)
 * 2. Vector/semantic matches (weight: vectorWeight)
 * 3. Graph-adjacent facts (weight: graphWeight)
 */
export function searchFactsGraphBoosted(
  baseResults: MemorySearchResult[],
  queryEntities: string[],
  options: {
    limit?: number;
    graphWeight?: number;
    graphDepth?: number;
  } = {}
): MemorySearchResult[] {
  const { limit = 10, graphWeight = 0.2, graphDepth = 2 } = options;
  const db = getDatabase();

  // Collect related entities from graph
  const relatedEntities = new Map<string, number>();
  for (const entity of queryEntities) {
    for (const related of getRelatedEntities(entity, { depth: graphDepth })) {
      const existing = relatedEntities.get(related.entity) ?? 0;
      relatedEntities.set(related.entity, Math.max(existing, related.score));
    }
  }

  if (relatedEntities.size === 0) return baseResults;

  // Fetch facts for related entities
  const entityList = Array.from(relatedEntities.keys());
  const placeholders = entityList.map(() => '?').join(',');
  const graphRows = db.query(`
    SELECT id, entity, key, value, category, decay_class as decayClass,
           importance, created_at as createdAt
    FROM facts
    WHERE entity IN (${placeholders})
      AND (expires_at IS NULL OR expires_at > strftime('%s', 'now'))
    ORDER BY importance DESC
    LIMIT 50
  `).all(...entityList) as Array<{
    id: string;
    entity: string;
    key: string | null;
    value: string;
    category: string;
    decayClass: string;
    importance: number;
    createdAt: number;
  }>;

  // Build graph results scored by entity relationship strength
  const graphResults: MemorySearchResult[] = graphRows.map(row => ({
    entry: {
      id: row.id,
      entity: row.entity,
      key: row.key,
      value: row.value,
      decay: row.decayClass as DecayClass,
      createdAt: new Date(row.createdAt * 1000).toISOString(),
      updatedAt: new Date(row.createdAt * 1000).toISOString(),
      tags: row.category ? [row.category] : undefined,
    },
    score: relatedEntities.get(row.entity) ?? 0,
    matchType: 'graph' as const,
  }));

  // RRF fusion of base results + graph results
  const k = 60;
  const scores = new Map<string, { entry: MemoryEntry; score: number; matchType: MemorySearchResult['matchType'] }>();

  const baseWeight = 1 - graphWeight;

  baseResults.forEach((result, rank) => {
    const rrfScore = (1 / (k + rank + 1)) * baseWeight;
    scores.set(result.entry.id, {
      entry: result.entry,
      score: rrfScore,
      matchType: result.matchType,
    });
  });

  graphResults
    .sort((a, b) => b.score - a.score)
    .forEach((result, rank) => {
      const rrfScore = (1 / (k + rank + 1)) * graphWeight;
      const existing = scores.get(result.entry.id);
      if (existing) {
        existing.score += rrfScore;
      } else {
        scores.set(result.entry.id, {
          entry: result.entry,
          score: rrfScore,
          matchType: 'graph',
        });
      }
    });

  return Array.from(scores.values())
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(r => ({
      entry: r.entry,
      score: r.score,
      matchType: r.matchType,
    }));
}

/**
 * Extract entity names from a query string.
 * Simple heuristic: capitalized words, quoted strings, known entities.
 */
export function extractQueryEntities(query: string): string[] {
  const db = getDatabase();
  const words = query.split(/\s+/);

  // Check which words match known entities in facts
  const knownEntities = new Set<string>();
  const entityRows = db.query(
    'SELECT DISTINCT entity FROM facts'
  ).all() as { entity: string }[];

  const entitySet = new Set(entityRows.map(r => r.entity.toLowerCase()));

  // Match individual words and bigrams
  for (let i = 0; i < words.length; i++) {
    const word = words[i].replace(/[^a-zA-Z0-9_-]/g, '');
    if (entitySet.has(word.toLowerCase())) {
      knownEntities.add(word);
    }
    // Try bigrams
    if (i < words.length - 1) {
      const bigram = `${word} ${words[i + 1].replace(/[^a-zA-Z0-9_-]/g, '')}`;
      if (entitySet.has(bigram.toLowerCase())) {
        knownEntities.add(bigram);
      }
    }
  }

  return Array.from(knownEntities);
}

// Local type alias to avoid import cycle
type DecayClass = 'permanent' | 'long' | 'medium' | 'short';
