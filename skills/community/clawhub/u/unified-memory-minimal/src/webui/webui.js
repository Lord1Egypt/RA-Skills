/**
 * Memory WebUI - 完整 Web UI 服务器 v1.0
 * 
 * 功能:
 * - HTTP 服务器（内存浏览、搜索、统计）
 * - 知识图谱可视化
 * - 记忆管理和分析
 * 
 * Ported from Python memory_webui.py
 */

import http from 'http';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname, extname } from 'path';
import { URL } from 'url';
import { homedir } from 'os';

const HOME = homedir();
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const WEBUI_DIR = join(MEMORY_DIR, 'webui');

// Ensure webui dir exists
try { mkdirSync(WEBUI_DIR, { recursive: true }); } catch {}

// ============================================================
// Configuration
// ============================================================

const DEFAULT_PORT = 3838;
const DEFAULT_HOST = '0.0.0.0';

// ============================================================
// Memory Data
// ============================================================

export function getAllMemories() {
  const file = join(MEMORY_DIR, 'memories.json');
  if (!existsSync(file)) return [];

  try {
    const content = readFileSync(file, 'utf-8');
    const data = JSON.parse(content);
    if (Array.isArray(data)) return data;
    return data.memories || [];
  } catch {
    return [];
  }
}

export function getMemoryStats() {
  const memories = getAllMemories();

  const byCategory = {};
  const byImportance = { high: 0, medium: 0, low: 0 };
  const byScope = {};
  let totalImportance = 0;

  for (const mem of memories) {
    const cat = mem.category || 'general';
    byCategory[cat] = (byCategory[cat] || 0) + 1;

    const scope = mem.scope || 'unknown';
    byScope[scope] = (byScope[scope] || 0) + 1;

    const imp = mem.importance || 0.5;
    totalImportance += imp;
    if (imp >= 0.7) byImportance.high++;
    else if (imp >= 0.4) byImportance.medium++;
    else byImportance.low++;
  }

  return {
    total: memories.length,
    byCategory,
    byImportance,
    byScope,
    avgImportance: memories.length > 0 ? totalImportance / memories.length : 0,
  };
}

export function getRecentMemories(limit = 20) {
  const memories = getAllMemories();
  return memories
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, limit);
}

export function getTopMemories(limit = 10) {
  const memories = getAllMemories();
  return [...memories]
    .sort((a, b) => (b.importance || 0) - (a.importance || 0))
    .slice(0, limit);
}

export function searchMemories(query, limit = 20) {
  if (!query) return [];

  const memories = getAllMemories();
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/);

  const scored = memories.map(mem => {
    const text = (mem.text || '').toLowerCase();
    let score = 0;

    if (text.includes(queryLower)) {
      score = 1.0;
    } else {
      const textWords = text.split(/\s+/);
      const overlap = queryWords.filter(w => textWords.some(tw => tw.includes(w))).length;
      score = overlap / queryWords.length;
    }

    return { ...mem, _score: score };
  });

  return scored
    .filter(m => m._score > 0)
    .sort((a, b) => b._score - a._score)
    .slice(0, limit);
}

// ============================================================
// Ontology Graph
// ============================================================

export function getOntologyGraph() {
  const graphFile = join(MEMORY_DIR, 'ontology', 'graph.jsonl');
  const entities = [];
  const relations = [];

  if (!existsSync(graphFile)) {
    return { entities, relations };
  }

  try {
    const content = readFileSync(graphFile, 'utf-8');
    const lines = content.split('\n').filter(Boolean);

    for (const line of lines) {
      try {
        const data = JSON.parse(line);
        if (data.op === 'create') {
          const entity = data.entity || {};
          entities.push(entity);
        } else if (data.op === 'relate') {
          relations.push({
            from: data.from,
            rel: data.rel,
            to: data.to,
          });
        }
      } catch {}
    }
  } catch {}

  return { entities, relations };
}

// ============================================================
// Utilities
// ============================================================

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN');
  } catch {
    return '';
  }
}

function getUniqueCategories() {
  const memories = getAllMemories();
  const categories = new Set();
  for (const m of memories) {
    categories.add(m.category || 'general');
  }
  return [...categories].sort();
}

// ============================================================
// API Handler
// ============================================================

async function handleApi(req, res, pathname) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const path = pathname.replace('/api/', '');

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (path === 'stats') {
    res.writeHead(200);
    res.end(JSON.stringify(getMemoryStats()));
    return;
  }

  if (path === 'memories') {
    const memories = getAllMemories();
    res.writeHead(200);
    res.end(JSON.stringify(memories));
    return;
  }

  if (path === 'recent') {
    res.writeHead(200);
    res.end(JSON.stringify(getRecentMemories()));
    return;
  }

  if (path === 'search') {
    const query = url.searchParams.get('q') || '';
    const results = searchMemories(query);
    res.writeHead(200);
    res.end(JSON.stringify({ query, results }));
    return;
  }

  if (path === 'graph') {
    res.writeHead(200);
    res.end(JSON.stringify(getOntologyGraph()));
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({ error: 'Not found' }));
}

// ============================================================
// HTTP Server
// ============================================================

export class MemoryWebUI {
  constructor(port = DEFAULT_PORT, host = DEFAULT_HOST) {
    this.port = port;
    this.host = host;
    this.server = null;
  }

  start() {
    this.server = http.createServer(async (req, res) => {
      try {
        const url = new URL(req.url, `http://${req.headers.host}`);
        const pathname = url.pathname;

        // Handle API routes
        if (pathname.startsWith('/api/')) {
          await handleApi(req, res, pathname);
          return;
        }

        // Handle page routes
        if (pathname === '/' || pathname === '/dashboard') {
          const stats = getMemoryStats();
          const recent = getRecentMemories();
          const html = renderDashboard(stats, recent);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
          return;
        }

        if (pathname === '/memories') {
          const memories = getAllMemories();
          const page = parseInt(url.searchParams.get('page') || '1');
          const html = renderMemories(memories, page);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
          return;
        }

        if (pathname === '/search') {
          const query = url.searchParams.get('q') || '';
          const results = query ? searchMemories(query) : [];
          const html = renderSearch(query, results);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
          return;
        }

        if (pathname === '/graph') {
          const html = renderGraph();
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
          return;
        }

        // 404
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
      } catch (e) {
        console.error('Request error:', e);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
      }
    });

    return new Promise((resolve) => {
      this.server.listen(this.port, this.host, () => {
        console.log(`\n🌐 Memory WebUI: http://${this.host}:${this.port}`);
        resolve();
      });
    });
  }

  stop() {
    if (this.server) {
      this.server.close();
    }
  }
}

// ============================================================
// HTML Templates
// ============================================================

function renderDashboard(stats, recent) {
  const cats = Object.entries(stats.byCategory);
  const maxCat = Math.max(...cats.map(([, v]) => v), 1);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🧠 Unified Memory</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh}
.container{max-width:1200px;margin:0 auto;padding:20px}
h1{color:white;text-align:center;padding:30px 0;font-size:2.5em}
.card{background:white;border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 10px 40px rgba(0,0,0,0.1)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}
.stat{background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);padding:24px;border-radius:12px;color:white;text-align:center}
.stat.blue{background:linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)}
.stat.green{background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%)}
.stat.v{font-size:2.5em;font-weight:bold}
.stat.l{font-size:0.85em;opacity:0.9;margin-top:4px}
h2{color:#333;margin-bottom:16px;font-size:1.2em;border-left:4px solid #667eea;padding-left:12px}
.nav{display:flex;gap:12px;margin-bottom:20px}
.nav a{padding:10px 20px;background:rgba(255,255,255,0.2);color:white;text-decoration:none;border-radius:8px}
.nav a:hover,.nav a.active{background:white;color:#667eea}
.bar{display:flex;align-items:flex-end;gap:6px;height:150px;padding:10px 0}
.bar>div{flex:1;background:linear-gradient(180deg,#667eea 0%,#764ba2 100%);border-radius:4px 4px 0 0;position:relative;min-height:10px}
.bar>div span{position:absolute;bottom:-22px;left:50%;transform:translateX(-50%);font-size:0.7em;color:#666;white-space:nowrap}
.bar>div::after{content:attr(data-v);position:absolute;top:-20px;left:50%;transform:translateX(-50%);font-size:0.7em;font-weight:bold;color:#333}
.list{list-style:none}
.list li{padding:14px 0;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center}
.list li:last-child{border-bottom:none}
.list .text{flex:1;color:#333;font-size:0.95em}
.list .meta{display:flex;gap:10px}
.tag{padding:3px 10px;border-radius:15px;font-size:0.75em;font-weight:500}
.tag.cat{background:#e3f2fd;color:#1565c0}
.tag.imp{background:#fff3e0;color:#ef6c00}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:768px){.grid2{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">
<h1>🧠 Unified Memory</h1>
<nav class="nav">
<a href="/" class="active">📊 Dashboard</a>
<a href="/memories">📝 Memories</a>
<a href="/search">🔍 Search</a>
<a href="/graph">🕸️ Graph</a>
</nav>

<div class="stats">
<div class="stat"><div class="v">${stats.total}</div><div class="l">Total</div></div>
<div class="stat blue"><div class="v">${Object.keys(stats.byCategory).length}</div><div class="l">Categories</div></div>
<div class="stat green"><div class="v">${(stats.avgImportance*100).toFixed(0)}%</div><div class="l">Avg Imp.</div></div>
<div class="stat"><div class="v">${stats.byImportance.high}</div><div class="l">High ⭐</div></div>
</div>

<div class="card">
<h2>📊 Categories</h2>
<div class="bar">
${cats.map(([k,v])=>`<div style="height:${(v/maxCat)*100}%" data-v="${v}"><span>${escapeHtml(k)}</span></div>`).join('')}
</div>
</div>

<div class="card">
<h2>⭐ Importance</h2>
<div style="display:flex;justify-content:center;gap:40px;padding:20px 0">
<div style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#f093fb,#f5576c);display:flex;align-items:center;justify-content:center;font-size:1.5em;font-weight:bold;color:white">${stats.byImportance.high}</div><div style="margin-top:8px;font-size:0.85em;color:#666">High</div></div>
<div style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#4facfe,#00f2fe);display:flex;align-items:center;justify-content:center;font-size:1.5em;font-weight:bold;color:white">${stats.byImportance.medium}</div><div style="margin-top:8px;font-size:0.85em;color:#666">Medium</div></div>
<div style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#43e97b,#38f9d7);display:flex;align-items:center;justify-content:center;font-size:1.5em;font-weight:bold;color:white">${stats.byImportance.low}</div><div style="margin-top:8px;font-size:0.85em;color:#666">Low</div></div>
</div>
</div>

<div class="card">
<h2>🕐 Recent</h2>
<ul class="list">
${recent.slice(0,5).map(m=>`<li><span class="text">${escapeHtml((m.text||'').substring(0,80))}...</span><div class="meta"><span class="tag cat">${escapeHtml(m.category||'general')}</span><span class="tag imp">${((m.importance||0.5)*100).toFixed(0)}%</span></div></li>`).join('')}
</ul>
</div>
</div>
</body>
</html>`;
}

function renderMemories(memories, page = 1, perPage = 30) {
  const totalPages = Math.ceil(memories.length / perPage);
  const start = (page - 1) * perPage;
  const pageMem = memories.slice(start, start + perPage);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>📝 Memories</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f5}
.header{background:linear-gradient(135deg,#667eea,#764ba2);padding:20px 0}
.container{max-width:1000px;margin:0 auto;padding:20px}
h1{color:white;margin-bottom:20px}
.nav{display:flex;gap:12px;margin-bottom:20px}
.nav a{padding:10px 20px;background:rgba(255,255,255,0.2);color:white;text-decoration:none;border-radius:8px}
.nav a:hover,.nav a.active{background:white;color:#667eea}
.card{background:white;border-radius:12px;padding:24px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
.item{padding:20px 0;border-bottom:1px solid #eee}
.item:last-child{border-bottom:none}
.item-head{display:flex;justify-content:space-between;margin-bottom:10px}
.meta{display:flex;gap:10px}
.tag{padding:3px 10px;border-radius:15px;font-size:0.8em;font-weight:500}
.tag.cat{background:#e3f2fd;color:#1565c0}
.tag.imp{background:#fff3e0;color:#ef6c00}
.text{color:#333;line-height:1.6;white-space:pre-wrap}
.id{font-size:0.75em;color:#999;font-family:monospace;margin-top:8px}
.pages{display:flex;justify-content:center;gap:8px;margin-top:20px}
.pages a{padding:8px 16px;background:#667eea;color:white;text-decoration:none;border-radius:8px}
.pages span{padding:8px 16px;color:#666}
.filter{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.filter input,.filter select{padding:10px 16px;border:2px solid #eee;border-radius:8px;font-size:0.95em}
.filter input{flex:1;min-width:200px}
.filter input:focus,.filter select:focus{outline:none;border-color:#667eea}
</style>
</head>
<body>
<div class="header">
<div class="container">
<h1>📝 Memory Browser</h1>
<nav class="nav">
<a href="/">📊 Dashboard</a>
<a href="/memories" class="active">📝 Memories</a>
<a href="/search">🔍 Search</a>
<a href="/graph">🕸️ Graph</a>
</nav>
</div>
</div>
<div class="container">
<div class="card">
<div class="filter">
<input type="text" placeholder="Filter memories..." onkeyup="f(this.value)">
<select onchange="fcat(this.value)"><option value="">All Categories</option>
${getUniqueCategories().map(c=>`<option value="${c}">${escapeHtml(c)}</option>`).join('')}
</select>
</div>
<div id="list">
${pageMem.map((m,i)=>`<div class="item" data-cat="${escapeHtml(m.category||'general')}" data-text="${escapeHtml((m.text||'').toLowerCase())}">
<div class="item-head"><div class="meta"><span class="tag cat">${escapeHtml(m.category||'general')}</span><span class="tag imp">${((m.importance||0.5)*100).toFixed(0)}%</span><span style="color:#999;font-size:0.85em">${formatDate(m.created_at)}</span></div></div>
<div class="text">${escapeHtml(m.text||'')}</div>
<div class="id">ID: ${m.id||'n/a'}</div>
</div>`).join('')}
</div>
<div class="pages">
${page>1?`<a href="/memories?page=${page-1}">← Prev</a>`:''}
<span>Page ${page} of ${totalPages}</span>
${page<totalPages?`<a href="/memories?page=${page+1}">Next →</a>`:''}
</div>
</div>
</div>
<script>
function f(q){q=q.toLowerCase();document.querySelectorAll('.item').forEach(e=>{e.style.display=e.dataset.text.includes(q)?'block':'none'})}
function fcat(c){document.querySelectorAll('.item').forEach(e=>{e.style.display=!c||e.dataset.cat===c?'block':'none'})}
</script>
</body>
</html>`;
}

function renderSearch(query, results) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🔍 Search</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f5}
.header{background:linear-gradient(135deg,#667eea,#764ba2);padding:20px 0}
.container{max-width:900px;margin:0 auto;padding:20px}
h1{color:white;margin-bottom:20px}
.nav{display:flex;gap:12px;margin-bottom:20px}
.nav a{padding:10px 20px;background:rgba(255,255,255,0.2);color:white;text-decoration:none;border-radius:8px}
.nav a:hover,.nav a.active{background:white;color:#667eea}
.card{background:white;border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 4px 16px rgba(0,0,0,0.1)}
.box{width:100%;padding:16px 20px;border:2px solid #eee;border-radius:12px;font-size:1.1em;transition:border-color .2s}
.box:focus{outline:none;border-color:#667eea}
.result{padding:20px 0;border-bottom:1px solid #eee}
.result:last-child{border-bottom:none}
.score{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:4px 12px;border-radius:20px;font-size:0.85em;margin-bottom:8px}
.text{color:#333;line-height:1.6;margin:8px 0}
.meta{font-size:0.85em;color:#666;display:flex;gap:12px}
.empty{text-align:center;padding:60px 20px;color:#999}
</style>
</head>
<body>
<div class="header">
<div class="container">
<h1>🔍 Search</h1>
<nav class="nav">
<a href="/">📊 Dashboard</a>
<a href="/memories">📝 Memories</a>
<a href="/search" class="active">🔍 Search</a>
<a href="/graph">🕸️ Graph</a>
</nav>
</div>
</div>
<div class="container">
<div class="card">
<form method="get" action="/search">
<input type="text" name="q" class="box" placeholder="Search your memories..." value="${escapeHtml(query)}" autofocus>
</form>
</div>
${results.length>0?`<div class="card"><p style="margin-bottom:16px;color:#666">Found ${results.length} results for "${escapeHtml(query)}"</p>
${results.map(r=>`<div class="result">
<span class="score">${((r._score||0)*100).toFixed(0)}%</span>
<div class="text">${escapeHtml(r.text||'')}</div>
<div class="meta"><span>📁 ${escapeHtml(r.category||'general')}</span><span>⭐ ${((r.importance||0.5)*100).toFixed(0)}%</span><span>🕐 ${formatDate(r.created_at)}</span></div>
</div>`).join('')}
</div>`:query?`<div class="card"><div class="empty"><p>No results for "${escapeHtml(query)}"</p></div></div>`:''}
</div>
</body>
</html>`;
}

function renderGraph() {
  const { entities, relations } = getOntologyGraph();
  const types = [...new Set(entities.map(e=>e.type||'unknown'))];

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🕸️ Knowledge Graph</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f5}
.header{background:linear-gradient(135deg,#667eea,#764ba2);padding:20px 0}
.container{max-width:1200px;margin:0 auto;padding:20px}
h1{color:white;margin-bottom:20px}
.nav{display:flex;gap:12px;margin-bottom:20px}
.nav a{padding:10px 20px;background:rgba(255,255,255,0.2);color:white;text-decoration:none;border-radius:8px}
.nav a:hover,.nav a.active{background:white;color:#667eea}
.card{background:white;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
.stats{display:flex;justify-content:center;gap:60px;padding:20px 0}
.s{text-align:center}
.sv{font-size:2.5em;font-weight:bold;color:#667eea}
.sl{font-size:0.9em;color:#666;margin-top:4px}
.graph{height:500px;background:#fafafa;border-radius:8px;position:relative;overflow:hidden}
.node{position:absolute;padding:10px 18px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:25px;font-size:0.9em;cursor:pointer;transition:transform .2s,box-shadow .2s;box-shadow:0 4px 12px rgba(0,0,0,0.2)}
.node:hover{transform:scale(1.1);box-shadow:0 8px 24px rgba(0,0,0,0.3)}
.node.project{background:linear-gradient(135deg,#f093fb,#f5576c)}
.node.person{background:linear-gradient(135deg,#4facfe,#00f2fe)}
.node.task{background:linear-gradient(135deg,#43e97b,#38f9d7)}
.node.preference{background:linear-gradient(135deg,#fa709a,#fee140)}
.nodes{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.nodes>div{padding:12px 16px;border-radius:8px;font-size:0.9em}
.legend{display:flex;justify-content:center;gap:20px;margin-bottom:20px}
.legend>span{padding:6px 14px;border-radius:20px;font-size:0.85em;color:white}
</style>
</head>
<body>
<div class="header">
<div class="container">
<h1>🕸️ Knowledge Graph</h1>
<nav class="nav">
<a href="/">📊 Dashboard</a>
<a href="/memories">📝 Memories</a>
<a href="/search">🔍 Search</a>
<a href="/graph" class="active">🕸️ Graph</a>
</nav>
</div>
</div>
<div class="container">
<div class="card">
<div class="stats">
<div class="s"><div class="sv">${entities.length}</div><div class="sl">Entities</div></div>
<div class="s"><div class="sv">${relations.length}</div><div class="sl">Relations</div></div>
<div class="s"><div class="sv">${types.length}</div><div class="sl">Types</div></div>
</div>
</div>
<div class="card">
<h2 style="margin-bottom:16px">🕸️ Visualization</h2>
<div class="legend">
${types.map(t=>`<span class="node ${t}">${t}</span>`).join('')}
</div>
<div class="graph" id="graph"></div>
</div>
<div class="card">
<h2 style="margin-bottom:16px">📋 Entities</h2>
<div class="nodes">
${entities.map(e=>`<div class="node ${e.type||''}"><strong>${escapeHtml((e.properties||{}).name||e.id)}</strong><br><small>${escapeHtml(e.type||'unknown')}</small></div>`).join('')}
</div>
</div>
</div>
<script>
const entities=${JSON.stringify(entities.map(e=>({id:e.id,name:(e.properties||{}).name||e.id,type:e.type||'unknown'})))};
const relations=${JSON.stringify(relations)};
if(entities.length>0){
const container=document.getElementById('graph');
const rect=container.getBoundingClientRect();
const cx=rect.width/2,cy=rect.height/2;
const r=Math.min(rect.width,rect.height)*0.35;
entities.forEach((e,i)=>{
const angle=(2*Math.PI*i)/entities.length;
const x=cx+r*Math.cos(angle)-50;
const y=cy+r*Math.sin(angle)-20;
const node=document.createElement('div');
node.className='node '+(e.type||'');
node.style.left=x+'px';
node.style.top=y+'px';
node.innerHTML='<strong>'+e.name.substring(0,15)+'</strong>';
container.appendChild(node);
});
}
</script>
</body>
</html>`;
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'start') {
    const port = parseInt(args.find(a=>a.startsWith('--port='))?.split('=')[1]||DEFAULT_PORT);
    const host = args.find(a=>a.startsWith('--host='))?.split('=')[1]||DEFAULT_HOST;
    const ui = new MemoryWebUI(port, host);
    await ui.start();
    console.log('Press Ctrl+C to stop');
  } else if (command === 'dashboard') {
    const stats = getMemoryStats();
    console.log('\n📊 Memory Dashboard\n');
    console.log(`  Total: ${stats.total}`);
    console.log(`  Categories: ${Object.keys(stats.byCategory).length}`);
    console.log(`  Avg Importance: ${(stats.avgImportance*100).toFixed(1)}%`);
    console.log(`  High: ${stats.byImportance.high}, Medium: ${stats.byImportance.medium}, Low: ${stats.byImportance.low}`);
  } else {
    console.log('Usage:');
    console.log('  node webui.js start [--port=3838] [--host=0.0.0.0]');
    console.log('  node webui.js dashboard');
  }
}

const isMain = process.argv[1]?.endsWith('webui.js') || process.argv[1]?.endsWith('webui.mjs');
if (isMain) {
  main().catch(console.error);
}

export default { MemoryWebUI, getAllMemories, getMemoryStats, searchMemories };
