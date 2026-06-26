/**
 * 统一 HTTP 客户端
 */

const { buildHeaders } = require('./auth');
const { validateConfig, getEndpointConfig } = require('./validate');

let _config = null;

/**
 * 初始化配置
 * @param {object} config - 配置对象
 */
function init(config) {
  validateConfig(config);
  _config = config;
}

/**
 * 获取当前配置
 * @returns {object} 配置对象
 */
function getConfig() {
  if (!_config) {
    throw new Error('未初始化，请先调用 init(config)');
  }
  return _config;
}

/**
 * 获取凭证
 * @returns {object} { appKey, appSecret }
 */
function getCredentials() {
  const config = getConfig();
  
  if (!config.appKey || !config.appSecret) {
    throw new Error(
      '\n❌ 凭证未配置\n' +
      '   请在 config.json 中配置 appKey 和 appSecret\n'
    );
  }
  
  return {
    appKey: config.appKey,
    appSecret: config.appSecret
  };
}

/**
 * 统一请求方法
 * @param {string} product - 产品名称，如 'chain', 'evidence', 'certificate', 'sign'
 * @param {string} endpoint - 端点名称，如 'upload', 'queryResult'
 * @param {object} body - 请求体
 * @returns {Promise<object>} 响应数据
 */
async function request(product, endpoint, body) {
  const { path, productId } = getEndpointConfig(_config, product, endpoint);
  const credentials = getCredentials();
  
  const url = `${_config.baseUrl}${path}`;
  const headers = buildHeaders('POST', path, body, {
    appKey: credentials.appKey,
    appSecret: credentials.appSecret,
    productId
  });
  
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  });
  
  const data = await response.json();
  
  // 检查全局响应
  if (data.code !== 200) {
    const error = new Error(data.message || `API Error: ${data.code}`);
    error.code = data.code;
    error.response = data;
    throw error;
  }
  
  // 检查服务响应
  if (data.data && data.data.code !== undefined) {
    const serviceCode = data.data.code;
    // 兼容字符串和数字类型的状态码
    if (serviceCode !== 0 && serviceCode !== '0' && serviceCode !== '200' && serviceCode !== 200) {
      const error = new Error(data.data.msg || data.data.message || `Service Error: ${serviceCode}`);
      error.code = serviceCode;
      error.response = data;
      throw error;
    }
  }
  
  return data.data;
}

/**
 * 带重试的请求
 * @param {string} product - 产品名称
 * @param {string} endpoint - 端点名称
 * @param {object} body - 请求体
 * @param {number} retries - 重试次数，默认 3
 * @param {number} delay - 重试间隔（毫秒），默认 1000
 * @returns {Promise<object>} 响应数据
 */
async function requestWithRetry(product, endpoint, body, retries = 3, delay = 1000) {
  let lastError;
  
  for (let i = 0; i < retries; i++) {
    try {
      return await request(product, endpoint, body);
    } catch (error) {
      lastError = error;
      
      // 某些错误不应该重试
      if (error.code === 401 || error.code === 403) {
        throw error;
      }
      
      if (i < retries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
}

/**
 * 下载文件
 * @param {string} product - 产品名称
 * @param {string} endpoint - 端点名称
 * @param {object} body - 请求体
 * @returns {Promise<{buffer: Buffer, contentType: string}>}
 */
async function downloadFile(product, endpoint, body) {
  const { path, productId } = getEndpointConfig(_config, product, endpoint);
  const credentials = getCredentials();
  
  const url = `${_config.baseUrl}${path}`;
  const headers = buildHeaders('POST', path, body, {
    appKey: credentials.appKey,
    appSecret: credentials.appSecret,
    productId
  });
  
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  });
  
  if (!response.ok) {
    throw new Error(`Download failed: ${response.status}`);
  }
  
  const buffer = await response.arrayBuffer();
  const contentType = response.headers.get('content-type');
  
  return {
    buffer: Buffer.from(buffer),
    contentType
  };
}

module.exports = {
  init,
  getConfig,
  getCredentials,
  request,
  requestWithRetry,
  downloadFile
};