#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spider Web - Web Dashboard Server
Interactive management panel for the trigger network.
"""
import os, sys, json, time, threading
from pathlib import Path

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from index_triggers import index_all_skills, load_db, save_db
from match_engine import SpiderMatchEngine

# ── HTML Template ──────────────────────────────────────────────────

DASHBOARD_HTML = r'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🕷️ Spider Web - Trigger Network Dashboard</title>
<style>
:root {
  --bg: #0f0f1a;
  --card: #1a1a2e;
  --border: #2a2a4a;
  --text: #e0e0e0;
  --dim: #8888aa;
  --accent: #6c5ce7;
  --accent2: #00cec9;
  --green: #00b894;
  --yellow: #fdcb6e;
  --red: #ff6b6b;
  --orange: #e17055;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { 
  font-family: -apple-system, "Microsoft YaHei", sans-serif; 
  background: var(--bg); color: var(--text); 
  min-height: 100vh; 
}
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%);
  padding: 24px 32px; border-bottom: 2px solid var(--accent);
  display: flex; justify-content: space-between; align-items: center;
}
.header h1 { font-size: 24px; font-weight: 700; }
.header h1 span { color: var(--accent2); }
.header .actions { display: flex; gap: 12px; }
.btn {
  padding: 8px 20px; border-radius: 8px; border: none;
  font-size: 14px; cursor: pointer; font-weight: 600;
  transition: all 0.2s;
}
.btn-primary { background: var(--accent); color: white; }
.btn-primary:hover { background: #7c6ff7; }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { border-color: var(--accent); color: var(--accent); }
.btn-danger { background: var(--red); color: white; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; padding: 24px 32px; }
.stat-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px; text-align: center;
}
.stat-card .value { font-size: 36px; font-weight: 800; }
.stat-card .label { font-size: 13px; color: var(--dim); margin-top: 4px; }
.stat-card.accent .value { color: var(--accent); }
.stat-card.accent2 .value { color: var(--accent2); }
.stat-card.green .value { color: var(--green); }
.stat-card.orange .value { color: var(--orange); }
.main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 0 32px 32px; }
.panel {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px;
}
.panel h2 { font-size: 16px; margin-bottom: 16px; color: var(--accent2); }
.search-box {
  display: flex; gap: 8px; margin-bottom: 16px;
}
.search-box input {
  flex: 1; padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--bg); color: var(--text); font-size: 14px; outline: none;
}
.search-box input:focus { border-color: var(--accent); }
.match-result {
  border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.2s;
}
.match-result:hover { border-color: var(--accent); background: #1e1e35; }
.match-result.best { border-color: var(--accent2); border-width: 2px; }
.match-result .skill-name { font-size: 15px; font-weight: 700; }
.match-result .score { 
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 12px; font-weight: 700; margin-left: 8px;
}
.match-result .score.high { background: rgba(0,184,148,0.2); color: var(--green); }
.match-result .score.medium { background: rgba(253,203,110,0.2); color: var(--yellow); }
.match-result .score.low { background: rgba(136,136,170,0.2); color: var(--dim); }
.match-result .triggers { font-size: 12px; color: var(--dim); margin-top: 4px; }
.skill-list { max-height: 500px; overflow-y: auto; }
.skill-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; border-bottom: 1px solid var(--border); font-size: 13px;
}
.skill-item:hover { background: #1e1e35; }
.skill-item .count {
  background: var(--accent); color: white; padding: 2px 8px;
  border-radius: 10px; font-size: 11px; font-weight: 700;
}
.tag {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; margin: 2px; background: #2a2a4a;
}
.tag.exact { background: rgba(0,184,148,0.3); }
.tag.chinese { background: rgba(108,92,231,0.3); }
.toast {
  position: fixed; top: 20px; right: 20px; padding: 12px 24px;
  border-radius: 8px; font-size: 14px; z-index: 1000; opacity: 0;
  transition: opacity 0.3s; pointer-events: none;
}
.toast.show { opacity: 1; }
.toast.success { background: var(--green); color: white; }
.toast.error { background: var(--red); color: white; }
#network-viz {
  width: 100%; height: 400px; border: 1px solid var(--border);
  border-radius: 8px; background: var(--bg);
}
.legend { display: flex; gap: 16px; margin-top: 8px; font-size: 12px; color: var(--dim); }
.legend span { display: flex; align-items: center; gap: 4px; }
.legend .dot {
  width: 10px; height: 10px; border-radius: 50%; display: inline-block;
}
</style>
</head>
<body>
<div class="header">
  <h1>🕷️ Spider Web <span>Trigger Network</span></h1>
  <div class="actions">
    <button class="btn btn-outline" onclick="reindex()">🔄 重新索引</button>
    <button class="btn btn-outline" onclick="exportData()">📥 导出数据</button>
  </div>
</div>

<div class="grid" id="stats-grid"></div>

<div class="main-content">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <div class="panel">
      <h2>🔍 实时匹配测试</h2>
      <div class="search-box">
        <input type="text" id="query-input" placeholder="输入自然语言查询，测试触发词匹配..." 
               onkeydown="if(event.key==='Enter') testMatch()">
        <button class="btn btn-primary" onclick="testMatch()">匹配</button>
        <button class="btn btn-outline" onclick="toggleFuzzy()" id="fuzzy-btn">模糊</button>
      </div>
      <div id="match-results" style="max-height:400px;overflow-y:auto;"></div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:20px;">
    <div class="panel">
      <h2>📋 技能触发词分布</h2>
      <div class="skill-list" id="skill-list"></div>
    </div>
  </div>
</div>

<div id="toast" class="toast"></div>

<script>
let fuzzyMode = false;
let allData = null;

async function loadData() {
  const r = await fetch('/api/data');
  allData = await r.json();
  renderStats(allData);
  renderSkills(allData);
}

function renderStats(d) {
  const s = d.meta;
  document.getElementById('stats-grid').innerHTML = `
    <div class="stat-card accent"><div class="value">${s.total_skills}</div><div class="label">已索引技能</div></div>
    <div class="stat-card accent2"><div class="value">${s.total_triggers}</div><div class="label">触发词总数</div></div>
    <div class="stat-card green"><div class="value">${s.unique_triggers}</div><div class="label">唯一触发词</div></div>
    <div class="stat-card orange"><div class="value">${s.overlap_triggers}</div><div class="label">重叠触发词</div></div>
    <div class="stat-card"><div class="value">${s.avg_per_skill}</div><div class="label">平均触发词/技能</div></div>
    <div class="stat-card"><div class="value">${s.network_density||'N/A'}%</div><div class="label">网络密度</div></div>
  `;
}

function renderSkills(d) {
  const skills = d.skills || {};
  const sorted = Object.entries(skills).sort((a,b) => b[1].length - a[1].length);
  document.getElementById('skill-list').innerHTML = sorted.map(([name,triggers]) => `
    <div class="skill-item">
      <span>🕸️ ${name}</span>
      <span class="count">${triggers.length} 触发词</span>
    </div>
  `).join('');
}

async function testMatch() {
  const query = document.getElementById('query-input').value.trim();
  if (!query) return;
  
  const r = await fetch('/api/match', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query, mode: 'auto', fuzzy: fuzzyMode, top_k: 10})
  });
  const result = await r.json();
  
  const container = document.getElementById('match-results');
  if (!result.matches || result.matches.length === 0) {
    container.innerHTML = `<div style="padding:20px;text-align:center;color:var(--dim);">
      ❌ 未找到匹配技能<br><small>${result.suggestion||'试试其他关键词'}</small></div>`;
    return;
  }
  
  container.innerHTML = result.matches.map((m,i) => {
    const cls = m.score >= 10 ? 'high' : m.score >= 5 ? 'medium' : 'low';
    return `<div class="match-result ${i===0?'best':''}" onclick="document.getElementById('query-input').value='${m.skill}';testMatch()">
      <span class="skill-name">#${i+1} ${m.skill}</span>
      <span class="score ${cls}">${m.score.toFixed(1)}</span>
      <div class="triggers">触发: ${(m.matched_triggers||[]).join(', ')}</div>
    </div>`;
  }).join('');
  
  if (result.suggestion) {
    container.innerHTML += `<div style="font-size:12px;color:var(--dim);margin-top:8px;">💡 ${result.suggestion}</div>`;
  }
}

function toggleFuzzy() {
  fuzzyMode = !fuzzyMode;
  document.getElementById('fuzzy-btn').style.background = fuzzyMode ? 'var(--accent)' : 'transparent';
}

async function reindex() {
  showToast('正在重新索引...', 'success');
  const r = await fetch('/api/reindex', {method: 'POST'});
  const d = await r.json();
  await loadData();
  showToast(`索引完成: ${d.meta.total_skills} 技能, ${d.meta.total_triggers} 触发词`, 'success');
}

function exportData() {
  window.open('/api/export', '_blank');
}

function showToast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.className = `toast ${type} show`;
  setTimeout(() => t.classList.remove('show'), 2500);
}

loadData();
</script>
</body>
</html>
'''

# ── HTTP Server ────────────────────────────────────────────────────

class SpiderWebHandler(BaseHTTPRequestHandler):
    engine = None

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/' or path == '/dashboard':
            self._serve_html(DASHBOARD_HTML)
        elif path == '/api/data':
            self._serve_json(self._get_full_data())
        elif path == '/api/stats':
            self._serve_json(self._get_stats())
        elif path == '/api/export':
            self._serve_export()
        elif path == '/api/health':
            self._serve_json({"status": "ok", "timestamp": time.time()})
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len) if content_len > 0 else b'{}'
        try:
            data = json.loads(body)
        except:
            data = {}

        if path == '/api/match':
            self._handle_match(data)
        elif path == '/api/reindex':
            self._handle_reindex()
        else:
            self.send_error(404)

    def _handle_match(self, data):
        if not self.engine:
            self.engine = SpiderMatchEngine()
        query = data.get('query', '')
        mode = data.get('mode', 'auto')
        fuzzy = data.get('fuzzy', False)
        top_k = data.get('top_k', 10)
        result = self.engine.match(query, mode=mode, top_k=top_k, fuzzy=fuzzy)
        self._serve_json(result)

    def _handle_reindex(self):
        try:
            db = index_all_skills()
            save_db(db)
            self.engine = SpiderMatchEngine()  # reload
            self._serve_json(db)
        except Exception as e:
            self._serve_json({"error": str(e)}, 500)

    def _get_full_data(self):
        db = load_db()
        if not db:
            return {"error": "No database found"}
        if self.engine and self.engine.db:
            stats = self.engine.get_stats()
            db['meta']['network_density'] = stats.get('network_density', 0)
        return db

    def _get_stats(self):
        if not self.engine:
            self.engine = SpiderMatchEngine()
        return self.engine.get_stats()

    def _serve_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _serve_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _serve_export(self):
        db = load_db()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Disposition', 'attachment; filename="spider-web-triggers.json"')
        self.end_headers()
        self.wfile.write(json.dumps(db, ensure_ascii=False, indent=2).encode('utf-8'))

    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    import argparse
    # Fix encoding on Windows
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except: pass

    parser = argparse.ArgumentParser(description="Spider Web Dashboard Server")
    parser.add_argument("--port", type=int, default=8766, help="Server port")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    args = parser.parse_args()

    # Initialize engine
    SpiderWebHandler.engine = SpiderMatchEngine()

    server = HTTPServer((args.host, args.port), SpiderWebHandler)
    print(f"[Spider Web] Dashboard running at http://{args.host}:{args.port}")
    print(f"  Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
