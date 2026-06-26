/**
 * CDP连接辅助工具
 * 获取Chrome远程调试的WebSocket URL并连接
 */
const http = require('http');

/**
 * 获取Chrome WebSocket调试URL
 * @returns {Promise<string>} WebSocket URL
 */
async function getChromeWSUrl() {
  return new Promise((resolve, reject) => {
    http.get('http://localhost:9222/json/version', res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.webSocketDebuggerUrl);
        } catch (e) {
          reject(new Error('Failed to parse Chrome debug info'));
        }
      });
    }).on('error', reject);
  });
}

/**
 * 连接到Chrome并返回浏览器实例
 * @param {object} options - 连接选项
 * @returns {Promise<Browser>} Playwright浏览器实例
 */
async function connectToChrome(options = {}) {
  const { chromium } = require('playwright');
  const wsUrl = await getChromeWSUrl();
  return await chromium.connectOverCDP(wsUrl, options);
}

/**
 * 创建带上下文的浏览器实例
 * @param {string} storageStatePath - 可选，存储状态文件路径
 * @returns {Promise<{browser: Browser, context: BrowserContext, page: Page}>}
 */
async function createBrowserContext(storageStatePath = null) {
  const { chromium } = require('playwright');
  const wsUrl = await getChromeWSUrl();
  const browser = await chromium.connectOverCDP(wsUrl);

  const contextOptions = {};
  if (storageStatePath) {
    contextOptions.storageState = storageStatePath;
  }

  const context = await browser.newContext(contextOptions);
  const page = await context.newPage();

  return { browser, context, page };
}

module.exports = {
  getChromeWSUrl,
  connectToChrome,
  createBrowserContext
};
