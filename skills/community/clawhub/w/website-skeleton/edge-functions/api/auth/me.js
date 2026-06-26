/**
 * Auth Me API — Edge Function
 *
 * GET /api/auth/me
 * 从 Cookie 读取 sessionId → KV lookup → 返回用户信息或 401
 *
 * Phase 4A P0-1 实现
 */

import { verifyJWT, extractToken } from '../../sharing/jwt-helper.js';
import { sessionKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, unauthorized, internalError } from '../../sharing/response.js';

async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  const token = auth.slice(7);
  try {
    const payload = await verifyJWT(token, env);
    return payload;
  } catch {
    return null;
  }
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'GET') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    // 方式 A：从 Authorization header 验证 JWT
    const payload = await authenticate(request, env);
    if (payload) {
      const tenant = getTenant(payload);
      const userId = String(payload.sub);

      // 尝试从 KV session 补充信息
      let userData = { id: userId, email: payload.email, role: payload.role, tenant };

      // 扫描所有 session key 来匹配 userId（简化：直接用 userId 查）
      // 实际应通过 session cookie 关联
      return ok({ user: userData });
    }

    // 方式 B：从 Cookie 读 sessionId
    const cookieHeader = request.headers.get('Cookie') || '';
    const sessionMatch = cookieHeader.match(/(?:^|;\s*)at=([^;]+)/);
    if (!sessionMatch) {
      return unauthorized('未登录');
    }

    const token = decodeURIComponent(sessionMatch[1]);
    const sessionPayload = await verifyJWT(token, env);
    if (!sessionPayload) {
      return unauthorized('Token 过期或无效');
    }

    const tenant = getTenant(sessionPayload);
    const userId = String(sessionPayload.sub);

    return ok({
      user: {
        id: userId,
        email: sessionPayload.email,
        role: sessionPayload.role || 'user',
        tenant,
      },
    });
  } catch (err) {
    console.error('[Me] Error:', err.message);
    return internalError('获取用户信息失败');
  }
}
