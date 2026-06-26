/**
 * 审计日志中间件 — superadmin 操作追踪
 *
 * Phase 4A W3 实现（安全专家 S-04）：
 * - superadmin 跨租户操作自动记录
 * - 所有写操作（非 GET）记录审计
 * - 90 天 KV 保留期
 *
 * 使用方式：
 *   import { auditLog } from '../middleware/audit.js';
 *
 *   export async function onRequest(request, env) {
 *     const ctx = await withTenant(request, env);
 *     const result = await handleRequest(request, ctx);
 *     await auditLog(request, ctx, result, env);
 *     return result;
 *   }
 */

/**
 * 写入审计日志
 * @param {Request} request - HTTP 请求
 * @param {Object} context - 租户上下文（含 userId, role, tenant）
 * @param {Response} result - 处理结果
 * @param {Object} env - 环境变量（含 env.KV）
 */
export async function auditLog(request, context, result, env) {
  // 仅记录：superadmin 的所有操作 + 所有角色的写操作
  if (!shouldAudit(context.role, request.method)) return;

  const entry = {
    timestamp: new Date().toISOString(),
    actor: context.userId || 'anonymous',
    actorRole: context.role || 'guest',
    actingTenant: context.tenant || 'default',
    method: request.method,
    path: extractPath(request.url),
    statusCode: result?.status || 0,
    ip: request.headers.get('CF-Connecting-IP') || '',
    userAgent: request.headers.get('User-Agent')?.slice(0, 200) || '',
  };

  try {
    if (env?.KV) {
      await env.KV.put(
        `audit:${Date.now()}:${context.userId || 'anon'}`,
        JSON.stringify(entry),
        { expirationTtl: 7776000 } // 90 天
      );
    }
  } catch (err) {
    // 审计日志写入失败不应阻塞业务
    console.warn('[Audit] Failed to write log:', err.message);
  }
}

/**
 * 批量查询审计日志（superadmin 专用）
 * @param {Object} env - 环境变量
 * @param {Object} filters - 过滤条件（tenant, actor, method, limit）
 * @returns {Promise<Array>} 审计日志列表
 */
export async function queryAuditLogs(env, filters = {}) {
  const { tenant, actor, method, limit = 50 } = filters;
  const results = [];

  try {
    if (!env?.KV) return results;

    // 使用 KV 前缀扫描（注意：list 操作可能有性能限制）
    const prefix = 'audit:';
    const listResult = await env.KV.list({ prefix, limit: Math.min(limit, 1000) });

    for (const key of listResult.keys) {
      const raw = await env.KV.get(key.name);
      if (!raw) continue;
      try {
        const entry = JSON.parse(raw);
        // 应用过滤条件
        if (tenant && entry.actingTenant !== tenant) continue;
        if (actor && entry.actor !== actor) continue;
        if (method && entry.method !== method) continue;
        results.push(entry);
      } catch { /* skip malformed */ }
    }
  } catch (err) {
    console.warn('[Audit] Failed to query logs:', err.message);
  }

  // 按时间降序排列
  results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  return results.slice(0, limit);
}

// ===================== 内部工具 =====================

function shouldAudit(role, method) {
  // superadmin 的所有操作都需要审计
  if (role === 'superadmin') return true;
  // 所有角色的写操作都需要审计
  return !['GET', 'HEAD', 'OPTIONS'].includes(method);
}

function extractPath(urlStr) {
  try {
    return new URL(urlStr).pathname;
  } catch {
    return urlStr?.slice(0, 200) || 'unknown';
  }
}
