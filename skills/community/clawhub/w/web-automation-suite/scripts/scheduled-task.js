/**
 * 定时任务辅助工具
 * 支持cron式定时执行监控任务
 */

const http = require('http');

/**
 * 获取Chrome WebSocket URL
 */
async function getChromeWSUrl() {
  return new Promise((resolve, reject) => {
    http.get('http://localhost:9222/json/version', res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data).webSocketDebuggerUrl);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/**
 * 解析简单cron表达式
 * @param {string} cron - cron表达式
 * @returns {number} 间隔毫秒数（仅支持简单格式）
 */
function parseSimpleCron(cron) {
  const parts = cron.trim().split(/\s+/);
  if (parts.length === 5) {
    const [min, hour, day, month, dow] = parts;
    // 简化版：仅支持每分钟、每小时、每天
    if (min === '*' && hour === '*') return 60000;
    if (min === '*/5' && hour === '*') return 5 * 60000;
    if (min === '*/15') return 15 * 60000;
    if (min === '*/30') return 30 * 60000;
    if (min === '0' && hour === '*') return 3600000;
  }
  // 默认60秒
  return 60000;
}

/**
 * 创建定时任务
 * @param {object} config - 任务配置
 * @param {string} config.name - 任务名称
 * @param {string} config.url - 监控URL
 * @param {Function} config.extractor - 数据提取函数
 * @param {string} config.cron - cron表达式
 * @param {string} config.outputFile - 输出文件路径
 */
async function createScheduledTask(config) {
  const { chromium } = require('playwright');
  const fs = require('fs');

  const {
    name,
    url,
    extractor,
    cron = '*/60 * * * *',
    outputFile = `./${name}-log.json`
  } = config;

  const interval = parseSimpleCron(cron);
  const wsUrl = await getChromeWSUrl();

  console.log(`[${name}] Starting scheduled task, interval: ${interval}ms`);

  async function runOnce() {
    let browser;
    try {
      browser = await chromium.connectOverCDP(wsUrl);
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

      const data = await extractor(page);
      const record = {
        timestamp: new Date().toISOString(),
        url,
        data
      };

      // 保存数据
      let logs = [];
      if (fs.existsSync(outputFile)) {
        try {
          logs = JSON.parse(fs.readFileSync(outputFile, 'utf8'));
        } catch (e) {
          logs = [];
        }
      }
      logs.push(record);

      // 保留最近1000条记录
      if (logs.length > 1000) {
        logs = logs.slice(-1000);
      }

      fs.writeFileSync(outputFile, JSON.stringify(logs, null, 2));
      console.log(`[${name}] ${new Date().toISOString()} - Data saved`);
    } catch (e) {
      console.error(`[${name}] Error:`, e.message);
    } finally {
      if (browser) await browser.close();
    }
  }

  // 立即执行一次
  await runOnce();

  // 定时执行
  return setInterval(runOnce, interval);
}

/**
 * 价格监控任务
 * @param {string} url - 商品页面URL
 * @param {string} priceSelector - 价格选择器
 * @param {string} name - 商品名称
 */
async function priceMonitor(url, priceSelector, name = 'Product') {
  return createScheduledTask({
    name: `price-${name}`,
    url,
    extractor: async (page) => {
      const price = await page.textContent(priceSelector);
      return { name, price: price?.trim() };
    },
    cron: '*/15 * * * *',
    outputFile: `./price-monitor-${name}.json`
  });
}

/**
 * 内容变更监控
 * @param {string} url - 监控URL
 * @param {string} selector - 内容选择器
 * @param {string} name - 名称
 */
async function contentMonitor(url, selector, name = 'Content') {
  let lastContent = null;

  return createScheduledTask({
    name: `content-${name}`,
    url,
    extractor: async (page) => {
      await page.waitForSelector(selector);
      const content = await page.textContent(selector);

      const result = {
        name,
        content: content?.trim(),
        changed: content !== lastContent
      };

      lastContent = content;
      return result;
    },
    cron: '*/5 * * * *',
    outputFile: `./content-monitor-${name}.json`
  });
}

module.exports = {
  getChromeWSUrl,
  parseSimpleCron,
  createScheduledTask,
  priceMonitor,
  contentMonitor
};
