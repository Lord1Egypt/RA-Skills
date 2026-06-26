/**
 * unified-memory v3.0 — Premium Web UI + API Server
 */

import http from 'http';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync, readFileSync } from 'fs';
import { homedir } from 'os';
import { getMemory, addMemory, deleteMemory } from '../storage.js';
import { getGraphStats } from '../graph/graph_store.js';

const HOME = homedir();
const MEMORY_FILE = join(HOME, '.openclaw', 'workspace', 'memory', 'memories.json');
const PORT = parseInt(process.argv.find(a => a.startsWith('--port='))?.split('=')[1]) || 3850;

function getAllMemories() {
  try {
    if (!existsSync(MEMORY_FILE)) return [];
    const data = JSON.parse(readFileSync(MEMORY_FILE, 'utf-8'));
    return Array.isArray(data) ? data : (data.memories || []);
  } catch { return []; }
}

function getStats() {
  const memories = getAllMemories();
  const byCategory = {}, byImportance = { high: 0, medium: 0, low: 0 };
  let totalImportance = 0;
  const now = Date.now(), dayMs = 86400000;
  const recent = { today: 0, week: 0, month: 0 };
  const importanceDist = [];
  for (let i = 0; i <= 10; i++) importanceDist.push(0);
  for (const mem of memories) {
    const cat = mem.category || 'general';
    byCategory[cat] = (byCategory[cat] || 0) + 1;
    const imp = mem.importance || 0.5;
    totalImportance += imp;
    if (imp >= 0.7) byImportance.high++;
    else if (imp >= 0.4) byImportance.medium++;
    else byImportance.low++;
    importanceDist[Math.floor(imp * 10)]++;
    const daysAgo = (now - new Date(mem.created_at || mem.createdTime || 0).getTime()) / dayMs;
    if (daysAgo < 1) recent.today++;
    if (daysAgo < 7) recent.week++;
    if (daysAgo < 30) recent.month++;
  }
  const timeline = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(now - i * dayMs);
    const label = (d.getMonth() + 1) + '月' + d.getDate() + '日';
    const count = memories.filter(m => {
      const t = new Date(m.created_at || m.createdTime || 0).getTime();
      const start = new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
      return t >= start && t < start + dayMs;
    }).length;
    timeline.push({ label, count });
  }
  let graphStats = { entities: 0, relations: 0 };
  try { if (getGraphStats) graphStats = getGraphStats(); } catch {}
  return {
    total: memories.length,
    avgImportance: memories.length ? totalImportance / memories.length : 0,
    byCategory,
    byImportance,
    recent,
    importanceDist,
    timeline,
    graphStats,
    memories
  };
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function catColor(cat) {
  const m = { fact: '#3b82f6', preference: '#10b981', decision: '#f59e0b', entity: '#8b5cf6', reflection: '#ec4899', general: '#64748b', conversation: '#06b6d4' };
  return m[cat] || '#64748b';
}

function catLabel(cat) {
  const m = { fact: '事实', preference: '偏好', decision: '决策', entity: '实体', reflection: '反思', general: '一般', conversation: '对话', test: '测试' };
  return m[cat] || cat;
}

function fmtDate(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  const now = new Date();
  const diff = now - d;
  if (diff < 86400000 && d.getDate() === now.getDate()) return '今天';
  if (diff < 172800000) return '昨天';
  if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';
  return (d.getMonth() + 1) + '月' + d.getDate() + '日';
}

function renderDashboard() {
  const stats = getStats();
  const s = stats;
  
  // Build timeline data
  const tLabels = s.timeline.map(t => '"' + t.label + '"').join(',');
  const tData = s.timeline.map(t => t.count).join(',');
  
  // Importance distribution
  const iData = s.importanceDist.join(',');
  
  // Category data
  const catEntries = Object.entries(s.byCategory).sort((a, b) => b[1] - a[1]);
  const cData = JSON.stringify(catEntries.map(([name, value]) => ({
    name: catLabel(name),
    value,
    color: catColor(name)
  })));
  
  // Donut legend HTML - fixed, no template placeholders
  let donutLegend = '';
  for (const [cat, count] of catEntries) {
    donutLegend += '<div class="donut-legend-item"><div class="legend-dot" style="background:' + catColor(cat) + '"></div><span class="legend-name">' + catLabel(cat) + '</span><span class="legend-count">' + count + '</span></div>';
  }
  
  // Recent memories
  const recent = s.memories.slice(0, 10);
  let recentHTML = '';
  for (const m of recent) {
    const imp = m.importance || 0.5;
    const impClass = imp >= 0.7 ? 'high' : 'medium';
    recentHTML += '<div class="memory-item" data-id="' + (m.id || '') + '" onclick="showModal(\'' + (m.id || '') + '\')"><div class="content"><div class="text">' + esc(m.text || m.content || '') + '</div><div class="meta"><span class="cat" style="background:' + catColor(m.category) + '">' + catLabel(m.category) + '</span><span class="date">' + fmtDate(m.created_at || m.createdTime) + '</span></div></div><span class="importance ' + impClass + '">' + (imp * 100).toFixed(0) + '%</span></div>';
  }
  if (!recentHTML) recentHTML = '<div class="empty-state"><div class="icon">📭</div><p>暂无记忆</p></div>';
  
  // Top importance memories
  const top = s.memories.filter(m => (m.importance || 0.5) >= 0.8).slice(0, 5);
  let topHTML = '';
  for (const m of top) {
    const imp = m.importance || 0.5;
    topHTML += '<div class="memory-item" data-id="' + (m.id || '') + '" onclick="showModal(\'' + (m.id || '') + '\')"><div class="content"><div class="text">' + esc(m.text || m.content || '') + '</div><div class="meta"><span class="cat" style="background:' + catColor(m.category) + '">' + catLabel(m.category) + '</span><span class="date">' + fmtDate(m.created_at || m.createdTime) + '</span></div></div><span class="importance high">' + (imp * 100).toFixed(0) + '%</span></div>';
  }
  if (!topHTML) topHTML = '<div class="empty-state"><div class="icon">📭</div><p>暂无高重要度记忆</p></div>';
  
  // Memories JSON for modal
  const memoriesJSON = JSON.stringify(s.memories.map(m => ({
    id: m.id || '',
    text: m.text || m.content || '',
    category: m.category || 'general',
    importance: m.importance || 0.5,
    created_at: m.created_at || m.createdTime || 0,
    scope: m.scope || '',
    tags: m.tags || []
  })));
  
  return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 记忆系统 v3.0</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script><style>' + DASHBOARD_CSS + '</style></head><body><header><div class="header-inner"><div class="logo"><div class="logo-icon">🧠</div><h1>记忆系统</h1><span class="badge">v3.0</span></div><div class="header-actions"><button class="icon-btn" onclick="toggleTheme()" title="切换主题">🌓</button></div></div></header><div class="container"><nav class="nav"><a href="/" class="active">📊 概览</a><a href="/memories">📝 记忆列表</a><a href="/search">🔍 搜索</a></nav><div class="stats-grid"><div class="stat-card"><div class="icon blue">💾</div><h3>记忆总数</h3><div class="value">' + s.total + '<small>条</small></div><div class="sub">分布在 ' + Object.keys(s.byCategory).length + ' 个分类</div></div><div class="stat-card"><div class="icon green">📈</div><h3>本周新增</h3><div class="value">' + s.recent.week + '</div><div class="sub">今日 ' + s.recent.today + ' | 本月 ' + s.recent.month + '</div></div><div class="stat-card"><div class="icon purple">⭐</div><h3>平均重要度</h3><div class="value">' + (s.avgImportance * 100).toFixed(0) + '%</div><div class="sub">高重要度 ' + s.byImportance.high + ' 条</div></div><div class="stat-card"><div class="icon orange">🔗</div><h3>知识图谱</h3><div class="value">' + (s.graphStats?.entities || 0) + '<small>实体</small></div><div class="sub">' + (s.graphStats?.relations || 0) + ' 个关系</div></div></div><div class="charts-grid"><div class="chart-card"><h2>📈 记忆趋势（7天）</h2><div class="chart-container"><canvas id="timelineChart"></canvas></div></div><div class="chart-card"><h2>⭐ 重要度分布</h2><div class="chart-container"><canvas id="importanceChart"></canvas></div></div></div><div class="chart-card" style="margin-bottom:24px"><h2>🏷️ 分类分布</h2><div class="donut-container"><div class="donut-chart"><canvas id="categoryChart"></canvas><div class="donut-center"><div class="num">' + s.total + '</div></div></div><div class="donut-legend">' + donutLegend + '</div></div></div><div class="memory-section"><div class="section-header"><h2>🕐 最近记忆</h2><a href="/memories" class="view-all">查看全部 →</a></div><div class="memory-list">' + recentHTML + '</div></div><div class="memory-section"><div class="section-header"><h2>🔥 高重要度记忆</h2></div><div class="memory-list">' + topHTML + '</div></div></div><footer class="footer"><p>🧠 Unified Memory v3.0</p></footer><div class="modal" id="memoryModal"><div class="modal-content"><div class="modal-header"><h2>📝 记忆详情</h2><button class="modal-close" onclick="closeModal()">×</button></div><div id="modalBody"></div></div></div><script>var memories=' + memoriesJSON + ';Chart.defaults.color="#9ca3af";Chart.defaults.borderColor="rgba(255,255,255,0.1)";new Chart(document.getElementById("timelineChart"),{type:"line",data:{labels:[' + tLabels + '],datasets:[{data:[' + tData + '],borderColor:"#6366f1",backgroundColor:"rgba(99,102,241,0.1)",fill:true,tension:0.4,pointRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:"rgba(255,255,255,0.05)"}},x:{grid:{display:false}}}}});new Chart(document.getElementById("importanceChart"),{type:"bar",data:{labels:["0-0.1","0.1-0.2","0.2-0.3","0.3-0.4","0.4-0.5","0.5-0.6","0.6-0.7","0.7-0.8","0.8-0.9","0.9-1.0"],datasets:[{data:[' + iData + '],backgroundColor:["rgba(107,114,128,0.6)","rgba(107,114,128,0.6)","rgba(107,114,128,0.6)","rgba(107,114,128,0.6)","rgba(245,158,11,0.6)","rgba(245,158,11,0.6)","rgba(245,158,11,0.6)","rgba(239,68,68,0.6)","rgba(239,68,68,0.6)","rgba(239,68,68,0.6)"],borderRadius:6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:"rgba(255,255,255,0.05)"}},x:{grid:{display:false}}}}});new Chart(document.getElementById("categoryChart"),{type:"doughnut",data:{labels:' + cData.replace(/"name"|"value"|"color"/g, '').replace(/\{/g, '[').replace(/\}/g, ']') + '.map(d=>d.name),datasets:[{data:' + cData + '.map(d=>d.value),backgroundColor:' + cData + '.map(d=>d.color),borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,cutout:"70%",plugins:{legend:{display:false}}}});function toggleTheme(){document.body.classList.toggle("light");localStorage.setItem("theme",document.body.classList.contains("light")?"light":"dark");}if(localStorage.getItem("theme")==="light")document.body.classList.add("light");function showModal(id){var m=memories.find(function(x){return x.id===id;});if(!m)return;var body=document.getElementById("modalBody");var html=\'<div class="detail-row"><span class="detail-label">内容</span><span class="detail-value">\'+esc(m.text||m.content||"")+"</span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>分类</span><span class=\\'detail-value\\'><span class=\\'cat\\' style=\\'background:"+catColor(m.category)+"\\'>"+catLabel(m.category)+"</span></span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>重要度</span><span class=\\'detail-value\\'>"+((m.importance||0.5)*100).toFixed(0)+"%</span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>创建时间</span><span class=\\'detail-value\\'>"+new Date(m.created_at||m.createdTime||0).toLocaleString("zh-CN")+"</span></div>";if(m.scope)html+=\'<div class="detail-row"><span class="detail-label">范围</span><span class="detail-value">\'+m.scope+"</span></div>";if(m.tags&&m.tags.length)html+=\'<div class="detail-row"><span class="detail-label">标签</span><span class="detail-value">\'+m.tags.join(", ")+"</span></div>";body.innerHTML=html;document.getElementById("memoryModal").classList.add("show");}function closeModal(){document.getElementById("memoryModal").classList.remove("show");}document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal();});function esc(s){if(!s)return"";return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}function catColor(c){var m={fact:"#3b82f6",preference:"#10b981",decision:"#f59e0b",entity:"#8b5cf6",reflection:"#ec4899",general:"#64748b",conversation:"#06b6d4"};return m[c]||"#64748b";}function catLabel(c){var m={fact:"事实",preference:"偏好",decision:"决策",entity:"实体",reflection:"反思",general:"一般",conversation:"对话",test:"测试"};return m[c]||c;}</script></body></html>';
}

const DASHBOARD_CSS = `*{box-sizing:border-box;margin:0;padding:0}:root{--bg:#0a0f1c;--bg2:#111827;--bg3:#1f2937;--text:#f9fafb;--text2:#9ca3af;--text3:#6b7280;--accent:#6366f1;--accent2:#818cf8;--gradient:linear-gradient(135deg,#667eea 0%,#764ba2 100%)}.light{--bg:#f8fafc;--bg2:#f1f5f9;--bg3:#e2e8f0;--text:#0f172a;--text2:#475569;--text3:#94a3b8}body{font-family:Inter,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}.container{max-width:1400px;margin:0 auto;padding:24px}.header{background:rgba(17,24,39,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.1);padding:16px 24px;position:sticky;top:0;z-index:100}.light .header{background:rgba(255,255,255,0.9)}.header-inner{display:flex;align-items:center;justify-content:space-between}.logo{display:flex;align-items:center;gap:12px}.logo-icon{width:40px;height:40px;background:var(--gradient);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px}.logo h1{font-size:1.25rem;font-weight:700;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.badge{background:rgba(99,102,241,0.2);color:var(--accent2);padding:4px 12px;border-radius:20px;font-size:0.75rem}.icon-btn{width:40px;height:40px;background:var(--bg3);border:none;border-radius:10px;color:var(--text2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:all 0.2s}.icon-btn:hover{transform:translateY(-2px)}.nav{display:flex;gap:8px;padding:16px 0;flex-wrap:wrap}.nav a{padding:10px 20px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);color:var(--text2);text-decoration:none;border-radius:10px;font-size:0.875rem;font-weight:500;transition:all 0.3s}.light .nav a{background:rgba(0,0,0,0.03);border-color:rgba(0,0,0,0.1)}.nav a:hover{background:rgba(255,255,255,0.08)}.light .nav a:hover{background:rgba(0,0,0,0.08)}.nav a.active{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 4px 15px rgba(99,102,241,0.4)}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-bottom:24px}.stat-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:24px;transition:all 0.3s}.light .stat-card{background:rgba(255,255,255,0.8);border-color:rgba(0,0,0,0.1)}.stat-card:hover{transform:translateY(-4px);box-shadow:0 10px 15px rgba(0,0,0,0.3)}.stat-card .icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:16px}.stat-card .icon.blue{background:rgba(59,130,246,0.2);color:#60a5fa}.stat-card .icon.green{background:rgba(16,185,129,0.2);color:#34d399}.stat-card .icon.purple{background:rgba(139,92,246,0.2);color:#a78bfa}.stat-card .icon.orange{background:rgba(245,158,11,0.2);color:#fbbf24}.stat-card h3{font-size:0.75rem;color:var(--text3);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px}.stat-card .value{font-size:2rem;font-weight:700}.stat-card .sub{font-size:0.8rem;color:var(--text3);margin-top:8px}.charts-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:24px;margin-bottom:24px}.chart-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:24px}.light .chart-card{background:rgba(255,255,255,0.8);border-color:rgba(0,0,0,0.1)}.chart-card h2{font-size:1rem;font-weight:600;margin-bottom:20px}.chart-container{position:relative;height:250px}.donut-container{display:flex;align-items:center;gap:32px;flex-wrap:wrap}.donut-chart{position:relative;width:180px;height:180px}.donut-center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}.donut-center .num{font-size:1.75rem;font-weight:700}.donut-legend{flex:1;min-width:150px}.donut-legend-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)}.light .donut-legend-item{border-color:rgba(0,0,0,0.05)}.legend-dot{width:10px;height:10px;border-radius:50%}.legend-name{flex:1;font-size:0.875rem}.legend-count{font-weight:600;color:var(--text2)}.memory-section{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:24px;margin-bottom:24px}.light .memory-section{background:rgba(255,255,255,0.8);border-color:rgba(0,0,0,0.1)}.section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}.section-header h2{font-size:1rem;font-weight:600}.view-all{color:var(--accent2);text-decoration:none;font-size:0.875rem}.memory-list{display:flex;flex-direction:column;gap:12px}.memory-item{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px;display:flex;gap:16px;align-items:flex-start;transition:all 0.2s;cursor:pointer}.light .memory-item{background:rgba(255,255,255,0.5);border-color:rgba(0,0,0,0.06)}.memory-item:hover{background:rgba(255,255,255,0.05);transform:translateX(4px)}.light .memory-item:hover{background:rgba(255,255,255,0.9)}.memory-item .content{flex:1;min-width:0}.memory-item .text{font-size:0.9rem;line-height:1.5;margin-bottom:8px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.memory-item .meta{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.memory-item .cat{padding:3px 10px;border-radius:6px;font-size:0.7rem;font-weight:500;color:#fff}.memory-item .date{font-size:0.75rem;color:var(--text3)}.memory-item .importance{font-size:0.875rem;font-weight:600;padding:4px 12px;border-radius:8px}.memory-item .importance.high{background:rgba(239,68,68,0.2);color:#f87171}.memory-item .importance.medium{background:rgba(245,158,11,0.2);color:#fbbf24}.empty-state{text-align:center;padding:60px;color:var(--text3)}.empty-state .icon{font-size:3rem;margin-bottom:16px;opacity:0.5}.footer{text-align:center;padding:32px;color:var(--text3);font-size:0.8rem}.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:1000;align-items:center;justify-content:center;padding:20px}.modal.show{display:flex}.modal-content{background:var(--bg2);border-radius:16px;max-width:600px;width:100%;max-height:80vh;overflow-y:auto;padding:24px;position:relative}.light .modal-content{background:#fff}.modal-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}.modal-header h2{font-size:1.1rem;font-weight:600}.modal-close{width:32px;height:32px;border-radius:8px;background:var(--bg3);border:none;color:var(--text2);cursor:pointer;font-size:1.2rem;display:flex;align-items:center;justify-content:center}.modal-close:hover{background:var(--accent)}.detail-row{display:flex;gap:12px;margin-bottom:12px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)}.light .detail-row{border-color:rgba(0,0,0,0.05)}.detail-label{font-weight:500;color:var(--text2);min-width:80px}.detail-value{flex:1;color:var(--text)}@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}.stat-card{animation:fadeIn 0.5s ease-out}@media(max-width:640px){.stats-grid{grid-template-columns:repeat(2,1fr)}.chart-container{height:200px}.donut-container{flex-direction:column}.header-inner{flex-wrap:wrap;gap:12px}}`;

function renderMemories() {
  const stats = getStats();
  const s = stats;
  let html = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>📝 记忆列表</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>' + DASHBOARD_CSS + '</style></head><body><header><div class="header-inner"><div class="logo"><div class="logo-icon">📝</div><h1>记忆列表</h1></div><div class="header-actions"><button class="icon-btn" onclick="toggleTheme()">🌓</button></div></div></header><div class="container"><nav class="nav"><a href="/">📊 概览</a><a href="/" class="active">📝 记忆列表</a><a href="/search">🔍 搜索</a></nav>';
  
  html += '<div class="stats-grid"><div class="stat-card"><div class="icon blue">💾</div><h3>记忆总数</h3><div class="value">' + s.total + '</div></div></div>';
  
  html += '<div class="memory-section"><div class="section-header"><h2>全部记忆（' + s.total + '条）</h2></div><div class="memory-list">';
  
  for (const m of s.memories) {
    const imp = m.importance || 0.5;
    const impClass = imp >= 0.7 ? 'high' : 'medium';
    html += '<div class="memory-item" data-id="' + (m.id || '') + '" onclick="showModal(\'' + (m.id || '') + '\')"><div class="content"><div class="text">' + esc(m.text || m.content || '') + '</div><div class="meta"><span class="cat" style="background:' + catColor(m.category) + '">' + catLabel(m.category) + '</span><span class="date">' + fmtDate(m.created_at || m.createdTime) + '</span></div></div><span class="importance ' + impClass + '">' + (imp * 100).toFixed(0) + '%</span></div>';
  }
  
  html += '</div></div></div><footer class="footer"><p>🧠 Unified Memory v3.0</p></footer>';
  html += '<div class="modal" id="memoryModal"><div class="modal-content"><div class="modal-header"><h2>📝 记忆详情</h2><button class="modal-close" onclick="closeModal()">×</button></div><div id="modalBody"></div></div></div>';
  
  const memoriesJSON = JSON.stringify(s.memories.map(m => ({
    id: m.id || '',
    text: m.text || m.content || '',
    category: m.category || 'general',
    importance: m.importance || 0.5,
    created_at: m.created_at || m.createdTime || 0,
    scope: m.scope || '',
    tags: m.tags || []
  })));
  
  html += '<script>var memories=' + memoriesJSON + ';function toggleTheme(){document.body.classList.toggle("light");localStorage.setItem("theme",document.body.classList.contains("light")?"light":"dark");}if(localStorage.getItem("theme")==="light")document.body.classList.add("light");function showModal(id){var m=memories.find(function(x){return x.id===id;});if(!m)return;var body=document.getElementById("modalBody");var html=\'<div class="detail-row"><span class="detail-label">内容</span><span class="detail-value">\'+esc(m.text||m.content||"")+"</span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>分类</span><span class=\\'detail-value\\'><span class=\\'cat\\' style=\\'background:"+catColor(m.category)+"\\'>"+catLabel(m.category)+"</span></span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>重要度</span><span class=\\'detail-value\\'>"+((m.importance||0.5)*100).toFixed(0)+"%</span></div><div class=\\'detail-row\\'><span class=\\'detail-label\\'>创建时间</span><span class=\\'detail-value\\'>"+new Date(m.created_at||m.createdTime||0).toLocaleString("zh-CN")+"</span></div>";if(m.scope)html+=\'<div class="detail-row"><span class="detail-label">范围</span><span class="detail-value">\'+m.scope+"</span></div>";if(m.tags&&m.tags.length)html+=\'<div class="detail-row"><span class="detail-label">标签</span><span class="detail-value">\'+m.tags.join(", ")+"</span></div>";body.innerHTML=html;document.getElementById("memoryModal").classList.add("show");}function closeModal(){document.getElementById("memoryModal").classList.remove("show");}document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal();});function esc(s){if(!s)return"";return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}function catColor(c){var m={fact:"#3b82f6",preference:"#10b981",decision:"#f59e0b",entity:"#8b5cf6",reflection:"#ec4899",general:"#64748b",conversation:"#06b6d4"};return m[c]||"#64748b";}function catLabel(c){var m={fact:"事实",preference:"偏好",decision:"决策",entity:"实体",reflection:"反思",general:"一般",conversation:"对话",test:"测试"};return m[c]||c;}</script></body></html>';
  
  return html;
}

function renderSearch() {
  return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=function renderSearch() {
  const params = new URLSearchParams(url.split('?')[1] || '');
  const q = params.get('q') || '';
  const stats = getStats();
  const s = stats;
  
  let results = s.memories;
  if (q) {
    const qq = q.toLowerCase();
    results = results.filter(m => 
      (m.text || m.content || '').toLowerCase().includes(qq) ||
      (m.category || '').toLowerCase().includes(qq)
    );
  }
  
  let html = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🔍 搜索</title><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>' + DASHBOARD_CSS + '.search-box{margin-bottom:24px}.search-box input{width:100%;padding:12px 16px;background:var(--bg2);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:var(--text);font-size:1rem}.search-box input:focus{outline:none;border-color:var(--accent)}.search-info{margin-bottom:16px;color:var(--text2)}</style></head><body><header><div class="header-inner"><div class="logo"><div class="logo-icon">🔍</div><h1>搜索记忆</h1></div><div class="header-actions"><button class="icon-btn" onclick="toggleTheme()">🌓</button></div></div></header><div class="container"><nav class="nav"><a href="/">📊 概览</a><a href="/memories">📝 记忆列表</a><a href="/search" class="active">🔍 搜索</a></nav><div class="search-box"><input type="text" id="searchInput" placeholder="搜索记忆..." value="' + esc(q) + '" oninput="doSearch()"></div><div class="search-info">找到 ' + results.length + ' 条记忆</div><div class="memory-section"><div class="memory-list">';
  
  for (const m of results.slice(0, 50)) {
    const imp = m.importance || 0.5;
    const impClass = imp >= 0.7 ? 'high' : 'medium';
    html += '<div class="memory-item" data-id="' + (m.id || '') + '" onclick="showModal(\'' + (m.id || '') + '\')"><div class="content"><div class="text">' + esc(m.text || m.content || '') + '</div><div class="meta"><span class="cat" style="background:' + catColor(m.category) + '">' + catLabel(m.category) + '</span><span class="date">' + fmtDate(m.created_at || m.createdTime) + '</span></div></div><span class="importance ' + impClass + '">' + (imp * 100).toFixed(0) + '%</span></div>';
  }
  
  if (!results.length) {
    html += '<div class="empty-state"><div class="icon">🔍</div><p>没有找到相关记忆</p></div>';
  }
  
  html += '</div></div></div><footer class="footer"><p>🧠 Unified Memory v3.0</p></footer>';
  html += '<div class="modal" id="memoryModal"><div class="modal-content"><div class="modal-header"><h2>📝 记忆详情</h2><button class="modal-close" onclick="closeModal()">×</button></div><div id="modalBody"></div></div></div>';
  
  const memoriesJSON = JSON.stringify(s.memories.map(m => ({
    id: m.id || '',
    text: m.text || m.content || '',
    category: m.category || 'general',
    importance: m.importance || 0.5,
    created_at: m.created_at || m.createdTime || 0,
    scope: m.scope || '',
    tags: m.tags || []
  })));
  
  html += '<script>var memories=' + memoriesJSON + ',currentQuery="' + esc(q) + '";function toggleTheme(){document.body.classList.toggle("light");localStorage.setItem("theme",document.body.classList.contains("light")?"light":"dark");}if(localStorage.getItem("theme")==="light")document.body.classList.add("light");function doSearch(){var q=document.getElementById("searchInput").value;window.location.href="/search?q="+encodeURIComponent(q);}function showModal(id){var m=memories.find(function(x){return x.id===id;});if(!m)return;var body=document.getElementById("modalBody");var h=' + "'" + '<div class="detail-row"><span class="detail-label">内容</span><span class="detail-value">' + "'" + '+esc(m.text||m.content||"")+"</span></div><div class=\'detail-row\'><span class=\'detail-label\'>分类</span><span class=\'detail-value\'><span class=\'cat\' style=\'background:"+catColor(m.category)+"\'>"+catLabel(m.category)+"</span></span></div><div class=\'detail-row\'><span class=\'detail-label\'>重要度</span><span class=\'detail-value\'>"+((m.importance||0.5)*100).toFixed(0)+"%</span></div><div class=\'detail-row\'><span class=\'detail-label\'>创建时间</span><span class=\'detail-value\'>"+new Date(m.created_at||m.createdTime||0).toLocaleString("zh-CN")+"</span></div>";if(m.scope)h+=' + "'" + '<div class="detail-row"><span class="detail-label">范围</span><span class="detail-value">'+m.scope+"</span></div>";if(m.tags&&m.tags.length)h+=' + "'" + '<div class="detail-row"><span class="detail-label">标签</span><span class="detail-value">'+m.tags.join(", ")+"</span></div>";body.innerHTML=h;document.getElementById("memoryModal").classList.add("show");}function closeModal(){document.getElementById("memoryModal").classList.remove("show");}document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal();});function esc(s){if(!s)return"";return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}function catColor(c){var m={fact:"#3b82f6",preference:"#10b981",decision:"#f59e0b",entity:"#8b5cf6",reflection:"#ec4899",general:"#64748b",conversation:"#06b6d4"};return m[c]||"#64748b";}function catLabel(c){var m={fact:"事实",preference:"偏好",decision:"决策",entity:"实体",reflection:"反思",general:"一般",conversation:"对话",test:"测试"};return m[c]||c;}</script></body></html>';
  
  return html;
}

const SERVER_HTML = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 记忆系统</title><style>body{font-family:system-ui;background:#0a0f1c;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}.card{text-align:center;padding:40px}.card h1{font-size:2rem;margin-bottom:8px}.card p{color:#9ca3af;margin-bottom:24px}.card a{display:inline-block;padding:12px 24px;background:#6366f1;color:#fff;text-decoration:none;border-radius:8px;font-weight:500}.card a:hover{background:#4f46e5}</style></head><body><div class="card"><h1>🧠 Unified Memory</h1><p>v3.0 运行中</p><a href="/">打开 Dashboard</a></div></body></html>';

const server = http.createServer(async (req, res) => {
  const url = req.url.split('?')[0];
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  try {
    if (url === '/api/stats') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getStats()));
      return;
    }
    
    if (url === '/api/memories') {
      if (req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(getAllMemories()));
      } else if (req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', async () => {
          try {
            const data = JSON.parse(body);
            const result = await addMemory(data.text, data);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ ok: true, id: result }));
          } catch (e) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: e.message }));
          }
        });
      } else {
        res.writeHead(405);
        res.end();
      }
      return;
    }
    
    if (url.startsWith('/api/memory/')) {
      const id = url.split('/')[3];
      if (req.method === 'GET') {
        const mem = getMemory(id);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(mem || { error: 'Not found' }));
      } else if (req.method === 'DELETE') {
        await deleteMemory(id);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } else {
        res.writeHead(405);
        res.end();
      }
      return;
    }
    
    if (url.startsWith('/api/search')) {
      const q = new URL(req.url, 'http://localhost').searchParams.get('q') || '';
      const memories = getAllMemories();
      const results = q ? memories.filter(m => 
        (m.text || m.content || '').toLowerCase().includes(q.toLowerCase())
      ) : memories;
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(results));
      return;
    }
    
    if (url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      const stats = getStats();
      res.end(JSON.stringify({ status: 'ok', version: '3.0.0', memories: stats.total }));
      return;
    }
    
    if (url === '/' || url === '/index.html') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(renderDashboard());
    } else if (url === '/memories') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(renderMemories());
    } else if (url.startsWith('/search')) {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(renderSearch());
    } else {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(SERVER_HTML);
    }
  } catch (e) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Error: ' + e.message);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log('🧠 Unified Memory v3.0 Server');
  console.log('   Dashboard: http://localhost:' + PORT + '/');
  console.log('   Memories: http://localhost:' + PORT + '/memories');
  console.log('   Search: http://localhost:' + PORT + '/search');
});
