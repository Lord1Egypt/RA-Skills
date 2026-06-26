/**
 * Auth Refresh API — Edge Function
 *
 * POST /api/auth/refresh
 * 读 RT → 验证 → KV version 检查 → 轮换 → 返回新 token
 * 409 on concurrent rotation
 *
 * Phase 4A P0-1 实现
 */

import { verifyRefreshToken, signAccessToken, signRefreshToken, extractRefreshToken } from '../../sharing/jwt-helper.js';
import { rtMetaKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, unauthorized, conflict, internalError } from '../../sharing/response.js';

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    // ===== 步骤 1：提取 Refresh Token =====
    // 从 Cookie 读取
    let refreshToken = extractRefreshToken(request);

    // 如果 Cookie 没有，尝试从请求体读取（方便客户端调用）
    if (!refreshToken) {
      try {
        const body = await request.json();
        refreshToken = body.refreshToken;
      } catch {
        // ignore
      }
    }

    if (!refreshToken) {
      return unauthorized('缺少 Refresh Token');
    }

    // ===== 步骤 2：验证 RT =====
    const payload = await verifyRefreshToken(refreshToken, env);
    if (!payload) {
      return unauthorized('Refresh Token 无效或已过期');
    }

    if (payload.type !== 'refresh') {
      return unauthorized('Token 类型错误，需要 Refresh Token');
    }

    const userId = String(payload.sub);
    const tenant = getTenant(payload);
    const rtMetaKeyStr = rtMetaKey(tenant, userId);

    // ===== 步骤 3：检查 KV version（乐观锁） =====
    const rtMetaStr = await env.KV.get(rtMetaKeyStr);
    if (!rtMetaStr) {
      return unauthorized('Refresh Token 已被吊销');
    }

    const rtMeta = JSON.parse(rtMetaStr);

    if (String(rtMeta.version) !== String(payload.v)) {
      // version 不匹配 → 并发轮换或 Token 重用攻击
      console.warn(`[Refresh] Version mismatch for user ${userId}: expected ${rtMeta.version}, got ${payload.v}`);
      return conflict('Token 已被轮换，请重新登录');
    }

    // ===== 步骤 4：轮换 Token =====
    const newVersion = Date.now().toString(36);
    const newAccessToken = await signAccessToken(
      { sub: userId, email: payload.email, role: payload.role || 'user', tenant },
      env
    );
    const newRefreshToken = await signRefreshToken(userId, newVersion, env);

    // ===== 步骤 5：更新 KV =====
    rtMeta.version = newVersion;
    rtMeta.token = newRefreshToken;
    rtMeta.rotatedAt = Date.now();

    await env.KV.put(
      rtMetaKeyStr,
      JSON.stringify(rtMeta),
      { expirationTtl: 604800 } // 7d
    );

    // ===== 步骤 6：设置新 Cookie =====
    const atCookie = [
      `at=${newAccessToken}`,
      'HttpOnly',
      'Path=/',
      'SameSite=Lax',
      'Max-Age=900',
      ...(env.SITE_DOMAIN ? [`Domain=${env.SITE_DOMAIN}`] : []),
    ].join('; ');

    const rtCookie = [
      `rt=${newRefreshToken}`,
      'HttpOnly',
      'Path=/api/auth',
      'SameSite=Lax',
      'Max-Age=604800',
      ...(env.SITE_DOMAIN ? [`Domain=${env.SITE_DOMAIN}`] : []),
    ].join('; ');

    return new Response(JSON.stringify({
      success: true,
      data: {
        accessToken: newAccessToken,
        refreshToken: newRefreshToken,
      },
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Set-Cookie': [atCookie, rtCookie],
      },
    });
  } catch (err) {
    console.error('[Refresh] Error:', err.message, err.stack);
    return internalError('Token 轮换失败');
  }
}
