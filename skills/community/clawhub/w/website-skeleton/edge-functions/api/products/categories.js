/**
 * Product Categories API — Edge Function
 *
 * GET /api/products/categories
 * 查询分类列表
 *
 * Phase 4A P0-2 实现
 */

import { getTenant } from '../../sharing/kv-keys.js';
import { ok, internalError } from '../../sharing/response.js';

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'GET') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    if (!env.DB) {
      return internalError('数据库不可用');
    }

    const url = new URL(request.url);
    const tenant = url.searchParams.get('tenant') || 'default';

    // 查询分类及其商品数量
    const categories = await env.DB.prepare(
      'SELECT category as id, category as name, COUNT(*) as count FROM products WHERE tenant_id = ? AND status = \'active\' GROUP BY category ORDER BY category ASC'
    ).bind(tenant).all();

    return ok({ categories: categories.results || [] });
  } catch (err) {
    console.error('[Categories] Error:', err.message, err.stack);
    return internalError('获取分类列表失败');
  }
}
