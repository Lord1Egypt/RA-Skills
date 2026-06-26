/**
 * Security Guard - 权限管理系统
 * 细粒度权限控制
 */

import { EventEmitter } from 'events';

/**
 * 权限管理器
 */
export class PermissionManager extends EventEmitter {
  constructor(config = {}) {
    super();
    this.roles = new Map();
    this.permissions = new Map();
    this.userRoles = new Map();
    
    // 默认角色
    this.defineRole('admin', {
      permissions: ['*'],
      description: 'Full access'
    });
    
    this.defineRole('user', {
      permissions: [
        'file:read',
        'file:write:home',
        'web:read',
        'exec:safe',
        'memory:read',
        'memory:write'
      ],
      description: 'Standard user'
    });
    
    this.defineRole('restricted', {
      permissions: [
        'file:read:home',
        'memory:read'
      ],
      description: 'Restricted access'
    });
  }

  /**
   * 定义角色
   */
  defineRole(roleName, config) {
    this.roles.set(roleName, {
      name: roleName,
      permissions: config.permissions || [],
      description: config.description || ''
    });
  }

  /**
   * 为用户分配角色
   */
  assignRole(userId, roleName) {
    if (!this.roles.has(roleName)) {
      throw new Error(`Role ${roleName} not found`);
    }
    
    this.userRoles.set(userId, roleName);
    this.emit('role-assigned', { userId, roleName });
  }

  /**
   * 检查权限
   */
  checkPermission(userId, action, resource) {
    const roleName = this.userRoles.get(userId) || 'restricted';
    const role = this.roles.get(roleName);
    
    if (!role) {
      return { allowed: false, reason: 'No role assigned' };
    }

    // 管理员权限
    if (role.permissions.includes('*')) {
      return { allowed: true };
    }

    // 构建权限字符串
    const permissionString = `${action}:${resource}`;
    const actionWildcard = `${action}:*`;

    // 检查具体权限
    if (role.permissions.includes(permissionString)) {
      return { allowed: true };
    }

    // 检查通配权限
    if (role.permissions.includes(actionWildcard)) {
      return { allowed: true };
    }

    // 检查父级权限
    const resourceParts = resource.split(':');
    for (let i = resourceParts.length - 1; i > 0; i--) {
      const parentResource = resourceParts.slice(0, i).join(':');
      const parentPermission = `${action}:${parentResource}`;
      if (role.permissions.includes(parentPermission)) {
        return { allowed: true };
      }
    }

    return { 
      allowed: false, 
      reason: `Permission denied: ${permissionString}`,
      required: permissionString,
      currentRole: roleName
    };
  }

  /**
   * 要求确认（高风险操作）
   */
  async requireConfirmation(action, resource, reason = '') {
    return new Promise((resolve) => {
      this.emit('confirmation-required', {
        action,
        resource,
        reason,
        resolve
      });
    });
  }

  /**
   * 添加自定义权限
   */
  addPermission(userId, permission) {
    const roleName = this.userRoles.get(userId);
    if (!roleName) return false;
    
    const role = this.roles.get(roleName);
    if (!role.permissions.includes(permission)) {
      role.permissions.push(permission);
    }
    return true;
  }

  /**
   * 移除权限
   */
  removePermission(userId, permission) {
    const roleName = this.userRoles.get(userId);
    if (!roleName) return false;
    
    const role = this.roles.get(roleName);
    role.permissions = role.permissions.filter(p => p !== permission);
    return true;
  }

  /**
   * 获取用户权限列表
   */
  getUserPermissions(userId) {
    const roleName = this.userRoles.get(userId);
    if (!roleName) return [];
    
    const role = this.roles.get(roleName);
    return role.permissions;
  }

  /**
   * 检查是否为高风险操作
   */
  isHighRiskAction(action, resource) {
    const highRiskPatterns = [
      { action: 'file', resource: 'delete', level: 'high' },
      { action: 'file', resource: 'system', level: 'high' },
      { action: 'exec', resource: '*', level: 'high' },
      { action: 'web', resource: 'post', level: 'medium' },
      { action: 'memory', resource: 'delete', level: 'medium' }
    ];

    for (const pattern of highRiskPatterns) {
      if (action === pattern.action) {
        if (pattern.resource === '*' || resource.includes(pattern.resource)) {
          return pattern.level;
        }
      }
    }

    return 'low';
  }
}

export default PermissionManager;
