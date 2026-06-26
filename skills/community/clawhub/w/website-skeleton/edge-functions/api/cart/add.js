/**
 * Cart Add API — Edge Function
 *
 * POST /api/cart/add
 * body {productId, quantity}，要求 auth
 * KV `cart:{tenant}:{userId}` → 数组
 *
 * Phase 4A P0-3 实现
 */

import { verifyJWT } from '../../sharing/jwt-helper.js';
import { cartKey, getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, unauthorized, internalError } from '../../sharing/response.js';

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

  if (request.method !== 'POST') {
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

    const { productId, quantity = 1 } = body;
    if (!productId) {
      return badRequest('productId 为必填项');
    }
    if (typeof quantity !== 'number' || quantity < 1) {
      return badRequest('quantity 必须为正整数');
    }

    const cartKeyStr = cartKey(tenant, userId);

    // 读取当前购物车
    let cart = [];
    const existing = await env.KV.get(cartKeyStr);
    if (existing) {
      cart = JSON.parse(existing);
    }

    // 查找是否已有该商品
    const existingItem = cart.find(item => item.productId === productId);
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({ productId, quantity });
    }

    // 写回 KV
    await env.KV.put(cartKeyStr, JSON.stringify(cart), {
      expirationTtl: CART_TTL,
    });

    return ok({ cart });
  } catch (err) {
    console.error('[Cart Add] Error:', err.message, err.stack);
    return internalError('添加购物车失败');
  }
}
