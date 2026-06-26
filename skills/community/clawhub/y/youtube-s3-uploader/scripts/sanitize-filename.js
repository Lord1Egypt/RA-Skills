// 文件名清理函数
// 移除特殊字符，只保留中文、英文字母、数字，限制长度

const path = require('path');

/**
 * 清理文件名
 * @param {string} fileName - 原始文件名
 * @param {number} maxLength - 最大长度（不包括扩展名）
 * @returns {string} 清理后的文件名
 */
function sanitizeFileName(fileName, maxLength = 100) {
  // 获取文件扩展名
  const ext = path.extname(fileName).toLowerCase();
  
  // 移除扩展名和路径，只保留基本名
  const baseName = fileName.replace(ext, '');
  
  // 移除所有特殊字符（表情符号、标点、空格等）
  // 只保留中文、英文字母、数字、连字符
  const sanitized = baseName.replace(/[^\u4e00-\u9fa5\u4e00-\u9fa5a-zA-Z0-9_]/g, '');
  
  // 如果清理后的文件名为空，使用默认名
  let resultName = sanitized || 'video';
  
  // 限制长度（不包括扩展名）
  if (resultName.length > maxLength) {
    resultName = resultName.substring(0, maxLength);
  }
  
  // 加上扩展名
  return resultName + ext;
}

/**
 * 生成简单的文件名（用于上传）
 * @param {string} originalName - 原始文件名
 * @param {string} prefix - 文件名前缀
 * @param {number} index - 文件索引
 * @returns {string} 生成的简单文件名
 */
function generateSimpleFileName(originalName, prefix = 'video', index = 1) {
  const ext = path.extname(originalName).toLowerCase();
  
  // 生成简单的文件名：prefix-index.ext
  // 只使用字母、数字和连字符
  const simpleBase = `${prefix}-${index}`;
  
  return simpleBase + ext;
}

module.exports = {
  sanitizeFileName,
  generateSimpleFileName
};
