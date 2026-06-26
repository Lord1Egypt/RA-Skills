#!/usr/bin/env node
/**
 * XHS Login Tool
 * Used for first-time login and saving cookies
 */

import { getBrowser, closeBrowser } from './browser.js';
import readline from 'readline';

async function login() {
  console.log('='.repeat(60));
  console.log('  小红书登录工具');
  console.log('='.repeat(60));
  console.log('');

  const browser = await getBrowser({ headless: false });
  const page = await browser.getPage();

  try {
    // 访问小红书首页
    console.log('正在打开小红书首页...');
    await page.goto('https://www.xiaohongshu.com', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });

    console.log('');
    console.log('请在浏览器中完成登录操作：');
    console.log('1. 点击页面右上角的"登录"按钮');
    console.log('2. 使用手机 APP 扫码登录');
    console.log('3. 登录成功后，返回此处按回车键继续');
    console.log('');

    // 等待用户输入
    await waitForEnter('登录完成后按回车键继续...');

    // 验证登录状态
    console.log('');
    console.log('正在验证登录状态...');

    await page.goto('https://creator.xiaohongshu.com/publish/publish', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });

    await page.waitForTimeout(2000);

    const currentUrl = page.url();
    if (currentUrl.includes('login')) {
      console.error('❌ 登录验证失败：未检测到登录状态');
      console.log('请重新运行此工具并完成登录');
      return false;
    }

    // 保存 cookies
    await browser.saveCookies();

    console.log('');
    console.log('✅ 登录成功！');
    console.log('✅ Cookies 已保存');
    console.log('');
    console.log('现在可以启动 MCP 服务了：');
    console.log('  npm start');
    console.log('');

    return true;
  } catch (error) {
    console.error('❌ 登录过程出错:', error.message);
    return false;
  } finally {
    await closeBrowser();
  }
}

/**
 * 等待用户按回车键
 */
function waitForEnter(prompt) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(prompt, () => {
      rl.close();
      resolve();
    });
  });
}

// 运行登录
login()
  .then((success) => {
    process.exit(success ? 0 : 1);
  })
  .catch((error) => {
    console.error('登录失败:', error);
    process.exit(1);
  });
