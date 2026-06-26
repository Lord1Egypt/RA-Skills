/**
 * CAP-保管单组件模块
 * 用于生成和下载保管单 PDF 文件
 */

const { request } = require('../client');

/**
 * 生成保管单
 * @param {object} params - 保管单参数
 * @returns {Promise<{certNo: string}>} 存证编号
 */
async function create(params) {
  const result = await request('certificate', 'create', params);
  return result.data;
}

/**
 * 获取保管单下载地址
 * @param {string} certNo - 存证编号
 * @returns {Promise<{url: string}>}
 */
async function download(certNo) {
  const result = await request('certificate', 'download', { certNo });
  return {
    url: result.data
  };
}

/**
 * 获取客户模板列表
 * @returns {Promise<Array>}
 */
async function listTemplates() {
  const result = await request('certificate', 'listTemplates', {});
  return result.data;
}

/**
 * 生成保管单并等待完成
 * @param {object} params - 保管单参数
 * @param {number} [timeout] - 超时时间（毫秒）
 * @returns {Promise<{certNo: string, url: string}>}
 */
async function createAndGetUrl(params, options = {}) {
  const { timeout = 60000 } = options;
  
  const certNo = await create(params);
  
  if (!certNo) {
    throw new Error('生成保管单失败：未返回存证编号');
  }
  
  const startTime = Date.now();
  let lastError = null;
  
  while (Date.now() - startTime < timeout) {
    try {
      const downloadResult = await download(certNo);
      if (downloadResult.url) {
        return {
          certNo,
          url: downloadResult.url
        };
      }
    } catch (error) {
      lastError = error;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  return {
    certNo,
    url: null,
    error: lastError?.message || '获取下载地址超时'
  };
}

module.exports = {
  create,
  download,
  listTemplates,
  createAndGetUrl
};