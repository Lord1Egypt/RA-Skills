#!/usr/bin/env node
/**
 * 闲鱼数据抓取脚本
 * 使用 Playwright + OCR 技术
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG_PATH = path.join(__dirname, '../../.xianyu-grabber-config.json');
const DEFAULT_CONFIG = {
  gitee: { token: '', owner: '', repo: '' },
  xianyu: { cookie: '' },
  grabber: {
    keywords: ['Magisk', 'KernelSU', '手机维修'],
    screenshotDir: 'legion/screenshots',
    dataDir: 'legion/data',
    uploadToGitee: true,
    ocrLanguage: 'chi_sim+eng'
  }
};

// 加载配置
function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  return DEFAULT_CONFIG;
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const config = loadConfig();
  
  console.log('🐾 闲鱼数据抓取工具 v1.0.0\n');
  
  // 确保目录存在
  const screenshotDir = path.join(__dirname, '../../', config.grabber.screenshotDir);
  const dataDir = path.join(__dirname, '../../', config.grabber.dataDir);
  fs.mkdirSync(screenshotDir, { recursive: true });
  fs.mkdirSync(dataDir, { recursive: true });
  
  // 启动浏览器
  console.log('🚀 启动浏览器...');
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1920,1080'
    ]
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });
  
  const page = await context.newPage();
  
  // 注入伪装脚本
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [{ name: 'Chrome PDF Plugin' }] });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
  });
  
  // 加载 Cookie
  if (config.xianyu.cookie) {
    const cookies = config.xianyu.cookie.split(';').map(c => {
      const [name, value] = c.trim().split('=');
      return { name: name.trim(), value: value.trim(), domain: '.goofish.com', path: '/' };
    });
    await context.addCookies(cookies);
    console.log('✅ Cookie 已加载');
  }
  
  // 确定关键词
  let keywords = config.grabber.keywords;
  if (args.length > 0 && !args.includes('--config')) {
    keywords = args.filter(a => !a.startsWith('--'));
  }
  
  console.log(`📋 关键词：${keywords.join(', ')}\n`);
  
  // 抓取数据
  const allResults = [];
  
  for (let i = 0; i < keywords.length; i++) {
    const keyword = keywords[i];
    console.log(`[${i+1}/${keywords.length}] 搜索：${keyword}`);
    
    try {
      // 访问首页再搜索
      await page.goto('https://www.goofish.com/', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);
      
      const searchInput = await page.$('input[placeholder*="搜索"], input[type="text"]');
      if (searchInput) {
        await searchInput.fill(keyword);
        await searchInput.press('Enter');
        await page.waitForTimeout(4000);
      } else {
        await page.goto(`https://www.goofish.com/search?keyword=${encodeURIComponent(keyword)}`, {
          waitUntil: 'domcontentloaded',
          timeout: 30000
        });
        await page.waitForTimeout(3000);
      }
      
      // 截图
      const screenshotPath = path.join(screenshotDir, `xianyu-${keyword}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`  📸 截图：${screenshotPath}`);
      
      // 检查是否被拦截
      const content = await page.content();
      if (content.includes('非法访问')) {
        console.log('  ❌ 被检测到');
        continue;
      }
      
      allResults.push({ keyword, screenshot: screenshotPath });
      console.log(`  ✅ 成功`);
      
    } catch (err) {
      console.log(`  ❌ 错误：${err.message}`);
    }
    
    await page.waitForTimeout(1500);
  }
  
  await browser.close();
  
  // 保存截图列表
  const screenshotsList = path.join(dataDir, 'screenshots-list.json');
  fs.writeFileSync(screenshotsList, JSON.stringify(allResults, null, 2));
  console.log(`\n📸 共保存 ${allResults.length} 张截图`);
  
  // 调用 OCR
  console.log('\n🔍 开始 OCR 识别...\n');
  
  const ocrResults = [];
  const pythonScript = path.join(__dirname, 'ocr.py');
  
  for (const item of allResults) {
    try {
      const output = execSync(
        `python3 ${pythonScript} "${item.screenshot}"`,
        { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
      );
      
      const products = output.split('\n').map(l => l.trim()).filter(l => l);
      ocrResults.push({
        keyword: item.keyword,
        products: products.slice(0, 30)
      });
      
      console.log(`  ${item.keyword}: ${products.length} 个商品`);
      
    } catch (err) {
      console.log(`  ${item.keyword}: OCR 失败`);
    }
  }
  
  // 保存完整数据
  const fullDataPath = path.join(dataDir, 'xianyu-full-data.json');
  fs.writeFileSync(fullDataPath, JSON.stringify(ocrResults, null, 2));
  console.log(`\n💾 数据已保存：${fullDataPath}`);
  
  // 生成汇总报告
  const reportPath = path.join(dataDir, 'xianyu-summary.md');
  let report = '# 🐾 闲鱼数据调研报告\n\n';
  report += `**生成时间**: ${new Date().toISOString()}\n`;
  report += `**关键词数量**: ${ocrResults.length}\n\n`;
  
  let totalProducts = 0;
  for (const result of ocrResults) {
    totalProducts += result.products.length;
    report += `## ${result.keyword}\n\n`;
    if (result.products.length > 0) {
      report += '| 商品信息 |\n|----------|\n';
      result.products.forEach(p => {
        report += `| ${p} |\n`;
      });
    } else {
      report += '⚠️ 未识别到商品\n';
    }
    report += '\n';
  }
  
  report += `## 汇总\n\n`;
  report += `- 总关键词：${ocrResults.length} 个\n`;
  report += `- 总商品：${totalProducts} 个\n`;
  report += `- 平均每个关键词：${Math.round(totalProducts / ocrResults.length)} 个商品\n`;
  
  fs.writeFileSync(reportPath, report);
  console.log(`📄 报告：${reportPath}`);
  
  // 上传到 Gitee
  if (config.grabber.uploadToGitee && config.gitee.token) {
    console.log('\n🚀 上传到 Gitee...');
    const uploaderScript = path.join(__dirname, 'uploader.sh');
    try {
      execSync(`bash ${uploaderScript} "${dataDir}" "${reportPath}"`, { stdio: 'inherit' });
      console.log('✅ 上传完成');
    } catch (err) {
      console.log('⚠️ 上传失败:', err.message);
    }
  }
  
  console.log('\n👋 完成');
}

main().catch(console.error);
