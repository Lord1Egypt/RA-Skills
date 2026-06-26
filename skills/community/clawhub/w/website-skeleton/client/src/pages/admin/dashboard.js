/**
 * admin/dashboard.js — 管理后台首页
 *
 * 功能：统计卡片（总订单数、收入、活跃用户、商品数）、7天趋势图表
 * 路由：/admin
 * 权限：superadmin 或 tenant_admin
 */

import { api } from '../../services/api.js';
import { auth } from '../../app.js';
import { escapeHtml } from '../../utils/escape-html.js';

export function renderAdminDashboard() {
  // 权限检查
  if (!auth.isLoggedIn()) {
    return renderError('请先登录', '/login');
  }

  const role = auth.user?.role;
  if (role !== 'superadmin' && role !== 'tenant_admin') {
    return renderError('无权访问管理后台', '/');
  }

  return `
    <div class="admin-page admin-dashboard-page">
      <div class="admin-header">
        <h1>管理后台</h1>
        <p class="text-muted">系统数据概览</p>
      </div>

      <div id="dashboard-stats" class="dashboard-stats">
        <div class="empty-state" style="padding:3rem 1rem;grid-column:1/-1">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      </div>

      <div class="dashboard-chart-section">
        <div class="card">
          <div class="card-body">
            <h3>近7天趋势</h3>
            <div id="dashboard-chart" class="dashboard-chart">
              <div class="empty-state" style="padding:2rem">
                <div class="spinner"></div>
                <p>加载中...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

export function attachAdminDashboardEvents() {
  loadDashboardStats();
  loadTrendChart();
}

export const __mount = attachAdminDashboardEvents;

async function loadDashboardStats() {
  const container = document.getElementById('dashboard-stats');
  if (!container) return;

  try {
    const data = await api.get('/admin/dashboard/stats');
    const stats = data.stats || data.data || data;

    container.innerHTML = `
      <div class="stat-card">
        <div class="stat-icon stat-icon-orders">📦</div>
        <div class="stat-info">
          <span class="stat-value">${stats.totalOrders ?? '—'}</span>
          <span class="stat-label">总订单数</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon stat-icon-revenue">💰</div>
        <div class="stat-info">
          <span class="stat-value">¥${formatNumber(stats.totalRevenue ?? 0)}</span>
          <span class="stat-label">总收入</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon stat-icon-users">👥</div>
        <div class="stat-info">
          <span class="stat-value">${stats.activeUsers ?? '—'}</span>
          <span class="stat-label">活跃用户</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon stat-icon-products">🛍️</div>
        <div class="stat-info">
          <span class="stat-value">${stats.totalProducts ?? '—'}</span>
          <span class="stat-label">商品总数</span>
        </div>
      </div>`;
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state" style="padding:2rem;grid-column:1/-1">
        <div class="empty-icon">⚠️</div>
        <h3>加载失败</h3>
        <p class="text-muted">${escapeHtml(err.message || '请刷新重试')}</p>
        <button class="btn btn-primary mt-2" onclick="window.location.reload()">重新加载</button>
      </div>`;
  }
}

async function loadTrendChart() {
  const container = document.getElementById('dashboard-chart');
  if (!container) return;

  try {
    const data = await api.get('/admin/dashboard/trend', { days: 7 });
    const trend = data.trend || data.data || data || [];

    const days = trend.map(t => {
      const label = t.label || t.date || '—';
      const shortLabel = typeof label === 'string' ? label.slice(-2) : label;
      return shortLabel;
    });
    const values = trend.map(t => t.value || t.count || t.amount || 0);
    const maxValue = Math.max(...values, 1);

    container.innerHTML = `
      <div class="chart-container">
        <div class="chart-bars">
          ${values.map((v, i) => `
            <div class="chart-bar-item">
              <div class="chart-bar-wrapper">
                <div class="chart-bar" style="height:${(v / maxValue) * 100}%" title="${v}">
                  <span class="chart-bar-value">${v}</span>
                </div>
              </div>
              <div class="chart-bar-label">${escapeHtml(String(days[i] || ''))}</div>
            </div>
          `).join('')}
        </div>
      </div>`;
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state" style="padding:2rem">
        <div class="empty-icon">📊</div>
        <h3>暂无趋势数据</h3>
        <p class="text-muted">${escapeHtml(err.message || '加载失败')}</p>
      </div>`;
  }
}

function renderError(message, link) {
  return `
    <div class="container" style="padding:4rem 1rem;text-align:center">
      <div class="empty-icon" style="font-size:3rem">🔒</div>
      <h3>${escapeHtml(message)}</h3>
      <a href="${link}" class="btn btn-primary mt-4" data-nav>返回</a>
    </div>`;
}

function formatNumber(n) {
  if (n == null) return '0';
  if (n >= 10000) return (n / 10000).toFixed(1) + '万';
  return Number(n).toLocaleString('zh-CN');
}
