/**
 * server.js - REST API 服务器
 * Ported from Python memory_api_server.py
 * 
 * HTTP API for memory operations
 */

import { createServer } from 'http';
import { URL } from 'url';
import { getAllMemories, addMemory, deleteMemory } from '../storage.js';
import { hybridSearch } from '../fusion.js';
import { log } from '../utils/logger.js';

const PORT = 38421;

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function sendJSON(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

async function handleRequest(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname.replace(/^\/+/, '').split('/');
  const query = Object.fromEntries(url.searchParams);

  try {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    const route = path[0] || '';

    // Routes
    if (route === 'memory') {
      await handleMemory(req, res, path.slice(1), query);
    } else if (route === 'search') {
      await handleSearch(req, res, query);
    } else if (route === 'stats') {
      handleStats(req, res);
    } else if (route === 'health') {
      sendJSON(res, 200, { status: 'ok', timestamp: new Date().toISOString() });
    } else if (route === '') {
      sendJSON(res, 200, { 
        name: 'unified-memory-api',
        version: '1.0.0',
        endpoints: ['/memory', '/search', '/stats', '/health']
      });
    } else {
      sendJSON(res, 404, { error: 'Not found', path: url.pathname });
    }
  } catch (err) {
    log('ERROR', `API error: ${err.message}`);
    sendJSON(res, 500, { error: err.message });
  }
}

async function handleMemory(req, res, parts, query) {
  const method = req.method;

  if (method === 'GET' && parts.length === 0) {
    // List memories
    const limit = parseInt(query.limit || 50);
    const offset = parseInt(query.offset || 0);
    const memories = getAllMemories();
    const paginated = memories.slice(offset, offset + limit);
    sendJSON(res, 200, {
      memories: paginated,
      total: memories.length,
      limit,
      offset
    });
  } else if (method === 'GET' && parts.length > 0) {
    // Get single memory
    const memId = parts[0];
    const memories = getAllMemories();
    const mem = memories.find(m => m.id === memId);
    if (mem) {
      sendJSON(res, 200, mem);
    } else {
      sendJSON(res, 404, { error: 'Memory not found' });
    }
  } else if (method === 'POST') {
    // Create memory
    const body = await parseBody(req);
    const mem = addMemory({
      text: body.text,
      category: body.category || 'general',
      importance: body.importance || 0.5,
      tags: body.tags || []
    });
    sendJSON(res, 201, { success: true, id: mem.id });
  } else if (method === 'DELETE' && parts.length > 0) {
    // Delete memory
    const memId = parts[0];
    const success = deleteMemory(memId);
    sendJSON(res, success ? 200 : 404, { success });
  } else {
    sendJSON(res, 405, { error: 'Method not allowed' });
  }
}

async function handleSearch(req, res, query) {
  const q = query.q || query.query || '';
  const topK = parseInt(query.topK || 10);
  const mode = query.mode || 'hybrid';

  if (!q) {
    sendJSON(res, 400, { error: 'Query required' });
    return;
  }

  const results = await hybridSearch(q, topK, mode);
  sendJSON(res, 200, {
    query: q,
    count: results.length,
    results: results.map(r => ({
      id: r.memory.id,
      text: r.memory.text,
      category: r.memory.category,
      importance: r.memory.importance,
      score: Math.round(r.fusionScore * 1000) / 1000
    }))
  });
}

function handleStats(req, res) {
  const memories = getAllMemories();
  const categories = {};
  for (const m of memories) {
    categories[m.category || 'other'] = (categories[m.category || 'other'] || 0) + 1;
  }
  sendJSON(res, 200, {
    total: memories.length,
    categories
  });
}

export function startServer(port = PORT) {
  const server = createServer(handleRequest);
  server.listen(port, () => {
    log('INFO', `Memory API server running on port ${port}`);
  });
  return server;
}

// CLI
if (process.argv[1] && process.argv[1].endsWith('server.js')) {
  startServer();
}
