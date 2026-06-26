const fs = require('fs');
const path = require('path');
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (e) {
  console.error('\n[Error] Playwright is not installed. Please run "npm install playwright" and "npx playwright install chromium" first.');
  process.exit(1);
}


const cwd = __dirname;
const artifactsDir = path.resolve(cwd, 'verification-artifacts');
const statePath = path.resolve(artifactsDir, 'taobao-storage-state.json');

// Reusing login check logic from verify-taobao-runner.js
async function verifyTaobaoLogin(page, context) {
  const cookies = await context.cookies('https://www.taobao.com').catch(() => []);
  const nickCookieNames = ['_nk_', 'tracknick', 'lgc', 'uc1', 'unb', 'sn'];

  let cookieNick = null;
  let hasSessionCookie = false;

  for (const c of cookies) {
    const name = c.name.toLowerCase();
    const value = (c.value || '').trim().toLowerCase();
    
    if (nickCookieNames.includes(name) && value && !['deleted', 'null', 'undefined'].includes(value)) {
      cookieNick = c.value;
    }
    if (['_tb_token_', 'cookie2', 't'].includes(name) && value) {
      hasSessionCookie = true;
    }
  }

  const nickSelectors = [
    '.site-nav-login-info-nick',
    '.member-nick-info',
    '.J_UserNick',
    '.nick',
    '.name',
    '.site-nav-user',
    '#J_SiteNavMyTaobao'
  ];

  let pageNick = null;
  for (const selector of nickSelectors) {
    const node = page.locator(selector).first();
    const visible = await node.isVisible({ timeout: 1000 }).catch(() => false);
    if (!visible) continue;

    const text = ((await node.textContent().catch(() => null)) || '').trim();
    // If text contains '登录', it's likely a login button, not a nickname
    if (text && !/登录|注册/.test(text)) {
      pageNick = text;
      break;
    }
  }

  const loginPromptSelectors = [
    "text=亲，请登录",
    ".member-logout .login-guide-title",
    "a:has-text('立即登录')",
    ".login-btn"
  ];
  let loginPromptVisible = false;
  for (const selector of loginPromptSelectors) {
    if (await page.locator(selector).first().isVisible({ timeout: 800 }).catch(() => false)) {
      loginPromptVisible = true;
      break;
    }
  }

  // Robust check: 
  // 1. If we have a nickname on page, it's definitely logged in.
  // 2. If we have nick cookie AND session cookies (like _tb_token_), it's likely logged in.
  // 3. We only consider 'not logged in' if there's no nick AND a login prompt is visible.
  const isLoggedIn = Boolean(pageNick) || (Boolean(cookieNick) && hasSessionCookie);

  return {
    isLoggedIn,
    cookieNick,
    pageNick,
    hasSessionCookie,
    loginPromptVisible,
    debug: {
      hasNick: Boolean(pageNick || cookieNick),
      hasSession: hasSessionCookie
    }
  };
}

async function runAutoLogin() {
  fs.mkdirSync(artifactsDir, { recursive: true });
  const userDataDir = path.resolve(cwd, '.pw-user-data-taobao');
  fs.mkdirSync(userDataDir, { recursive: true });

  console.log('正在打开淘宝登录页面...');
  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    viewport: { width: 1440, height: 900 },
    locale: 'zh-CN'
  });

  const page = context.pages().length > 0 ? context.pages()[0] : await context.newPage();
  await page.goto('https://www.taobao.com', { waitUntil: 'domcontentloaded', timeout: 90000 });

  console.log('请在浏览器窗口完成登录。系统将自动检测登录状态，并在成功后保存。');
  console.log('超时时间为 10 分钟。');

  const timeoutMs = 10 * 60 * 1000;
  const startTime = Date.now();
  let loggedIn = false;

  while (Date.now() - startTime < timeoutMs) {
    try {
      const status = await verifyTaobaoLogin(page, context);
      if (status.isLoggedIn) {
        console.log(`\n检测到已登录！用户: ${status.pageNick || status.cookieNick || '未知'}`);
        loggedIn = true;
        break;
      }
      if (Date.now() % 10000 < 3000) {
        process.stdout.write(` [状态: nick=${status.pageNick || status.cookieNick || '无'}, prompt=${status.loginPromptVisible}] `);
      } else {
        process.stdout.write('.');
      }
      await page.waitForTimeout(3000);
    } catch (e) {
      if (e.message.includes('closed')) {
        console.log('\n[提示] 登录窗口已被关闭。');
        break;
      }
      throw e;
    }
  }

  if (loggedIn) {
    await context.storageState({ path: statePath });
    console.log(`\n登录成功！已保存登录态到: ${statePath}`);
    await context.close();
    return true;
  } else {
    console.log('\n登录超时，未检测到成功登录状态。');
    await context.close();
    return false;
  }
}

module.exports = { runAutoLogin, verifyTaobaoLogin };

if (require.main === module) {
  runAutoLogin()
    .then((success) => process.exit(success ? 0 : 1))
    .catch((err) => {
      console.error('自动登录脚本运行失败:', err);
      process.exit(1);
    });
}
