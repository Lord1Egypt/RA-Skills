/**
 * renderNavbar — 构建导航栏 HTML
 *
 * 基于当前 auth 状态渲染登录/用户菜单。
 */

import { auth } from '../app.js';

/**
 * 构建导航栏 HTML
 * @returns {string}
 */
export function renderNavbar() {
  const user = auth?.user;
  const isLoggedIn = auth?.isLoggedIn?.();

  let userMenuHtml;
  if (isLoggedIn && user) {
    const avatarLetter = (user.name || user.email || 'U')[0].toUpperCase();
    userMenuHtml = `
      <div class="user-menu">
        <button class="user-menu-trigger" id="user-menu-btn" data-user-menu>
          <span class="user-menu-avatar">${escapeAttr(avatarLetter)}</span>
          <span id="user-name">${escapeAttr(user.name || user.email || '用户')}</span>
        </button>
        <div class="user-menu-dropdown" id="user-menu-dropdown" style="display:none">
          <a href="/orders" data-nav>我的订单</a>
          <button id="logout-btn">退出登录</button>
        </div>
      </div>`;
  } else {
    userMenuHtml = `
      <div class="user-menu">
        <a href="/login" class="btn btn-sm btn-secondary" data-nav>登录</a>
        <a href="/register" class="btn btn-sm btn-primary" data-nav>注册</a>
      </div>`;
  }

  return `
    <div class="navbar-inner">
      <a href="/" class="navbar-brand" data-nav>
        <span class="brand-icon">⚡</span>
        <span>极客商城</span>
      </a>

      <ul class="navbar-links">
        <li><a href="/" data-nav>首页</a></li>
        <li><a href="/products" data-nav>商品</a></li>
        <li><a href="/orders" data-nav>订单</a></li>
      </ul>

      <div class="navbar-right">
        <a href="/cart" class="cart-badge" data-nav aria-label="购物车">
          🛒
          <span class="cart-count" id="cart-count" style="display:none">0</span>
        </a>
        ${userMenuHtml}
      </div>
    </div>`;
}

/**
 * 简单的属性转义
 */
function escapeAttr(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
