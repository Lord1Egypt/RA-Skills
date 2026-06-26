/**
 * unified-memory v2.7.0 — Dashboard Web UI Server
 * 
 * A lightweight Express-based monitoring dashboard for unified-memory.
 * Serves real-time stats, health, and management via AJAX.
 * 
 * Usage:
 *   node src/webui/dashboard.js [--port=3849]
 * 
 * Access: http://localhost:3849
 */

import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { createRequire } from 'module';
import { homedir } from 'os';
import { getAllMemories, saveMemories } from '../storage.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Try to load express from MCP SDK (peer dependency path)
let express = null;
try {
  const require = createRequire(import.meta.url);
  express = require('@modelcontextprotocol/sdk/node_modules/express');
} catch {
  // Fallback: use built-in http module
}

const HOME = homedir();
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_FILE = join(WORKSPACE, 'memory', 'memories.json');
const VECTOR_DB_DIR = join(HOME, '.unified-memory', 'vector.lance');
const PORT = parseInt(process.argv.find(a => a.startsWith('--port='))?.split('=')[1]) || 3849;

// ============================================================
// Data Loading Helpers
// ============================================================
// saveMemories now delegated to ../storage.js

// ============================================================
// Metrics Computation
// ============================================================

let _metricsCache = null;
let _metricsCacheTime = 0;
const METRICS_CACHE_TTL = 2000; // 2 seconds

function getStats() {
  const now = Date.now();
  if (_metricsCache && (now - _metricsCacheTime) < METRICS_CACHE_TTL) {
    return _metricsCache;
  }

  const memories = getAllMemories();
  const byCategory = {};
  const byScope = { AGENT: 0, USER: 0, TEAM: 0, GLOBAL: 0, unknown: 0 };
  const byTier = { HOT: 0, WARM: 0, COLD: 0 };
  const byImportance = { high: 0, medium: 0, low: 0 };
  let totalAccessCount = 0;
  const accessCounts = [];

  for (const m of memories) {
    // Category
    const cat = m.category || 'unknown';
    byCategory[cat] = (byCategory[cat] || 0) + 1;

    // Scope
    const scope = m.scope || 'unknown';
    if (scope in byScope) byScope[scope]++;
    else byScope.unknown++;

    // Tier
    if (m.tier) byTier[m.tier] = (byTier[m.tier] || 0) + 1;

    // Importance
    const imp = m.importance ?? 0.5;
    if (imp >= 0.7) byImportance.high++;
    else if (imp >= 0.4) byImportance.medium++;
    else byImportance.low++;

    // Access
    totalAccessCount += m.access_count || 0;
    if (m.access_count) accessCounts.push(m.access_count);
  }

  // Recent growth (last 7 days)
  const sevenDaysAgo = new Date(now - 7 * 24 * 60 * 60 * 1000);
  const growth7d = memories.filter(m => new Date(m.created_at) >= sevenDaysAgo).length;

  // Per-day growth for chart (last 14 days)
  const growthTrend = [];
  for (let i = 13; i >= 0; i--) {
    const dayStart = new Date(now - i * 24 * 60 * 60 * 1000);
    dayStart.setHours(0, 0, 0, 0);
    const dayEnd = new Date(dayStart);
    dayEnd.setDate(dayEnd.getDate() + 1);
    const count = memories.filter(m => {
      const d = new Date(m.created_at);
      return d >= dayStart && d < dayEnd;
    }).length;
    const label = `${dayStart.getMonth() + 1}/${dayStart.getDate()}`;
    growthTrend.push({ label, count });
  }

  _metricsCache = {
    total: memories.length,
    byCategory,
    byScope,
    byTier,
    byImportance,
    totalAccessCount,
    avgAccessCount: accessCounts.length ? (totalAccessCount / accessCounts.length).toFixed(2) : 0,
    growth7d,
    growthTrend,
    topTags: getTopTags(memories),
  };
  _metricsCacheTime = now;
  return _metricsCache;
}

function getTopTags(memories, topN = 10) {
  const tagCount = {};
  for (const m of memories) {
    if (Array.isArray(m.tags)) {
      for (const tag of m.tags) {
        tagCount[tag] = (tagCount[tag] || 0) + 1;
      }
    }
  }
  return Object.entries(tagCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([tag, count]) => ({ tag, count }));
}

// ============================================================
// Health Check
// ============================================================

async function getHealth() {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    ollama: { status: 'unknown' },
    lancedb: { status: 'unknown' },
    memoryFile: { status: 'unknown' },
    storage: { status: 'unknown', used: 0, total: 0, percent: 0 },
    memory: { status: 'unknown' },
  };

  // Ollama check
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 3000);
    const res = await fetch('http://localhost:11434/api/tags', { signal: controller.signal });
    clearTimeout(timeout);
    if (res.ok) {
      health.ollama = { status: 'online', url: 'http://localhost:11434' };
    } else {
      health.ollama = { status: 'degraded', code: res.status };
      health.status = 'degraded';
    }
  } catch {
    health.ollama = { status: 'offline', url: 'http://localhost:11434' };
    health.status = health.status === 'healthy' ? 'degraded' : health.status;
  }

  // Memory file check
  try {
    if (existsSync(MEMORY_FILE)) {
      const stat = fs.statSync(MEMORY_FILE);
      health.memoryFile = {
        status: 'ok',
        size: stat.size,
        sizeMB: (stat.size / 1024 / 1024).toFixed(2),
        path: MEMORY_FILE,
      };
      health.memory = { status: 'ok', count: getAllMemories().length };
    } else {
      health.memoryFile = { status: 'not_found', path: MEMORY_FILE };
      health.memory = { status: 'empty', count: 0 };
    }
  } catch (e) {
    health.memoryFile = { status: 'error', error: e.message };
    health.status = 'unhealthy';
  }

  // LanceDB check
  try {
    if (existsSync(VECTOR_DB_DIR)) {
      health.lancedb = { status: 'ok', path: VECTOR_DB_DIR };
    } else {
      health.lancedb = { status: 'not_initialized', path: VECTOR_DB_DIR };
    }
  } catch (e) {
    health.lancedb = { status: 'error', error: e.message };
  }

  // Storage check (workspace)
  try {
    const workspaceStat = fs.statSync(WORKSPACE);
    health.storage.path = WORKSPACE;
    // Check disk usage
    const { execSync } = await import('child_process');
    try {
      const df = execSync('df -B1 ' + WORKSPACE + ' 2>/dev/null').toString().split('\n')[1];
      if (df) {
        const parts = df.split(/\s+/);
        const total = parseInt(parts[1]) || 0;
        const used = parseInt(parts[2]) || 0;
        health.storage.total = total;
        health.storage.used = used;
        health.storage.percent = total > 0 ? Math.round((used / total) * 100) : 0;
        health.storage.status = health.storage.percent > 90 ? 'critical' : health.storage.percent > 75 ? 'warning' : 'ok';
      }
    } catch { /* df not available */ }
  } catch (e) {
    health.storage.status = 'error';
  }

  return health;
}

// ============================================================
// HTML Dashboard Template
// ============================================================

function buildDashboard(stats, health) {
  const s = stats || {};
  const h = health || {};
  const statusColor = { healthy: '#22c55e', degraded: '#f59e0b', unhealthy: '#ef4444', offline: '#ef4444' };
  const status = h.status || 'unknown';

  const categoryBars = Object.entries(s.byCategory || {})
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([cat, count]) => {
      const max = Math.max(...Object.values(s.byCategory || {}), 1);
      const pct = Math.round((count / max) * 100);
      return `<div class="bar-row"><span class="bar-label">${cat}</span><div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div><span class="bar-count">${count}</span></div>`;
    }).join('');

  const scopeData = Object.entries(s.byScope || {})
    .filter(([k]) => k !== 'unknown')
    .map(([k, v]) => `{ label: '${k}', value: ${v} }`).join(',');

  const growthLabels = (s.growthTrend || []).map(d => `'${d.label}'`).join(',');
  const growthData = (s.growthTrend || []).map(d => d.count).join(',');

  const tagCloud = (s.topTags || []).map(({ tag, count }) => {
    const max = s.topTags?.[0]?.count || 1;
    const size = 12 + Math.round((count / max) * 12);
    return `<span class="tag-item" style="font-size:${size}px">${tag}(${count})</span>`;
  }).join('');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🧠 Unified Memory v2.7 — Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}
header{background:#1e293b;padding:16px 24px;border-bottom:1px solid #334155;display:flex;align-items:center;justify-content:space-between}
header h1{font-size:18px;color:#f1f5f9}
header .version{color:#94a3b8;font-size:12px}
.main{padding:20px;max-width:1400px;margin:0 auto}
.status-bar{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.card{background:#1e293b;border-radius:10px;padding:18px;border:1px solid #334155}
.card h2{font-size:13px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:20px}
.stat-card{background:#1e293b;border-radius:10px;padding:16px;border:1px solid #334155;text-align:center}
.stat-card .num{font-size:28px;font-weight:700;color:#f1f5f9}
.stat-card .lbl{font-size:11px;color:#94a3b8;margin-top:4px;text-transform:uppercase}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.bar-row{display:flex;align-items:center;gap:8px;margin:4px 0}
.bar-label{width:80px;font-size:12px;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar-track{flex:1;height:8px;background:#334155;border-radius:4px;overflow:hidden}
.bar-fill{height:100%;background:#3b82f6;border-radius:4px;transition:width .3s}
.bar-count{width:36px;text-align:right;font-size:12px;color:#94a3b8}
.tag-cloud{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.tag-item{background:#334155;padding:3px 8px;border-radius:4px;color:#94a3b8}
.health-item{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #334155}
.health-item:last-child{border-bottom:none}
.health-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:8px}
.btn{background:#3b82f6;color:#fff;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:13px}
.btn:hover{background:#2563eb}
.btn-danger{background:#ef4444}
.btn-danger:hover{background:#dc2626}
.btn-row{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.chart-container{position:relative;height:160px}
#growthChart{width:100%;height:160px}
.row{display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap}
.col{flex:1;min-width:300px}
.refresh-info{font-size:11px;color:#64748b;text-align:right;margin-top:4px}
.health-badge{display:inline-flex;align-items:center;padding:4px 10px;border-radius:12px;font-size:12px;font-weight:600}
.health-badge.healthy{background:#166534;color:#4ade80}
.health-badge.degraded{background:#854d0e;color:#fbbf24}
.health-badge.unhealthy{background:#991b1b;color:#f87171}
.hidden{display:none}
#apiMsg{font-size:13px;margin-top:8px;padding:8px;border-radius:6px}
#apiMsg.success{background:#166534;color:#4ade80}
#apiMsg.error{background:#991b1b;color:#f87171}
canvas{width:100%!important;height:160px!important}
</style>
</head>
<body>
<header>
  <h1>🧠 Unified Memory v2.7 — Dashboard</h1>
  <div>
    <span class="version">v2.6 → v2.7</span>
    <span id="healthBadge" class="health-badge ${status}">${status}</span>
  </div>
</header>
<div class="main">
  <!-- Stats Row -->
  <div class="stat-grid">
    <div class="stat-card"><div class="num" id="statTotal">${s.total || 0}</div><div class="lbl">Total Memories</div></div>
    <div class="stat-card"><div class="num" id="statGrowth">${s.growth7d || 0}</div><div class="lbl">+7 Days</div></div>
    <div class="stat-card"><div class="num" id="statAccess">${s.totalAccessCount || 0}</div><div class="lbl">Total Accesses</div></div>
    <div class="stat-card"><div class="num" id="statAvgAccess">${s.avgAccessCount || 0}</div><div class="lbl">Avg Access</div></div>
  </div>

  <!-- Health + Scope -->
  <div class="row">
    <div class="col">
      <div class="card">
        <h2>🔧 System Health</h2>
        <div class="health-item">
          <span><span class="health-dot" style="background:${statusColor[health.ollama?.status]||'#94a3b8'}"></span>Ollama</span>
          <span style="color:#94a3b8;font-size:12px">${h.ollama?.status || 'unknown'}</span>
        </div>
        <div class="health-item">
          <span><span class="health-dot" style="background:${statusColor[health.memoryFile?.status]||'#94a3b8'}"></span>Memory File</span>
          <span style="color:#94a3b8;font-size:12px">${h.memoryFile?.sizeMB || '?'} MB</span>
        </div>
        <div class="health-item">
          <span><span class="health-dot" style="background:${statusColor[health.lancedb?.status]||'#94a3b8'}"></span>LanceDB</span>
          <span style="color:#94a3b8;font-size:12px">${h.lancedb?.status || 'unknown'}</span>
        </div>
        <div class="health-item">
          <span><span class="health-dot" style="background:${statusColor[health.storage?.status]||'#94a3b8'}"></span>Storage</span>
          <span style="color:#94a3b8;font-size:12px">${h.storage?.percent || 0}% used</span>
        </div>
        <div id="apiMsg"></div>
        <div class="btn-row">
          <button class="btn btn-danger" onclick="doCleanup()">🗑️ Cleanup Old</button>
          <button class="btn" onclick="doExport()">📤 Export JSON</button>
          <button class="btn" onclick="refreshAll()">🔄 Refresh</button>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h2>📊 Memory Growth (14d)</h2>
        <canvas id="growthChart"></canvas>
        <div class="refresh-info">Updated: <span id="updateTime">${new Date().toLocaleTimeString()}</span></div>
      </div>
    </div>
  </div>

  <!-- Categories -->
  <div class="row">
    <div class="col">
      <div class="card">
        <h2>📂 By Category</h2>
        ${categoryBars || '<p style="color:#64748b;font-size:13px">No data</p>'}
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h2>🏷️ Top Tags</h2>
        <div class="tag-cloud">${tagCloud || '<span style="color:#64748b;font-size:13px">No tags</span>'}</div>
      </div>
    </div>
  </div>

  <!-- Tiers + Scopes -->
  <div class="row">
    <div class="col">
      <div class="card">
        <h2>🌡️ By Tier (HOT/WARM/COLD)</h2>
        <div style="display:flex;gap:16px;margin-top:8px">
          ${['HOT','WARM','COLD'].map(tier => {
            const colors = { HOT: '#ef4444', WARM: '#f59e0b', COLD: '#3b82f6' };
            const count = s.byTier?.[tier] || 0;
            const max = Math.max(s.byTier?.HOT||1, s.byTier?.WARM||1, s.byTier?.COLD||1, 1);
            return `<div style="flex:1;text-align:center">
              <div style="font-size:22px;font-weight:700;color:${colors[tier]}">${count}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px">${tier}</div>
              <div style="height:6px;background:#334155;border-radius:3px;margin-top:6px">
                <div style="height:100%;width:${Math.round((count/max)*100)}%;background:${colors[tier]};border-radius:3px"></div>
              </div>
            </div>`;
          }).join('')}
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h2>🔒 By Scope</h2>
        <canvas id="scopeChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Importance -->
  <div class="row">
    <div class="col">
      <div class="card">
        <h2>⭐ By Importance</h2>
        <div style="display:flex;gap:16px;margin-top:8px">
          ${[['high','≥0.7','#22c55e'],['medium','0.4-0.7','#f59e0b'],['low','<0.4','#94a3b8']].map(([lvl,range,color]) => {
            const count = s.byImportance?.[lvl] || 0;
            return `<div style="flex:1;text-align:center">
              <div style="font-size:22px;font-weight:700;color:${color}">${count}</div>
              <div style="font-size:11px;color:#94a3b8;margin-top:4px">${lvl} (${range})</div>
            </div>`;
          }).join('')}
        </div>
      </div>
    </div>
    <div class="col">
      <div class="card">
        <h2>⚡ Quick Info</h2>
        <div class="health-item"><span>Memory File</span><span style="color:#94a3b8;font-size:12px">${h.memoryFile?.path || '-'}</span></div>
        <div class="health-item"><span>LanceDB Path</span><span style="color:#94a3b8;font-size:12px">${h.lancedb?.path ? h.lancedb.path.split('/').slice(-2).join('/') : '-'}</span></div>
        <div class="health-item"><span>Dashboard</span><span style="color:#94a3b8;font-size:12px">port ${PORT}</span></div>
        <div class="health-item"><span>Version</span><span style="color:#94a3b8;font-size:12px">v2.7.0</span></div>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
// Chart.js init
let growthChart, scopeChart;

function initCharts(growthLabels, growthData, scopeData) {
  const growthCtx = document.getElementById('growthChart').getContext('2d');
  growthChart = new Chart(growthCtx, {
    type: 'bar',
    data: {
      labels: growthLabels,
      datasets: [{
        label: 'Memories Added',
        data: growthData,
        backgroundColor: 'rgba(59,130,246,0.7)',
        borderRadius: 4,
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: '#334155' } }, y: { ticks: { color: '#64748b' }, grid: { color: '#334155' }, beginAtZero: true } } }
  });

  const scopeCtx = document.getElementById('scopeChart').getContext('2d');
  scopeChart = new Chart(scopeCtx, {
    type: 'doughnut',
    data: {
      labels: ['AGENT', 'USER', 'TEAM', 'GLOBAL'],
      datasets: [{
        data: scopeData,
        backgroundColor: ['#ef4444','#3b82f6','#22c55e','#f59e0b'],
        borderWidth: 0,
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 11 }, boxWidth: 12 } } } }
  });
}

async function refreshAll() {
  try {
    const [statsRes, healthRes] = await Promise.all([
      fetch('/api/stats'),
      fetch('/api/health')
    ]);
    const stats = await statsRes.json();
    const health = await healthRes.json();
    updateDashboard(stats, health);
  } catch (e) { console.error('Refresh failed', e); }
}

function updateDashboard(stats, health) {
  // Update stats
  document.getElementById('statTotal').textContent = stats.total || 0;
  document.getElementById('statGrowth').textContent = stats.growth7d || 0;
  document.getElementById('statAccess').textContent = stats.totalAccessCount || 0;
  document.getElementById('statAvgAccess').textContent = stats.avgAccessCount || 0;
  document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();

  // Update health badge
  const status = health.status || 'unknown';
  const badge = document.getElementById('healthBadge');
  badge.className = 'health-badge ' + status;
  badge.textContent = status;

  // Update charts
  if (growthChart && stats.growthTrend) {
    growthChart.data.labels = stats.growthTrend.map(d => d.label);
    growthChart.data.datasets[0].data = stats.growthTrend.map(d => d.count);
    growthChart.update();
  }
}

async function doCleanup() {
  if (!confirm('清理30天前未访问的记忆？')) return;
  try {
    const r = await fetch('/api/manage', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: 'cleanup', days: 30 }) });
    const data = await r.json();
    showMsg(data.message || JSON.stringify(data), r.ok);
    if (r.ok) setTimeout(refreshAll, 500);
  } catch (e) { showMsg('请求失败: ' + e.message, false); }
}

async function doExport() {
  try {
    const r = await fetch('/api/export');
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'memories_export_' + new Date().toISOString().slice(0,10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
    showMsg('导出成功', true);
  } catch (e) { showMsg('导出失败: ' + e.message, false); }
}

function showMsg(text, success) {
  const el = document.getElementById('apiMsg');
  el.textContent = text;
  el.className = success ? 'success' : 'error';
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 4000);
}

// Poll every 5s
let initialized = false;
async function init() {
  try {
    const [statsRes, healthRes] = await Promise.all([fetch('/api/stats'), fetch('/api/health')]);
    const stats = await statsRes.json();
    const health = await healthRes.json();
    if (!initialized) {
      const gl = (stats.growthTrend || []).map(d => d.label);
      const gd = (stats.growthTrend || []).map(d => d.count);
      const scopeVals = ['AGENT','USER','TEAM','GLOBAL'].map(k => stats.byScope?.[k] || 0);
      initCharts(gl, gd, scopeVals);
      initialized = true;
    }
    updateDashboard(stats, health);
  } catch (e) { console.error(e); }
  setTimeout(init, 5000);
}
init();
</script>
</body>
</html>`;
}

// ============================================================
// Management Actions
// ============================================================

function doCleanup(days = 30) {
  const memories = getAllMemories();
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const before = memories.length;
  const filtered = memories.filter(m => {
    const lastAccess = m.last_accessed ? new Date(m.last_accessed).getTime() : 0;
    const created = new Date(m.created_at).getTime();
    // Keep if accessed recently or created recently
    return lastAccess >= cutoff || created >= cutoff;
  });
  saveMemories(filtered);
  _metricsCache = null;
  return { cleaned: before - filtered.length, remaining: filtered.length };
}

// ============================================================
// Server
// ============================================================

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.ico': 'image/x-icon',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};

async function handleRequest(req, res) {
  const url = req.url.split('?')[0];

  // CORS + JSON headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  // ── HTML Dashboard ───────────────────────────────────────
  if ((url === '/' || url === '/dashboard') && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    const stats = getStats();
    const health = await getHealth();
    res.end(buildDashboard(stats, health));
    return;
  }

  // ── API Routes ──────────────────────────────────────────
  res.setHeader('Content-Type', 'application/json');

  if (url === '/api/stats' && req.method === 'GET') {
    res.end(JSON.stringify(getStats()));
    return;
  }

  if (url === '/api/health' && req.method === 'GET') {
    const health = await getHealth();
    res.end(JSON.stringify(health));
    return;
  }

  if (url === '/api/memories' && req.method === 'GET') {
    const memories = getAllMemories();
    res.end(JSON.stringify(memories));
    return;
  }

  if (url === '/api/export' && req.method === 'GET') {
    const memories = getAllMemories();
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Content-Disposition': `attachment; filename="memories_${new Date().toISOString().slice(0,10)}.json"`
    });
    res.end(JSON.stringify(memories, null, 2));
    return;
  }

  if (url === '/api/manage' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', async () => {
      try {
        const { action, days } = JSON.parse(body);
        if (action === 'cleanup') {
          const result = doCleanup(days || 30);
          res.end(JSON.stringify({ success: true, ...result }));
        } else {
          res.writeHead(400);
          res.end(JSON.stringify({ error: 'Unknown action' }));
        }
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // 404
  res.writeHead(404);
  res.end(JSON.stringify({ error: 'Not found' }));
}

// ── Express path (if available) ──────────────────────────
// Auto-start on CLI invocation (node src/webui/dashboard.js --port=XXXX)
// But NOT when imported as a module (used by memory_dashboard MCP tool)

const isMain = process.argv[1] && process.argv[1].endsWith('dashboard.js');
const AUTO_PORT = parseInt(process.argv.find(a => a.startsWith('--port='))?.split('=')[1]) || 3849;

export function startDashboard(port = 3849) {
  const server = http.createServer((req, res) => handleRequest(req, res));
  server.listen(port, () => {
    console.log(`\n✅ Dashboard ready: http://localhost:${port}`);
    console.log(`   Stats:    http://localhost:${port}/api/stats`);
    console.log(`   Health:   http://localhost:${port}/api/health`);
    console.log(`   Memories: http://localhost:${port}/api/memories\n`);
  });
  return server;
}

if (isMain) {
  startDashboard(AUTO_PORT);
}
