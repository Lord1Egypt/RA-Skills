/**
 * 工具函数模块
 * 包含下载、验证、缓存等通用功能
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const NodeCache = require('node-cache');

// 缓存实例（1 小时 TTL）
const cache = new NodeCache({ stdTTL: 3600, checkperiod: 600 });

/**
 * 验证 API Key 是否配置
 * @returns {boolean}
 */
function validateApiKey() {
  const apiKey = process.env.VOLC_API_KEY;
  return !!(apiKey && apiKey.length > 10);
}

/**
 * 生成唯一的文件名
 * @param {string} prefix - 文件名前缀
 * @returns {string}
 */
function generateFilename(prefix = 'volc') {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}.png`;
}

/**
 * 下载图片到本地
 * @param {string} url - 图片 URL
 * @param {string} filename - 文件名
 * @param {string} saveDir - 保存目录
 * @returns {Promise<string>} 本地文件路径
 */
async function downloadImage(url, filename, saveDir = '/tmp/openclaw') {
  try {
    // 确保目录存在
    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, { recursive: true });
    }

    const filePath = path.join(saveDir, filename);
    
    const response = await axios.get(url, {
      responseType: 'arraybuffer',
      timeout: 60000
    });

    fs.writeFileSync(filePath, response.data);
    
    console.log(`✅ 图片已保存到：${filePath}`);
    return filePath;
  } catch (error) {
    console.error('❌ 下载图片失败:', error.message);
    throw error;
  }
}

/**
 * 将本地文件转换为 Base64
 * @param {string} filePath - 文件路径
 * @returns {string} Base64 字符串
 */
function fileToBase64(filePath) {
  const data = fs.readFileSync(filePath);
  return data.toString('base64');
}

/**
 * 从 URL 或本地路径加载图片
 * @param {string} image - URL 或本地路径
 * @returns {Promise<string>} Base64 字符串
 */
async function loadImage(image) {
  if (image.startsWith('http://') || image.startsWith('https://')) {
    // 下载远程图片
    const filename = generateFilename('input');
    const localPath = await downloadImage(image, filename);
    return fileToBase64(localPath);
  } else if (fs.existsSync(image)) {
    // 本地文件
    return fileToBase64(image);
  } else {
    throw new Error('无效的图片来源：必须是 URL 或有效的本地文件路径');
  }
}

/**
 * 从缓存获取数据
 * @param {string} key - 缓存键
 * @returns {any} 缓存数据或 undefined
 */
function getFromCache(key) {
  return cache.get(key);
}

/**
 * 设置缓存
 * @param {string} key - 缓存键
 * @param {any} value - 缓存值
 */
function setCache(key, value) {
  cache.set(key, value);
}

/**
 * 生成缓存键（基于 prompt 和参数）
 * @param {string} prompt - 提示词
 * @param {object} params - 其他参数
 * @returns {string}
 */
function generateCacheKey(prompt, params = {}) {
  const paramsStr = JSON.stringify(params, Object.keys(params).sort());
  return `img:${Buffer.from(prompt + paramsStr).toString('base64').substring(0, 64)}`;
}

/**
 * 延迟执行
 * @param {number} ms - 毫秒数
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 指数退避计算
 * @param {number} attempt - 当前尝试次数（从 1 开始）
 * @param {number} baseDelay - 基础延迟（毫秒）
 * @returns {number} 延迟时间（毫秒）
 */
function calculateBackoff(attempt, baseDelay = 1000) {
  return baseDelay * Math.pow(2, attempt - 1);
}

module.exports = {
  validateApiKey,
  generateFilename,
  downloadImage,
  fileToBase64,
  loadImage,
  getFromCache,
  setCache,
  generateCacheKey,
  sleep,
  calculateBackoff
};
