/**
 * Skills Monitor PWA — 前端应用
 * 单页应用，暗色主题，通过 Agent ID + Token 登录
 */

const API_BASE = '/api/pwa';
let currentUser = null;
let currentPage = 'login';
let trendChart = null;

// ──────── 工具函数 ────────

function getToken() {
  return localStorage.getItem('sm_pwa_token') || '';
}

function setToken(token) {
  localStorage.setItem('sm_pwa_token', token);
}

function clearToken() {
  localStorage.removeItem('sm_pwa_token');
}

async function api(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['X-PWA-Token'] = token;

  const res = await fetch(API_BASE + path, { ...options, headers });
  const data = await res.json();

  if (res.status === 401) {
    clearToken();
    showPage('login');
    return null;
  }

  return data;
}

function showToast(msg, duration = 2000) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), duration);
}

function copyToClipboard(text, btnEl) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showToast('✅ 已复制到剪贴板');
      if (btnEl) {
        const orig = btnEl.innerHTML;
        btnEl.innerHTML = '<span class="rec-btn-icon">✅</span> 已复制';
        btnEl.classList.add('copied');
        setTimeout(() => { btnEl.innerHTML = orig; btnEl.classList.remove('copied'); }, 1500);
      }
    }).catch(() => fallbackCopy(text, btnEl));
  } else {
    fallbackCopy(text, btnEl);
  }
}

function fallbackCopy(text, btnEl) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px';
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    showToast('✅ 已复制到剪贴板');
    if (btnEl) {
      const orig = btnEl.innerHTML;
      btnEl.innerHTML = '<span class="rec-btn-icon">✅</span> 已复制';
      btnEl.classList.add('copied');
      setTimeout(() => { btnEl.innerHTML = orig; btnEl.classList.remove('copied'); }, 1500);
    }
  } catch (e) {
    showToast('❌ 复制失败，请手动复制');
  }
  document.body.removeChild(ta);
}

function $(id) { return document.getElementById(id); }

function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function toggleDiagnosticReport() {
  const wrap = document.getElementById('sec-diagnostic-report');
  const icon = document.getElementById('diag-toggle-icon');
  if (!wrap) return;
  const isHidden = wrap.style.display === 'none';
  wrap.style.display = isHidden ? 'block' : 'none';
  if (icon) icon.textContent = isHidden ? '▼' : '▶';
  if (isHidden) {
    setTimeout(() => {
      wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
  }
}

function toggleOverviewPanel() {
  const body = document.getElementById('ov-panel-body');
  const icon = document.getElementById('ov-toggle-icon');
  if (!body) return;
  const isHidden = body.style.display === 'none';
  body.style.display = isHidden ? 'block' : 'none';
  if (icon) icon.textContent = isHidden ? '▼' : '▶';
}

function toggleDetailDataPanel() {
  const body = document.getElementById('detail-data-body');
  const icon = document.getElementById('detail-data-toggle-icon');
  if (!body) return;
  const isHidden = body.style.display === 'none';
  body.style.display = isHidden ? 'block' : 'none';
  if (icon) icon.textContent = isHidden ? '▼' : '▶';
}

function getHealthClass(score) {
  if (score >= 80) return 'health-good';
  if (score >= 60) return 'health-warn';
  return 'health-bad';
}

function getHealthColor(score) {
  if (score >= 80) return '#27ae60';
  if (score >= 60) return '#f39c12';
  return '#e74c3c';
}

function escapeHtml(str = '') {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderInlineMarkdown(text = '') {
  return escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

function renderMarkdownTable(lines) {
  if (!lines.length) return '';
  const rows = lines.map(line => line.split('|').slice(1, -1).map(cell => renderInlineMarkdown(cell.trim())));
  const header = rows[0] || [];
  const body = rows.slice(2);
  return `
    <div class="markdown-table-wrap">
      <table class="markdown-table">
        <thead><tr>${header.map(cell => `<th>${cell}</th>`).join('')}</tr></thead>
        <tbody>
          ${body.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('')}
        </tbody>
      </table>
    </div>`;
}

function renderMarkdown(markdown = '') {
  if (!markdown) return '';
  const lines = markdown.split('\n');
  let html = '';
  let i = 0;
  let inList = false;

  const closeList = () => {
    if (inList) {
      html += '</ul>';
      inList = false;
    }
  };

  while (i < lines.length) {
    const raw = lines[i] || '';
    const line = raw.trim();

    if (!line) {
      closeList();
      i += 1;
      continue;
    }

    if (/^\|/.test(line)) {
      closeList();
      const tableLines = [];
      while (i < lines.length && /^\|/.test((lines[i] || '').trim())) {
        tableLines.push((lines[i] || '').trim());
        i += 1;
      }
      html += renderMarkdownTable(tableLines);
      continue;
    }

    if (/^---+$/.test(line)) {
      closeList();
      html += '<hr class="markdown-divider">';
      i += 1;
      continue;
    }

    if (/^###\s+/.test(line)) {
      closeList();
      html += `<h4>${renderInlineMarkdown(line.replace(/^###\s+/, ''))}</h4>`;
      i += 1;
      continue;
    }

    if (/^##\s+/.test(line)) {
      closeList();
      html += `<h3>${renderInlineMarkdown(line.replace(/^##\s+/, ''))}</h3>`;
      i += 1;
      continue;
    }

    if (/^#\s+/.test(line)) {
      closeList();
      html += `<h2>${renderInlineMarkdown(line.replace(/^#\s+/, ''))}</h2>`;
      i += 1;
      continue;
    }

    if (/^>\s+/.test(line)) {
      closeList();
      const quoteLines = [];
      while (i < lines.length && /^>\s+/.test((lines[i] || '').trim())) {
        quoteLines.push(renderInlineMarkdown((lines[i] || '').trim().replace(/^>\s+/, '')));
        i += 1;
      }
      html += `<blockquote>${quoteLines.join('<br>')}</blockquote>`;
      continue;
    }

    if (/^-\s+/.test(line)) {
      if (!inList) {
        html += '<ul class="markdown-list">';
        inList = true;
      }
      html += `<li>${renderInlineMarkdown(line.replace(/^-\s+/, ''))}</li>`;
      i += 1;
      continue;
    }

    closeList();
    html += `<p>${renderInlineMarkdown(line)}</p>`;
    i += 1;
  }

  closeList();
  return `<div class="markdown-body">${html}</div>`;
}

function getReportTypeLabel(type) {
  if (type === 'diagnostic') return '🏥 诊断报告';
  if (type === 'daily') return '📊 日报';
  return type || '报告';
}

function renderFactorChips(factors = {}) {
  const entries = Object.entries(factors || {});
  if (!entries.length) return '';
  return `<div class="factor-chip-list">${entries.map(([label, info]) => `
    <div class="factor-chip">
      <span class="factor-name">${escapeHtml(label)}</span>
      <span class="factor-score">${info?.score ?? '-'}分</span>
      <span class="factor-desc">${escapeHtml(info?.desc || '')}</span>
    </div>`).join('')}</div>`;
}

function renderRecommendations(recommendations = []) {
  if (!recommendations.length) return '';
  return `
    <div class="card report-section-card">
      <h2 class="card-title">✨ 推荐安装与替换建议</h2>
      <div class="recommend-list">
        ${recommendations.map((rec, index) => {
          const slug = rec.slug || '';
          const detailUrl = rec.detail_url || (slug ? `https://clawhub.ai/skills/${slug}` : '');
          const installCmd = rec.install_command || (slug ? `python install_skills.py ${slug}` : '');
          const installUrl = rec.install_url || (slug ? `https://clawhub.ai/api/v1/download?slug=${slug}` : '');
          return `
          <div class="recommend-card">
            <div class="recommend-top">
              <div>
                <div class="recommend-rank">TOP ${index + 1}</div>
                <div class="recommend-name">${escapeHtml(rec.name || slug || '未知 Skill')}</div>
              </div>
              <div class="recommend-score">${Math.round(rec.recommendation_score || 0)}</div>
            </div>
            <div class="recommend-meta">
              <span class="pill">${escapeHtml(rec.category || '未分类')}</span>
              <span class="pill accent">${escapeHtml(rec.reason_label || rec.reason_type || '推荐')}</span>
              ${rec.hub_rating ? `<span class="pill">⭐ ${rec.hub_rating}</span>` : ''}
              ${rec.hub_installs ? `<span class="pill">⬇ ${rec.hub_installs}</span>` : ''}
            </div>
            <div class="recommend-desc">${escapeHtml(rec.description || '')}</div>
            <div class="recommend-reason">${escapeHtml(rec.reason_detail || '')}</div>
            <div class="recommend-actions">
              ${installCmd ? `<button class="rec-action-btn rec-copy-btn" onclick="copyToClipboard('${escapeHtml(installCmd)}', this)" title="复制安装命令">
                <span class="rec-btn-icon">📋</span> 复制安装命令
              </button>` : ''}
              ${installUrl ? `<button class="rec-action-btn rec-url-btn" onclick="copyToClipboard('${escapeHtml(installUrl)}', this)" title="复制下载链接">
                <span class="rec-btn-icon">🔗</span> 复制下载链接
              </button>` : ''}
              ${detailUrl ? `<a class="rec-action-btn rec-detail-btn" href="${escapeHtml(detailUrl)}" target="_blank" rel="noopener noreferrer">
                <span class="rec-btn-icon">🌐</span> 查看 ClawHub 详情
              </a>` : ''}
            </div>
          </div>`;
        }).join('')}
      </div>
    </div>`;
}

function renderStringListCard(title, items = [], emptyText = '') {
  if (!items.length) return emptyText ? `<div class="card report-section-card"><h2 class="card-title">${title}</h2><div class="empty-inline">${emptyText}</div></div>` : '';
  return `
    <div class="card report-section-card">
      <h2 class="card-title">${title}</h2>
      <div class="bullet-card-list">
        ${items.map(item => `<div class="bullet-card-item">${escapeHtml(item)}</div>`).join('')}
      </div>
    </div>`;
}

function renderCoverage(coverage = []) {
  if (!coverage.length) return '';
  return `
    <div class="card report-section-card">
      <h2 class="card-title">🧩 能力覆盖</h2>
      <div class="coverage-list">
        ${coverage.map(item => `
          <div class="coverage-item">
            <div>
              <div class="coverage-name">${escapeHtml(item.category)}</div>
              <div class="coverage-meta">已安装 ${item.installed} · 可运行 ${item.runnable}</div>
            </div>
            <div class="coverage-right ${item.status === 'good' ? 'health-good' : 'health-warn'}">${Math.round(item.coverage_ratio || 0)}%</div>
          </div>`).join('')}
      </div>
    </div>`;
}

function renderUsageTop(usageTop = []) {
  if (!usageTop.length) return '';
  return `
    <div class="card report-section-card">
      <h2 class="card-title">📈 最近 7 天使用情况</h2>
      <div class="usage-list">
        ${usageTop.map((item, index) => `
          <div class="usage-item">
            <div class="usage-rank">${index + 1}</div>
            <div class="usage-main">
              <div class="usage-name">${escapeHtml(item.skill_id)}</div>
              <div class="usage-meta">${item.count} 次 · 成功 ${item.success_count} 次 · 成功率 ${item.success_rate}%</div>
            </div>
          </div>`).join('')}
      </div>
    </div>`;
}

function renderScoreList(scores = []) {
  if (!scores.length) {
    return `<div class="card report-section-card"><h2 class="card-title">🏆 技能评分</h2><div class="empty-inline">当前没有可展示的运行评分，通常是最近还没有产生有效运行记录。</div></div>`;
  }
  return `
    <div class="card report-section-card">
      <h2 class="card-title">🏆 技能评分与因子拆解</h2>
      <div class="score-detail-list">
        ${scores.map((s, i) => `
          <div class="score-detail-item">
            <div class="score-detail-top">
              <div class="score-left">
                <div class="skill-rank ${i < 3 ? 'top3' : ''}">${i + 1}</div>
                <div>
                  <div class="score-skill-name">${escapeHtml(s.skill_id || 'unknown')}</div>
                  <div class="score-skill-meta">${escapeHtml(s.grade_label || s.grade || '-')} · 运行 ${s.details?.total_runs || 0} 次</div>
                </div>
              </div>
              <div class="score-big">${Number(s.total_score || 0).toFixed(1)}</div>
            </div>
            ${renderFactorChips(s.factors || {})}
          </div>`).join('')}
      </div>
    </div>`;
}

// ──────── 页面切换 ────────

function showPage(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const el = $(page + '-page');
  if (el) el.classList.add('active');

  // Tab bar
  const tabBar = $('tab-bar');
  tabBar.classList.toggle('hidden', page === 'login' || page === 'report-detail' || page === 'skill-detail');

  // Tab active state
  document.querySelectorAll('.tab-item').forEach(t => {
    t.classList.toggle('active', t.dataset.page === page);
  });

  currentPage = page;

  // Load page data
  if (page === 'dashboard') loadDashboard();
  else if (page === 'reports') loadReports();
  else if (page === 'mine') loadMine();
}

// ──────── 登录 ────────

async function doLogin() {
  const agentId = $('login-agent-id').value.trim();
  const agentToken = $('login-agent-token').value.trim();

  if (!agentId || !agentToken) {
    showToast('请输入智能体 ID 和 Key');
    return;
  }

  const btn = $('login-btn');
  btn.disabled = true;
  btn.textContent = '登录中...';

  try {
    const data = await api('/login', {
      method: 'POST',
      body: JSON.stringify({ agent_id: agentId, agent_token: agentToken }),
    });

    if (data && data.ok) {
      setToken(data.token);
      currentUser = data.user;
      // 登录成功后清空输入框
      $('login-agent-id').value = '';
      $('login-agent-token').value = '';
      showToast('登录成功');
      showPage('dashboard');
    } else {
      showToast(data?.error || '登录失败');
    }
  } catch (e) {
    showToast('网络错误，请重试');
  }

  btn.disabled = false;
  btn.textContent = '登 录';
}

// ──────── 仪表盘 ────────

async function loadDashboard() {
  const container = $('dashboard-content');
  container.innerHTML = '<div class="loading"><div class="spinner"></div>加载中...</div>';

  const data = await api('/dashboard');
  if (!data || !data.ok) {
    container.innerHTML = '<div class="empty-state"><div class="icon">📭</div><h3>暂无数据</h3><p>Agent 尚未上报任何数据</p></div>';
    return;
  }

  const d = data.dashboard;
  const ringColor = getHealthColor(d.avg_health);
  const firstAgentId = d.agents && d.agents.length > 0 ? d.agents[0].agent_id : '';

  let agentsHtml = '';
  if (d.agents && d.agents.length > 0) {
    agentsHtml = d.agents.map(a => `
      <div class="card agent-card" onclick="loadAgentSkills('${a.agent_id}')">
        <div class="agent-header">
          <div class="agent-name">${a.name}${a.is_primary ? '<span class="badge badge-primary">主</span>' : ''}</div>
          <div class="agent-health ${getHealthClass(a.health_score)}">${Math.round(a.health_score || 0)}分</div>
        </div>
      </div>
    `).join('');
  }

  // ── 从最新报告数据中提取丰富内容 ──
  const lr = d.latest_report || {};
  const lrOv = lr.overview || {};
  const lrRecs = lr.recommendations || [];
  const lrDiag = lr.diagnostics || {};
  const lrInstalled = lr.installed_skills || [];

  // 用最新报告中的 overview 数据覆盖仪表盘汇总（更准确）
  const displayTotalSkills = lrOv.total_installed || d.total_skills || 0;
  const displayRunnableSkills = lrOv.total_runnable || 0;

  // 诊断问题 & 建议 HTML
  let diagHtml = '';
  const issues = lrDiag.issues || [];
  const suggestions = lrDiag.suggestions || [];
  if (issues.length > 0 || suggestions.length > 0) {
    diagHtml += '<div class="card report-section-card">';
    diagHtml += '<h2 class="card-title">🩺 诊断摘要</h2>';
    if (issues.length > 0) {
      diagHtml += '<div class="diag-section"><div class="diag-subtitle">🚨 发现问题</div>';
      diagHtml += '<div class="bullet-card-list">';
      issues.forEach(item => { diagHtml += `<div class="bullet-card-item">${escapeHtml(item)}</div>`; });
      diagHtml += '</div></div>';
    }
    if (suggestions.length > 0) {
      diagHtml += '<div class="diag-section" style="margin-top:12px"><div class="diag-subtitle">🛠 优化建议</div>';
      diagHtml += '<div class="bullet-card-list">';
      suggestions.forEach(item => { diagHtml += `<div class="bullet-card-item">${escapeHtml(item)}</div>`; });
      diagHtml += '</div></div>';
    }
    diagHtml += '</div>';
  }

  // 推荐安装 HTML
  let recsHtml = '';
  if (lrRecs.length > 0) {
    recsHtml = renderRecommendations(lrRecs);
  }

  // 已安装技能 HTML
  let installedHtml = '';
  if (lrInstalled.length > 0) {
    installedHtml = `
      <div class="card report-section-card">
        <h2 class="card-title">🧩 已安装 Skills <span style="font-size:13px; color:var(--text-muted); font-weight:400;">${lr.installed_skills_total || lrInstalled.length} 个</span></h2>
        <div class="installed-skill-list">
          ${lrInstalled.map(s => `
            <div class="installed-skill-item">
              <div>
                <div class="installed-name">${escapeHtml(s.name || s.slug || 'unknown')}</div>
                <div class="installed-meta">${escapeHtml(s.category || '未分类')} · ${s.runnable ? '可运行' : '仅文档'}</div>
              </div>
              <div class="installed-right">
                ${s.total_score != null ? `<span class="installed-score">${Number(s.total_score).toFixed(1)}</span>` : '<span class="installed-score muted">待评分</span>'}
              </div>
            </div>`).join('')}
        </div>
      </div>`;
  }

  // 能力覆盖 HTML
  let coverageHtml = renderCoverage(lrDiag.coverage || []);

  // 未使用技能 HTML
  let unusedHtml = '';
  const unused = lrDiag.unused_runnable || [];
  if (unused.length > 0) {
    unusedHtml = renderStringListCard('💤 未使用的可运行 Skills', unused);
  }

  // 报告来源标注
  let reportBadge = '';
  if (lr.id) {
    reportBadge = `
      <div class="card report-source-card" onclick="loadReportDetail(${lr.id})" style="cursor:pointer">
        <div class="report-source-inner">
          <span>📄 数据来源：${getReportTypeLabel(lr.report_type)} · ${lr.report_date || ''}</span>
          <span class="report-source-link">查看完整报告 →</span>
        </div>
      </div>`;
  }

  container.innerHTML = `
    <div class="compact-hero card">
      <div class="compact-hero-left">
        <div class="compact-agent-name">${escapeHtml(d.agents && d.agents.length > 0 ? d.agents[0].name : '智能体')}</div>
        <p class="compact-subtitle">数据总览</p>
      </div>
      <div class="compact-hero-right">
        <div class="compact-score" style="color: ${ringColor}">${Math.round(d.avg_health || 0)}</div>
        <div class="compact-score-label">健康度</div>
      </div>
    </div>

    <div class="compact-metrics">
      <div class="cm-item"><span class="cm-val">${displayTotalSkills}</span><span class="cm-lbl">已安装</span></div>
      <div class="cm-item clickable" onclick="${firstAgentId ? `loadAgentSkills('${firstAgentId}')` : ''}"><span class="cm-val">${displayRunnableSkills}</span><span class="cm-lbl">可运行 →</span></div>
      <div class="cm-item"><span class="cm-val">${d.total_runs}</span><span class="cm-lbl">运行</span></div>
      <div class="cm-item"><span class="cm-val">${d.avg_success_rate}%</span><span class="cm-lbl">成功率</span></div>
    </div>

    ${reportBadge}
    ${diagHtml}
    ${recsHtml}
    ${coverageHtml}
    ${installedHtml}
    ${unusedHtml}

    ${d.trend && d.trend.length > 1 ? `
    <div class="card">
      <h2 class="card-title">📈 7 日趋势</h2>
      <div class="chart-container"><canvas id="trendCanvas"></canvas></div>
    </div>` : ''}

    ${agentsHtml ? `<h2 class="card-title" style="margin: 16px 0 8px;">🤖 我的智能体</h2>${agentsHtml}` : ''}

    <footer class="footer">Skills Monitor PWA v1.0 · Powered by CodeBuddy</footer>
  `;

  // 画趋势图
  if (d.trend && d.trend.length > 1) {
    renderTrendChart(d.trend);
  }
}

function renderTrendChart(trend) {
  const ctx = document.getElementById('trendCanvas');
  if (!ctx) return;

  if (trendChart) trendChart.destroy();

  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: trend.map(t => t.date.slice(5)),
      datasets: [{
        label: '健康度',
        data: trend.map(t => t.health_score),
        borderColor: '#667eea',
        backgroundColor: 'rgba(102,126,234,0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: '#667eea',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { min: 0, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#999' } },
        x: { grid: { display: false }, ticks: { color: '#999' } }
      }
    }
  });
}

// ──────── Agent Skills ────────

async function loadAgentSkills(agentId) {
  showPage('skill-detail');
  const container = $('skill-detail-content');
  container.innerHTML = '<div class="loading"><div class="spinner"></div>加载中...</div>';

  const data = await api('/skills/' + agentId);
  if (!data || !data.ok) {
    container.innerHTML = '<div class="empty-state"><div class="icon">📭</div><h3>暂无数据</h3></div>';
    return;
  }

  const skills = data.skills || [];
  const sorted = skills.sort((a, b) => (b.total_score || 0) - (a.total_score || 0));

  let html = `
    <div class="back-btn" onclick="showPage('dashboard')">← 返回仪表盘</div>
    <div class="page-header" style="padding-top: 0">
      <div class="icon">🧠</div>
      <h1>${escapeHtml(data.agent_name || '智能体')}</h1>
      <p class="subtitle">${skills.length} 个有评分的技能</p>
    </div>
  `;

  if (sorted.length > 0) {
    html += renderScoreList(sorted);
  } else {
    html += '<div class="empty-state"><div class="icon">📭</div><h3>暂无技能数据</h3><p>这通常表示最近还没有有效运行记录，或报告尚未重新上报。</p></div>';
  }

  container.innerHTML = html;
}

// ──────── 报告列表 ────────

async function loadReports() {
  const container = $('reports-content');
  container.innerHTML = '<div class="loading"><div class="spinner"></div>加载中...</div>';

  const data = await api('/reports?limit=30&type=all');
  if (!data || !data.ok || !data.reports.length) {
    container.innerHTML = '<div class="empty-state"><div class="icon">📋</div><h3>暂无报告</h3><p>智能体尚未上报任何数据</p></div>';
    return;
  }

  let html = '<div class="card">';
  data.reports.forEach(r => {
    const scoreColor = getHealthColor(r.health_score);
    const typeLabel = r.report_type === 'diagnostic' ? '🏥 诊断' : r.report_type === 'daily' ? '📊 日报' : r.report_type;
    html += `
      <div class="report-item" onclick="loadReportDetail(${r.id})">
        <div class="report-info">
          <div class="report-date">${r.report_date} <span style="font-size:11px;color:var(--text-muted)">${typeLabel}</span></div>
          <div class="report-agent">${r.agent_name || r.agent_id.slice(0, 8)}</div>
        </div>
        <div class="report-score" style="color: ${scoreColor}">${Math.round(r.health_score || 0)}</div>
      </div>`;
  });
  html += '</div>';

  container.innerHTML = html;
}

// ──────── 报告详情 ────────

async function loadReportDetail(reportId) {
  showPage('report-detail');
  const container = $('report-detail-content');
  container.innerHTML = '<div class="loading"><div class="spinner"></div>加载中...</div>';

  const data = await api('/report/' + reportId);
  if (!data || !data.ok) {
    container.innerHTML = '<div class="empty-state"><div class="icon">❌</div><h3>加载失败</h3></div>';
    return;
  }

  const r = data.report;
  const ringColor = getHealthColor(r.health_score);
  const scores = r.scores || [];
  const sorted = scores.sort((a, b) => (b.total_score || 0) - (a.total_score || 0));
  const ov = r.overview || {};
  const dg = r.diagnostics || {};
  const recommendations = r.recommendations || [];
  const reportTypeLabel = getReportTypeLabel(r.report_type);
  const healthScore = Math.round(r.health_score || 0);

  // ── 紧凑顶栏：返回 + 报告基本信息 + 健康分数 ──
  let html = `
    <div class="back-btn" onclick="showPage('reports')">← 返回报告列表</div>
    <div class="compact-hero card">
      <div class="compact-hero-left">
        <div class="detail-badge">${reportTypeLabel} <span class="compact-id">#${r.id}</span></div>
        <h1 class="compact-title">${escapeHtml(r.report_date || '')}</h1>
        <p class="compact-subtitle">${escapeHtml(r.agent_name || (r.agent_id || '').slice(0, 8))} · ${escapeHtml(r.trigger || '已上报')}</p>
      </div>
      <div class="compact-hero-right">
        <div class="compact-score" style="color: ${ringColor}">${healthScore}</div>
        <div class="compact-score-label">健康度</div>
      </div>
    </div>

    <div class="compact-metrics">
      <div class="cm-item"><span class="cm-val">${r.total_runs || 0}</span><span class="cm-lbl">7天运行</span></div>
      <div class="cm-item"><span class="cm-val">${Number(r.success_rate || 0).toFixed(1)}%</span><span class="cm-lbl">成功率</span></div>
      <div class="cm-item"><span class="cm-val">${r.active_skills || 0}</span><span class="cm-lbl">活跃</span></div>
      <div class="cm-item"><span class="cm-val">${Math.round(ov.avg_duration_ms || 0)}ms</span><span class="cm-lbl">响应</span></div>
    </div>
  `;

  // ── 诊断摘要 — 直接突出展示 ──
  const issues = dg.issues || [];
  const suggestions = dg.suggestions || [];
  const hasMarkdown = !!r.report_markdown;

  if (issues.length > 0 || suggestions.length > 0) {
    html += `
      <div class="card highlight-card highlight-diag">
        <h2 class="card-title">🩺 诊断摘要</h2>`;
    if (issues.length > 0) {
      html += `<div class="diag-section"><div class="diag-subtitle">🚨 发现 ${issues.length} 个问题</div>`;
      html += '<div class="bullet-card-list">';
      issues.forEach(item => { html += `<div class="bullet-card-item highlight-issue-item">${escapeHtml(item)}</div>`; });
      html += '</div></div>';
    }
    if (suggestions.length > 0) {
      html += `<div class="diag-section" style="margin-top:12px"><div class="diag-subtitle">🛠 ${suggestions.length} 条优化建议</div>`;
      html += '<div class="bullet-card-list">';
      suggestions.forEach(item => { html += `<div class="bullet-card-item highlight-suggest-item">${escapeHtml(item)}</div>`; });
      html += '</div></div>';
    }
    if (hasMarkdown) {
      html += `<div class="diag-expand-row" onclick="toggleDiagnosticReport()"><span>📝 查看完整诊断报告原文</span><span id="diag-toggle-icon">▶</span></div>`;
    }
    html += `</div>`;
  }

  // ── 诊断原文（折叠，不占空间） ──
  if (hasMarkdown) {
    html += `
      <div id="sec-diagnostic-report" class="diagnostic-report-body-wrap" style="display:none;" id="diag-report-body">
        <div class="card report-section-card">
          <h2 class="card-title" style="margin-bottom:12px">📝 完整诊断报告</h2>
          ${renderMarkdown(r.report_markdown)}
        </div>
      </div>`;
  }

  // ── 推荐安装 — 紧随诊断，突出展示 ──
  if (recommendations.length > 0) {
    html += `<div id="sec-recommend"></div>`;
    html += `
      <div class="card highlight-card highlight-rec">
        <h2 class="card-title">✨ 推荐安装（${recommendations.length} 条）</h2>
        <div class="recommend-list">
          ${recommendations.map((rec, index) => {
            const slug = rec.slug || '';
            const detailUrl = rec.detail_url || (slug ? `https://clawhub.ai/skills/${slug}` : '');
            const installCmd = rec.install_command || (slug ? `python install_skills.py ${slug}` : '');
            const installUrl = rec.install_url || (slug ? `https://clawhub.ai/api/v1/download?slug=${slug}` : '');
            return `
            <div class="recommend-card">
              <div class="recommend-top">
                <div>
                  <div class="recommend-rank">TOP ${index + 1}</div>
                  <div class="recommend-name">${escapeHtml(rec.name || slug || '未知 Skill')}</div>
                </div>
                <div class="recommend-score">${Math.round(rec.recommendation_score || 0)}</div>
              </div>
              <div class="recommend-meta">
                <span class="pill">${escapeHtml(rec.category || '未分类')}</span>
                <span class="pill accent">${escapeHtml(rec.reason_label || rec.reason_type || '推荐')}</span>
                ${rec.hub_rating ? `<span class="pill">⭐ ${rec.hub_rating}</span>` : ''}
                ${rec.hub_installs ? `<span class="pill">⬇ ${rec.hub_installs}</span>` : ''}
              </div>
              <div class="recommend-desc">${escapeHtml(rec.description || '')}</div>
              <div class="recommend-reason">${escapeHtml(rec.reason_detail || '')}</div>
              <div class="recommend-actions">
                ${installCmd ? `<button class="rec-action-btn rec-copy-btn" onclick="copyToClipboard('${escapeHtml(installCmd)}', this)" title="复制安装命令">
                  <span class="rec-btn-icon">📋</span> 复制安装命令
                </button>` : ''}
                ${installUrl ? `<button class="rec-action-btn rec-url-btn" onclick="copyToClipboard('${escapeHtml(installUrl)}', this)" title="复制下载链接">
                  <span class="rec-btn-icon">🔗</span> 复制下载链接
                </button>` : ''}
                ${detailUrl ? `<a class="rec-action-btn rec-detail-btn" href="${escapeHtml(detailUrl)}" target="_blank" rel="noopener noreferrer">
                  <span class="rec-btn-icon">🌐</span> 查看 ClawHub 详情
                </a>` : ''}
              </div>
            </div>`;
          }).join('')}
        </div>
      </div>`;
  }

  // ── 报告概览（折叠面板，默认隐藏） ──
  if (Object.keys(ov).length > 0) {
    html += `
      <div class="card report-section-card">
        <div class="collapsible-header" onclick="toggleOverviewPanel()">
          <h2 class="card-title" style="margin:0">📋 报告概览</h2>
          <span class="collapsible-icon" id="ov-toggle-icon">▶</span>
        </div>
        <div class="collapsible-body" id="ov-panel-body" style="display:none;">
          <div class="overview-grid" style="margin-top:14px;">
            <div class="ov-item"><span class="ov-label">已安装技能</span><span class="ov-value">${ov.total_installed || '-'}</span></div>
            <div class="ov-item"><span class="ov-label">可运行技能</span><span class="ov-value">${ov.total_runnable || '-'}</span></div>
            <div class="ov-item"><span class="ov-label">平均得分</span><span class="ov-value">${ov.avg_score != null ? ov.avg_score : '-'}</span></div>
            <div class="ov-item"><span class="ov-label">最佳 Skill</span><span class="ov-value">${escapeHtml(ov.top_skill || '-')}</span></div>
            <div class="ov-item"><span class="ov-label">关注 Skill</span><span class="ov-value">${escapeHtml(ov.worst_skill || '-')}</span></div>
            <div class="ov-item"><span class="ov-label">数据体积</span><span class="ov-value">${r.data_size_bytes || 0}B</span></div>
          </div>
        </div>
      </div>`;
  }

  // ── 详细数据（折叠面板，默认隐藏） ──
  const hasCoverage = (dg.coverage || []).length > 0;
  const hasUsageTop = (dg.usage_top || []).length > 0;
  const hasUnused = (dg.unused_runnable || []).length > 0;
  const hasScores = sorted.length > 0;

  if (hasCoverage || hasUsageTop || hasUnused || hasScores) {
    html += `
      <div class="card report-section-card">
        <div class="collapsible-header" onclick="toggleDetailDataPanel()">
          <h2 class="card-title" style="margin:0">📊 详细数据</h2>
          <span class="collapsible-icon" id="detail-data-toggle-icon">▶</span>
        </div>
        <div class="collapsible-body" id="detail-data-body" style="display:none;">
          <div style="margin-top:14px;">
            ${renderCoverage(dg.coverage || [])}
            ${renderUsageTop(dg.usage_top || [])}
            ${renderStringListCard('💤 未使用的可运行 Skills', dg.unused_runnable || [], '最近 7 天没有未使用的可运行技能')}
            ${renderScoreList(sorted.slice(0, 15))}
          </div>
        </div>
      </div>`;
  }

  container.innerHTML = html;
}

// ──────── 我的 ────────

async function loadMine() {
  const container = $('mine-content');
  container.innerHTML = '<div class="loading"><div class="spinner"></div>加载中...</div>';

  const data = await api('/user');
  if (!data || !data.ok) {
    container.innerHTML = '<div class="empty-state"><div class="icon">❌</div><h3>加载失败</h3></div>';
    return;
  }

  const u = data.user;
  const agentsData = await api('/agents');
  const agents = agentsData?.agents || [];

  let agentsHtml = agents.map(a => `
    <div class="setting-item">
      <div>
        <div class="setting-label">${a.name}${a.is_primary ? ' <span class="badge badge-primary">主</span>' : ''}</div>
        <div class="setting-desc">技能: ${a.total_skills || 0} · 健康度: ${Math.round(a.health_score || 0)}</div>
      </div>
      <div class="agent-health ${getHealthClass(a.health_score)}">${Math.round(a.health_score || 0)}</div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="card" style="text-align: center;">
      <div class="user-avatar">👤</div>
      <div style="font-size: 18px; font-weight: 600;">${u.nickname || 'PWA 用户'}</div>
      <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">
        已绑定 ${u.agent_count} 个智能体
      </div>
    </div>

    <div class="card">
      <h2 class="card-title">🤖 我的智能体</h2>
      ${agentsHtml || '<div class="empty-state"><p>暂无绑定的智能体</p></div>'}
    </div>

    <div class="card">
      <h2 class="card-title" style="cursor: pointer;" onclick="toggleBindForm()">➕ 绑定新智能体 <span id="bind-toggle-arrow" style="float:right; font-size:14px; transition: transform .2s;">▶</span></h2>
      <div id="bind-form" style="display: none;">
        <div class="form-group">
          <label>智能体 ID</label>
          <input type="text" id="bind-agent-id" placeholder="输入智能体 ID">
        </div>
        <div class="form-group">
          <label>Key</label>
          <input type="password" id="bind-agent-token" placeholder="输入 Key">
        </div>
        <button class="btn btn-primary" onclick="doBind()" style="margin-top: 8px;">绑定</button>
      </div>
    </div>

    <div class="card">
      <h2 class="card-title">⚙️ 设置</h2>
      <div class="setting-item">
        <div>
          <div class="setting-label">关于</div>
          <div class="setting-desc">Skills Monitor PWA v1.0</div>
        </div>
      </div>
      <div class="setting-item">
        <div>
          <div class="setting-label" style="color: var(--danger); cursor: pointer;" onclick="doLogout()">退出登录</div>
        </div>
      </div>
    </div>

    <footer class="footer">Skills Monitor PWA v1.0 · Powered by CodeBuddy</footer>
  `;
}

function toggleBindForm() {
  const form = $('bind-form');
  const arrow = $('bind-toggle-arrow');
  if (form.style.display === 'none') {
    form.style.display = 'block';
    arrow.textContent = '▼';
  } else {
    form.style.display = 'none';
    arrow.textContent = '▶';
  }
}

async function doBind() {
  const agentId = $('bind-agent-id').value.trim();
  const agentToken = $('bind-agent-token').value.trim();

  if (!agentId || !agentToken) {
    showToast('请输入智能体 ID 和 Key');
    return;
  }

  const data = await api('/bind', {
    method: 'POST',
    body: JSON.stringify({ agent_id: agentId, agent_token: agentToken }),
  });

  if (data && data.ok) {
    showToast('绑定成功');
    loadMine();
  } else {
    showToast(data?.error || '绑定失败');
  }
}

function doLogout() {
  clearToken();
  currentUser = null;
  showPage('login');
  showToast('已退出');
}

// ──────── 初始化 ────────

async function init() {
  // 清理旧缓存 & 注册 Service Worker
  if ('serviceWorker' in navigator) {
    // 先 unregister 所有旧的 SW，确保缓存被清理
    const regs = await navigator.serviceWorker.getRegistrations();
    for (const reg of regs) {
      await reg.unregister();
    }
    // 清理所有 caches
    if (window.caches) {
      const keys = await caches.keys();
      await Promise.all(keys.map(k => caches.delete(k)));
    }
    // 注册新的 SW
    navigator.serviceWorker.register('/static/pwa/sw.js?v=20260319a').catch(() => {});
  }

  // Tab bar 事件
  document.querySelectorAll('.tab-item').forEach(tab => {
    tab.addEventListener('click', () => showPage(tab.dataset.page));
  });

  // 登录按钮
  $('login-btn').addEventListener('click', doLogin);

  // 回车登录
  $('login-agent-token').addEventListener('keydown', e => {
    if (e.key === 'Enter') doLogin();
  });

  // 检查登录状态
  const token = getToken();
  if (token) {
    const data = await api('/user');
    if (data && data.ok) {
      currentUser = data.user;
      showPage('dashboard');
      return;
    }
  }

  showPage('login');
}

document.addEventListener('DOMContentLoaded', init);
