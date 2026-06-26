/**
 * 自动化取证模块
 * 支持拼多多、淘宝、抖音、公众号取证
 */

const { request, getConfig } = require('../client');

/**
 * 创建批量取证任务
 * @param {string} batchId - 批次ID
 * @param {Array<object>} tasks - 任务列表
 * @returns {Promise<{batch_id: string, ws_url: string, url: string, bind_time: string}>}
 */
async function createTask(batchId, tasks) {
  const result = await request('evidence', 'createTask', { 
    batch_id: batchId, 
    tasks 
  });
  return result.data;
}

/**
 * 创建公众号取证任务
 * @param {Array<object>} tasks - 任务列表
 * @returns {Promise<object>}
 */
async function createWechatTask(tasks) {
  const result = await request('evidence', 'createWechatTask', { tasks });
  return result.data;
}

/**
 * 查询批次状态
 * @param {string} batchId - 批次ID
 * @returns {Promise<object>}
 */
async function queryBatch(batchId) {
  const result = await request('evidence', 'queryBatch', { batch_id: batchId });
  return result.data;
}

/**
 * 查询单个任务
 * @param {string} attId - 任务ID
 * @returns {Promise<object>}
 */
async function queryTask(attId) {
  const result = await request('evidence', 'queryTask', { att_id: attId });
  return result.data;
}

/**
 * 获取证据包下载地址
 * @param {string} attId - 任务ID
 * @returns {Promise<{url: string, expire_time: string}>}
 */
async function downloadZip(attId) {
  const result = await request('evidence', 'downloadZip', { att_id: attId });
  return result.data;
}

/**
 * 检查是否有空闲机器
 * @returns {Promise<{has_device: boolean}>}
 */
async function checkDevice() {
  const result = await request('evidence', 'checkDevice', {});
  return result.data;
}

/**
 * 分配机器
 * @param {string} batchId - 批次ID
 * @param {string} [callbackFailedUrl] - 失败回调URL
 * @returns {Promise<{ws_url: string, assigned_time: string}>}
 */
async function assignDevice(batchId, callbackFailedUrl) {
  const body = { batch_id: batchId };
  if (callbackFailedUrl) {
    body.callback_failed_url = callbackFailedUrl;
  }
  const result = await request('evidence', 'assignDevice', body);
  return result.data;
}

/**
 * 轮询等待任务完成
 * @param {string} attId - 任务ID
 * @param {object} options - 选项
 * @returns {Promise<object>}
 */
async function waitForComplete(attId, options = {}) {
  const { interval = 5000, timeout = 600000, onProgress } = options;
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    const task = await queryTask(attId);
    
    if (onProgress) {
      onProgress(task);
    }
    
    if (task.status === 'SUCCESSED') {
      return task;
    }
    
    if (task.status === 'FAILED') {
      throw new Error(`取证失败: ${task.error_msg || '未知错误'}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  
  throw new Error('等待取证超时');
}

/**
 * 轮询等待批次完成
 * @param {string} batchId - 批次ID
 * @param {object} options - 选项
 * @returns {Promise<object>}
 */
async function waitForBatchComplete(batchId, options = {}) {
  const { interval = 10000, timeout = 1800000, onProgress } = options;
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    const batch = await queryBatch(batchId);
    
    if (onProgress) {
      onProgress(batch);
    }
    
    if (batch.status === 'SUCCESSED') {
      return batch;
    }
    
    if (batch.status === 'FAILED') {
      throw new Error(`批次失败: ${batch.message || '未知错误'}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  
  throw new Error('等待批次超时');
}

/**
 * 获取取证类型说明
 * @param {number} type - 类型代码
 * @returns {string} 类型说明
 */
function getTypeText(type) {
  const config = getConfig();
  const types = config.products?.evidence?.types || {};
  return types[type] || `未知类型(${type})`;
}

/**
 * 获取批次状态说明
 * @param {string} status - 状态码
 * @returns {string} 状态说明
 */
function getBatchStatusText(status) {
  const config = getConfig();
  const statusMap = config.products?.evidence?.batchStatus || {};
  return statusMap[status] || status;
}

/**
 * 获取任务状态说明
 * @param {string} status - 状态码
 * @returns {string} 状态说明
 */
function getTaskStatusText(status) {
  const config = getConfig();
  const statusMap = config.products?.evidence?.taskStatus || {};
  return statusMap[status] || status;
}

module.exports = {
  createTask,
  createWechatTask,
  queryBatch,
  queryTask,
  downloadZip,
  checkDevice,
  assignDevice,
  waitForComplete,
  waitForBatchComplete,
  getTypeText,
  getBatchStatusText,
  getTaskStatusText
};