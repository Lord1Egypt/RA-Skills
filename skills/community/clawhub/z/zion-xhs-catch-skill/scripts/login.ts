/**
 * 小红书登录脚本
 * 首次运行会弹出浏览器，用户扫码登录后保存 Cookie 到 cookies.json
 * 用法: npx ts-node scripts/login.ts
 */

import { chromium, BrowserContext } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const COOKIE_FILE = path.resolve(process.cwd(), 'cookies.json');
const XHS_HOME = 'https://www.xiaohongshu.com';

async function login() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });

  const page = await context.newPage();
  await page.goto(XHS_HOME, { waitUntil: 'networkidle' });

  console.log('请在浏览器中扫码登录小红书...');
  console.log('登录成功后，按回车键保存 Cookie（或等待 60 秒后自动检测）');

  // 等待用户登录完成：检测页面是否出现用户头像或退出登录按钮
  let loggedIn = false;
  const checkInterval = setInterval(async () => {
    try {
      // 小红书登录后通常会出现头像或特定元素
      const avatar = await page.locator('img.avatar, .avatar-img, [class*="avatar"]').first();
      if (await avatar.isVisible().catch(() => false)) {
        loggedIn = true;
        clearInterval(checkInterval);
        await saveCookies(context);
        console.log('检测到登录状态，Cookie 已保存到 cookies.json');
        await browser.close();
        process.exit(0);
      }
    } catch {
      // 忽略检查过程中的错误
    }
  }, 3000);

  // 60 秒超时
  setTimeout(async () => {
    if (!loggedIn) {
      clearInterval(checkInterval);
      await saveCookies(context);
      console.log('超时，已保存当前 Cookie（可能未登录成功）');
      await browser.close();
      process.exit(1);
    }
  }, 60000);

  // 也支持按回车保存
  process.stdin.once('data', async () => {
    clearInterval(checkInterval);
    await saveCookies(context);
    console.log('Cookie 已保存到 cookies.json');
    await browser.close();
    process.exit(0);
  });
}

async function saveCookies(context: BrowserContext) {
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIE_FILE, JSON.stringify(cookies, null, 2));
}

login().catch((err) => {
  console.error('登录失败:', err);
  process.exit(1);
});
