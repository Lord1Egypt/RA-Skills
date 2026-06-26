#!/usr/bin/env node

/**
 * After-Sales CLI - 售后管理统一命令行工具
 * 
 * 整合所有售后模块功能：
 * - complaint: 投诉管理
 * - repeat-order: 返单报价
 * - satisfaction: 满意度调查
 * - analytics: 分析报表
 * - okki: OKKI 同步
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');

// Chalk v5+ 需要动态导入（ESM）
let chalk;
(async () => {
  chalk = (await import('chalk')).default;
  
  // 重新定义工具函数
  global.printSuccess = (message) => console.log('✅', message);
  global.printError = (message) => console.error('❌', message);
  global.printInfo = (message) => console.log('ℹ️', message);
  global.chalk = chalk;
})();

const program = new Command();

// ==================== 导入各模块 API ====================

// 分析报表 API
const analyticsAPI = require('../api/controllers/analytics_api');

// OKKI 同步控制器
const okkiSyncController = require('../api/controllers/okki_sync_controller');

// OKKI 同步日志模型
const OkkiSyncLogModule = require('../models/okki_sync_log_model');
const OkkiSyncLog = OkkiSyncLogModule.OkkiSyncLog;

// 分析模型（用于获取模拟数据）
const analyticsModel = require('../models/analytics_model');

// ==================== 工具函数 ====================

/**
 * 生成 ID
 */
function generateId(prefix) {
  const timestamp = new Date().toISOString().replace(/[-:]/g, '').slice(0, 14);
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
  return `${prefix}-${timestamp}-${random}`;
}

/**
 * 加载 JSON 数据文件
 */
function loadJsonFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return [];
    }
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(chalk.red(`读取文件失败：${error.message}`));
    return [];
  }
}

/**
 * 保存 JSON 数据文件
 */
function saveJsonFile(filePath, data) {
  try {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error(chalk.red(`保存文件失败：${error.message}`));
    return false;
  }
}

/**
 * 格式化表格
 */
function formatTable(headers, rows) {
  if (rows.length === 0) {
    return '暂无数据';
  }
  
  const widths = headers.map((h, i) => {
    const maxRowWidth = Math.max(...rows.map(r => String(r[i] || '').length));
    return Math.max(h.length, maxRowWidth, 10);
  });
  
  const separator = '+' + widths.map(w => '-'.repeat(w + 2)).join('+') + '+';
  const headerRow = '|' + widths.map((w, i) => ` ${headers[i].padEnd(w)} `).join('|') + '|';
  const dataRows = rows.map(row => 
    '|' + widths.map((w, i) => ` ${String(row[i] || '').padEnd(w)} `).join('|') + '|'
  );
  
  return [separator, headerRow, separator, ...dataRows, separator].join('\n');
}

/**
 * 打印 JSON
 */
function printJson(data) {
  console.log(JSON.stringify(data, null, 2));
}

/**
 * 打印成功消息
 */
function printSuccess(message) {
  console.log(chalk.green('✅'), message);
}

/**
 * 打印错误消息
 */
function printError(message) {
  console.error(chalk.red('❌'), message);
}

/**
 * 打印信息消息
 */
function printInfo(message) {
  console.log(chalk.cyan('ℹ️'), message);
}

// ==================== 投诉管理 ====================

const COMPLAINT_DATA_FILE = path.join(__dirname, '../data/complaints.json');

/**
 * 获取所有投诉（使用模拟数据）
 */
function getAllComplaints() {
  // 使用 analytics_api 获取统计数据，这里使用简化的模拟数据
  const mockComplaints = [
    {
      id: 'CMP-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      productId: 'PROD-001',
      productName: 'HDMI Cable 2.0',
      type: 'quality',
      status: 'resolved',
      description: 'Cable stopped working after 2 weeks',
      createdAt: '2026-03-10',
      resolvedAt: '2026-03-15',
      severity: 'medium',
      assignedTo: null,
      currentStep: 'resolved',
      satisfactionScore: 4
    },
    {
      id: 'CMP-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      productId: 'PROD-003',
      productName: 'USB-C Cable',
      type: 'delivery',
      status: 'pending',
      description: 'Delivery delayed by 1 week',
      createdAt: '2026-03-20',
      resolvedAt: null,
      severity: 'low',
      assignedTo: null,
      currentStep: 'pending',
      satisfactionScore: null
    },
    {
      id: 'CMP-003',
      customerId: 'CUST-003',
      customerName: 'Global Tech Solutions',
      productId: 'PROD-002',
      productName: 'DP Cable 1.4',
      type: 'quality',
      status: 'resolved',
      description: 'Connector loose, poor contact',
      createdAt: '2026-03-05',
      resolvedAt: '2026-03-12',
      severity: 'high',
      assignedTo: 'sales-1',
      currentStep: 'resolved',
      satisfactionScore: 5
    }
  ];
  
  return mockComplaints;
}

/**
 * 保存投诉
 */
function saveComplaints(complaints) {
  return saveJsonFile(COMPLAINT_DATA_FILE, complaints);
}

/**
 * 创建投诉
 */
function createComplaint(options) {
  const complaints = getAllComplaints();
  
  const newComplaint = {
    id: generateId('CMP'),
    customerId: options.customer || 'CUST-UNKNOWN',
    customerName: options.customerName || '未指定客户',
    productId: options.product || 'PROD-UNKNOWN',
    productName: options.productName || '未指定产品',
    type: options.type || 'quality',
    status: 'pending',
    description: options.description || '无描述',
    severity: options.severity || 'medium',
    createdAt: new Date().toISOString().split('T')[0],
    resolvedAt: null,
    assignedTo: options.assignee || null,
    currentStep: 'pending',
    satisfactionScore: null
  };
  
  complaints.push(newComplaint);
  saveComplaints(complaints);
  
  printSuccess('投诉创建成功');
  console.log(`   ID: ${chalk.bold(newComplaint.id)}`);
  console.log(`   客户：${newComplaint.customerName}`);
  console.log(`   产品：${newComplaint.productName}`);
  console.log(`   类型：${newComplaint.type}`);
  console.log(`   严重程度：${newComplaint.severity}`);
  console.log(`   状态：${newComplaint.status}`);
  
  return newComplaint;
}

/**
 * 列出投诉
 */
function listComplaints(options) {
  const complaints = getAllComplaints();
  
  let filtered = complaints;
  
  if (options.status) {
    filtered = filtered.filter(c => c.status === options.status);
  }
  if (options.type) {
    filtered = filtered.filter(c => c.type === options.type);
  }
  if (options.severity) {
    filtered = filtered.filter(c => c.severity === options.severity);
  }
  
  if (filtered.length === 0) {
    printInfo('暂无投诉记录');
    return;
  }
  
  console.log(chalk.cyan(`\n投诉列表 (共 ${filtered.length} 条)\n`));
  
  const headers = ['ID', '客户', '产品', '类型', '严重程度', '状态', '创建时间'];
  const rows = filtered.map(c => [
    c.id,
    (c.customerName || '-').slice(0, 15),
    (c.productName || '-').slice(0, 15),
    c.type,
    c.severity,
    c.status,
    c.createdAt
  ]);
  
  console.log(formatTable(headers, rows));
}

/**
 * 获取投诉详情
 */
function getComplaint(complaintId) {
  const complaints = getAllComplaints();
  const complaint = complaints.find(c => c.id === complaintId);
  
  if (!complaint) {
    printError(`未找到投诉：${complaintId}`);
    return null;
  }
  
  console.log(chalk.cyan('\n投诉详情\n'));
  console.log(`ID:           ${chalk.bold(complaint.id)}`);
  console.log(`客户 ID:      ${complaint.customerId}`);
  console.log(`客户名称：    ${complaint.customerName}`);
  console.log(`产品 ID:      ${complaint.productId}`);
  console.log(`产品名称：    ${complaint.productName}`);
  console.log(`类型：        ${complaint.type}`);
  console.log(`描述：        ${complaint.description}`);
  console.log(`严重程度：    ${complaint.severity}`);
  console.log(`状态：        ${complaint.status}`);
  console.log(`当前步骤：    ${complaint.currentStep || 'pending'}`);
  console.log(`处理人：      ${complaint.assignedTo || '未分配'}`);
  console.log(`创建时间：    ${complaint.createdAt}`);
  console.log(`解决时间：    ${complaint.resolvedAt || '未解决'}`);
  if (complaint.satisfactionScore !== null) {
    console.log(`满意度评分：  ${complaint.satisfactionScore}/5`);
  }
  
  return complaint;
}

/**
 * 更新投诉
 */
function updateComplaint(complaintId, options) {
  const complaints = getAllComplaints();
  const index = complaints.findIndex(c => c.id === complaintId);
  
  if (index === -1) {
    printError(`未找到投诉：${complaintId}`);
    return false;
  }
  
  const complaint = complaints[index];
  
  if (options.description) complaint.description = options.description;
  if (options.type) complaint.type = options.type;
  if (options.severity) complaint.severity = options.severity;
  if (options.status) complaint.status = options.status;
  if (options.currentStep) complaint.currentStep = options.currentStep;
  if (options.assignee) complaint.assignedTo = options.assignee;
  
  saveComplaints(complaints);
  
  printSuccess('投诉更新成功');
  console.log(`   ID: ${complaint.id}`);
  
  return complaint;
}

/**
 * 更新投诉状态
 */
function updateComplaintStatus(complaintId, status) {
  return updateComplaint(complaintId, { status });
}

/**
 * 分配投诉
 */
function assignComplaint(complaintId, assignee) {
  return updateComplaint(complaintId, { assignee });
}

/**
 * 更新投诉步骤
 */
function updateComplaintStep(complaintId, step) {
  return updateComplaint(complaintId, { currentStep: step });
}

/**
 * 记录满意度
 */
function recordSatisfaction(complaintId, score) {
  const complaints = getAllComplaints();
  const index = complaints.findIndex(c => c.id === complaintId);
  
  if (index === -1) {
    printError(`未找到投诉：${complaintId}`);
    return false;
  }
  
  const complaint = complaints[index];
  complaint.satisfactionScore = parseInt(score);
  
  saveComplaints(complaints);
  
  printSuccess('满意度评分已记录');
  console.log(`   投诉 ID: ${complaint.id}`);
  console.log(`   评分：${score}/5`);
  
  return complaint;
}

/**
 * 删除投诉
 */
function deleteComplaint(complaintId) {
  const complaints = getAllComplaints();
  const index = complaints.findIndex(c => c.id === complaintId);
  
  if (index === -1) {
    printError(`未找到投诉：${complaintId}`);
    return false;
  }
  
  complaints.splice(index, 1);
  saveComplaints(complaints);
  
  printSuccess('投诉已删除');
  console.log(`   ID: ${complaintId}`);
  
  return true;
}

/**
 * 投诉统计
 */
function getComplaintStats() {
  const complaints = getAllComplaints();
  
  const stats = {
    total: complaints.length,
    byStatus: {},
    byType: {},
    bySeverity: {},
    resolved: 0,
    pending: 0,
    avgResolutionDays: 0
  };
  
  let totalResolutionDays = 0;
  let resolvedCount = 0;
  
  complaints.forEach(c => {
    stats.byStatus[c.status] = (stats.byStatus[c.status] || 0) + 1;
    stats.byType[c.type] = (stats.byType[c.type] || 0) + 1;
    stats.bySeverity[c.severity] = (stats.bySeverity[c.severity] || 0) + 1;
    
    if (c.status === 'resolved') {
      stats.resolved++;
      if (c.resolvedAt && c.createdAt) {
        const days = (new Date(c.resolvedAt) - new Date(c.createdAt)) / (1000 * 60 * 60 * 24);
        totalResolutionDays += days;
        resolvedCount++;
      }
    } else {
      stats.pending++;
    }
  });
  
  if (resolvedCount > 0) {
    stats.avgResolutionDays = (totalResolutionDays / resolvedCount).toFixed(1);
  }
  
  console.log(chalk.cyan('\n投诉统计\n'));
  console.log(`总投诉数：    ${chalk.bold(stats.total)}`);
  console.log(`已解决：      ${chalk.green(stats.resolved)}`);
  console.log(`待处理：      ${chalk.yellow(stats.pending)}`);
  console.log(`解决率：      ${((stats.resolved / stats.total) * 100).toFixed(1)}%`);
  console.log(`平均解决时间：${stats.avgResolutionDays} 天\n`);
  
  console.log('按类型统计:');
  Object.entries(stats.byType).forEach(([type, count]) => {
    console.log(`  ${type}: ${count}`);
  });
  console.log('');
  
  console.log('按严重程度统计:');
  Object.entries(stats.bySeverity).forEach(([severity, count]) => {
    console.log(`  ${severity}: ${count}`);
  });
  
  return stats;
}

// ==================== 返单报价管理 ====================

const REPEAT_ORDER_DATA_FILE = path.join(__dirname, '../data/repeat_orders.json');

/**
 * 获取所有返单（使用模拟数据）
 */
function getAllRepeatOrders() {
  const mockOrders = [
    {
      id: 'RO-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      initialOrderId: 'ORD-100',
      repeatOrderId: 'ORD-150',
      initialOrderDate: '2026-01-15',
      repeatOrderDate: '2026-03-10',
      initialAmount: 50000,
      repeatAmount: 75000,
      daysToRepeat: 54,
      status: 'completed',
      products: [],
      notes: '首次返单',
      createdAt: '2026-03-10T10:00:00.000Z'
    },
    {
      id: 'RO-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      initialOrderId: 'ORD-120',
      repeatOrderId: 'ORD-180',
      initialOrderDate: '2026-02-01',
      repeatOrderDate: '2026-03-20',
      initialAmount: 30000,
      repeatAmount: 45000,
      daysToRepeat: 47,
      status: 'pending',
      products: [],
      notes: '',
      createdAt: '2026-03-20T14:30:00.000Z'
    }
  ];
  
  return mockOrders;
}

/**
 * 保存返单
 */
function saveRepeatOrders(orders) {
  return saveJsonFile(REPEAT_ORDER_DATA_FILE, orders);
}

/**
 * 创建返单
 */
function createRepeatOrder(options) {
  const orders = getAllRepeatOrders();
  
  const newOrder = {
    id: generateId('RO'),
    customerId: options.customer || 'CUST-UNKNOWN',
    customerName: options.customerName || '未指定客户',
    initialOrderId: options.initialOrder || 'ORD-UNKNOWN',
    repeatOrderId: options.repeatOrder || generateId('ORD'),
    initialOrderDate: options.initialDate || new Date().toISOString().split('T')[0],
    repeatOrderDate: new Date().toISOString().split('T')[0],
    initialAmount: parseFloat(options.initialAmount) || 0,
    repeatAmount: parseFloat(options.repeatAmount) || 0,
    daysToRepeat: 0,
    status: options.status || 'pending',
    products: options.products || [],
    notes: options.notes || '',
    createdAt: new Date().toISOString()
  };
  
  // 计算返单周期
  const initialDate = new Date(newOrder.initialOrderDate);
  const repeatDate = new Date(newOrder.repeatOrderDate);
  newOrder.daysToRepeat = Math.ceil((repeatDate - initialDate) / (1000 * 60 * 60 * 24));
  
  orders.push(newOrder);
  saveRepeatOrders(orders);
  
  printSuccess('返单报价创建成功');
  console.log(`   ID: ${chalk.bold(newOrder.id)}`);
  console.log(`   客户：${newOrder.customerName}`);
  console.log(`   初始订单：${newOrder.initialOrderId}`);
  console.log(`   返单金额：¥${newOrder.repeatAmount.toLocaleString()}`);
  console.log(`   返单周期：${newOrder.daysToRepeat} 天`);
  
  return newOrder;
}

/**
 * 列出返单
 */
function listRepeatOrders(options) {
  const orders = getAllRepeatOrders();
  
  let filtered = orders;
  
  if (options.status) {
    filtered = filtered.filter(o => o.status === options.status);
  }
  if (options.customer) {
    filtered = filtered.filter(o => o.customerId === options.customer || o.customerName.includes(options.customer));
  }
  
  if (filtered.length === 0) {
    printInfo('暂无返单记录');
    return;
  }
  
  console.log(chalk.cyan(`\n返单列表 (共 ${filtered.length} 条)\n`));
  
  const headers = ['ID', '客户', '初始订单', '返单金额', '周期', '状态'];
  const rows = filtered.map(o => [
    o.id,
    (o.customerName || '-').slice(0, 15),
    o.initialOrderId,
    `¥${o.repeatAmount.toLocaleString()}`,
    `${o.daysToRepeat}天`,
    o.status
  ]);
  
  console.log(formatTable(headers, rows));
}

/**
 * 获取返单详情
 */
function getRepeatOrder(orderId) {
  const orders = getAllRepeatOrders();
  const order = orders.find(o => o.id === orderId);
  
  if (!order) {
    printError(`未找到返单：${orderId}`);
    return null;
  }
  
  console.log(chalk.cyan('\n返单详情\n'));
  console.log(`ID:             ${chalk.bold(order.id)}`);
  console.log(`客户 ID:        ${order.customerId}`);
  console.log(`客户名称：      ${order.customerName}`);
  console.log(`初始订单：      ${order.initialOrderId}`);
  console.log(`返单订单：      ${order.repeatOrderId}`);
  console.log(`初始订单日期：  ${order.initialOrderDate}`);
  console.log(`返单日期：      ${order.repeatOrderDate}`);
  console.log(`初始金额：      ¥${order.initialAmount.toLocaleString()}`);
  console.log(`返单金额：      ¥${order.repeatAmount.toLocaleString()}`);
  console.log(`返单周期：      ${order.daysToRepeat} 天`);
  console.log(`状态：          ${order.status}`);
  console.log(`备注：          ${order.notes || '无'}`);
  console.log(`创建时间：      ${order.createdAt}`);
  
  return order;
}

/**
 * 更新返单
 */
function updateRepeatOrder(orderId, options) {
  const orders = getAllRepeatOrders();
  const index = orders.findIndex(o => o.id === orderId);
  
  if (index === -1) {
    printError(`未找到返单：${orderId}`);
    return false;
  }
  
  const order = orders[index];
  
  if (options.status) order.status = options.status;
  if (options.repeatAmount) order.repeatAmount = parseFloat(options.repeatAmount);
  if (options.notes !== undefined) order.notes = options.notes;
  if (options.products) order.products = options.products;
  
  saveRepeatOrders(orders);
  
  printSuccess('返单更新成功');
  console.log(`   ID: ${order.id}`);
  
  return order;
}

// ==================== 满意度调查管理 ====================

const SATISFACTION_DATA_FILE = path.join(__dirname, '../data/satisfaction_surveys.json');

/**
 * 获取所有满意度调查
 */
function getAllSatisfactionSurveys() {
  return loadJsonFile(SATISFACTION_DATA_FILE);
}

/**
 * 保存满意度调查
 */
function saveSatisfactionSurveys(surveys) {
  return saveJsonFile(SATISFACTION_DATA_FILE, surveys);
}

/**
 * 创建满意度调查
 */
function createSatisfaction(options) {
  const surveys = getAllSatisfactionSurveys();
  
  const newSurvey = {
    id: generateId('SAT'),
    complaintId: options.complaintId || null,
    customerId: options.customer || 'CUST-UNKNOWN',
    customerName: options.customerName || '未指定客户',
    overallScore: parseInt(options.overall) || 0,
    qualityScore: parseInt(options.quality) || 0,
    serviceScore: parseInt(options.service) || 0,
    deliveryScore: parseInt(options.delivery) || 0,
    communicationScore: parseInt(options.communication) || 0,
    comments: options.comments || '',
    createdAt: new Date().toISOString()
  };
  
  surveys.push(newSurvey);
  saveSatisfactionSurveys(surveys);
  
  printSuccess('满意度调查创建成功');
  console.log(`   ID: ${chalk.bold(newSurvey.id)}`);
  console.log(`   客户：${newSurvey.customerName}`);
  console.log(`   综合评分：${newSurvey.overallScore}/5`);
  
  return newSurvey;
}

/**
 * 列出满意度调查
 */
function listSatisfaction(options) {
  const surveys = getAllSatisfactionSurveys();
  
  let filtered = surveys;
  
  if (options.customer) {
    filtered = filtered.filter(s => s.customerId === options.customer || s.customerName.includes(options.customer));
  }
  
  if (filtered.length === 0) {
    printInfo('暂无满意度调查记录');
    return;
  }
  
  console.log(chalk.cyan(`\n满意度调查列表 (共 ${filtered.length} 条)\n`));
  
  const headers = ['ID', '客户', '综合评分', '质量', '服务', '物流', '时间'];
  const rows = filtered.map(s => [
    s.id,
    (s.customerName || '-').slice(0, 15),
    `${s.overallScore}/5`,
    `${s.qualityScore}/5`,
    `${s.serviceScore}/5`,
    `${s.deliveryScore}/5`,
    s.createdAt.slice(0, 10)
  ]);
  
  console.log(formatTable(headers, rows));
}

/**
 * 获取满意度调查详情
 */
function getSatisfaction(surveyId) {
  const surveys = getAllSatisfactionSurveys();
  const survey = surveys.find(s => s.id === surveyId);
  
  if (!survey) {
    printError(`未找到满意度调查：${surveyId}`);
    return null;
  }
  
  console.log(chalk.cyan('\n满意度调查详情\n'));
  console.log(`ID:           ${chalk.bold(survey.id)}`);
  console.log(`客户 ID:      ${survey.customerId}`);
  console.log(`客户名称：    ${survey.customerName}`);
  if (survey.complaintId) {
    console.log(`关联投诉：    ${survey.complaintId}`);
  }
  console.log(`综合评分：    ${'★'.repeat(survey.overallScore)}${'☆'.repeat(5 - survey.overallScore)} (${survey.overallScore}/5)`);
  console.log(`产品质量：    ${survey.qualityScore}/5`);
  console.log(`服务质量：    ${survey.serviceScore}/5`);
  console.log(`物流配送：    ${survey.deliveryScore}/5`);
  console.log(`沟通效率：    ${survey.communicationScore}/5`);
  console.log(`备注：        ${survey.comments || '无'}`);
  console.log(`创建时间：    ${survey.createdAt}`);
  
  return survey;
}

/**
 * 满意度统计
 */
function getSatisfactionStats() {
  const surveys = getAllSatisfactionSurveys();
  
  if (surveys.length === 0) {
    printInfo('暂无满意度调查数据');
    return { total: 0 };
  }
  
  const stats = {
    total: surveys.length,
    avgOverallScore: 0,
    avgQualityScore: 0,
    avgServiceScore: 0,
    avgDeliveryScore: 0,
    avgCommunicationScore: 0,
    distribution: {}
  };
  
  let totalOverall = 0, totalQuality = 0, totalService = 0, totalDelivery = 0, totalCommunication = 0;
  
  surveys.forEach(s => {
    totalOverall += s.overallScore;
    totalQuality += s.qualityScore;
    totalService += s.serviceScore;
    totalDelivery += s.deliveryScore;
    totalCommunication += s.communicationScore;
    
    stats.distribution[s.overallScore] = (stats.distribution[s.overallScore] || 0) + 1;
  });
  
  stats.avgOverallScore = (totalOverall / surveys.length).toFixed(2);
  stats.avgQualityScore = (totalQuality / surveys.length).toFixed(2);
  stats.avgServiceScore = (totalService / surveys.length).toFixed(2);
  stats.avgDeliveryScore = (totalDelivery / surveys.length).toFixed(2);
  stats.avgCommunicationScore = (totalCommunication / surveys.length).toFixed(2);
  
  console.log(chalk.cyan('\n满意度统计\n'));
  console.log(`总调查数：      ${chalk.bold(stats.total)}`);
  console.log(`综合平均分：  ${chalk.bold(stats.avgOverallScore)}/5.0`);
  console.log(`产品质量：    ${stats.avgQualityScore}/5.0`);
  console.log(`服务质量：    ${stats.avgServiceScore}/5.0`);
  console.log(`物流配送：    ${stats.avgDeliveryScore}/5.0`);
  console.log(`沟通效率：    ${stats.avgCommunicationScore}/5.0\n`);
  
  console.log('分数分布:');
  for (let score = 5; score >= 1; score--) {
    const count = stats.distribution[score] || 0;
    const bar = '★'.repeat(score) + '☆'.repeat(5 - score);
    console.log(`  ${bar} (${score}分): ${count} 票`);
  }
  
  return stats;
}

// ==================== 分析报表 ====================

/**
 * 投诉分析
 */
function analyzeComplaints(options) {
  const result = analyticsAPI.getComplaintAnalytics(options.range);
  
  if (result.success) {
    console.log(chalk.cyan('\n=== 投诉统计分析 ===\n'));
    console.log(`日期范围：${result.dateRange.startDate} 至 ${result.dateRange.endDate}`);
    console.log(`生成时间：${result.generatedAt}\n`);
    
    const summary = result.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总投诉数：${summary.total}`);
    console.log(`  已解决：${summary.resolved}`);
    console.log(`  待处理：${summary.pending}`);
    console.log(`  解决率：${summary.resolutionRate}`);
    console.log(`  平均解决时间：${summary.avgResolutionDays} 天\n`);
  } else {
    printError(`分析失败：${result.error}`);
  }
}

/**
 * 返单分析
 */
function analyzeRepeatOrders(options) {
  const result = analyticsAPI.getRepeatOrderAnalytics(options.range);
  
  if (result.success) {
    console.log(chalk.cyan('\n=== 返单统计分析 ===\n'));
    console.log(`日期范围：${result.dateRange.startDate} 至 ${result.dateRange.endDate}`);
    console.log(`生成时间：${result.generatedAt}\n`);
    
    const summary = result.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总返单数：${summary.total}`);
    console.log(`  转化率：${summary.conversionRate}`);
    console.log(`  总返单金额：¥${summary.totalAmount.toLocaleString()}`);
    console.log(`  平均返单金额：¥${parseFloat(summary.avgAmount).toLocaleString()}`);
    console.log(`  平均返单周期：${summary.avgDaysToRepeat} 天\n`);
  } else {
    printError(`分析失败：${result.error}`);
  }
}

/**
 * 满意度分析
 */
function analyzeSatisfaction(options) {
  const result = analyticsAPI.getSatisfactionAnalytics(options.range);
  
  if (result.success) {
    console.log(chalk.cyan('\n=== 满意度统计分析 ===\n'));
    console.log(`日期范围：${result.dateRange.startDate} 至 ${result.dateRange.endDate}`);
    console.log(`生成时间：${result.generatedAt}\n`);
    
    const summary = result.data.summary;
    if (summary.total === 0) {
      printInfo('暂无满意度调查数据');
    } else {
      console.log('📊 概要统计:');
      console.log(`  总调查数：${summary.total}`);
      console.log(`  综合平均分：${summary.avgOverallScore}/5.0`);
      console.log(`  产品质量：${summary.avgQualityScore}/5.0`);
      console.log(`  服务质量：${summary.avgServiceScore}/5.0`);
      console.log(`  物流配送：${summary.avgDeliveryScore}/5.0`);
      console.log(`  沟通效率：${summary.avgCommunicationScore}/5.0\n`);
    }
  } else {
    printError(`分析失败：${result.error}`);
  }
}

/**
 * 客户风险分析
 */
function analyzeRisk() {
  const result = analyticsAPI.getCustomerRiskAnalysis();
  
  if (result.success) {
    console.log(chalk.cyan('\n=== 客户风险分析 ===\n'));
    console.log(`生成时间：${result.generatedAt}\n`);
    
    const summary = result.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总客户数：${summary.totalCustomers}`);
    console.log(`  低风险客户：${summary.lowRisk}`);
    console.log(`  中风险客户：${summary.mediumRisk}`);
    console.log(`  高风险客户：${summary.highRisk}`);
    console.log(`  高风险占比：${summary.highRiskRatio}\n`);
  } else {
    printError(`分析失败：${result.error}`);
  }
}

/**
 * 产品质量分析
 */
function analyzeQuality() {
  const result = analyticsAPI.getProductQualityAnalysis();
  
  if (result.success) {
    console.log(chalk.cyan('\n=== 产品质量分析 ===\n'));
    console.log(`生成时间：${result.generatedAt}\n`);
    
    const summary = result.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总产品数：${summary.totalProducts}`);
    console.log(`  平均缺陷率：${(parseFloat(summary.avgDefectRate) * 100).toFixed(2)}%\n`);
  } else {
    printError(`分析失败：${result.error}`);
  }
}

/**
 * 综合摘要
 */
function analyzeSummary(options) {
  const result = analyticsAPI.getAnalyticsSummary(options.range);
  
  if (result.success) {
    console.log(chalk.cyan('\n========================================'));
    console.log('     售后分析综合摘要报告');
    console.log('========================================\n');
    console.log(`生成时间：${result.generatedAt}\n`);

    console.log('📊 投诉统计:');
    const c = result.summary.complaints;
    console.log(`  总数：${c.total} | 已解决：${c.resolved} | 解决率：${c.resolutionRate} | 平均解决时间：${c.avgResolutionDays}天\n`);

    console.log('🔄 返单统计:');
    const r = result.summary.repeatOrders;
    console.log(`  总数：${r.total} | 转化率：${r.conversionRate} | 总金额：¥${r.totalAmount.toLocaleString()} | 平均周期：${r.avgDaysToRepeat}天\n`);

    console.log('⭐ 满意度统计:');
    const s = result.summary.satisfaction;
    if (s.total > 0) {
      console.log(`  总调查数：${s.total} | 综合评分：${s.avgOverallScore}/5.0 | 质量：${s.avgQualityScore} | 服务：${s.avgServiceScore}\n`);
    } else {
      console.log(`  暂无数据\n`);
    }

    console.log('⚠️  客户风险:');
    const risk = result.summary.customerRisk;
    console.log(`  总客户：${risk.totalCustomers} | 低：${risk.lowRisk} | 中：${risk.mediumRisk} | 高：${risk.highRisk} (${risk.highRiskRatio})\n`);

    console.log('📦 产品质量:');
    const q = result.summary.productQuality;
    console.log(`  总产品：${q.totalProducts} | 平均缺陷率：${(parseFloat(q.avgDefectRate) * 100).toFixed(2)}%\n`);

    console.log('========================================');
  } else {
    printError(`分析失败：${result.error}`);
  }
}

// ==================== OKKI 同步 ====================

/**
 * 同步投诉到 OKKI
 */
async function syncComplaintToOkki(complaintId) {
  console.log(chalk.cyan(`🔄 正在同步投诉记录 ${complaintId} 到 OKKI...`));
  
  try {
    const result = await okkiSyncController.syncComplaintToOKKI(complaintId);
    
    if (result.success) {
      printSuccess('同步成功!');
      console.log(`   投诉 ID: ${result.complaintId}`);
      console.log(`   客户：${result.companyName} (${result.companyId})`);
      console.log(`   OKKI Trail ID: ${result.trailId}`);
      console.log(`   跟进类型：售后跟进 (trail_type=${result.trailType})`);
      console.log(`   匹配方式：${result.matchType}`);
      console.log(`   日志 ID: ${result.logId}`);
    } else {
      printError('同步失败!');
      console.log(`   原因：${result.message}`);
      if (result.error) {
        console.log(`   错误：${result.error}`);
      }
      if (result.note) {
        console.log(`   提示：${result.note}`);
      }
    }
    
    return result;
  } catch (error) {
    printError(`同步失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 同步返单到 OKKI
 */
async function syncRepeatOrderToOkki(repeatOrderId) {
  console.log(chalk.cyan(`🔄 正在同步返单报价 ${repeatOrderId} 到 OKKI...`));
  
  try {
    const result = await okkiSyncController.syncRepeatOrderToOKKI(repeatOrderId);
    
    if (result.success) {
      printSuccess('同步成功!');
      console.log(`   返单 ID: ${result.repeatOrderId}`);
      console.log(`   客户：${result.companyName} (${result.companyId})`);
      console.log(`   OKKI Trail ID: ${result.trailId}`);
      console.log(`   跟进类型：售后跟进 (trail_type=${result.trailType})`);
      console.log(`   匹配方式：${result.matchType}`);
      console.log(`   日志 ID: ${result.logId}`);
    } else {
      printError('同步失败!');
      console.log(`   原因：${result.message}`);
      if (result.error) {
        console.log(`   错误：${result.error}`);
      }
      if (result.note) {
        console.log(`   提示：${result.note}`);
      }
    }
    
    return result;
  } catch (error) {
    printError(`同步失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 查看同步状态
 */
function showSyncStatus(id) {
  console.log(chalk.cyan(`📊 查询同步状态：${id}`));
  
  const log = OkkiSyncLogModule.getById(id);
  
  if (!log) {
    printError('未找到同步记录');
    return null;
  }
  
  console.log(`\n📋 同步日志详情:`);
  console.log(`   日志 ID: ${log.id}`);
  console.log(`   类型：${log.syncType === 'complaint' ? '投诉' : '返单'}`);
  
  if (log.complaintId) {
    console.log(`   投诉 ID: ${log.complaintId}`);
  }
  if (log.repeatOrderId) {
    console.log(`   返单 ID: ${log.repeatOrderId}`);
  }
  
  console.log(`   客户 ID: ${log.companyId || '(未关联)'}`);
  console.log(`   OKKI Trail ID: ${log.trailId || '(未生成)'}`);
  console.log(`   状态：${log.status === 'success' ? '✅ 成功' : log.status === 'failed' ? '❌ 失败' : '⏳ 待处理'}`);
  console.log(`   匹配方式：${log.matchType || '(无)'}`);
  console.log(`   同步时间：${log.syncedAt}`);
  
  if (log.errorMessage) {
    console.log(`   错误信息：${log.errorMessage}`);
  }
  if (log.retryCount > 0) {
    console.log(`   重试次数：${log.retryCount}`);
  }
  
  return log.toObject();
}

/**
 * 查看同步日志
 */
function showSyncLogs(options = {}) {
  const limit = options.limit || 10;
  const logs = OkkiSyncLogModule.getRecent(limit);
  
  if (logs.length === 0) {
    printInfo('暂无同步日志');
    return [];
  }
  
  console.log(chalk.cyan(`\n最近 ${logs.length} 条同步日志:\n`));
  
  logs.forEach((log, index) => {
    const statusIcon = log.status === 'success' ? '✅' : log.status === 'failed' ? '❌' : '⏳';
    const typeLabel = log.syncType === 'complaint' ? '投诉' : '返单';
    const businessId = log.complaintId || log.repeatOrderId;
    
    console.log(`${index + 1}. ${statusIcon} [${typeLabel}] ${businessId}`);
    console.log(`   日志 ID: ${log.id}`);
    console.log(`   客户 ID: ${log.companyId || '(未关联)'}`);
    console.log(`   Trail ID: ${log.trailId || '(未生成)'}`);
    console.log(`   时间：${log.syncedAt}`);
    if (log.errorMessage) {
      console.log(`   错误：${log.errorMessage}`);
    }
    console.log('');
  });
  
  return logs.map(log => log.toObject());
}

// ==================== 命令定义 ====================

program
  .name('after-sales-cli')
  .description('售后管理统一 CLI 工具')
  .version('1.0.0');

// ----- Complaint 命令 -----
const complaintCmd = program.command('complaint')
  .description('投诉管理');

complaintCmd.command('create')
  .description('创建投诉')
  .option('-c, --customer <customer>', '客户 ID')
  .option('-n, --customerName <name>', '客户名称')
  .option('-p, --product <product>', '产品 ID')
  .option('-P, --productName <name>', '产品名称')
  .option('-t, --type <type>', '投诉类型 (quality/delivery/packaging/other)')
  .option('-d, --description <desc>', '投诉描述')
  .option('-s, --severity <severity>', '严重程度 (low/medium/high)')
  .option('-a, --assignee <assignee>', '处理人')
  .action(createComplaint);

complaintCmd.command('list')
  .description('列出投诉')
  .option('-s, --status <status>', '按状态过滤')
  .option('-t, --type <type>', '按类型过滤')
  .option('-S, --severity <severity>', '按严重程度过滤')
  .action(listComplaints);

complaintCmd.command('get <complaintId>')
  .description('获取投诉详情')
  .action(getComplaint);

complaintCmd.command('update <complaintId>')
  .description('更新投诉')
  .option('-d, --description <desc>', '描述')
  .option('-t, --type <type>', '类型')
  .option('-s, --severity <severity>', '严重程度')
  .option('-S, --status <status>', '状态')
  .option('-T, --currentStep <step>', '当前步骤')
  .option('-a, --assignee <assignee>', '处理人')
  .action(updateComplaint);

complaintCmd.command('status <complaintId> <status>')
  .description('更新投诉状态')
  .action(updateComplaintStatus);

complaintCmd.command('assign <complaintId> <assignee>')
  .description('分配投诉')
  .action(assignComplaint);

complaintCmd.command('step <complaintId> <step>')
  .description('更新投诉步骤')
  .action(updateComplaintStep);

complaintCmd.command('satisfy <complaintId> <score>')
  .description('记录满意度评分')
  .action(recordSatisfaction);

complaintCmd.command('delete <complaintId>')
  .description('删除投诉')
  .action(deleteComplaint);

complaintCmd.command('stats')
  .description('投诉统计')
  .action(getComplaintStats);

// ----- Repeat-Order 命令 -----
const repeatOrderCmd = program.command('repeat-order')
  .description('返单报价管理');

repeatOrderCmd.command('create')
  .description('创建返单报价')
  .option('-c, --customer <customer>', '客户 ID')
  .option('-n, --customerName <name>', '客户名称')
  .option('-i, --initialOrder <order>', '初始订单 ID')
  .option('-r, --repeatOrder <order>', '返单订单 ID')
  .option('-I, --initialDate <date>', '初始订单日期 (YYYY-MM-DD)')
  .option('-A, --initialAmount <amount>', '初始订单金额')
  .option('-R, --repeatAmount <amount>', '返单金额')
  .option('-s, --status <status>', '状态')
  .option('-N, --notes <notes>', '备注')
  .action(createRepeatOrder);

repeatOrderCmd.command('list')
  .description('列出返单')
  .option('-s, --status <status>', '按状态过滤')
  .option('-c, --customer <customer>', '按客户过滤')
  .action(listRepeatOrders);

repeatOrderCmd.command('get <orderId>')
  .description('获取返单详情')
  .action(getRepeatOrder);

repeatOrderCmd.command('update <orderId>')
  .description('更新返单')
  .option('-s, --status <status>', '状态')
  .option('-R, --repeatAmount <amount>', '返单金额')
  .option('-N, --notes <notes>', '备注')
  .action(updateRepeatOrder);

// ----- Satisfaction 命令 -----
const satisfactionCmd = program.command('satisfaction')
  .description('满意度调查管理');

satisfactionCmd.command('create')
  .description('创建满意度调查')
  .option('-C, --complaintId <id>', '关联投诉 ID')
  .option('-c, --customer <customer>', '客户 ID')
  .option('-n, --customerName <name>', '客户名称')
  .option('-o, --overall <score>', '综合评分 (1-5)')
  .option('-q, --quality <score>', '产品质量评分 (1-5)')
  .option('-s, --service <score>', '服务质量评分 (1-5)')
  .option('-d, --delivery <score>', '物流配送评分 (1-5)')
  .option('-m, --communication <score>', '沟通效率评分 (1-5)')
  .option('-M, --comments <comments>', '备注')
  .action(createSatisfaction);

satisfactionCmd.command('list')
  .description('列出满意度调查')
  .option('-c, --customer <customer>', '按客户过滤')
  .action(listSatisfaction);

satisfactionCmd.command('get <surveyId>')
  .description('获取满意度调查详情')
  .action(getSatisfaction);

satisfactionCmd.command('stats')
  .description('满意度统计')
  .action(getSatisfactionStats);

// ----- Analytics 命令 -----
const analyticsCmd = program.command('analytics')
  .description('分析报表');

analyticsCmd.command('complaint')
  .description('投诉分析')
  .option('--range <range>', '日期范围 (YYYY-MM-DD_YYYY-MM-DD)')
  .action(analyzeComplaints);

analyticsCmd.command('repeat-order')
  .description('返单分析')
  .option('--range <range>', '日期范围')
  .action(analyzeRepeatOrders);

analyticsCmd.command('satisfaction')
  .description('满意度分析')
  .option('--range <range>', '日期范围')
  .action(analyzeSatisfaction);

analyticsCmd.command('risk')
  .description('客户风险分析')
  .action(analyzeRisk);

analyticsCmd.command('quality')
  .description('产品质量分析')
  .action(analyzeQuality);

analyticsCmd.command('summary')
  .description('综合摘要')
  .option('--range <range>', '日期范围')
  .action(analyzeSummary);

// ----- OKKI 命令 -----
const okkiCmd = program.command('okki')
  .description('OKKI 同步管理');

okkiCmd.command('sync-complaint <complaintId>')
  .description('同步投诉到 OKKI')
  .action(syncComplaintToOkki);

okkiCmd.command('sync-repeat-order <repeatOrderId>')
  .description('同步返单到 OKKI')
  .action(syncRepeatOrderToOkki);

okkiCmd.command('status <id>')
  .description('查看同步状态')
  .action(showSyncStatus);

okkiCmd.command('logs')
  .description('查看同步日志')
  .option('-l, --limit <limit>', '限制数量', '10')
  .action(showSyncLogs);

// 解析命令行
program.parse(process.argv);

// 如果没有提供任何参数，显示帮助
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
