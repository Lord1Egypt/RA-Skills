/**
 * app.js — 应用入口
 *
 * 初始化 SPA：创建全局实例、启动路由、绑定事件。
 *
 * 导出供各模块使用的全局单例：
 *   bus  — EventBus 事件总线
 *   auth — AuthService 认证服务
 *   cart — CartService 购物车服务
 */

import { router } from './utils/router.js';
import { EventBus } from './utils/event-bus.js';
import { AuthService } from './services/auth.js';
import { CartService } from './services/cart.js';
import { trackPageView, initAnalytics } from './utils/analytics.js';
import { renderNavbar } from './components/navbar.js';
import { ToastService } from './components/toast.js';

// ===================== 全局单例 =====================

/** @type {EventBus} */
export const bus = new EventBus();

/** @type {AuthService} */
export const auth = new AuthService();

/** @type {CartService} */
export const cart = new CartService();

/** @type {ToastService} */
export const toast = new ToastService();

// ===================== 应用初始化 =====================

async function init() {
  // 1) 创建导航栏
  const navbar = document.getElementById('navbar');
  if (navbar) {
    navbar.innerHTML = renderNavbar();
  }

  // 2) 检查登录状态
  await auth.checkSession();

  // 3) 初始化购物车
  await cart.init();

  // 4) 初始化路由
  router.init();

  // 5) 初始化埋点
  initAnalytics();

  // 6) 绑定全局事件
  bindGlobalEvents();

  // 7) 监听 popstate（浏览器前进/后退）
  window.addEventListener('popstate', () => {
    router.render();
    trackPageView();
  });

  console.log('[App] 应用初始化完成');
}

/**
 * 绑定全局交互事件
 */
function bindGlobalEvents() {
  // 全局导航点击（拦截 <a data-nav> 避免整页刷新）
  document.addEventListener('click', (e) => {
    const link = e.target.closest('[data-nav]');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href || href.startsWith('http') || href.startsWith('//')) return;
    if (href === '#') return;

    e.preventDefault();
    router.navigate(href);
  });
}

// ===================== 启动 =====================

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
