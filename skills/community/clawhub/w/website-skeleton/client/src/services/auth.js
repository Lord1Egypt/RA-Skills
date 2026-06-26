/**
 * AuthService — 认证服务
 *
 * 管理用户登录/注册/登出/会话检查。
 * ⚠️ 安全说明：Access Token 通过 HttpOnly Cookie 传递（防 XSS），
 *    不需要手动管理 token 存储。localStorage 仅作后备缓存。
 *
 * 事件：
 *   auth:login   — 用户登录成功
 *   auth:logout  — 用户登出
 *   auth:updated — 用户信息更新
 */

import { api } from './api.js';
import { bus } from '../app.js';
import { storage } from '../utils/storage.js';

const USER_KEY = 'user';

export class AuthService {
  constructor() {
    /** @type {Object|null} */
    this.user = null;
  }

  // ===================== 登录 =====================

  /**
   * 登录
   * @param {string} email
   * @param {string} password
   * @returns {Promise<Object>} 用户信息
   */
  async login(email, password) {
    const data = await api.post('/auth/login', { email, password });
    // Token 已由服务端通过 HttpOnly Cookie 设置，无需客户端存储
    this.user = data.user || data;
    storage.set(USER_KEY, this.user);
    bus.emit('auth:login', this.user);
    return this.user;
  }

  // ===================== 注册 =====================

  /**
   * 注册
   */
  async register(email, password, name) {
    const data = await api.post('/auth/register', { email, password, name });
    return data;
  }

  // ===================== 登出 =====================

  /**
   * 登出
   */
  async logout() {
    try {
      await api.post('/auth/logout');
    } catch {
      // 即使服务端报错，也清除本地状态
    }
    this.clearSession();
    bus.emit('auth:logout');
  }

  // ===================== 会话检查 =====================

  /**
   * 检查登录状态（应用启动时调用）
   * 通过 HttpOnly Cookie 自动携带凭证，调用 /api/auth/me 验证
   */
  async checkSession() {
    const user = storage.get(USER_KEY);

    try {
      // Cookie 自动携带，无需手动传 token
      const me = await api.get('/auth/me');
      this.user = me.user || me;
      storage.set(USER_KEY, this.user);
      bus.emit('auth:updated', this.user);
    } catch {
      this.user = user || null;
    }
  }

  // ===================== Session 管理 =====================

  /**
   * 是否已登录
   * @returns {boolean}
   */
  isLoggedIn() {
    return !!this.user;
  }

  /**
   * 获取当前用户信息
   * @returns {Object|null}
   */
  getUser() {
    return this.user;
  }

  /**
   * 清除本地 session（登出时调用）
   */
  clearSession() {
    this.user = null;
    storage.remove(USER_KEY);
  }
}
