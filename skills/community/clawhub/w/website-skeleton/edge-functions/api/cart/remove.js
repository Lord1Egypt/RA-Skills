/**
 * Cart Remove API — Edge Function
 *
 * DELETE /api/cart/remove
 * body {productId}，从 KV 删除商品
 *
 * Phase 4A P0-3 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { cartKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, unauthorized, notFound, internalError } from '../../sharing/response.js';

const CART_TTL = 2592000; // 30 天

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

  if (request.method !== 'DELETE') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const payload = await authenticate(request, env);
    if (!payload) {
      return unauthorized('请先登录');
    }

    const tenant = getTenant(payload);
    const userId = String(payload.sub);

    let body;
    try {
      body = await request.json();
    } catch {
      return badRequest('Invalid JSON body');
    }

    const { productId } = body;
    if (!productId) {
      return badRequest('productId 为必填项');
    }

    const cartKeyStr = cartKey(tenant, userId);

    // 读取购物车
    const existing = await env.KV.get(cartKeyStr);
    if (!existing) {
      return notFound('购物车为空');
    }

    let cart = JSON.parse(existing);
    const itemIndex = cart.findIndex(item => item.productId === productId);

    if (itemIndex === -1) {
      return notFound('购物车中未找到该商品');
    }

    // 移除商品
    cart.splice(itemIndex, 1);

    // 写回 KV
    await env.KV.put(cartKeyStr, JSON.stringify(cart), {
      expirationTtl: CART_TTL,
    });

    return ok({ cart });
  } catch (err) {
    console.error('[Cart Remove] Error:', err.message, err.stack);
    return internalError('删除购物车商品失败');
  }
}
