/**
 * Products List API — Edge Function
 *
 * GET /api/products/list
 * 查询 D1 商品列表，支持 category、page、limit 参数
 * KV 缓存第一页 (product_cache:{tenant}:list) 5min TTL
 *
 * Phase 4A P0-2 实现
 */

import { verifyJWT, extractToken } from '../../sharing/jwt-helper.js';
import { getTenant } from '../../sharing/kv-keys.js';
import { ok, badRequest, internalError } from '../../sharing/response.js';

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
    const category = url.searchParams.get('category') || null;
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1'));
    const limit = Math.min(100, Math.max(1, parseInt(url.searchParams.get('limit') || '20')));

    // 获取租户（公开 API，未登录用户使用 default）
    const payload = await authenticate(request, env);
    const tenant = payload ? getTenant(payload) : 'default';

    // ===== KV 缓存：仅缓存第一页（无分类筛选） =====
    const cacheKey = `${tenant}:product:list`;
    if (page === 1 && !category) {
      const cached = await env.KV.get(cacheKey);
      if (cached) {
        const data = JSON.parse(cached);
        return new Response(JSON.stringify({
          success: true,
          data: { products: data.products, total: data.total, page: 1, limit },
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'X-Cache': 'HIT',
          },
        });
      }
    }

    // ===== 查询 D1 =====
    if (!env.DB) {
      return internalError('数据库不可用');
    }

    let query = 'SELECT id, name, description, price, image_url, category, status, stock, created_at FROM products WHERE tenant_id = ?';
    let countQuery = 'SELECT COUNT(*) as total FROM products WHERE tenant_id = ?';
    const params = [tenant];

    if (category) {
      query += ' AND category = ?';
      countQuery += ' AND category = ?';
      params.push(category);
    }

    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?';
    const offset = (page - 1) * limit;
    params.push(limit, offset);

    const [products, countResult] = await Promise.all([
      env.DB.prepare(query).bind(...params).all(),
      env.DB.prepare(countQuery).bind(...(category ? [tenant, category] : [tenant])).first(),
    ]);

    const total = countResult?.total || 0;
    const result = {
      products: products.results || [],
      total,
      page,
      limit,
    };

    // ===== 写入缓存（仅第一页，无筛选） =====
    if (page === 1 && !category) {
      await env.KV.put(cacheKey, JSON.stringify(result), {
        expirationTtl: CACHE_TTL,
      });
    }

    return ok(result);
  } catch (err) {
    console.error('[Products List] Error:', err.message, err.stack);
    return internalError('获取商品列表失败');
  }
}
