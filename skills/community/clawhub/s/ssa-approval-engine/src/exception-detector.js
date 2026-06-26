/**
 * Exception Detector - 异常检测器
 * 
 * 负责检测各类异常情况：审批超时、系统错误、订单异常、规则触发异常等
 */

const fs = require('fs');
const path = require('path');
const { logException } = require('./exception-logger');

const CONFIG_FILE = path.join(__dirname, '../config/approval-rules.json');
const DATA_DIR = path.join(__dirname, '../data');

/**
 * 加载审批规则配置
 */
function loadConfig() {
  try {
    const content = fs.readFileSync(CONFIG_FILE, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error('[ExceptionDetector] Failed to load config:', error.message);
    return null;
  }
}

/**
 * 加载待处理的审批记录
 */
function loadPendingApprovals() {
  const approvalsFile = path.join(DATA_DIR, 'approvals.json');
  try {
    if (!fs.existsSync(approvalsFile)) {
      return [];
    }
    const content = fs.readFileSync(approvalsFile, 'utf8');
    const data = JSON.parse(content);
    return data.approvals?.filter(a => a.status === 'pending') || [];
  } catch (error) {
    console.error('[ExceptionDetector] Failed to load pending approvals:', error.message);
    return [];
  }
}

/**
 * 加载订单数据
 */
function loadOrders() {
  const ordersFile = path.join(DATA_DIR, 'orders.json');
  try {
    if (!fs.existsSync(ordersFile)) {
      return [];
    }
    const content = fs.readFileSync(ordersFile, 'utf8');
    const data = JSON.parse(content);
    return data.orders || [];
  } catch (error) {
    console.error('[ExceptionDetector] Failed to load orders:', error.message);
    return [];
  }
}

/**
 * 检测审批超时异常
 * @param {Object} approval - 审批记录
 * @returns {Object|null} 异常对象或 null
 */
function detectApprovalTimeout(approval) {
  if (!approval || approval.status !== 'pending') {
    return null;
  }
  
  const config = loadConfig();
  if (!config) {
    return null;
  }
  
  // 查找对应规则的超时配置
  const rule = config.rules.find(r => r.id === approval.rule_id);
  const timeoutHours = rule?.timeout_hours || 24;
  
  const createdAt = new Date(approval.created_at).getTime();
  const now = Date.now();
  const elapsedHours = (now - createdAt) / (1000 * 60 * 60);
  
  if (elapsedHours > timeoutHours) {
    return {
      type: 'approval_timeout',
      severity: 'warning',
      message: `审批 ${approval.id} 已超时 ${Math.round(elapsedHours - timeoutHours)} 小时`,
      context: {
        approval_id: approval.id,
        rule_id: approval.rule_id,
        rule_name: rule?.name || 'Unknown',
        timeout_hours: timeoutHours,
        elapsed_hours: Math.round(elapsedHours * 10) / 10,
        created_at: approval.created_at,
        item_type: approval.item_type,
        item_id: approval.item_id
      }
    };
  }
  
  return null;
}

/**
 * 检测系统错误
 * @param {Error} error - 错误对象
 * @param {Object} context - 上下文信息
 * @returns {Object} 异常对象
 */
function detectSystemError(error, context = {}) {
  return {
    type: 'system_error',
    severity: 'critical',
    message: error.message || 'Unknown system error',
    context: {
      error_name: error.name || 'Error',
      error_stack: error.stack?.split('\n').slice(0, 5).join('\n'),
      module: context.module || 'unknown',
      operation: context.operation || 'unknown',
      timestamp: new Date().toISOString(),
      ...context
    }
  };
}

/**
 * 检测订单异常
 * @param {Object} order - 订单对象
 * @returns {Array} 异常对象列表
 */
function detectOrderAnomaly(order) {
  const anomalies = [];
  const config = loadConfig();
  
  if (!order || !config) {
    return anomalies;
  }
  
  // 1. 检测金额异常（超出阈值）
  const amountThreshold = config.thresholds?.quotation_amount_limit || 50000;
  if (order.amount && order.amount > amountThreshold * 3) {
    anomalies.push({
      type: 'order_amount_anomaly',
      severity: 'warning',
      message: `订单金额 ${order.amount} 超出正常阈值 ${amountThreshold * 3}`,
      context: {
        order_id: order.id,
        amount: order.amount,
        threshold: amountThreshold * 3,
        customer: order.customer_name || order.customer?.name
      }
    });
  }
  
  // 2. 检测重复订单（相同客户 + 相同产品 + 短时间内）
  if (order.id && order.customer_id) {
    const orders = loadOrders();
    const recentOrders = orders.filter(o => 
      o.customer_id === order.customer_id && 
      o.id !== order.id &&
      new Date(o.created_at).getTime() > Date.now() - (24 * 60 * 60 * 1000)
    );
    
    if (recentOrders.length >= 3) {
      anomalies.push({
        type: 'duplicate_order_suspect',
        severity: 'warning',
        message: `客户 ${order.customer_id} 在 24 小时内下单 ${recentOrders.length + 1} 次`,
        context: {
          order_id: order.id,
          customer_id: order.customer_id,
          recent_order_count: recentOrders.length + 1,
          recent_orders: recentOrders.map(o => o.id).slice(0, 5)
        }
      });
    }
  }
  
  // 3. 检测状态异常
  const validStatuses = ['pending', 'pending_approval', 'approved', 'in_production', 'ready_to_ship', 'shipped', 'completed', 'cancelled', 'exception'];
  if (order.status && !validStatuses.includes(order.status)) {
    anomalies.push({
      type: 'order_status_anomaly',
      severity: 'warning',
      message: `订单 ${order.id} 状态 "${order.status}" 不在有效状态列表中`,
      context: {
        order_id: order.id,
        current_status: order.status,
        valid_statuses: validStatuses
      }
    });
  }
  
  // 4. 检测交期异常（已逾期）
  if (order.delivery_date) {
    const deliveryDate = new Date(order.delivery_date).getTime();
    const now = Date.now();
    if (deliveryDate < now && order.status !== 'completed' && order.status !== 'cancelled') {
      const daysOverdue = Math.round((now - deliveryDate) / (1000 * 60 * 60 * 24));
      anomalies.push({
        type: 'order_overdue',
        severity: 'critical',
        message: `订单 ${order.id} 已逾期 ${daysOverdue} 天`,
        context: {
          order_id: order.id,
          delivery_date: order.delivery_date,
          days_overdue: daysOverdue,
          current_status: order.status,
          customer: order.customer_name || order.customer?.name
        }
      });
    }
  }
  
  // 5. 检测负数量或零数量
  if (order.quantity !== undefined && order.quantity <= 0) {
    anomalies.push({
      type: 'order_quantity_anomaly',
      severity: 'warning',
      message: `订单 ${order.id} 数量 ${order.quantity} 无效`,
      context: {
        order_id: order.id,
        quantity: order.quantity
      }
    });
  }
  
  return anomalies;
}

/**
 * 检测规则触发异常
 * @param {Object} ruleEvaluation - 规则评估结果
 * @returns {Object|null} 异常对象或 null
 */
function detectRuleTriggerAnomaly(ruleEvaluation) {
  if (!ruleEvaluation) {
    return null;
  }
  
  if (ruleEvaluation.error) {
    return {
      type: 'rule_evaluation_error',
      severity: 'warning',
      message: `规则评估失败：${ruleEvaluation.error}`,
      context: {
        rule_id: ruleEvaluation.rule_id,
        evaluation_input: ruleEvaluation.input,
        error: ruleEvaluation.error
      }
    };
  }
  
  return null;
}

/**
 * 定期扫描所有待处理审批的超时状态
 * @returns {Array} 超时异常列表
 */
function runPeriodicCheck() {
  console.log('[ExceptionDetector] Running periodic check...');
  
  const pendingApprovals = loadPendingApprovals();
  const timeoutExceptions = [];
  
  pendingApprovals.forEach(approval => {
    const timeoutException = detectApprovalTimeout(approval);
    if (timeoutException) {
      timeoutExceptions.push(timeoutException);
      logException(timeoutException);
    }
  });
  
  // 检测所有订单异常
  const orders = loadOrders();
  const orderAnomalies = [];
  
  orders.forEach(order => {
    const anomalies = detectOrderAnomaly(order);
    anomalies.forEach(anomaly => {
      orderAnomalies.push(anomaly);
      logException(anomaly);
    });
  });
  
  const summary = {
    checked_at: new Date().toISOString(),
    pending_approvals_checked: pendingApprovals.length,
    timeout_exceptions_found: timeoutExceptions.length,
    orders_checked: orders.length,
    order_anomalies_found: orderAnomalies.length
  };
  
  console.log('[ExceptionDetector] Periodic check completed:', summary);
  return {
    exceptions: [...timeoutExceptions, ...orderAnomalies],
    summary
  };
}

/**
 * 检测所有类型异常（入口函数）
 * @param {Object} options - 检测选项
 * @returns {Object} 检测结果
 */
function detectAll(options = {}) {
  const results = {
    checked_at: new Date().toISOString(),
    exceptions: [],
    summary: {}
  };
  
  // 审批超时检测
  if (options.check_approvals !== false) {
    const pendingApprovals = loadPendingApprovals();
    pendingApprovals.forEach(approval => {
      const exc = detectApprovalTimeout(approval);
      if (exc) results.exceptions.push(exc);
    });
  }
  
  // 订单异常检测
  if (options.check_orders !== false) {
    const orders = loadOrders();
    orders.forEach(order => {
      const anomalies = detectOrderAnomaly(order);
      results.exceptions.push(...anomalies);
    });
  }
  
  results.summary = {
    total_exceptions: results.exceptions.length,
    by_severity: {
      critical: results.exceptions.filter(e => e.severity === 'critical').length,
      warning: results.exceptions.filter(e => e.severity === 'warning').length,
      info: results.exceptions.filter(e => e.severity === 'info').length
    }
  };
  
  return results;
}

module.exports = {
  detectApprovalTimeout,
  detectSystemError,
  detectOrderAnomaly,
  detectRuleTriggerAnomaly,
  runPeriodicCheck,
  detectAll,
  loadConfig,
  loadPendingApprovals,
  loadOrders
};
