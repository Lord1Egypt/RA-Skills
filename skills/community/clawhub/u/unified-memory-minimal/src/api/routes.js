/**
 * routes.js - API Router
 * Route definitions for the memory API server
 */

import { getAllMemories, addMemory, deleteMemory } from '../storage.js';
import { hybridSearch } from '../fusion.js';
import { qmdSearch } from '../tools/qmd_search.js';
import { analyzeInsights } from '../tools/insights.js';
import { getSyncStatus } from '../backup/sync.js';
import { log } from '../utils/logger.js';

/**
 * Route definitions and handlers
 * Each route maps a path pattern to a handler function
 */
export const routes = [
  // ---- Memory CRUD ----
  {
    method: 'GET',
    path: '/memory',
    description: 'List all memories',
    handler: handleListMemories
  },
  {
    method: 'GET',
    path: '/memory/:id',
    description: 'Get a single memory by ID',
    handler: handleGetMemory
  },
  {
    method: 'POST',
    path: '/memory',
    description: 'Store a new memory',
    handler: handleStoreMemory
  },
  {
    method: 'DELETE',
    path: '/memory/:id',
    description: 'Delete a memory',
    handler: handleDeleteMemory
  },

  // ---- Search ----
  {
    method: 'GET',
    path: '/search',
    description: 'Search memories (hybrid)',
    handler: handleSearch
  },
  {
    method: 'GET',
    path: '/search/qmd',
    description: 'QMD-style search',
    handler: handleQMDSearch
  },

  // ---- Stats & Info ----
  {
    method: 'GET',
    path: '/stats',
    description: 'Get memory statistics',
    handler: handleStats
  },
  {
    method: 'GET',
    path: '/health',
    description: 'Health check',
    handler: handleHealth
  },
  {
    method: 'GET',
    path: '/insights',
    description: 'Get memory insights',
    handler: handleInsights
  },

  // ---- Sync ----
  {
    method: 'GET',
    path: '/sync/status',
    description: 'Get sync status',
    handler: handleSyncStatus
  },

  // ---- Graph ----
  {
    method: 'GET',
    path: '/graph',
    description: 'Get knowledge graph',
    handler: handleGraph
  }
];

// ---- Handlers ----

async function handleListMemories(req, params, query) {
  const limit = parseInt(query.limit || 50);
  const offset = parseInt(query.offset || 0);
  const memories = getAllMemories();
  return {
    memories: memories.slice(offset, offset + limit),
    total: memories.length,
    limit,
    offset
  };
}

async function handleGetMemory(req, params, query) {
  const { id } = params;
  const memories = getAllMemories();
  const mem = memories.find(m => m.id === id);
  if (!mem) {
    return { error: 'Memory not found' };
  }
  return { memory: mem };
}

async function handleStoreMemory(req, params, query, body) {
  if (!body || !body.text) {
    return { error: 'text is required' };
  }
  const mem = addMemory({
    text: body.text,
    category: body.category || 'general',
    importance: body.importance || 0.5,
    tags: body.tags || []
  });
  log('INFO', `Memory stored: ${mem.id}`);
  return { success: true, id: mem.id, memory: mem };
}

async function handleDeleteMemory(req, params, query) {
  const { id } = params;
  const success = deleteMemory(id);
  log('INFO', `Memory deleted: ${id}, success=${success}`);
  return { success };
}

async function handleSearch(req, params, query) {
  const q = query.q || query.query || '';
  const topK = parseInt(query.topK || query.k || 10);
  const mode = query.mode || 'hybrid';

  if (!q) {
    return { error: 'Query parameter (q) is required' };
  }

  try {
    const results = await hybridSearch(q, topK, mode);
    return {
      query: q,
      count: results.length,
      results: results.map(r => ({
        id: r.memory.id,
        text: r.memory.text,
        category: r.memory.category,
        importance: r.memory.importance,
        score: Math.round(r.fusionScore * 1000) / 1000,
        highlight: r.highlight || null
      }))
    };
  } catch (err) {
    log('ERROR', `Search error: ${err.message}`);
    return { error: err.message, results: [] };
  }
}

async function handleQMDSearch(req, params, query) {
  const q = query.q || query.query || '';
  const topK = parseInt(query.topK || query.k || 10);

  if (!q) {
    return { error: 'Query parameter (q) is required' };
  }

  try {
    const results = await qmdSearch(q, { topK });
    return {
      query: q,
      count: results.length,
      mode: 'qmd',
      results: results.map(r => ({
        id: r.id,
        text: r.text,
        category: r.category,
        score: Math.round(r.score * 1000) / 1000,
        mode: r.mode
      }))
    };
  } catch (err) {
    log('ERROR', `QMD search error: ${err.message}`);
    return { error: err.message, results: [] };
  }
}

async function handleStats(req, params, query) {
  const memories = getAllMemories();
  const categories = {};
  const tagCounts = {};
  
  for (const m of memories) {
    const cat = m.category || 'other';
    categories[cat] = (categories[cat] || 0) + 1;
    for (const tag of m.tags || []) {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }

  const topTags = Object.entries(tagCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([tag, count]) => ({ tag, count }));

  return {
    total: memories.length,
    categories,
    top_tags: topTags
  };
}

async function handleHealth(req, params, query) {
  let ollamaOk = false;
  try {
    const res = await fetch('http://localhost:11434/api/tags');
    ollamaOk = res.ok;
  } catch { }

  const memories = getAllMemories();

  return {
    status: 'ok',
    timestamp: new Date().toISOString(),
    memories: memories.length,
    ollama: ollamaOk ? 'connected' : 'disconnected',
    embedding_model: 'nomic-embed-text'
  };
}

async function handleInsights(req, params, query) {
  try {
    const result = await analyzeInsights();
    return JSON.parse(result.content[0].text);
  } catch (err) {
    log('ERROR', `Insights error: ${err.message}`);
    return { error: err.message };
  }
}

async function handleSyncStatus(req, params, query) {
  return getSyncStatus();
}

async function handleGraph(req, params, query) {
  // Placeholder - would call graph module
  return {
    entities: [],
    relations: [],
    node_count: 0,
    edge_count: 0
  };
}

/**
 * Parse route parameters from path
 * e.g., /memory/:id -> /memory/abc123 -> { id: 'abc123' }
 */
export function parseRouteParams(routePath, actualPath) {
  const routeParts = routePath.split('/');
  const actualParts = actualPath.split('/');
  const params = {};

  for (let i = 0; i < routeParts.length; i++) {
    if (routeParts[i].startsWith(':')) {
      const key = routeParts[i].slice(1);
      params[key] = actualParts[i] || null;
    }
  }

  return params;
}

/**
 * Match a route
 * Returns { matched: true, params: {} } or { matched: false }
 */
export function matchRoute(method, path, route) {
  if (route.method !== method) {
    return { matched: false };
  }

  const routeParts = route.path.split('/');
  const pathParts = path.split('/');

  if (routeParts.length !== pathParts.length) {
    return { matched: false };
  }

  for (let i = 0; i < routeParts.length; i++) {
    if (routeParts[i].startsWith(':')) {
      continue; // parameter, ok
    }
    if (routeParts[i] !== pathParts[i]) {
      return { matched: false };
    }
  }

  return {
    matched: true,
    params: parseRouteParams(route.path, path)
  };
}
