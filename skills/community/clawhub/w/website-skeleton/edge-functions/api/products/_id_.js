/**
 * Product Detail API — Edge Function
 *
 * GET /api/products/:id
 * 单商品查询，KV 缓存 5min
 *
 * Phase 4A P0-2 实现
 */

import { verifyJWT, extractToken } from '../../sharing/jwt-helper.js';
import { getTenant } from '../../sharing/kv-keys.js';
import { ok, notFound, internalError } from '../../sharing/response.js';

const CACHE_TTL = 300; // 5 min

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
    const url = new URL(request.url);
    // URL 模式: /api/products/{id}
    // 注意：EdgeOne/Cloudflare 路由会解析动态参数为 url 的 pathname 部分
    const pathParts = url.pathname.split('/').filter(Boolean);
    // pathParts = ['api', 'products', '{id}']
    const productId = pathParts[2]; // 第三个元素是动态 ID

    if (!productId) {
      return notFound('缺少商品 ID');
    }

    // 获取租户
    const payload = await authenticate(request, env);
    const tenant = payload ? getTenant(payload) : 'default';

    // ===== KV 缓存 =====
    const cacheKey = `${tenant}:product:${productId}`;
    const cached = await env.KV.get(cacheKey);
    if (cached) {
      return new Response(JSON.stringify({
        success: true,
        data: { product: JSON.parse(cached) },
      }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'X-Cache': 'HIT',
        },
      });
    }

    // ===== 查询 D1 =====
    if (!env.DB) {
      return internalError('数据库不可用');
    }

    const product = await env.DB.prepare(
      'SELECT id, name, description, price, image_url, category, status, stock, created_at, updated_at FROM products WHERE id = ? AND tenant_id = ?'
    ).bind(productId, tenant).first();

    if (!product) {
      return notFound('商品不存在');
    }

    // ===== 写入 KV 缓存 =====
    await env.KV.put(cacheKey, JSON.stringify(product), {
      expirationTtl: CACHE_TTL,
    });

    return ok({ product });
  } catch (err) {
    console.error('[Product Detail] Error:', err.message, err.stack);
    return internalError('获取商品详情失败');
  }
}
