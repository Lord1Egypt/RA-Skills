/**
 * HITL (Human-in-the-Loop) 支持 - 人工确认机制
 * 
 * 基于 2026 最佳实践：
 * - 关键操作前暂停等待人工确认
 * - 支持自定义确认回调
 * - 超时处理（用户未确认）
 * - 审批历史记录
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

/**
 * HITL 配置
 * @typedef {Object} HITLConfig
 * @property {boolean} enabled - 是否启用 HITL
 * @property {string[]} requireApproval - 需要确认的工具列表
 * @property {Function} onApprovalRequired - 确认回调
 * @property {number} timeout - 超时时间（毫秒）
 * @property {Function} onTimeout - 超时回调
 */

/**
 * 审批请求
 * @typedef {Object} ApprovalRequest
 * @property {string} id - 请求 ID
 * @property {string} toolName - 工具名称
 * @property {Object} params - 工具参数
 * @property {string} reason - 请求原因
 * @property {Date} createdAt - 创建时间
 * @property {'pending'|'approved'|'rejected'} status - 状态
 * @property {Date|null} respondedAt - 响应时间
 */

class HITLManager {
  constructor(options = {}) {
    this.options = {
      // 默认配置
      enabled: options.enabled !== false,
      requireApproval: options.requireApproval || [],
      onApprovalRequired: options.onApprovalRequired || null,
      timeout: options.timeout || 300000, // 5 分钟
      onTimeout: options.onTimeout || null,
      // 自动批准模式（白名单）
      autoApprove: options.autoApprove || [],
      // 日志
      verbose: options.verbose || false,
    };

    // 审批请求存储
    this.pendingRequests = new Map();
    this.approvalHistory = [];
    
    // 事件监听器
    this.eventListeners = new Map();

    this.log('HITL Manager 初始化完成');
  }

  /**
   * 日志
   */
  log(...args) {
    if (this.options.verbose) {
      console.log('[HITL]', ...args);
    }
  }

  /**
   * 注册事件监听器
   * @param {string} event - 事件名称
   * @param {Function} listener - 监听器函数
   */
  on(event, listener) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(listener);
  }

  /**
   * 触发事件
   * @param {string} event - 事件名称
   * @param {any} data - 事件数据
   */
  emit(event, data) {
    const listeners = this.eventListeners.get(event) || [];
    listeners.forEach(listener => {
      try {
        listener(data);
      } catch (error) {
        console.error(`[HITL] 事件监听器错误 (${event}):`, error);
      }
    });
  }

  /**
   * 检查工具调用是否需要审批
   * @param {string} toolName - 工具名称
   * @returns {boolean}
   */
  requiresApproval(toolName) {
    if (!this.options.enabled) return false;
    
    // 白名单：自动批准
    if (this.options.autoApprove.includes(toolName)) {
      this.log(`✅ 自动批准：${toolName} (白名单)`);
      return false;
    }

    // 检查是否需要审批
    const needsApproval = this.options.requireApproval.includes(toolName);
    this.log(`${needsApproval ? '⚠️' : '✅'} ${toolName} ${needsApproval ? '需要审批' : '不需要审批'}`);
    return needsApproval;
  }

  /**
   * 创建审批请求
   * @param {string} toolName - 工具名称
   * @param {Object} params - 工具参数
   * @param {string} reason - 请求原因
   * @returns {Promise<{approved: boolean, request: ApprovalRequest}>}
   */
  async createApprovalRequest(toolName, params, reason = '') {
    const requestId = `approval-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const request = {
      id: requestId,
      toolName,
      params,
      reason,
      createdAt: new Date(),
      status: 'pending',
      respondedAt: null,
      timeoutId: null,
      _resolve: null, // Promise resolver
    };

    // 创建 Promise
    const promise = new Promise((resolve) => {
      request._resolve = resolve;
    });

    // 存储请求
    this.pendingRequests.set(requestId, request);

    // 设置超时
    request.timeoutId = setTimeout(() => {
      this.handleTimeout(requestId);
    }, this.options.timeout);

    this.log(`⏳ 创建审批请求：${requestId} (${toolName})`);
    this.emit('approval-request', request);

    // 调用确认回调（如果有）
    if (this.options.onApprovalRequired) {
      try {
        const approved = await this.options.onApprovalRequired(request);
        if (approved !== undefined) {
          // 异步响应，不阻塞
          this.respond(requestId, approved).catch(console.error);
        }
      } catch (error) {
        this.log(`❌ 确认回调错误：${error.message}`);
        this.respond(requestId, false, `回调错误：${error.message}`).catch(console.error);
      }
    }

    // 返回 Promise
    return promise;
  }

  /**
   * 响应审批请求
   * @param {string} requestId - 请求 ID
   * @param {boolean} approved - 是否批准
   * @param {string} reason - 原因（可选）
   */
  async respond(requestId, approved, reason = '') {
    const request = this.pendingRequests.get(requestId);
    
    if (!request) {
      this.log(`❌ 请求不存在：${requestId}`);
      return { success: false, error: '请求不存在' };
    }

    if (request.status !== 'pending') {
      this.log(`⚠️ 请求已响应：${requestId} (${request.status})`);
      return { success: false, error: '请求已响应' };
    }

    // 清除超时
    if (request.timeoutId) {
      clearTimeout(request.timeoutId);
    }

    // 更新状态
    request.status = approved ? 'approved' : 'rejected';
    request.respondedAt = new Date();
    request.responseReason = reason;

    // 移动到历史记录
    this.pendingRequests.delete(requestId);
    this.approvalHistory.push(request);

    this.log(`${approved ? '✅ 批准' : '❌ 拒绝'}: ${requestId} (${reason || '无原因'})`);
    this.emit('approval-response', request);

    // 解析 Promise
    if (request._resolve) {
      request._resolve({ approved, request });
    }

    return { success: true, approved, request };
  }

  /**
   * 批准请求
   */
  async approve(requestId, reason = '') {
    return this.respond(requestId, true, reason);
  }

  /**
   * 拒绝请求
   */
  async reject(requestId, reason = '') {
    return this.respond(requestId, false, reason);
  }

  /**
   * 处理超时
   */
  async handleTimeout(requestId) {
    const request = this.pendingRequests.get(requestId);
    
    if (!request || request.status !== 'pending') {
      return;
    }

    this.log(`⏰ 审批超时：${requestId}`);
    this.emit('approval-timeout', request);

    // 调用超时回调
    if (this.options.onTimeout) {
      try {
        const action = await this.options.onTimeout(request);
        if (action === 'approve') {
          await this.approve(requestId, '超时自动批准');
        } else if (action === 'reject') {
          await this.reject(requestId, '超时自动拒绝');
        } else {
          // 保持等待
          this.log('⏳ 超时回调选择继续等待');
        }
      } catch (error) {
        this.log(`❌ 超时回调错误：${error.message}`);
        await this.reject(requestId, `超时回调错误：${error.message}`);
      }
    } else {
      // 默认：超时自动拒绝
      await this.reject(requestId, '超时未响应');
    }
  }

  /**
   * 获取待审批请求列表
   * @returns {ApprovalRequest[]}
   */
  getPendingRequests() {
    return Array.from(this.pendingRequests.values());
  }

  /**
   * 获取审批历史
   * @param {number} limit - 限制数量
   * @returns {ApprovalRequest[]}
   */
  getHistory(limit = 50) {
    return this.approvalHistory.slice(-limit);
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.approvalHistory.length;
    const approved = this.approvalHistory.filter(r => r.status === 'approved').length;
    const rejected = this.approvalHistory.filter(r => r.status === 'rejected').length;
    const pending = this.pendingRequests.size;

    return {
      total,
      approved,
      rejected,
      pending,
      approvalRate: total > 0 ? ((approved / total) * 100).toFixed(1) : 0,
      averageResponseTime: this._calculateAverageResponseTime(),
    };
  }

  /**
   * 计算平均响应时间
   */
  _calculateAverageResponseTime() {
    const responded = this.approvalHistory.filter(r => r.respondedAt);
    if (responded.length === 0) return 0;

    const total = responded.reduce((sum, r) => {
      return sum + (r.respondedAt - r.createdAt);
    }, 0);

    return Math.round(total / responded.length);
  }

  /**
   * 清除历史记录
   * @param {number} olderThan - 清除早于此时间（毫秒）的记录
   */
  clearHistory(olderThan = 3600000) {
    const now = Date.now();
    const initialCount = this.approvalHistory.length;
    
    this.approvalHistory = this.approvalHistory.filter(r => {
      const age = now - r.createdAt.getTime();
      return age < olderThan;
    });

    const removed = initialCount - this.approvalHistory.length;
    this.log(`🗑️ 清除 ${removed} 条历史记录`);
    
    return removed;
  }

  /**
   * 更新配置
   */
  updateConfig(newConfig) {
    this.options = { ...this.options, ...newConfig };
    this.log('📝 配置已更新');
    
    if (newConfig.enabled === false) {
      this.log('⏸️ HITL 已禁用，所有请求将自动批准');
    } else if (newConfig.enabled === true) {
      this.log('▶️ HITL 已启用');
    }
  }

  /**
   * 导出配置
   */
  exportConfig() {
    return {
      enabled: this.options.enabled,
      requireApproval: this.options.requireApproval,
      autoApprove: this.options.autoApprove,
      timeout: this.options.timeout,
      verbose: this.options.verbose,
    };
  }

  /**
   * 重置状态
   */
  reset() {
    // 清除所有待处理请求
    for (const [id, request] of this.pendingRequests) {
      if (request.timeoutId) {
        clearTimeout(request.timeoutId);
      }
    }
    this.pendingRequests.clear();
    this.approvalHistory = [];
    this.log('🔄 HITL Manager 已重置');
  }
}

/**
 * 简化的 HITL 辅助函数
 */
class HITLHelper {
  /**
   * 创建简单的确认对话框（命令行）
   */
  static async createConfirmationDialog(request) {
    console.log('\n⚠️ 需要您的确认\n');
    console.log(`工具：${request.toolName}`);
    console.log(`参数：${JSON.stringify(request.params, null, 2)}`);
    if (request.reason) {
      console.log(`原因：${request.reason}`);
    }
    console.log('\n是否继续？(yes/no): ');

    return new Promise((resolve) => {
      const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout,
      });

      readline.question('> ', (answer) => {
        readline.close();
        const approved = answer.toLowerCase().startsWith('y');
        resolve(approved);
      });
    });
  }

  /**
   * 创建 Web 界面确认（伪代码，需配合前端）
   */
  static createWebInterface(hidlManager, port = 3000) {
    // 需要 express 等 Web 框架
    // 这是一个示例，展示如何集成 Web 界面
    console.log(`Web 界面将在 http://localhost:${port} 启动`);
    console.log('功能：查看待审批请求、批准/拒绝、历史记录');
    
    // 实际实现需要：
    // 1. Express 服务器
    // 2. WebSocket 实时更新
    // 3. 前端页面（React/Vue）
  }
}

// 导出
module.exports = {
  HITLManager,
  HITLHelper,
};
