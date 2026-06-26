#!/usr/bin/env node
/**
 * zhihu-export-cookie.js — 知乎 Cookie 导出工具
 *
 * 手动登录知乎后，将 Cookie 导出并加密保存。
 * 使用方式:
 *   node scripts/zhihu-export-cookie.js               # 交互式登录
 *   node scripts/zhihu-export-cookie.js --path cookies.json  # 从文件导入
 *
 * G9
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';
import { encryptAndSaveCookies } from './zhihu-core.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function interactiveLogin() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('  知乎 Cookie 导出工具');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log('即将打开浏览器，请手动登录知乎。');
  console.log('登录成功后，Cookie 将自动保存并加密。');
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: 'zh-CN',
  });

  const page = await context.newPage();

  try {
    await page.goto('https://www.zhihu.com/signin', { waitUntil: 'networkidle', timeout: 60000 });
    console.log('✅ 登录页面已打开，请扫码或账号登录...');
    console.log('⏳ 等待登录完成（超时 5 分钟）...');

    // 等待导航到首页（登录成功后自动跳转）
    await page.waitForURL('https://www.zhihu.com/', { timeout: 5 * 60 * 1000 });
    
    // 额外等待页面加载
    await page.waitForTimeout(3000);

    // 确认登录状态
    const isLoggedIn = await page.$('.AppHeader-profileAvatar');
    if (isLoggedIn) {
      const cookies = await context.cookies();
      encryptAndSaveCookies(cookies);
      console.log(`✅ 导出成功！共 ${cookies.length} 条 Cookie`);
      console.log(`   保存位置: ~/.hermes/credentials/zhihu-cookies.enc`);
    } else {
      console.log('⚠️ 未能确认登录状态，请检查是否成功登录');
    }
  } catch (err) {
    console.error('❌ Cookie 导出失败:', err.message);
  } finally {
    await browser.close();
  }
}

async function importFromFile(filePath) {
  try {
    const resolvedPath = resolve(process.cwd(), filePath);
    const data = readFileSync(resolvedPath, 'utf-8');
    const cookies = JSON.parse(data);

    if (!Array.isArray(cookies)) {
      throw new Error('Cookie 文件格式错误，应为 JSON 数组');
    }

    encryptAndSaveCookies(cookies);
    console.log(`✅ 从文件导入成功！共 ${cookies.length} 条 Cookie`);
  } catch (err) {
    console.error('❌ 导入失败:', err.message);
    console.error('   文件格式应为 Playwright cookies() 输出的 JSON 数组');
  }
}

function main() {
  const args = process.argv.slice(2);
  const pathIndex = args.indexOf('--path');

  if (pathIndex !== -1 && args[pathIndex + 1]) {
    importFromFile(args[pathIndex + 1]);
  } else {
    interactiveLogin();
  }
}

main();
