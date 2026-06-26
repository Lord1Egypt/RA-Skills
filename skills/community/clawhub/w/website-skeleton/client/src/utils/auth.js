/**
 * auth — 认证工具（analytics 桥接层）
 *
 * 注意：这是 utils 层的薄封装，从 services/auth.js 导入真实实现。
 * analytics.js 等旧模块通过 `import { getUserId } from './auth.js'` 引用。
 */

import { auth } from '../app.js';

/**
 * 获取当前用户 ID（用于埋点）
 * @returns {string|null}
 */
export function getUserId() {
  return auth?.user?.id || null;
}

/**
 * 获取会话 ID（用于埋点）
 * @returns {string|null}
 */
export function getSessionId() {
  // 尽量复用已有 session，否则按需生成
  const stored = sessionStorage.getItem('analytics:session_id');
  if (stored) return stored;
  const id = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
  try { sessionStorage.setItem('analytics:session_id', id); } catch { /* ignore */ }
  return id;
}
