/**
 * 商品管理 API — 管理员 CRUD
 *
 * GET  /api/admin/products?page=&limit=    — 分页列表
 * POST   /api/admin/products                 — 创建商品
 * PUT    /api/admin/products                 — 更新商品
 * DELETE /api/admin/products                 — 删除商品
 *
 * 所有操作需要 admin 角色 (superadmin / tenant_admin)
 */

import { query, execute, queryOne } from '../../utils/db.js';
import { requireRole, parsePagination } from '../_helpers.js';
import { ok, created, badRequest, notFound, internalError } from '../../../sharing/response.js';

export async function onRequest(request, env) {
  // === 认证 + 角色校验 ===
  const user = await requireRole(request, env, ['superadmin', 'tenant_admin']);
  if (user instanceof Response) return user;
  const { tenant } = user;

  const method = request.method;

  try {
    switch (method) {
      case 'GET':
        return handleList(request, env, tenant);
      case 'POST':
        return handleCreate(request, env, tenant);
      case 'PUT':
        return handleUpdate(request, env, tenant);
      case 'DELETE':
        return handleDelete(request, env, tenant);
      default:
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
          status: 405,
          headers: { 'Content-Type': 'application/json' },
        });
    }
  } catch (err) {
    console.error('[Admin Products] Error:', err);
    return internalError('操作失败');
  }
}

// ===================== GET: 商品列表（分页） =====================

async function handleList(request, env, tenant) {
  const url = new URL(request.url);
  const { page, limit, offset } = parsePagination(url);

  const [items, [{ total }]] = await Promise.all([
    query(
      env,
      'SELECT id, name, price, stock, category_id, status, created_at, updated_at FROM products WHERE tenant_id = {tenant} ORDER BY id DESC LIMIT ? OFFSET ?',
      [limit, offset],
      tenant
    ),
    query(
      env,
      'SELECT COUNT(*) as total FROM products WHERE tenant_id = {tenant}',
      [],
      tenant
    ),
  ]);

  return ok({ items, total, page, limit, totalPages: Math.ceil(total / limit) });
}

// ===================== POST: 创建商品 =====================

async function handleCreate(request, env, tenant) {
  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { name, price, stock, categoryId, status } = body;

  if (!name || price === undefined) {
    return badRequest('name 和 price 为必填项');
  }

  const result = execute(
    env,
    `INSERT INTO products (tenant_id, name, price, stock, category_id, status)
     VALUES ({tenant}, ?, ?, ?, ?, ?)`,
    [
      name,
      parseFloat(price) || 0,
      parseInt(stock, 10) || 0,
      categoryId || null,
      status || 'active',
    ],
    tenant
  );

  return created({
    id: result.meta?.last_row_id || null,
    name,
    price,
    stock,
    categoryId,
    status: status || 'active',
  });
}

// ===================== PUT: 更新商品 =====================

async function handleUpdate(request, env, tenant) {
  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { id, name, price, stock, categoryId, status } = body;

  if (!id) {
    return badRequest('id 为必填项');
  }

  // 构建动态更新语句
  const fields = [];
  const params = [];

  if (name !== undefined) {
    fields.push('name = ?');
    params.push(name);
  }
  if (price !== undefined) {
    fields.push('price = ?');
    params.push(parseFloat(price));
  }
  if (stock !== undefined) {
    fields.push('stock = ?');
    params.push(parseInt(stock, 10));
  }
  if (categoryId !== undefined) {
    fields.push('category_id = ?');
    params.push(categoryId);
  }
  if (status !== undefined) {
    fields.push('status = ?');
    params.push(status);
  }

  if (fields.length === 0) {
    return badRequest('没有需要更新的字段');
  }

  params.push(id);

  const result = execute(
    env,
    `UPDATE products SET ${fields.join(', ')} WHERE tenant_id = {tenant} AND id = ?`,
    params,
    tenant
  );

  if (result.affectedRows === 0) {
    return notFound('商品不存在');
  }

  return ok({ id, updated: true });
}

// ===================== DELETE: 删除商品 =====================

async function handleDelete(request, env, tenant) {
  let body;
  try {
    body = await request.json();
  } catch {
    return badRequest('Invalid JSON body');
  }

  const { id } = body;

  if (!id) {
    return badRequest('id 为必填项');
  }

  const result = execute(
    env,
    'DELETE FROM products WHERE tenant_id = {tenant} AND id = ?',
    [id],
    tenant
  );

  if (result.affectedRows === 0) {
    return notFound('商品不存在');
  }

  return ok({ id, deleted: true });
}
