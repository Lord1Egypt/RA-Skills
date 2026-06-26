/**
 * Security Guard - 统一安全守护入口
 * 整合权限管理、内容审查、审计日志
 */

import PermissionManager from './permission-manager.js';
import ContentSafety from './content-safety.js';
import AuditLogger from './audit-logger.js';
import { EventEmitter } from 'events';

/**
 * 安全守护器
 */
export class SecurityGuard extends EventEmitter {
  constructor(config = {}) {
    super();
    
    this.permissionManager = new PermissionManager(config.permissions);
    this.contentSafety = new ContentSafety(config.contentSafety);
    this.auditLogger = new AuditLogger(config.audit);
    
    this.enabled = config.enabled !== false;
    this.strictMode = config.strictMode || false;
  }

  /**
   * 执行安全检查（完整流程）
   */
  async check(userId, action, resource, content = '') {
    if (!this.enabled) {
      return { allowed: true };
    }

    const startTime = Date.now();
    const result = {
      allowed: false,
      userId,
      action,
      resource,
      checks: {}
    };

    try {
      // 1. 权限检查
      result.checks.permission = this.permissionManager.checkPermission(
        userId, action, resource
      );
      
      if (!result.checks.permission.allowed) {
        result.reason = result.checks.permission.reason;
        await this.auditLogger.logPermissionCheck(userId, action, resource, false);
        return result;
      }

      // 2. 内容安全检查
      if (content) {
        result.checks.content = this.contentSafety.checkInput(content);
        
        if (!result.checks.content.safe) {
          result.reason = 'Content safety check failed';
          result.warnings = result.checks.content.warnings;
          await this.auditLogger.logSecurity({
            type: 'unsafe_content',
            severity: 'high',
            description: 'Content failed safety check',
            details: result.checks.content.warnings
          });
          return result;
        }
      }

      // 3. 高风险操作确认
      const riskLevel = this.permissionManager.isHighRiskAction(action, resource);
      if (riskLevel === 'high') {
        result.checks.riskLevel = riskLevel;
        result.requiresConfirmation = true;
        
        await this.auditLogger.logHighRisk({
          userId,
          action,
          resource,
          details: { riskLevel }
        });
      }

      // 4. 记录审计日志
      await this.auditLogger.log({
        userId,
        action,
        resource,
        status: 'success',
        duration: Date.now() - startTime
      });

      result.allowed = true;
      return result;

    } catch (error) {
      result.error = error.message;
      this.emit('check-error', { userId, action, resource, error });
      return result;
    }
  }

  /**
   * 验证确认（高风险操作）
   */
  async confirm(userId, action, resource, confirmed) {
    if (confirmed) {
      await this.auditLogger.log({
        userId,
        action,
        resource,
        status: 'confirmed',
        details: { confirmed: true }
      });
      return { allowed: true };
    } else {
      await this.auditLogger.log({
        userId,
        action,
        resource,
        status: 'denied',
        details: { confirmed: false, reason: 'User rejected' }
      });
      return { allowed: false, reason: 'Operation rejected by user' };
    }
  }

  /**
   * 包装函数执行
   */
  async wrap(userId, action, resource, fn, content = '') {
    const check = await this.check(userId, action, resource, content);
    
    if (!check.allowed) {
      throw new Error(`Security check failed: ${check.reason}`);
    }

    if (check.requiresConfirmation) {
      // 需要人工确认
      this.emit('confirmation-required', {
        userId,
        action,
        resource,
        resolve: async (confirmed) => {
          const confirmResult = await this.confirm(userId, action, resource, confirmed);
          if (confirmResult.allowed) {
            return await fn();
          } else {
            throw new Error('Operation rejected');
          }
        }
      });
      return;
    }

    return await fn();
  }

  /**
   * 生成安全报告
   */
  async generateReport(timeRange = '24h') {
    const auditReport = await this.auditLogger.generateReport(timeRange);
    
    return {
      timeRange,
      generatedAt: new Date().toISOString(),
      audit: auditReport,
      permissions: {
        totalRoles: this.permissionManager.roles.size,
        totalUsers: this.permissionManager.userRoles.size
      },
      contentSafety: {
        sensitiveWords: this.contentSafety.sensitiveWords.length,
        dangerousPatterns: this.contentSafety.dangerousPatterns.length
      }
    };
  }

  /**
   * 关闭安全守护
   */
  async close() {
    await this.auditLogger.close();
  }
}

export { PermissionManager, ContentSafety, AuditLogger };
export default SecurityGuard;
