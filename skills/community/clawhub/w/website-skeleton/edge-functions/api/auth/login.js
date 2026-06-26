/**
 * Auth Login API — Edge Function
 *
 * POST /api/auth/login
 * 验证 email/password，生成 JWT（15min），创建 KV session，设置 HttpOnly Cookie
 *
 * Phase 4A P0-1 实现
 */

import { signAccessToken, signRefreshToken, extractToken } from '../../sharing/jwt-helper.js';
import { sessionKey, rtMetaKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, unauthorized, internalError } from '../../sharing/response.js';

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { email, password } = body;
  if (!email || !password) {
    return badRequest('email 和 password 为必填项');
  }

  try {
    // ===== 步骤 1：验证凭据 =====
    // 方式 A：调用 Cloud Function 验证密码（推荐，bcrypt 在 Node.js 侧）
    // 方式 B：直接查询 D1（如果 D1 在 EdgeOne 中可用）
    let user;

    if (env.DB) {
      // D1 直接查询
      user = await env.DB.prepare('SELECT id, email, role, tenant_id, password_hash FROM users WHERE email = ?')
        .bind(email).first();

      if (!user) {
        return unauthorized('邮箱或密码错误');
      }

      // 注意：Edge V8 没有 bcrypt，此处假设 D1 返回的 password_hash 是明文（仅演示）
      // 生产环境应调用 Cloud Function /api/auth/verify
      if (password !== user.password_hash) {
        return unauthorized('邮箱或密码错误');
      }
    } else if (env.CLOUD_FUNCTION_BASE) {
      // 调用 Cloud Function 验证
      const verifyRes = await fetch(`${env.CLOUD_FUNCTION_BASE}/api/auth/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!verifyRes.ok) {
        return unauthorized('邮箱或密码错误');
      }

      user = await verifyRes.json();
    } else {
      return internalError('认证服务不可用（缺少 DB 或 CLOUD_FUNCTION_BASE）');
    }

    const tenant = user.tenant_id || 'default';
    const userId = String(user.id);

    // ===== 步骤 2：生成 Token =====
    const accessToken = await signAccessToken(
      { sub: userId, email: user.email, role: user.role || 'user', tenant },
      env
    );

    const refreshVersion = Date.now().toString(36);
    const refreshToken = await signRefreshToken(userId, refreshVersion, env);

    // ===== 步骤 3：创建 KV Session =====
    const sessionId = crypto.randomUUID();
    const sessionData = {
      userId,
      email: user.email,
      role: user.role || 'user',
      tenant,
      createdAt: Date.now(),
    };

    await env.KV.put(
      sessionKey(tenant, sessionId),
      JSON.stringify(sessionData),
      { expirationTtl: 86400 } // 24h
    );

    // ===== 步骤 4：存储 Refresh Token 元信息 =====
    const rtMeta = {
      version: refreshVersion,
      userId,
      token: refreshToken,
      rotatedAt: null,
    };
    await env.KV.put(
      rtMetaKey(tenant, userId),
      JSON.stringify(rtMeta),
      { expirationTtl: 604800 } // 7d
    );

    // ===== 步骤 5：设置 Cookie =====
    const cookieOptions = [
      `at=${accessToken}`,
      'HttpOnly',
      'Path=/',
      'SameSite=Lax',
      'Max-Age=900', // 15 min
      ...(env.SITE_DOMAIN ? [`Domain=${env.SITE_DOMAIN}`] : []),
    ];

    const rtCookieOptions = [
      `rt=${refreshToken}`,
      'HttpOnly',
      'Path=/api/auth',
      'SameSite=Lax',
      'Max-Age=604800', // 7d
      ...(env.SITE_DOMAIN ? [`Domain=${env.SITE_DOMAIN}`] : []),
    ];

    return new Response(JSON.stringify({
      success: true,
      data: {
        accessToken,
        refreshToken,
        user: {
          id: userId,
          email: user.email,
          role: user.role || 'user',
          tenant,
        },
      },
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Set-Cookie': [cookieOptions.join('; '), rtCookieOptions.join('; ')],
      },
    });
  } catch (err) {
    console.error('[Login] Error:', err.message, err.stack);
    return internalError('登录失败');
  }
}
