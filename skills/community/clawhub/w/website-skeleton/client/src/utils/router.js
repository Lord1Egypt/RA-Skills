/**
 * router — 基于 History API 的 SPA 路由
 *
 * 用法：
 *   import { router, navigate } from './utils/router.js';
 *   router.init();
 *   // 手动跳转
 *   navigate('/products?id=123');
 *
 * 路由表定义于底部 routes 对象，每个 handler 接收 params 对象，
 * 返回 HTML 字符串，渲染至 #app 容器。
 */

import { renderHome } from '../pages/home.js';
import { renderLogin } from '../pages/login.js';
import { renderRegister } from '../pages/register.js';
import { renderProducts } from '../pages/products.js';
import { renderCart } from '../pages/cart.js';
import { renderOrders } from '../pages/orders.js';
import { renderNotFound } from '../pages/home.js';
import { renderCheckout } from '../pages/checkout.js';
import { renderOrderDetail } from '../pages/order-detail.js';
import { renderAIChat } from '../pages/ai-chat.js';
import { renderProfile } from '../pages/profile.js';
import { renderProductDetail } from '../pages/product-detail.js';
import { renderAdminDashboard } from '../pages/admin/dashboard.js';
import { renderAdminProducts } from '../pages/admin/products.js';
import { renderAdminOrders } from '../pages/admin/orders.js';

// ===================== 路由表 =====================

/**
 * 路由定义：路径 → handler 函数
 * 支持 :param 动态段（如 /products/:id）
 */
const routes = [
  { pattern: '/', handler: renderHome },
  { pattern: '/login', handler: renderLogin },
  { pattern: '/register', handler: renderRegister },
  { pattern: '/products', handler: renderProducts },
  { pattern: '/products/:id', handler: renderProductDetail },
  { pattern: '/cart', handler: renderCart },
  { pattern: '/orders', handler: renderOrders },
  { pattern: '/checkout', handler: renderCheckout },
  { pattern: '/order/:orderNo', handler: renderOrderDetail },
  { pattern: '/ai-chat', handler: renderAIChat },
  { pattern: '/profile', handler: renderProfile },
  { pattern: '/admin', handler: renderAdminDashboard },
  { pattern: '/admin/products', handler: renderAdminProducts },
  { pattern: '/admin/orders', handler: renderAdminOrders },
];

// ===================== 路由匹配 =====================

/**
 * 将路径模式编译为正则
 * /products/:id → /^\/products\/([^/]+)$/
 */
function compilePattern(pattern) {
  const paramNames = [];
  const regexStr = pattern.replace(/:([^/]+)/g, (_, name) => {
    paramNames.push(name);
    return '([^/]+)';
  });
  return { regex: new RegExp(`^${regexStr}$`), paramNames };
}

// 预编译路由表
const compiled = routes.map(r => ({
  ...r,
  ...compilePattern(r.pattern),
}));

/**
 * 匹配当前路径，返回匹配的 handler 和参数
 */
function matchRoute(pathname) {
  // 去除尾部斜杠（根路径除外）
  const path = pathname === '/' ? '/' : pathname.replace(/\/$/, '');

  for (const route of compiled) {
    const match = path.match(route.regex);
    if (match) {
      const params = {};
      route.paramNames.forEach((name, i) => {
        params[name] = decodeURIComponent(match[i + 1]);
      });
      // 解析 query string
      const qIndex = pathname.indexOf('?');
      if (qIndex !== -1) {
        const qs = new URLSearchParams(pathname.slice(qIndex));
        for (const [k, v] of qs) {
          params[k] = v;
        }
      }
      return { handler: route.handler, params };
    }
  }
  return null;
}

// ===================== Router 对象 =====================

export const router = {
  /**
   * 初始化路由（DOMContentLoaded 后调用）
   */
  init() {
    this.render();
  },

  /**
   * 根据当前 URL 渲染对应页面
   */
  render() {
    const path = window.location.pathname;
    const match = matchRoute(path);
    const app = document.getElementById('app');
    if (!app) return;

    let content;
    if (match) {
      content = match.handler(match.params);
    } else {
      content = renderNotFound();
    }
    app.innerHTML = content;

    // 更新活动导航高亮
    this._updateActiveNav(path);
  },

  /**
   * 编程式导航（pushState + 渲染）
   * @param {string} path - 路径（如 /products）
   * @param {Object} [state] - 可选的 history state
   */
  navigate(path, state) {
    window.history.pushState(state || null, '', path);
    this.render();
  },

  /**
   * 替换当前历史记录（不增加历史条目）
   * @param {string} path
   */
  replace(path) {
    window.history.replaceState(null, '', path);
    this.render();
  },

  /** 内部：更新导航高亮 */
  _updateActiveNav(path) {
    document.querySelectorAll('[data-nav]').forEach(el => {
      const href = el.getAttribute('href');
      if (href) {
        const isActive = path === href || (href !== '/' && path.startsWith(href));
        el.classList.toggle('active', isActive);
      }
    });
  },
};

/**
 * 便捷导航函数
 * @param {string} path
 */
export function navigate(path) {
  router.navigate(path);
}
