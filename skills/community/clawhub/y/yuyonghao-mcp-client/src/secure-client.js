// MCP Client 安全控制增强版
// 包含权限验证、敏感操作确认、审计日志

import { MCPClient, MCPClientConfig, MCPServerConfig, MCPError } from './client.js';

/**
 * MCP 安全控制器
 * 负责权限验证、敏感操作确认、审计日志
 */
export class MCPSecurityController {
  constructor(options = {}) {
    this.requireApproval = options.requireApproval ?? true;
    this.autoApprovePatterns = options.autoApprovePatterns || [];
    this.blockedPatterns = options.blockedPatterns || [];
    this.auditLog = [];
    this.approvedTools = new Map();
    this.approvedResources = new Map();
  }

  /**
   * 检查工具调用是否需要批准
   */
  shouldRequireApproval(serverId, toolName, args) {
    const toolKey = `${serverId}:${toolName}`;
    
    if (this.approvedTools.has(toolKey)) {
      return false;
    }

    for (const pattern of this.autoApprovePatterns) {
      if (this.matchesPattern(toolKey, pattern)) {
        return false;
      }
    }

    for (const pattern of this.blockedPatterns) {
      if (this.matchesPattern(toolKey, pattern)) {
        throw new Error(`工具被禁止：${toolKey}`);
      }
    }

    return this.requireApproval;
  }

  /**
   * 批准工具
   */
  approveTool(serverId, toolName, permanent = false) {
    const toolKey = `${serverId}:${toolName}`;
    this.approvedTools.set(toolKey, {
      approvedAt: new Date(),
      permanent
    });
    this.log('approve_tool', { serverId, toolName, permanent });
  }

  /**
   * 检查资源访问权限
   */
  checkResourceAccess(serverId, resourceUri) {
    const resourceKey = `${serverId}:${resourceUri}`;
    
    if (this.approvedResources.has(resourceKey)) {
      return true;
    }

    if (this.isSensitivePath(resourceUri)) {
      throw new Error(`敏感资源访问需要特别授权：${resourceUri}`);
    }

    return this.requireApproval;
  }

  /**
   * 检查路径是否敏感
   */
  isSensitivePath(path) {
    const sensitivePatterns = [
      /\/\./,
      /\/etc\//,
      /\/passwd/,
      /\/shadow/,
      /\.env$/,
      /\.git\//,
    ];

    return sensitivePatterns.some(pattern => pattern.test(path));
  }

  /**
   * 模式匹配
   */
  matchesPattern(str, pattern) {
    if (pattern instanceof RegExp) {
      return pattern.test(str);
    }
    const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
    return regex.test(str);
  }

  /**
   * 记录审计日志
   */
  log(action, details) {
    this.auditLog.push({
      timestamp: new Date(),
      action,
      details
    });
    
    if (this.auditLog.length > 1000) {
      this.auditLog.shift();
    }
  }

  /**
   * 获取审计日志
   */
  getAuditLog(limit = 100) {
    return this.auditLog.slice(-limit);
  }
}

/**
 * MCP 错误类型定义
 */
export class MCPClientError extends MCPError {
  constructor(code, message, details = {}) {
    super(message, code, details);
    this.name = 'MCPClientError';
  }
}

/**
 * 错误码定义
 */
export const MCPErrorCode = {
  CONNECTION_FAILED: 'CONNECTION_FAILED',
  CONNECTION_TIMEOUT: 'CONNECTION_TIMEOUT',
  CONNECTION_LOST: 'CONNECTION_LOST',
  AUTHENTICATION_REQUIRED: 'AUTHENTICATION_REQUIRED',
  AUTHENTICATION_FAILED: 'AUTHENTICATION_FAILED',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
  TOOL_NOT_FOUND: 'TOOL_NOT_FOUND',
  TOOL_EXECUTION_FAILED: 'TOOL_EXECUTION_FAILED',
  TOOL_APPROVAL_REQUIRED: 'TOOL_APPROVAL_REQUIRED',
  RESOURCE_NOT_FOUND: 'RESOURCE_NOT_FOUND',
  RESOURCE_ACCESS_DENIED: 'RESOURCE_ACCESS_DENIED',
  RESOURCE_READ_FAILED: 'RESOURCE_READ_FAILED',
  PROTOCOL_ERROR: 'PROTOCOL_ERROR',
  INVALID_REQUEST: 'INVALID_REQUEST',
  SERVER_ERROR: 'SERVER_ERROR',
  TIMEOUT: 'TIMEOUT',
  UNKNOWN: 'UNKNOWN'
};

/**
 * 增强的 MCP 客户端（带错误处理和安全控制）
 */
export class SecureMCPClient extends MCPClient {
  constructor(config = new MCPClientConfig(), securityOptions = {}) {
    super(config);
    this.security = new MCPSecurityController(securityOptions);
    this.retryConfig = {
      maxRetries: 3,
      baseDelay: 1000,
      maxDelay: 10000,
    };
  }

  /**
   * 连接到 MCP 服务器（带错误处理）
   */
  async connect(serverConfig) {
    try {
      console.log(`[MCP] 正在连接到服务器：${serverConfig.name} (${serverConfig.id})`);
      
      const result = await super.connect(serverConfig);
      
      this.security.log('connect', {
        serverId: serverConfig.id,
        serverName: serverConfig.name,
        success: true
      });
      
      return result;
    } catch (error) {
      const mcpError = new MCPClientError(
        MCPErrorCode.CONNECTION_FAILED,
        `连接失败：${serverConfig.name}`,
        { serverConfig, originalError: error.message }
      );
      
      this.security.log('connect', {
        serverId: serverConfig.id,
        success: false,
        error: error.message
      });
      
      throw mcpError;
    }
  }

  /**
   * 调用工具（带安全检查和重试）
   */
  async callTool(serverId, toolName, args, requireApproval = true) {
    try {
      if (this.security.shouldRequireApproval(serverId, toolName, args)) {
        console.warn(`[MCP] 工具调用需要批准：${serverId}:${toolName}`);
      }
    } catch (error) {
      throw new MCPClientError(
        MCPErrorCode.PERMISSION_DENIED,
        error.message,
        { serverId, toolName }
      );
    }

    return this.withRetry(
      async () => super.callTool(serverId, toolName, args, false),
      MCPErrorCode.TOOL_EXECUTION_FAILED,
      `工具执行失败：${toolName}`
    );
  }

  /**
   * 读取资源（带安全检查）
   */
  async readResource(serverId, resourceUri, requireApproval = true) {
    try {
      if (this.security.checkResourceAccess(serverId, resourceUri)) {
        console.warn(`[MCP] 资源访问需要批准：${resourceUri}`);
      }
    } catch (error) {
      throw new MCPClientError(
        MCPErrorCode.RESOURCE_ACCESS_DENIED,
        error.message,
        { serverId, resourceUri }
      );
    }

    return this.withRetry(
      async () => super.readResource(serverId, resourceUri, false),
      MCPErrorCode.RESOURCE_READ_FAILED,
      `资源读取失败：${resourceUri}`
    );
  }

  /**
   * 带重试的执行
   */
  async withRetry(fn, errorCode, errorMessage) {
    let lastError;
    
    for (let attempt = 0; attempt < this.retryConfig.maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        
        if (error instanceof MCPClientError) {
          throw error;
        }
        
        if (attempt < this.retryConfig.maxRetries - 1) {
          const delay = Math.min(
            this.retryConfig.baseDelay * Math.pow(2, attempt),
            this.retryConfig.maxDelay
          );
          
          console.warn(`[MCP] 尝试 ${attempt + 1}/${this.retryConfig.maxRetries} 失败，${delay}ms 后重试...`);
          await this.sleep(delay);
        }
      }
    }
    
    throw new MCPClientError(
      errorCode,
      errorMessage,
      { originalError: lastError?.message, attempts: this.retryConfig.maxRetries }
    );
  }

  /**
   * 睡眠工具
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 批准工具
   */
  approveTool(serverId, toolName, permanent = false) {
    this.security.approveTool(serverId, toolName, permanent);
    super.approveTool(serverId, toolName);
  }

  /**
   * 获取审计日志
   */
  getAuditLog(limit = 100) {
    return this.security.getAuditLog(limit);
  }

  /**
   * 获取错误统计
   */
  getErrorStats() {
    const logs = this.security.getAuditLog(1000);
    const errors = logs.filter(log => log.details.error);
    
    return {
      total: logs.length,
      errors: errors.length,
      errorRate: logs.length > 0 ? errors.length / logs.length : 0,
      recentErrors: errors.slice(-10)
    };
  }
}

// 导出默认实例
export const secureMcpClient = new SecureMCPClient();
