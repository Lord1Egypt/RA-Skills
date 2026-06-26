/**
 * Cloud Functions 统一租户中间件 — 从 JWT 解析 tenant 上下文
 *
 * Phase 4A W1 实现：
 * - 从 JWT 解析 tenant / userId / role
 * - 旧 token（无 tenant 字段）在 jwt-helper 中已从 users 表反查
 * - 删除 X-Tenant-ID Header 来源（防止租户伪造）
 * - 注入 superadmin 操作审计日志
 *
 * 使用方式：
 *   import { withTenant } from '../middleware/tenant-context.js';
 *
 *   export async function onRequest(request, env) {
 *     const ctx = await withTenant(request, env);
 *     if (ctx instanceof Response) return ctx; // 401
 *     const { tenant, userId, role } = ctx;
 *     // ...
 *   }
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';

/**
 * 从请求中提取 tenant 上下文
 * @param {Request} request - HTTP 请求
 * @param {Object} env - 环境变量
 * @returns {Object|Response} { tenant, userId, role, isLegacy } 或 401 Response
 */
export async function withTenant(request, env) {
  // 从 Authorization Header 提取 token
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) {
    // 无 Auth 场景（如支付回调）：返回 guest 上下文
    return { tenant: 'default', userId: null, role: 'guest', isLegacy: false };
  }

  const token = auth.slice(7);
  const payload = await verifyJWT(token, env);

  if (!payload) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // ✅ Phase 4: 从 JWT payload 获取 tenant（旧 token 已在 verifyJWT 中反查）
  // ⚠️ 不读取 X-Tenant-ID Header（防止租户伪造）
  const tenant = payload.tenant || 'default';
  const userId = payload.sub || null;
  const role = payload.role || 'guest';
  const isLegacy = payload._isLegacy || false;

  return { tenant, userId, role, isLegacy };
}

/**
 * 获取带审计的 tenant 上下文（用于写操作）
 * @param {Request} request - HTTP 请求
 * @param {Object} env - 环境变量
 * @returns {Object|Response} 上下文对象或 401
 */
export async function withTenantAudit(request, env) {
  const ctx = await withTenant(request, env);
  if (ctx instanceof Response) return ctx;

  // superadmin 操作自动记录审计日志
  if (ctx.role === 'superadmin' || request.method !== 'GET') {
    const auditEntry = {
      timestamp: new Date().toISOString(),
      actor: ctx.userId,
      actorRole: ctx.role,
      actingTenant: ctx.tenant,
      method: request.method,
      path: new URL(request.url).pathname,
      ip: request.headers.get('CF-Connecting-IP') || '',
    };

    // 非阻塞写入审计日志
    if (env.KV) {
      env.KV.put(
        `audit:${Date.now()}:${ctx.userId || 'anon'}`,
        JSON.stringify(auditEntry),
        { expirationTtl: 7776000 } // 90 天
      ).catch(err => console.warn('[Audit] Failed to write:', err.message));
    }
  }

  return ctx;
}
