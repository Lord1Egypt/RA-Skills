/**
 * 微信读书扫码登录脚本
 * 
 * 用法：
 *   node scripts/login.js
 * 
 * 流程：
 * 1. 检查是否有已保存的 cookies
 * 2. 如有，验证 cookies 是否有效（访问书架页）
 * 3. 如无效或无 cookies，打开登录页面
 * 4. 点击「登录」按钮弹出微信二维码
 * 5. 截取二维码图片并输出路径
 * 6. 轮询检测登录状态（每 2 秒）
 * 7. 登录成功后保存 cookies
 * 8. 输出登录成功状态
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = __dirname;
const SKILL_DIR = path.resolve(SCRIPTS_DIR, '..');
const PROFILE_DIR = path.join(SKILL_DIR, 'profile');
const COOKIES_FILE = path.join(PROFILE_DIR, 'weread-cookies.json');
const QR_CODE_FILE = path.join(SCRIPTS_DIR, 'login-qrcode.png');

// 确保 profile 目录存在
if (!fs.existsSync(PROFILE_DIR)) {
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
}

/**
 * 检查 cookies 是否有效（能访问书架页）
 */
async function checkCookies(page) {
  try {
    await page.goto('https://weread.qq.com/web/shelf', {
      waitUntil: 'networkidle',
      timeout: 15000,
    });
    const bodyText = await page.evaluate(() => document.body.innerText);
    // 登录成功后书架页会显示书架内容，未登录会跳转/显示登录相关文字
    const loggedIn = !bodyText.includes('登录') || page.url().includes('/web/shelf');
    return loggedIn;
  } catch (e) {
    return false;
  }
}

/**
 * 保存 cookies 到文件
 */
async function saveCookies(context) {
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2), 'utf-8');
  console.log(`[weread] Cookies 已保存: ${COOKIES_FILE}`);
}

/**
 * 加载 cookies 到 browser context
 */
async function loadCookies(context) {
  if (fs.existsSync(COOKIES_FILE)) {
    const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));
    await context.addCookies(cookies);
    console.log(`[weread] 已加载 Cookies: ${COOKIES_FILE}`);
    return true;
  }
  return false;
}

async function login() {
  console.log('[weread] 正在启动浏览器...');

  const browser = await chromium.launch({
    headless: true,
  });

  try {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      locale: 'zh-CN',
    });

    const page = await context.newPage();

    // === 第一步：尝试复用已有 cookies ===
    const hasCookies = await loadCookies(context);
    if (hasCookies) {
      console.log('[weread] 正在验证 Cookies 有效性...');
      const valid = await checkCookies(page);
      if (valid) {
        console.log('[weread] ✅ Cookies 有效，无需重新登录');
        await saveCookies(context); // 刷新 cookies
        console.log('[weread] 登录状态: success');
        return true;
      } else {
        console.log('[weread] Cookies 已过期，需要重新登录');
      }
    }

    // === 第二步：打开首页，点击登录 ===
    console.log('[weread] 正在打开微信读书首页...');
    await page.goto('https://weread.qq.com', {
      waitUntil: 'networkidle',
      timeout: 20000,
    });
    console.log('[weread] 首页加载完成');

    // 点击登录按钮
    console.log('[weread] 正在点击登录按钮...');
    const loginBtn = page.getByText('登录').first();
    await loginBtn.waitFor({ timeout: 10000 });
    await loginBtn.click();
    console.log('[weread] 已点击登录按钮');

    // === 第三步：等待 iframe 加载完成并获取二维码 ===
    // 等待 iframe 加载
    await page.waitForTimeout(3000);

    // 找到微信登录的 iframe
    const loginFrame = page.frames().find(f => f.url().includes('open.weixin.qq.com/connect/qrconnect'));
    if (!loginFrame) {
      throw new Error('未找到微信登录 iframe');
    }

    // 等待 iframe 加载完成
    await page.waitForTimeout(3000);

    // 等待 iframe 加载完成
    await page.waitForTimeout(3000);

    // 从 iframe 中获取二维码图片的 URL
    const qrCodeUrl = await loginFrame.evaluate(() => {
      const img = document.querySelector('.js_qrcode_img');
      return img ? img.getAttribute('src') : null;
    });

    if (!qrCodeUrl) {
      throw new Error('未找到二维码图片 URL');
    }

    const fullQrUrl = qrCodeUrl.startsWith('http') ? qrCodeUrl : `https://open.weixin.qq.com${qrCodeUrl}`;
    console.log(`[weread] 二维码 URL: ${fullQrUrl}`);

    // 直接下载二维码图片
    const { execSync } = require('child_process');
    execSync(`curl -sL "${fullQrUrl}" -o "${QR_CODE_FILE}"`, { timeout: 10000 });
    console.log(`[weread] 二维码已保存: ${QR_CODE_FILE}`);

    console.log(`[weread] 📱 请用微信扫描二维码登录`);
    console.log(`[weread]    二维码图片: ${QR_CODE_FILE}`);

    // === 第四步：轮询检测登录状态 ===
    console.log('[weread] 等待扫码登录...');
    let loggedIn = false;
    const maxWaitMs = 5 * 60 * 1000; // 最长等待 5 分钟
    const pollIntervalMs = 2000; // 每 2 秒检测一次
    let waitedMs = 0;

    while (!loggedIn && waitedMs < maxWaitMs) {
      await page.waitForTimeout(pollIntervalMs);
      waitedMs += pollIntervalMs;

      try {
        // 检测登录成功标志：
        // 1. URL 变为书架页
        // 2. 页面出现用户相关元素（头像、昵称等）
        loggedIn = await page.evaluate(() => {
          // 登录弹窗消失 — 通常登录成功后弹窗会关闭
          const modal = document.querySelector('.wr_login_modal_wrapper');
          const modalGone = !modal || modal.style.display === 'none';

          // URL 变为书架（登录成功后的正常页面）
          const onShelf = window.location.href.includes('/web/shelf');

          // 出现用户菜单/头像（登录后页面头部会变化）
          const userAvatar = document.querySelector('.wr_header_user');
          const userMenu = document.querySelector('[class*="user"]');

          return onShelf || modalGone || !!userAvatar || !!userMenu;
        });
      } catch (e) {
        // 页面可能跳转了，继续检测
      }

      if (waitedMs % 10000 === 0) {
        console.log(`[weread] 等待登录中... (已等待 ${Math.round(waitedMs / 1000)} 秒)`);
      }
    }

    // === 第五步：处理登录结果 ===
    if (loggedIn) {
      console.log('[weread] ✅ 扫码登录成功！');
      // 等待页面稳定
      await page.waitForTimeout(2000);
      await saveCookies(context);
      console.log('[weread] 登录状态: success');
      return true;
    } else {
      console.log('[weread] ❌ 扫码登录超时（5分钟未扫码）');
      console.log('[weread] 登录状态: timeout');
      return false;
    }
  } finally {
    await browser.close();
    console.log('[weread] 浏览器已关闭');
  }
}

// 运行
login()
  .then((success) => {
    process.exit(success ? 0 : 1);
  })
  .catch((err) => {
    console.error('[weread] 登录出错:', err.message);
    process.exit(1);
  });
