/**
 * 租户管理 API — Edge Functions 版本
 *
 * Phase 4A W4 实现：
 * - 租户 CRUD + 配额管理 + 邀请 + 启用/停用
 * - 使用 RBAC 中间件 requireRole(['superadmin'])
 * - 租户元数据存储在 KV 中
 *
 * 路由：
 *   GET    /api/admin/tenants              — 租户列表
 *   POST   /api/admin/tenants              — 创建租户
 *   GET    /api/admin/tenants/:id          — 租户详情
 *   PUT    /api/admin/tenants/:id          — 更新租户
 *   DELETE /api/admin/tenants/:id          — 删除租户
 *   POST   /api/admin/tenants/:id/invite   — 邀请管理员
 *   PUT    /api/admin/tenants/:id/status   — 启用/停用
 */
import { requireRole } from '../../middleware/rbac.js';

const TENANT_META_PREFIX = 'tenant:meta:';
const TENANT_LIST_KEY = 'tenant:list';

export async function onRequest(request, env) {
  // RBAC 检查：仅 superadmin
  const rbac = await requireRole(['superadmin'])(request, env);
  if (rbac instanceof Response) return rbac;

  const { userId, role, tenant: actingTenant } = request.tenantContext;
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/').filter(Boolean);
  const tenantId = pathParts[3]; // api/admin/tenants/:id

  try {
    let result, statusCode = 200;

    switch (request.method) {
      case 'GET':
        if (tenantId) {
          const data = await getTenant(env, tenantId);
          if (!data) { result = { error: 'Tenant not found' }; statusCode = 404; }
          else result = { ok: true, data };
        } else {
          result = await listTenants(env, url);
        }
        break;

      case 'POST':
        if (tenantId && pathParts[4] === 'invite') {
          result = await inviteTenantAdmin(env, tenantId, await request.json());
        } else {
          result = await createTenant(env, await request.json());
        }
        break;

      case 'PUT':
        if (tenantId && pathParts[4] === 'status') {
          result = await updateTenantStatus(env, tenantId, await request.json());
        } else if (tenantId) {
          result = await updateTenant(env, tenantId, await request.json());
        } else {
          result = { error: 'tenantId is required' }; statusCode = 400;
        }
        break;

      case 'DELETE':
        if (tenantId) result = await deleteTenant(env, tenantId);
        else { result = { error: 'tenantId is required' }; statusCode = 400; }
        break;

      default:
        result = { error: 'Method Not Allowed' }; statusCode = 405;
    }

    return new Response(JSON.stringify(result), {
      status: statusCode, headers: { 'Content-Type': 'application/json' }
    });
  } catch (err) {
    console.error('[Tenants API] Error:', err.message);
    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}

// ===================== CRUD =====================

async function listTenants(env, url) {
  const listJson = await env.KV.get(TENANT_LIST_KEY);
  const ids = listJson ? JSON.parse(listJson) : [];
  const limit = parseInt(url.searchParams.get('limit') || '50');
  const offset = parseInt(url.searchParams.get('offset') || '0');

  const tenants = [];
  for (const id of ids.slice(offset, offset + limit)) {
    const meta = await env.KV.get(`${TENANT_META_PREFIX}${id}`);
    if (meta) tenants.push(JSON.parse(meta));
  }
  return { ok: true, data: tenants, total: ids.length };
}

async function getTenant(env, tenantId) {
  const meta = await env.KV.get(`${TENANT_META_PREFIX}${tenantId}`);
  return meta ? JSON.parse(meta) : null;
}

async function createTenant(env, body) {
  const { name, email, plan = 'free' } = body;
  if (!name || !email) return { error: 'name 和 email 为必填项' };

  const tenantId = `tenant_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const meta = {
    id: tenantId, name, email, plan, status: 'active',
    createdAt: new Date().toISOString(), createdBy: 'superadmin',
    quotas: { kv_ops: 10000, storage: 10485760, api_calls: 1000 },
  };

  await env.KV.put(`${TENANT_META_PREFIX}${tenantId}`, JSON.stringify(meta));

  const listJson = await env.KV.get(TENANT_LIST_KEY);
  const ids = listJson ? JSON.parse(listJson) : [];
  ids.push(tenantId);
  await env.KV.put(TENANT_LIST_KEY, JSON.stringify(ids));

  return { ok: true, data: meta };
}

async function updateTenant(env, tenantId, body) {
  const existing = await env.KV.get(`${TENANT_META_PREFIX}${tenantId}`);
  if (!existing) return { error: 'Tenant not found' };

  const meta = JSON.parse(existing);
  if (body.name) meta.name = body.name;
  if (body.plan) meta.plan = body.plan;
  if (body.quotas) meta.quotas = { ...meta.quotas, ...body.quotas };
  meta.updatedAt = new Date().toISOString();

  await env.KV.put(`${TENANT_META_PREFIX}${tenantId}`, JSON.stringify(meta));
  return { ok: true, data: meta };
}

async function deleteTenant(env, tenantId) {
  await env.KV.delete(`${TENANT_META_PREFIX}${tenantId}`);
  const listJson = await env.KV.get(TENANT_LIST_KEY);
  if (listJson) {
    const ids = JSON.parse(listJson).filter(id => id !== tenantId);
    await env.KV.put(TENANT_LIST_KEY, JSON.stringify(ids));
  }
  return { ok: true, message: `Tenant ${tenantId} deleted` };
}

async function inviteTenantAdmin(env, tenantId, body) {
  const { email } = body;
  if (!email) return { error: 'email 为必填项' };
  const existing = await env.KV.get(`${TENANT_META_PREFIX}${tenantId}`);
  if (!existing) return { error: 'Tenant not found' };

  const inviteCode = `invite_${tenantId}_${Math.random().toString(36).slice(2, 12)}`;
  await env.KV.put(
    `tenant:invite:${inviteCode}`,
    JSON.stringify({ tenantId, email, role: 'tenant_admin', createdAt: new Date().toISOString() }),
    { expirationTtl: 86400 * 7 }
  );

  return { ok: true, message: `Invitation sent to ${email}`, inviteCode };
}

async function updateTenantStatus(env, tenantId, body) {
  if (!['active', 'suspended'].includes(body.status)) {
    return { error: 'status 必须为 active 或 suspended' };
  }
  const existing = await env.KV.get(`${TENANT_META_PREFIX}${tenantId}`);
  if (!existing) return { error: 'Tenant not found' };

  const meta = JSON.parse(existing);
  meta.status = body.status;
  meta.updatedAt = new Date().toISOString();
  await env.KV.put(`${TENANT_META_PREFIX}${tenantId}`, JSON.stringify(meta));
  return { ok: true, data: { id: tenantId, status: body.status } };
}
