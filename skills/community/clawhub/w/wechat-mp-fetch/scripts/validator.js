/**
 * URL验证模块
 * 负责验证微信公众号文章链接的有效性
 */

/**
 * 验证URL是否为有效的微信公众号文章链接
 * @param {string} url - 要验证的URL
 * @returns {boolean} 是否为有效的微信公众号文章链接
 */
function validateWeChatUrl(url) {
  if (!url) {
    return false;
  }
  
  // 检查是否包含微信公众号域名
  if (!url.includes('mp.weixin.qq.com')) {
    return false;
  }
  
  // 检查是否为文章链接（通常包含 /s/ 路径）
  if (!url.includes('/s/')) {
    return false;
  }
  
  return true;
}

/**
 * 验证URL格式是否正确
 * @param {string} url - 要验证的URL
 * @returns {boolean} URL格式是否正确
 */
function validateUrlFormat(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

module.exports = {
  validateWeChatUrl,
  validateUrlFormat
};
