/**
 * home.js — 首页
 *
 * Hero 区域 + 功能卡片展示
 */

import { navigate } from '../utils/router.js';
import { auth } from '../app.js';

/**
 * 渲染首页
 * @returns {string}
 */
export function renderHome() {
  return `
    <div class="home-page">
      <!-- Hero 区域 -->
      <section class="hero">
        <div class="container hero-content">
          <h1 class="hero-title">极客商城</h1>
          <p class="hero-subtitle">正品保证 · 极速发货 · 极客首选</p>
          <div class="hero-actions">
            <a href="/products" class="btn btn-primary btn-lg" data-nav>浏览商品</a>
            ${auth.isLoggedIn() ? '' : '<a href="/register" class="btn btn-secondary btn-lg" data-nav>免费注册</a>'}
          </div>
        </div>
      </section>

      <!-- 功能卡片 -->
      <section class="container">
        <h2 class="section-title">快速开始</h2>
        <div class="grid grid-3">
          ${renderTemplateCard({
            icon: '🛍️',
            title: '电子商务',
            desc: '完整的前后端 E-Commerce 模板，支持商品管理、购物车、订单系统。',
            link: '/products',
          })}
          ${renderTemplateCard({
            icon: '🤖',
            title: 'AI 助手',
            desc: '智能对话界面，流式 SSE 响应，支持多轮对话与上下文记忆。',
            link: '#',
          })}
          ${renderTemplateCard({
            icon: '📊',
            title: 'SaaS 管理后台',
            desc: '响应式仪表盘、数据可视化、用户权限管理，开箱即用。',
            link: '#',
          })}
        </div>
      </section>

      <!-- 特性介绍 -->
      <section class="container features-section">
        <h2 class="section-title">核心特性</h2>
        <div class="grid grid-3">
          <div class="card feature-card">
            <div class="card-body text-center">
              <div class="feature-icon">⚡</div>
              <h3>极速响应</h3>
              <p class="text-muted">基于 Vanilla JS 构建，零依赖，首屏加载极快。</p>
            </div>
          </div>
          <div class="card feature-card">
            <div class="card-body text-center">
              <div class="feature-icon">🌓</div>
              <h3>深色模式</h3>
              <p class="text-muted">自动跟随系统偏好，CSS Variables 全面支持。</p>
            </div>
          </div>
          <div class="card feature-card">
            <div class="card-body text-center">
              <div class="feature-icon">📱</div>
              <h3>移动优先</h3>
              <p class="text-muted">从手机到桌面，响应式布局，体验无缝衔接。</p>
            </div>
          </div>
        </div>
      </section>
    </div>`;
}

/**
 * 渲染模板卡片
 */
function renderTemplateCard({ icon, title, desc, link }) {
  return `
    <div class="card template-card" onclick="event.preventDefault(); window.__navigate && window.__navigate('${link}')">
      <div class="card-body text-center">
        <div class="template-icon">${icon}</div>
        <h3>${title}</h3>
        <p class="text-muted">${desc}</p>
        <a href="${link}" class="btn btn-sm btn-primary mt-2" data-nav>查看详情</a>
      </div>
    </div>`;
}

/**
 * 404 页面
 * @returns {string}
 */
export function renderNotFound() {
  return `
    <div class="container not-found-page" style="text-align:center;padding:4rem 1rem">
      <div style="font-size:4rem;margin-bottom:1rem">🔍</div>
      <h1>404 — 页面未找到</h1>
      <p class="text-muted">您访问的页面不存在或已被移除。</p>
      <a href="/" class="btn btn-primary mt-4" data-nav>返回首页</a>
    </div>`;
}
