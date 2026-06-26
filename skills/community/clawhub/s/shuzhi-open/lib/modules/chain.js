/**
 * 区块链API服务模块
 * 支持数据上链、批量查询上链结果
 */

const { request, getConfig } = require('../client');

/**
 * 生成请求ID
 * @returns {string} UUID格式的请求ID
 */
function generateRequestId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * 数据上链
 * @param {string} data - 业务数据（JSON字符串或对象）
 * @param {object} options - 可选参数
 * @param {string[]} [options.business] - 业务名，如 ['EVIDENCE_PRESERVATION']
 * @param {string[]} [options.source] - 来源，如 ['BQ_INTERNATIONAL']
 * @param {string} [options.requestId] - 请求ID，不传则自动生成
 * @param {string[]} [options.extension] - 扩展内容
 * @returns {Promise<{index: string, requestId: string}>} 交易索引和请求ID
 * 
 * @example
 * const result = await chain.upload('{"ano":"BQ123","sha256":"xxx"}');
 * console.log(result.index); // 'd670b1db-926c-4e71-bf65-92df6c3b8aeb'
 */
async function upload(data, options = {}) {
  const { 
    business, 
    source, 
    requestId = generateRequestId(),
    extension 
  } = options;
  
  // 构建请求体
  const body = {
    data: typeof data === 'object' ? JSON.stringify(data) : data,
    requestId
  };
  
  // 添加可选字段
  if (business) body.business = business;
  if (source) body.source = source;
  if (extension) body.extension = extension;
  
  const result = await request('chain', 'upload', body);
  
  return {
    index: result.data.index,
    requestId
  };
}

/**
 * 批量查询上链结果
 * @param {string[]} indexList - 交易索引号列表
 * @returns {Promise<Array>} 上链结果列表
 * 
 * @example
 * const result = await chain.queryResult(['d670b1db-926c-4e71-bf65-92df6c3b8aeb']);
 * // result[0].chain_results[0].status: 1=成功
 */
async function queryResult(indexList) {
  const result = await request('chain', 'queryResult', { index_list: indexList });
  return result.data;
}

/**
 * 等待上链完成（轮询）
 * @param {string} index - 交易索引
 * @param {object} options - 选项
 * @param {number} options.interval - 轮询间隔（毫秒），默认 5000
 * @param {number} options.timeout - 超时时间（毫秒），默认 300000
 * @returns {Promise<object>} 上链结果
 */
async function waitUntilUploaded(index, options = {}) {
  const { interval = 5000, timeout = 300000 } = options;
  const startTime = Date.now();
  
  while (Date.now() - startTime < timeout) {
    const results = await queryResult([index]);
    
    if (results && results.length > 0) {
      const chainResults = results[0].chain_results;
      if (chainResults && chainResults.length > 0) {
        const status = chainResults[0].status;
        
        // 1 = 上链成功
        if (status === 1) {
          return results[0];
        }
        
        // 0 = 上链失败
        if (status === 0) {
          throw new Error(`上链失败，状态: ${status}`);
        }
      }
    }
    
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  
  throw new Error('等待上链超时');
}

/**
 * 获取链类型列表
 * @returns {string[]} 支持的链类型
 */
function getSupportedChains() {
  const config = getConfig();
  return config.products?.chain?.chains || ['tritium', 'conflux'];
}

/**
 * 获取状态说明
 * @param {number} status - 状态码
 * @returns {string} 状态说明
 */
function getStatusText(status) {
  const config = getConfig();
  const statusMap = config.products?.chain?.status || {};
  return statusMap[status] || `未知状态(${status})`;
}

module.exports = {
  upload,
  queryResult,
  waitUntilUploaded,
  getSupportedChains,
  getStatusText,
  generateRequestId
};