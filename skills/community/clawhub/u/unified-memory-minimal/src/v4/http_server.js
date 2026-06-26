/**
 * http_server.js — v4.0 HTTP REST API (child process mode)
 *
 * This file is STARTED by the MCP tool `memory_v4_http_start` via child_process.spawn.
 * It inherits the node environment from mcporter, giving it access to better-sqlite3.
 *
 * Endpoints:
 *   GET  /api/v4/health
 *   GET  /api/v4/memories        ?scope=&scopeType=&scopeId=&category=&tier=&limit=
 *   POST /api/v4/memories         body: {text, category, importance, scope, scopeId, tags}
 *   GET  /api/v4/memories/:id
 *   DELETE /api/v4/memories/:id
 *   GET  /api/v4/search           ?q=&topK=&scope=&scopeType=&scopeId=
 *   GET  /api/v4/teams
 *   POST /api/v4/teams            body: {teamId, name, config}
 *   GET  /api/v4/stats
 *   GET  /api/v4/wal             ?limit=&since=
 */

import { createServer } from 'http';
import { StorageGateway } from './storage-gateway.js';

const PORT = parseInt(process.argv[2] || process.env.MEMORY_HTTP_PORT || '3099');
const HOST = process.env.MEMORY_HTTP_HOST || '0.0.0.0';

let _server = null;
let _gw = null;

async function getGw() {
  if (!_gw) {
    _gw = new StorageGateway();
    await _gw.init();
  }
  return _gw;
}

function json(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(JSON.stringify(data, null, 2));
}

function err(res, status, msg) { json(res, status, { error: msg, status }); }

function body(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      const buf = Buffer.concat(chunks);
      try { resolve(buf.length ? JSON.parse(buf.toString()) : {}); }
      catch { resolve({}); }
    });
  });
}

async function handler(req, res) {
  const base = 'http://' + (req.headers.host || 'localhost:' + PORT);
  let pathname;
  try { pathname = new URL(req.url, base).pathname.replace(/^\/api\/v4\//, ''); }
  catch { pathname = req.url || '/'; }

  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Access-Control-Allow-Origin': '*' });
    res.end();
    return;
  }

  try {
    let gw;
    try { gw = await getGw(); }
    catch (e) { return err(res, 500, 'Storage init failed: ' + e.message); }

    // GET /health
    if (pathname === 'health' && req.method === 'GET') {
      const stats = await gw.stats();
      return json(res, 200, { status: 'ok', v4: true, ...stats });
    }

    // GET /memories
    if (pathname === 'memories' && req.method === 'GET') {
      const url = new URL(req.url, base);
      const limit = parseInt(url.searchParams.get('limit') || '50');
      const mems = await gw.getMemories({
        scope: url.searchParams.get('scope') || undefined,
        scopeType: url.searchParams.get('scopeType') || undefined,
        scopeId: url.searchParams.get('scopeId') || undefined,
        category: url.searchParams.get('category') || undefined,
        tier: url.searchParams.get('tier') || undefined,
        limit,
      });
      return json(res, 200, { v4: true, count: mems.length, memories: mems });
    }

    // POST /memories
    if (pathname === 'memories' && req.method === 'POST') {
      const b = await body(req);
      if (!b.text) return err(res, 400, 'Missing required field: text');
      const mem = await gw.writeMemory(b);
      return json(res, 201, { v4: true, id: mem.id, success: true });
    }

    // GET|DELETE /memories/:id
    const memId = pathname.match(/^memories\/(.+)$/);
    if (memId) {
      if (req.method === 'GET') {
        const mem = await gw.getMemory(memId[1]);
        return mem ? json(res, 200, { v4: true, memory: mem }) : err(res, 404, 'Memory not found');
      }
      if (req.method === 'DELETE') {
        await gw.deleteMemory(memId[1]);
        return json(res, 200, { v4: true, id: memId[1], deleted: true });
      }
    }

    // GET /search
    if (pathname === 'search' && req.method === 'GET') {
      const url = new URL(req.url, base);
      const q = url.searchParams.get('q') || '';
      const topK = parseInt(url.searchParams.get('topK') || '10');
      const results = await gw.searchMemories(q, {
        topK,
        scope: url.searchParams.get('scope') || undefined,
        scopeType: url.searchParams.get('scopeType') || undefined,
        scopeId: url.searchParams.get('scopeId') || undefined,
      });
      return json(res, 200, { v4: true, engine: 'bm25', query: q, count: results.length, results });
    }

    // GET /teams
    if (pathname === 'teams' && req.method === 'GET') {
      const teams = await gw.listTeams();
      return json(res, 200, { v4: true, count: teams.length, teams });
    }

    // POST /teams
    if (pathname === 'teams' && req.method === 'POST') {
      const b = await body(req);
      if (!b.teamId) return err(res, 400, 'Missing required field: teamId');
      const team = await gw.createTeam(b.teamId, b.name, b.config || {});
      return json(res, 201, { v4: true, team, success: true });
    }

    // GET /stats
    if (pathname === 'stats' && req.method === 'GET') {
      const [stats, ev, rev, wal] = await Promise.all([
        gw.stats(), gw.getEvidenceStats(), gw.getRevisionStats(), gw.getWalStatus(),
      ]);
      return json(res, 200, { v4: true, memories: stats, evidence: ev, revisions: rev, wal });
    }

    // GET /wal
    if (pathname === 'wal' && req.method === 'GET') {
      const url = new URL(req.url, base);
      const limit = parseInt(url.searchParams.get('limit') || '100');
      const since = url.searchParams.get('since') ? parseInt(url.searchParams.get('since')) : undefined;
      const entries = await gw.exportWal({ since, limit });
      return json(res, 200, { v4: true, count: entries.length, entries });
    }

    err(res, 404, 'Not found: ' + req.method + ' /' + pathname);

  } catch (e) {
    console.error('[/api/v4/' + pathname + ']', e.message);
    err(res, 500, e.message);
  }
}

_server = createServer(handler);
_server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error('[http_server] Port ' + PORT + ' in use. Kill existing server and retry.');
  }
  process.exit(1);
});

_server.listen(PORT, HOST, () => {
  console.log('[http_server] v4.0 REST API listening on http://' + HOST + ':' + PORT + '/api/v4/');
});

process.on('SIGTERM', () => { _server.close(); process.exit(0); });
process.on('SIGINT', () => { _server.close(); process.exit(0); });
