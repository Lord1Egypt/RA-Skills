/**
 * Auth Logout API — Edge Function
 *
 * POST /api/auth/logout
 * 清除 Cookie + 删除 KV session
 *
 * Phase 4A P0-1 实现
 */

import { verifyJWT, extractToken } from '../../sharing/jwt-helper.js';
import { sessionKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, internalError } from '../../sharing/response.js';

async function authenticate(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  const token = auth.slice(7);
  try {
    return await verifyJWT(token, env);
  } catch {
    return null;
  }
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    // 尝试从请求体获取 sessionId（可选）
    let sessionId;
    try {
      const body = await request.json();
      sessionId = body.sessionId;
    } catch {
      // ignore
    }

    // 如果请求体没有，尝试从 Cookie 解析
    if (!sessionId) {
      const cookieHeader = request.headers.get('Cookie') || '';
      const sessionMatch = cookieHeader.match(/(?:^|;\s*)at=([^;]+)/);
      if (sessionMatch) {
        const token = decodeURIComponent(sessionMatch[1]);
        const payload = await verifyJWT(token, env);
        if (payload) {
          sessionId = payload.jti;
        }
      }
    }

    // 如果有 sessionId，尝试删除 KV
    if (sessionId) {
      // 通过认证获取 tenant
      const payload = await authenticate(request, env);
      const tenant = payload ? getTenant(payload) : 'default';

      // 尝试删除 session（key 的精确格式取决于创建时的 session key 命名）
      const possibleKeys = [
        sessionKey(tenant, sessionId),
        `${tenant}:session:${sessionId}`,
      ];

      for (const key of possibleKeys) {
        try {
          const existing = await env.KV.get(key);
          if (existing) {
            await env.KV.delete(key);
            break;
          }
        } catch {
          // continue
        }
      }
    }

    // 清除 Cookie
    const clearAtCookie = 'at=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0';
    const clearRtCookie = 'rt=; HttpOnly; Path=/api/auth; SameSite=Lax; Max-Age=0';

    return new Response(JSON.stringify({
      success: true,
      data: { message: '已登出' },
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Set-Cookie': [clearAtCookie, clearRtCookie],
      },
    });
  } catch (err) {
    console.error('[Logout] Error:', err.message);
    return internalError('登出失败');
  }
}
