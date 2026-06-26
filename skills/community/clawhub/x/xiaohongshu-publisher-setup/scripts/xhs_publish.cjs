#!/usr/bin/env node
// -*- coding: utf-8 -*-
/**
 * 小红书笔记自动化发布工具
 *
 * 基于 Playwright 浏览器自动化，封装小红书创作者中心的发布流程。
 * 依赖：npm install playwright && npx playwright install chromium
 *
 * 用法：
 *   node xhs_publish.cjs <command> [args]
 *
 * 命令：
 *   login              打开浏览器，手动扫码登录，保存 session
 *   check-login        验证当前登录状态（静默检查）
 *   publish <json路径>  从内容 JSON 文件发布笔记
 *   get-note <笔记ID>  查询笔记数据统计
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ============================================================
// 配置
// ============================================================

const WORKSPACE_DIR = path.join(os.homedir(), '.openclaw', 'workspace-xiaohongshu-publisher');
const SESSION_DIR = path.join(WORKSPACE_DIR, '.session');
const SESSION_FILE = path.join(SESSION_DIR, 'state.json');

const XHS_BASE_URL = 'https://www.xiaohongshu.com';
const XHS_CREATOR_URL = 'https://creator.xiaohongshu.com';
const XHS_PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish';

// ============================================================
// 工具函数
// ============================================================

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function loadContentJson(jsonPath) {
  if (!jsonPath || !fs.existsSync(jsonPath)) {
    console.error(`❌ 找不到内容文件：${jsonPath}`);
    console.error('   请提供有效的 content.json 路径');
    printContentJsonExample();
    process.exit(1);
  }

  let content;
  try {
    content = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  } catch (e) {
    console.error(`❌ content.json 解析失败：${e.message}`);
    process.exit(1);
  }

  const required = ['title', 'body'];
  for (const field of required) {
    if (!content[field]) {
      console.error(`❌ content.json 缺少必填字段：${field}`);
      process.exit(1);
    }
  }

  if (content.title.length > 20) {
    console.warn(`⚠️  标题超过 20 字（当前 ${content.title.length} 字），建议缩短`);
  }

  return content;
}

function printContentJsonExample() {
  console.log('\ncontent.json 格式示例：');
  const example = {
    title: '🌟 标题（含emoji，≤20字）',
    body: '正文内容（已排版，含emoji和话题标签）\n\n#话题1 #话题2 #话题3',
    tags: ['话题1', '话题2', '话题3'],
    images: ['/path/to/cover.jpg', '/path/to/img2.jpg'],
    type: 'normal',
  };
  console.log(JSON.stringify(example, null, 2));
}

async function getPlaywright() {
  try {
    return require('playwright');
  } catch (e) {
    console.error('❌ Playwright 未安装');
    console.error('   请在工作目录运行：');
    console.error('     npm install playwright');
    console.error('     npx playwright install chromium');
    process.exit(1);
  }
}

// ============================================================
// 命令实现
// ============================================================

async function cmdLogin() {
  const { chromium } = await getPlaywright();

  console.log('🌐 正在打开小红书登录页面...');
  console.log('   请在浏览器中完成扫码登录，登录成功后窗口会自动关闭');

  ensureDir(SESSION_DIR);

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(XHS_BASE_URL, { waitUntil: 'networkidle' });

  console.log('   等待登录完成...');

  // 等待登录成功（检测到用户信息相关元素或 URL 变化）
  try {
    await page.waitForFunction(
      () => {
        // 检测是否已登录（小红书登录后首页会出现用户相关元素）
        return document.cookie.includes('web_session') ||
               document.querySelector('[class*="user-info"]') ||
               document.querySelector('[class*="avatar"]');
      },
      { timeout: 120000 } // 2分钟超时
    );
  } catch (e) {
    console.log('   等待超时，请检查是否已完成登录后按 Enter 继续...');
    await new Promise(resolve => process.stdin.once('data', resolve));
  }

  // 保存 session
  await context.storageState({ path: SESSION_FILE });
  console.log(`✅ 登录成功，session 已保存至：${SESSION_FILE}`);

  await browser.close();
}

async function cmdCheckLogin() {
  if (!fs.existsSync(SESSION_FILE)) {
    console.log('❌ 未找到登录 session');
    console.log('   请先运行：node xhs_publish.cjs login');
    process.exit(1);
  }

  const { chromium } = await getPlaywright();

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: SESSION_FILE,
  });
  const page = await context.newPage();

  try {
    await page.goto(XHS_CREATOR_URL, { waitUntil: 'networkidle', timeout: 30000 });

    const currentUrl = page.url();

    // 如果被重定向到登录页，说明 session 已失效
    if (currentUrl.includes('login') || currentUrl.includes('signin')) {
      console.log('❌ 登录已过期，请重新登录');
      console.log('   运行：node xhs_publish.cjs login');
      await browser.close();
      process.exit(1);
    }

    console.log('✅ 登录状态有效');
    console.log(`   当前页面：${currentUrl}`);
  } catch (e) {
    console.error(`❌ 检查登录状态失败：${e.message}`);
    await browser.close();
    process.exit(1);
  }

  await browser.close();
}

async function cmdPublish(jsonPath) {
  const content = loadContentJson(jsonPath);
  const { chromium } = await getPlaywright();

  if (!fs.existsSync(SESSION_FILE)) {
    console.error('❌ 未找到登录 session，请先运行 login 命令');
    process.exit(1);
  }

  // 验证图片文件存在
  if (content.images && content.images.length > 0) {
    for (const imgPath of content.images) {
      if (!fs.existsSync(imgPath)) {
        console.error(`❌ 图片文件不存在：${imgPath}`);
        process.exit(1);
      }
    }
  }

  console.log('🚀 准备发布小红书笔记...');
  console.log(`   标题：${content.title}`);
  console.log(`   图片：${(content.images || []).length} 张`);
  console.log(`   话题：${(content.tags || []).join(' ')}`);

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    storageState: SESSION_FILE,
  });
  const page = await context.newPage();

  try {
    // 导航到发布页面
    console.log('   打开发布页面...');
    await page.goto(XHS_PUBLISH_URL, { waitUntil: 'networkidle', timeout: 30000 });

    // 检查是否被重定向到登录页
    if (page.url().includes('login') || page.url().includes('signin')) {
      console.error('❌ 登录已过期，请重新运行 login 命令');
      await browser.close();
      process.exit(1);
    }

    // 上传图片（如有）
    if (content.images && content.images.length > 0) {
      console.log(`   上传图片（${content.images.length} 张）...`);

      // 等待文件上传按钮出现
      const fileInput = await page.waitForSelector('input[type="file"]', { timeout: 15000 });

      // 上传所有图片
      await fileInput.setInputFiles(content.images);

      // 等待图片上传完成（等待加载指示器消失）
      await page.waitForTimeout(3000);
      console.log('   图片上传完成');
    }

    // 填写标题
    console.log('   填写标题...');
    const titleInput = await page.waitForSelector(
      '[placeholder*="标题"], input[class*="title"], textarea[class*="title"]',
      { timeout: 15000 }
    );
    await titleInput.click();
    await titleInput.fill(content.title);

    // 填写正文
    console.log('   填写正文...');
    const bodyInput = await page.waitForSelector(
      '[placeholder*="正文"], [placeholder*="描述"], textarea[class*="content"], div[contenteditable="true"]',
      { timeout: 15000 }
    );
    await bodyInput.click();
    await bodyInput.fill(content.body);

    // 等待一下，确保内容填写完成
    await page.waitForTimeout(1500);

    // 截图供用户确认
    const screenshotPath = path.join(WORKSPACE_DIR, 'publish_preview.png');
    await page.screenshot({ path: screenshotPath, fullPage: false });
    console.log(`\n📸 发布预览截图已保存：${screenshotPath}`);
    console.log('   请检查截图确认内容无误\n');

    // 提示用户确认
    console.log('⚠️  即将提交发布，请在浏览器中确认内容后按 Enter 继续...');
    console.log('   （如需修改，请直接在浏览器中调整，调整完毕后按 Enter）');
    await new Promise(resolve => process.stdin.once('data', resolve));

    // 点击发布按钮
    console.log('   提交发布...');
    const publishBtn = await page.waitForSelector(
      'button:has-text("发布"), [class*="publish-btn"], [class*="submit"]',
      { timeout: 10000 }
    );
    await publishBtn.click();

    // 等待发布完成
    await page.waitForTimeout(3000);

    const finalUrl = page.url();
    console.log('\n✅ 发布操作已完成');
    console.log(`   当前页面：${finalUrl}`);
    console.log('   请在小红书创作者中心确认笔记状态');
    console.log(`   创作者中心：${XHS_CREATOR_URL}`);

    // 保存发布记录
    const record = {
      title: content.title,
      publishedAt: new Date().toISOString(),
      finalUrl: finalUrl,
      tags: content.tags || [],
    };
    const recordPath = path.join(WORKSPACE_DIR, `published_${Date.now()}.json`);
    fs.writeFileSync(recordPath, JSON.stringify(record, null, 2), 'utf-8');
    console.log(`   发布记录已保存：${recordPath}`);

  } catch (e) {
    console.error(`❌ 发布过程出错：${e.message}`);
    console.error('   请在浏览器中手动完成发布，或检查页面结构是否变化');

    const errorScreenshot = path.join(WORKSPACE_DIR, 'publish_error.png');
    try {
      await page.screenshot({ path: errorScreenshot });
      console.error(`   错误截图：${errorScreenshot}`);
    } catch (_) {}

    await browser.close();
    process.exit(1);
  }

  await browser.close();
}

async function cmdGetNote(noteId) {
  if (!noteId) {
    console.log('用法：node xhs_publish.cjs get-note <笔记ID>');
    console.log('   笔记ID 可在小红书创作者中心的笔记管理页面找到');
    process.exit(1);
  }

  const { chromium } = await getPlaywright();

  if (!fs.existsSync(SESSION_FILE)) {
    console.error('❌ 未找到登录 session，请先运行 login 命令');
    process.exit(1);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: SESSION_FILE,
  });
  const page = await context.newPage();

  try {
    // 导航到创作者中心数据页面
    const dataUrl = `${XHS_CREATOR_URL}/data/note`;
    await page.goto(dataUrl, { waitUntil: 'networkidle', timeout: 30000 });

    if (page.url().includes('login')) {
      console.error('❌ 登录已过期，请重新运行 login 命令');
      await browser.close();
      process.exit(1);
    }

    // 截图返回给用户手动查看（数据页面结构复杂，截图更可靠）
    const screenshotPath = path.join(WORKSPACE_DIR, `note_data_${noteId}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });

    console.log(`📊 笔记数据页面截图已保存：${screenshotPath}`);
    console.log(`   请在截图中查看笔记 ${noteId} 的数据`);
    console.log(`   也可直接访问：${dataUrl}`);

  } catch (e) {
    console.error(`❌ 获取笔记数据失败：${e.message}`);
    await browser.close();
    process.exit(1);
  }

  await browser.close();
}

function printUsage() {
  console.log('小红书笔记自动化发布工具');
  console.log();
  console.log('用法：node xhs_publish.cjs <command> [args]');
  console.log();
  console.log('命令：');
  console.log('  login              打开浏览器，手动扫码登录，保存 session');
  console.log('  check-login        验证当前登录状态');
  console.log('  publish <json路径>  从内容 JSON 文件发布笔记');
  console.log('  get-note <笔记ID>  查询笔记数据（通过创作者中心截图）');
  console.log();
  console.log('首次使用前请确保已安装依赖：');
  console.log('  npm install playwright');
  console.log('  npx playwright install chromium');
  console.log();
  printContentJsonExample();
}

// ============================================================
// 主入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printUsage();
    process.exit(0);
  }

  const command = args[0];

  const commands = {
    'login': () => cmdLogin(),
    'check-login': () => cmdCheckLogin(),
    'publish': () => cmdPublish(args[1] || null),
    'get-note': () => cmdGetNote(args[1] || null),
  };

  if (commands[command]) {
    await commands[command]();
  } else {
    console.error(`❌ 未知命令：${command}`);
    console.log();
    printUsage();
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(`❌ 未预期的错误：${e.message}`);
  if (process.env.DEBUG) {
    console.error(e.stack);
  }
  process.exit(1);
});
