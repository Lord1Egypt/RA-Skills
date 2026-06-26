/**
 * @website-skeleton/admin — 租户管理模块入口
 *
 * Cloud Functions 管理后台工具函数。
 *
 * 使用方式（Cloud Functions handler 中）：
 *   import { createTenant, listTenants } from '@website-skeleton/admin';
 *   import { checkPermission } from '@website-skeleton/shared';
 *
 *   export async function onRequest(request, env) {
 *     // 权限检查
 *     if (!checkPermission(role, 'tenant:list')) {
 *       return new Response('Forbidden', { status: 403 });
 *     }
 *     return listTenants(env, url);
 *   }
 */

export {
  listTenants, getTenant, createTenant,
  updateTenant, deleteTenant,
  inviteTenantAdmin, updateTenantStatus,
} from '../../edge-functions/api/admin/tenants.js';
