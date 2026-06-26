/**
 * 共享常量 — 角色定义 + 权限矩阵
 *
 * Phase 4A W3 实现：
 * - 三层角色模型（架构专家 C3/O4 修正）
 * - action-based 权限矩阵（非 flat role 检查）
 * - checkPermission() 运行时权限校验
 *
 * 使用方式：
 *   import { ROLES, checkPermission } from '../sharing/constants.js';
 *
 *   if (!checkPermission(user.role, 'order:create')) {
 *     return new Response('Forbidden', { status: 403 });
 *   }
 */

// ===================== 角色定义 =====================

export const ROLES = {
  SUPERADMIN: 'superadmin',     // 平台管理员（跨租户，全权限）
  TENANT_ADMIN: 'tenant_admin', // 租户管理员（本租户内管理）
  USER: 'user',                 // 普通用户（本租户内个人数据）
};

export const ROLE_HIERARCHY = {
  superadmin: 100,
  tenant_admin: 50,
  user: 10,
  guest: 0,
};

// ===================== 权限矩阵 =====================

/**
 * action-based 权限定义
 * key = permission name, value = 允许的角色列表
 */
export const PERMISSIONS = {
  // === superadmin 独有 ===
  'tenant:list':      ['superadmin'],
  'tenant:create':    ['superadmin'],
  'tenant:delete':    ['superadmin'],
  'tenant:update':    ['superadmin'],
  'tenant:invite':    ['superadmin'],
  'quota:set':        ['superadmin'],
  'data:cross-tenant-view': ['superadmin'],
  'audit:view':       ['superadmin'],

  // === 租户内管理（superadmin + tenant_admin） ===
  'user:manage':      ['superadmin', 'tenant_admin'],
  'user:list':        ['superadmin', 'tenant_admin'],
  'user:role:change': ['superadmin', 'tenant_admin'],

  // === 本租户数据操作（所有角色） ===
  'order:read':       ['superadmin', 'tenant_admin', 'user'],
  'order:create':     ['superadmin', 'tenant_admin', 'user'],
  'order:cancel':     ['superadmin', 'tenant_admin'],
  'product:read':     ['superadmin', 'tenant_admin', 'user'],
  'product:manage':   ['superadmin', 'tenant_admin'],
  'cart:read':        ['superadmin', 'tenant_admin', 'user'],
  'cart:write':       ['superadmin', 'tenant_admin', 'user'],
};

// ===================== 工具函数 =====================

/**
 * 检查角色是否拥有指定权限
 * @param {string} role - 用户角色
 * @param {string} permission - 权限名（见 PERMISSIONS）
 * @returns {boolean} 是否有权限
 */
export function checkPermission(role, permission) {
  const allowedRoles = PERMISSIONS[permission];
  if (!allowedRoles) return false; // 未知权限，默认拒绝
  return allowedRoles.includes(role);
}

/**
 * 检查角色是否至少达到指定级别
 * @param {string} role - 用户角色
 * @param {string} minRole - 最低角色要求
 * @returns {boolean}
 */
export function hasMinRole(role, minRole) {
  const userLevel = ROLE_HIERARCHY[role] ?? 0;
  const minLevel = ROLE_HIERARCHY[minRole] ?? 0;
  return userLevel >= minLevel;
}

/**
 * 判断角色是否为 superadmin
 */
export function isSuperadmin(role) {
  return role === ROLES.SUPERADMIN;
}

/**
 * 判断角色是否为租户管理员或以上
 */
export function isAdmin(role) {
  return hasMinRole(role, ROLES.TENANT_ADMIN);
}
