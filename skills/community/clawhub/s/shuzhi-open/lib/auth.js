/**
 * HMAC-SHA256 签名模块
 * 用于生成 X-HMAC-SIGNATURE 和 X-HMAC-DIGEST
 */

const crypto = require('crypto');

/**
 * 生成 GMT 格式时间
 * @returns {string} GMT格式时间，如 "Tue, 06 Aug 2024 07:15:26 GMT"
 */
function getGMTDate() {
  return new Date().toUTCString();
}

/**
 * 生成全局签名 X-HMAC-SIGNATURE
 * 签名公式: HMAC-SHA256-HEX(appSecret, signingString)
 * signingString = HTTP Method + \n + URI + \n + "" + \n + appKey + \n + Date + \n
 * 
 * @param {string} method - HTTP方法，如 "POST"
 * @param {string} uri - 请求路径，如 "/1848921633505587202"
 * @param {string} appKey - 应用 appKey
 * @param {string} date - GMT格式时间
 * @param {string} appSecret - 应用 appSecret
 * @returns {string} Base64编码的签名
 */
function signRequest(method, uri, appKey, date, appSecret) {
  const signingString = `${method}\n${uri}\n\n${appKey}\n${date}\n`;
  
  return crypto
    .createHmac('sha256', appSecret)
    .update(signingString)
    .digest('base64');
}

/**
 * 生成 Body 签名 X-HMAC-DIGEST
 * 签名公式: HMAC-SHA256-HEX(appSecret, body)
 * 
 * @param {object|string} body - 请求体
 * @param {string} appSecret - 应用 appSecret
 * @returns {string} Base64编码的签名
 */
function signBody(body, appSecret) {
  const bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
  
  return crypto
    .createHmac('sha256', appSecret)
    .update(bodyStr)
    .digest('base64');
}

/**
 * 构建完整的请求头
 * 
 * @param {string} method - HTTP方法
 * @param {string} uri - 请求路径
 * @param {object|string} body - 请求体
 * @param {object} config - 配置对象 { appKey, appSecret, productId }
 * @returns {object} 完整的请求头对象
 */
function buildHeaders(method, uri, body, config) {
  const date = getGMTDate();
  const bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
  
  return {
    'X-HMAC-ACCESS-KEY': config.appKey,
    'X-APP-PRODUCT-ID': config.productId,
    'X-HMAC-ALGORITHM': 'hmac-sha256',
    'X-HMAC-SIGNATURE': signRequest(method, uri, config.appKey, date, config.appSecret),
    'X-HMAC-DIGEST': signBody(bodyStr, config.appSecret),
    'Date': date,
    'Content-Type': 'application/json'
  };
}

module.exports = {
  buildHeaders,
  signRequest,
  signBody,
  getGMTDate
};