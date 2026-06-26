/**
 * approval-engine.js
 * 
 * 审批流程引擎核心模块
 * 
 * 主要功能：
 * 1. 规则评估与审批创建
 * 2. 审批决策提交与处理
 * 3. 超时检测与自动升级
 * 4. 多级审批支持（serial/parallel）
 * 
 * 依赖模块：
 * - rule-evaluator.js: 规则评估
 * - approval-store.js: 状态存储
 */

const fs = require('fs');
const path = require('path');
const store = require('./approval-store');
const evaluator = require('./rule-evaluator');

// 日志文件路径
const LOG_FILE = path.join(__dirname, '..', 'logs', 'approval.log');

/**
 * 写入日志
 * @param {string} level - log/info/warn/error
 * @param {string} message 
 */
function log(level, message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
  
  console.log(logLine.trim());
  
  // 写入日志文件
  try {
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    fs.appendFileSync(LOG_FILE, logLine);
  } catch (error) {
    console.error(`[ApprovalEngine] Failed to write log: ${error.message}`);
  }
}

/**
 * 获取规则配置的审批人级别
 * @param {object} rule - 规则对象
 * @param {number} level - 当前级别
 * @returns {object|null}
 */
function getApproversForLevel(rule, level) {
  if (!rule.approvers || !Array.isArray(rule.approvers)) {
    return null;
  }
  
  return rule.approvers.filter(approver => approver.level === level);
}

/**
 * 获取下一级审批级别
 * @param {object} rule - 规则对象
 * @param {number} currentLevel - 当前级别
 * @returns {number|null} 下一级级别，无更多级别返回 null
 */
function getNextLevel(rule, currentLevel) {
  if (!rule.approvers || !Array.isArray(rule.approvers)) {
    return null;
  }
  
  const levels = [...new Set(rule.approvers.map(a => a.level))].sort((a, b) => a - b);
  const currentIndex = levels.indexOf(currentLevel);
  
  if (currentIndex < levels.length - 1) {
    return levels[currentIndex + 1];
  }
  
  return null;
}

/**
 * 检查当前级别审批是否完成
 * @param {object} approval - 审批记录
 * @param {object} rule - 规则对象
 * @returns {boolean}
 */
function isLevelComplete(approval, rule) {
  const currentApprovers = getApproversForLevel(rule, approval.current_level);
  
  if (!currentApprovers || currentApprovers.length === 0) {
    return true;
  }
  
  // 并行审批：需要所有审批人都同意
  if (rule.approval_type === 'parallel') {
    const levelDecisions = approval.decisions.filter(d => d.level === approval.current_level);
    const uniqueApprovers = new Set(levelDecisions.map(d => d.approver_id));
    const requiredApprovers = new Set(currentApprovers.map(a => a.user_ids).flat());
    
    // 检查是否所有审批人都已决策
    for (const approverId of requiredApprovers) {
      if (!uniqueApprovers.has(approverId)) {
        return false;
      }
    }
    
    // 检查是否有拒绝
    const hasRejection = levelDecisions.some(d => d.decision === 'reject');
    if (hasRejection) {
      return true; // 有拒绝则级别完成（结果是拒绝）
    }
    
    return true; // 所有人都同意
  }
  
  // 串行审批：只需要当前级别的任意一个审批人同意
  if (rule.approval_type === 'serial') {
    const levelDecisions = approval.decisions.filter(d => d.level === approval.current_level);
    return levelDecisions.length > 0;
  }
  
  // 默认按串行处理
  const levelDecisions = approval.decisions.filter(d => d.level === approval.current_level);
  return levelDecisions.length > 0;
}

/**
 * 检查当前级别审批结果
 * @param {object} approval - 审批记录
 * @param {object} rule - 规则对象
 * @returns {string|null} 'approved' / 'rejected' / null (未完成)
 */
function getLevelResult(approval, rule) {
  const levelDecisions = approval.decisions.filter(d => d.level === approval.current_level);
  
  if (levelDecisions.length === 0) {
    return null;
  }
  
  // 并行审批：任一拒绝则拒绝，全部同意则通过
  if (rule.approval_type === 'parallel') {
    if (levelDecisions.some(d => d.decision === 'reject')) {
      return 'rejected';
    }
    return 'approved';
  }
  
  // 串行审批：看最后一个决策
  const lastDecision = levelDecisions[levelDecisions.length - 1];
  return lastDecision.decision;
}

/**
 * 创建审批实例
 * @param {string} ruleId - 规则 ID
 * @param {object} context - 触发上下文
 * @returns {object|null} 创建的审批记录或 null
 */
function createApproval(ruleId, context) {
  log('info', `Creating approval for rule: ${ruleId}`);
  
  const rule = evaluator.getRule(ruleId);
  if (!rule) {
    log('error', `Rule not found: ${ruleId}`);
    return null;
  }
  
  if (!rule.enabled) {
    log('warn', `Rule is disabled: ${ruleId}`);
    return null;
  }
  
  // 验证触发条件
  const config = evaluator.loadConfig();
  const triggerMatched = evaluator.evaluateTrigger(rule.trigger, context, config);
  const conditionsMatched = evaluator.evaluateConditions(rule.conditions, context);
  
  if (!triggerMatched || !conditionsMatched) {
    log('warn', `Rule conditions not met: ${ruleId}`);
    return null;
  }
  
  // 创建审批记录
  const approval = store.createApproval(ruleId, context, rule.timeout_hours);
  
  log('info', `Approval created: ${approval.id} (rule: ${ruleId}, timeout: ${rule.timeout_hours}h)`);
  
  return approval;
}

/**
 * 提交审批决策
 * @param {string} approvalId - 审批 ID
 * @param {string} approverId - 审批人 ID
 * @param {string} decision - 决策 (approve/reject)
 * @param {string} comment - 评论
 * @returns {object|null} 更新后的审批记录或 null
 */
function submitApproval(approvalId, approverId, decision, comment = '') {
  log('info', `Submitting approval decision: ${approvalId} by ${approverId} - ${decision}`);
  
  const approval = store.getApproval(approvalId);
  if (!approval) {
    log('error', `Approval not found: ${approvalId}`);
    return null;
  }
  
  if (approval.status !== 'pending') {
    log('warn', `Approval is not pending: ${approvalId} (status: ${approval.status})`);
    return null;
  }
  
  const rule = evaluator.getRule(approval.rule_id);
  if (!rule) {
    log('error', `Rule not found for approval: ${approval.rule_id}`);
    return null;
  }
  
  // 验证审批人是否有权审批当前级别
  const currentApprovers = getApproversForLevel(rule, approval.current_level);
  if (!currentApprovers || currentApprovers.length === 0) {
    log('error', `No approvers found for level ${approval.current_level}`);
    return null;
  }
  
  const authorizedApprovers = currentApprovers.flatMap(a => a.user_ids);
  if (!authorizedApprovers.includes(approverId)) {
    log('warn', `Unauthorized approver: ${approverId} for level ${approval.current_level}`);
    return null;
  }
  
  // 检查是否已决策
  const existingDecision = approval.decisions.find(
    d => d.level === approval.current_level && d.approver_id === approverId
  );
  if (existingDecision) {
    log('warn', `Approver ${approverId} already submitted decision for level ${approval.current_level}`);
    return null;
  }
  
  // 提交决策
  store.submitDecision(approvalId, approverId, approval.current_level, decision, comment);
  
  // 重新获取更新后的审批记录
  const updatedApproval = store.getApproval(approvalId);
  
  // 检查级别结果
  const levelResult = getLevelResult(updatedApproval, rule);
  
  if (levelResult === 'rejected') {
    // 拒绝：审批结束
    store.updateApproval(approvalId, { status: 'rejected' });
    log('info', `Approval rejected: ${approvalId}`);
    return store.getApproval(approvalId);
  }
  
  if (levelResult === 'approved') {
    // 通过：检查是否有下一级
    const nextLevel = getNextLevel(rule, approval.current_level);
    
    if (nextLevel) {
      // 有下一级：升级级别
      store.updateApproval(approvalId, { current_level: nextLevel });
      log('info', `Approval advanced to level ${nextLevel}: ${approvalId}`);
    } else {
      // 无下一级：审批完成
      store.updateApproval(approvalId, { status: 'approved' });
      log('info', `Approval completed: ${approvalId}`);
    }
    
    return store.getApproval(approvalId);
  }
  
  // 级别未完成（并行审批等待其他人）
  log('info', `Level ${approval.current_level} still pending more decisions: ${approvalId}`);
  return updatedApproval;
}

/**
 * 获取审批状态
 * @param {string} approvalId - 审批 ID
 * @returns {object|null}
 */
function getApprovalStatus(approvalId) {
  const approval = store.getApproval(approvalId);
  if (!approval) {
    return null;
  }
  
  const rule = evaluator.getRule(approval.rule_id);
  
  return {
    id: approval.id,
    rule_id: approval.rule_id,
    rule_name: rule?.name || 'Unknown',
    status: approval.status,
    current_level: approval.current_level,
    created_at: approval.created_at,
    updated_at: approval.updated_at,
    timeout_at: approval.timeout_at,
    decisions: approval.decisions,
    context: approval.context
  };
}

/**
 * 检查超时审批并执行超时动作
 * @returns {Array} 处理的超时审批列表
 */
function checkTimeouts() {
  log('info', 'Checking for expired approvals');
  
  const expiredApprovals = store.getExpiredApprovals();
  const processed = [];
  
  for (const approval of expiredApprovals) {
    const rule = evaluator.getRule(approval.rule_id);
    if (!rule) {
      log('error', `Rule not found for expired approval: ${approval.rule_id}`);
      continue;
    }
    
    log('warn', `Approval expired: ${approval.id} (rule: ${rule.id}, timeout_action: ${rule.timeout_action})`);
    
    switch (rule.timeout_action) {
      case 'escalate':
        triggerEscalation(approval.id, 'timeout_expired');
        break;
      case 'auto_reject':
        store.updateApproval(approval.id, { status: 'expired', updated_at: new Date().toISOString() });
        log('info', `Approval auto-rejected due to timeout: ${approval.id}`);
        break;
      case 'notify_admin':
        store.updateApproval(approval.id, { updated_at: new Date().toISOString() });
        log('warn', `Admin notification required for expired approval: ${approval.id}`);
        break;
      default:
        store.updateApproval(approval.id, { status: 'expired', updated_at: new Date().toISOString() });
    }
    
    processed.push(approval.id);
  }
  
  log('info', `Processed ${processed.length} expired approvals`);
  return processed;
}

/**
 * 触发审批升级
 * @param {string} approvalId - 审批 ID
 * @param {string} reason - 升级原因 (timeout_expired / consecutive_rejections / severity_critical)
 * @returns {object|null}
 */
function triggerEscalation(approvalId, reason) {
  log('warn', `Triggering escalation for approval: ${approvalId} (reason: ${reason})`);
  
  const approval = store.getApproval(approvalId);
  if (!approval) {
    log('error', `Approval not found: ${approvalId}`);
    return null;
  }
  
  const rule = evaluator.getRule(approval.rule_id);
  if (!rule) {
    log('error', `Rule not found: ${approval.rule_id}`);
    return null;
  }
  
  // 获取 escalation 规则
  const escalationRules = evaluator.getEscalationRules();
  const escalationRule = escalationRules.find(r => {
    if (reason === 'timeout_expired') return r.trigger === 'timeout_expired';
    if (reason === 'consecutive_rejections') return r.trigger === 'consecutive_rejections';
    if (reason === 'severity_critical') return r.trigger === 'severity_critical';
    return false;
  });
  
  // 升级到下一级或管理员
  const nextLevel = getNextLevel(rule, approval.current_level);
  
  if (nextLevel) {
    store.updateApproval(approvalId, {
      current_level: nextLevel,
      updated_at: new Date().toISOString()
    });
    log('info', `Approval escalated to level ${nextLevel}: ${approvalId}`);
  } else {
    // 无下一级：升级到管理员
    store.updateApproval(approvalId, {
      status: 'escalated',
      updated_at: new Date().toISOString()
    });
    log('warn', `Approval escalated to admin: ${approvalId}`);
  }
  
  return store.getApproval(approvalId);
}

/**
 * 根据上下文自动匹配并创建审批
 * @param {object} context - 上下文数据
 * @returns {Array} 创建的审批列表
 */
function autoCreateApprovals(context) {
  log('info', 'Auto-creating approvals for context');
  
  const matchedRules = evaluator.matchRules(context);
  const createdApprovals = [];
  
  for (const rule of matchedRules) {
    const approval = createApproval(rule.id, context);
    if (approval) {
      createdApprovals.push(approval);
    }
  }
  
  log('info', `Created ${createdApprovals.length} approvals`);
  return createdApprovals;
}

/**
 * 获取审批统计
 * @returns {object}
 */
function getStats() {
  return store.getStats();
}

/**
 * 获取所有审批（可选过滤）
 * @param {object} filter 
 * @returns {Array}
 */
function listApprovals(filter = {}) {
  return store.getAllApprovals(filter);
}

// 导出 API
module.exports = {
  // 核心操作
  createApproval,
  submitApproval,
  getApprovalStatus,
  checkTimeouts,
  triggerEscalation,
  
  // 自动化
  autoCreateApprovals,
  
  // 查询
  getStats,
  listApprovals,
  
  // 工具
  log
};
