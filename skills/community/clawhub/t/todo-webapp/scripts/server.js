#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3456;
const TODO_PATH = path.join(__dirname, '../TODO.md');
const BG_PATH = path.join(__dirname, 'bg.jpg');

// SSE clients
const sseClients = new Set();

// Watch TODO.md for changes and notify all SSE clients
function notifyClients() {
  for (const client of sseClients) {
    try { client.write('data: reload\n\n'); } catch(e) { sseClients.delete(client); }
  }
}
fs.watchFile(TODO_PATH, { interval: 500 }, () => {
  notifyClients();
});

function parseTodo(md) {
  const lines = md.split('\n');
  const sections = [];
  let current = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('## ')) {
      if (current) sections.push(current);
      current = { heading: line.slice(3), items: [], rawLines: [] };
    } else if (current) {
      const checked = line.match(/^(\s*)-\s+\[x\]\s+(.*)/i);
      const unchecked = line.match(/^(\s*)-\s+\[\s\]\s+(.*)/);
      if (checked) {
        current.items.push({ type: 'item', checked: true, text: checked[2], raw: line, lineIndex: i });
      } else if (unchecked) {
        current.items.push({ type: 'item', checked: false, text: unchecked[2], raw: line, lineIndex: i });
      } else if (line.startsWith('### ')) {
        current.items.push({ type: 'subheading', text: line.slice(4) });
      } else if (line.trim() === '' || line.startsWith('Completed') || line.startsWith('---')) {
        // skip
      } else if (line.trim()) {
        current.items.push({ type: 'note', text: line });
      }
    }
  }
  if (current) sections.push(current);
  return sections;
}

const DONE_PATH = path.join(__dirname, '../TODO-done.md');

function toggleLine(lineIndex, newState) {
  const md = fs.readFileSync(TODO_PATH, 'utf8');
  const lines = md.split('\n');
  const line = lines[lineIndex];
  if (newState) {
    lines[lineIndex] = line.replace(/- \[ \]/, '- [x]');
  } else {
    lines[lineIndex] = line.replace(/- \[x\]/i, '- [ ]');
  }
  fs.writeFileSync(TODO_PATH, lines.join('\n'), 'utf8');
}

function archiveDone() {
  const md = fs.readFileSync(TODO_PATH, 'utf8');
  const lines = md.split('\n');
  const keep = [];
  const done = [];

  for (const line of lines) {
    if (line.match(/^(\s*)-\s+\[x\]/i)) {
      // strip leading whitespace and extract text
      const m = line.match(/^(?:\s*)-\s+\[x\]\s+(.*)/i);
      done.push('- [x] ' + (m ? m[1] : line.trim()));
    } else {
      keep.push(line);
    }
  }

  if (done.length === 0) return 0;

  // Remove consecutive blank lines left behind
  const cleaned = keep.join('\n').replace(/\n{3,}/g, '\n\n').trimEnd() + '\n';
  fs.writeFileSync(TODO_PATH, cleaned, 'utf8');

  // Append to TODO-done.md
  const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'America/Chicago' });
  const doneEntry = `\n## Archived ${today}\n${done.join('\n')}\n`;
  fs.appendFileSync(DONE_PATH, doneEntry, 'utf8');

  return done.length;
}

function renderHTML(sections) {
  const sectionHTML = sections.map(sec => {
    const itemsHTML = sec.items.map(item => {
      if (item.type === 'subheading') {
        return `<h3 class="subheading">${escHtml(item.text)}</h3>`;
      }
      if (item.type === 'note') {
        return `<p class="note">${escHtml(item.text)}</p>`;
      }
      const cls = item.checked ? 'todo-item checked' : 'todo-item';
      const emoji = item.text.match(/^(🔥|⚡|✅)/)?.[0] || '';
      const textNoEmoji = emoji ? item.text.slice(emoji.length).trim() : item.text;
      const formatted = textNoEmoji.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      return `
        <div class="${cls}" data-line="${item.lineIndex}" data-checked="${item.checked}" onclick="toggle(this)">
          <span class="checkbox">${item.checked ? '✅' : '☐'}</span>
          <span class="item-text">${emoji ? `<span class="emoji">${emoji}</span>` : ''}${formatted}</span>
        </div>`;
    }).join('');
    return `
      <div class="section">
        <h2 class="section-heading">${escHtml(sec.heading)}</h2>
        <div class="section-body">${itemsHTML}</div>
      </div>`;
  }).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jim's TODO</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: Verdana, Geneva, sans-serif;
    min-height: 100vh;
    background: #1a1a2e;
    background-image: url('/bg.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: relative;
  }
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(10, 10, 30, 0.78);
    z-index: 0;
  }
  #app {
    position: relative;
    z-index: 1;
    max-width: 860px;
    margin: 0 auto;
    padding: 32px 20px 60px;
  }
  header {
    text-align: center;
    margin-bottom: 36px;
  }
  header h1 {
    font-size: 2rem;
    color: #fff;
    text-shadow: 0 2px 8px rgba(0,0,0,0.7);
    letter-spacing: 1px;
  }
  header p {
    color: rgba(255,255,255,0.55);
    font-size: 0.78rem;
    margin-top: 6px;
  }
  .archive-btn {
    display: inline-block;
    margin-top: 14px;
    padding: 8px 22px;
    background: rgba(80,200,120,0.25);
    color: #a8f0c0;
    border: 1px solid rgba(80,200,120,0.35);
    border-radius: 30px;
    font-family: Verdana, sans-serif;
    font-size: 0.78rem;
    cursor: pointer;
    box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    transition: background 0.15s, box-shadow 0.15s;
  }
  .archive-btn:hover {
    background: rgba(80,200,120,0.45);
    box-shadow: 0 5px 16px rgba(80,200,120,0.25);
  }
  #live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.45);
    margin-top: 8px;
  }
  #live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4caf50;
    box-shadow: 0 0 6px #4caf50;
    animation: pulse 2s infinite;
  }
  #live-dot.disconnected { background: #f44336; box-shadow: 0 0 6px #f44336; animation: none; }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }
  .section {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.08) inset;
    margin-bottom: 24px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .section-heading {
    font-size: 1rem;
    font-weight: bold;
    color: #e0d7ff;
    padding: 14px 20px;
    background: rgba(120, 80, 255, 0.2);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
  }
  .section-body { padding: 10px 16px 14px; }
  .subheading {
    font-size: 0.8rem;
    color: #a0c4ff;
    margin: 14px 0 6px 4px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .note {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.35);
    padding: 2px 8px;
    font-style: italic;
  }
  .todo-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 9px 12px;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.15s, transform 0.1s, box-shadow 0.15s;
    margin: 3px 0;
    user-select: none;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .todo-item:hover {
    background: rgba(255,255,255,0.13);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transform: translateY(-1px);
  }
  .todo-item:active { transform: scale(0.98); }
  .todo-item.checked {
    background: rgba(80,200,120,0.1);
    border-color: rgba(80,200,120,0.15);
  }
  .todo-item.checked .item-text {
    color: rgba(255,255,255,0.35);
    text-decoration: line-through;
  }
  .checkbox {
    font-size: 1rem;
    min-width: 22px;
    text-align: center;
    margin-top: 1px;
  }
  .item-text {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.88);
    line-height: 1.5;
    flex: 1;
  }
  .emoji { margin-right: 4px; }
  #toast {
    position: fixed;
    bottom: 28px;
    left: 50%;
    transform: translateX(-50%) translateY(60px);
    background: rgba(30,30,60,0.95);
    color: #fff;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 0.82rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    transition: transform 0.3s ease;
    z-index: 100;
    pointer-events: none;
  }
  #toast.show { transform: translateX(-50%) translateY(0); }
</style>
</head>
<body>
<div id="app">
  <header>
    <h1>🌸 Jim's TODO</h1>
    <div id="live-indicator">
      <span id="live-dot"></span>
      <span id="live-label">Live</span>
    </div>
    <div style="margin-top:10px;">
      <button class="archive-btn" onclick="archiveDone()">✅ Archive Done</button>
    </div>
  </header>
  ${sectionHTML}
</div>
<div id="toast"></div>
<script>
// SSE: auto-reload content when file changes
(function connectSSE() {
  const dot = document.getElementById('live-dot');
  const label = document.getElementById('live-label');
  const es = new EventSource('/events');
  es.onmessage = (e) => {
    if (e.data === 'reload') {
      // Fetch fresh HTML and swap just the sections
      fetch('/sections')
        .then(r => r.text())
        .then(html => {
          document.getElementById('app').innerHTML = html;
          showToast('↻ Updated');
        });
    }
  };
  es.onopen = () => {
    dot.classList.remove('disconnected');
    label.textContent = 'Live';
  };
  es.onerror = () => {
    dot.classList.add('disconnected');
    label.textContent = 'Reconnecting...';
    es.close();
    setTimeout(connectSSE, 3000);
  };
})();

function toggle(el) {
  const line = el.dataset.line;
  const checked = el.dataset.checked === 'true';
  const newState = !checked;
  fetch('/toggle', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ lineIndex: parseInt(line), checked: newState })
  }).then(r => r.json()).then(d => {
    if (d.ok) {
      el.dataset.checked = String(newState);
      el.classList.toggle('checked', newState);
      el.querySelector('.checkbox').textContent = newState ? '✅' : '☐';
      showToast(newState ? '✅ Done!' : '↩ Reopened');
    }
  });
}

function archiveDone() {
  fetch('/archive', { method: 'POST' })
    .then(r => r.json())
    .then(d => {
      if (d.count > 0) showToast('📦 Archived ' + d.count + ' item' + (d.count > 1 ? 's' : ''));
      else showToast('Nothing to archive');
    });
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1800);
}
</script>
</body>
</html>`;
}

function renderSections(sections) {
  return `<header>
    <h1>🌸 Jim's TODO</h1>
    <div id="live-indicator">
      <span id="live-dot"></span>
      <span id="live-label">Live</span>
    </div>
    <div style="margin-top:10px;">
      <button class="archive-btn" onclick="archiveDone()">✅ Archive Done</button>
    </div>
  </header>` + sections.map(sec => {
    const itemsHTML = sec.items.map(item => {
      if (item.type === 'subheading') return `<h3 class="subheading">${escHtml(item.text)}</h3>`;
      if (item.type === 'note') return `<p class="note">${escHtml(item.text)}</p>`;
      const cls = item.checked ? 'todo-item checked' : 'todo-item';
      const emoji = item.text.match(/^(🔥|⚡|✅)/)?.[0] || '';
      const textNoEmoji = emoji ? item.text.slice(emoji.length).trim() : item.text;
      const formatted = textNoEmoji.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      return `
        <div class="${cls}" data-line="${item.lineIndex}" data-checked="${item.checked}" onclick="toggle(this)">
          <span class="checkbox">${item.checked ? '✅' : '☐'}</span>
          <span class="item-text">${emoji ? `<span class="emoji">${emoji}</span>` : ''}${formatted}</span>
        </div>`;
    }).join('');
    return `
      <div class="section">
        <h2 class="section-heading">${escHtml(sec.heading)}</h2>
        <div class="section-body">${itemsHTML}</div>
      </div>`;
  }).join('');
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    const md = fs.readFileSync(TODO_PATH, 'utf8');
    const sections = parseTodo(md);
    const html = renderHTML(sections);
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
    res.end(html);

  } else if (req.method === 'GET' && req.url === '/sections') {
    const md = fs.readFileSync(TODO_PATH, 'utf8');
    const sections = parseTodo(md);
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
    res.end(renderSections(sections));

  } else if (req.method === 'GET' && req.url === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    res.write(': connected\n\n');
    sseClients.add(res);
    req.on('close', () => sseClients.delete(res));

  } else if (req.method === 'GET' && req.url === '/bg.jpg') {
    const img = fs.readFileSync(BG_PATH);
    res.writeHead(200, {'Content-Type': 'image/jpeg'});
    res.end(img);

  } else if (req.method === 'POST' && req.url === '/toggle') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { lineIndex, checked } = JSON.parse(body);
        toggleLine(lineIndex, checked);
        notifyClients();
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ ok: true }));
      } catch(e) {
        res.writeHead(400, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });

  } else if (req.method === 'POST' && req.url === '/archive') {
    try {
      const count = archiveDone();
      notifyClients();
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({ ok: true, count }));
    } catch(e) {
      res.writeHead(500, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }

  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`TODO server running at http://0.0.0.0:${PORT}`);
});
