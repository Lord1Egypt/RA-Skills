/**
 * 登录状态守护器
 * 职责：检测登录状态、自动恢复登录、会话保活
 */

const config = {
  // 检查间隔（毫秒）
  checkIntervalMs: 60000, // 1分钟检查一次
  
  // 登录状态检测选择器
  loginSelectors: {
    // 已登录状态
    loggedIn: [
      '.avatar-icon',
      '.user-avatar',
      '[class*="avatar"]',
      '[class*="user-info"]'
    ],
    // 未登录状态
    notLoggedIn: [
      '.login-button',
      '[class*="login-btn"]',
      'button:has-text("登录")'
    ],
    // 登录弹窗
    loginDialog: [
      '.login-dialog',
      '.login-modal',
      '[class*="login-dialog"]',
      '[class*="login-modal"]'
    ]
  },
  
  // 保活操作间隔（毫秒）- 防止会话过期
  keepAliveIntervalMs: 5 * 60 * 1000, // 5分钟
  
  // 登录恢复最大重试次数
  maxRecoveryAttempts: 3,
  
  // 恢复间隔（毫秒）
  recoveryIntervalMs: 30000
};

// 状态存储
let state = {
  isLoggedIn: false,
  lastCheckTime: null,
  lastKeepAliveTime: null,
  recoveryAttempts: 0,
  lastError: null
};

/**
 * 检测登录状态
 * @param {Page} page - Playwright页面对象
 * @returns {Promise<{isLoggedIn: boolean, method: string}>}
 */
async function checkLoginStatus(page) {
  try {
    // 方法1：检查已登录元素
    for (const selector of config.loginSelectors.loggedIn) {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          return { isLoggedIn: true, method: 'logged_in_element' };
        }
      }
    }
    
    // 方法2：检查未登录元素
    for (const selector of config.loginSelectors.notLoggedIn) {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          return { isLoggedIn: false, method: 'not_logged_in_element' };
        }
      }
    }
    
    // 方法3：检查URL
    const url = page.url();
    if (url.includes('/login') || url.includes('/passport')) {
      return { isLoggedIn: false, method: 'url_check' };
    }
    
    // 方法4：检查localStorage中的登录信息
    const hasLoginData = await page.evaluate(() => {
      try {
        const token = localStorage.getItem('token') || 
                     localStorage.getItem('auth_token') ||
                     sessionStorage.getItem('token');
        return !!token;
      } catch {
        return false;
      }
    });
    
    if (hasLoginData) {
      return { isLoggedIn: true, method: 'storage_check' };
    }
    
    // 默认：需要进一步验证
    return { isLoggedIn: null, method: 'unknown' };
    
  } catch (error) {
    console.error('[LoginGuard] 检测登录状态失败:', error.message);
    return { isLoggedIn: null, method: 'error', error: error.message };
  }
}

/**
 * 执行保活操作
 * @param {Page} page - Playwright页面对象
 */
async function performKeepAlive(page) {
  try {
    // 方法1：页面刷新（轻量）
    // await page.reload({ waitUntil: 'networkidle' });
    
    // 方法2：触发一个小操作保持会话活跃
    await page.evaluate(() => {
      // 触发mousemove事件模拟用户活动
      document.dispatchEvent(new MouseEvent('mousemove', {
        bubbles: true,
        cancelable: true,
        clientX: Math.random() * window.innerWidth,
        clientY: Math.random() * window.innerHeight
      }));
    });
    
    state.lastKeepAliveTime = new Date().toISOString();
    console.log('[LoginGuard] 保活操作完成');
    
  } catch (error) {
    console.error('[LoginGuard] 保活操作失败:', error.message);
  }
}

/**
 * 尝试恢复登录
 * @param {Page} page - Playwright页面对象
 * @param {Object} account - 账号信息
 * @returns {Promise<{success: boolean, method: string}>}
 */
async function attemptRecovery(page, account) {
  if (state.recoveryAttempts >= config.maxRecoveryAttempts) {
    console.error('[LoginGuard] 已达到最大重试次数，放弃恢复');
    return { success: false, method: 'max_attempts_reached' };
  }
  
  state.recoveryAttempts++;
  console.log(`[LoginGuard] 尝试恢复登录 (第${state.recoveryAttempts}次)`);
  
  try {
    // 方法1：刷新页面重新加载session
    await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    const statusAfterReload = await checkLoginStatus(page);
    if (statusAfterReload.isLoggedIn) {
      state.recoveryAttempts = 0;
      console.log('[LoginGuard] 通过刷新页面恢复登录');
      return { success: true, method: 'page_reload' };
    }
    
    // 方法2：导航到主页触发登录检查
    await page.goto('https://creator.douyin.com/', { 
      waitUntil: 'networkidle', 
      timeout: 30000 
    });
    await page.waitForTimeout(2000);
    
    const statusAfterNavigate = await checkLoginStatus(page);
    if (statusAfterNavigate.isLoggedIn) {
      state.recoveryAttempts = 0;
      console.log('[LoginGuard] 通过导航恢复登录');
      return { success: true, method: 'navigate' };
    }
    
    // 方法3：如果提供了账号信息，尝试重新登录
    if (account && account.loginUrl) {
      console.log('[LoginGuard] 需要人工重新登录');
      return { success: false, method: 'manual_login_required' };
    }
    
    return { success: false, method: 'all_methods_failed' };
    
  } catch (error) {
    state.lastError = error.message;
    console.error('[LoginGuard] 恢复登录失败:', error.message);
    return { success: false, method: 'error', error: error.message };
  }
}

/**
 * 登录守护主循环
 * @param {Page} page - Playwright页面对象
 * @param {Object} options - 配置选项
 */
async function startGuardian(page, options = {}) {
  const { account, onLoginLost, onLoginRecovered } = options;
  
  console.log('[LoginGuard] 启动登录状态守护');
  
  // 初始检测
  const initialStatus = await checkLoginStatus(page);
  state.isLoggedIn = initialStatus.isLoggedIn;
  state.lastCheckTime = new Date().toISOString();
  
  console.log(`[LoginGuard] 初始状态: ${state.isLoggedIn ? '已登录' : '未登录'}`);
  
  // 定时检查
  const checkTimer = setInterval(async () => {
    try {
      const status = await checkLoginStatus(page);
      state.lastCheckTime = new Date().toISOString();
      
      // 状态变化检测
      if (state.isLoggedIn && !status.isLoggedIn) {
        console.warn('[LoginGuard] ⚠️ 检测到登录丢失！');
        state.isLoggedIn = false;
        
        // 通知回调
        if (onLoginLost) {
          onLoginLost({ status, state });
        }
        
        // 尝试恢复
        const recovery = await attemptRecovery(page, account);
        if (recovery.success) {
          state.isLoggedIn = true;
          console.log('[LoginGuard] ✅ 登录已恢复');
          
          if (onLoginRecovered) {
            onLoginRecovered({ recovery, state });
          }
        }
      } else if (!state.isLoggedIn && status.isLoggedIn) {
        console.log('[LoginGuard] ✅ 登录状态恢复');
        state.isLoggedIn = true;
        state.recoveryAttempts = 0;
      }
      
      // 保活检查
      const now = Date.now();
      const lastKeepAlive = state.lastKeepAliveTime 
        ? new Date(state.lastKeepAliveTime).getTime() 
        : 0;
      
      if (state.isLoggedIn && (now - lastKeepAlive > config.keepAliveIntervalMs)) {
        await performKeepAlive(page);
      }
      
    } catch (error) {
      console.error('[LoginGuard] 检查循环错误:', error.message);
    }
  }, config.checkIntervalMs);
  
  return {
    stop: () => {
      clearInterval(checkTimer);
      console.log('[LoginGuard] 已停止');
    },
    getState: () => ({ ...state }),
    forceCheck: async () => {
      const status = await checkLoginStatus(page);
      state.isLoggedIn = status.isLoggedIn;
      state.lastCheckTime = new Date().toISOString();
      return status;
    }
  };
}

/**
 * 获取当前状态
 */
function getState() {
  return { ...state };
}

/**
 * 重置状态
 */
function resetState() {
  state = {
    isLoggedIn: false,
    lastCheckTime: null,
    lastKeepAliveTime: null,
    recoveryAttempts: 0,
    lastError: null
  };
}

module.exports = {
  checkLoginStatus,
  performKeepAlive,
  attemptRecovery,
  startGuardian,
  getState,
  resetState,
  config
};
