/**
 * Cloud Functions 共享辅助函数
 *
 * 提供 authenticate, requireRole 等通用函数，供各 API 端点复用。
 * 路径约定：cloud-functions/api/_helpers.js
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { unauthorized, forbidden } from '../../sharing/response.js';

/**
 * 从请求中提取并验证 JWT
 * @param {Request} request
 * @param {Object} env
 * @returns {Object|null} JWT payload 或 null
 */
export async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  try {
    return await verifyJWT(auth.slice(7), env);
  } catch {
    return null;
  }
}

/**
 * 校验当前用户是否拥有指定角色之一
 * @param {Object} user - JWT payload（含 role）
 * @param {string[]} allowedRoles - 允许的角色列表
 * @returns {boolean}
 */
export function hasRole(user, allowedRoles) {
  if (!user) return false;
  return allowedRoles.includes(user.role);
}

/**
 * 认证 + 角色校验中间件
 * @param {Request} request
 * @param {Object} env
 * @param {string[]} allowedRoles - 允许的角色列表
 * @returns {Object|Response} JWT payload 或错误 Response
 */
export async function requireRole(request, env, allowedRoles) {
  const user = await authenticate(request, env);
  if (!user) {
    return unauthorized();
  }
  if (!hasRole(user, allowedRoles)) {
    return forbidden('权限不足');
  }
  return user;
}

/**
 * 分页辅助：从 URL 解析 page 和 limit
 * @param {URL} url
 * @param {number} [maxLimit=100]
 * @returns {{ page: number, limit: number, offset: number }}
 */
export function parsePagination(url, maxLimit = 100) {
  const page = Math.max(1, parseInt(url.searchParams.get('page'), 10) || 1);
  const limit = Math.min(maxLimit, Math.max(1, parseInt(url.searchParams.get('limit'), 10) || 20));
  const offset = (page - 1) * limit;
  return { page, limit, offset };
}
