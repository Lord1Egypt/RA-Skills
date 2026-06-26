/**
 * 工具函数模块
 */

/**
 * 延迟函数
 */
export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 安全的 JSON 解析
 */
export function safeJsonParse(str, defaultValue = null) {
  try {
    return JSON.parse(str);
  } catch {
    return defaultValue;
  }
}

/**
 * 格式化数字（如：1.2万）
 */
export function formatNumber(num) {
  if (typeof num === 'string') {
    num = parseFloat(num);
  }
  if (isNaN(num)) return '0';
  
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toString();
}

/**
 * 截断文本
 */
export function truncateText(text, maxLength) {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

/**
 * 验证 URL 格式
 */
export function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch {
    return false;
  }
}

/**
 * 判断是否为本地文件路径
 */
export function isLocalPath(path) {
  return (
    path.startsWith('/') ||
    path.startsWith('./') ||
    path.startsWith('../') ||
    /^[A-Za-z]:/.test(path) // Windows 路径
  );
}

/**
 * 日志工具
 */
export const logger = {
  info: (msg) => console.error(`[INFO] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`),
  warn: (msg) => console.error(`[WARN] ${msg}`),
  debug: (msg) => {
    if (process.env.DEBUG) {
      console.error(`[DEBUG] ${msg}`);
    }
  },
};
