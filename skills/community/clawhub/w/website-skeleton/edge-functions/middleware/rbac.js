/**
 * Edge Functions RBAC 中间件 — 角色授权
 *
 * Phase 4 P0-4 实现：
 * - 从 JWT 解析 role 并校验
 * - 与 Cloud 侧 tenant-context.js 对称设计
 * - 注入 request.tenantContext 供下游使用
 *
 * 使用方式：
 *   import { requireRole } from '../middleware/rbac.js';
 *
 *   export async function onRequest(request, env) {
 *     const rbac = await requireRole(['superadmin'])(request, env);
 *     if (rbac instanceof Response) return rbac;
 *     const { tenant, role, userId } = request.tenantContext;
 *     // ...
 *   }
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';

/**
 * 创建角色授权中间件
 * @param {string[]} allowedRoles - 允许的角色列表
 * @returns {Function} 中间件函数 (request, env) => Response | undefined
 */
export function requireRole(allowedRoles) {
  return async (request, env) => {
    try {
      // 从 Authorization Header 提取 token
      const auth = request.headers.get('Authorization');
      if (!auth?.startsWith('Bearer ')) {
        return new Response(JSON.stringify({
          error: 'Unauthorized',
          message: 'Missing or invalid Authorization header',
        }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      const token = auth.slice(7);
      const payload = await verifyJWT(token, env);

      if (!payload) {
        return new Response(JSON.stringify({
          error: 'Unauthorized',
          message: 'Invalid or expired token',
        }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      const role = payload.role || 'guest';

      if (!allowedRoles.includes(role)) {
        return new Response(JSON.stringify({
          error: 'Forbidden',
          message: `Requires one of roles: ${allowedRoles.join(', ')}`,
        }), {
          status: 403,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      // 注入 tenantContext 供下游 handler 使用
      request.tenantContext = {
        tenant: payload.tenant || 'default',
        role,
        userId: payload.sub,
        isLegacy: payload._isLegacy || false,
      };

      // 返回 undefined 表示放行
      return undefined;
    } catch (err) {
      console.error('[RBAC] Error:', err.message);
      return new Response(JSON.stringify({
        error: 'Internal Server Error',
        message: 'Authorization check failed',
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }
  };
}

/**
 * 便捷中间件：仅 superadmin 可访问
 */
export const requireSuperadmin = () => requireRole(['superadmin']);

/**
 * 便捷中间件：superadmin 或 tenant_admin 可访问
 */
export const requireAdmin = () => requireRole(['superadmin', 'tenant_admin']);
