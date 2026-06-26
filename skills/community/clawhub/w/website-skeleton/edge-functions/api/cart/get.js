/**
 * Cart Get API — Edge Function
 *
 * GET /api/cart/get
 * 返回 KV 中的购物车内容
 *
 * Phase 4A P0-3 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { cartKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, unauthorized, internalError } from '../../sharing/response.js';

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

  if (request.method !== 'GET') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const payload = await authenticate(request, env);
    if (!payload) {
      return unauthorized('请先登录');
    }

    const tenant = getTenant(payload);
    const userId = String(payload.sub);
    const cartKeyStr = cartKey(tenant, userId);

    const cartData = await env.KV.get(cartKeyStr);
    const cart = cartData ? JSON.parse(cartData) : [];

    return ok({ cart });
  } catch (err) {
    console.error('[Cart Get] Error:', err.message, err.stack);
    return internalError('获取购物车失败');
  }
}
