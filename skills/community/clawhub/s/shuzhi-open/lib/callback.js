/**
 * 回调验签模块（MD5）
 * 用于验证电子签章组件的回调签名
 */

const crypto = require('crypto');

/**
 * 生成回调签名
 * 签名规则：
 * 1. 参数按 key 字典序排序（排除 sign 字段）
 * 2. 拼接 key=value，用 & 连接
 * 3. 末尾追加 &appSecret=xxx
 * 4. MD5 加密，转小写
 * 
 * @param {object} params - 回调参数
 * @param {string} appSecret - 应用 appSecret
 * @returns {string} MD5签名（小写）
 */
function generateCallbackSign(params, appSecret) {
  const sortedKeys = Object.keys(params)
    .filter(key => key !== 'sign')
    .sort();
  
  const str = sortedKeys
    .map(key => `${key}=${params[key]}`)
    .join('&') + `&appSecret=${appSecret}`;
  
  return crypto.createHash('md5').update(str).digest('hex').toLowerCase();
}

/**
 * 验证回调签名
 * @param {object} params - 回调参数（包含 sign 字段）
 * @param {string} appSecret - 应用 appSecret
 * @returns {boolean} 验签通过返回 true
 */
function verifyCallback(params, appSecret) {
  const { sign } = params;
  
  if (!sign) {
    return false;
  }
  
  const expectedSign = generateCallbackSign(params, appSecret);
  return sign === expectedSign;
}

/**
 * 解析回调数据
 * @param {object} params - 回调参数
 * @param {string} appSecret - 应用 appSecret
 * @returns {object|null} 验签成功返回解析后的数据，失败返回 null
 */
function parseCallback(params, appSecret) {
  if (!verifyCallback(params, appSecret)) {
    return null;
  }
  
  // 解析 signerList（可能是 JSON 字符串）
  if (params.signerList && typeof params.signerList === 'string') {
    try {
      params.signerList = JSON.parse(params.signerList);
    } catch (e) {
      // 保持原样
    }
  }
  
  return {
    signFlowId: params.signFlowId,
    signStatus: params.signStatus,
    createStatus: params.createStatus,
    templateId: params.templateId,
    templateStatus: params.templateStatus,
    fileId: params.fileId,
    signerList: params.signerList,
    timestamp: params.timestamp,
    nonce: params.nonce,
    appKey: params.appKey
  };
}

module.exports = {
  generateCallbackSign,
  verifyCallback,
  parseCallback
};