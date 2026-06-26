/**
 * approval-store.js
 * 
 * 审批记录存储模块 - 使用 JSON 文件持久化审批状态
 * 
 * 存储路径：$APPROVAL_ENGINE_ROOT/data/approvals.json
 * 
 * 审批记录结构：
 * {
 *   id: string,              // 审批实例 ID (UUID)
 *   rule_id: string,         // 关联的规则 ID
 *   status: string,          // pending / approved / rejected / escalated / expired
 *   created_at: string,      // ISO 时间戳
 *   updated_at: string,      // ISO 时间戳
 *   timeout_at: string,      // 超时时间戳
 *   context: object,         // 触发审批的上下文数据
 *   current_level: number,   // 当前审批级别 (从 1 开始)
 *   decisions: array,        // 审批决策记录 [{approver_id, level, decision, comment, timestamp}]
 *   notification_sent: boolean
 * }
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 存储文件路径
const DATA_DIR = process.env.APPROVAL_ENGINE_DATA_DIR || path.join(__dirname, '..', 'data');
const STORAGE_FILE = path.join(DATA_DIR, 'approvals.json');

/**
 * 确保存储文件存在
 */
function ensureStorageFile() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(STORAGE_FILE)) {
    fs.writeFileSync(STORAGE_FILE, JSON.stringify({ approvals: [], version: '1.0' }, null, 2));
  }
}

/**
 * 读取存储数据
 * @returns {{ approvals: Array, version: string }}
 */
function readStorage() {
  ensureStorageFile();
  const content = fs.readFileSync(STORAGE_FILE, 'utf8');
  return JSON.parse(content);
}

/**
 * 写入存储数据
 * @param {{ approvals: Array, version: string }} data 
 */
function writeStorage(data) {
  ensureStorageFile();
  // 创建备份
  if (fs.existsSync(STORAGE_FILE)) {
    fs.copyFileSync(STORAGE_FILE, STORAGE_FILE + '.bak');
  }
  fs.writeFileSync(STORAGE_FILE, JSON.stringify(data, null, 2));
}

/**
 * 生成唯一审批 ID
 * @returns {string}
 */
function generateApprovalId() {
  return 'APV-' + Date.now() + '-' + crypto.randomBytes(4).toString('hex').toUpperCase();
}

/**
 * 创建审批记录
 * @param {string} ruleId - 规则 ID
 * @param {object} context - 触发上下文
 * @param {number} timeoutHours - 超时小时数
 * @returns {object} 创建的审批记录
 */
function createApproval(ruleId, context, timeoutHours = 24) {
  const storage = readStorage();
  const now = new Date();
  const timeoutAt = new Date(now.getTime() + timeoutHours * 60 * 60 * 1000);
  
  const approval = {
    id: generateApprovalId(),
    rule_id: ruleId,
    status: 'pending',
    created_at: now.toISOString(),
    updated_at: now.toISOString(),
    timeout_at: timeoutAt.toISOString(),
    context: context,
    current_level: 1,
    decisions: [],
    notification_sent: false
  };
  
  storage.approvals.push(approval);
  writeStorage(storage);
  
  console.log(`[ApprovalStore] Created approval: ${approval.id} for rule: ${ruleId}`);
  return approval;
}

/**
 * 获取审批记录
 * @param {string} approvalId - 审批 ID
 * @returns {object|null} 审批记录或 null
 */
function getApproval(approvalId) {
  const storage = readStorage();
  const approval = storage.approvals.find(a => a.id === approvalId);
  return approval || null;
}

/**
 * 获取所有审批记录
 * @param {object} filter - 可选过滤条件 { status, rule_id, current_level }
 * @returns {Array} 审批记录列表
 */
function getAllApprovals(filter = {}) {
  const storage = readStorage();
  let approvals = storage.approvals;
  
  if (filter.status) {
    approvals = approvals.filter(a => a.status === filter.status);
  }
  if (filter.rule_id) {
    approvals = approvals.filter(a => a.rule_id === filter.rule_id);
  }
  if (filter.current_level) {
    approvals = approvals.filter(a => a.current_level === filter.current_level);
  }
  
  return approvals;
}

/**
 * 更新审批记录
 * @param {string} approvalId - 审批 ID
 * @param {object} updates - 要更新的字段
 * @returns {object|null} 更新后的审批记录或 null
 */
function updateApproval(approvalId, updates) {
  const storage = readStorage();
  const index = storage.approvals.findIndex(a => a.id === approvalId);
  
  if (index === -1) {
    console.log(`[ApprovalStore] Approval not found: ${approvalId}`);
    return null;
  }
  
  const approval = storage.approvals[index];
  Object.assign(approval, updates, { updated_at: new Date().toISOString() });
  storage.approvals[index] = approval;
  
  writeStorage(storage);
  console.log(`[ApprovalStore] Updated approval: ${approvalId}`);
  return approval;
}

/**
 * 提交审批决策
 * @param {string} approvalId - 审批 ID
 * @param {string} approverId - 审批人 ID
 * @param {number} level - 审批级别
 * @param {string} decision - 决策 (approve/reject)
 * @param {string} comment - 评论
 * @returns {object|null} 更新后的审批记录或 null
 */
function submitDecision(approvalId, approverId, level, decision, comment = '') {
  const approval = getApproval(approvalId);
  if (!approval) {
    console.log(`[ApprovalStore] Approval not found: ${approvalId}`);
    return null;
  }
  
  // 添加决策记录
  approval.decisions.push({
    approver_id: approverId,
    level: level,
    decision: decision,
    comment: comment,
    timestamp: new Date().toISOString()
  });
  
  approval.updated_at = new Date().toISOString();
  
  const storage = readStorage();
  const index = storage.approvals.findIndex(a => a.id === approvalId);
  storage.approvals[index] = approval;
  writeStorage(storage);
  
  console.log(`[ApprovalStore] Decision submitted: ${approvalId} by ${approverId} - ${decision}`);
  return approval;
}

/**
 * 删除审批记录
 * @param {string} approvalId - 审批 ID
 * @returns {boolean} 是否删除成功
 */
function deleteApproval(approvalId) {
  const storage = readStorage();
  const initialLength = storage.approvals.length;
  storage.approvals = storage.approvals.filter(a => a.id !== approvalId);
  
  if (storage.approvals.length < initialLength) {
    writeStorage(storage);
    console.log(`[ApprovalStore] Deleted approval: ${approvalId}`);
    return true;
  }
  
  console.log(`[ApprovalStore] Approval not found for deletion: ${approvalId}`);
  return false;
}

/**
 * 获取待处理审批 (pending 且未超时)
 * @returns {Array}
 */
function getPendingApprovals() {
  return getAllApprovals({ status: 'pending' });
}

/**
 * 获取超时审批
 * @returns {Array}
 */
function getExpiredApprovals() {
  const now = new Date();
  return getAllApprovals({ status: 'pending' }).filter(a => new Date(a.timeout_at) < now);
}

/**
 * 获取审批统计
 * @returns {object}
 */
function getStats() {
  const storage = readStorage();
  const approvals = storage.approvals;
  
  return {
    total: approvals.length,
    pending: approvals.filter(a => a.status === 'pending').length,
    approved: approvals.filter(a => a.status === 'approved').length,
    rejected: approvals.filter(a => a.status === 'rejected').length,
    escalated: approvals.filter(a => a.status === 'escalated').length,
    expired: approvals.filter(a => a.status === 'expired').length
  };
}

// 导出 API
module.exports = {
  // CRUD
  createApproval,
  getApproval,
  getAllApprovals,
  updateApproval,
  deleteApproval,
  
  // 决策
  submitDecision,
  
  // 查询
  getPendingApprovals,
  getExpiredApprovals,
  getStats,
  
  // 工具
  generateApprovalId,
  readStorage,
  writeStorage
};
