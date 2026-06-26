/**
 * HTTP Observability Server for Unified Memory v2
 * Native Node.js http module — no third-party dependencies
 */

import http from 'http';
import { URL } from 'url';
import { getAllMemories, saveMemories, loadMemories } from '../storage.js';
import { loadGraph, getGraphStats } from '../graph/graph_store.js';
import { analyzeInsights } from '../tools/insights.js';

const PORT = 3849;

// Lazily-imported insight store — avoid hard dependency
let PendingInsightStore = null;
function getPendingInsightStore() {
  if (!PendingInsightStore) {
    try {
      PendingInsightStore = require('../system/pending_insight_store.js')?.PendingInsightStore;
    } catch {
      PendingInsightStore = null;
    }
  }
  return PendingInsightStore;
}

let server = null;

/** Send a JSON response */
function json(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(JSON.stringify(data));
}

/** Parse JSON body from IncomingMessage */
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch (e) { reject(new Error('Invalid JSON')); }
    });
    req.on('error', reject);
  });
}

// ── Route handlers ──────────────────────────────────────────────────────────

async function handleHealth() {
  const memories = getAllMemories();
  let entityCount = 0;
  try {
    const graph = loadGraph();
    entityCount = graph.entities?.length ?? 0;
  } catch { /* ignore */ }

  return json;
}

/**
 * GET /health
 * Returns: { status: "ok", memories: N, entities: M }
 */
function routeHealth() {
  const memories = getAllMemories();
  let entityCount = 0;
  try {
    const graph = loadGraph();
    entityCount = graph.entities?.length ?? 0;
  } catch { /* ignore */ }

  return { status: 'ok', memories: memories.length, entities: entityCount };
}

/**
 * GET /memories?page=1&limit=20
 * Returns paginated memory list
 */
function routeMemoriesList(page = 1, limit = 20) {
  const memories = getAllMemories();
  const offset = (page - 1) * limit;
  const items = memories.slice(offset, offset + Number(limit));
  return {
    total: memories.length,
    page: Number(page),
    limit: Number(limit),
    items: items.map(m => ({
      id: m.id,
      text: m.text,
      category: m.category,
      importance: m.importance,
      created_at: m.created_at,
      updated_at: m.updated_at,
    })),
  };
}

/**
 * GET /memories/:id
 * Returns single memory by id
 */
function routeMemoryById(id) {
  const memories = getAllMemories();
  const mem = memories.find(m => m.id === id || m.id?.startsWith(id));
  if (!mem) return null;
  return mem;
}

/**
 * POST /memories  { text, category?, importance? }
 * Creates a new memory
 */
function routeCreateMemory(body) {
  const { text, category = 'general', importance = 0.5 } = body;
  if (!text || typeof text !== 'string' || text.trim().length === 0) {
    throw new Error('text is required');
  }

  const memories = getAllMemories();
  const { randomUUID } = require('crypto');
  const newMem = {
    id: randomUUID ? randomUUID() : `mem_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
    text: text.trim(),
    category,
    importance: Math.max(0, Math.min(1, Number(importance))),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  memories.unshift(newMem);
  saveMemories(memories);
  return newMem;
}

/**
 * DELETE /memories/:id
 * Deletes a memory
 */
function routeDeleteMemory(id) {
  const memories = getAllMemories();
  const idx = memories.findIndex(m => m.id === id || m.id?.startsWith(id));
  if (idx === -1) return false;

  memories.splice(idx, 1);
  saveMemories(memories);
  return true;
}

/**
 * GET /insights/pending
 * Returns pending insights
 */
function routeInsightsPending() {
  const Store = getPendingInsightStore();
  if (!Store) {
    return { pending: [], note: 'pending_insight_store not available' };
  }
  try {
    const store = new Store();
    const pending = store.getAll ? store.getAll() : [];
    return { pending };
  } catch {
    return { pending: [], note: 'error loading insights' };
  }
}

/**
 * GET /stats
 * Returns system statistics
 */
function routeStats() {
  const memories = getAllMemories();
  const count = memories.length;

  // Category distribution
  const categoryDist = {};
  // Importance distribution (buckets)
  const importanceDist = { '0.0-0.2': 0, '0.2-0.4': 0, '0.4-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0 };

  for (const m of memories) {
    const cat = m.category || 'other';
    categoryDist[cat] = (categoryDist[cat] || 0) + 1;

    const imp = m.importance ?? 0.5;
    if (imp <= 0.2) importanceDist['0.0-0.2']++;
    else if (imp <= 0.4) importanceDist['0.2-0.4']++;
    else if (imp <= 0.6) importanceDist['0.4-0.6']++;
    else if (imp <= 0.8) importanceDist['0.6-0.8']++;
    else importanceDist['0.8-1.0']++;
  }

  return { count, category_distribution: categoryDist, importance_distribution: importanceDist };
}

/**
 * GET /graph/entities
 * Returns knowledge graph entities
 */
function routeGraphEntities() {
  try {
    const graph = loadGraph();
    return { entities: graph.entities || [] };
  } catch {
    return { entities: [] };
  }
}

/**
 * GET /graph/stats
 * Returns graph statistics
 */
function routeGraphStats() {
  try {
    const stats = getGraphStats ? getGraphStats() : null;
    if (stats) return stats;
    const graph = loadGraph();
    return {
      entities: graph.entities?.length ?? 0,
      relations: graph.relations?.length ?? 0,
      built_at: graph.built_at,
    };
  } catch {
    return { entities: 0, relations: 0 };
  }
}

// ── Router ─────────────────────────────────────────────────────────────────

async function route(req, res) {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end();
    return;
  }

  try {
    const base = 'http://localhost';
    const url = new URL(req.url, base);
    const pathname = url.pathname;
    const method = req.method;

    // ── GET /health ──────────────────────────────────────────────
    if (method === 'GET' && pathname === '/health') {
      return json(res, 200, routeHealth());
    }

    // ── GET /memories ─────────────────────────────────────────────
    if (method === 'GET' && pathname === '/memories') {
      const page = Number(url.searchParams.get('page') || 1);
      const limit = Number(url.searchParams.get('limit') || 20);
      return json(res, 200, routeMemoriesList(page, limit));
    }

    // ── POST /memories ─────────────────────────────────────────────
    if (method === 'POST' && pathname === '/memories') {
      const body = await parseBody(req);
      const mem = routeCreateMemory(body);
      return json(res, 201, mem);
    }

    // ── GET /memories/:id ──────────────────────────────────────────
    if (method === 'GET' && pathname.startsWith('/memories/')) {
      const id = pathname.replace('/memories/', '');
      const mem = routeMemoryById(id);
      if (!mem) return json(res, 404, { error: 'Memory not found' });
      return json(res, 200, mem);
    }

    // ── DELETE /memories/:id ───────────────────────────────────────
    if (method === 'DELETE' && pathname.startsWith('/memories/')) {
      const id = pathname.replace('/memories/', '');
      const deleted = routeDeleteMemory(id);
      if (!deleted) return json(res, 404, { error: 'Memory not found' });
      return json(res, 200, { deleted: true });
    }

    // ── GET /insights/pending ──────────────────────────────────────
    if (method === 'GET' && pathname === '/insights/pending') {
      return json(res, 200, routeInsightsPending());
    }

    // ── GET /stats ─────────────────────────────────────────────────
    if (method === 'GET' && pathname === '/stats') {
      return json(res, 200, routeStats());
    }

    // ── GET /graph/entities ───────────────────────────────────────
    if (method === 'GET' && pathname === '/graph/entities') {
      return json(res, 200, routeGraphEntities());
    }

    // ── GET /graph/stats ───────────────────────────────────────────
    if (method === 'GET' && pathname === '/graph/stats') {
      return json(res, 200, routeGraphStats());
    }

    // 404
    json(res, 404, { error: 'Not found', path: pathname });

  } catch (err) {
    console.error('[http_server] route error:', err.message);
    json(res, 500, { error: err.message });
  }
}

// ── Server lifecycle ───────────────────────────────────────────────────────

/**
 * Start the HTTP observability server
 * @param {number} [port=3849]
 * @returns {Promise<http.Server>}
 */
export function startHttpServer(port = PORT) {
  return new Promise((resolve, reject) => {
    if (server) {
      resolve(server);
      return;
    }
    server = http.createServer(route);
    server.on('error', err => {
      server = null;
      reject(err);
    });
    server.listen(port, () => {
      console.log(`[http_server] Observability HTTP server listening on port ${port}`);
      resolve(server);
    });
  });
}

/**
 * Stop the HTTP observability server
 * @returns {Promise<void>}
 */
export function stopHttpServer() {
  return new Promise((resolve, reject) => {
    if (!server) {
      resolve();
      return;
    }
    server.close(err => {
      if (err) reject(err);
      else {
        server = null;
        console.log('[http_server] Observability HTTP server stopped');
        resolve();
      }
    });
  });
}

/**
 * Get the current server instance (for testing)
 * @returns {http.Server|null}
 */
export function getServer() {
  return server;
}
