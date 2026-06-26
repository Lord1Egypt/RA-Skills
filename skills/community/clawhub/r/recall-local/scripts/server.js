#!/usr/bin/env node
// Recall Local — search Wren's memory files at http://localhost:3456
// No dependencies. Just: node server.js

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = 3456;
const MEMORY_DIR = path.join(os.homedir(), 'clawd', 'memory');
const MEMORY_FILE = path.join(os.homedir(), 'clawd', 'MEMORY.md');
const WORKING_FILE = path.join(os.homedir(), 'clawd', 'WORKING.md');

// ── Load and index all memory files ──────────────────────────────────────────

function loadMemories() {
  const chunks = [];

  function addFile(filePath, source) {
    if (!fs.existsSync(filePath)) return;
    const text = fs.readFileSync(filePath, 'utf8');
    // Split by double newline (paragraphs) or ## headers
    const parts = text.split(/\n(?=##|\n)/).map(s => s.trim()).filter(s => s.length > 20);
    for (const part of parts) {
      chunks.push({ text: part, source: path.basename(source || filePath), file: filePath });
    }
  }

  // Core files
  addFile(MEMORY_FILE, 'MEMORY.md');
  addFile(WORKING_FILE, 'WORKING.md');

  // Daily logs
  if (fs.existsSync(MEMORY_DIR)) {
    const files = fs.readdirSync(MEMORY_DIR)
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse(); // newest first
    for (const f of files) {
      addFile(path.join(MEMORY_DIR, f), f);
    }
  }

  return chunks;
}

function search(memories, query, limit = 20) {
  if (!query || !query.trim()) return memories.slice(0, limit);

  const words = query.toLowerCase().split(/\s+/).filter(w => w.length > 1);
  if (!words.length) return memories.slice(0, limit);

  const scored = memories.map(m => {
    const haystack = m.text.toLowerCase();
    let score = 0;
    for (const w of words) {
      if (haystack.includes(w)) {
        score += 1;
        // Bonus for exact multi-word phrase
        if (words.length > 1 && haystack.includes(query.toLowerCase())) score += 3;
      }
    }
    return { ...m, score };
  }).filter(m => m.score > 0);

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, limit);
}

// ── HTML ──────────────────────────────────────────────────────────────────────

const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recall</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,sans-serif; background:#0d1117; color:#c9d1d9; min-height:100vh; }
.page { padding:20px 16px; max-width:680px; margin:0 auto; }
.logo { text-align:center; margin:50px 0 36px; }
.logo h1 { font-size:2.8rem; font-weight:700; color:#f0f6fc; letter-spacing:-1px; }
.logo h1 span { color:#58a6ff; }
.logo p { color:#8b949e; font-size:0.85rem; margin-top:6px; }
.search-box { display:flex; flex-direction:column; gap:10px; }
.search-box input {
  width:100%; padding:16px 18px; font-size:1rem;
  background:#161b22; border:2px solid #30363d; border-radius:12px;
  color:#f0f6fc; outline:none;
}
.search-box input:focus { border-color:#58a6ff; }
.search-box button {
  width:100%; padding:16px; font-size:1rem; font-weight:700;
  background:#58a6ff; color:#0d1117; border:none; border-radius:12px; cursor:pointer;
}
.search-box button:active { background:#79b8ff; }
#status { margin-top:18px; font-size:0.8rem; color:#8b949e; min-height:18px; }
#results { margin-top:10px; display:flex; flex-direction:column; gap:10px; padding-bottom:40px; }
.card { background:#161b22; border:1px solid #21262d; border-radius:10px; padding:14px 16px; }
.card-text { white-space:pre-wrap; line-height:1.55; font-size:0.88rem; word-break:break-word; }
.card-meta { margin-top:8px; font-size:0.72rem; color:#8b949e; }
.card-meta .src { color:#58a6ff; }
</style>
</head>
<body>
<div class="page">
  <div class="logo">
    <h1>Re<span>c</span>all 🧠</h1>
    <p>Your agent's memory &mdash; local &amp; private</p>
  </div>
  <div class="search-box">
    <input type="text" id="q" placeholder="Search memories..." autocomplete="off" autocorrect="off" autocapitalize="off">
    <button id="btn">Search</button>
  </div>
  <div id="status"></div>
  <div id="results"></div>
</div>
<script>
document.getElementById('btn').addEventListener('click', run);
document.getElementById('q').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') run();
});

function run() {
  var q = document.getElementById('q').value.trim();
  document.getElementById('status').textContent = q ? 'Searching...' : 'Loading recent...';
  document.getElementById('results').innerHTML = '';
  fetch('/search?q=' + encodeURIComponent(q))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var list = data.results || [];
      document.getElementById('status').textContent = list.length + ' result' + (list.length !== 1 ? 's' : '') + (q ? ' for "' + esc(q) + '"' : '');
      if (!list.length) {
        document.getElementById('results').innerHTML = '<div style="text-align:center;color:#8b949e;padding:30px">Nothing found</div>';
        return;
      }
      document.getElementById('results').innerHTML = list.map(function(m) {
        return '<div class="card"><div class="card-text">' + esc(m.text) + '</div>'
          + '<div class="card-meta"><span class="src">' + esc(m.source) + '</span></div></div>';
      }).join('');
    })
    .catch(function(e) { document.getElementById('status').textContent = 'Error: ' + e.message; });
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Load recent on page open
run();
</script>
</body>
</html>`;

// ── Server ────────────────────────────────────────────────────────────────────

let memories = [];

function reload() {
  memories = loadMemories();
  console.log(`Loaded ${memories.length} memory chunks`);
}

reload();

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(HTML);
    return;
  }

  if (url.pathname === '/search') {
    const q = url.searchParams.get('q') || '';
    // Reload files on each search so it always reflects latest memory
    reload();
    const results = search(memories, q);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ results, total: memories.length }));
    return;
  }

  if (url.pathname === '/reload') {
    reload();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, chunks: memories.length }));
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`\nRecall running at http://localhost:${PORT}`);
  console.log('Memory files: MEMORY.md + WORKING.md + memory/*.md');
  console.log('Press Ctrl+C to stop\n');

  // To open: http://localhost:3456
});
