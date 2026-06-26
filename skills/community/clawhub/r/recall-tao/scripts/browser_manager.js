/**
 * 浏览器重启管理器
 * 职责：管理浏览器生命周期、崩溃恢复、资源清理
 */

const path = require('path');
const fs = require('fs');

// 动态加载 playwright（可选依赖）
let chromium = null;
try {
  chromium = require('playwright').chromium;
} catch (e) {
  console.log('[BrowserManager] playwright 未安装，浏览器管理功能不可用');
}

// 配置
const config = {
  // 浏览器启动配置
  browser: {
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-infobars',
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  },
  
  // 上下文配置
  context: {
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  },
  
  // 保活配置
  keepAlive: {
    enabled: true,
    intervalMs: 60000,  // 1分钟检查一次
    maxIdleTimeMs: 30 * 60 * 1000  // 30分钟无操作视为空闲
  },
  
  // 重启配置
  restart: {
    maxCrashCount: 3,      // 最大崩溃次数
    crashWindowMs: 300000, // 5分钟内
    cooldownMs: 10000      // 重启冷却时间
  },
  
  // 用户数据目录（持久化登录）
  userDataDir: path.join(process.env.LOCALAPPDATA || process.env.TEMP, 'douyin-automation-browser')
};

// 状态
let state = {
  browser: null,
  context: null,
  page: null,
  isRunning: false,
  startTime: null,
  lastActivityTime: null,
  crashCount: 0,
  crashTimestamps: [],
  restartCount: 0
};

// 事件监听器
const listeners = {
  onBrowserStart: [],
  onBrowserClose: [],
  onBrowserCrash: [],
  onPageReady: []
};

/**
 * 启动浏览器
 * @param {Object} options - 启动选项
 * @returns {Promise<{browser, context, page}>}
 */
async function startBrowser(options = {}) {
  console.log('[BrowserManager] 启动浏览器...');
  
  // 检查 playwright 是否可用
  if (!chromium) {
    throw new Error('playwright 未安装，请先安装: npm install playwright');
  }
  
  try {
    // 清理旧实例
    if (state.browser) {
      await stopBrowser();
    }
    
    // 确保用户数据目录存在
    if (!fs.existsSync(config.userDataDir)) {
      fs.mkdirSync(config.userDataDir, { recursive: true });
    }
    
    // 启动浏览器
    state.browser = await chromium.launch({
      ...config.browser,
      ...options
    });
    
    // 创建上下文（使用持久化存储）
    state.context = await state.browser.newContext({
      ...config.context,
      storageState: options.storageState
    });
    
    // 创建页面
    state.page = await state.context.newPage();
    
    // 设置事件监听
    setupEventListeners();
    
    // 更新状态
    state.isRunning = true;
    state.startTime = new Date().toISOString();
    state.lastActivityTime = state.startTime;
    
    console.log('[BrowserManager] ✅ 浏览器启动成功');
    
    // 触发事件
    emit('onBrowserStart', { state });
    
    return {
      browser: state.browser,
      context: state.context,
      page: state.page
    };
    
  } catch (error) {
    console.error('[BrowserManager] 启动失败:', error.message);
    throw error;
  }
}

/**
 * 停止浏览器
 */
async function stopBrowser() {
  console.log('[BrowserManager] 停止浏览器...');
  
  try {
    if (state.page && !state.page.isClosed()) {
      await state.page.close().catch(() => {});
    }
    
    if (state.context) {
      await state.context.close().catch(() => {});
    }
    
    if (state.browser && state.browser.isConnected()) {
      await state.browser.close().catch(() => {});
    }
    
    // 重置状态
    state.browser = null;
    state.context = null;
    state.page = null;
    state.isRunning = false;
    
    console.log('[BrowserManager] ✅ 浏览器已停止');
    
    emit('onBrowserClose', { state });
    
  } catch (error) {
    console.error('[BrowserManager] 停止失败:', error.message);
  }
}

/**
 * 重启浏览器
 * @param {Object} options - 重启选项
 */
async function restartBrowser(options = {}) {
  console.log('[BrowserManager] 重启浏览器...');
  
  // 检查是否在冷却期
  const cooldownEnd = state.lastRestartTime 
    ? new Date(state.lastRestartTime).getTime() + config.restart.cooldownMs 
    : 0;
  
  if (Date.now() < cooldownEnd) {
    const waitMs = cooldownEnd - Date.now();
    console.log(`[BrowserManager] 冷却中，等待 ${waitMs}ms...`);
    await sleep(waitMs);
  }
  
  state.restartCount++;
  state.lastRestartTime = new Date().toISOString();
  
  await stopBrowser();
  await sleep(1000);
  
  return startBrowser(options);
}

/**
 * 设置事件监听器
 */
function setupEventListeners() {
  // 浏览器断开连接
  state.browser.on('disconnected', async () => {
    console.warn('[BrowserManager] ⚠️ 浏览器断开连接');
    
    state.crashCount++;
    state.crashTimestamps.push(Date.now());
    
    // 清理过期的时间戳
    const windowStart = Date.now() - config.restart.crashWindowMs;
    state.crashTimestamps = state.crashTimestamps.filter(t => t > windowStart);
    
    emit('onBrowserCrash', { 
      crashCount: state.crashCount,
      recentCrashes: state.crashTimestamps.length 
    });
    
    // 检查是否超过崩溃阈值
    if (state.crashTimestamps.length > config.restart.maxCrashCount) {
      console.error('[BrowserManager] ❌ 崩溃次数过多，停止自动重启');
      state.isRunning = false;
      return;
    }
    
    // 自动重启
    if (state.isRunning) {
      console.log('[BrowserManager] 尝试自动重启...');
      try {
        await restartBrowser();
        console.log('[BrowserManager] ✅ 自动重启成功');
      } catch (error) {
        console.error('[BrowserManager] 自动重启失败:', error.message);
      }
    }
  });
  
  // 页面错误
  state.page.on('pageerror', (error) => {
    console.error('[BrowserManager] 页面错误:', error.message);
  });
  
  // 控制台消息
  state.page.on('console', (msg) => {
    if (msg.type() === 'error') {
      console.error('[BrowserManager] 控制台错误:', msg.text());
    }
  });
}

/**
 * 检查浏览器健康状态
 * @returns {Object} 健康状态
 */
function checkHealth() {
  const health = {
    isRunning: state.isRunning,
    isConnected: state.browser?.isConnected() || false,
    pageReady: state.page && !state.page.isClosed(),
    uptimeMs: state.startTime ? Date.now() - new Date(state.startTime).getTime() : 0,
    lastActivity: state.lastActivityTime,
    crashCount: state.crashCount,
    restartCount: state.restartCount
  };
  
  health.healthy = health.isRunning && health.isConnected && health.pageReady;
  
  return health;
}

/**
 * 记录活动
 */
function recordActivity() {
  state.lastActivityTime = new Date().toISOString();
}

/**
 * 导航到页面
 * @param {string} url - 目标URL
 * @param {Object} options - 导航选项
 */
async function navigate(url, options = {}) {
  if (!state.page) {
    throw new Error('浏览器未启动');
  }
  
  recordActivity();
  
  try {
    await state.page.goto(url, {
      waitUntil: 'networkidle',
      timeout: 30000,
      ...options
    });
    
    emit('onPageReady', { url, state });
    
  } catch (error) {
    console.error('[BrowserManager] 导航失败:', error.message);
    throw error;
  }
}

/**
 * 获取当前页面
 */
function getPage() {
  return state.page;
}

/**
 * 获取状态
 */
function getState() {
  return { ...state };
}

/**
 * 添加事件监听器
 */
function on(event, callback) {
  if (listeners[event]) {
    listeners[event].push(callback);
  }
}

/**
 * 移除事件监听器
 */
function off(event, callback) {
  if (listeners[event]) {
    const index = listeners[event].indexOf(callback);
    if (index > -1) {
      listeners[event].splice(index, 1);
    }
  }
}

/**
 * 触发事件
 */
function emit(event, data) {
  if (listeners[event]) {
    listeners[event].forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`[BrowserManager] 事件处理错误 (${event}):`, error.message);
      }
    });
  }
}

/**
 * 保存登录状态
 * @param {string} filePath - 保存路径
 */
async function saveSession(filePath) {
  if (!state.context) {
    throw new Error('上下文不存在');
  }
  
  const savePath = filePath || path.join(config.userDataDir, 'auth-state.json');
  await state.context.storageState({ path: savePath });
  console.log('[BrowserManager] 登录状态已保存');
}

/**
 * 加载登录状态
 * @param {string} filePath - 文件路径
 */
async function loadSession(filePath) {
  const loadPath = filePath || path.join(config.userDataDir, 'auth-state.json');
  
  if (!fs.existsSync(loadPath)) {
    console.log('[BrowserManager] 没有保存的登录状态');
    return false;
  }
  
  try {
    const state = JSON.parse(fs.readFileSync(loadPath, 'utf-8'));
    return state;
  } catch (error) {
    console.error('[BrowserManager] 加载登录状态失败:', error.message);
    return false;
  }
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  startBrowser,
  stopBrowser,
  restartBrowser,
  checkHealth,
  recordActivity,
  navigate,
  getPage,
  getState,
  on,
  off,
  saveSession,
  loadSession,
  config
};
